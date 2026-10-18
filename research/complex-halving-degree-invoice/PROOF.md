# Halving degree of the selected complex finite invoice: scoped statement and proof

All numbers below are recomputed exactly by [verify.py](verify.py) and stored in
[RESULT.json](RESULT.json). This is a scoped finite statement under inherited
hypotheses. It is not a supplier, not a κ and not a multiplication theorem.

## Objects

- **Selected invoice.** The selected #1094 replay stores its finite invoice at
  `candidate/strict/global/audit/PREFIX-AND-INVOICE.json` inside
  `research/community-frontier1094-audit/selected-replay.tar.gz`. Its member
  SHA256 is `212cf4ee…0d12`. The fields are: physical roles 14826, stock bits
  S = 2642, physical row 16469, retained row 20161, `row_prefix_extra` 1024, and the
  halving inequality [5329, 4608], that is, 73² > 2·48².
- **Ledger formula.** The finite-invoice assembler lineage vendored at
  `research/complex-571-hpem46c/code/` computes
  `row=2*stock.bit_length()+9909+252+2*payload` with `payload=512`
  (`invoice_allcold.py`). It checks `row<20161` and `halving=m*m>2*maxchild*maxchild`.
  `assemble.py` re-asserts the row identity and
  `0<physical_row_coefficient<retained_row_coefficient==20161`. It certifies the
  outer bridge with `degree_gap = 10**6 - (51/25)*20161`. verify.py recomputes the
  selected stock as `group(36)·14826` and checks that the selected invoice satisfies
  the same identity: 2·2642 + 9909 + 252 + 1024 = 16469.
- **Guard.** At halving degree t the guard on child rank R is 73^t > 2R^t. Every
  complex ceiling screen uses t = 2, which forces R ≤ 51.

## Inherited hypotheses (not proved here)

