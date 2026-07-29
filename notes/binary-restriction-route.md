# Binary restrictions and the spin-flip cycle expansion

Fix color zero and, independently at every vertex, contract against the
two-parameter local state

\[
 e_0+z_v(e_1+t_ve_2).
\]

If a three-color matching tensor were `Delta_(B,3)`, the resulting scalar
matching polynomial would be

\[
 \operatorname{Haf}(p_{uv})
   =1+\left(1+\prod_{v\in B}t_v\right)\prod_{v\in B}z_v.     \tag{1}
\]

Every restricted edge has the endpoint-local form

\[
 p_{uv}=a_{uv}+b_{uv}(t_u)z_u+c_{uv}(t_v)z_v
              +d_{uv}(t_u,t_v)z_uz_v,                       \tag{2}
\]

where `b,c` are affine in their displayed variable and `d` is bilinear.
Pointwise classification at a fixed `t` cannot suffice: on a Hamilton cycle,
put the constant tensor on one alternating perfect matching and the full
`z` tensor on the other, and scale one latter edge by an arbitrary scalar
`lambda`.  This realizes `1+lambda prod z` for every `lambda`.  Any useful
invariant must retain the endpoint locality in (2) as `t` varies.

## 1. The binary spin-flip invariant

Let `V=C^2` with basis `e_0,e_1` and alternating form

\[
 \epsilon(e_0,e_1)=1,\qquad \epsilon(e_1,e_0)=-1.
\]

For binary tensors `T,S` on an even vertex set `B`, put

\[
 [T,S]=\epsilon^{\otimes B}(T,S)
 =\sum_{x\in\{0,1\}^B}(-1)^{|x|}T_xS_{\bar x}.              \tag{3}
\]

This form is symmetric because `|B|` is even.  In particular

\[
 [e_0^{\otimes B}+\lambda e_1^{\otimes B},
  e_0^{\otimes B}+\lambda e_1^{\otimes B}]=2\lambda.        \tag{4}
\]

Attach an arbitrary binary matrix `A_e` to every pair and, for a perfect
matching `M`, write `A_M=bigotimes_(e in M) A_e`.  Expanding both copies of
the hafnian gives

\[
 [H_B(A),H_B(A)]=\sum_{M,N\in\operatorname{PM}(B)}[A_M,A_N].\tag{5}
\]

The union of `M` and `N` is a disjoint union of even alternating cycles;
a common edge is regarded as a doubled 2-cycle.  Since (3) is a product over
vertices, the summand in (5) factors exactly:

\[
 [A_M,A_N]=\prod_{C\in\mathcal C(M,N)}\Gamma_C(M,N),         \tag{6}
\]

where

\[
 \Gamma_C(M,N)=
 \sum_{x\in\{0,1\}^C}(-1)^{|x|}
 \prod_{e=uv\in M|_C}(A_e)_{x_u x_v}
 \prod_{e=uv\in N|_C}(A_e)_{1-x_u,1-x_v}.                  \tag{7}
\]

For a doubled edge, `Gamma_C=2 det A_e`.  For a cycle ordered so that its
`M`-edges are `A_1,...,A_k` and its oppositely oriented `N`-edges are
`B_1,...,B_k`, the same contraction can be written

\[
 \Gamma_C=\operatorname{tr}\prod_{r=1}^k
             (J^T A_rJ)B_r,
 \qquad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.            \tag{8}
\]

Combining the two orders of every distinct pair gives the explicit invariant

\[
\boxed{
 \lambda=2^{|B|/2-1}\sum_M\prod_{e\in M}\det A_e
 +\sum_{\{M,N\},\,M\ne N}
       \prod_{C\in\mathcal C(M,N)}\Gamma_C(M,N).}            \tag{9}
\]

No rank-one, symmetry, support, or noncancellation assumption enters (9).

## 2. Endpoint-local form of the cycle factors

For (2), let `L_v(t_v):C^2 -> C^3` send the binary basis to
`e_0,e_1+t_ve_2`.  Then

\[
 A_{uv}(t_u,t_v)=L_u(t_u)^T X_{uv}L_v(t_v).
\]

The alternating form used at vertex `v` in (7) is carried to the bivector

\[
 L_v(t_v)e_0\wedge L_v(t_v)e_1
   =e_0\wedge e_1+t_v e_0\wedge e_2.                         \tag{10}
\]

Consequently every `Gamma_C` is a multiaffine polynomial in exactly the
variables at the vertices of `C`.  Equation (9) turns (1) into the exact
alternating-cycle identity

