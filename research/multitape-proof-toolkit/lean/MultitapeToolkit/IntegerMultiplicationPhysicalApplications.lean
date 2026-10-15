import MultitapeToolkit.IntegerMultiplicationEngine
import Mathlib.Logic.Function.Iterate

/-!
# Physical tape endpoint adapters for the concrete multiplication table

A fixed permutation compiles the finite transition table; it is not a free
runtime rearrangement. The accumulator/sumReverse swap fixes both operand tapes
and all initial work tapes are blank, so its input configuration is literally
unchanged. The product is returned at accumulator cell zero, with genuine halt
and the same charged transition count.
-/
set_option autoImplicit false
namespace MultitapeToolkit.Absolute.EndpointAdapters
open TapeEmbedding
variable {I J Γ Q : Type*} [Fintype I] [Fintype J] [Fintype Γ] [Fintype Q]

@[simp] theorem decode_equiv (e : I ≃ J) (j : J) :
    decode e.toEmbedding j = some (e.symm j) := by
  simpa using decode_image e.toEmbedding (e.symm j)

/-- A disjoint tape permutation retains each designated operand tape literally. -/
theorem fixes_designated (e : I ≃ I) (c : MultitapeToolkit.Absolute.Config I Γ Q)
    (H : I → ℤ) (C : I → ℤ → Γ) (i : I) (hi : e i = i) :
    (liftCfg e.toEmbedding c H C).head i = c.head i ∧
    (liftCfg e.toEmbedding c H C).cell i = c.cell i := by
  have h := liftCfg_head_image e.toEmbedding c H C i
  have hc := liftCfg_cell_image e.toEmbedding c H C i
  change (liftCfg e.toEmbedding c H C).head (e i) = c.head i at h
  change (liftCfg e.toEmbedding c H C).cell (e i) = c.cell i at hc
  rw [hi] at h hc
  exact ⟨h,hc⟩

/-- One-MultitapeToolkit.Absolute.step compiler conjugacy also transports executable Option iterates. -/
theorem lift_iterate (e : I ↪ J) (P : Program I Γ Q)
    (H : J → ℤ) (C : J → ℤ → Γ) (n : ℕ) (c : Option (MultitapeToolkit.Absolute.Config I Γ Q)) :
    Option.map (fun d => liftCfg e d H C) ((fun d => d.bind (MultitapeToolkit.Absolute.step P))^[n] c) =
      (fun d => d.bind (MultitapeToolkit.Absolute.step (liftProgram e P)))^[n]
        (Option.map (fun d => liftCfg e d H C) c) := by
  have h : Function.Semiconj (Option.map (fun d => liftCfg e d H C))
      (fun d => d.bind (MultitapeToolkit.Absolute.step P)) (fun d => d.bind (MultitapeToolkit.Absolute.step (liftProgram e P))) := by
    intro d
    cases d with
    | none => rfl
    | some d => simpa using (lift_step e P d H C).symm
  exact (h.iterate_right n) c

/-- Every completed run survives a fixed injective physical tape compilation. -/
theorem completed (e : I ↪ J) (P : Program I Γ Q)
    (H : J → ℤ) (C : J → ℤ → Γ) {n : ℕ} {c d : MultitapeToolkit.Absolute.Config I Γ Q}
    (hr : MultitapeToolkit.Absolute.Runs P n c d) (hh : MultitapeToolkit.Absolute.Halts P d) :
    MultitapeToolkit.Absolute.Runs (liftProgram e P) n (liftCfg e c H C) (liftCfg e d H C) ∧
      MultitapeToolkit.Absolute.Halts (liftProgram e P) (liftCfg e d H C) :=
  ⟨lift_runs e P hr H C,(lift_halts e P d H C).2 hh⟩
end MultitapeToolkit.Absolute.EndpointAdapters

namespace MultitapeToolkit.IntegerMultiplicationPhysicalApplications
open MultitapeToolkit.Absolute MultitapeToolkit.IntegerMultiplicationEngine
open MultitapeToolkit.BinaryMultiplication Lax51Proofs.RamToTM

/-- A single fixed finite permutation, independent of width and data. -/
def outputPermutation : MulStack ≃ MulStack := Equiv.swap .accumulator .sumReverse

@[simp] theorem outputPermutation_multiplier : outputPermutation .multiplier = .multiplier := by decide
@[simp] theorem outputPermutation_multiplicand : outputPermutation .multiplicand = .multiplicand := by decide
@[simp] theorem outputPermutation_accumulator : outputPermutation .accumulator = .sumReverse := by decide
@[simp] theorem outputPermutation_sumReverse : outputPermutation .sumReverse = .accumulator := by decide
@[simp] theorem outputPermutation_symm : outputPermutation.symm = outputPermutation := by
  rfl

