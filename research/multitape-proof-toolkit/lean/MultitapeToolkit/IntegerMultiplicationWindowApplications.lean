import MultitapeToolkit.IntegerMultiplicationEngine
import MultitapeToolkit.Relocation
set_option autoImplicit false
namespace MultitapeToolkit.Absolute.BoundedWindows
open MultitapeToolkit.Locality FrameRule
variable {I A Q : Type} [Inhabited A] [Fintype I] [Fintype A] [Fintype Q]
/-- A closed, explicit tape window around each supplied initial head. -/
def window (h : I → ℤ) (budget : ℕ) : I → Set ℤ :=
  fun i => {x | (x-h i).natAbs ≤ budget}
/-- The actual scanned footprint lies in the time-budget window. -/
theorem footprint_radius {P : Program I A Q} {n : ℕ} {c d : Config I A Q}
    {F : I → Finset ℤ} (h : FootprintedRuns P n c d F) :
    ∀ i x, x ∈ F i → (x-c.head i).natAbs ≤ n := by
  induction h with
  | refl c => intro i x hx; simpa using hx
  | @cons n c middle final F hs hr ih =>
    intro i x hx
    rcases Finset.mem_insert.mp hx with he | ht
    · subst x; simp
    · exact (Trace.head_distance_triangle x (middle.head i) (c.head i)).trans
        (Nat.add_le_add (ih i x ht) ((Trace.step_frame P hs).1 i))
/-- Finite windows suffice for the exact run and genuine halt. Every cell beyond
    the window may initially contain arbitrary data and is preserved literally. -/
theorem completed_window {P : Program I A Q} {n budget : ℕ} {c d : Config I A Q}
    (hr : Runs P n c d) (hh : Halts P d) (hb : n ≤ budget)
    (other : Config I A Q) (hm : MatchesOn (window c.head budget) c other) :
    ∃ final, Runs P n other final ∧ Halts P final ∧
      MatchesOn (window c.head budget) d final ∧
      ∀ i x, budget < (x-c.head i).natAbs → final.cell i x = other.cell i x := by
  rcases footprint_of_runs hr with ⟨F,hF⟩
  have hsub : ∀ i x, x ∈ F i → x ∈ window c.head budget i :=
    fun i x hx => (footprint_radius hF i x hx).trans hb
  rcases hF.completed_lockstep (window c.head budget) hsub
    (fun i => ((Trace.runs_reach_and_frame P hr).1 i).trans hb) hh other hm with
    ⟨final,hOther,hHalt,hMatch⟩
  refine ⟨final,hOther.toRuns,hHalt,hMatch,?_⟩
  intro i x hx
  exact hOther.frame i x (fun hmem => Nat.not_le_of_gt hx (hsub i x hmem))
end MultitapeToolkit.Absolute.BoundedWindows
namespace MultitapeToolkit.IntegerMultiplicationEngine.Windows
open MultitapeToolkit.Absolute MultitapeToolkit.Absolute.BoundedWindows
open MultitapeToolkit.Absolute.FrameRule MultitapeToolkit.Absolute.Relocation
open MultitapeToolkit.BinaryMultiplication Lax51Proofs.RamToTM
/-- This conservative radius is explicit and independent of actual execution time. -/
def radius (n : ℕ) := 280*n^2+322*n+122
/-- The same multiplication table works at independently chosen tape origins,
    requires agreement only inside explicit bounded windows, and preserves every
    arbitrary exterior cell. Origins are supplied coordinates, with no free moves. -/
theorem dirty_relocated_product (n a b : ℕ) (ha : a<2^n) (hb : b<2^n)
    (offset : MulStack → ℤ)
    (other : MultitapeToolkit.Absolute.Config MulStack (Option Bool) CleanState)
    (hm : MatchesOn (window (relocate offset (cleanInput n a b)).head (radius n))
      (relocate offset (cleanInput n a b)) other) :
    ∃ t final, t ≤ radius n ∧ MultitapeToolkit.Absolute.Runs cleanMachine t other final ∧ MultitapeToolkit.Absolute.Halts cleanMachine final ∧
      MatchesOn (window (relocate offset (cleanInput n a b)).head (radius n))
        (relocate offset (cleanOutput n (a*b))) final ∧
      ∀ i x, radius n < (x-(relocate offset (cleanInput n a b)).head i).natAbs →
        final.cell i x = other.cell i x := by
  rcases clean_product n a b ha hb with ⟨t,ht,hr,hh,hvalue⟩
  rcases relocate_completed cleanMachine offset hr hh with ⟨hrr,hhh⟩
  rcases completed_window hrr hhh ht other hm with ⟨final,hfr,hfh,hfm,hff⟩
  exact ⟨t,final,ht,hfr,hfh,hfm,hff⟩
/-- Each of the six window centers is the independently supplied origin. -/
theorem input_window_centers (n a b : ℕ) (offset : MulStack → ℤ) :
    (relocate offset (cleanInput n a b)).head = offset := by
  funext i
  have h := congrFun (clean_input_control_and_heads n a b).2 i
  simp only [relocate]
  change (cleanInput n a b).head i + offset i = offset i
  rw [h,zero_add]
/-- The protected product window has the literal padded MSB word at its chosen origin. -/
theorem product_word_in_window (n a b : ℕ) (offset : MulStack → ℤ)
    (final : MultitapeToolkit.Absolute.Config MulStack (Option Bool) CleanState)
    (hm : MatchesOn (window (relocate offset (cleanInput n a b)).head (radius n))
      (relocate offset (cleanOutput n (a*b))) final)
    (x : ℤ) (hx : x.natAbs ≤ radius n) :
    final.cell .sumReverse (x+offset .sumReverse) =
      StackOriginSerializer.originWord (fixedBits (2*n) (a*b)).reverse x := by
  have hmem : x+offset .sumReverse ∈
      window (relocate offset (cleanInput n a b)).head (radius n) .sumReverse := by
    unfold window
    rw [input_window_centers]
    simpa using hx
  have hcell := (hm.2.2 .sumReverse (x+offset .sumReverse) hmem).symm
  simpa [relocate,cleanOutput] using hcell
end MultitapeToolkit.IntegerMultiplicationEngine.Windows
