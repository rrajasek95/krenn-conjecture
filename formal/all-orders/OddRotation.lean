import WickFinitePairing
import OddResponseVanishing

/-!
# Actual odd-response rotation cancels the common scalar factor

The two means stay independent until their alternating determinant is canceled
in a polynomial domain. Only afterwards is the second mean specialized to zero.
The rotation identity itself comes from the actual finite Wick construction.
-/

namespace KrennAllOrders.OddRotation

open scoped BigOperators Classical
open MvPolynomial

variable {K σ : Type*} [Field K] [CharZero K]

/-- The literal alternating linear-response factor in two independent vectors. -/
noncomputable def alternatingFactor (i j : σ) : MvPolynomial (σ ⊕ σ) K :=
  X (Sum.inl i) * X (Sum.inr j) - X (Sum.inl j) * X (Sum.inr i)

/-- First and second independent copies of the row-parameter polynomial. -/
noncomputable def leftCopy : MvPolynomial σ K →+* MvPolynomial (σ ⊕ σ) K :=
  (rename (Sum.inl : σ → σ ⊕ σ)).toRingHom

noncomputable def rightCopy : MvPolynomial σ K →+* MvPolynomial (σ ⊕ σ) K :=
  (rename (Sum.inr : σ → σ ⊕ σ)).toRingHom

/-- A coordinate substitution used by the forty-five-degree replica rotation. -/
noncomputable def rotatedLeft (s : K) : MvPolynomial σ K →+* MvPolynomial (σ ⊕ σ) K :=
  eval₂Hom C (fun i => C s * (X (Sum.inl i) - X (Sum.inr i)))

noncomputable def rotatedRight (s : K) : MvPolynomial σ K →+* MvPolynomial (σ ⊕ σ) K :=
  eval₂Hom C (fun i => C s * (X (Sum.inl i) + X (Sum.inr i)))

omit [CharZero K] in
@[simp] theorem eval_leftCopy (a : σ ⊕ σ → K) (g : MvPolynomial σ K) :
    eval a (leftCopy g) = eval (fun i => a (Sum.inl i)) g :=
  eval_rename _ _ _

omit [CharZero K] in
@[simp] theorem eval_rightCopy (a : σ ⊕ σ → K) (g : MvPolynomial σ K) :
    eval a (rightCopy g) = eval (fun i => a (Sum.inr i)) g :=
  eval_rename _ _ _

omit [CharZero K] in
@[simp] theorem eval_rotatedLeft (a : σ ⊕ σ → K) (s : K) (g : MvPolynomial σ K) :
    eval a (rotatedLeft s g) =
      eval (fun i => s * (a (Sum.inl i) - a (Sum.inr i))) g := by
  have hhom : (eval a).comp (rotatedLeft s) =
      eval (fun i => s * (a (Sum.inl i) - a (Sum.inr i))) := by
    ext <;> simp [rotatedLeft]
  exact RingHom.congr_fun hhom g

omit [CharZero K] in
@[simp] theorem eval_rotatedRight (a : σ ⊕ σ → K) (s : K) (g : MvPolynomial σ K) :
    eval a (rotatedRight s g) =
      eval (fun i => s * (a (Sum.inl i) + a (Sum.inr i))) g := by
  have hhom : (eval a).comp (rotatedRight s) =
      eval (fun i => s * (a (Sum.inl i) + a (Sum.inr i))) := by
    ext <;> simp [rotatedRight]
  exact RingHom.congr_fun hhom g

/-- The determinant is canceled as a nonzero polynomial, not at a possibly
singular numerical pair of mean vectors. -/
theorem alternatingFactor_ne_zero {i j : σ} (hij : i ≠ j) :
    alternatingFactor (K := K) i j ≠ 0 := by
  classical
  intro hz
  have h := congrArg (eval (Sum.elim (fun a => if a = i then 1 else 0)
    (fun b => if b = j then 1 else 0))) hz
  simp [alternatingFactor, hij, hij.symm] at h

