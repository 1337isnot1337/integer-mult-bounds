# The mixed-negative bound is attained at t = 1 and t = 2

**Partial. No new exponent.**

The necessary count `n` for `t` negative diagonal entries satisfies
`5n >= 11t`, and `n` has the same parity as `t`. That forces

`n(1) = 3`, `n(2) = 6`, `n(3) = 7`, `n(4) = 10`.

The two eight-element product tables agree on all 64 pairs. The cube of `i`
is `zi` and the cube of `j` is `zj`. Three paid calls on one role, each with
both masks equal to that role's basis vector, therefore send the role to its
negative target. Five endpoints are reached in exactly the bound: one `zi`,
one `zj`, two copies of `zi`, one of each, and two copies of `zj`. The
single-role `zj` word is two `i` calls followed by one `j` call. The same
three-call spine at `t = 3` uses 9 calls against a bound of 7, and the
balanced `t = 4` spine uses 12 calls against a bound of 10.

## What was executed

The checker multiplies these retained words. It does not search a shorter word.

`scripts/research_baseline.py` needs
`research/community-frontier1094-audit/ASSEMBLY.json`, which this checkout
does not have. The orientation used here is the mixed-negative attainment in
PR 3697, head `b5fa8645bff6db3ff219815e6fc820a4f08b0572`.

## Scope and evidence

Original card: `bit-new-register-model`, priority revision 6, refined to these
two values of `t`. [TASK.json](TASK.json) records the scope change.
[RESULT.json](RESULT.json) is the executed receipt and is not rewritten.
[SOURCES.json](SOURCES.json) pins the selected record. No selected frontier
file changes.

## Reproduce

From the repository root, CPython 3.12:

```sh
python3.12 -B research/q8-bound-attainment/verify.py
python3.12 -B research/q8-bound-attainment/test_verify.py
python3.12 -B scripts/research_package.py --package research/q8-bound-attainment
```

## Open next questions

Attainment through `t = 2` is this comparison. A shorter word at `t = 3` would leave it.

## Credit

Nick Petalas attained the bound for `t <= 2`.

Prepared by jwr with substantial Cursor agent assistance. No independent human
review is claimed. Apache-2.0.
