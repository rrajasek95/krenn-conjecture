# The prolonged cascade is φ-closed for commuting source-valid derivations

Companions:
[`h3-descent-defect-row-space-invisibility.md`](h3-descent-defect-row-space-invisibility.md)
(rows cannot cancel the descent defect, under stated hypotheses) and
[`h3-source-valid-tower-first-obstruction.md`](h3-source-valid-tower-first-obstruction.md)
(T1: no source-valid tower admits the template; T2: φ bites first at
order four; T3: 360 distinct residuals).  Model and conventions are the
fourth-Hasse audit's
([`h3-full-hasse-cone-d4-descent-obstruction.md`](h3-full-hasse-cone-d4-descent-obstruction.md)):
\(A=H_m\), \(B=H_0-u\), \(I=(A,B)\), cap \(dT=-Yw\), \(d\rho=w\),
\(\operatorname{tgt}(T)=1\), \(\operatorname{ores}_{\rm cap}(T)=0\)
(fourth-Hasse (9)), \(\operatorname{ores}_{\rm cap}(\rho)=1\) (the
tgt/ores table of
[`h3-full-hasse-koszul-cap-totalization.md`](h3-full-hasse-koszul-cap-totalization.md)),
target \(R\)-linear (the \(r_0[\varnothing]\)-coefficient), and one
selection's four marked directions \(J\).

**Status of this result.**  The theorem below is a **hand proof** whose
inputs are machine-verified by
`computations/verify_h3_prolonged_cascade_phi_closure.py`.  The universal
quantifier over towers is not machine-verified, and per the project's
discipline this note is a research reduction until independently
audited.  Krenn's conjecture remains open.

## Theorem (cascade φ-closure)

Fix one fourth-Hasse selection and extend the bounded physical complex by
the squarefree jet lattice of **any** four commuting source-valid
derivations \(D_1,\dots,D_4\) in the marked directions
(\(D_i(I)\subseteq I\); prolonged differential
\(d\,r[U]=\sum_{S\subseteq U}D_S(f)\,e_0[U\setminus S]\) with
\(D_S=\prod_{i\in S}D_i\), and — load-bearing hypothesis — the
differential is **\(R\)-linear on coefficients**,
\(d(a\,r[U])=a\,d(r[U])\), which is the committed model's convention
(`module_scale_polynomial` in the fourth-Hasse checker).  A
coefficient-prolonging convention \(d(a\,r[U])=\sum_SD_S(a)(dr)[U\setminus
S]\) would break Step 3's induction and is excluded; it is exactly where
a genuine Spencer lift would differ).  The restriction "in the marked
directions" is not used by the proof — the theorem holds for any four
commuting source-valid derivations; the marked case is the instance of
interest.  Then no chain

\[
 n=\sum_Ua_U\,r_0[U]+\sum_Ub_U\,r_m[U]+\alpha T+\beta\rho
   \;(+\ \text{strict chart cycles})
\]

satisfies \(dn=Yw\), \(\operatorname{tgt}(n)=0\),
\(\operatorname{ores}(n)=0\).

**Consequence, stated precisely.**  Every escape through the squarefree
four-direction prolonged lattice of commuting source-valid derivations is
closed — including, by the mixed-chain paragraph below, chains that also
carry rows satisfying the row-space theorem's hypotheses.  What remains
open: the **denominator attaching cell** (the chart-decoration fork of
[`h3-denominator-face-decoration-fork.md`](h3-denominator-face-decoration-fork.md)),
multiset and cross-selection lattices (sketched only, Scope 2), and rows
with a φ-surviving edge-degree-0 boundary term (the Spencer-unit
question, Scope 3).  The count of open escapes is **not** reduced to
one; what this theorem does is close the prolonged-lattice escape
completely within its hypotheses.

## Proof

