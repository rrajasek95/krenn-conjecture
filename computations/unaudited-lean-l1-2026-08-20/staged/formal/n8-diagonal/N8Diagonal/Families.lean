/-
UNAUDITED (lane L1 staging), 2026-08-20.
Part of `formal/n8-diagonal`; see that directory's README.md.
-/
import N8Diagonal.Wlog
import N8Diagonal.Normal
import N8Diagonal.Rup

/-!
# The Boolean abstraction: variables, the assignment, and the clause families

Section 5 of `proofs/eight-site-diagonal-obstruction.md`. One Boolean per
hafnian,

  `p(c, S)  ==  haf(t^c | S) != 0`,

with `S` an even-size subset of the eight sites carried as an 8-bit mask. The
encoder numbers these `1 + 128*c + rank(S)` in DIMACS, so with the
zero-based literals of `Rup.lean` the index is `128*c + rank(S)`; `rank` counts
the even-popcount masks strictly below `S`.

**The numbering is not proved correct here, and does not need to be.** The
ledger layer checks `replayExact : tags.map clauseOf = coreCNF` by `decide`, so
a disagreement between this indexing and the encoder's makes that check fail
loudly rather than silently proving a different theorem.

Each family below gets one lemma: the clause it names is satisfied by the
assignment induced by a genuine diagonal solution. Those lemmas are the entire
mathematical content of the abstraction-soundness step; everything else is
bookkeeping over finite data.
-/

namespace N8Diagonal

open MonochromaticQuantumGraph
open N8Diagonal.Rup

/- ## Sites as bitmasks -/

/-- Number of set bits below position 8. -/
def popc (m : Nat) : Nat := ((List.range 8).filter (fun i => m.testBit i)).length

/-- The sites of a mask, in increasing order: literally the colour-class filter that
`pmSumN_diagonal` produces. -/
def maskToList (m : Nat) : List (V 8) :=
  (vertices 8).filter (fun v => m.testBit v.val)

/-- Position of an even-popcount mask among the even-popcount masks. -/
def rankOf (m : Nat) : Nat :=
  ((List.range m).filter (fun k => popc k % 2 == 0)).length

/-- The Boolean variable index of `p(c, S)`, zero-based. -/
def pvar (c : Fin 3) (m : Nat) : Nat := c.val * 128 + rankOf m

/- ## The assignment induced by a solution -/

variable {α : Type} [CommRing α] [IsDomain α]

/-- The hafnian of a colour class given as a mask. -/
def hafM (W : WeightsN 8 3 α) (c : Fin 3) (m : Nat) : α :=
  haf W c (maskToList m)

open scoped Classical in
/-- The base assignment: a variable is true exactly when its hafnian is nonzero. -/
noncomputable def baseAssign (W : WeightsN 8 3 α) : Fin 3 → Nat → Bool :=
  fun c m => decide (hafM W c m ≠ 0)

/-- A positive literal `p(c,m)` is satisfied exactly when the hafnian is nonzero, and a
negative one exactly when it vanishes. This is the only bridge between the algebra and
`Rup.SatLit`, so every family lemma goes through it. -/
theorem satLit_pos {W : WeightsN 8 3 α} {a : Rup.Assign} {c : Fin 3} {m : Nat}
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    (h : hafM W c m ≠ 0) : Rup.SatLit a (pvar c m, true) := by
  rw [Rup.SatLit, ha c m, baseAssign]
  simpa using h

theorem satLit_neg {W : WeightsN 8 3 α} {a : Rup.Assign} {c : Fin 3} {m : Nat}
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    (h : hafM W c m = 0) : Rup.SatLit a (pvar c m, false) := by
  rw [Rup.SatLit, ha c m, baseAssign]
  simpa using h

/- ## A0: the empty class

`haf(t^c | empty) = 1`, one of the three facts Remark 1.5 says the whole proof needs about
the coefficient ring, and here it is definitional. -/

@[simp] theorem maskToList_zero : maskToList 0 = [] := by
  simp [maskToList]

theorem hafM_zero (W : WeightsN 8 3 α) (c : Fin 3) : hafM W c 0 = 1 := by
  rw [hafM, maskToList_zero, haf_nil]

