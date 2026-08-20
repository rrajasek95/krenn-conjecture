/-
UNAUDITED — lane L1, 2026-08-20, pinned krenn-conjecture HEAD f9a3bd6.
Scratch: lives inside a throwaway formal-conjectures clone. Not a PR.
-/
import N8Diagonal.Haf

/-!
# Hafnians are symmetric functions

`haf W c L` is defined on a list and `haf_cons'` expands at its head. The A3
clause family expands at *every* site of a set, which needs invariance of `haf`
under permuting `L`. That is false for a general `WeightsN` — the registry's `W`
is an arbitrary function on `EdgeN` and need not satisfy
`W ⟨u,v,i,j⟩ = W ⟨v,u,j,i⟩` — so it is bought here from an explicit endpoint
symmetry hypothesis.

Measured: A3 at every site is load-bearing at `N = 8` (head-only A3 leaves
0/87 orbits refuted) though not at `N = 6` (13/13 survive). See
`REHEARSAL.md` §3.2.
-/

namespace MonochromaticQuantumGraph

variable {α : Type} [CommSemiring α] {N D : Nat}

/-- Endpoint symmetry, off the diagonal. Diagonal labels `e.u = e.v` are never read by
`pmSumList` on a duplicate-free list, so they are excluded. -/
def IsSymm (W : WeightsN N D α) : Prop :=
  ∀ e : EdgeN N D, e.u ≠ e.v → W e = W ⟨e.v, e.u, e.j, e.i⟩

variable {W : WeightsN N D α}

/-- A scalar pulls into a mapped sum. -/
private theorem mul_sum_map {β : Type} [NonUnitalNonAssocSemiring β]
    (l : List (V N)) (k : β) (g : V N → β) :
    k * (l.map g).sum = (l.map (fun v => k * g v)).sum := by
  induction l with
  | nil => simp
  | cons a t iht => simp [mul_add, iht]

/-- A mapped sum of sums splits. -/
private theorem sum_map_add {β : Type} [AddCommMonoid β]
    (l : List (V N)) (f g : V N → β) :
    (l.map (fun u => f u + g u)).sum = (l.map f).sum + (l.map g).sum := by
  induction l with
  | nil => simp
  | cons a t iht => simp only [List.map_cons, List.sum_cons, iht]; abel

/-- Peeling the head off a double sum over ordered distinct pairs. -/
private theorem double_peel {β : Type} [AddCommMonoid β]
    {a : V N} {t : List (V N)} (hat : a ∉ t) (G : V N → V N → β) :
    ((a :: t).map (fun u => (((a :: t).erase u).map (fun v => G u v)).sum)).sum
      = ((t.map (fun v => G a v)).sum + (t.map (fun u => G u a)).sum)
        + (t.map (fun u => ((t.erase u).map (fun v => G u v)).sum)).sum := by
  have hpeel : ∀ u ∈ t,
      (((a :: t).erase u).map (fun v => G u v)).sum
        = G u a + ((t.erase u).map (fun v => G u v)).sum := by
    intro u hu
    have hua : u ≠ a := fun h => hat (h ▸ hu)
    rw [List.erase_cons_tail (by simpa using hua.symm), List.map_cons, List.sum_cons]
  rw [List.map_cons, List.sum_cons, List.erase_cons_head,
    List.map_congr_left (l := t)
      (g := fun u => G u a + ((t.erase u).map (fun v => G u v)).sum) hpeel,
    sum_map_add, ← add_assoc]

/-- **The double sum over ordered distinct pairs is symmetric.** -/
private theorem sum_erase_swap {β : Type} [AddCommMonoid β] :
    ∀ (l : List (V N)), l.Nodup → ∀ (F : V N → V N → β),
      (l.map (fun u => ((l.erase u).map (fun v => F u v)).sum)).sum
        = (l.map (fun u => ((l.erase u).map (fun v => F v u)).sum)).sum := by
  intro l
  induction l with
  | nil => intro _ _; simp
  | cons a t iht =>
    intro hnd F
    have hat : a ∉ t := (List.nodup_cons.1 hnd).1
    have hndt : t.Nodup := (List.nodup_cons.1 hnd).2
    rw [double_peel hat (fun u v => F u v), double_peel hat (fun u v => F v u),
      iht hndt F, add_comm ((t.map (fun v => F a v)).sum)]

