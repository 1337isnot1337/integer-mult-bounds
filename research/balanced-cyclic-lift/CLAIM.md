# Seed 55: determinant-balanced cyclic lifts

Track: recursive interfaces. Assignment seed **55**, drawn using
`secrets.randbelow(100)` from OS randomness on 2026-10-13 at 05:18 UTC.
Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`, freshly fetched `origin/main`.
Selected result: PR626 with PR543, conditional kappa
`51110230636731/31250000000000000`; it is not a target for editing here.

Three candidates considered:

1. Multiple clean checkpoints in a dirty factor chain. Not chosen: PR714,
   PR730 and PR758 already cover nearby checkpoint/tree scheduling questions.
2. Batch multiple Gaussian boundary right-hand sides. Not chosen: PR481's
   concrete Strassen construction already covers the most immediate mechanism.
3. Enlarge a stable real cyclic factor by one scalar to balance its determinant;
   implement the enlarged map by rounded integer shears and compose it in place.
   **Chosen:** this changes the leaf interface, rather than the echo tree.

Exact scope: a length-L real cyclic recurrence with position-dependent rational
coefficients of absolute value at most 1/2. One arbitrary dirty length-L array
and one arbitrary dirty scalar are borrowed. Test a reversible LU/pivot lift,
then a two-evaluation conjugation adapter for an ordered factor product.
Seed 55 selects the 55-factor, length-5 signed dyadic fixture. Include genuinely
noncommuting factors, complete rounding and restoration checks, an independent
dense rational reference, instruction corruption controls and a complete cost
recurrence. No common-label primitive or new multiplication exponent is assumed.

Expected deliverable: standalone research construction and exact certificate,
or a scoped obstruction if the mechanism fails. Stop after the stated finite
domain and one implementation; do not search for a new frontier. Target finish:
2026-10-13 01:18 America/Chicago (06:18 UTC); reserve 06:03 onward for verification
and publication/handoff. The scope was selected within the first 20% of this hour.

Preimplementation cost screen: the adapter pays four executions of the enlarged
pipeline, two source translations and two target scatters; exact prefix/closure
coefficients can grow with L. A smaller factor-execution count therefore does not
imply a supplier moment improvement. The experiment targets the changed leaf
contract and exact restoration, with that coefficient expense retained.

Coordination: GitHub reported no pinned issue at 05:18 UTC; the only open issue
was #650 (Discussions). No reservation issue is created. Relevant pending PRs
#628, #663, #665, #673, #689, #705, #714, #730, #744, #758 and #764 were inspected
at the description/source level as applicable. The chosen one-scalar leaf lift
is distinct from their additive leaf/echo-tree and spectral-hosting contracts.
PR756's balanced-Fano verification tooling is reserved for the coordinating chat.

Contributor: Wentao Li (@VictorLiwentao; X: [@Is__Victor](https://x.com/Is__Victor)), with substantial OpenAI Codex
assistance. No independent human review or priority claim is made.
