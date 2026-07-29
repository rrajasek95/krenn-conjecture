# The normalized four-centre survivors do not lift to the common power

## 1. Outcome

The two four-centre patterns left by
[`live-isotropic-second-jet-cover-patterns.md`](live-isotropic-second-jet-cover-patterns.md)
have exact degree-two cofactor models on each isotropic component.  Those
models are not cofactors of the structural quadratic from Section 6 of that
note.  The first omitted common-power identity already excludes both
normalized patterns.

More precisely, take the minimal eight-site internal chart

\[
 W=N\sqcup\{y\},\qquad |N|=7,                           \tag{1}
\]

where `N` consists of three live sites and four nonzero centre sites,
while `P_y=0`.  Give every site in `N` the value `beta_i=1`, give `y` the
value `beta_y=-1`, and use the rational `H` and diagonal centre matrices
from the earlier note.  More explicitly, with

\[
 \Delta=\operatorname {diag}(2,3,5),
 \quad
 B=E_{00}\quad\hbox{or}\quad
 B={1\over2}(E_{01}+E_{10}),
 \quad A_{pq}=B\Delta.
\]

the two direct quadratics are respectively `v_0^2` and `v_0v_1`, and
`B=A_pq Delta^(-1)` is symmetric exactly.  The blocks incident with `y` remain completely
arbitrary, as equation

\[
                         P_iHP_j^{\mathsf T}
                              =(\beta_i+\beta_j)q_{ij}              \tag{2}
\]

places no restriction on them.  Nevertheless, for every colour `c`,

\[
 [X_c]Q=0,
 \qquad
 \left[X_c\right]
       \left(p_c^2{q^3\over3!}\right)=0.                \tag{3}
\]

The direct deleted block cannot repair this: its diagonal contribution is
`b_cc[X_c]Q=0`.  Hence the coefficient of `X_c` in the diagonal cap has
left side zero and right side `1/d_c!=0`.  All three diagonal caps fail,
and the first exact failing coefficient may be taken to be the constant
colour-zero word.

The proof is a one-hole hafnian recurrence, not another zero-cross witness
count.  It couples the apparently independent component cofactors through
the fact that they must all arise from the same `q`: after the unique zero
site is matched, the remaining constant-colour matching would require an
edge between two nonzero-star sites, but every such scalar edge is zero.

## 2. A matching-hole capacity lemma

Let an even site set be partitioned as `W=N sqcup Z`.  Fix a target colour
`c` and write

\[
                         g_{ij}=e_c^{\mathsf T}q_{ij}e_c.            \tag{4}
\]

Assume

\[
                    g_{ij}=0\quad(i,j\in N),
       \qquad       (p_c)_z=0\quad(z\in Z).             \tag{5}
\]

**Lemma 2.1 (constant-colour matching-hole obstruction).**

1. If `|N|>|Z|`, then `[X_c]Q=0`.
2. If `|N|-2>|Z|`, then
   `[X_c](p_c^2q^(r-1)/(r-1)!)=0`.

**Proof.**  A constant-colour term of `Q` is a perfect matching in the
scalar graph (4).  By (5), every vertex of `N` must be paired with a
distinct vertex of `Z`.  This is impossible when `|N|>|Z|`.

In a term of the square response, the two marked factors occupy two
distinct sites of `N`, again by (5).  Every one of the remaining
`|N|-2` vertices of `N` must be paired by `q` with a distinct vertex of
`Z`.  This is impossible when `|N|-2>|Z|`. `QED`

For the minimal chart (1), the two inequalities are `7>1` and `5>1`.
Equivalently, expand a putative matching at the one hole `y`.  For any
marked pair `i,j in N`, its constant-colour cofactor is

\[
 H_{W\setminus\{i,j\}}(g)
   =\sum_{k\in N\setminus\{i,j\}}g_{yk}
       H_{N\setminus\{i,j,k\}}(g)=0,                  \tag{6}
\]

because every positive-order hafnian on the remaining vertices of `N`
uses an `N`--`N` edge.  Formula (6) is the missing one-hole recurrence
which the free cofactor (17) of the preceding note did not impose.

## 3. Why every nonzero--nonzero scalar edge vanishes

Use

\[
 H=\begin{pmatrix}0&1&2\\1&0&3\\2&3&0\end{pmatrix}.               \tag{7}
\]

In both normalized patterns every nonzero `P_i` is diagonal:

* on the live sites, `P_i=I`;
* for `B=E_00`, the four centres are two copies each of
  `diag(1,1,0)` and `diag(1,0,1)`;
* for the two-coordinate-factor rank-two pattern, they are two copies
  each of `diag(1,1,0)` and `diag(0,0,1)`.

For `i,j in N`, equation (2) and `beta_i+beta_j=2` give

\[
 q_{ij}={1\over2}P_iHP_j^{\mathsf T}.                   \tag{8}
\]

If `a_(i,c)` is the `c`-th diagonal entry of `P_i`, then

\[
 e_c^{\mathsf T}q_{ij}e_c
       ={1\over2}a_{i,c}a_{j,c}H_{cc}=0.                \tag{9}
\]

Thus (5) holds simultaneously for all three colours.  Also `P_y=0`, so
every `p_c` vanishes at `y`; the matrices `q_yi` may be arbitrary without
affecting the argument.  Lemma 2.1 proves (3).

For `|W|=8`, the diagonal cap is

\[
 p_c^2{q^3\over3!}+b_{cc}{q^4\over4!}={1\over d_c}X_c. \tag{10}
\]

Taking its `X_c` coefficient and applying (3) gives

\[
                              0={1\over d_c},            \tag{11}
\]

the promised exact contradiction.  Notice that (11) includes the actual
common power and the direct deleted block; setting `b_cc=0` was not used.

## 4. Coupling the two isotropic-component models

For the rank-two direct quadratic, the first coordinate plane asks for a
four-centre cofactor producing the two active constant tensors on that
plane, and the second coordinate plane asks for the analogous pair with a
different centre colour.  Taken separately, both requests have the free
solution (17)--(18) of the preceding note.

Equation (6) says that every one of the required constant-colour pair
cofactors of the **common** `q` is zero.  Thus the two free tensors cannot
be chosen independently, or even one at a time: neither lies in the image
of the one-hole cofactor map of (8).  This is the exact coupling missing
from the isotropic square-jet analysis.

The same obstruction applies to the `B=E_00` four-centre model.  Its two
active kernel colours already fail, and the remaining colour cannot be
supplied by the direct `B Q` term because its constant coefficient in `Q`
also vanishes.

## 5. Scope

This closes both **normalized rational test cases** from Sections 5--6 of
the preceding note, uniformly over every choice of the unrestricted blocks
incident with the zero boundary site.  More generally, Lemma 2.1 applies
whenever the constant-colour support of `q` is bipartite across `N|Z` and
`|N|-2>|Z|`.

It does not yet exclude every abstract four-centre pattern.  A general
centre may have a non-diagonal complementary column, or two singular sites
may have `beta_i+beta_j=0`; either feature can create a nonzero constant-
colour block inside `N` and escapes (9).  Those are now the precise first
algebraic deviations required of any surviving four-centre lift.

## 6. Exact audit

[`verify_four_centre_common_power_one_hole.py`](../computations/verify_four_centre_common_power_one_hole.py)
constructs both eight-site patterns over the rationals, verifies (2),
checks all `21` nonzero--nonzero blocks in all three constant colours,
enumerates the `105` full perfect matchings and every marked pair cofactor,
keeps the zero-site star entries as independent symbolic variables, and
finds the exact residual `-1/d_c` at each constant target word.
