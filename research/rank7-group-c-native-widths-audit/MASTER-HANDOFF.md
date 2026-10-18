# Master handoff: rank7-group-c-native-widths-audit

## Result

Group C of #2979: both providers and both orientations emit residual pair
`115:262` for helpers 452/453/532/533 (entrance `[30]`, width **6**) under
shared `W = ⟨256,128,64,32,19,11,6⟩`. Adapter and `LOCAL-CHECKS` hashes match
the retained `FULL-NATIVE-RECEIPT.json`. These widths join all **2664** T74
fill placements. No new kappa.

**Not headlined (soft-overlap trap):** guide margins `+17170` / single-helper
negatives — already in `#2979` `STAGE-PRICES.json` / joint-frame invoices. Do
not open a CrocSwap PR that reprints them.

## Pins

- Base / selected main: `6f100d4bb5083f8c35d96fd95a539811c62f245c`
- Selected κ: `0.001672660197076918`
- Task card: `independent-moment` (priority revision 6)
- Predecessor head #2979: `be191346391661f4d35fc0d1508d0a6029572576`
- Branch: `cursor/group-c-native-widths-60b9`
- Content tip SHA: `82407e5bded3c213537ef443c8b9e64e2ee51573`
- Publish tip: branch HEAD of `cursor/group-c-native-widths-60b9` (docs-only handoff commits may follow content tip)
- Package: `research/rank7-group-c-native-widths-audit/`

## Exact commands

```sh
python3 -I -B research/rank7-group-c-native-widths-audit/verify.py
python3 -I -O -B research/rank7-group-c-native-widths-audit/verify.py
python3 -I -B research/rank7-group-c-native-widths-audit/test_verify.py -v
python3 -I -B scripts/research_package.py --package research/rank7-group-c-native-widths-audit --check-only
python3 -I -B scripts/research_package.py --package research/rank7-group-c-native-widths-audit
```

## Expected PASS lines

```text
PASS_GROUP_C_NATIVE_WIDTHS providers=2 helpers=4 residual_widths=6,6,6,6 pairs=452:115:262,453:115:262,532:115:262,533:115:262 placements=2664 adapter_pinned both_orientations no_new_kappa
PASS_PACKAGE_METADATA_AND_PINS (not a mathematical acceptance check)
PASS_REGISTERED_RESEARCH_PACKAGE research/rank7-group-c-native-widths-audit outcome=partial
```

(`-O` verify must print the same `PASS_GROUP_C_NATIVE_WIDTHS` line; `need`/`require`
admission stays enforced.)

## Closest priors

| Prior | Relation |
|---|---|
| `research/rank7-group-a-entrance-audit/` | Methodology predecessor; different helpers/W |
| #3411 `research/rank7-group-b-native-widths-audit/` | Leave-alone group-B native style; different helpers/W |
| `research/rank7-joint-endframes/` (#2979 @ `be191346…`) | Source WORD / FULL-NATIVE / adapters |
| #2993 `rank7-joint-frame-audit` | Frame invoices; not imported |

## What is new vs soft-overlap traps

- **New:** phase-exact residual class `115:262`, entrance `[30]`, climb/wrapper/scalar clocks in both orientations, adapter pin match, native-width → T74 join for helpers `{452,453,532,533}` (2664 placements).
- **Do not claim as new:** joint/single guide margins `+17170`, width inventory `6/6/6/6` alone without native residual binding, or placement counts alone.

## Open next questions

1. Complete peer-native / private-cleanup dependency closure for group C.
2. Physical movement, precision/tape, supplier caps and outer release for the
   unchanged #2979 source.
3. Group D native residual widths under the same method.

## Leave-alone

Open CrocSwap #3421, #3411, #3392, #3386, #3374, #3349; deferred V45 `1910fd12`;
deferred group-B single-control `f795116d`; blocked W=532 unpaid F17 terms;
merged tariff series through #2883; do not reprint #3259 /
`p104-pooled-cut-independent`; in-flight rho tip
`cursor/selected-stock-rho-zero-60b9`.

## Attribution

Wentao Li `<wentaol4@illinois.edu>`. Prepared by Wentao Li with substantial AI
assistance. No `Co-authored-by: Victor Li`. Do **not** open a CrocSwap PR from
this worker (master publishes).