noncomputable def accumulatorMachine : Program MulStack (Option Bool) CleanState :=
  TapeEmbedding.liftProgram outputPermutation.toEmbedding cleanMachine

noncomputable def accumulatorOutput (n product : ℕ) : MultitapeToolkit.Absolute.Config MulStack (Option Bool) CleanState :=
  TapeEmbedding.liftCfg outputPermutation.toEmbedding (cleanOutput n product)
    (fun _ => 0) (fun _ _ => none)

/-- Both padded input words and all original tape indices are unchanged. -/
theorem unchanged_input (n a b : ℕ) :
    TapeEmbedding.liftCfg outputPermutation.toEmbedding (cleanInput n a b)
      (fun _ => 0) (fun _ _ => none) = cleanInput n a b := by
  apply MultitapeToolkit.Absolute.Config.ext
  · rfl
  · funext k
    simp [TapeEmbedding.liftCfg,clean_input_control_and_heads]
  · funext k
    cases k <;> simp [TapeEmbedding.liftCfg,outputPermutation,Equiv.swap_apply_def,
      clean_input_work_blank n a b .accumulator (by decide),
      clean_input_work_blank n a b .sumReverse (by decide)]

/-- Literal output location and global cleanliness of every other tape. -/
theorem accumulator_output_contract (n product : ℕ) :
    (accumulatorOutput n product).head .accumulator = 0 ∧
    (accumulatorOutput n product).cell .accumulator =
      StackOriginSerializer.originWord (fixedBits (2*n) product).reverse ∧
    (∀ k, k ≠ .accumulator → (accumulatorOutput n product).cell k = fun _ => none) := by
  constructor
  · simp [accumulatorOutput,TapeEmbedding.liftCfg,cleanOutput]
  constructor
  · simp [accumulatorOutput,TapeEmbedding.liftCfg,cleanOutput]
  · intro k hk
    cases k <;> simp_all [accumulatorOutput,TapeEmbedding.liftCfg,outputPermutation,
      Equiv.swap_apply_def,cleanOutput]

/-- No head is silently returned to origin: the swap transports true endpoints. -/
theorem accumulator_output_heads (n product : ℕ) (k : MulStack) :
    (accumulatorOutput n product).head k = match k with
      | .multiplier | .multiplicand => n
      | .sumReverse => -((2*n : ℕ) : ℤ)
      | _ => 0 := by
  cases k <;> simp [accumulatorOutput,TapeEmbedding.liftCfg,outputPermutation,
    Equiv.swap_apply_def,cleanOutput]

/-- The actual multiplication table, specialized to accumulator output, accepts
exactly the original six-tape input ABI and preserves its charged bound. -/
theorem accumulator_product (n a b : ℕ) (ha : a < 2^n) (hb : b < 2^n) :
    ∃ t, t ≤ 280*n^2+322*n+122 ∧
      MultitapeToolkit.Absolute.Runs accumulatorMachine t (cleanInput n a b) (accumulatorOutput n (a*b)) ∧
      MultitapeToolkit.Absolute.Halts accumulatorMachine (accumulatorOutput n (a*b)) ∧
      bitsValue ((fixedBits (2*n) (a*b)).reverse.reverse) = a*b := by
  rcases clean_product n a b ha hb with ⟨t,ht,hr,hh,hv⟩
  rcases EndpointAdapters.completed outputPermutation.toEmbedding cleanMachine
    (fun _ => 0) (fun _ _ => none) hr hh with ⟨hr',hh'⟩
  rw [unchanged_input] at hr'
  exact ⟨t,ht,hr',hh',hv⟩

/-- The executable iterator for the specialized table is the exact physical
embedding of the original iterator, including Option.none after halt. -/
theorem accumulator_iterate (n : ℕ) (c : Option (MultitapeToolkit.Absolute.Config MulStack (Option Bool) CleanState)) :
    Option.map (fun d => TapeEmbedding.liftCfg outputPermutation.toEmbedding d
      (fun _ => 0) (fun _ _ => none))
        ((fun d => d.bind (MultitapeToolkit.Absolute.step cleanMachine))^[n] c) =
      (fun d => d.bind (MultitapeToolkit.Absolute.step accumulatorMachine))^[n]
        (Option.map (fun d => TapeEmbedding.liftCfg outputPermutation.toEmbedding d
          (fun _ => 0) (fun _ _ => none)) c) :=
  EndpointAdapters.lift_iterate outputPermutation.toEmbedding cleanMachine _ _ n c
end MultitapeToolkit.IntegerMultiplicationPhysicalApplications
