# Independent verification of the retimed nine-stage complex component

This package fills the certificate-specific checks explicitly left open in PR384 at `fd81a16a1e4e82acfb4d45752cba17450644fde6`. It reproduces the original PR377 component and checks PR378's substituted local word through the actual emitter, scalar programs, lifetimes, Clifford recipes, global template and finite invoice.

The verified conditional complex saving is **999632926176283 / 10^18 = 0.000999632926176283**. PR384 already reports this value. Our contribution is the missing component verification and its reproducible evidence. **No new numerical record or combined kappa admission is claimed.** PR275's weighted-matching result remains unchanged.

## Reproduce

Python 3.11 or newer, standard library only. No package installation, compiler, network, Lean build or cleanup command is used.

```sh
python3 -B research/e8-retimed-component-verification/verify.py --check-inputs
python3 -B research/e8-retimed-component-verification/verify.py --output /path/to/new/external/output
```

The output directory must not exist. Every scratch file, control and failure is retained. Frozen expected counts do not replace computation. The verifier first runs all eight original PR377 stages. In a separate copy it binds both certificate consumers to PR378, prepares candidate regression values while preserving structural pins, freezes the complete key set, and strengthens final admission to reject every missing regression pin. It then runs strict local admission and all six downstream component stages. The original source package stays unchanged.

## What passed

- Original PR377: all eight stages freshly reproduced.
- Changed unit: reference gx and mirror checks, both full dirty-scalar directions on 1,023 columns, restored private work, exact labels/splice and all 20 splice/global controls.
- Exact Clifford construction: all 948 frames and 3,122 directed transitions, including global phases; endpoint adapters and data/cover corrections remain checked.
- Global construction: all 72 source-bound local invocations, owner mappings, bank padding, 14727 cover corrections, emitted profile and finite costs.
- Independent emitted-template audit, five structural controls, nine omitted-bridge controls, both rational moment engines and adjacent-grid rejection.
- Unchanged old-bit outer-assembly regression. This is not a replay or admission of PR382's stronger bit construction.

The fresh candidate invoice gives local bound 7,040,031,186,072, 271,456 local adapters, per-cover cost 558,450,079,948,471, physical stock 2,642 bits, router 7,984 bits, literal charge 35,284 bits, required C0 charge 200,012 bits, halving degree 2 and physical row 15,445 below 20,161. Rank mass 1,072,575, live stock 14,727 and deficit 2,496 stay unchanged. Every retained strict finite inequality passed.

## Actual run and report recovery

The bounded run on existing local Python took 195.92 seconds with peak RSS 144,015,360 bytes and zero swaps. All nine outer scientific stages returned zero, including the eight-stage original regression. All 161 original source files and the frozen candidate code/certificate/pin inputs stayed unchanged.

The original wrapper then hit Python's 4,300-digit JSON parsing limit when reading a 9,634-digit integer. Its original FAILURE.json and frozen adapter are preserved under evidence. A separately reviewed receipt-only completion script disabled that parsing limit, checked all remaining assertions and every log/input binding, and wrote RECEIPT-COMPLETION.json. It launched no child process and repeated no mathematical computation. The portable wrapper includes the same parsing fix from startup; PORTABLE-CHANGES.diff records that fix, relative source paths and input-check mode. The exact scientific replay ran with the preserved original adapter; the portable path changes were checked separately without repeating it.

The completion receipt SHA256 is `10158abd3f447bba67ed440003bc9a53e85f667bf5dfca88e2be321bf4ab8e8f`. The original reviewed adapter manifest is `c5c9072b2ef2439fae694c0dde807828e2e1aaf56a43389962974624a57c9fb7`. The complete candidate input map is pinned by `11ccb2e75eb4eebd927219fdcf5eeaa9c6be37adcb1729e8a4da5d7940ded907`. Historical absolute paths, original manifests and upstream-head fields in recorded receipts describe the actual run; SOURCE-MAPPING.json and the candidate input map identify the changed component. Historical manifests are not misrepresented as candidate manifests.

## Limits

The local E8 invocation, exact Clifford-to-tape compiler, common Gaussian-dyadic grid, precision/recovery and all-size analytic interfaces remain assumptions. The dirty-scalar checks specialize recursive frame operators to identity; exact frame/splice/phase checks address the separate finite obligations. No astronomical cover enumeration or Lean kernel proof ran. This package does not settle PR382's E8 kernel-entrance geometry or full bit finite bill and cannot by itself certify PR384's combined exponent.

Source pins and credits are in SOURCE-MAPPING.json and NOTICE.md. All original licenses and notices are retained.
