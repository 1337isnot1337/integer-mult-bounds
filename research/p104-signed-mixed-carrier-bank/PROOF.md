# Signed pair-mixture carriers: finite schematic proof and restrictions

## A. The frame-line identity

Let `u_0,...,u_7` denote the independent binary labels in the reviewed P104 model, and `H_t` the target's binary hyperplane. Define `S_t={i:u_i∈H_t}`. For any two distinct indices `i,j`, because `H_t` is the kernel of a linear functional `λ_t`,

`λ_t(u_i+u_j)=λ_t(u_i)+λ_t(u_j)∈F₂`.

Therefore `u_i+u_j∈H_t` iff either `i,j ∈ S_t` or `i,j ∉ S_t`. This identity is independent of target signs. In the former case either integer data `x_i+x_j` or `x_i−x_j` on a *new allowed carrier with line* `<u_i+u_j>` can replace the two individual signed reads: for `c_i,c_j∈{−1,1}` choose `m⁺` if `c_i=c_j`, else `m⁻`, and add it to the target with sign `c_i`. Then exactly `c_i m^± = c_i x_i + c_j x_j`.

This is a necessary algebraic and geometric compatibility statement. Existence of such a new carrier as a physically legal recursive word is a **separate, unproved requirement**.

## B. Constructive schedule inside the relaxed frame model

For each selected edge `(i,j)`, put `U=span(u_i,u_j)` (rank two). Move both original clean source carriers from their rank-one home lines to U (cost one each). Create two zero helpers and move each from frame `0` to U (cost two each). Perform four signed ADDs to create both `m⁺` and `m⁻`. Restore both source carriers to their own home lines (cost one each), and move each new helper down from U to `<u_i+u_j>` (cost one each). The invoice is **10 rank-move units and 4 ADDs per edge**, including helper creation; two new live auxiliaries remain.

For each target support S, select a matching of disjoint available edges inside S. Every selected pair becomes one signed mixer read. Every remaining vertex becomes a singleton read. Their binary labels are independent because their constituent vertex sets are disjoint subsets of the original independent eight `u_i`. All these ingredient lines lie in H_t. Starting with a zero target, read them successively at the monotonically increasing span U_j, then grow the target to H_t. Each source carrier comes up from its home line, executes an ADD, and goes back to its home line. For k ingredients, the target pays **8** frame-rank units and the k individual carrier trips pay `2∑_{j=1}^k(j−1)=k(k−1)`; the target executes k signed ADDs. All scalar identities hold over the integers, not merely mod 2. This verifies the complete *abstract trace*, not its real E8 compiler lowering.

## C. Exhaustive bank optimization

The three-cube has exactly 12 edges. There are 4096 subsets B. For each target S define `matching(S,B)` to be the maximum cardinality matching among edges of B with both endpoints in S. Then `k(S,B)=|S|−matching(S,B)`. For q edges in the bank the complete schematic invoice is:

`ADD(B) = 4 q + ∑_{S∈F} k(S,B)`

`RANK(B) = 10 q + 104·8 + ∑_{S∈F} k(S,B)(k(S,B)−1)`.

The script computes all 4096 masks by an edge-conflict recurrence and identifies the unique minimum RANK at all 12 edges: ADD=288 and RANK=1312. It separately checks this solution by actually evolving register frames and symbolic data. The independent checker derives the maximum matchings using a vertex-delete / pair recurrence, reproducing every one of the 4096 invoices. The unmixed fixed return-home baseline has ADD=416 and RANK=2224. No claim is made that the baseline is the optimal real decoder or that RANK equals the project's actual recursive cost.

## D. Restricted static-basis obstruction (unsigned case)

For the 104 binary incidence masks S, interpret its **unsigned** target coefficient vector as `1_S∈Q^8`. Suppose eight independent persistent carriers encode an invertible linear basis of the eight original term scalars. Each basis carrier j has a fixed nonzero decoding functional `f_j∈Q^8`: its coefficient in the unique expansion of any output y_S equals `f_j(1_S)`. Its fixed geometric home line is a nonzero `v_j∈span_F2(u_0,...,u_7)`. It may only be read when `v_j∈H_S`. Thus `f_j(1_S)=0` whenever `v_j∉H_S`.

For each nonzero binary v, define `Bad(v)={1_S : S∈F, parity(v ∩ (complement S))=1}`. The checker exhibits an explicit set of eight rows in Bad(v) linearly independent modulo 3 for each of the 247 non-singleton v. They are therefore independent over Q and force any f_j vanishing on Bad(v) to be zero, a contradiction. For each of eight singleton v, Bad(v) has rank seven, and the only allowed f_j is a scalar multiple of the original corresponding coordinate. Consequently a global invertible eight-channel home-line basis cannot use nontrivial mixed lines in the unsigned fixed-access model. A redundant dictionary escapes because its channel coefficients need not be a fixed inverse-basis functional across *every* output and it has extra channels.

This excludes neither signed geometry-dependent target coefficients nor dynamic changes to a frame, and says nothing about the general P104 decoding problem.

## E. Limits

Do not conflate these exact finite results with a certificate for a complete recursive multiplication algorithm. The new composite lines and terminated helper values require source/phase/cleanup work not discharged here. Existing P104 price screens may make a full realization uneconomical even when this schematic beats its stipulated direct baseline. Upstream signed E8 geometry is tested for one exemplar and carries inherited assumptions for other instances.