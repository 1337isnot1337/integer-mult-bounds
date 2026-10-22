# Linux replay of PR4703's complementary native suppliers

Prepared for Cinna Davis with OpenAI assistance. The constructions and verifier
belong to Dugongue and the source authors credited in PR4703. No new kappa.

Pinned source: CrocSwap/integer-mult-bounds PR4703,
commit 4cc96829fad977aecf0018b26beb067cfd2689a5,
package research/native-dual-suppliers.

An unchanged Git archive of that package was extracted into a temporary,
Git-free directory on Linux. CPython ran:

    python -I -O -B research/native-dual-suppliers/verify.py

The process returned zero. RESULT.json is its complete stdout receipt. The
source verifier authenticates its files, regenerates both providers in separate
temporary copies, compares four mathematical payloads per provider, and checks
two rejecting source-corruption controls. This is a fresh execution of the
producer's verifier, not an independently written mathematical verifier.

The local interfaces retain 56 A plus 56 B (quotient) and 56 A plus 56 C
(restriction) ports. The actual paid profiles and independently restored helper
jobs are not compatible with silently substituting these words into the old
uniform width-eight controller. No profitable complete consumer was supplied
by this review. The current numerical benchmark remains PR4610's conditional
0.0030217758; selected main remains 0.00302015.

This directory is an execution record, not a registered standalone replay
package: reproduce from the exact upstream commit above. Source proofs were
read, but no new Lean proof, compiler/outer transfer, or novel native word is
claimed. The original source package was not modified.
