import MultitapeToolkit.Trace

/-!
# Executable certificates for exact physical multitape execution

`eval` counts successful machine transitions and fails on early halting. Its
soundness and completeness refer to the actual finite-table `Program.step`.
These are semantic certificates, not a bound on the Lean evaluator's own cost.
-/

namespace MultitapeToolkit.Absolute.Execution

variable {ι Γ Q : Type*} [Inhabited Γ]
  [Fintype ι] [Fintype Γ] [Fintype Q]

/-- Execute exactly `n` transitions; halting before the budget is a failure. -/
def eval (P : Program ι Γ Q) : ℕ → MultitapeToolkit.Absolute.Config ι Γ Q → Option (MultitapeToolkit.Absolute.Config ι Γ Q)
  | 0, c => some c
  | n + 1, c => (MultitapeToolkit.Absolute.step P c).bind (eval P n)

@[simp] theorem eval_zero (P : Program ι Γ Q) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    eval P 0 c = some c := rfl

@[simp] theorem eval_succ (P : Program ι Γ Q) (n : ℕ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    eval P (n + 1) c = (MultitapeToolkit.Absolute.step P c).bind (eval P n) := rfl

/-- A mathematical execution produces the very same executable certificate. -/
theorem runs_eval (P : Program ι Γ Q) {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) : eval P n c = some d := by
  induction h with
  | refl => rfl
  | cons hs hr ih => simp [eval, hs, ih]

/-- Every successful evaluator result reconstructs actual transitions. -/
theorem eval_runs (P : Program ι Γ Q) {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : eval P n c = some d) : MultitapeToolkit.Absolute.Runs P n c d := by
  induction n generalizing c with
  | zero =>
    have hc : c = d := Option.some.inj h
    subst d
    exact MultitapeToolkit.Absolute.Runs.refl c
  | succ n ih =>
    cases hs : MultitapeToolkit.Absolute.step P c with
    | none => simp [eval, hs] at h
    | some e =>
      have he : eval P n e = some d := by simpa [eval, hs] using h
      exact MultitapeToolkit.Absolute.Runs.cons hs (ih he)

theorem eval_eq_some_iff (P : Program ι Γ Q) (n : ℕ) (c d : MultitapeToolkit.Absolute.Config ι Γ Q) :
    eval P n c = some d ↔ MultitapeToolkit.Absolute.Runs P n c d := ⟨eval_runs P, runs_eval P⟩

/-- Exact physical execution is deterministic, including all tape cells. -/
theorem runs_deterministic (P : Program ι Γ Q) {n : ℕ}
    {c d e : MultitapeToolkit.Absolute.Config ι Γ Q} (h : MultitapeToolkit.Absolute.Runs P n c d) (h' : MultitapeToolkit.Absolute.Runs P n c e) : d = e := by
  exact Option.some.inj ((runs_eval P h).symm.trans (runs_eval P h'))

/-- An exact trace can be cut at any specified transition count. -/
theorem runs_split (P : Program ι Γ Q) {n m : ℕ} {c e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P (n + m) c e) :
    ∃ d, MultitapeToolkit.Absolute.Runs P n c d ∧ MultitapeToolkit.Absolute.Runs P m d e := by
  induction n generalizing c with
  | zero => exact ⟨c, MultitapeToolkit.Absolute.Runs.refl c, by simpa using h⟩
  | succ n ih =>
    have h' : MultitapeToolkit.Absolute.Runs P ((n + m) + 1) c e := by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h
    cases h' with
    | cons hs hr =>
      obtain ⟨d, hfirst, hrest⟩ := ih hr
      exact ⟨d, MultitapeToolkit.Absolute.Runs.cons hs hfirst, hrest⟩

theorem runs_add_iff (P : Program ι Γ Q) (n m : ℕ) (c e : MultitapeToolkit.Absolute.Config ι Γ Q) :
    MultitapeToolkit.Absolute.Runs P (n + m) c e ↔ ∃ d, MultitapeToolkit.Absolute.Runs P n c d ∧ MultitapeToolkit.Absolute.Runs P m d e := by
  exact ⟨runs_split P, fun ⟨d, h, h'⟩ => Trace.runs_trans P h h'⟩

/-- The executable certificate supports the same exact sequential decomposition. -/
theorem eval_add_eq_some_iff (P : Program ι Γ Q) (n m : ℕ) (c e : MultitapeToolkit.Absolute.Config ι Γ Q) :
    eval P (n + m) c = some e ↔
      ∃ d, eval P n c = some d ∧ eval P m d = some e := by
  simp only [eval_eq_some_iff, runs_add_iff]

/-- A successful prefix is unique and is a prefix of every longer execution. -/
theorem runs_prefix (P : Program ι Γ Q) {n m : ℕ} {c d e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) (h' : MultitapeToolkit.Absolute.Runs P m c e) (hle : n ≤ m) :
    MultitapeToolkit.Absolute.Runs P (m - n) d e := by
  have hm : n + (m - n) = m := by omega
  obtain ⟨middle, hfirst, hrest⟩ := runs_split P (n := n) (m := m - n) (hm ▸ h')
  have heq : middle = d := runs_deterministic P hfirst h
  simpa [heq] using hrest

/-- A halted configuration cannot take even the first positive transition. -/
theorem halt_no_positive_run (P : Program ι Γ Q) {n : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q}
    (hh : MultitapeToolkit.Absolute.Halts P c) (hn : 0 < n) : ¬ MultitapeToolkit.Absolute.Runs P n c d := by
  intro h
  cases n with
  | zero => omega
  | succ n =>
    cases h with
    | cons hs hr =>
      change MultitapeToolkit.Absolute.step P c = none at hh
      rw [hh] at hs
      cases hs

/-- Once a trace halts, no successful longer certificate exists. -/
theorem halted_run_maximal (P : Program ι Γ Q) {n m : ℕ} {c d e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) (hh : MultitapeToolkit.Absolute.Halts P d) (h' : MultitapeToolkit.Absolute.Runs P m c e) : m ≤ n := by
  by_contra hnot
  have hn : n ≤ m := by omega
  exact halt_no_positive_run P hh (by omega) (runs_prefix P h h' hn)

/-- Two complete runs from the same input have exactly the same physical time. -/
theorem halted_time_unique (P : Program ι Γ Q) {n m : ℕ} {c d e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) (hd : MultitapeToolkit.Absolute.Halts P d) (h' : MultitapeToolkit.Absolute.Runs P m c e) (he : MultitapeToolkit.Absolute.Halts P e) : n = m := by
  exact Nat.le_antisymm (halted_run_maximal P h' he h) (halted_run_maximal P h hd h')

/-- Complete execution certifies both exact time and the entire terminal configuration. -/
theorem halted_execution_unique (P : Program ι Γ Q) {n m : ℕ} {c d e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) (hd : MultitapeToolkit.Absolute.Halts P d) (h' : MultitapeToolkit.Absolute.Runs P m c e) (he : MultitapeToolkit.Absolute.Halts P e) :
    n = m ∧ d = e := by
  have htime := halted_time_unique P h hd h' he
  exact ⟨htime, runs_deterministic P h (htime.symm ▸ h')⟩

/-- A certificate beyond a proved halting time fails instead of charging padded steps. -/
theorem eval_after_halt (P : Program ι Γ Q) {n m : ℕ} {c d : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : MultitapeToolkit.Absolute.Runs P n c d) (hh : MultitapeToolkit.Absolute.Halts P d) (hlt : n < m) : eval P m c = none := by
  cases he : eval P m c with
  | none => rfl
  | some e =>
    have hle := halted_run_maximal P h hh (eval_runs P he)
    omega

/-- Execute exactly `n` transitions and additionally check actual terminal halting. -/
def evalHalted (P : Program ι Γ Q) (n : ℕ) (c : MultitapeToolkit.Absolute.Config ι Γ Q) :
    Option (MultitapeToolkit.Absolute.Config ι Γ Q) :=
  (eval P n c).bind fun d => match MultitapeToolkit.Absolute.step P d with
    | none => some d
    | some _ => none

/-- The executable halting certificate is equivalent to the complete actual run. -/
theorem evalHalted_eq_some_iff (P : Program ι Γ Q) (n : ℕ) (c d : MultitapeToolkit.Absolute.Config ι Γ Q) :
    evalHalted P n c = some d ↔ MultitapeToolkit.Absolute.Runs P n c d ∧ MultitapeToolkit.Absolute.Halts P d := by
  cases hv : eval P n c with
  | none =>
    constructor
    · intro h
      simp [evalHalted, hv] at h
    · intro h
      have hrun := runs_eval P h.1
      rw [hv] at hrun
      cases hrun
  | some e =>
    cases hs : MultitapeToolkit.Absolute.step P e with
    | none =>
      constructor
      · intro h
        have he : e = d := by simpa [evalHalted, hv, hs] using h
        subst d
        exact ⟨eval_runs P hv, hs⟩
      · intro h
        have he : e = d := Option.some.inj (hv.symm.trans (runs_eval P h.1))
        subst d
        simp [evalHalted, hv, hs]
    | some f =>
      constructor
      · intro h
        simp [evalHalted, hv, hs] at h
      · intro h
        have he : e = d := Option.some.inj (hv.symm.trans (runs_eval P h.1))
        subst d
        have hh := h.2
        change MultitapeToolkit.Absolute.step P e = none at hh
        rw [hs] at hh
        cases hh
/-- A successful executable certificate determines the unique halting invoice. -/
theorem evalHalted_unique (P : Program ι Γ Q) {n m : ℕ} {c d e : MultitapeToolkit.Absolute.Config ι Γ Q}
    (h : evalHalted P n c = some d) (h' : evalHalted P m c = some e) :
    n = m ∧ d = e := by
  obtain ⟨hr, hh⟩ := (evalHalted_eq_some_iff P n c d).mp h
  obtain ⟨hr', hh'⟩ := (evalHalted_eq_some_iff P m c e).mp h'
  exact halted_execution_unique P hr hh hr' hh'

end MultitapeToolkit.Absolute.Execution

