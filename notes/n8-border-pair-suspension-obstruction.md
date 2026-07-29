# The eight-site Laurent border core cannot be pair-suspended

## 1. Statement

On sites `0,...,7`, let `q` consist of the following twelve unit diagonal
cells:

\[
\begin{array}{c|c}
0&02,14,36,57\\
1&03,15,24,67\\
2&01,23,47,56.
\end{array}                                                \tag{1}
\]

Thus an edge in row `r` of (1) carries the cell `E_(rr)`.  This is the
specialization at `t=1` of the Laurent border source in
[`n8-counterexample-recon.md`](n8-counterexample-recon.md).

**Theorem 1.1.**  Add two new sites `p,s`, arbitrary `3 by 3` matrices on
all sixteen stars from those sites to (1), and an arbitrary direct matrix
on `ps`.  The resulting ten-site matching tensor is not
`Delta_(10,3)`.

The proof uses all nine new-color slices simultaneously.  Its key feature
is that the quadratic response of (1) has singleton rows exposing every
cell outside the twelve displayed cells.  The nine polarized star products
must consequently live on a matching of the 24 old site-colour ports.  A
short zero-product lemma then puts all of their nonzero values on one
rank-one matrix line, whereas the target requires the three independent
lines `C E_(00), C E_(11), C E_(22)`.

This is a fixed-internal-core obstruction.  It rules out reversing the
known eight-site border degeneration by one arbitrary pair suspension; it
does not assert that every ten-site source contains this core.

## 2. The five terms of the internal matching tensor

Work in the site-square-zero algebra and write

\[
             H_8(q)={q^4\over4!}.
\]

Besides the three monochromatic matchings in (1), the selected union has
exactly the two compatible matchings

\[
\begin{aligned}
 N&=01\mid24\mid36\mid57,\\
 N'&=02\mid15\mid36\mid47.                              \tag{2}
\end{aligned}
\]

Their words are respectively

\[
 y=22101000,\qquad y'=01002102.
\]

Every term has unit coefficient, so

\[
 H_8(q)=X_0+X_1+X_2+Y+Y',                               \tag{3}
\]

where `X_r=e_r^(tensor 8)` and `Y,Y'` denote the two displayed mixed
coordinate tensors.

For a quadratic `Z` on the eight sites put

\[
                  \mathcal L_q(Z)={Zq^3\over3!}.          \tag{4}
\]

The following finite incidence fact is the only computation in the proof.

**Lemma 2.1 (complete singleton exposure).**  If