\[
 1+\prod_vt_v
 =2^{|B|/2-1}\sum_M\prod_{uv\in M}D_{uv}(t_u,t_v)
 +\sum_{\{M,N\},M\ne N}\prod_{C\in\mathcal C(M,N)}
        \Gamma_C(t_C),                                      \tag{11}
\]

with `D_uv=det A_uv`.  Thus all cancellation is now organized by unions of
two perfect matchings rather than by individual color coefficients.

There is one immediate exact restriction.  The Laurent polynomial
`1+prod_v t_v` is irreducible: viewed as a primitive degree-one polynomial
in any one `t_v`, this follows from Gauss' lemma.  Hence if a degeneration
or support argument isolates one nonzero summand on the right of (11), its
union must be one Hamilton alternating cycle.  A diagonal term factors over
the `|B|/2` doubled edges and is impossible, while a pair with two or more
cycle components factors over disjoint nonempty variable sets and is also
impossible.  More generally, any proof that separates the cycle summands
(for example by an auxiliary grading) reduces the open case to Hamilton
alternating pairs.

The remaining loophole is exact cancellation among several cycle-cover
summands in (11).  The identity alone does not yet show that one proper
excited-sector hafnian is nonzero, but it gives a precise scalar target for
that step.  `computations/verify_binary_spinflip_cycle_identity.py` audits
(3)--(7) over the integers at six vertices and checks (4) on an exact GHZ
example.

## 3. The all-subset loop gas and why the full target does not determine it

There is an exact exponential refinement of (5).  For every even subset
`S subseteq B`, let `H_S` be the matching tensor of the *induced* edge
system on `S`, and put

\[
 D_S=[H_S,H_S],\qquad D_\varnothing=1.                       \tag{12}
\]

Work in the square-free vertex algebra with basis symbols `u_S`, where
`u_Su_T=u_(S union T)` for disjoint supports and zero otherwise.  Define

\[
 \mathcal D=\sum_{S\text{ even}}D_Su_S.                     \tag{13}
\]

For nonempty even `S`, let `C_S` be the sum of `[A_M,A_N]` over the ordered
pairs of perfect matchings of `S` for which the multigraph `M union N` is
connected (a doubled edge is connected).  Unique decomposition of an
ordered pair into its alternating-cycle components, followed by the labeled
exponential formula, gives

\[
 \boxed{\mathcal D=\exp\left(\sum_{S\ne\varnothing}C_Su_S\right),
 \qquad \log\mathcal D=\sum_{S\ne\varnothing}C_Su_S.}        \tag{14}
\]

Thus the logarithm really does remove every multi-cycle contribution.  The
problem is that the full binary target does **not** determine the proper
coefficients `D_S`: `H_B=Delta_(B,2)` says nothing by itself about the
matching tensors of induced subnetworks.

There is a small exact obstruction to making that inference.  Start with
the signed six-vertex cancellation realization of `Delta_(6,2)` from
`computations/verify_cancellation_example.py`.  In zero-based labels its
four-site cofactor on `{1,2,3,5}` is the zero tensor.  Therefore one may add
the rank-two identity matrix on the missing edge `04`; the expansion by that
edge shows that the full six-site matching tensor remains exactly
`Delta_(6,2)`.  In particular all its proper excited coefficients still
vanish.  But on the induced two-site network

\[
 D_{\{0,4\}}=[I_2,I_2]=2\det(I_2)=2,                         \tag{15}
\]

so (14) has the nonzero proper connected term
`C_{\{0,4\}}=2`.  Hence one cannot replace the all-subset series by
`1+2lambda u_B` using only the full GHZ coefficient equations.

Removing tensor-inactive matrices still does not repair the inference.  A
stronger eight-edge example uses

\[
\begin{array}{c|c}
01&e_0e_0\\
23&e_0e_0+e_1e_1\\
02&-e_0e_1\\
13&e_0e_1\\
45&e_0e_0\\
05,12,34&e_1e_1.
\end{array}                                                   \tag{16}
\]

The first two supported matchings give

\[
 e_0e_0\,(e_0e_0+e_1e_1)e_0e_0
 -(e_0e_1)(e_0e_1)e_0e_0=e_0^{\otimes6},                   \tag{17}
\]

and the third gives `e_1^(tensor 6)`.  Thus (16) realizes
`Delta_(6,2)` exactly.  Every one of its eight matrices has a nonzero
four-site tensor cofactor (each edge lies in one of the three displayed
supported matchings, and the shared-edge cofactor is `e_0^(tensor4)`), so
deleting any matrix changes the full tensor.  Nevertheless `A_23=I_2`, and
therefore again