- **H1 (degree-t ledger).** The lineage's finite-cover transfer can be instantiated
  at halving degree t. It then needs the guard 73^t > 2R^t and charges
  Row(t, S) = t·S + 9909 + 252 + prefix(t). The source support is in the lineage's own
  notes, which charge "a row divisor W(w) at each coarse level"
  (`notes/three-stage-cover-rows.tex`). They instantiate the same ledger at degree 4
  (`notes/paired-cube-assembly.tex`: "least halving degree for 72→60 is four,
  contributing 10,284" = 4·2571, then 10284 + 9909 + 252 = 20445). They also
  instantiate it at degree 24 (`notes/three-stage-cover-assembly.tex`: 24·2431 = 58344,
  then 58344 + 9909 + 252 = 68505). In both, 9909 + 252 is unchanged and the multiplier
  of the stock bits is the least halving degree. Not checked here: whether the written
  transfer proof behind this particular assembler is generic in the degree.
- **H2 (prefix).** prefix(t) is either the fixed value 1024 or 512·t. Source does not
  settle this. `row_prefix_extra = 2*payload` is only instantiated at t = 2, and the
  t = 4 and t = 24 precedents carry no prefix term. Both values are carried throughout.
- **H3 (row contract).**
  - Reading **A**: the retained coefficient 20161 is a binding contract, so
    Row < 20161 (`assemble.py` lines 133 and 149).
  - Reading **B**: the retained coefficient A may be re-chosen while the bridge factor
    51/25 and reserve 10^6 stay fixed. The cap is A ≤ ⌊(25·10^6 − 1)/51⌋ = 490196, with
    gap 10^6 − (51/25)·490196 = 4/25 > 0, and Row < A.
  - Reading **C**, recorded but not used for numbers: the reserve exponent itself is
    chosen per assembly. The pinned notes use 70000, 108000 and 160000;
    `notes/structured-bulk-assembly.tex` says the related suffix condition "holds
    eventually for every fixed ε<1". Under C the row invoice gives no finite cap on t,
    and every conclusion of B holds a fortiori.
- **H4 (other checks independent of t).** None of the formulas for
  `local_primitive_bound`, `logical`, `router`, `literal`, `mass`, `precision` and
  `tape` contains the halving degree. The square in `router` and `literal` is the
  exchange count of a W-role permutation ("A full W-role permutation costs at most W²
  elementary exchanges"). The degree-24 precedent keeps it at W²
  (`2GW^2+8s+4W+4+32m_c<E`). verify.py recomputes router bits (7988), literal bits
  (35284) and required C0 bits (200012) exactly from the selected invoice fields, and
  rechecks all of these inequalities.

## Theorem (scoped)

Assume H1–H4 and the selected stock S = 2642.

1. The admissible degrees form the interval {2, …, t_max}. Here t_max = 3 under
   reading A with either prefix, t_max = 181 under B with the fixed prefix, and
   t_max = 152 under B with the 512·t prefix.
2. Let t_min(R) be the least t with 73^t > 2R^t. A child rank R is admissible exactly
   when t_min(R) ≤ t_max. So R ≤ 57 under A and R ≤ 72 under B. R = 73 is never
   admissible. A rank-56 idle bin (t_min = 3) is admissible under every reading.
3. For general stock, (R, S) is admissible exactly when
   S ≤ S_max(R) = ⌊(cap − 1 − 10161 − prefix(t))/t⌋ with t = t_min(R). Examples:
   - R = 57: S ≤ 2991 or 2821 (reading A, fixed or per-level prefix).
   - R = 72 under A: S ≤ 175 with the fixed prefix; with the per-level prefix no
     positive S works.
   - R = 72 under B: S ≤ 9392 or 8900.
4. Apply the relaxation of `research/complex-local-word-ceiling` (Colkitt) to the
   selected local word, letting idle ranks go up to R. The certified ceilings are:
   - R = 51: a < 1690054109089/10^15, the published value.
   - R = 57: a < 426212879067/(2.5·10^14) ≈ 0.001704851516268, which is +0.875558%
     over R = 51 (κ < 0.0017019499).
   - R = 72: a < 347355787341/(2·10^14) ≈ 0.001736778936705, which is +2.76469%
     (κ < 0.0017337678).

   R = 71 is the least rank whose ceiling cell lies entirely above the selected bit
   endpoint 0.001733427039589844234749. Its t_min is 25, its ceiling is
   0.001734834336053, and R = 70 gives 0.001732866531911.

## Proof

**(1)** S > 0 and prefix(t) is nondecreasing, so Row(t, S) is strictly increasing in t.
The admissible degrees are therefore an initial segment. The boundary rows are:

| Reading and prefix | Row at t_max | Row at t_max + 1 | Cap |
|---|---|---|---|
| A, fixed | 3·2642 + 11185 = 19111 | 21753 | 20161 |
| A, 512·t | 19623 | 22777 | 20161 |
| B, fixed | 181·2642 + 11185 = 489387 | 492029 | 490196 |
| B, 512·t | 152·3154 + 10161 = 489569 | 492723 | 490196 |

The bridge holds at both caps; at 490197 it fails. verify.py also checks that the
admissible set is an initial segment, by direct scan over t = 2..200.

**(2)** For R < 73, (73/R)^t is strictly increasing in t, so the guard holds exactly
for t ≥ t_min(R). The largest admissible rank R_max(t) is therefore nondecreasing in t.
For R ≥ 73, 73^t ≤ R^t < 2R^t, so the guard fails. The boundary cases, all exact
integer comparisons:
- 2·51² = 5202 < 5329 = 73² < 5408 = 2·52².
- 2·57³ = 370386 < 389017 = 73³ < 390224 = 2·58³.
- 73^50 ≤ 2·72^50 and 73^51 > 2·72^51.

A second method computes every t_min(R), R = 1..72, by iterating the coarse
recurrence n ↦ R·⌊n/73⌋ from n₀ = 73^80, where the floors are exact. It returns the
first level with 2n_t < n₀ and agrees with the power search at every R.

**(3)** Row(t, S) < cap holds exactly when S ≤ S_max(t), by integer division.
verify.py checks Row(t, S_max) < cap ≤ Row(t, S_max + 1). Row is increasing in t,
so the least guard-admissible degree t_min(R) is optimal for a given R.

**(4)** Colkitt's lemma gives the bound. A rank-r child costs (r/73)^{1−a}
= r·r^{−a}·73^{a−1}, and the per-unit-mass price is non-increasing in r. So every idle
histogram with ranks ≤ R has moment at least relax_R(a): the local word plus all idle
mass I = 1646 per call placed in fractional rank-R children, divided by w = 896/9.

- relax_R(a) is strictly increasing in a, because each term is (r/73)·e^{a·ln(73/r)}
  with r < 73.
- For a > 0, relax_R(a) is strictly decreasing in R, because the idle term is
  (I/73)(73/R)^a.

The certificate relax_R(a_lo) < 1 < relax_R(a_hi), with a_hi − a_lo = 10^−15, puts the
root in one grid cell. Two enclosure methods agree on both sides at every
R = 51, …, 72:

- **Own method.** The `decimal` module's `ln` and `exp`, which are documented as
  correctly rounded, so the error is within half an ulp. Each is widened by one ulp,
  and every other operation uses directed rounding at 60 digits.
- **Second method.** Colkitt's unmodified rational `child_cost` enclosures
  (atanh/Taylor series, 256-bit outward rounding), aggregated independently. The guard
  check in `model()` is not called.

At R = 51 the bracket equals the unmodified `ceiling.ceiling()` and the published
`RESULT.json`. The ceilings increase strictly with R. The bit crossing is the least R
whose whole cell lies above the bit endpoint, and R = 70 is checked to be at or below
it. ∎

## What this does not show

The ceilings are optimistic relaxations. They do not show that idle children of
rank > 48 can be hosted physically (the open question in #3805). They also do not
reprice stock or coarse depth for children of higher rank: #3113 records only the
selected m = 73 stock envelope and its missing shape lemma, and the coarse depth per
halving grows like 1/log2(73/R). They do not cover native admission either. Reading A versus B (or C) is
an unresolved contract question: the computation is exact under each reading and
decides neither.
