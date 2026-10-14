# Validation record

Base: bce54fb3f895cbe5cd4c0eb477c3afeed100190f

Local interpreter: CPython 3.14.7. Standard library only.

| Command | Result |
|---|---|
| python3 -B scripts/research_baseline.py | PASS_RESEARCH_BASELINE_BINDINGS_ONLY; selected kappa 0.001672660197076918; complex supplier binding |
| python3 -I -B research/s3-three-transposition-restoration-seed58/verify.py | PASS_S3_THREE_TRANSPOSITION_BOUNDARY reduced_words=45 length4_relations=12 pair=103_vs79 echo=205_vs157 saved=24_and_48 workspace_vectors=729 no_new_kappa |
| python3 -I -O -B research/s3-three-transposition-restoration-seed58/verify.py | Same pass marker |
| python3 scripts/research_package.py --package research/s3-three-transposition-restoration-seed58 --check-only | PASS_PACKAGE_METADATA_AND_PINS |
| git diff --cached --check | PASS |

The full registered replay is pinned to Python 3.12 by the repository hook.
This host has Python 3.14.7 and no python3.12 executable, so that hook replay
was not run locally. The direct verifier passed under normal and optimized
Python 3.14.7, and the version-independent metadata/pin check passed. Hosted
PR checks will provide the Python 3.12 replay.

The selected supplier files and selected record are unchanged, so the full
selected cold replay, make frontier1094-verify, was not run. This package does
not claim supplier admission, native execution, a new kappa, or a complete
multiplication theorem.