\[
 D_{\{2,3\}}=2\det A_{23}=2.                                \tag{18}
\]

Hence support-minimality in the tensor-active sense does not make the proper
induced double-dimer coefficients recoverable from the full target.  A
strengthened route needs a *relative* cluster expansion weighted by the
complementary vacuum hafnians, and even that expansion must retain enough
polarization to detect rank-one excited tensors (whose self spin-flip is
zero).  The inactive-edge example is checked in
`computations/verify_double_dimer_log_counterexample.py`; the stronger
active rank-two gadget (16) is checked in
`computations/verify_active_ranktwo_binary_gadget.py`.

## 4. Two overlapping active binary modules do not couple to three colors

The active gadget (16) can be treated as a nine-cell decorated module: the
eight underlying pairs carry nine nonzero cells because `A_23` has its two
diagonal entries.  Embed one copy on global colors `{0,1}` and a second copy
on `{0,2}`, after an arbitrary permutation of the six vertices.  Give every
displayed cell in each copy an arbitrary nonzero complex coefficient.  If
two copies land on the same decorated cell, aggregate them as required; the
two contributions are allowed to cancel exactly.

**Proposition 4.1 (pure two-module obstruction).**  No such superposition is
`Delta_(6,3)`, for any relative vertex permutation or nonzero coefficients.

Here is a finite exact proof.  For a fixed relative permutation, mark every
aggregate decorated cell as zero or nonzero.  A cell supplied by only one
module is forced nonzero; a coincident cell is allowed either status, which
is an overapproximation of every possible complex cancellation.  Discard a
status pattern if some constant coloring has no nonzero perfect-matching
term.  In every remaining pattern, some mixed coloring has exactly one
nonzero perfect-matching term.  That term is a product of three nonzero field
elements and cannot vanish or cancel.

There are only `6!=720` relative placements.  Across them there are `1344`
shared-cell status patterns in total, with at most three coincident decorated
cells in one placement.  Exact enumeration proves the preceding assertion;
it does not substitute numerical values for the coefficients and does not
assume that different matching terms vanish separately.  The audit is
`computations/verify_two_active_modules_obstruction.py`.  A pair sharing
colors `{0,1}` and `{1,2}` is the same statement after a global color
permutation.

The relative placement with the fewest initially unique mixed fibers is

\[
 (0,1,2,3,4,5)\quad\hbox{and}\quad(0,1,2,3,5,4).            \tag{19}
\]

Its union of underlying pairs is

\[
 U=\{01,02,04,05,12,13,23,34,35,45\}.                      \tag{20}
\]

This most promising overlap remains impossible even if the nine-cell module
ansatz is abandoned and every matrix on (20) is made an arbitrary asymmetric
`3 by 3` matrix.

**Proposition 4.2 (arbitrary-matrix obstruction on the best union).**  If
all matrices outside `U` vanish, then `H_6(A) != Delta_(6,3)`.

**Proof.**  Vertices `1,2,4,5` have exactly three allowed neighbors.  The
cubic-vertex lemma therefore makes every incident matrix a nonzero
same-color rank-one basis tensor, with three distinct incident colors at
each of those vertices.  Every edge of `U` meets one of these four cubic
vertices, so all ten matrices have this form.

The graph (20) has exactly four perfect matchings,

\[
\begin{aligned}
 M_A&=01|23|45,&M_B&=02|13|45,\\
 M_C&=04|12|35,&M_D&=05|12|34.                              \tag{21}
\end{aligned}
\]

Their induced colorings are pairwise distinct: at any cubic vertex, a color
selects a unique incident edge, so two matchings inducing the same coloring
would be equal.  Hence no two terms in (21) can cancel, and every one of the
four induced colorings would have to be constant.  But `M_A` and `M_B` share
edge `45`; if both were constant they would have the same constant color.
Then edges `01` and `13` would have that same color at cubic vertex `1`,
contradicting the three distinct incident colors there.  This proves the
claim. \(\square\)

The four-matchings and proper-edge-coloring conclusion are independently
enumerated by `computations/verify_best_module_support_obstruction.py` (there
are 144 proper assignments at the four cubic vertices).

Thus arbitrary extra color cells on the existing ten module pairs cannot
repair the best overlap.  Any further constructive coupling must introduce
new underlying pairs (and thereby leave this sparse module chart), or use
three or more modules in a way not reducible to a two-copy superposition.