/-- **Adjacent transposition.** Swapping the first two sites of a duplicate-free list
leaves the hafnian unchanged. -/
theorem haf_swap (hs : IsSymm W) (c : Fin D) {a b : V N} {l : List (V N)}
    (hnd : (a :: b :: l).Nodup) :
    haf W c (a :: b :: l) = haf W c (b :: a :: l) := by
  have h1 := (List.nodup_cons.1 hnd).1
  have hab : a ≠ b := fun h => h1 (by simp [h])
  have hal : a ∉ l := fun h => h1 (by simp [h])
  have hbl : b ∉ l := (List.nodup_cons.1 (List.nodup_cons.1 hnd).2).1
  have hndl : l.Nodup := (List.nodup_cons.1 (List.nodup_cons.1 hnd).2).2
  -- expand twice on each side
  have expand : ∀ (x y : V N), x ∉ l → y ∉ l →
      haf W c (x :: y :: l) = W (mkEdge x y c c) * haf W c l
        + (l.map (fun u => ((l.erase u).map (fun v =>
            W (mkEdge x u c c) * (W (mkEdge y v c c) *
              haf W c ((l.erase u).erase v)))).sum)).sum := by
    intro x y _ hyl
    rw [haf_cons' W c x (y :: l), List.map_cons, List.sum_cons, List.erase_cons_head]
    congr 1
    rw [List.map_congr_left (l := l)
      (g := fun u => ((l.erase u).map (fun v =>
        W (mkEdge x u c c) * (W (mkEdge y v c c) *
          haf W c ((l.erase u).erase v)))).sum) ?inner]
    case inner =>
      intro u hu
      have huy : u ≠ y := fun h => hyl (h ▸ hu)
      rw [List.erase_cons_tail (by simpa using huy.symm), haf_cons' W c y (l.erase u),
        mul_sum_map]
  rw [expand a b hal hbl, expand b a hbl hal,
    hs (mkEdge a b c c) hab,
    sum_erase_swap l hndl (fun u v =>
      W (mkEdge a u c c) * (W (mkEdge b v c c) * haf W c ((l.erase u).erase v)))]
  congr 1
  refine congrArg List.sum (List.map_congr_left fun u _ => ?_)
  refine congrArg List.sum (List.map_congr_left fun v _ => ?_)
  rw [List.erase_comm]
  ring

/-- A summand may be peeled from anywhere in a mapped sum. -/
private theorem sum_map_erase {β : Type} [AddCommMonoid β] (f : V N → β) :
    ∀ (t : List (V N)) (w : V N), w ∈ t →
      (t.map f).sum = f w + ((t.erase w).map f).sum := by
  intro t
  induction t with
  | nil => intro w hw; simp at hw
  | cons a s ihs =>
    intro w hw
    by_cases h : w = a
    · subst h; simp
    · have hws : w ∈ s := by rcases List.mem_cons.1 hw with h' | h'; exact absurd h' h; exact h'
      rw [List.erase_cons_tail (by simpa using (Ne.symm h)), List.map_cons, List.sum_cons,
        List.map_cons, List.sum_cons, ihs w hws]
      abel

/-- **General-position Laplace.** Any site of a duplicate-free list may be moved to the
front without changing the hafnian, so the expansion may be taken at any site.

This is what the A3 clause family needs, and it is the reason the symmetrization layer
exists at all. -/
theorem haf_move_head (hs : IsSymm W) (c : Fin D) :
    ∀ (n : Nat) (L : List (V N)), L.length = n → L.Nodup → ∀ w ∈ L,
      haf W c L = haf W c (w :: L.erase w) := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro L hL hnd w hw
    match L with
    | [] => simp at hw
    | a :: t =>
      by_cases hwa : w = a
      · subst hwa; rw [List.erase_cons_head]
      · have hwt : w ∈ t := by
          rcases List.mem_cons.1 hw with h' | h'
          · exact absurd h' hwa
          · exact h'
        have hat : a ∉ t := (List.nodup_cons.1 hnd).1
        have hndt : t.Nodup := (List.nodup_cons.1 hnd).2
        have haw : a ≠ w := fun h => hwa h.symm
        have hnw : t.erase w |>.Nodup := hndt.erase w
        have hawl : a ∉ t.erase w := fun h => hat (List.mem_of_mem_erase h)
        rw [List.erase_cons_tail (by simpa using haw),
          haf_cons' W c a t, haf_cons' W c w (a :: t.erase w),
          List.map_cons, List.sum_cons, List.erase_cons_head,
          sum_map_erase (fun u => W (mkEdge a u c c) * haf W c (t.erase u)) t w hwt,
          hs (mkEdge a w c c) haw]
      -- the two head terms agree; the tails are the symmetric double sum
        have hn : n = t.length + 1 := by rw [← hL]; simp
        have hleft :
            ((t.erase w).map (fun u => W (mkEdge a u c c) * haf W c (t.erase u))).sum
              = ((t.erase w).map (fun u => (((t.erase w).erase u).map (fun v =>
                  W (mkEdge a u c c) * (W (mkEdge w v c c) *
                    haf W c (((t.erase w).erase u).erase v)))).sum)).sum := by
          refine congrArg List.sum (List.map_congr_left fun u hu => ?_)
          have hut : u ∈ t := List.mem_of_mem_erase hu
          have huw : u ≠ w := (hndt.mem_erase_iff.1 hu).1
          have hwtu : w ∈ t.erase u := (List.mem_erase_of_ne (Ne.symm huw)).2 hwt
          have hlen : (t.erase u).length < n := by
            have h := List.length_erase_of_mem hut
            have h2 : 1 ≤ t.length := List.length_pos_of_mem hut
            omega
          rw [ih _ hlen (t.erase u) rfl (hndt.erase u) w hwtu,
            haf_cons' W c w ((t.erase u).erase w), mul_sum_map, List.erase_comm]
        have hright :
            ((t.erase w).map (fun u =>
                W (mkEdge w u c c) * haf W c ((a :: t.erase w).erase u))).sum
              = ((t.erase w).map (fun u => (((t.erase w).erase u).map (fun v =>
                  W (mkEdge w u c c) * (W (mkEdge a v c c) *
                    haf W c (((t.erase w).erase u).erase v)))).sum)).sum := by
          refine congrArg List.sum (List.map_congr_left fun u hu => ?_)
          have hua : a ≠ u := fun h => hawl (h ▸ hu)
          rw [List.erase_cons_tail (by simpa using hua),
            haf_cons' W c a ((t.erase w).erase u), mul_sum_map]
        rw [hleft, hright, sum_erase_swap (t.erase w) hnw (fun u v =>
          W (mkEdge a u c c) * (W (mkEdge w v c c) *
            haf W c (((t.erase w).erase u).erase v)))]
        congr 1
        refine congrArg List.sum (List.map_congr_left fun u _ => ?_)
        refine congrArg List.sum (List.map_congr_left fun v _ => ?_)
        rw [List.erase_comm]
        ring

/-- **The A3 identity.** Laplace expansion of a hafnian at an arbitrary site.

This is the hypothesis of the A3 clause family: if every summand has a vanishing factor
then `haf W c L = 0`. -/
theorem haf_expand (hs : IsSymm W) (c : Fin D) {L : List (V N)} (hnd : L.Nodup)
    {w : V N} (hw : w ∈ L) :
    haf W c L = ((L.erase w).map (fun u =>
      W (mkEdge w u c c) * haf W c ((L.erase w).erase u))).sum := by
  rw [haf_move_head hs c L.length L rfl hnd w hw, haf_cons']

/-- The Boolean content of A3: a hafnian all of whose Laplace summands have a vanishing
factor is itself zero. -/
theorem haf_eq_zero_of_expand (hs : IsSymm W) (c : Fin D) {L : List (V N)} (hnd : L.Nodup)
    {w : V N} (hw : w ∈ L)
    (h : ∀ u ∈ L.erase w,
      W (mkEdge w u c c) = 0 ∨ haf W c ((L.erase w).erase u) = 0) :
    haf W c L = 0 := by
  rw [haf_expand hs c hnd hw]
  refine List.sum_eq_zero ?_
  intro x hx
  obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hx
  rcases h u hu with h' | h' <;> simp [h']

end MonochromaticQuantumGraph
