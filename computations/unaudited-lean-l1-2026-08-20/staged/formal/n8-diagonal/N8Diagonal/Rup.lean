/-
UNAUDITED (lane L1 staging), 2026-08-20.
Part of `formal/n8-diagonal`; see that directory's README.md.
-/

/-!
# A kernel-reducible RUP proof checker

Lean's standard LRAT machinery (`Std.Tactic.BVDecide.Reflect.verifyCert`)
cannot be reduced by the kernel: its parser is built from `partial def`s, which
have no equational theory, and `Std.Tactic.BVDecide.LRAT.check` itself gets
stuck under `decide` even on a one-variable, two-clause, one-action instance at
`maxRecDepth 1000000`, while `#eval` on the same term returns `true`. Replaying
a refutation through it therefore costs `Lean.ofReduceBool` and
`Lean.trustCompiler`.

This file is a self-contained replacement. It has **no imports**: every
definition is structurally recursive over `List`, `Nat` or the clause store, so
`decide` discharges it in the kernel and the axiom closure stays
`[propext, Classical.choice, Quot.sound]`.

Scope: **RUP only**, no RAT. Every certificate this project consumes is RUP-only
(`encoder/gen_rup_core.py` refuses to emit otherwise), which is what keeps the
checker this small.

Deletions are simply ignored. Dropping a deletion only leaves more clauses in
the store, and every stored clause is entailed by the original formula, so the
invariant is untouched and soundness is unaffected. This removes the whole
clause-removal bookkeeping.

The clause store is a binary trie rather than an array. In the kernel `Array` is
a `List` wrapper, so indexed lookup is linear and the cost of a few thousand
hints against an eight-hundred-clause store dominates everything else; the trie
makes lookup logarithmic. Only *soundness* of the trie is proved — that anything
retrievable was put there. Completeness is not needed: a lookup that loses a
clause can only make the checker fail.
-/

namespace N8Diagonal.Rup

/-- A literal: a variable index together with the polarity that satisfies it. -/
abbrev Lit := Nat × Bool

/-- A clause is a disjunction of literals. -/
abbrev Clause := List Lit

/-- A total assignment of Booleans to variables. -/
abbrev Assign := Nat → Bool

/-- The literal falsified by exactly the assignments satisfying `l`. -/
def negLit (l : Lit) : Lit := (l.1, !l.2)

@[simp] theorem negLit_fst (l : Lit) : (negLit l).1 = l.1 := rfl
@[simp] theorem negLit_snd (l : Lit) : (negLit l).2 = !l.2 := rfl

/-- `a` satisfies the literal `l`. -/
def SatLit (a : Assign) (l : Lit) : Prop := a l.1 = l.2

/-- `a` satisfies the clause `c`. -/
def SatClause (a : Assign) (c : Clause) : Prop := ∃ l ∈ c, SatLit a l

/-- `a` satisfies every clause of `f`. -/
def SatAll (a : Assign) (f : List Clause) : Prop := ∀ c ∈ f, SatClause a c

/-- `f` has no satisfying assignment. -/
def Unsat (f : List Clause) : Prop := ∀ a, ¬ SatAll a f

theorem not_satLit_negLit {a : Assign} {l : Lit} (h : SatLit a l) :
    ¬ SatLit a (negLit l) := by
  intro h'
  rw [SatLit] at h
  rw [SatLit, negLit_fst, negLit_snd, h] at h'
  simp at h'

theorem satLit_negLit_of_not {a : Assign} {l : Lit} (h : ¬ SatLit a l) :
    SatLit a (negLit l) := by
  rw [SatLit, negLit_fst, negLit_snd]
  rw [SatLit] at h
  cases hb : a l.1 <;> cases hl : l.2 <;> simp_all

/-! ## The clause store

A binary trie on the index: index `0` sits at the root, `2k+1` in the left
subtree at index `k`, and `2k+2` in the right subtree at index `k`. Lookup is
logarithmic and structural on the tree.
-/

/-- A binary trie of clauses, indexed by `Nat`. -/
inductive Store where
  | leaf : Store
  | node : Store → Option Clause → Store → Store

/-- The left subtree, with `leaf` acting as an all-empty node. -/
def Store.left : Store → Store
  | .leaf => .leaf
  | .node l _ _ => l

/-- The value at the root. -/
def Store.val : Store → Option Clause
  | .leaf => none
  | .node _ v _ => v

/-- The right subtree, with `leaf` acting as an all-empty node. -/
def Store.right : Store → Store
  | .leaf => .leaf
  | .node _ _ r => r

/-- Retrieve the clause stored at an index. -/
def Store.get : Store → Nat → Option Clause
  | .leaf, _ => none
  | .node _ v _, 0 => v
  | .node l _ r, n + 1 => if n % 2 == 0 then l.get (n / 2) else r.get (n / 2)

