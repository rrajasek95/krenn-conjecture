# Rigidity and obstruction for an exceptional triangle

This note closes the `F=C_3\sqcup3P_1` support branch on six vertices.  Its
algebraic input is an equality case for a three-term decomposition of the
diagonal tensor.  The finite input is the exact support audit in
`computations/verify_color_sensitive_support_obstruction.py`.

Throughout, `V_i=C^3` has basis `e_0,e_1,e_2`, and tensors are put in the
canonical vertex order without further mention.  Write

\[
 \Delta_{6,3}=\sum_{r=0}^2e_r^{(0)}\otimes\cdots\otimes e_r^{(5)}.
                                                               \tag{1}
\]

## 1. Rigidity of a triangular three-term decomposition

Let `T={0,1,2}` and `W=V_3\otimes V_4\otimes V_5`.  Suppose

\[
 \Delta_{6,3}
 =B_{01}\otimes C_{01}+B_{02}\otimes C_{02}
                         +B_{12}\otimes C_{12},              \tag{2}
\]

where `B_ij` lies in `V_i\otimes V_j`, `C_ij` lies on the four
complementary vertices, and all three displayed summands are nonzero.

**Lemma 1.1 (exceptional-triangle rigidity).**  There is a bijection

\[
 \kappa:\{01,02,12\}\longrightarrow\{0,1,2\}
\]

and nonzero scalars `lambda_ij` such that

\[
 \begin{aligned}
 B_{ij}&=\lambda_{ij}
       e_{\kappa(ij)}^{(i)}\otimes e_{\kappa(ij)}^{(j)},\\
 C_{ij}&=\lambda_{ij}^{-1}
       \bigotimes_{v\notin\{i,j\}}e_{\kappa(ij)}^{(v)}.
 \end{aligned}                                               \tag{3}
\]

In particular every `B_ij` has matrix rank one.  After relabeling the
three colors, (2) is just the three defining summands of (1), with a scalar
moved across each cut.

**Proof.**  Put

\[
 w_r=e_r^{(3)}\otimes e_r^{(4)}\otimes e_r^{(5)}\in W.
\]

Regard `C_01`, `C_02`, and `C_12`, respectively, as elements of
`V_2\otimes W`, `V_1\otimes W`, and `V_0\otimes W`.  They define nonzero
linear maps

\[
 L_2,L_1,L_0:W^*\longrightarrow V_2,V_1,V_0                 \tag{4}
\]

by contraction in `W`.  There is a nonempty Zariski-open set `Omega` in
`W^*` on which every `L_i(phi)` is nonzero and every `phi(w_r)` is
nonzero.  Indeed, the excluded sets are the kernels of three nonzero
linear maps and three proper hyperplanes.

Contract (2) by `phi in Omega`.  On the triangle this gives

\[
 \sum_{r=0}^2\phi(w_r)e_r^{(0)}\otimes e_r^{(1)}\otimes e_r^{(2)}
 =B_{01}\otimes L_2(\phi)+B_{02}\otimes L_1(\phi)
                         +B_{12}\otimes L_0(\phi).           \tag{5}
\]

The three-slice center lemma (`notes/tensor-route.md`, (25a)--(25b))
applies: the three singleton factors `L_0(phi),L_1(phi),L_2(phi)` lie on
three distinct coordinate axes.  The nonzero coefficients `phi(w_r)` do
not affect those axes; they may be absorbed into one of the three diagonal
factor triples.

This conclusion for generic `phi` has no hidden genericity residue.  For
fixed `i` and distinct colors `a,b`,

\[
 (L_i(\phi))_a(L_i(\phi))_b=0\qquad(\phi\in\Omega).
\]

The left side is a polynomial in `phi`, so it vanishes on all of `W^*`.
Thus the linear subspace `im L_i` is contained in the union of the three
coordinate lines.  A vector space over an infinite field contained in a
finite union of proper subspaces is contained in one of them.  Since
`L_i` is nonzero, there is a fixed color `k_i` with

\[
 \operatorname{im}L_i=\mathbb C e_{k_i}.                    \tag{6}
\]

Taking one `phi in Omega` shows that `k_0,k_1,k_2` are distinct.  By the
tensor--hom identification, (6) factors the complementary tensors:

