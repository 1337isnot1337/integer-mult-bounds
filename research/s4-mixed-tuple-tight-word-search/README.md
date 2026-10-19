# No cost-20 word for the mixed S4 tuple on four or five roles

**Scoped finite exclusion (negative result); no κ, supplier or native
claim.** The setting is the formal `F2[S4]` register model of PR2583 and
PR2998, with adjacent prices `(s1,s2,s3) = (2,1,2)`, free `GL_r(F2)`, all
roles dirty and spectators restored. Here no circuit of paid cost at most 20
realizes

    diag([2143], [3142], [4231], [2143])        on exactly 4 roles,
    diag([2143], [3142], [4231], [2143], 1)     on 5 roles (one dirty spectator).

The direct words cost 21 and leave a spectator untouched, so **the four-role
and five-role optima are both exactly 21**. This
holds even though coordinate cuts allow 20 for every r (PR2998). Coordinate-cut
pricing is therefore not exact for this mixed nonabelian tuple on at most five
roles. Six or more roles were not searched, so this is **not** a theorem that
the optimum is 21 with arbitrary workspace.

## What is new

* **A window lemma ([PROOF.md](PROOF.md) section 3).** For any cut potential
  and any prefix `P_j` of a word with label counts n, it gives
  `Phi(T) - c.(n-m_j) <= phi(P_j) <= c.m_j`. When the cut is tight
  (`c.n = Phi(T)`), the potential is fixed exactly at every prefix.
* **A count lemma (section 4).** The inv, c1 and c3 cuts force any cost-20
  word to have exactly four of each label, twelve paid letters in total. All
  three cuts are then tight.
* **A target-end search (section 5).** Searching backwards from T, over every
  binary rank-one idempotent at every step, makes the windows prune hard. The
  whole r = 4 tree has 1,839,762 window-feasible nodes and dies at depth 8,
  with zero words. The r = 5 tree, searched over 7 symmetry-orbit
  representatives of the first letter, dies at depth 8 as well.
* **Three-target sub-tuple gaps (section 6).** Exact LPs over all `2^24`
  regular coordinate cuts give LP 15 against a direct cost of 16 for
  `(4231,2143,2143)`, and LP 16 against 17 for `(2143,3142,4231)`. By the
  four-role result, both cost their direct values on three roles.

PR2998 (Arham Tahir) and PR3408 (Nick Petalas) showed that coordinate cuts,
and natural/edge subspace cuts, stop at 20; neither searched for words. This
package makes the first circuit-level decision for this tuple and adds no new
cut class.

## Reproduce

Python 3.12+ and the standard library suffice. From the repository root:

```sh
python3 -I -B research/s4-mixed-tuple-tight-word-search/verify.py
```

Expected last line:

```
PASS_S4_MIXED_TUPLE_WINDOW_SEARCH no cost-20 word on r=4 or r=5 roles (recorded searches); r=6+ not searched
```

The default replay takes one to two minutes. It runs five checks:

1. It recomputes the count lemma.
2. It replays the separately written explicit-matrix search: the whole r = 3
   sub-tuple tree, the first three r = 4 depths (56, 1904, 28562) and the
   r = 5 depth-1 count (56). Each is compared with the recorded primary runs.
3. It recounts the 146 words of a two-role control with an unpruned
   frozenset group-algebra brute force. The pruned primary engine also found
   146, so pruning lost no solution there.
