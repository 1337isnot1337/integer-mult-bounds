# Cross-endframe observability in the PR2979 word

**Claim: no κ improvement.** This package finds exact eligible linear forms only by pooling outputs from incomparable rank-seven terminal subspaces. It does not identify a consumer, realize a new helper, provide a complete invoice, or change the selected result.

## Result

The pinned `WORD-base` and `WORD-extra` providers from [the joint-endframes package](../rank7-joint-endframes/README.md) each have 49 observed rank-seven endpoint classes (104 registers) and 126 rank-eight classes (336 registers). An independent exact reverse-adjoint checker examines every endpoint class individually, all 1,176 pairs, and all 18,424 triples of rank-seven endpoint classes, grouped by the dimension of their join.

- No individual rank-seven or rank-eight endpoint exposes an eligible input form.
- Of 413 rank-eight pair joins, one exposes a form. The other 763 pair joins have rank nine and expose none.
- Of 2,571 rank-eight triple joins, one exposes the same form as that pair.
- Of 15,853 rank-nine triple joins, 52 expose eligible forms: 50 classes have eligible rank one and two have eligible rank two. Deduplication gives 11 scalar forms, ten of them additional. The ten additional forms span a five-dimensional space; five have six input terms and five have eight.

The rank-eight witness is

```text
-out[7] - out[232] + out[236] + out[238]
 = 1/2 * (-h224 + h227 - h229 - h231 - h232 + h233
         -h234 + h235 + h236 - h237 + h238 - h239 - h276 - h292).
```

The five independent six-term forms in the rank-nine block have these exact readouts:

| Eligible form | Terminal readout |
| --- | --- |
| `h224 + h229 - h235 + h237 - h238 + h239` | `2 out[7] - 2 out[87] - 2 out[238]` |
| `h227 - h231 + h233 + h236 - h237 - h239` | `-2 out[7] + 2 out[236] + 2 out[239]` |
| `h229 + h231 + h236 - h237 + h238 - h239` | `-2 out[7] - out[76] + out[231]` |
| `h232 + h234 - h237 - h239 + h276 + h292` | `-2 out[7] + 2 out[87] + 2 out[232] + 2 out[239]` |
| `h232 + h234 + h237 + h239 + h276 + h292` | `2 out[7] + out[76] + 2 out[232] - out[233]` |

Each equation cancels all 497 protected initial columns and every nonempty formal warp word. The five forms are independent. The ten new forms, including five additional eight-term forms, span the same five-dimensional space. Their readouts use three or four terminal registers, but the contributing rank-seven endpoints have a rank-nine join. Both provider orientations produce the same counts and coefficients.

The test follows the open boundary identified by [PR #3172](https://github.com/CrocSwap/integer-mult-bounds/pull/3172): its fixed-word obstruction covers each common endpoint separately and explicitly leaves pooling incomparable endpoints outside scope. This package tests that escape on the changed PR2979 word. It does not claim that the pooling idea itself is new or that the result generalizes beyond these two words.

## Reproduce

The checker uses only the Python standard library. From the repository root:

```sh
python3 -B research/cross-endframe-observability/verify.py
python3 scripts/research_package.py --package research/cross-endframe-observability --check-only
python3.12 scripts/research_package.py --package research/cross-endframe-observability
```

The two compressed word inputs are hash-pinned in `SOURCES.json`. `verify.py` independently reconstructs the endpoint frames and the non-target formal-polynomial maps; it does not import the predecessor producer or verifier. Its checks include the complete rank-eight/nine pair and triple census, exact canonical forms, orientation agreement, and controls that delete each register from the rank-eight witness in turn.

## What remains before κ can change

These are information identities, not a supplier. The ten additional forms give a five-dimensional opportunity for a changed helper interface. A caller must accept this block; the circuit must deliver it through a real multi-register contract; and the full synthesis, observation, storage, restoration, physical and recursive costs must be charged. In particular, every witness found for the ten new forms uses a rank-nine join, so treating their rank-seven sources as a free common endpoint would be incorrect.

The current selected κ is still 0.001672660197076918. The conditional 0.0017290339826465… claim in the predecessor package is not selected, and this result does not exceed it.

## Open next questions

Can a downstream caller consume the five-dimensional readout block directly without materializing a new rank-nine register? First match the five independent six-term forms to one real caller, derive the input basis change and dirty-state restoration, then price the shared observation and full recursive profile. The blocker is that no current caller accepts these forms or supplies the complete rank-nine transfer cost.

## Credit

This scoped follow-up uses the two PR2979 word providers and preserves their attribution in the predecessor package. Ross Richardson's PR #3172 explicitly identifies incomparable-endpoint pooling as outside its theorem. New analysis and checker prepared by OpenAI Codex with substantial AI assistance; no independent human or formal-kernel review is claimed. Apache-2.0.
