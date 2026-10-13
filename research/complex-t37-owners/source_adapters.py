# SPDX-License-Identifier: Apache-2.0
"""Parameterize the replication-dependent PR870 checker cardinalities for T37.

The vendored PR870 sources are read from PR890's package and pinned there.
Beyond cardinalities, the charged global prefix payload changes from 512 to
1024 bits; every place that charges it (prefix reserve, row reserve 2*payload,
bootstrap cutoff 2*(4+payload)) is edited explicitly, and the retained
PR531 invoice is still required to have been charged at 512.

The literal edit table records each before/after string and expected count.
Constants unrelated to replicas, including 144 factors per wrapper and the
scalar adapter multiplier 16, are unchanged. Source notices are preserved.
"""
import argparse
import shutil
from common import HERE, ROOT, read, require, sha, dump

T21 = ROOT/'research/complex-t21-owners'


def materialize(out):
    source = T21/'vendor/pr870'
    pins = read(T21/'VENDOR-PINS.json')['pr870']['files']
    edits = read(HERE/'data/ADAPTER-EDITS.json')
    require(not out.exists(), 'Runtime output must be new')
    (out/'code').mkdir(parents=True)
    receipt = {}
    for path in sorted((source/'code').glob('*.py')):
        relative = 'code/'+path.name
        require(sha(path) == pins[relative], 'Vendored source pin: '+relative)
        text = path.read_text()
        for before, after, count in edits.get(path.name, []):
            require(text.count(before) == count, 'Exact edit multiplicity: '+path.name+' '+before)
            text = text.replace(before, after)
        target = out/'code'/path.name
        target.write_text(text)
        receipt[path.name] = dict(source_sha256=pins[relative], output_sha256=sha(target),
                                  edits=edits.get(path.name, []))
    shutil.copytree(source/'inputs', out/'inputs')
    dump(out/'ADAPTERS.json', receipt)
    return receipt


if __name__ == '__main__':
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    materialize(parser.parse_args().out)
