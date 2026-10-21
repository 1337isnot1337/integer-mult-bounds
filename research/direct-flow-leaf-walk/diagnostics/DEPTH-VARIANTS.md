# Diagnostic: forcing a shallower lockstep depth

This answers open question 1 of the README negatively, for the obvious lever. It is not registered
and not part of the verifier. Run it with `python3.12 -B depth_variants.py`.
`overlap_flow_depth.py` is the package's flow with one optional `G` override added.

| N | G0 | G | exact identity | g | κ(0.001), η = 0.99422 | source mass ≤ N/m |
| --- | --- | --- | --- | --- | --- | --- |
| 10⁵ | 4 | 4 | yes | 2.823 | 0.995257 | 0 |
| 10⁵ | 4 | 3 | yes | 3.220 | 0.994592 | 2.0·10⁻⁶ |
| 10⁵ | 4 | 2 | yes | 3.783 | 0.993648 | 0.296 |
| 2·10⁶ | 6 | 6 | yes | 3.219 | 0.994593 | 0 |
| 2·10⁶ | 6 | 5 | yes | 3.618 | 0.993927 | 1.3·10⁻¹⁰ |
| 2·10⁶ | 6 | 3 | yes | 5.022 | 0.991578 | 0.327 |

## What the table shows

- A shallower depth keeps the rank-one potential identity, and the `t*` balance, exactly. It also
  raises `g` substantially.
- But it puts sources at or below `N/m`.
- `G0 = ⌊log₅(N/m)⌋` is the only depth with every source in `(N/m, N]`.

## Open question

`G0 − 1` violates the source range only by a mass of about `10⁻⁶` to `10⁻¹⁰`, yet gains about 0.4 in
`g`. Can #4405's induction absorb a tiny low-source mass, for example through the induction hypothesis
at smaller rank? If so, a mixed-depth flow could lift the single-step ceiling. That is a question for
#4436 and #4405, and it is not claimed here.
