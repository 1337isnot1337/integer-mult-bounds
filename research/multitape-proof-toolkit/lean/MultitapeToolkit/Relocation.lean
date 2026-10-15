import MultitapeToolkit.FrameRule

/-!
# Independent tape-origin relocation of actual multitape executions

A coordinate change relocates BOTH heads and the entire corresponding tape.
The transition table cannot observe absolute coordinates, so the same finite
program executes the relocated instance in exactly the same number of steps.
This is a symmetry of supplied configurations, never a free head movement or
an input conversion performed by the machine.
-/
set_option autoImplicit false
namespace MultitapeToolkit.Absolute.Relocation

open MultitapeToolkit.Locality
variable {ι Γ Q : Type*}

/-- Translate each complete tape and its head by its own fixed displacement. -/
def relocate (offset : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) : MultitapeToolkit.Absolute.Config ι Γ Q :=
  ⟨c.state, fun i => c.head i + offset i, fun i x => c.cell i (x - offset i)⟩

@[simp] theorem relocate_zero (c : MultitapeToolkit.Absolute.Config ι Γ Q) : relocate (fun _ => 0) c = c := by
  cases c
  simp [relocate]

@[simp] theorem relocate_relocate (a b : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    relocate a (relocate b c) = relocate (fun i => b i + a i) c := by
  apply MultitapeToolkit.Absolute.Config.ext
  · rfl
  · funext i; simp [relocate, Int.add_assoc]
  · funext i x; simp [relocate]; congr 1 <;> omega

@[simp] theorem relocate_neg (a : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    relocate (fun i => -a i) (relocate a c) = c := by
  simp

 theorem relocate_injective (a : ι → ℤ) : Function.Injective (relocate (Γ := Γ) (Q := Q) a) := by
  intro c d h
  have hh := congrArg (relocate (fun i => -a i)) h
  simpa using hh

@[simp] theorem relocate_scan (a : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) (i : ι) :
    (relocate a c).cell i ((relocate a c).head i) = c.cell i (c.head i) := by
  simp [relocate]

variable [Fintype ι] [Fintype Γ] [Fintype Q]

/-- Literal one-MultitapeToolkit.Absolute.step conjugacy, including the halting case. -/
theorem relocate_step (P : Program ι Γ Q) (a : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    MultitapeToolkit.Absolute.step P (relocate a c) = (MultitapeToolkit.Absolute.step P c).map (relocate a) := by
  have hscan : (fun i => (relocate a c).cell i ((relocate a c).head i)) =
      (fun i => c.cell i (c.head i)) := by funext i; simp
  unfold MultitapeToolkit.Absolute.step
  rw [hscan]
  rw [show (relocate a c).state = c.state from rfl]
  cases ht : P.transition c.state (fun i => c.cell i (c.head i)) with
  | none => rfl
  | some p =>
    simp only [Option.map_some]
    congr 1
    apply MultitapeToolkit.Absolute.Config.ext
    · rfl
    · funext i; simp [relocate]; omega
    · funext i x
      change (if x = c.head i + a i then (p.2 i).1 else c.cell i (x-a i)) =
        (if x-a i = c.head i then (p.2 i).1 else c.cell i (x-a i))
      have he : (x = c.head i + a i) ↔ (x-a i = c.head i) := by omega
      simp only [he]

/-- Exact successful runs are equivariant under independent tape origins. -/
theorem relocate_runs (P : Program ι Γ Q) (a : ι → ℤ)
    {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q} (h : MultitapeToolkit.Absolute.Runs P n c d) :
    MultitapeToolkit.Absolute.Runs P n (relocate a c) (relocate a d) := by
  induction h with
  | refl c => exact .refl _
  | cons hs hr ih =>
    apply MultitapeToolkit.Absolute.Runs.cons _ ih
    rw [relocate_step,hs]
    rfl

/-- Relocation neither creates nor destroys executions at any exact time. -/
theorem relocate_runs_iff (P : Program ι Γ Q) (a : ι → ℤ)
    {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q} :
    MultitapeToolkit.Absolute.Runs P n (relocate a c) (relocate a d) ↔ MultitapeToolkit.Absolute.Runs P n c d := by
  constructor
  · intro h
    simpa using relocate_runs P (fun i => -a i) h
  · exact relocate_runs P a

/-- The real terminal table lookup is preserved, without adding a transition. -/
theorem relocate_halts_iff (P : Program ι Γ Q) (a : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    MultitapeToolkit.Absolute.Halts P (relocate a c) ↔ MultitapeToolkit.Absolute.Halts P c := by
  unfold MultitapeToolkit.Absolute.Halts
  rw [relocate_step]
  cases MultitapeToolkit.Absolute.step P c <;> simp

/-- Completed executions transport at their exact physical cost. -/
theorem relocate_completed (P : Program ι Γ Q) (a : ι → ℤ)
    {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q} (hr : MultitapeToolkit.Absolute.Runs P n c d) (hh : MultitapeToolkit.Absolute.Halts P d) :
    MultitapeToolkit.Absolute.Runs P n (relocate a c) (relocate a d) ∧ MultitapeToolkit.Absolute.Halts P (relocate a d) :=
  ⟨relocate_runs P a hr, (relocate_halts_iff P a d).2 hh⟩

/-- Every output cell, including dirty background, is relocated literally. -/
@[simp] theorem relocate_cell (a : ι → ℤ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) (i : ι) (x : ℤ) :
    (relocate a c).cell i (x+a i) = c.cell i x := by simp [relocate]

/-- A coordinate change preserves actual head displacement, hence reach bounds. -/
@[simp] theorem relocate_displacement (a : ι → ℤ) (c d : MultitapeToolkit.Absolute.Config ι Γ Q) (i : ι) :
    (relocate a d).head i - (relocate a c).head i = d.head i-c.head i := by
  simp [relocate]

/-- Region agreement can be relocated together with the physical tape data. -/
theorem relocate_matches (a : ι → ℤ) (region : ι → Set ℤ)
    {c d : MultitapeToolkit.Absolute.Config ι Γ Q} (h : FrameRule.MatchesOn region c d) :
    FrameRule.MatchesOn (fun i => {x | x-a i ∈ region i}) (relocate a c) (relocate a d) := by
  refine ⟨h.1, ?_, ?_⟩
  · funext i; change c.head i+a i = d.head i+a i; rw [h.2.1]
  · intro i x hx; exact h.2.2 i (x-a i) hx

end MultitapeToolkit.Absolute.Relocation

