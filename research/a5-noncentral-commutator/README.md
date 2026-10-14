# Eight-call minimum for a noncentral A5 commutator pair

## Result

In the exact two-role model below, `diag([c],[c^-1])` has minimum paid-call cost eight. The 24-call alphabet has no word of length at most seven. The direct eight-call word applies `abAB` on the first role and `baBA` on the second, where uppercase letters denote inverse generators. This is a scoped exact finite result in `F2[A5]`.

Let `A5` act on five points, with `a=(1 2 3 4 5)`, `b=(1 2 3)`, and `c=aba^-1b^-1`. Then `|A5|=60`; `c` has order three, is noncentral (`ca != ac`), and both `c` and `c^-1` have shortest generator length four in `{a,a^-1,b,b^-1}`. Each paid call is

```text
F(N,g) = I + ([g] + 1)N
```

where `N` is one of the six rank-one idempotents in `M2(F2)`, and `g` is one of those four generator labels. Both scalar roles contain arbitrary dirty data. Every generator factor costs one call. No other address labels, clean roles, or extra registers occur in this model.

Free scalar `GL2(F2)` mixing is included. Moving any free scalar map through a paid factor conjugates `N` and preserves the six-projector set. Under augmentation `[g] -> 1`, every paid factor becomes `I`, while the target augments to `I`; therefore the net free scalar map must be `I`. The verifier checks conjugation closure for all six scalar basis changes and both inverse products for each paid call.

## Exact search

The verifier stores each element of `F2[A5]` as a 60-bit coefficient vector and each two-role map as a complete 2x2 matrix of such vectors. It constructs the radius-three prefix ball, retaining a shortest word for each matrix, then tests every ordered suffix word of length zero through four by multiplying the target by the exact suffix inverse. Any word of length at most seven splits into a prefix of length at most three and a suffix of length at most four. The finite search therefore covers every candidate in the claimed domain.

The certificate records 6,476 distinct prefix states, 346,201 suffix words, and zero prefix/suffix matches. It also records the direct eight-call witness. A one-role target `diag([c],1)` is absent from the prefix ball, as expected from the generator-word length of `c`; this is the negative control. The six projectors are also recovered by exhaustive enumeration of all 16 binary 2x2 matrices. The ring product is checked on all 3,600 basis pairs and 32 dense masks against a separate slow convolution. Projector idempotence, invertibility of all calls, the `A5` order, the commutator order and noncentrality are checked exactly.

## Reproduction and scope

```sh
python3 -I -B research/a5-noncentral-commutator/verify.py
python3 scripts/research_package.py --package research/a5-noncentral-commutator --check-only
```

The first command regenerates `CERTIFICATE.json`. The repository's generic registered replay requires Python 3.12; only Python 3.14.7 is installed in this session, so the second command validates package metadata and source pins without launching the registered replay.

This result does not establish a physical bit-supplier construction, an improved conditional `kappa`, or a statement about another group, target, alphabet, or role count. The current selected result remains pinned at base `0b1cccf86e2f5132ed286a26ef0a681a495740ea`, record SHA-256 `10b9e340fd8e354a37a0c4813c90e5de1dd42044b5f6aca4a3fc5a42b685fa32`, with conditional `kappa = 836330098538459/500000000000000000` (decimal `0.001672660197076918`). Its reviewed source record points to `docs/research/community-batch1099-review.md`, source manifest `research/community-frontier1094-audit/SELECTED-SOURCE.json`, certificate `research/community-frontier1094-audit/ASSEMBLY.json`, and reproduction command `make frontier1094-verify`. This A5 experiment is not an input to that selected construction.

## Predecessors and overlap

The closest finite predecessor, `research/bit-dihedral-commutator`, proves an eight-call minimum for a two-role central target over `F2[UT3(F2)]`; its active Discussion #1738 asks whether a third role helps. This package uses a different group, a noncentral commutator, and the inverse-paired target. A second cached claim in Discussion #1163 studies a two-role `F2[S5]` longest-element target. The current PR scan contained 433 fully paginated PR records; the latest complete Discussion cache contained 383 records, fetched at 08:34 UTC; PR pagination refreshed at 08:55 UTC, immediately before submission. A fresh GraphQL discussion read, claim post, and PR creation were unavailable because the GitHub API rate limit was exceeded. The contribution branch was pushed to the fork for review, but no PR was created. Exact A5 search terms returned no cached matches. The scan details and submission status are in `OVERLAP.json` and `TASK.json`.

## Open next questions

Does adding one restored dirty scalar role in this same A5 model lower the inverse-pair target cost? A saving would identify a role-sharing mechanism beyond this two-role obstruction. The first step is to enumerate the 28 rank-one idempotents in `M3(F2)`, prove the corresponding free-`GL3` normalization, and run a capped exact search to cost seven. The enlarged state space needs its own search coverage and certificate.

## Credit

The finite group-algebra costing approach is related to the retained D8 commutator package and its cited predecessors; this package supplies a distinct `A5` model and target. Prepared with substantial OpenAI Codex assistance. No independent human review is claimed.