/-- Exact polynomial cancellation of the alternating linear response. -/
theorem cancel_alternating_rotation (g : MvPolynomial σ K) {i j : σ}
    (hij : i ≠ j) (s : K)
    (hrotation : ∀ a b : σ → K,
      (a i * b j - a j * b i) *
          (eval (fun h => s * (a h - b h)) g * eval (fun h => s * (a h + b h)) g) =
        (a i * b j - a j * b i) * (eval a g * eval b g)) :
    rotatedLeft s g * rotatedRight s g = leftCopy g * rightCopy g := by
  apply mul_left_cancel₀ (alternatingFactor_ne_zero hij)
  apply MvPolynomial.funext
  intro a
  simpa only [map_mul, eval_rotatedLeft, eval_rotatedRight, eval_leftCopy,
    eval_rightCopy, alternatingFactor, map_sub, eval_X] using
    hrotation (fun i => a (Sum.inl i)) (fun i => a (Sum.inr i))

/-- Specializing after cancellation yields the finite scalar rescaling law. -/
theorem rescaling_square_of_alternating_rotation (g : MvPolynomial σ K) {i j : σ}
    (hij : i ≠ j) (s : K) (hzero : eval (fun _ => 0) g = 1)
    (hrotation : ∀ a b : σ → K,
      (a i * b j - a j * b i) *
          (eval (fun h => s * (a h - b h)) g * eval (fun h => s * (a h + b h)) g) =
        (a i * b j - a j * b i) * (eval a g * eval b g)) :
    (FiniteResponseRigidity.scaleVariables s g) ^ 2 = g := by
  have hpoly := cancel_alternating_rotation g hij s hrotation
  apply MvPolynomial.funext
  intro a
  have h := congrArg (eval (Sum.elim a (fun _ => 0))) hpoly
  simp only [map_mul, eval_rotatedLeft, eval_rotatedRight, eval_leftCopy,
    eval_rightCopy, Sum.elim_inl, Sum.elim_inr, sub_zero, add_zero, hzero, mul_one] at h
  have hs : eval a (FiniteResponseRigidity.scaleVariables s g) =
      eval (fun i => s * a i) g := by
    have hh : (eval a).comp (FiniteResponseRigidity.scaleVariables s) =
        eval (fun i => s * a i) := by
      ext <;> simp [FiniteResponseRigidity.scaleVariables]
    exact RingHom.congr_fun hh g
  rw [map_pow, hs, pow_two]
  exact h

section ActualResponse

variable {ι E : Type*} [Fintype ι] [Nonempty ι] [AddCommGroup E] [Module K E]

omit [CharZero K] in
/-- Evaluate a pure odd tensor pairing using its actual common scalar factor. -/
theorem pairing_factored_response (B : E →ₗ[K] E →ₗ[K] K)
    (μ : (σ → K) →ₗ[K] (E →ₗ[K] K)) (u v : ι → E)
    (g : MvPolynomial σ K) (i j : σ) (hodd : Odd (Fintype.card ι))
    (hfactor : ∀ a : σ → K, WickFinitePairing.responseTensor B (μ a) u v =
      eval a g • (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true))
    (a b : σ → K) :
    BinaryPairing.pairing (WickFinitePairing.responseTensor B (μ a) u v)
      (WickFinitePairing.responseTensor B (μ b) u v) =
      (a i * b j - a j * b i) * (eval a g * eval b g) := by
  rw [hfactor a, hfactor b, BinaryPairing.pairing_smul_left,
    BinaryPairing.pairing_smul_right, BinaryPairing.pairing_pure_combinations_odd hodd]
  ring

