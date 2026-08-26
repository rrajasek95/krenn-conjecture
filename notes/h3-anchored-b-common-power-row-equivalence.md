# The anchored \(B\)-system is an exact row change, not a new full-nine constraint

## Result

Work in the six-residual-site square-zero algebra and retain the literal
full-nine rows

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i.
 \tag{1}
\]

Fix an off-diagonal entry \(a_{ab}=\alpha\ne0\), put

\[
 F=q^{[2]},\qquad z=\alpha^{-1}p_as_b,
 \qquad C=q+3z,
 \qquad B_{ij}=p_is_j-a_{ij}z.
 \tag{2}
\]

Then, without cancelling \(F\),

\[
 \boxed{CF=0,\qquad B_{ij}F=\delta_{ij}X_i,
        \qquad B_{ab}=0.}
 \tag{3}
\]

The factor three in \(C\) is forced by
\(qF=3q^{[3]}\).  In particular, the selected row gives
\(q^{[3]}=-zF\), hence \((q+3z)F=0\), not \((q+z)F=0\).

This packet is exactly row-equivalent on \(D(\alpha)\) to the normalized
quadratics already used in
[`selector-macaulay-double-jet-and-offdiagonal-hexagon.md`](selector-macaulay-double-jet-and-offdiagonal-hexagon.md):

\[
 D_{ij}=p_is_j+{a_{ij}\over3}q,
 \qquad D_{ij}F=\delta_{ij}X_i.
 \tag{4}
\]

Indeed

\[
 \boxed{
 D_{ab}={\alpha\over3}C,
 \qquad
 B_{ij}=D_{ij}-{a_{ij}\over\alpha}D_{ab}.}
 \tag{5}
\]

Conversely,

\[
 \boxed{
 C={3\over\alpha}D_{ab},
 \qquad
 D_{ij}=B_{ij}+{a_{ij}\over3}C.}
 \tag{6}
\]

Thus choosing \(\alpha=1\) and eliminating the selected off-diagonal cell
merely puts the old full-nine system in row-echelon form.  It neither loses
nor adds a common-power equation.  The exact zero \(B_{ab}=0\) replaces the
old annihilator row \(D_{ab}F=0\), while \(C=3D_{ab}\) records that row.

## Proof and source scope

The selected \((a,b)\) row of (1) is

\[
 \alpha q^{[3]}+p_as_bF=0.
\]

Because \(p_as_b=\alpha z\), division by the declared live scalar
\(\alpha\) gives \(q^{[3]}=-zF\).  Multiplying the divided-power identity
\(qF=3q^{[3]}\) into this equality proves \(CF=0\).  Substitution in every
row of (1) gives

\[
 (p_is_j-a_{ij}z)F=\delta_{ij}X_i,
\]

and the definition of \(z\) gives \(B_{ab}=0\).  Equations (5)--(6) are
literal scalar row operations.  No quadratic, site form, or common power is
inverted.  If one first uses the endpoint/direct scalar gauge to set
\(\alpha=1\), the only localization hidden in (2) disappears; otherwise
the theorem is explicitly confined to \(D(\alpha)\).

The nearby archived system
\(D_{ij}=p_is_j+(a_{ij}/3)q\) therefore already contains this exact
information.  What is new is only the convenient zero-anchor
representative (2), not an additional equation.

## The shifted Segre relations do not evade the archived degree guard

Writing \(R_{ij}=p_is_j=B_{ij}+a_{ij}z\), source factorization gives every
response rectangle in the exact shifted form

\[
 (B_{ij}+a_{ij}z)(B_{k\ell}+a_{k\ell}z)
 =
 (B_{i\ell}+a_{i\ell}z)(B_{kj}+a_{kj}z).
 \tag{7}
\]

On the anchor chart this includes

\[
 z(B_{ij}+a_{ij}z)
 =(B_{ib}+a_{ib}z)(B_{aj}+a_{aj}z).
 \tag{8}
\]

These are precisely the ordinary response Segre relations after the
invertible row change (5)--(6).  They do not create an uncontracted
common-power consequence: (7) has residual degree four, so multiplying it
by \(F\), of residual degree four, vanishes identically on six sites.  The
primitive off-diagonal cubic is already top degree.  As in the archived
hexagon audit, a nontrivial interaction with a diagonal target must first
take a literal site coefficient, where product-rule/four-cut terms appear.

Hence the proposed \(B=p s^{\mathsf T}-az\) rewrite does not advance the
full-nine scalar-zero frontier by itself.  Its smallest nonredundant use
would be a coefficient-cut identity in which (8) is differentiated or
contracted before the common power is applied.

## Hostile factor-three guard

Let the six residual sites be paired into three disjoint decorated edges
\(e_0,e_1,e_2\), and put

\[
 q=e_0+e_1+e_2,
 \qquad z=-e_0=p_as_b,
 \qquad \alpha=1.
 \tag{9}
\]

Then

\[
 F=e_0e_1+e_0e_2+e_1e_2,
 \qquad q^{[3]}=e_0e_1e_2,
 \qquad zF=-e_0e_1e_2.
 \tag{10}
\]

Thus the literal selected row \(q^{[3]}+zF=0\) holds with nonzero top,
and

\[
 (q+3z)F=0,
 \qquad
 (q+z)F=2e_0e_1e_2\ne0.
 \tag{11}
\]

This is only a selected-row normalization guard, not a full-nine source and
not a counterexample to Krenn's conjecture.  It rules out the tempting
factor-one replacement at the literal source level.

The exact replay is
[`verify_h3_anchored_b_common_power_row_equivalence.py`](../computations/verify_h3_anchored_b_common_power_row_equivalence.py).

