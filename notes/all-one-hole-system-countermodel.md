# An exact countermodel to every pairwise one-hole system

## 1. Outcome

The one-hole identities in
`notes/two-vertex-annihilation-identities.md` remain insufficient even when
they are imposed simultaneously for every deleted pair and without
discarding anchor-line components.  This note gives an explicit `0,+1,-1`
array on eight vertices such that all

\[
 \binom82(8-2)3=504                                      \tag{1}
\]

one-hole polynomial identities hold exactly.  The array is very far from a
solution: its matching tensor has `103` nonzero coefficients and is not
`Delta_(8,3)`.

The same array satisfies `404` of the `420` full two-hole matrix identities,
including all two-hole identities for every pair wholly inside the six-site
anchor web.  It fails `16`; the first failure already occurs for the central
invertible pair.  Thus the full two-hole identity—not its determinant/rank
shadow—is the first contraction in this hierarchy which detects the array.

This is a countermodel to an implication, not a counterexample to Krenn's
conjecture.

## 2. The eight-vertex array

Use vertices

\[
 U=\{0,1,2\},\qquad V=\{3,4,5\},\qquad p=6,\quad q=7.      \tag{2}
\]

Matrices are ordered by their displayed endpoints.  Put

\[
 A_{67}=I_3,                                               \tag{3}
\]

and, for `i=0,1,2`,

\[
 A_{6,i}=E_{ii},\qquad A_{7,i}=I_3,
 \qquad
 A_{6,3+i}=I_3,\qquad A_{7,3+i}=E_{ii}.                   \tag{4}
\]

Thus `U` is the set of the three selected coordinate anchors from `p`, and
`V` is the set of the three selected coordinate anchors from `q`; the
opposite star matrices are invertible.

Among the first six vertices use exactly eight nonzero blocks:

\[
\begin{array}{c|cccccccc}
uv&01&02&35&45&23&24&13&14\\ \hline
A_{uv}&E_{20}&E_{10}&E_{10}&E_{01}&-E_{12}&-E_{12}&-E_{22}&-E_{22}.
\end{array}                                                \tag{5}
\]

Every unlisted block is zero, and reverse orientation means transpose.

Formula (5) is the three-color lift of the binary Koszul web from
`notes/one-hole-cofactor-kernel.md`.  Explicitly, use the following ordered
binary bases in the quotients by the anchor lines:

\[
\begin{array}{c|cccccc}
u&0&1&2&3&4&5\\ \hline
f_u^0&e_2&e_0&e_1&-e_2&-e_0&-e_1\\
f_u^1&-e_1&-e_2&-e_0&e_1&e_2&e_0.
\end{array}                                                \tag{6}
\]

Then the eight blocks in (5) are exactly the lift of (20) in the preceding
note.  In particular,

\[
 C_{67}=H_{\{0,1,2,3,4,5\}}(A)
 =(f_0^0f_1^0f_2^0-f_0^1f_1^1f_2^1)
  \otimes
  (f_3^0f_4^0f_5^0-f_3^1f_4^1f_5^1).                     \tag{7}
\]

The star matrices (4) turn these two cubic factors into the two
three-plane multiplication kernels.  Hence the six one-hole contractions
for the pair `67` vanish conceptually.  The surprising point is that the
same phenomenon propagates through every other pair.

## 3. All one-hole identities hold

For an ordered pair `a,b`, covectors `alpha,beta`, and
`u notin {a,b}`, set

\[
 \gamma_u=(\alpha^TA_{au})\times(\beta^TA_{bu}),
 \qquad g_{ab}=\alpha^TA_{ab}\beta.                       \tag{8}
\]

Let `T_abwr` be coordinate `r` of the partial contraction of
`H_{B\setminus{a,b}}` by all `gamma_u` except at the hole `w`.  Direct
exact expansion gives

\[
 \boxed{
 \alpha_r\beta_r\prod_{u\notin\{a,b,w\}}\gamma_{u,r}
 =g_{ab}T_{abwr}}                                         \tag{9}
\]

for every one of the `28` pairs, every one of its six holes, and every
color.  No evaluation or radical test is used: the checker expands both
sides in

\[
 \mathbb Z[\alpha_0,\alpha_1,\alpha_2,
            \beta_0,\beta_1,\beta_2]                      \tag{10}
\]

and compares every coefficient.  This includes all anchor-line lift
coordinates and every overlapping pair among the six sites of (7).

Nevertheless, for example,

\[
 [e_1e_0e_0e_0e_0e_1e_0e_0]H_8(A)=1,                    \tag{11}
\]

so `H_8(A)` is not diagonal.  Exact enumeration finds `103` nonzero output
coefficients.

The array does not satisfy every separate necessary condition already
known for a true solution: in particular, some vertices among `0,...,5`
do not have all three forced-anchor ports.  Its role is narrower and exact:
even the *entire uncompressed family* (9) does not imply the target tensor.

## 4. The first detected obstruction is the full two-hole identity

For holes `w,z`, put `S=B\setminus{a,b,w,z}`.  The exact two-hole identity
required by the target is

\[
 \operatorname{diag}\!\left(
   \alpha_r\beta_r\prod_{u\in S}\gamma_{u,r}
 \right)_{r=0}^2
 =g_{ab}Q_{wz}
  +h_S\bigl(x_w^Ty_z+y_w^Tx_z\bigr),                      \tag{12}
\]

where

\[
 x_t=\alpha^TA_{at},\quad y_t=\beta^TA_{bt},\quad
 h_S=\left\langle H_S,\bigotimes_{u\in S}\gamma_u\right\rangle,
                                                                    \tag{13}
\]

and `Q_wz` is the two-site partial contraction of
`H_{B\setminus{a,b}}` at the sites in `S`.

For the array above, exact symbolic expansion gives:

* all `15` hole-pair identities (12) for each of the `15` pairs contained
  in `{0,...,5}`;
* `404` valid identities out of all `28*15=420`; but
* `16` failures in total.

The simplest central failure deletes `a=6,b=7` and leaves holes `w=0,z=3`.
The `(0,0)` entry of `LHS-RHS` in (12) is the nonzero monomial

\[
 \boxed{
 \alpha_0\alpha_1^2\alpha_2^2
 \beta_0\beta_1^2\beta_2^2.}                              \tag{14}
\]

Thus (12), with its actual rank-two correction tensor, is the first
nonlocal identity in the hole hierarchy that is not implied by all the
pairwise one-hole equations.  The determinant consequence of (12) loses
the information in (14); the full matrix equation must be retained.

## 5. Exact audit

Run

```text
python computations/verify_all_one_hole_countermodel.py
```

The checker constructs (3)--(5), enumerates perfect matchings exactly,
expands all `504` identities (9), enumerates the `103` nonzero coefficients
of `H_8`, expands all `420` identities (12), checks the `404/16` split, and
verifies the explicit residual (14).

