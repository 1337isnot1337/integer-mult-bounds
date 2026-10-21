# Explicit compiler interface for weak rank separation

`WeakRule` is a new validated rule type for the finite compiler. It admits

```math
1\leq r_j\leq k_{\min}<m,\qquad k_{\min}\geq2.
```

The original PR #4359 `Rule` requires the strict inequality
`r_max<k_min`. Its constructor and scientific source remain unchanged.
This package intentionally broadens the interface and then uses the
frozen `IntegerTree` and `Compiler` implementations with that new type.
The mathematical justification is the companion
[weak-separation proof](../kappa-4359-weak-separation/PROOF.md).

The imported compiler is authenticated before execution against SHA-256
`f842f0e07ca40a181782a565a381b0ee20c6a4b08b8c2b8a4d5d630381bd1e8e`.
Its source is
`research/kappa-rebuild/transfer-audit/finite_dag_audit.py` at
`da637c87c89482bc4c86be36bd0071b3d400dbed`.

## Retained interface obligations

Productive field names are distinct, owned names are distinct, and the
two sets are disjoint. Every target and paid rank is a positive integer.
Every paid call names an actual productive or owned field; an anonymous
paid histogram does not suffice. The maximum paid rank may equal the
smallest target rank, but that target rank is at least two and strictly
smaller than the ambient rank.

The lower bound of two is operationally necessary: the original lattice
generation loop multiplies by `k_min`. A value of one would not reduce
the scale. The strict upper inequality `k_min<m` ensures that equality
at the paid/target boundary still leaves every recursive exit below the
ambient rank.

## Discriminating materialized examples

The tested productive roles and ordered calls are:

```text
roles:  a -> 2, b -> 2, c -> 3
rounds: (1,a), (2,owned-C0), (1,b), (2,c)
```

The productive rank sum is seven and the paid rank sum is six. Thus the
example has a positive rank surplus, an actual equality edge at rank two,
and a paid call acting on the owned center. The original strict
constructor rejects this exact contract; `WeakRule` accepts it.

The unchanged compiler materializes complete graphs at ranks 3, 6, 12,
24, and 48. They exercise generation depths zero through four:

| Ambient rank | Native units | Event nodes | Parent owned center becomes a child input |
| ---: | ---: | ---: | --- |
| 3 | 1 | 10 | No deeper generation |
| 6 | 6 | 52 | Yes |
| 12 | 30 | 244 | Yes |
| 24 | 140 | 1096 | Yes |
| 48 | 628 | 4792 | Yes |

Every graph is acyclic. The original field validator verifies distinct
actual fields within each invocation. All exits are smaller than their
parent ambient rank. Source complements are included in the full leaf
count. One owned field is conservatively allocated per native unit and
receives no productive credit. The final replication factor makes every
chronological child batch integral separately.

Eight rejection controls check the strict predecessor's rejection of
equality, a paid rank above the minimum target, a minimum target equal to
the ambient rank, the nonterminating rank-one lattice case, duplicate
productive names, owned-field output credit, a nonexistent paid owner,
and an actual field alias injected into a materialized equality-case
tree. The last control restores the original field after checking it.

This toy is a structural complete-role contract. It is not asserted to
be a native transform. The actual adjusted native tariff and its operator
deletion are established separately in
`../kappa-4359-native-five/`; the weighted exit estimate and uniform rank
are established in `../kappa-4359-weak-separation/`.

## Reproduction

Run from the contribution checkout with the pinned predecessor available
separately at `/path/to/pr4359`:

```sh
python3 -B research/kappa-4359-weak-compiler/verify.py --source-root /path/to/pr4359
```

The default command authenticates the source, reruns the complete checks,
and compares the deterministic result with [CERTIFICATE.json](CERTIFICATE.json).
Use `--out /tmp/weak-compiler.json` to write a separate certificate.
The certificate binds the verifier itself as well as the imported
compiler. It does not import the native-five receipt, so the dependency
graph has no native-proof cycle.

## Actual native-five integration

`native_five.py` independently reconstructs the complete p3 rule from
the pinned native word, helper bindings, main endpoints, and formal
controller order. It removes exactly the 102 residual calls bound by the
native-five receipt, then instantiates `WeakRule` with all 2,242 actual
productive owners and 25,292 ordered paid calls.

The frozen compiler materializes its rank-57 graph: one native unit,
generation depth zero, 50,586 event nodes, and 25,292 separate ordered
exit batches. The result has `B_57=2242` and `P_57=127570`, including all
source complements. The full-rank leaf total remains the same as in the
original rank-57 audit because removing each sixth-axis call adds one
axis to that source's complement. The improved mixed moment requires
the separately proved large fixed rank.

Every emitted exit is checked against its literal round index, paid rank,
and physical owner. The graph is acyclic, all source fields are distinct,
and the owned center is uncredited. Additional controls reject applying
the old strict constructor to this actual rule, dropping an actual paid
center call, and retaining unearned rank-six credit after a deletion.

```sh
python3 -B research/kappa-4359-weak-compiler/native_five.py --source-root /path/to/pr4359
```

This replays [NATIVE-FIVE.json](NATIVE-FIVE.json). It complements the
positive-generation generic toy checks; it does not materialize the
large native template or replace the separate endpoint proof. The
original weak-compiler toy receipt remains independent of this additional
integration check.

New material is Apache-2.0. The frozen compiler and its attribution remain
those of PR [#4359](https://github.com/CrocSwap/integer-mult-bounds/pull/4359);
the underlying mixed integer flow derives from Jacob Alan Sussman's
PR [#4268](https://github.com/CrocSwap/integer-mult-bounds/pull/4268).