**Step 1 (cap bookkeeping).**  The \(w\)-slot of \(dn\) is
\(-\alpha Yw+\beta w\) (denominator attachment excluded by hypothesis —
it is the fork's other branch).  \(dn=Yw\) forces
\(-\alpha Y+\beta=Y\); \(\operatorname{ores}(n)=\beta=0\); hence
\(\alpha=-1\).  Target zero then forces
\(a_\varnothing=-\alpha\cdot\operatorname{tgt}(T)=1\).  Chart cycles have
zero boundary; their target vanishes under the \(R\)-linear convention,
and their cap ordinary residue is taken to vanish — no artifact defines
\(\operatorname{ores}\) on the chart summand, so this is a stated
convention, flagged in Scope.

**Step 2 (output equations).**  For each jet mask \(V\), the
\(e_0[V]\)-coefficient of \(dn\) must vanish:

\[
 \sum_{U\supseteq V}a_U\,D_{U\setminus V}(B)
 +\sum_{U\supseteq V}b_U\,D_{U\setminus V}(A)=0.
\]

**Step 3 (φ-shadow).**  \(\varphi(I)\subseteq(\bar B)\) with
\(\bar B=\varphi(B)=B\) (it is mdeg-0; checked).  Write
\(\varphi D_S(B)=g_S\bar B\), \(\varphi D_S(A)=h_S\bar B\) for
\(S\ne\varnothing\) (defined by source-validity), and note
\(\varphi(A)=0\), \(\varphi(D_\varnothing B)=\bar B\).  By the T2
filtration, \(h_S=0\) for \(1\le|S|\le3\): in the multilinear expansion
over a squarefree monomial, consuming fewer than four edges leaves a bare
\(\varphi(e)=0\) factor.  Since \(|U\setminus V|\le3\) whenever
\(V\ne\varnothing\), the \(b\)-terms drop from every
\(V\ne\varnothing\) equation, which after dividing by \(\bar B\) reads

\[
 \varphi(a_V)+\sum_{U\supsetneq V}\varphi(a_U)\,g_{U\setminus V}=0.
\]

This system is **unitriangular** over the mask poset: top-down induction
from the maximal support gives \(\varphi(a_U)=0\) for all
\(U\ne\varnothing\).  (The checker verifies unitriangularity of the 15-equation system from
its construction and solves a *planted inhomogeneous* system two
independent ways — poset back-substitution and dense Gaussian
elimination — requiring agreement; uniqueness then yields the
homogeneous-zero conclusion.  An earlier draft ran the homogeneous
back-substitution, which returns zero for every input; the audit caught
that as vacuous.)

**Step 4 (the \(V=\varnothing\) equation).**  With
\(\varphi(a_U)=0\) (\(U\ne\varnothing\)), \(a_\varnothing=1\), and
\(\varphi(A)=0\), the φ-image of the \(V=\varnothing\) equation is

\[
 \bar B+\sum_{|U|=4}\varphi(b_U)\,h_U\bar B=0
 \qquad\Longrightarrow\qquad
 1+\sum_{|U|=4}\varphi(b_U)\,h_U=0 .
\]

**Step 5 (divisibility lemma).**  *For any derivation \(D\) with
\(D(A)\in I\), the pure part \(P_e=\varphi(D(e))\) of every edge \(e\)
occurring in \(A\) lies in \((\bar B)\).*  Proof: \(A\) is a polynomial
in mixed edges only (checked), so \(D(A)=\sum_eD(e)\,\partial_eA\) over
\(A\)'s edges.  Mixed-degree is a ring grading; \(A\) is mdeg-4 and \(B\)
mdeg-0 homogeneous (checked), so the mdeg-3 component of \(I\) is
\(q_3B\) and the mdeg-3 component of \(D(A)\) is
\(\sum_eP_e\,\partial_eA\).  The 360 residuals are pairwise distinct
(checked), so matching the coefficient of the residual
\(M\setminus\{e\}\) — which the checker performs symbolically with formal
\(P_e\), through the actual derivative code — gives
\(P_e=\gamma_{M\setminus e}\bar B\in(\bar B)\).  \(\square\)

**Step 5b (mixed chains: jets plus rows).**  A chain may carry the
prolonged generators *and* target-zero rows \(\rho_i\) satisfying the
row-space theorem's hypotheses (\(e_0\)-coefficients \(\beta_i\) with
every monomial of \(\varphi(\beta_i)\) of edge-degree \(\ge1\)).
Neither companion covers this case alone, so it is proved here.  Steps
1–3 are unchanged (the rows do not enter the \(w\)-slot, the target, or
the jet slots \(V\ne\varnothing\)).  The \(V=\varnothing\) equation
becomes

\[
 \bar B\Bigl(1+\sum_{|U|=4}\varphi(b_U)h_U\Bigr)
 +\sum_i\varphi(c_i)\varphi(\beta_i)=0 .
\]