\[
 C_{01}=e_{k_2}^{(2)}\otimes D_{01},\quad
 C_{02}=e_{k_1}^{(1)}\otimes D_{02},\quad
 C_{12}=e_{k_0}^{(0)}\otimes D_{12},                         \tag{7}
\]

for nonzero `D_ij in W`.

Now flatten (2) across `T|{3,4,5}`.  The left side is the rank-three
matrix

\[
 \sum_{r=0}^2
 (e_r^{(0)}\otimes e_r^{(1)}\otimes e_r^{(2)})\otimes w_r. \tag{8}
\]

After (7), the right side is a sum of three rank-one matrices whose triangle
factors are

\[
 t_{01}=B_{01}\otimes e_{k_2}^{(2)},\quad
 t_{02}=B_{02}\otimes e_{k_1}^{(1)},\quad
 t_{12}=B_{12}\otimes e_{k_0}^{(0)}.                         \tag{9}
\]

A rank-three matrix expressed as three rank-one matrices has independent
left factors and independent right factors.  Its column space therefore
equals

\[
 \operatorname{span}\{t_{01},t_{02},t_{12}\}
 =S:=\operatorname{span}\{e_r^{(0)}\otimes e_r^{(1)}
                              \otimes e_r^{(2)}:0\le r<3\}. \tag{10}
\]

But

\[
 S\cap(V_0\otimes V_1\otimes\mathbb C e_k^{(2)})
 =\mathbb C(e_k^{(0)}\otimes e_k^{(1)}\otimes e_k^{(2)}),  \tag{11}
\]

and the analogous identity holds with any one of the three modes fixed.
Equations (9)--(11) force each `B_ij` to have the first form in (3), with
`k_2=\kappa(01)`, `k_1=\kappa(02)`, and `k_0=\kappa(12)`.  Comparing the
three independent diagonal coefficients in (2) gives the second form in
(3).  This proves the lemma. `QED`

The nonzero-summand hypothesis will be automatic in the application.  For
completeness, (1) cannot be a sum of only two of the three kinds of slice
in (2).  After a generic contraction in `W`, such an identity would express
a three-way diagonal tensor with three nonzero coefficients as two slices
centered at two different modes.  Annihilate the singleton factor of each
slice.  The resulting two annihilator spaces in `C^3` both have dimension
at least two, but all of their coordinatewise products would have to be
zero.  This is impossible: each two-dimensional subspace is contained in
at most one coordinate hyperplane, so some coordinate functional is
nonzero on both spaces.  Thus the diagonal tensor has slice rank three.

## 2. The color-sensitive stabilizer implication

Let aggregate edge matrices `A_uv` satisfy `H_6(A)=Delta_(6,3)`.  Choose
numbers `alpha_(v,r)` such that

\[
 \sum_{v=0}^5\alpha_{v,r}=1\quad(r=0,1,2).                  \tag{12}
\]

The color-sensitive star identity from `notes/color-sensitive-averaging.md`
is

\[
 \Delta_{6,3}=\sum_{u<v}A_{uv}^{(\alpha)}\otimes
 H_{[6]\setminus\{u,v\}}(A),                               \tag{13}
\]

where, entrywise,

\[
 A_{uv}^{(\alpha)}(a,b)
   =(\alpha_{u,a}+\alpha_{v,b})A_{uv}(a,b).                 \tag{14}
\]

Suppose the exceptional graph is the triangle
`F={01,02,12}`, every matrix on `F` has rank at least two, and `alpha`
satisfies the following equations on the *actual* matrix supports:

\[
 \begin{array}{ll}
 \alpha_{u,a}+\alpha_{v,b}=0,
   &uv\notin F,\ (a,b)\in\operatorname{supp}A_{uv},\\[2mm]
 \alpha_{u,a}+\alpha_{v,b}=1,
   &uv\in F,\ (a,b)\in\operatorname{supp}A_{uv}.
 \end{array}                                                \tag{15}
\]

Then (14) kills every edge outside `F` and leaves each exceptional matrix
*equal to* `A_uv`, not merely proportional to it.  Hence (13) becomes (2)
with

\[
 B_{ij}=A_{ij},\qquad
 C_{ij}=H_{[6]\setminus\{i,j\}}(A).                         \tag{16}
\]

