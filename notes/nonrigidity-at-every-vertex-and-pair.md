# Rigidity is impossible: every vertex, every colour pair

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  This does **not** decide
\((8,3)\); it is a satisfiable constraint, met by the guards below and by the
\((4,3)\) solutions.

## 1. The theorem

Fix a vertex \(v\), a colour \(c\), and the complementary pair
\(\{a,b\}=\{0,1,2\}\setminus\{c\}\).  Expanding the matching sum along \(v\) at
a word carrying \(c\) at \(v\) and letters from \(\{a,b\}\) elsewhere gives a
cofactor lying entirely inside the \(\{a,b\}\) block, so the **cross row**

\[
 \rho^c_v=\bigl(A(v,u)[c][d]\bigr)_{u\neq v,\ d\in\{a,b\}}\in\mathbb C^{14}
\]

must lie in the kernel of a map \(\Phi^{ab}_v\) built from the \(\{a,b\}\)
binary restriction alone.

> **Theorem.**  In any solution, \(\ker\Phi^{ab}_v\neq0\) for **every** vertex
> \(v\) and **every** colour pair.  All \(24\) places are non-rigid.

**It is not an eight-vertex statement.**  The proof uses \(d\geq3\) in exactly
two places — the cross row and head \(Z^c(v,v')\) must exist, and \(c^n\) must
be a target-one word — and uses \(n=8\) nowhere.  It holds for every even
\(n\geq4\) and every \(d\geq3\).

## 2. Proof

1. **Null row.**  Every such word is non-constant, so \(T=0\); the cofactors
   never leave the \(\{a,b\}\) block.  Hence \(\ker\Phi^{ab}_v=0\) forces
   \(\rho^c_v=0\).
2. **A dead partner gives two kernel dimensions.**  The entry of
   \(\Phi^{ab}_v\) at row \(\hat w\), column \((u,d)\) is
   \([\hat w_u=d]\cdot\operatorname{haf}(B[V\setminus\{v,u\}];\hat w)\), and the
   cofactor does not depend on the letter at \(u\).  So a dead pair zeroes
   *both* columns at \(u\).
3. **The tail dies term by term.**  At a level-two word — \(c\) exactly at
   \(v,v'\) — every matching either contains \(\{v,v'\}\), the head, or matches
   \(v\) to some \(u\notin\{v,v'\}\), and then its monomial contains the
   *literal cell* \(A(v,u)[c][\hat w_u]\), which is one of the fourteen cells of
   \(\rho^c_v\).  So \(\rho^c_v=0\) alone kills the tail, with **no hypothesis
   on \(v'\)**.
4. **The anchor.**  \(\operatorname{haf}(Z^c)=1\), so expanding along row \(v\)
   gives some \(Z^c(v,u)\neq0\); by step 3 that single \(u\) is dead.
   Contradiction.

**Nothing cancels.**  Step 3 is a term-by-term vanishing — every tail monomial
carries a zero factor — so complex cancellation, the central difficulty
everywhere else in this project, never enters.  Step 4 needs **one** live
partner, not all of them.

## 3. What it costs, and what it buys

**The rigid arm is empty.**  The dichotomy "all colour-pair restrictions rigid
\(\Rightarrow\) every cross cell zero \(\Rightarrow\) monochromatic" is a valid
implication whose hypothesis now fails at each of the \(24\) places
individually.  The implication is not withdrawn; it is **vacuous**.  All of
\((8,3)\) is the non-rigid branch.

**No binary block may be rigid anywhere.**  So the \(E/O\) free-side family —
rigid at four vertices — cannot be a colour-pair block of a solution, and the
"\(\geq16\) parameters, no finite classification" objection does not threaten
\((8,3)\).

## 4. Calibration, which is the real evidence

* **At \(d=2\) the statement is false, correctly.**  The free-side member is a
  genuine \((8,2)\) solution, rigid at all four odd vertices.  There is no
  third colour, no anchor, and no theorem — the proof does not accidentally
  apply.
* **At \((4,3)\), where solutions provably exist, the theorem holds via
  exactly the branch the proof predicts.**  On the \(K_4\) one-factorization
  every \(\rho^c_v=0\), the unique \(Z^c\)-neighbour of \(v\) **is** dead, and
  \(\dim\ker=2\).  A theorem that is true and non-vacuous where solutions exist
  is far better evidence than one stated only where nothing is known.

## 5. Structure established alongside

* **Row-linearity.**  With the \(189\) cells off \(v\) fixed, the whole
  \(6561\)-equation system is **linear** in the \(63\) cells at \(v\), splitting
  into \(24\) blocks of \(2187\times21\), block \((v,c)\) carrying the single
  target row \(c^8\); each cell lies in exactly two blocks
  (\(24\cdot21=504=2\cdot252\)).
* **Level \(\leq2\) is everything.**  Since \(8<3\cdot3\), the system is exactly
  L0 \((765)\) + L1 \((2856)\) + L2 \((2940)\), incidences \(768/3072/5376\).
* **Free edge = dead pair.**  \(T\) is independent of a pair's cells iff
  \(\operatorname{haf}(A[V\setminus\{u,v\}];\cdot)\equiv0\).  This is the general
  invariant; \(E/O\) parity is a **sufficient condition** producing dead pairs,
  and still needs its own parity count — the general statement does not by
  itself imply it.
* **Refuted:** \(\ker\Phi_v\) is *not* the span of the dead directions, by an
  exact witness on the eight-cycle.

## 6. Guards

Three pairwise-Hamiltonian one-factors satisfy **all** \(768\) L0 and **all**
\(3072\) L1 conditions and fail exactly **\(4\) of \(5376\)** L2 conditions,
each with residual exactly \(1\); failing words \(11100221\) and \(21012011\).
No rewriting of a single vertex row repairs it — each inconsistency is
certified by two equations.  L1 holds *vacuously* there, the guard having no
cross cells.

A **non-monochromatic** variant also satisfies L0 and L1 and fails \(8\), all
at level two, so L0 + L1 does not force monochromaticity either.

## 7. What this does not say

1. Nothing about whether \((8,3)\) has a solution.  The constraint is
   satisfiable.
2. \(\ker\Phi^{ab}_v\) is not classified.  Bounds
   \(2\deg_D(v)\leq\dim\ker\leq12\) hold, but the upper bound is **not** sharp:
   no vertex has six dead partners, so \(\deg_D\leq5\), and
   \(\operatorname{rank}\Phi^{ab}_v\geq3\) gives \(\dim\ker\leq11\).  An earlier
   draft claimed the eight-cycle attained both bounds; it attains only the
   lower one, at \(6=2\cdot3\).
3. Whether L0 + L1 alone could tolerate a rigid vertex — i.e. whether the
   level-two hypothesis is genuinely needed — is open.

## 8. Audit

[`verify_nonrigidity_at_every_vertex_and_pair.py`](../computations/verify_nonrigidity_at_every_vertex_and_pair.py)
pins its model against both committed guard ledgers, then verifies each step as
a formal identity in all \(252\) cell variables, plus a reconstruction of all
\(6561\) rows from the literal eight-vertex matching tensor.  Stdlib only,
exact `Fraction`, zero bare asserts, passing `python3`, `-O` and `-I -S`,
byte-identical across hash seeds.  Thirteen injected faults all raise in both
modes.

**Independently audited**, by an agent that rebuilt the mathematics from the
definition in code sharing nothing with the checker.  Verdict: the theorem is
correct and established, with **no gap at step 3**.  It upgraded two sampled
checks to exhaustive — row-linearity at all \(8\) vertices \(\times\) all
\(6561\) words \((52{,}488\) identities\()\) and the tail-kill at all eight
vertices \((10{,}752)\) — re-ran the tail claim by direct evaluation at random
rationals as a separate code path to exclude a shared indexing bug, and
confirmed the guard to the last digit.  It refuted the sharpness claim in
item 2 above and supplied the two lemmas replacing it.
