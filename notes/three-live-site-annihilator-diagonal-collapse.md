# Three live sites collapse after the singular-star annihilator projection

## 1. Outcome

The diagonal identities give an exact obstruction beyond the five-witness
count on the smallest surviving live component. Suppose the complete live set

\[
                         U=\{a,b,c\}
\]

has three sites. At every outside site \(z\in Z=W\setminus U\), the matrix
\(P_z\) is singular. Contract the \(z\)-factor by an arbitrary covector

\[
                 \ell_z\in L_z:=\operatorname {Ann}(\operatorname {im}P_z).
                                                               \tag{1}
\]

Then all six polarized product responses vanish after this contraction:

\[
 \left\langle
   \mathcal H_q\bigl(p(x)p(y)\bigr),
   \bigotimes_{z\in Z}\ell_z
 \right\rangle=0
 \qquad(x,y\in\mathbb C^3).                              \tag{2}
\]

This uses the actual common power \(q^{r-1}\), not only the relation blocks.
It follows from a rigid three-site tensor lemma: the three off-diagonal
polarizations of a common triple of one-hole cofactors cannot span a line
unless every cofactor is zero.

Two consequences are immediate.

1. If every outside site is literal two-star-zero, so \(P_z=0\), then the
   contractions in (1) range over the full outside dual tensor space. Hence
   the uncontracted map \(\overline\Phi\) is zero. The three diagonal target
   values are impossible. In particular, the uniform five-witness
   counterconfiguration cannot be repaired by changing only its internal
   \(q\)-blocks while retaining \(P_z=0\) at all five outside sites.
2. In the general singular outside branch, at least two target colours \(d\)
   have an outside site \(z\) for which

   \[
                         e_d^{(z)}\in\operatorname {im}P_z.          \tag{3}
   \]

   Thus a putative order-ten live chart must use genuinely nonzero singular
   stars, and those stars must cover at least two of the three target axes.

The same projection for a two-site live component also kills every product
response. The three-site case is the sharp one when the deleted-star rows are
supported entirely on the live component, because row density forces
\(|U|\ge3\).

## 2. Normalization and contraction

The live-component normal form gives

\[
                         S_i=P_i\Delta
\]

at every internal site, and every \(P_i\) with \(i\in U\) is invertible.
Apply \(P_i^{-1}\) at the three live sites. The local components of \(p(x)\)
there are then simply \(x\). This changes neither tensor nonvanishing nor the
dimension of any response span.

Fix a tuple \(\ell=(\ell_z)_{z\in Z}\) satisfying (1). If one of the two
linear factors in \(p(x)p(y)\) is placed at an outside site \(z\), its
contraction is

\[
                         \ell_z(P_zx)=0.                 \tag{4}
\]

Thus, after contracting all outside factors, both marked linear factors are
forced onto two distinct sites of \(U\). Let

\[
 R_a(\ell)\in V_a,\qquad R_b(\ell)\in V_b,\qquad
 R_c(\ell)\in V_c                                       \tag{5}
\]

be the contracted common-power cofactors left after the marked factors occupy,
respectively, \(bc,ac,ab\). Harmless common factorials are suppressed. The
contracted polarized response is the linear map

\[
\begin{aligned}
 L_R(x\odot y)={}&R_a\otimes(x^{(b)}\otimes y^{(c)}
                              +y^{(b)}\otimes x^{(c)})\\
 &+(x^{(a)}\otimes R_b\otimes y^{(c)}
                              +y^{(a)}\otimes R_b\otimes x^{(c)})\\
 &+(x^{(a)}\otimes y^{(b)}
                              +y^{(a)}\otimes x^{(b)})\otimes R_c.
                                                               \tag{6}
\end{aligned}
\]

The six off-diagonal cap equations say that

\[
 L_R(e_0\odot e_1),\quad L_R(e_0\odot e_2),\quad
 L_R(e_1\odot e_2)                                      \tag{7}
\]

all belong to the one line spanned by the corresponding contraction of
\(Q=q^r/r!\). The next lemma shows that this forces \(R_a=R_b=R_c=0\).

## 3. The three-site tensor lemma