No term in (16) can vanish, by the two-slice observation after Lemma 1.1.
The lemma now says every `A_ij` has rank one, contradicting the definition
of `F`.  We have proved the following exact implication.

**Corollary 2.1.**  A support pattern with a rank-at-least-two exceptional
triangle is impossible whenever the rational affine system (12), (15) is
consistent.

The value `1` in the second line of (15) is essential.  Merely retaining a
triangle edge would replace `A_ij` by a coordinatewise rescaling and would
not contradict the rank of the original matrix.

We also record explicitly the lower bound used when a stabilizer leaves at
most two arbitrary edges.  Given two distinct edge cuts `e|([6]\setminus e)`
and `f|([6]\setminus f)`, choose a three-vertex set meeting both sides of
both cuts.  (For disjoint edges take one endpoint of each and a fifth
vertex; for intersecting edges take the two noncommon endpoints and a
vertex outside their union.)  Contract the other three vertices by product
covectors that are nonzero on every coordinate basis vector.  The target
becomes a three-way diagonal tensor with three nonzero coefficients, while
each retained edge term becomes a slice across a nontrivial cut of the
chosen triple.  The slice-rank-three argument following Lemma 1.1 rules out
two such terms.  Hence `Delta_(6,3)` cannot be a sum of at most two
edge-partition terms, regardless of which two edges survive.

## 3. Exhaustive support certificate for `F=C_3`

The checker `computations/verify_color_sensitive_support_obstruction.py`
uses only necessary conditions for an exact realization:

1. every nonexceptional matrix has arbitrary nonempty rank-one endpoint
   supports;
2. the forced incident-edge theorem supplies, for every ordered
   `(vertex,color)`, an incident rank-one factor whose opposite-head support
   is exactly that color singleton;
3. every rank-at-least-two exceptional matrix contains two supported cells
   in distinct rows and columns;
4. each constant-color coefficient has a supported perfect matching, while
   no mixed coefficient has exactly one supported perfect matching.

For each Boolean support model the checker first searches, by exact rational
rank comparison, for a stabilizer that kills all but at most two active
edges.  Such a model contradicts partition rank three.  If that search
fails, it solves (12), (15) with all three triangle edges fixed.  A
consistent system then invokes Corollary 2.1.  In either case the checker
blocks that exact support pattern together with its graph/color orbit.  This
first alternative is important when the support model allows one of the
three nominally exceptional matrices to be zero; the second alternative
automatically has all three matrices active and of rank at least two.

For `F=C_3\sqcup3P_1`, after 32 such support representatives the remaining
CNF is UNSAT.  No translated-fiber or numerical cancellation cut is used in
this row.  Thus the two rigorous stabilizer contradictions exhaust every
support pattern allowed by the necessary conditions.

The count is solver-trajectory metadata: deterministic ordering of the
support variables changed an earlier `3+26` partition/triangle transcript to
the current `3+29` transcript without changing the formula or implication.
The persistent semantic certificate records all 32 representative supports.
Replay independently resolves the rational stabilizer witness for each,
regenerates every graph/color orbit, checks the augmented-CNF hash with two
SAT engines, and verifies a deletion-free DRUP trace by reverse unit
propagation.

Run the isolated audit with

```sh
.venv/bin/python computations/verify_color_sensitive_support_obstruction.py \
  --only C3+3P1
```

Its terminal certificate line is

```text
C3+3P1: UNSAT; support_blocks=32, transfers=0, witnesses={'partition-rank': 3, 'triangle-rank': 29}
```

Run the independent semantic and propositional replays with

```sh
.venv/bin/python computations/certify_exceptional_triangle_obstruction.py
.venv/bin/python computations/verify_drup_certificate.py \
  computations/exceptional_triangle_support.cnf \
  computations/exceptional_triangle_support.drup
```

The canonical CNF has 11,163 variables and 85,755 clauses.  Its SHA-256 is
`4961aeaad85296f4be4005e166880186f2ce5f995b595162bf673a7d3eda087c`;
the 57,045-addition deletion-free DRUP trace has SHA-256
`db3dfebc12e25f0be44477f8593e51d7793572cf5e3acd72a93f6b08eb7ca0fa`.

Consequently the exceptional graph `F` cannot be
`C_3\sqcup3P_1` in a six-vertex, three-color realization.