theorem a0_sound {W : WeightsN 8 3 α} {a : Rup.Assign} (c : Fin 3)
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k) :
    Rup.SatClause a [(pvar c 0, true)] :=
  ⟨_, List.mem_singleton_self _, satLit_pos ha (by rw [hafM_zero]; exact one_ne_zero)⟩

/- ## A1: the constant rows

The only place the constant rows are used, and only their nonvanishing. -/

theorem maskToList_full : maskToList 255 = vertices 8 := by
  refine List.filter_eq_self.mpr fun v _ => ?_
  have : v.val < 8 := v.isLt
  interval_cases h : v.val <;> simp_all [Nat.testBit]

theorem a1_sound {W : WeightsN 8 3 α} {a : Rup.Assign} (c : Fin 3)
    (hW : IsDiagonal W) (hEq : EqSystemNZ 8 3 W)
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k) :
    Rup.SatClause a [(pvar c 255, true)] := by
  refine ⟨_, List.mem_singleton_self _, satLit_pos ha ?_⟩
  rw [hafM, maskToList_full]
  exact haf_vertices_ne_zero hW hEq c

/- ## A2: the exactness rows

Every mixed all-even word says a product of three hafnians vanishes, so over a domain some
factor vanishes. This is the only family that consumes the product formula, and it is the
bulk of every case formula (1638 of the roughly 13,800 clauses). -/

/-- The colouring induced by an ordered partition of the sites into three masks. The third
mask is determined as the complement, so only two are needed. -/
def partColour (m0 m1 : Nat) (v : V 8) : Fin 3 :=
  if m0.testBit v.val then 0 else if m1.testBit v.val then 1 else 2

/-- The colour-`c` class of `partColour` is the corresponding mask. -/
theorem filter_partColour_zero (m0 m1 : Nat) :
    (vertices 8).filter (fun v => decide (partColour m0 m1 v = 0)) = maskToList m0 := by
  refine List.filter_congr fun v _ => ?_
  by_cases h : m0.testBit v.val
  · simp [partColour, maskToList, h]
  · by_cases h1 : m1.testBit v.val <;> simp [partColour, maskToList, h, h1]

theorem filter_partColour_one {m0 m1 : Nat}
    (hdisj : ∀ v : V 8, m1.testBit v.val → ¬ m0.testBit v.val) :
    (vertices 8).filter (fun v => decide (partColour m0 m1 v = 1)) = maskToList m1 := by
  refine List.filter_congr fun v _ => ?_
  by_cases h1 : m1.testBit v.val
  · simp [partColour, maskToList, h1, hdisj v h1]
  · by_cases h0 : m0.testBit v.val <;> simp [partColour, maskToList, h0, h1]

theorem filter_partColour_two {m0 m1 m2 : Nat}
    (hcover : ∀ v : V 8, m2.testBit v.val ↔ (¬ m0.testBit v.val ∧ ¬ m1.testBit v.val)) :
    (vertices 8).filter (fun v => decide (partColour m0 m1 v = 2)) = maskToList m2 := by
  refine List.filter_congr fun v _ => ?_
  by_cases h0 : m0.testBit v.val
  · simp [partColour, maskToList, h0, (hcover v).mp.mt (by simp [h0])]
  · by_cases h1 : m1.testBit v.val
    · simp [partColour, maskToList, h0, h1, (hcover v).mp.mt (by simp [h1])]
    · simp [partColour, maskToList, h0, h1, (hcover v).mpr ⟨h0, h1⟩]

/-- The semantic content of an A2 row: some colour class has vanishing hafnian. -/
theorem a2_exists_zero {W : WeightsN 8 3 α} (hW : IsDiagonal W) (hEq : EqSystemNZ 8 3 W)
    {m0 m1 m2 : Nat}
    (hdisj : ∀ v : V 8, m1.testBit v.val → ¬ m0.testBit v.val)
    (hcover : ∀ v : V 8, m2.testBit v.val ↔ (¬ m0.testBit v.val ∧ ¬ m1.testBit v.val))
    (hne : ¬ allEqual (partColour m0 m1)) :
    hafM W 0 m0 = 0 ∨ hafM W 1 m1 = 0 ∨ hafM W 2 m2 = 0 := by
  have hprod := prod_haf_eq_zero hW hEq (partColour m0 m1) hne
  rw [Finset.prod_eq_zero_iff] at hprod
  obtain ⟨c, -, hc⟩ := hprod
  fin_cases c
  · exact Or.inl (by rwa [hafM, ← filter_partColour_zero m0 m1])
  · exact Or.inr (Or.inl (by rwa [hafM, ← filter_partColour_one hdisj]))
  · exact Or.inr (Or.inr (by rwa [hafM, ← filter_partColour_two hcover]))