**Lemma 3.1.** Let \(V\) be three-dimensional over a field of
characteristic different from two. For \(R_a,R_b,R_c\in V\), define \(L_R\)
by (6). If the three tensors in (7) span a space of dimension at most one,
then

\[
                            R_a=R_b=R_c=0.               \tag{8}
\]

**Proof.** First fix two distinct colours \(i,j\). The map

\[
 (R_a,R_b,R_c)\longmapsto L_R(e_i\odot e_j)             \tag{9}
\]

is injective. For the third colour \(k\), the coefficient of a word having
\(k\) at one specified site and \(i,j\) at the other two reads off directly
the \(e_k\)-coordinate of the corresponding \(R\). In the \(iij\)-sector,
the three word coefficients are

\[
       r_b+r_c,\qquad r_a+r_c,\qquad r_a+r_b,            \tag{10}
\]

where \(r_a,r_b,r_c\) are the \(e_i\)-coordinates of the three vectors.
The coefficient matrix of (10) has determinant \(2\), so these coordinates
are also recovered. The \(ijj\)-sector is identical. This proves injectivity.

If one tensor in (7) is zero, injectivity immediately proves (8). Otherwise
all three are nonzero and, by hypothesis, proportional. Compare just the
\(01\) and \(02\) tensors. Their possible colour multisets are

\[
 \{001,011,012\},\qquad \{002,022,012\},                 \tag{11}
\]

so a common nonzero tensor must be supported entirely in the \(012\)-sector.
For the \(01\) tensor, vanishing of the \(001\)- and \(011\)-sectors and the
invertibility of (10) force every \(R\) to lie in \(\mathbb C e_2\). For the
\(02\) tensor, the same argument forces every \(R\) to lie in
\(\mathbb C e_1\). Their intersection is zero, contradicting nonzeroness.
Thus the nonzero case is impossible and (8) follows. \(\square\)

Applying the lemma to (6) proves (2).

For completeness, when \(|U|=2\), the contraction is a scalar cofactor times
\(x\otimes y+y\otimes x\). Its three off-diagonal values are linearly
independent whenever that scalar is nonzero, so the same one-line condition
forces the scalar, and hence every contracted product response, to vanish.

## 4. The diagonal target-cover consequence

Let the local factor of the \(d\)-th pure target at \(z\) be denoted
\(e_d^{(z)}\); this notation is unchanged if the preceding live-site basis
normalization is viewed as a change of coordinates. Contracting the diagonal
cap and using (2) gives

\[
 a_{dd}\,Q(\ell)
   =\left(\prod_{z\in Z}\ell_z(e_d^{(z)})\right)
      X_{d,U},                                           \tag{12}
\]

where \(X_{d,U}\) is the nonzero pure target tensor on the three live sites.
For two distinct colours \(d,e\), the tensors \(X_{d,U},X_{e,U}\) are linearly
independent. Therefore the two products on the right of (12) cannot both be
nonzero for one tuple \(\ell\).

The parameter space \(\prod_zL_z\) is an irreducible affine space. If the two
product polynomials for \(d,e\) were both nonzero polynomials, their nonzero
open sets would intersect. Hence at most one of the three products is a
nonzero polynomial. For at least two colours \(d\), one product vanishes
identically. Since it is a product of linear forms on independent factors,
some factor vanishes identically:

\[
 \ell_z(e_d^{(z)})=0\quad(\ell_z\in L_z).
\]

Taking annihilators gives exactly (3).

If \(P_z=0\) for every outside site, then \(L_z=V_z^*\). Varying \(\ell\)
in (2) separates tensors, so \(\mathcal H_q(p(x)p(y))=0\) for every \(x,y\).
The diagonal equations reduce to \(a_{dd}Q=X_d\) for all three \(d\), which
puts three independent tensors on one line. This proves the first consequence
in Section 1.

## 5. Exact audit

[verify_three_live_site_annihilator_diagonal_collapse.py](../computations/verify_three_live_site_annihilator_diagonal_collapse.py)
constructs the map (6) over the rationals. It verifies that each fixed-colour
map (9) has rank nine, that the repeated-colour coefficient matrix (10) has
determinant two, and that imposing proportionality of either pair of nonzero
off-diagonal tensors after restriction to their common \(012\)-sector forces
all nine cofactor coordinates to vanish.