4. It runs a positive control (scalar 4312 at counts (1,3,1): one word).
5. It runs a negative control (scalar 4231 at counts (1,3,1): no word, as
   PR2998's precedence argument requires).

`verify.py --self-test` checks that perturbed recorded values are rejected.
`verify.py --full` needs g++ with OpenMP. It recompiles `search.cpp` and
`indep.cpp` and replays the complete r = 4 and r = 5 searches plus the
independent r = 4 engine, taking minutes on about three threads. The
sub-tuple LP replay is
`g++ -O2 -o cutlp cutlp.cpp && ./cutlp > cuts.txt && python3 lp.py cuts.txt`.
It needs about 10 MB.

## Evidence and its limits

* **Primary engine (`search.cpp`).** Group-algebra elements are 24-bit masks.
  Gates are applied by right multiplication, and the windows are computed in
  the natural and ordered-pair modules. Runs:
  * r = 4: all 360 first letters, node counts
    `56, 1904, 28562, 207168, 571536, 648720, 381816, 0`. This took 187 s
    on 3 threads.
  * r = 5: `7, 238, 3571, 25940, 72256, 85622, 52422, 0`, over the
    representatives of the 56 depth-1 survivors. This took about 3 minutes.
* **Second engine (`indep.cpp`).** It multiplies explicit F2 matrices in the
  natural and ordered-pair representations and uses no group-algebra masks.
  It reproduces the full r = 4 tree; see RESULT.json.
* **Positive control at r = 4.** Replacing 4231 by 4312 gives a tuple whose
  direct words cost 20 with counts (4,4,4). The same engine finds such a
  word (RESULT.json `controls`).
* The r = 5 symmetry reduction uses `GL_2(F2)` on the two `2143` roles
  together with `w0`-conjugation, which swaps s1 and s3. PROOF.md section 5
  shows that it is sound. The r = 4 run uses no symmetry.

Local environment: CPython 3.14.4 and g++ 15.2.0 (Ubuntu, x86_64). The
default, `--self-test` and `--full` replays and `scripts/research_package.py
--check-only` pass. `--full` took 14 minutes on a shared 4-CPU machine. The 3.12-pinned registered hook was not run, because no
3.12 interpreter was available. Its two commands are the replays above.

Assumptions inherited from predecessors: the model of PR2583/PR2998 and the
cut-rank lemma of PR1941/PR1966/PR1989. The finite search was not
formally verified.

Unresolved obligations:

* the case of six or more roles (arbitrary workspace);
* a uniform written invariant explaining why the window tree dies;
* any native realization, routing or ownership invoice, bit supplier or κ.

## Open next questions

1. **Does a second spectator (r >= 6) allow cost 20?** Coordinate cuts allow
   20 for every r, so only extra workspace can still realize it. A yes would
   be the first restored-spectator saving in this weighted model. First step:
   run `search.cpp` at r = 6 (6048 gates) with the same first-letter
   symmetry. The r = 4 and r = 5 trees both die at depth 8 with similar sizes
   per representative. This needs a separately budgeted run, with the
   five-point expansion decision posted in Discussion #2570 first.
2. **Is there a uniform stronger-than-cut obstruction?** An all-r argument
   would give the arbitrary-workspace 21 theorem that PR2998 left open. First
   step: find which window, and which block, kills every depth-8 extension of
   the 381,816 depth-7 survivors at r = 4. Then try to state that window as a
   chronological rank inequality valid for every r.

## Sources and credit

Base: canonical main `20ecf2891d80b5acf18d980b2164fb44ea7faa90`, priority
revision 6. [SOURCES.json](SOURCES.json) pins the inputs with git blobs and
SHA256. Claim and canonical thread:
[Discussion #2570](https://github.com/CrocSwap/integer-mult-bounds/discussions/2570#discussioncomment-19027763).
The task did not come from a #1166 handoff.

Credit:

* Arham Tahir (Arham-Tahir64): PR2998, head `3aa400ed59`,
  `research/s4-two-premium-cut-envelope`. Supplied the sharp coordinate-cut
  value 20, the attaining potential `f_0`, the scalar precedence argument and
  this open question.
* Nick Petalas (petalas): PR2583, head `715f558e04`, the two-register census
  and model; PR3408, head `8ed0087a75`, the subspace-cut boundary.
* Ross Richardson: PR1966 and PR1989, the `s4-permutation-cut-cone` archive
  and the two-cut tariff in Discussion #2570.
* Adam Gall: PR1941, the cut-rank lemma.
* David Arias (DavidAriasC): PR2738.

New here: the window lemma as a pruning device, the count lemma, the
r = 4 and r = 5 exhaustive exclusions, the four-role exact optimum 21 and the
three-target sub-tuple LP gaps.

Prepared by Sagar Thakrar (thakrarsagar) with substantial AI assistance from
Claude (Anthropic, Claude Opus 5.5). All engines and checks were written in
the same AI-assisted session. They are two implementations by one author,
not independent human review. Apache-2.0.
