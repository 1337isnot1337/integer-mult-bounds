# Scalar-demand gain transfer and the complete bridge-reader family

These are separate deductions, audited in [INDEPENDENT-PROOF.md](INDEPENDENT-PROOF.md).
They use the gain-incidence rank argument proved in [PROOF.md](PROOF.md),
but require no common reader support and no row gauge: their demands are
singleton coordinates in the canonical target basis. The executable checks
the exact bridge kernel, particular endpoint, and coefficient identities
that describe every reader matrix. The universal transfer and tariff
conclusions remain written proofs, not a finite enumeration of readers.

## Scalar-demand transfer lemma

Let C have nonempty, pairwise disjoint indicator columns c_j, let M=C C^T, and suppose M=(C A) R over Q. Assume every column of A has at most two nonzero entries. A may be dependent; actual reader columns may differ arbitrarily.

For any actual reader column at a port of c_j, injectivity of C gives A r=e_j. Select an independent query basis inside that reader's active coefficient-column set, solve for e_j and delete zero coefficients. Its active gain graph has only one nonempty component, containing j: another active component would yield a nontrivial zero combination of independent columns. That component cannot be an ungrounded tree, whose nonzero switching annihilator forbids a singleton demand. It is therefore an unbalanced unicyclic component or a tree with a unit column.

Give every coefficient-space two-port query its own independent formal gain over F2(t_e), and retain unit columns. Every possible simple cycle has nontrivial holonomy, so each selected support remains full-row-rank. Thus every actual singleton demand is recoverable within its old support, independently for every actual reader column. This yields A'R'=C^T over the characteristic-two field, and hence (C A')R'=C C^T. Disjoint columns of C ensure that support(C A')=support(C A): changing a nonzero coefficient cannot cancel across different canonical columns. Reader supports shrink. Full physical-group tariffs therefore do not grow, and the retained I334 expansion gives the canonical invoice floor.

The conclusion permits arbitrary query dependence and arbitrary copy-asymmetric readers, but requires each query to be a combination of at most two complete canonical columns. It is different from requiring at most two literal scalar ports. It does not cover arbitrary queries in the canonical span.

## Exact application to the seven-query bridge family

Let c0=e0+e3, c1=e1+e4, c2=e2+e5. The six triangle queries are

    q0=e0+e1, q1=e1+e2, q2=e2+e0,
    q3=e3+e4, q4=e4+e5, q5=e5+e3,

and q6=c0. The first six columns form an invertible Q6. Write

    D = Q6^{-1} [c0 c1 c2]
      = (1/2) [[1,1,-1],[-1,1,1],[1,-1,1],
                [1,1,-1],[-1,1,1],[1,-1,1]].

One reader solution is R0=[D C^T; 0]. The one-dimensional query kernel is spanned by

    k=(-1/2,1/2,-1/2,-1/2,1/2,-1/2,1)^T.

Consequently every exact reader matrix is R=R0+k z^T for arbitrary rational z on the actual reader ports (including extra zero-target columns if desired). Both R0 and k have identical entries on corresponding rows e and e+3, for e=0,1,2. Thus those reader rows are identical for every z.

Coalesce each equal-reader pair of terms into one term. Its query becomes

    q0+q3=c0+c1,
    q1+q4=c1+c2,
    q2+q5=c2+c0,

and the bridge remains c0. The endpoint is unchanged. Each coalesced source support is a union of the old source supports, with the same reader; binary pairing rank subadditivity proves its tariff is at most the sum of the two old tariffs. This comparison remains true when distinct scalar vertices occupy the same physical triad.

All four remaining queries mix at most two complete canonical target columns, so the scalar-demand transfer lemma applies regardless of z and regardless of copy-asymmetric readers. The coalesced invoice is at least the canonical local invoice18. Therefore the original seven-query family has invoice at least 18 for every rational reader matrix, every literal embedding into three ordinary paired targets, and every number of extra zero-target reader columns. The stated queries have no exterior source vertices; arbitrary query-column rescalings can be absorbed before applying the proof.

This is a whole-family obstruction without a coefficient or geometry grid. It does not assert that invoice18 is attained in the seven-query representation or close different dependent-query architectures. Earlier particular invoices 36 and 39 are not needed by this proof and are not asserted to be optima.

## Relation to the stronger strict-fit result

The bridge's original seven queries already touch at most two literal ports.
The main strict-fit theorem therefore gives its local floor 18 directly after
the zero-overhead canonical completion described in PROOF.md, including the
residual pair/unit refinement. The coalescing proof above remains useful as
an endpoint-preserving derivation and an example of coefficient-space sparse
queries whose literal source supports may have four or more ports.
