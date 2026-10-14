## Result

This package gives an exact minimum of eight paid calls for one fixed two-role target over `F2[A5]`. The full 24-call alphabet has no word of length at most seven for `diag([c],[c^-1])`, where `c=aba^-1b^-1`, `a=(1 2 3 4 5)`, and `b=(1 2 3)`. A direct eight-call word supplies the upper bound.

## Evidence

- Base commit: `0b1cccf86e2f5132ed286a26ef0a681a495740ea`
- Catalogue priority revision: 3; seed: `105bdc7c008d8e95710ae18653b8a901`
- Selected record SHA-256: `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`
- Exact search: 6,476 prefix states, all 346,201 suffix words through length four, zero matches. The split covers every word through length seven.
- Additional controls: all 3,600 group-basis products and 32 dense convolution products; all 16 binary 2x2 matrices enumerated to recover the six legal projectors; both inverse products checked for all 24 calls; direct eight-call word; one-role radius-three negative control.

Reproduce with `python3 -I -B research/a5-noncentral-commutator/verify.py`. Package source and metadata validation passed with `python3 scripts/research_package.py --package research/a5-noncentral-commutator --check-only`. Generic registered replay requires Python 3.12, which is unavailable in this session (installed Python is 3.14.7).

## Scope and limits

The result applies only to the declared `A5` alphabet and exactly two arbitrary dirty scalar roles. It does not produce a physical bit supplier, a selected-bound improvement, or a new `kappa`. The closest retained work is the two-role `UT3(F2)` central-commutator package; this package changes the group and uses a noncentral inverse-paired target. A separate `S5` two-role claim studies a longest-element target.

The final PR overlap scan fully paginated 433 open PR records at 08:55 UTC. Discussion refresh and claim posting were blocked by the GitHub GraphQL rate limit; the last complete cached discussion set had 383 records at 08:34 UTC. A local claim and overlap report are included.

Substantial OpenAI Codex assistance; no independent human review claimed.