@[simp] theorem Store.get_zero (t : Store) : t.get 0 = t.val := by
  cases t <;> rfl

theorem Store.get_succ (t : Store) (n : Nat) :
    t.get (n + 1) = if n % 2 == 0 then t.left.get (n / 2) else t.right.get (n / 2) := by
  cases t with
  | leaf => simp [Store.get, Store.left, Store.right]
  | node l v r => rfl

/-- Insert a clause at an index. `fuel` bounds the depth; `insert` supplies
enough for any index this project can produce. Running out of fuel loses the
clause, which is harmless — see the module docstring. -/
def insertAux : Nat → Store → Nat → Clause → Store
  | 0, t, _, _ => t
  | fuel + 1, t, i, c =>
      match i with
      | 0 => .node t.left (some c) t.right
      | n + 1 =>
          if n % 2 == 0 then .node (insertAux fuel t.left (n / 2) c) t.val t.right
          else .node t.left t.val (insertAux fuel t.right (n / 2) c)

/-- Insert a clause at an index. -/
def Store.insert (t : Store) (i : Nat) (c : Clause) : Store := insertAux 64 t i c

/-- Build a store from a list, placing the `i`-th clause at index `i`. -/
def ofListAux : Store → Nat → List Clause → Store
  | t, _, [] => t
  | t, i, c :: cs => ofListAux (t.insert i c) (i + 1) cs

/-- Build a store from a list, placing the `i`-th clause at index `i`. -/
def ofList (f : List Clause) : Store := ofListAux .leaf 0 f

/-! ## Store soundness

Only one direction is needed: everything retrievable was put there.
-/

theorem insertAux_sound :
    ∀ (fuel : Nat) (t : Store) (i : Nat) (c : Clause) (j : Nat) (x : Clause),
      (insertAux fuel t i c).get j = some x → t.get j = some x ∨ x = c := by
  intro fuel
  induction fuel with
  | zero => intro t i c j x h; exact Or.inl h
  | succ f ih =>
    intro t i c j x h
    cases i with
    | zero =>
      cases j with
      | zero =>
        right
        rw [insertAux] at h
        simp only [Store.get] at h
        exact (Option.some.inj h).symm
      | succ m =>
        left
        rw [insertAux] at h
        rw [Store.get_succ] at h ⊢
        simpa [Store.left, Store.right] using h
    | succ n =>
      rw [insertAux] at h
      cases j with
      | zero =>
        left
        rw [Store.get_zero]
        by_cases hn : n % 2 == 0 <;> simp [hn] at h ⊢ <;> exact h
      | succ m =>
        rw [Store.get_succ] at h ⊢
        by_cases hn : n % 2 == 0 <;> by_cases hm : m % 2 == 0 <;>
          simp only [hn, hm, if_true, if_false, Store.left, Store.right,
            Bool.false_eq_true] at h ⊢
        · rcases ih t.left (n / 2) c (m / 2) x h with h' | h'
          · exact Or.inl h'
          · exact Or.inr h'
        · exact Or.inl h
        · exact Or.inl h
        · rcases ih t.right (n / 2) c (m / 2) x h with h' | h'
          · exact Or.inl h'
          · exact Or.inr h'

theorem insert_sound (t : Store) (i : Nat) (c : Clause) (j : Nat) (x : Clause)
    (h : (t.insert i c).get j = some x) : t.get j = some x ∨ x = c :=
  insertAux_sound 64 t i c j x h