In fact one new underlying pair is still insufficient.

**Proposition 4.3 (all one-pair extensions).**  For every pair
`e notin U`, arbitrary matrices supported on `U union {e}` cannot realize
`Delta_(6,3)`.

**Proof.**  The automorphism group of `U` has two orbits on its five missing
pairs: the singleton `{03}` and the cross orbit `{14,15,24,25}`.

First add `03`.  Vertices `1,2,4,5` remain cubic, so every matrix on `U` is
a nonzero properly colored basis edge; only `A_03` can be arbitrary.  Its
sole perfect matching is `03|12|45`, whose coefficient slice fixes the
colors at vertices `1,2` to `kappa(12)` and those at `4,5` to `kappa(45)`.
The coloring of `M_A=01|23|45` is outside this slice because properness at
vertex `1` gives `kappa(01)!=kappa(12)`.  The coloring of
`M_B=02|13|45` is outside it because properness at vertex `2` gives
`kappa(02)!=kappa(12)`.  The four basis matching colorings remain distinct,
so both `M_A,M_B` would have to be constant.  Their shared edge `45` would
make the constants equal, contradicting the distinct colors of `01,13` at
vertex `1`.

It remains, by symmetry, to add `14`.  Cubic rigidity at vertices `2` and
`5` gives the two color permutations

\[
 (a,b,c)=(\kappa(02),\kappa(12),\kappa(23)),\qquad
 (d,e,f)=(\kappa(05),\kappa(35),\kappa(45)).                 \tag{22}
\]

The six perfect matchings and their sole arbitrary edges are

\[
\begin{array}{c|cccccc}
 &01|23|45&02|13|45&02|14|35&04|12|35&05|12|34&05|14|23\\
\hline
\text{arbitrary edge}&01&13&14&04&34&14.
\end{array}                                                  \tag{23}
\]

A constant color is covered by the respective slices in (23) exactly under
the six conditions

\[
 c=f,\quad a=f,\quad a=e,\quad b=e,\quad d=b,\quad d=c.       \tag{24}
\]

After globally relabeling `(a,b,c)=(0,1,2)`, checking the six permutations
`(d,e,f)` shows that all three constants are covered only in the two cases

\[
 (d,e,f)=(1,0,2)\quad\text{or}\quad(2,1,0).                 \tag{25}
\]

In the first case, the constant-zero coefficient is supplied uniquely by
the `(0,0)` cell of `A_14` in matching `02|14|35`, so that cell is nonzero.
The same cell occurs uniquely in `05|14|23` at the mixed coloring
`(1,0,2,2,0,1)`, a contradiction.  In the second case, the constant-two
coefficient is supplied uniquely by the `(2,2)` cell of `A_14` in
`05|14|23`; the same cell occurs uniquely in `02|14|35` at
`(0,2,0,1,2,1)`.  This is again a nonzero mixed coefficient.  The direct
slice checks also show uniqueness, so no coefficientwise cancellation was
discarded. \(\square\)

`computations/verify_one_edge_extensions_best_module.py` checks the
16-element support automorphism group, the two missing-pair orbits, all 36
proper color assignments in the cross case, and the unique mixed companions.
Consequently a repair of the best two-module overlay needs at least **two**
new underlying pairs.

The most direct three-module repair also fails.

**Proposition 4.4 (third active module).**  Keep the best `{0,1}` and
`{0,2}` placements (19), and add a copy of the active gadget on colors
`{1,2}` in any relative vertex placement.  Give every module cell an
arbitrary nonzero coefficient and allow arbitrary exact cancellation in
every coincident aggregate cell.  The resulting superposition is never
`Delta_(6,3)`.

The proof is the same exact support-fiber certificate as Proposition 4.1.
For all 720 placements of the third module, enumerate every zero/nonzero
status of aggregate cells receiving two or three module contributions;
single-source cells remain forced nonzero.  There are 32,096 status patterns
in total and at most nine coincident cells.  Every pattern in which all three
constant colorings retain a nonzero matching term has a mixed coloring with
exactly one nonzero matching term.  This proves the claim over every field,
independently of the actual nonzero coefficients.  The exact audit is
`computations/verify_three_active_modules_obstruction.py`.

This does not exclude an arbitrary three-color network on the union support:
new cells not belonging to one of the three binary modules can create extra
terms in the singleton fibers.  It does show that simply overlapping all
three pairwise GHZ cancellation gadgets—even with reweighting and aggregate
cancellation—does not produce a counterexample.