/-- The alternating polynomial relation is supplied by the proved actual Wick
rotation. It is not a new hypothesis of this theorem. -/
theorem actual_alternating_rotation (B : E →ₗ[K] E →ₗ[K] K)
    (μ : (σ → K) →ₗ[K] (E →ₗ[K] K)) (u v : ι → E)
    (g : MvPolynomial σ K) (i j : σ) (hodd : Odd (Fintype.card ι))
    (hfactor : ∀ a : σ → K, WickFinitePairing.responseTensor B (μ a) u v =
      eval a g • (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true))
    (s : K) (hs : s * s + s * s = 1) (a b : σ → K) :
    (a i * b j - a j * b i) *
        (eval (fun h => s * (a h - b h)) g * eval (fun h => s * (a h + b h)) g) =
      (a i * b j - a j * b i) * (eval a g * eval b g) := by
  have h := WickFinitePairing.response_pairing_rotation B (μ a) (μ b) u v s s hs
  have hm : μ (s • a - s • b) = s • μ a - s • μ b := by simp
  have hp : μ (s • a + s • b) = s • μ a + s • μ b := by simp
  rw [← hm, ← hp, pairing_factored_response B μ u v g i j hodd hfactor,
    pairing_factored_response B μ u v g i j hodd hfactor] at h
  have hd : (s • a - s • b) i * (s • a + s • b) j -
      (s • a - s • b) j * (s • a + s • b) i = a i * b j - a j * b i := by
    simp only [Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    linear_combination (a i * b j - a j * b i) * hs
  rw [hd] at h
  have ha' : (fun h => s * (a h - b h)) = s • a - s • b := by
    funext x
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have hb' : (fun h => s * (a h + b h)) = s • a + s • b := by
    funext x
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    ring
  simpa only [ha', hb'] using h

/-- Actual odd-response covariance removes its normalized common scalar factor. -/
theorem actual_scalar_factor_eq_one (B : E →ₗ[K] E →ₗ[K] K)
    (μ : (σ → K) →ₗ[K] (E →ₗ[K] K)) (u v : ι → E)
    (g : MvPolynomial σ K) {i j : σ} (hij : i ≠ j)
    (hodd : Odd (Fintype.card ι))
    (hfactor : ∀ a : σ → K, WickFinitePairing.responseTensor B (μ a) u v =
      eval a g • (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true))
    (hzero : eval (fun _ => 0) g = 1) (s : K) (hs : s * s + s * s = 1) : g = 1 := by
  have hs0 : s ≠ 0 := by intro h; simp [h] at hs
  apply FiniteResponseRigidity.eq_one_of_rescaling_square g s hs0 hzero
  exact rescaling_square_of_alternating_rotation g hij s hzero
    (actual_alternating_rotation B μ u v g i j hodd hfactor s hs)

/-- The actual rotation closes the existing finite odd-factor vanishing API.
Only the common-factor identities remain inputs, to be supplied by the separate
physical reflection bridge; no response rotation assumption remains. -/
theorem higher_factors_zero_of_actual_rotation {D : ℕ}
    (B : E →ₗ[K] E →ₗ[K] K)
    (μ : (Fin D → K) →ₗ[K] (E →ₗ[K] K)) (u v : ι → E)
    (k : ℕ) (q : ℕ → MvPolynomial (Fin D) K)
    (hq : ∀ r ≤ k, IsWeightedHomogeneous (fun _ : Fin D => (1 : ℕ)) (q r) (2 * r))
    (hzero : q 0 = 1) {i j : Fin D} (hij : i ≠ j)
    (hodd : Odd (Fintype.card ι))
    (hfactor : ∀ a : Fin D → K, WickFinitePairing.responseTensor B (μ a) u v =
      eval a (OddResponseVanishing.finiteScalarFactor k q) •
        (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true))
    (s : K) (hs : s * s + s * s = 1)
    (r : ℕ) (hr : r ≤ k) (hpos : 0 < r) : q r = 0 := by
  have hnorm := OddResponseVanishing.finiteScalarFactor_eval_zero k q hq hzero
  have hg := actual_scalar_factor_eq_one B μ u v
    (OddResponseVanishing.finiteScalarFactor k q) hij hodd hfactor hnorm s hs
  exact OddResponseVanishing.factors_zero_of_finiteScalarFactor_eq_one k q hq hg r hr hpos

/-- The full finite shifted response on the selected binary palette is its
original linear response once reflection has supplied the common factor. -/
theorem actual_response_eq_linear (B : E →ₗ[K] E →ₗ[K] K)
    (μ : (σ → K) →ₗ[K] (E →ₗ[K] K)) (u v : ι → E)
    (g : MvPolynomial σ K) {i j : σ} (hij : i ≠ j)
    (hodd : Odd (Fintype.card ι))
    (hfactor : ∀ a : σ → K, WickFinitePairing.responseTensor B (μ a) u v =
      eval a g • (a i • BinaryPairing.pure false + a j • BinaryPairing.pure true))
    (hzero : eval (fun _ => 0) g = 1) (s : K) (hs : s * s + s * s = 1)
    (a : σ → K) : WickFinitePairing.responseTensor B (μ a) u v =
      a i • BinaryPairing.pure false + a j • BinaryPairing.pure true := by
  have hg := actual_scalar_factor_eq_one B μ u v g hij hodd hfactor hzero s hs
  rw [hfactor a, hg, map_one, one_smul]

end ActualResponse

end KrennAllOrders.OddRotation
