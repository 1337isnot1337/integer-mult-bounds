#!/usr/bin/env python3
"""Compare package working bytes with a commit before publishing hash receipts.

This is a byte-transport preflight, not a research verifier or CI-equivalence
claim. Prepared for ywz65 with OpenAI Codex assistance. Apache-2.0.
"""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import subprocess

from research_package import canonical_relative_path, git, git_blobs, relative_file, require

ROOT = Path(__file__).resolve().parents[1]


def check(root, package, ref='HEAD'):
    require(re.fullmatch(r'research/[a-z0-9][a-z0-9-]*', package), 'package must be research/<slug>')
    manifest = json.loads(relative_file(root, package+'/VERIFY.json').read_text(encoding='utf-8'))
    require(isinstance(manifest, dict), 'VERIFY.json must be an object')
    inputs = manifest.get('inputs')
    require(isinstance(inputs, list), 'declare input paths in VERIFY.json')
    for name in inputs:
        canonical_relative_path(name)
    commit = git(root, 'rev-parse', '--verify', '--end-of-options', ref+'^{commit}').decode('ascii').strip()
    # Literal pathspecs keep wildcard filenames from selecting other files.
    records = git(root, '--literal-pathspecs', 'ls-tree', '-r', '-z', '--full-tree',
                  commit, '--', package, *inputs).split(b'\0')
    entries = {}
    for record in records:
        if not record:
            continue
        header, raw_name = record.split(b'\t', 1)
        mode, kind, obj = header.split()
        name = raw_name.decode('utf-8')
        require(mode in (b'100644', b'100755') and kind == b'blob',
                'commit contains a non-regular file: '+name)
        entries[name] = obj.decode('ascii')
    # New nonignored local checkers must not disappear from the publication.
    local = git(root, '--literal-pathspecs', 'ls-files', '-c', '-o', '--exclude-standard',
                '-z', '--', package).decode('utf-8').split('\0')
    expected = {name for name in local if name} | set(inputs)
    require(set(entries) == expected, 'working/commit file inventory differs: '+
            ', '.join(sorted(set(entries) ^ expected)))
    names = sorted(entries)
    require(names, 'empty package inventory')
    with closing(git_blobs(root, [entries[name] for name in names])) as blobs:
        # Advance the blob iterator once past its last yield, so its final
        # Git exit-status check runs before reporting success.
        for (_, committed), name in zip(blobs, names):
            working = relative_file(root, name).read_bytes()
            require(working == committed,
                    'working/commit bytes differ: '+name+' (working SHA256 '+
                    hashlib.sha256(working).hexdigest()+', commit SHA256 '+
                    hashlib.sha256(committed).hexdigest()+')')
    return {'commit':commit, 'files':len(names), 'package':package}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', required=True)
    parser.add_argument('--ref', default='HEAD', help='commit to publish; default HEAD')
    args = parser.parse_args()
    try:
        result = check(ROOT, args.package, args.ref)
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        parser.exit(1, str(exc)+'\n')
    print('PASS_RESEARCH_COMMIT_BYTES '+json.dumps(result))


if __name__ == '__main__':
    main()
