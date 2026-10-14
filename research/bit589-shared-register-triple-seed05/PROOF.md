# Exact finite census argument

## Claim and scope

For the one seed-selected A-section triple `(927, 928, 930)` in the pinned
PR589 `v=111`, `R=439` word, every assignment of its individually legal
PR1345 frame/slot options either violates the full register-chain nesting
condition, preserves the original paid profile, or strictly raises its exact
moment cost. The census has no improving or unresolved assignment. The claim
concerns this tuple and this word only.

## Fixed inputs

`SOURCES.json` pins the selected-result record, review, assembly, selected word
bytes, bit-cost record and moment-cost implementation to base commit
`bce54fb3f895cbe5cd4c0eb477c3afeed100190f`. It separately pins the exact
PR1345 atlas source and the relevant predecessor heads. `verify.py` checks both
Git blob IDs and SHA-256 hashes before using these inputs. It also checks that
the selected certificate still names
`836330098538459/500000000000000000` and that PR589's bit saving is exactly
`1733427039589844234749/1000000000000000000000000`.

The vendored atlas is loaded only through the definitions needed for legal
options and exact scoring. The verifier stops before executing PR1345's own
single/pair census, so this package independently applies those definitions to
the new triple.

## Domain construction

Let each A operation's legal options be its exact `(slot, frame)` pairs from
the pinned atlas. Form the graph on movable A operations, joining operations
whose source/target register sets intersect. Keep components whose product of
individual option counts exceeds 200,000. Within that large component, collect
same-register triples with option-product at most 5,000 and with more than one
distinct legal frame for each member. Sort by `(option product, operation
indices)`. This gives 200 tuples; seed `5 mod 200` selects index 5,
`(927, 928, 930)`.

The selected operations all write register 325 at frame 282, from sources 256,
442 and 392. Their complete option-domain sizes are 7, 6 and 5, so the joint
domain has exactly 210 assignments. No random sampling is used within the
selected tuple.

## Classification and pricing

For each Cartesian-product assignment, the pinned PR1345 chain scorer checks
whether the simultaneous transports are compatible with the complete
register-chain nesting constraints. If it returns no score, the reconstructed
word is also replayed and required to fail the full map check. Otherwise, the
verifier constructs the candidate word, preserving the selected gates and
operands, rebuilds the C section, and computes the exact paid profile by
replaying all 661 registers.

It then prices the profile difference against the original using the pinned
rank-cost intervals. The independently aggregated profile interval must be
contained in the full-chain scorer's interval. Equal profiles have exact zero
direct delta. For changed profiles, the reported interval is strictly positive;
all 64 such assignments have the same changed profile. This establishes a
negative result only over the 210 assignments in the stated finite domain.

The full census is: 46 nesting-incompatible assignments, 100 valid assignments
with the baseline profile, and 64 valid assignments with a strictly higher
profile cost. There are zero improvements and zero unresolved assignments.

## Controls and limitations

The replay checks an all-home identity, rejects a changed source operand, and
rejects a word with the selected A ADD omitted. These controls check the input
identity and coverage paths used by this finite verifier; they do not turn the
census into a formal proof of all PR589 transports.

Other triples, four-way changes, cross-section triples, gate-order or
structural changes, and other supplier words remain open. No optimum theorem,
new supplier admission, or new `kappa` is claimed. Inherited PR589/compiler,
realization, hosting, precision/tape, and analytic assumptions are unchanged.