Take edge-degree-0 parts.  The row sum contributes nothing (every
monomial has edge-degree \(\ge1\)).  With \(h_U\in(\bar B^3)\) (Step
6), \(\bar B\sum\varphi(b_U)h_U\in(\bar B^4)\), whose edge-degree-0
part is \(p(u)\,u^4\); and the edge-degree-0 part of \(\bar B\) is
\(-u\).  So the equation's edge-degree-0 part reads
\(-u+p(u)u^4=0\), impossible: the coefficient of \(u^1\) is \(-1\).
This argument is due to the independent audit of the first draft.

**Step 6 (contradiction).**  Every φ-surviving term of
\(\varphi(D_U(A))\), \(|U|=4\), is a product of four order-one pure parts
(T2 again: all four edges must be consumed at order one), each in
\((\bar B)\) by Step 5 — the order-one component of each direction is
itself a source-valid derivation, being the \(n=1\) case.  So
\(\varphi(D_U(A))\in(\bar B^4)\) and \(h_U\in(\bar B^3)\subseteq(\bar B)\).
Step 4 then demands \(-1\in(\bar B)\).  But \(\bar B\) is nonzero with no
constant term (checked), so a constant multiple of \(\bar B\) is zero.
Contradiction.  \(\blacksquare\)

## The example that shows the theorem is sharp in the right way

The tower \(D_i=B\,\partial_{z_i}\) is source-valid
(\(D_i(B)=B\,\partial_{z_i}B=0\) since the marked directions annihilate
\(B\) — checked on all fifteen selections — and
\(D_i(A)=B\,\partial_{z_i}A\in I\)), and its directions commute.  Its
template is a cycle and the coupled chain delivers boundary
\(B^4Yw\) — both **definitional for this tower** (the checker verifies
\(D_i(B)=0\) and \(\partial_JA=1\) on all selections and does *not*
re-verify the cycle property, which follows by the two-line cancellation
\(D_S(B)=0\) for \(S\ne\varnothing\)).  The boundary is an
\(I\)-multiple of the class, vanishing on the source quotient.  So source-valid towers exist and produce the
template; what they can never produce is the *unit*, exactly as T1 and
this theorem require.

## Scope

1. One selection's squarefree four-direction lattice; commuting
   derivations; the fourth-Hasse cap model, \(R\)-linear target, and
   \(R\)-linear prolonged differential on coefficients; the cap
   ordinary residue is taken to vanish on the chart summand (a stated
   convention — no artifact defines it there); denominator attachment
   excluded by hypothesis (it is the fork's other branch, not an
   omission).
2. Multiset lattices (higher order per direction) and cross-selection
   combinations are not formalized.  For multiset lattices the same
   argument applies — the surviving φ-terms at total order four are
   still products of four order-one values — but this is a sketch, not a
   proof, and is excluded from the theorem statement.
3. Rows outside the row-space theorem's hypotheses (a φ-surviving
   edge-degree-0 boundary term) remain the Spencer-unit question; they
   are not part of the prolonged lattice treated here.
4. The theorem is a hand proof; the checker verifies its inputs, the
   symbolic residual extraction, the unitriangular solve, and the
   example tower.  Krenn's conjecture remains open.

## Verification

Run

~~~text
python3 computations/verify_h3_prolonged_cascade_phi_closure.py
python3 -O computations/verify_h3_prolonged_cascade_phi_closure.py
python3 -I computations/verify_h3_prolonged_cascade_phi_closure.py
python3 -S computations/verify_h3_prolonged_cascade_phi_closure.py
python3 -I -S computations/verify_h3_prolonged_cascade_phi_closure.py
~~~

Runtime is under one second.  The ledger binds the geometry (a content
hash of the \(H_m\) and \(H_0-u\) monomial sets), and the mixed word and
direct-free pair of the imported model are pinned by explicit requires.
Frozen ledger digest:

~~~text
43a9a4aab4d6be92290058c6b12fcd106841636e575dcd113d55b6d78d9ec3fd
~~~

Mutation-tested: perturbing the symbolic-extraction coefficient, the
constant-term check, the mdeg table, the \(\partial_JA=1\) check, the
solver's \(g\)-index or accumulation sign, the imported model's
direct-free pair, and its mixed word each raise under both `python3`
and `python3 -O`, with a message naming the broken property.