\[
 \mathcal L_q(Z)\in\operatorname {span}\{X_0,X_1,X_2,Y,Y'\}, \tag{5}
\]

then `Z` is supported on the twelve cells in (1).  On that twelve-cell
space the five coordinates in (5) are the incidence sums over the four
edges of the corresponding matchings `M_0,M_1,M_2,N,N'`.

**Proof.**  There are `binom(8,2)3^2=252` quadratic cells.  Enumerate a
term of (4) by its distinguished `Z` cell and a perfect matching of the six
remaining sites using three cells of (1).  Outside the five words in (3),
there are 358 output rows having exactly one such term, with coefficient
one.  Their distinguished cells comprise exactly the 240 cells outside
(1).  Equation (5) therefore sets every one of those 240 coordinates of
`Z` to zero.

If the distinguished cell is one of (1), completing it with three further
selected cells is possible precisely inside one of the five matchings in
(3).  In each case differentiation replaces any one of its four cells, so
the corresponding response coordinate is the sum of the four `Z`
coordinates.  This also shows directly that the restricted response has
rank five.  The dependency-free checker cited in Section 6 enumerates all
252 cells and all perfect matchings, and verifies the stated counts and
incidences.  \(\square\)

## 3. The nine pair slices

For a colour `c` at `p`, let

\[
 p_c=\sum_{i=0}^7\sum_{a=0}^2p_{c,i,a}x_{i,a},
\]

and define `s_d` analogously from the colour-`d` row of the other star.
Let `a_cd` be the `(c,d)` entry of the direct `ps` matrix.  Sorting a
ten-site perfect matching according to whether it uses `ps` gives the
exact nine equations

\[
 a_{cd}H_8(q)+\mathcal L_q(p_cs_d)=\delta_{cd}X_c,
 \qquad 0\le c,d\le2.                                    \tag{6}
\]

Both the first term and the right side of (6) lie in the five-space (5).
Lemma 2.1 therefore says that every one of the nine quadratics `p_cs_d` is
supported on (1).

Package the cap indices at a local old port `x=(i,a)` as column vectors

\[
 P_x=(p_{0,i,a},p_{1,i,a},p_{2,i,a})^t,\qquad
 S_x=(s_{0,i,a},s_{1,i,a},s_{2,i,a})^t,                  \tag{7}
\]

and define

\[
 \Phi(x,z)=P_xS_z^t+P_zS_x^t.                            \tag{8}
\]

For ports on distinct sites, (8) is exactly the `3 by 3` matrix whose
`(c,d)` entry is the corresponding cell of `p_cs_d`.  The twelve allowed
port pairs

\[
             \{(u,r),(v,r)\}\quad(uv\in M_r)             \tag{9}
\]

form a perfect matching of the 24 ports `(i,r)`: every port occurs once.
Consequently

\[
 \Phi(x,z)=0                                             \tag{10}
\]

for every pair of ports at distinct sites except its possible pair in
(9).  Write `F_e` for (8) on an allowed pair `e`.

## 4. Polarized products supported on a port matching

We first record the elementary zero geometry behind (10).  For vectors
`x=(P,S)` and `z=(Q,T)` in `C^3\oplus C^3`, retain the notation

\[
                       \Phi(x,z)=PT^t+QS^t.              \tag{11}
\]

**Lemma 4.1 (common-zero line).**  Suppose `Phi(x,y)` is nonzero and a
nonzero `z` satisfies

\[
                     \Phi(x,z)=\Phi(y,z)=0.              \tag{12}
\]

Then there are nonzero `P,S`, and nonzero scalars `alpha,beta,gamma`, such
that, after interchanging the names of the two summands if necessary,

\[
 x=\alpha(P,-S),\qquad y=\beta(P,-S),\qquad
 z=\gamma(P,S).                                         \tag{13}
\]

In particular `Phi(x,y)` has rank one.  Every other nonzero common zero of
`x,y` is proportional to `z`, and the value of `Phi` on two such common
zeros is proportional to `Phi(x,y)`.

**Proof.**  A nonzero pure point `(P,0)` has zero product only with points
of the same pure type; the analogous statement holds for `(0,S)`.  Thus
`z` cannot be pure, since that would make both `x,y` pure of the same type
and force `Phi(x,y)=0`.

Write `z=(P,S)` with both components nonzero.  If `(Q,T)` is nonzero and
`Phi(z,(Q,T))=0`, then

\[
                         PT^t=-QS^t.                     \tag{14}
\]

Neither side can have a zero factor.  Uniqueness of the factors of a
nonzero simple tensor gives `(Q,T)=lambda(P,-S)`.  Apply this separately to
`x` and `y` to obtain (13).  Finally

\[
 \Phi((P,-S),(P,-S))=-2PS^t,
 \qquad \Phi((P,S),(P,S))=2PS^t,                         \tag{15}
\]

which proves all remaining assertions over characteristic zero.  \(\square\)

**Lemma 4.2 (matching-line collapse).**  Under (10), all nonzero matrices
`F_e` lie on one common rank-one line in `Mat_(3 by 3)`.

**Proof.**  Compare two allowed pairs `e={x,y}` and `f={z,w}` with
`F_e,F_f` nonzero.

If their physical site pairs are disjoint, every cross pair between
`{x,y}` and `{z,w}` satisfies (10).  Thus `z` and `w` are nonzero common
zeros of `x,y`.  Lemma 4.1 says that `F_f=Phi(z,w)` is proportional to
`F_e`, and both have rank one.

If the physical edges share a site, write them as `e={x,y}` and
`f={x',z}`, where `x,x'` are the two ports at the shared site.  The ports
`z` and `x,y` lie at distinct sites, and neither cross pair is allowed, so

\[
                         \Phi(x,z)=\Phi(y,z)=0.           \tag{16}
\]

Lemma 4.1 puts `x,y` on one mixed line and `z` on its antipodal line.
Moreover `y` and `x'` lie at distinct sites and are not paired in (9), so
`Phi(y,x')=0`; the classification in the proof of Lemma 4.1 puts `x'` on
the same antipodal line as `z`.  Formula (15) again makes `F_f`
proportional to `F_e`.  Since every two nonzero allowed values are
comparable in one of these cases, the conclusion follows.  \(\square\)

## 5. Target contradiction

Let `M_0,M_1,M_2` denote the three rows of (1).  Taking in (6) the five
coordinates of Lemma 2.1 gives matrix equations

\[
\begin{aligned}
 A+\sum_{e\in M_r}F_e&=E_{rr} &&(r=0,1,2),\\
 A+\sum_{e\in N}F_e&=0,\\
 A+\sum_{e\in N'}F_e&=0,                                \tag{17}
\end{aligned}
\]

where `A=(a_cd)`.  Subtract the `N` equation from each of the first three:

\[
 E_{rr}=\sum_{e\in M_r}F_e-\sum_{e\in N}F_e
 \qquad(r=0,1,2).                                       \tag{18}
\]

Lemma 4.2 puts every matrix on the right sides of (18) in one vector line.
The three matrices `E_(00),E_(11),E_(22)` are linearly independent.  This
contradiction proves Theorem 1.1.

The argument permits zero star rows, singular and nonsymmetric star
blocks, arbitrary complex entries, and an arbitrary direct matrix.  It
uses no division by a star coordinate and no genericity assumption.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_border_pair_suspension_obstruction.py
```

The script independently enumerates the 105 internal perfect matchings and
the full quadratic response.  It verifies (3), all 363 response rows, the
358 singleton rows exposing exactly 240 nonseed cells, the five four-term
incidence rows, their exact rational rank five, and the perfect-matching
property of the twelve allowed port pairs.  Lemmas 4.1--4.2 are the
symbolic part of the proof and require no computational assumption.
