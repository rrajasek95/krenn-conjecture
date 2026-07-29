# Independent hard-first audit for a four-site witness union

This note cross-checks the finite and local-algebra parts of
[`n8-hard-annihilator-union-four.md`](n8-hard-annihilator-union-four.md).
It deliberately uses only the hard-witness argument from that proof.

An earlier draft tried to derive general restrictions from an exact
two-element witness set by applying the three-hole one-slice covering lemma
to a diagonal having only one or two nonzero colors.  That application is
invalid: the covering lemma requires a full ternary diagonal, and anchors
for a binary diagonal can collide.  None of those proposed exact-pair
restrictions or the resulting `8+9+3+3` routing is used here.

## 1. Hard-witness enumeration

Fix an invertible deleted block `A_pq` at `n=8`, and let

\[
 S_r=\{u:A_{pu}K_rA_{qu}^T=0\}\qquad(r=0,1,2).
\]

Assume that the full witness union is a four-set `U={0,1,2,3}`.  Each
`S_r` has size at least two.  At an outside site, over the incidence
function field, put

\[
 x_u=A_{pu}^T\alpha,\qquad y_u=A_{qu}^T\beta,\qquad
 N_u=(\operatorname{span}\{x_u,y_u\})^\perp.
\]

A site is hard for color `r` when `N_u` is contained in `e_r^perp`.
The arbitrary one-hole identity forces at least two hard sites per color.
If `W_u={r:u in S_r}`, then a nontriple site is hard for exactly the
colors in `W_u`, while a triple-zero site is hard for at most one color.

There are 23 triples `(S_0,S_1,S_2)` modulo site and color permutations.
Applying only these hard-capacity rules leaves the following twelve:

\[
\begin{array}{c|ccc|c}
 &S_0&S_1&S_2&\text{disposition}\\ \hline
1&01&01&23&\text{anchor rectangle}\\
2&01&012&023&\text{determinant}\\
3&01&012&23&\text{determinant}\\
4&01&0123&0123&\text{two monomials}\\
5&01&0123&023&\text{determinant}\\
6&01&0123&23&\text{determinant}\\
7&01&02&123&\text{determinant}\\
8&01&02&13&\text{determinant}\\
9&01&023&023&\text{two monomials}\\
10&01&023&123&\text{determinant}\\
11&012&0123&013&\text{determinant}\\
12&012&013&023&\text{determinant}
\end{array}
\]

The companion checker independently recovers the counts `23 -> 12 -> 3`:
nine of the twelve survivors satisfy the two-hole determinant criterion,
and the three displayed exceptional rows are exactly the ones handled in
Sections 5--6 of the main note.

## 2. Local determinant audit

Suppose the two holes `u,v` are exact double witnesses and are both hard
for color `r`.  Choose their other supported coordinates `a,b`.  Write the
relevant star coordinates as

\[
 (x_{u,r},x_{u,a})=(x_r,x_a),\quad
 (y_{u,r},y_{u,a})=(y_r,y_a)
\]

and similarly `(X_r,X_b),(Y_r,Y_b)` at `v`.  The selected block of the
two-hole correction `R_uv=x_u y_v^T+y_u x_v^T` is

\[
 \begin{pmatrix}
 x_rY_r+y_rX_r&x_rY_b+y_rX_b\\
 x_aY_r+y_aX_r&x_aY_b+y_aX_b
 \end{pmatrix}.
\]

Its determinant factors as

\[
 (x_ry_a-x_ay_r)(Y_rX_b-Y_bX_r),
\]

which is nonzero because both holes are exact double witnesses.  This is
the local contradiction used on the nine determinant rows after the other
two target colors have hard witnesses outside the holes.

For the two variable-annihilator exceptions, the checker also verifies
that the target monomials in the free plane variables are distinct.  The
remaining incidence row `(01,01,23)` requires the full four-hole ternary
identity and the anchor-rectangle argument of the main note; no weaker
one- or two-color covering assertion is made here.

The exact audit is
[`verify_invertible_pair_witness_union4_obstruction.py`](../computations/verify_invertible_pair_witness_union4_obstruction.py).