/-- The clause the encoder emits for an A2 row: one negative literal per non-empty part.
An empty part has `haf = 1 != 0`, so its literal would be false and is omitted. -/
def a2Clause (m0 m1 m2 : Nat) : Rup.Clause :=
  (if m0 = 0 then [] else [(pvar 0 m0, false)]) ++
  (if m1 = 0 then [] else [(pvar 1 m1, false)]) ++
  (if m2 = 0 then [] else [(pvar 2 m2, false)])

theorem a2_sound {W : WeightsN 8 3 α} {a : Rup.Assign} (hW : IsDiagonal W)
    (hEq : EqSystemNZ 8 3 W)
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    {m0 m1 m2 : Nat}
    (hdisj : ∀ v : V 8, m1.testBit v.val → ¬ m0.testBit v.val)
    (hcover : ∀ v : V 8, m2.testBit v.val ↔ (¬ m0.testBit v.val ∧ ¬ m1.testBit v.val))
    (hne : ¬ allEqual (partColour m0 m1)) :
    Rup.SatClause a (a2Clause m0 m1 m2) := by
  have hne0 : ∀ (c : Fin 3) (m : Nat), hafM W c m = 0 → m ≠ 0 := by
    intro c m hm hz
    rw [hz, hafM_zero] at hm
    exact one_ne_zero hm
  rcases a2_exists_zero hW hEq hdisj hcover hne with h | h | h
  · exact ⟨_, by simp [a2Clause, if_neg (hne0 0 m0 h)], satLit_neg ha h⟩
  · exact ⟨_, by simp [a2Clause, if_neg (hne0 1 m1 h)], satLit_neg ha h⟩
  · exact ⟨_, by simp [a2Clause, if_neg (hne0 2 m2 h)], satLit_neg ha h⟩

/- ## A3: Laplace expansion, and its gate variables

`haf(t^c|S) = sum over u in S-w of t^c_{wu} * haf(t^c | S-w-u)`, so if every summand has a
vanishing factor the hafnian vanishes. The encoder Tseitin-encodes each summand as a gate
variable `g(c,S,w,u)` standing for the conjunction of its two inputs. Expanding at an
arbitrary `w` — not just the least site — is what `haf_expand` supplies and what the
symmetrisation layer was built for. -/

theorem maskToList_nodup (m : Nat) : (maskToList m).Nodup :=
  List.Pairwise.sublist List.filter_sublist
    ((vertices_sorted 8).imp (fun h => ne_of_lt h))

