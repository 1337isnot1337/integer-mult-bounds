"""Changed-path matches beyond the first page and honest incomplete snapshots."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import find_overlap as overlap
sys.path.pop(0)


def page(paths, start=0):
    end = start + 100
    return {'nodes': [{'path': path} for path in paths[start:end]],
            'pageInfo': {'hasNextPage': end < len(paths), 'endCursor': str(end)}}


def fixture():
    paths = [f'research/case/{i:03d}.py' for i in range(250)]
    pull = {'number': 42, 'headRefOid': 'a' * 40, 'changedFiles': len(paths), 'files': page(paths)}
    return paths, pull


class PullFilePages(unittest.TestCase):
    def test_late_path_is_searchable_after_all_pages(self):
        paths, pull = fixture()
        calls = []
        def api(query, variables):
            calls.append(variables)
            self.assertEqual(variables['number'], 42)
            continuation = {**pull, 'files': page(paths, int(variables['cursor']))}
            return {'repository': {'pullRequest': continuation}}
        with patch.object(overlap, 'graphql', side_effect=api):
            row = overlap.pull_file_record(pull)
        self.assertEqual(row, {'number': 42, 'paths': paths, 'truncated': False})
        self.assertEqual([c['cursor'] for c in calls], ['100', '200'])
        matches = overlap.path_report([], [row], ['research/case/249.py'])
        self.assertEqual(matches[0]['matched_paths'], [paths[-1]])
        self.assertFalse(matches[0]['truncated'])

    def test_head_change_count_change_missing_page_and_repeated_cursor_fail(self):
        paths, pull = fixture()
        good = {**pull, 'files': page(paths, 100)}
        variants = []
        for key, value in [('headRefOid', 'b' * 40), ('changedFiles', 251), ('files', None)]:
            variants.append({**good, key: value})
        stuck = copy.deepcopy(good)
        stuck['files']['pageInfo']['endCursor'] = '100'
        variants.append(stuck)
        for changed in variants:
            with self.subTest(changed=changed), patch.object(overlap, 'graphql',
                    return_value={'repository': {'pullRequest': changed}}):
                with self.assertRaises(ValueError):
                    overlap.pull_file_record(pull)

    def test_unavailable_or_short_response_never_claims_complete(self):
        _, pull = fixture()
        for connection in (None, {'nodes': [{'path': 'only.py'}],
                                 'pageInfo': {'hasNextPage': False}}):
            with self.subTest(connection=connection), patch.object(overlap, 'graphql',
                    side_effect=AssertionError('unexpected request')):
                row = overlap.pull_file_record({**pull, 'files': connection})
                self.assertTrue(row['truncated'])

    def test_continuation_failure_preserves_previous_complete_cache(self):
        paths, pull = fixture()
        listing = {'repository': {'pullRequests': {'nodes': [pull],
                   'pageInfo': {'hasNextPage': False}}}}
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / 'cache.json'
            old = {'records': [{'number': 7, 'paths': ['keep.py'], 'truncated': False}],
                   'fetched_at': overlap.now(), 'complete_pagination': True}
            cache.write_text(json.dumps({'schema_version': 1, 'repository': overlap.REPO,
                                        'sources': {'pr_files': old}}), encoding='utf-8')
            with patch.object(overlap, 'graphql', side_effect=[listing, ValueError('late failure')]), \
                 patch.object(overlap, 'gh_json', return_value=[[]]), \
                 patch.object(overlap, 'fetch_discussions', return_value=[]):
                snapshot, warnings = overlap.remote_snapshot(cache, refresh=True, need_files=True)
            self.assertTrue(any('pr_files: refresh failed' in w for w in warnings))
            self.assertEqual(snapshot['sources']['pr_files'], old)
            self.assertEqual(json.loads(cache.read_text())['sources']['pr_files'], old)


if __name__ == '__main__':
    unittest.main()
