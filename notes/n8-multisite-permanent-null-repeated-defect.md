# The binary permanent-null cap leaves an eight-sector multisite defect

## Exact normal form

Let `p0,p1,s0,s1` be arbitrary multisite star rows in the site-square-zero
algebra and put

\[
 K=\begin{pmatrix}1&1\\-1&1\end{pmatrix},\qquad
 R_K=p_0s_0+p_0s_1-p_1s_0+p_1s_1.                       \tag{1}
\]

Although `perm(K)=0`, direct divided-power expansion gives

\[
\begin{aligned}
R_K^{[2]}={}&
 \tfrac12\sum_{i,j=0}^1p_i^2s_j^2
 +(p_0^2-p_1^2)s_0s_1
 +p_0p_1(s_1^2-s_0^2).                                  \tag{2}
\end{aligned}
\]

Equivalently, using `p_i^[2]=p_i^2/2` and similarly for `s`,

\[
R_K^{[2]}=2\left(
 \sum_{i,j}p_i^{[2]}s_j^{[2]}
 +(p_0^{[2]}-p_1^{[2]})s_0s_1
 +p_0p_1(s_1^{[2]}-s_0^{[2]})\right).                   \tag{3}
\]

The only distinct-row/distinct-column sector is

\[
 (K_{00}K_{11}+K_{01}K_{10})p_0p_1s_0s_1=0.            \tag{4}
\]

Thus permanent zero cancels one sector and leaves eight labelled sectors:
four same-entry squares, two repeated-row products, and two repeated-column
products.  They vanish for literal one-site ports because repeated uses
collide at a physical site.  They need not vanish for multisite rows.

The exact checker is
`computations/verify_n8_multisite_permanent_null_repeated_defect.py`.

## Reduction by the nine response rows is not formal

The nine response identities determine the first insertion

\[
                R_Kq^{[2]}=\sum_{i,j}K_{ij}(p_is_jq^{[2]}), \tag{5}
\]

but (2) shows that the next insertion has different literal provenance:

\[
                         R_K^{[2]}q.                    \tag{6}
\]

There is no universal reduction of (6) from the nine rows alone.  The
checker realizes this in the committed six-site one-anchor source packet.
Its complete response matrix is

\[
 p_0s_0q^{[2]}=X_0,qquad
 p_is_jq^{[2]}=0\quad ((i,j)\ne(0,0)).                  \tag{7}

\]

So all nine literal response rows hold.  Nevertheless, for the exact `K` in
(1), the source-labelled normal form of (6), in site order
`(A0,A1,A2,B0,B1,B2)`, is

```text
(0,0,1,0,0,1) : 2    repeated row, distinct columns
(0,1,0,0,1,0) : 2    same row and same column label
(0,1,0,1,1,0) : 2    same row and same column label.
```

Every distinct-row/distinct-column contribution cancels before this
readout.  The three displayed mixed coefficients are exactly the
`q^1 R_K^2` coefficients obtained by an independent aggregate matching
expansion.

## Consequence and scope

This is the bounded obstruction to extending the fixed-star cap theorem to
arbitrary multisite rows: permanent zero does not kill the quadratic cap
tail, and the first-response equations do not supply a provenance-preserving
nullhomotopy for its repeated-label part.

The counterguard has one nonzero diagonal target and eight zero response
rows.  It is **not** a full ternary response packet and does not show that
the two additional diagonal anchors cannot kill the defect.  A theorem for
the full-nine, three-target setting must use those anchors, activity, or a
new connection/Bianchi relation.  It cannot cite `perm(K)=0` or the nine row
shapes alone.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_multisite_permanent_null_repeated_defect.py
.venv/bin/python -O computations/verify_n8_multisite_permanent_null_repeated_defect.py
```