theorem ofListAux_sound :
    ∀ (cs : List Clause) (t : Store) (i : Nat) (j : Nat) (x : Clause),
      (ofListAux t i cs).get j = some x → t.get j = some x ∨ x ∈ cs := by
  intro cs
  induction cs with
  | nil => intro t i j x h; exact Or.inl h
  | cons c rest ih =>
    intro t i j x h
    rw [ofListAux] at h
    rcases ih (t.insert i c) (i + 1) j x h with h' | h'
    · rcases insert_sound t i c j x h' with h'' | h''
      · exact Or.inl h''
      · exact Or.inr (by simp [h''])
    · exact Or.inr (List.mem_cons_of_mem _ h')

theorem ofList_sound (f : List Clause) (j : Nat) (x : Clause)
    (h : (ofList f).get j = some x) : x ∈ f := by
  rcases ofListAux_sound f .leaf 0 j x h with h' | h'
  · simp [Store.get] at h'
  · exact h'

/-! ## The checker -/

/-- A single RUP step: the derived clause, and the ordered hints (indices into the
clause store) that unit-propagate to a conflict. -/
structure Step where
  clause : Clause
  hints : List Nat
  deriving Inhabited

/-- Drop from `c` the literals falsified by the partial assignment `α`. -/
def reduceClause (α : List Lit) (c : Clause) : Clause :=
  c.filter (fun l => !(α.contains (negLit l)))

/-- Unit propagation along the hint list, from the partial assignment `α`.
Returns `true` exactly when a hint clause becomes empty, i.e. a conflict. -/
def propagate (store : Store) : List Lit → List Nat → Bool
  | _, [] => false
  | α, h :: hs =>
      match store.get h with
      | none => false
      | some c =>
          match reduceClause α c with
          | [] => true
          | [u] => propagate store (u :: α) hs
          | _ => false

/-- Check one step: assume the derived clause false, then propagate. -/
def checkStep (store : Store) (s : Step) : Bool :=
  propagate store (s.clause.map negLit) s.hints

/-- Replay the proof, growing the store. Succeeds when the empty clause is derived. -/
def run (store : Store) : Nat → List Step → Bool
  | _, [] => false
  | i, s :: rest =>
      if checkStep store s then
        match s.clause with
        | [] => true
        | _ => run (store.insert i s.clause) (i + 1) rest
      else
        false

/-- Check a RUP refutation of `f`. -/
def check (f : List Clause) (steps : List Step) : Bool :=
  run (ofList f) f.length steps

/-! ## Soundness -/

theorem satClause_reduceClause {a : Assign} {α : List Lit} {c : Clause}
    (hα : ∀ l ∈ α, SatLit a l) (hc : SatClause a c) :
    SatClause a (reduceClause α c) := by
  obtain ⟨l, hl, hsat⟩ := hc
  refine ⟨l, ?_, hsat⟩
  rw [reduceClause, List.mem_filter]
  refine ⟨hl, ?_⟩
  have hnot : ¬ (negLit l ∈ α) := fun hmem => not_satLit_negLit hsat (hα _ hmem)
  simpa using hnot

/-- The store invariant: every retrievable clause is satisfied. -/
def StoreSat (a : Assign) (t : Store) : Prop :=
  ∀ j x, t.get j = some x → SatClause a x

theorem propagate_sound {a : Assign} {store : Store} (hstore : StoreSat a store) :
    ∀ (hints : List Nat) (α : List Lit), (∀ l ∈ α, SatLit a l) →
      propagate store α hints = true → False := by
  intro hints
  induction hints with
  | nil => intro α _ h; simp [propagate] at h
  | cons h hs ih =>
    intro α hα hrun
    rw [propagate] at hrun
    split at hrun
    · simp at hrun
    · rename_i c hget
      have hred : SatClause a (reduceClause α c) :=
        satClause_reduceClause hα (hstore _ _ hget)
      split at hrun
      · rename_i hr
        rw [hr] at hred
        obtain ⟨l, hl, _⟩ := hred
        simp at hl
      · rename_i u hr
        rw [hr] at hred
        obtain ⟨l, hl, hsat⟩ := hred
        have hlu : l = u := by simpa using hl
        subst hlu
        refine ih (l :: α) ?_ hrun
        intro x hx
        rcases List.mem_cons.mp hx with rfl | hx'
        · exact hsat
        · exact hα _ hx'
      · simp at hrun

theorem checkStep_sound {a : Assign} {store : Store} {s : Step}
    (hstore : StoreSat a store) (h : checkStep store s = true) :
    SatClause a s.clause := by
  refine Classical.byContradiction fun hcon => ?_
  refine propagate_sound hstore s.hints (s.clause.map negLit) ?_ h
  intro l hl
  obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hl
  refine satLit_negLit_of_not ?_
  intro hsat
  exact hcon ⟨x, hx, hsat⟩

theorem run_sound {a : Assign} :
    ∀ (steps : List Step) (store : Store) (i : Nat),
      StoreSat a store → run store i steps = true → False := by
  intro steps
  induction steps with
  | nil => intro store i _ h; simp [run] at h
  | cons s rest ih =>
    intro store i hstore hrun
    rw [run] at hrun
    split at hrun
    · rename_i hchk
      have hsat : SatClause a s.clause := checkStep_sound hstore hchk
      split at hrun
      · rename_i hc
        rw [hc] at hsat
        obtain ⟨l, hl, _⟩ := hsat
        simp at hl
      · refine ih (store.insert i s.clause) (i + 1) ?_ hrun
        intro j x hj
        rcases insert_sound store i s.clause j x hj with h' | h'
        · exact hstore _ _ h'
        · exact h' ▸ hsat
    · simp at hrun

/-- **Soundness.** If `check f steps` succeeds then `f` is unsatisfiable. -/
theorem check_sound (f : List Clause) (steps : List Step) (h : check f steps = true) :
    Unsat f := by
  intro a hsat
  refine run_sound (a := a) steps (ofList f) f.length ?_ h
  intro j x hj
  exact hsat x (ofList_sound f j x hj)

end N8Diagonal.Rup