/-- A two-element hafnian is a single edge weight. -/
theorem haf_pair {W : WeightsN 8 3 α} (hs : IsSymm W) (c : Fin 3) {L : List (V 8)}
    (hnd : L.Nodup) {w u : V 8} (hw : w ∈ L) (he : L.erase w = [u]) :
    haf W c L = W (mkEdge w u c c) := by
  rw [haf_move_head hs c L.length L rfl hnd w hw, he, haf_cons']
  simp

/-- The data the encoder attaches to one Laplace summand. -/
structure GateData where
  /-- the gate's Boolean variable index -/
  idx : Nat
  /-- the partner site `u` -/
  u : V 8
  /-- mask of the pair `{w, u}` -/
  mwu : Nat
  /-- mask of `S - w - u` -/
  mrest : Nat

/-- `A3g`, first half: a true gate forces its pair input. Pure Boolean reasoning. -/
theorem a3g1_sound {W : WeightsN 8 3 α} {a : Rup.Assign} {c : Fin 3} {g : GateData}
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    (hg : a g.idx = (baseAssign W c g.mwu && baseAssign W c g.mrest)) :
    Rup.SatClause a [(g.idx, false), (pvar c g.mwu, true)] := by
  by_cases h : a g.idx = true
  · refine ⟨(pvar c g.mwu, true), by simp, ?_⟩
    rw [Rup.SatLit, ha c g.mwu]
    rw [hg, Bool.and_eq_true] at h
    exact h.1
  · exact ⟨(g.idx, false), by simp, by simpa [Rup.SatLit] using h⟩

/-- `A3g`, second half: a true gate forces its cofactor input. -/
theorem a3g2_sound {W : WeightsN 8 3 α} {a : Rup.Assign} {c : Fin 3} {g : GateData}
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    (hg : a g.idx = (baseAssign W c g.mwu && baseAssign W c g.mrest)) :
    Rup.SatClause a [(g.idx, false), (pvar c g.mrest, true)] := by
  by_cases h : a g.idx = true
  · refine ⟨(pvar c g.mrest, true), by simp, ?_⟩
    rw [Rup.SatLit, ha c g.mrest]
    rw [hg, Bool.and_eq_true] at h
    exact h.2
  · exact ⟨(g.idx, false), by simp, by simpa [Rup.SatLit] using h⟩

/-- **A3.** If no Laplace summand survives then the hafnian vanishes. -/
theorem a3_sound {W : WeightsN 8 3 α} {a : Rup.Assign} (hs : IsSymm W) {c : Fin 3}
    {m : Nat} {w : V 8} {gs : List GateData}
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    (hga : ∀ g ∈ gs, a g.idx = (baseAssign W c g.mwu && baseAssign W c g.mrest))
    (hw : w ∈ maskToList m)
    (hpair : ∀ g ∈ gs, haf W c (maskToList g.mwu) = W (mkEdge w g.u c c))
    (hrest : ∀ g ∈ gs, maskToList g.mrest = ((maskToList m).erase w).erase g.u)
    (hcover : ∀ u ∈ (maskToList m).erase w, ∃ g ∈ gs, g.u = u) :
    Rup.SatClause a ((pvar c m, false) :: gs.map (fun g => (g.idx, true))) := by
  by_cases hsome : ∃ g ∈ gs, a g.idx = true
  · obtain ⟨g, hg, hgt⟩ := hsome
    have hmem : (g.idx, true) ∈ (pvar c m, false) :: gs.map (fun g => (g.idx, true)) :=
      List.mem_cons_of_mem _ (List.mem_map.mpr ⟨g, hg, rfl⟩)
    exact ⟨(g.idx, true), hmem, hgt⟩
  · push_neg at hsome
    refine ⟨(pvar c m, false), by simp, satLit_neg ha ?_⟩
    rw [hafM]
    refine haf_eq_zero_of_expand hs c (maskToList_nodup m) hw ?_
    intro u hu
    obtain ⟨g, hg, rfl⟩ := hcover u hu
    have hgf : (baseAssign W c g.mwu && baseAssign W c g.mrest) ≠ true := by
      rw [← hga g hg]; exact hsome g hg
    rw [ne_eq, Bool.and_eq_true, not_and_or] at hgf
    have conv : ∀ (d : Fin 3) (k : Nat), ¬ (baseAssign W d k = true) → hafM W d k = 0 := by
      intro d k hd
      simpa [baseAssign] using hd
    rcases hgf with h | h
    · left
      rw [← hpair g hg]
      exact conv c g.mwu h
    · right
      rw [← hrest g hg]
      exact conv c g.mrest h

/- ## The free set, and Lemma 3.2

Definition 3.1: `y` is *free* for colour `c` at the solve site `z` when every even split of
`V' - y` between the other two colours has vanishing product. Lemma 3.2 says that a site which
is **not** free has `x^c_y = 0` — the support statement C0 rests on, and through it FR and XF.
The two "other" colours follow the encoder's convention: `c = 0, 1, 2` gives `(1,2)`, `(0,2)`,
`(0,1)`.

As with A2 and A3, the finite mask bookkeeping is taken as hypotheses rather than proved in
general; each is a concrete computation that `decide` discharges where the lemma is used. -/

/-- First of the two colours other than `c`. -/
def oth1 : Fin 3 → Fin 3
  | 0 => 1
  | 1 => 0
  | 2 => 0

/-- Second of the two colours other than `c`. -/
def oth2 : Fin 3 → Fin 3
  | 0 => 2
  | 1 => 2
  | 2 => 1

theorem oth1_ne (c : Fin 3) : oth1 c ≠ c := by fin_cases c <;> decide

theorem oth2_ne (c : Fin 3) : oth2 c ≠ c := by fin_cases c <;> decide

theorem oth12_ne (c : Fin 3) : oth1 c ≠ oth2 c := by fin_cases c <;> decide

/-- A product over the three colours, split at `c`. -/
theorem prod_fin3_split {M : Type} [CommMonoid M] (f : Fin 3 → M) (c : Fin 3) :
    ∏ x : Fin 3, f x = f c * f (oth1 c) * f (oth2 c) := by
  fin_cases c <;> simp [Fin.prod_univ_three, oth1, oth2] <;> try ring

/-- The general exactness row, indexed by a colouring and the masks of its classes. -/
theorem prod_hafM_eq_zero {W : WeightsN 8 3 α} (hW : IsDiagonal W) (hEq : EqSystemNZ 8 3 W)
    (ι : V 8 → Fin 3) (m : Fin 3 → Nat)
    (hm : ∀ c, (vertices 8).filter (fun v => decide (ι v = c)) = maskToList (m c))
    (hne : ¬ allEqual ι) :
    ∏ c : Fin 3, hafM W c (m c) = 0 := by
  have h := prod_haf_eq_zero hW hEq ι hne
  rw [← h]
  exact Finset.prod_congr rfl fun c _ => by rw [hafM, ← hm c]

/-- Definition 3.1, as a predicate on the solution. Used to state the case hypothesis; the
support lemma below takes the witnessing split directly. -/
def IsFree (W : WeightsN 8 3 α) (z : V 8) (c : Fin 3) (y : V 8) : Prop :=
  ∀ m1 m2 : Nat,
    (∀ v : V 8, ¬ (m1.testBit v.val = true ∧ m2.testBit v.val = true)) →
    (∀ v : V 8, (m1.testBit v.val = true ∨ m2.testBit v.val = true) ↔ (v ≠ z ∧ v ≠ y)) →
    hafM W (oth1 c) m1 * hafM W (oth2 c) m2 = 0

/-- **Lemma 3.2 (FREE).** If some even split of `V' - y` has nonvanishing product, then the
edge from the solve site to `y` in colour `c` is zero.

`ι` is the word putting `c` on `{z, y}` and the other two colours on the split parts; `m`
records the three colour classes as masks. Both, and the fact that `ι` is not constant, are
finite data supplied by the caller. -/
theorem free_support {W : WeightsN 8 3 α} (hW : IsDiagonal W) (hEq : EqSystemNZ 8 3 W)
    {c : Fin 3} {mzy m1 m2 : Nat} {ι : V 8 → Fin 3} {m : Fin 3 → Nat}
    (hmc : m c = mzy) (hm1 : m (oth1 c) = m1) (hm2 : m (oth2 c) = m2)
    (hfilter : ∀ x, (vertices 8).filter (fun v => decide (ι v = x)) = maskToList (m x))
    (hne : ¬ allEqual ι)
    (hprod : hafM W (oth1 c) m1 * hafM W (oth2 c) m2 ≠ 0) :
    hafM W c mzy = 0 := by
  have hz := prod_hafM_eq_zero hW hEq ι m hfilter hne
  rw [prod_fin3_split (fun x => hafM W x (m x)) c, hmc, hm1, hm2, mul_assoc] at hz
  exact (mul_eq_zero.mp hz).resolve_right hprod

/-- **C0.** The clause the encoder emits for a site that is not free. -/
theorem c0_sound {W : WeightsN 8 3 α} {a : Rup.Assign} (hW : IsDiagonal W)
    (hEq : EqSystemNZ 8 3 W)
    (ha : ∀ d : Fin 3, ∀ k : Nat, a (pvar d k) = baseAssign W d k)
    {c : Fin 3} {mzy m1 m2 : Nat} {ι : V 8 → Fin 3} {m : Fin 3 → Nat}
    (hmc : m c = mzy) (hm1 : m (oth1 c) = m1) (hm2 : m (oth2 c) = m2)
    (hfilter : ∀ x, (vertices 8).filter (fun v => decide (ι v = x)) = maskToList (m x))
    (hne : ¬ allEqual ι)
    (hprod : hafM W (oth1 c) m1 * hafM W (oth2 c) m2 ≠ 0) :
    Rup.SatClause a [(pvar c mzy, false)] :=
  ⟨_, List.mem_singleton_self _,
    satLit_neg ha (free_support hW hEq hmc hm1 hm2 hfilter hne hprod)⟩

end N8Diagonal