# PR4610 compiler-tightening arithmetic replay

At head 085251d8113b174651cac0f3a04ed4505d1d35b0, the published arithmetic engine reproduces its complete ARITHMETIC.json exactly when run with `--kappa .0030217758`. This includes both tails, the finite compiler threshold and all 54 strict plus four functional outer predicates. The same native profile has raw crossing in (0.00302177587077, 0.00302177587078).

Inputs were exported into an isolated temporary tree from that Git head. All source_sha256 pins matched. The engine also reads `research/kappa-rebuild/complex/full-identity-certificates/RESULT.json` transitively; that file was supplied from the same head, beyond the listed source manifest. Its values are overwritten for the changed supplier invoice, but the file is required to execute.

This replays the producer's exact arithmetic, not an independently implemented proof. No fresh Lean compile, absolute-phase replay or universal transfer proof was performed here. The earlier native word is unchanged. Credit Cao Yifan and all retained supplier/compiler authors. Prepared for Cinna Davis with OpenAI assistance.

Reproduction: export the published source_sha256 paths, native receipt, and extra runtime input at the pinned head. Run the round6 arithmetic.py with `--native` pointing to the round3 NATIVE-VALIDATION.json, `--kappa .0030217758`, and a separate `--out`. Compare the resulting JSON to the published round6 ARITHMETIC.json.

## Open next questions

This improves the supported compiler claim, not the native raw moment. A larger construction improvement still requires a changed paid/productive invoice. The optional full Lean replay remains separate.
