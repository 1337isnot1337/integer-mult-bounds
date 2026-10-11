# Exact preservation by stage-local address tables

The pinned PR447 scalar replay defines a mapping M_e for each local stage e.
Its closed-over values V, LOCAL, K, R, temp, stage s, pair p and reflection rev
stay unchanged while that stage's instruction stream is consumed. Therefore
G_e[i] = M_e(i), constructed once for 0 <= i <= LOCAL, equals each original
mapping evaluation on that domain. The inclusive endpoint is required because
LOCAL denotes the private copy/clear location; its mapped value is temp.

For every consumed nonzero opcode with operand indices in that domain,
replacing M_e(z[1]), M_e(z[2]) by G_e[z[1]], G_e[z[2]] preserves both addressed
rows exactly. Opcode zero is skipped by both versions and its frame fields
must not be interpreted as row addresses. Negative indices are excluded from
this precondition because Python list negative indexing would not represent
the original mapper. Unsupported positive indices are also excluded.

The subsequent XOR, copy, clear and assertion statements are unchanged. By
induction over instructions, the values and open-private state are identical
after every instruction. The complete stage's dirty-helper restoration test,
level updates, bridges, schedule, stage receipts and terminal identity follow
unchanged. The integer scalar matrix and individual bridge omission checks
are source-identical and remain part of the extracted validation.

The table is newly constructed at each local stage, so it cannot carry an
address from an earlier pair, reflection or helper-stage interval. Its extra
space is O(LOCAL); setup evaluates the mapper LOCAL+1 times per local stage.
Whether this improves runtime requires measurement that includes this setup.

This statement concerns the scalar replay implementation. It adds no new
hosting interface, numerical bound, finite mathematical coefficient, or full
PR447 admission. Testing the pinned eleven-stage recipe using retained local
words is a contract workload, not a reproduction of all PR447 supplier inputs.
The earlier digest-encoding cache operates in a separate later loop; any
composed source still needs an exact patch-scope check.

The retained measurements execute the exact source-extracted replay, including
initialization, table construction, all stage/terminal assertions and all 24
integer bridge omission controls. Original and changed versions independently
return the same complete values, levels, schedule, stage receipts and controls.
The contract also compares every consumed operand mapping, checks all bounds
and both reflections, and proves the actual two-line patch's scope by AST
normalization. Focused controls exercise address-block boundaries and cache
freshness across stages, reject unsupported indices, and show that omitting
the private endpoint causes the extracted replay to fail.

The address patch and the previously published digest-cache patch apply in
both orders to identical source. The offline verifier reproduces that exact
composition from retained patches; their speedups are separate measurements
and must not be multiplied into a whole-emitter speedup claim.
