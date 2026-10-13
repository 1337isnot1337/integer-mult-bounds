# Four exact U8 B-stage shear rewrites

**Finite complex-supplier construction; no new kappa.** Four three-add fragments in
the selected PR942 U8 local word admit the exact rewrite

`x += a*s; y += q*x; x -= a*s` -> `y += q*x; y += (q*a)*s`.

The B stage drops from 1,918 to 1,914 scalar operations. Under the unchanged selected
binary-Horner invoice, each orientation saves 52 real-component primitives:
193,306 -> 193,254 forward and 193,354 -> 193,302 backward. All 728 arbitrary
columns and the paid rank profile are unchanged.

## Reproduce

From repository root, using Python 3.10+ and the standard library:

```sh
python3 -I -B research/u8-b-cancellation-seed32/verify.py
python3 -I -B research/u8-b-cancellation-seed32/test_package.py
```

Expected:

```text
PASS_U8_B_SHEAR_REWRITE_SEED32 rewrites=4 B=1918->1914 primitives=193306->193254/193354->193302 columns=728 controls=9 no_new_kappa
PASS_U8_B_SHEAR_PACKAGE deterministic_result=1
```

## Evidence and scope

`verify.py` pins the accepted `t37-replay.tar.gz` and canonical-word payload, applies
the four literal rewrites, compares complete exact sparse-rational B-stage matrices,
checks each symbolic three-register identity separately, reproduces baseline receipts,
and rejects nine controls: four single deletions, four wrong cross terms and one
intervening dependency touch.

The unchanged `hpe_emit_local.py` and `hpe_audit_local.py` additionally passed on the
candidate during validation: 728 columns in each orientation, unchanged paid profile,
25 inherited frame/wrapper controls rejected, and prefix bounds of 55/72 bits under
the retained 192-bit allowance. These validation commands are source-bound to the
current repository but are not needed by the one-command independent replay.

No global owner map, complete complex-supplier invoice or outer 47-inequality assembly
was rebuilt, so no kappa change is claimed. All-size/compiler, common-label and
mutable-source realization, whole-call hosting, physical routing, precision/tape,
exact recovery and analytic transfer remain inherited. Finite replay is not a formal
proof of the multiplication theorem.

Base commit: `abdc6a7002abdbcd9e21bfc5e1a795784deacfdf`. OS-random assignment seed:
32 (complex-supplier track). The selected PR942 certificate remains unchanged.
