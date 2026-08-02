# The common-coloop anchor and polar actions share one response quotient

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

On one common-coloop affine fibre, let \(\mathcal T\) be the
five-dimensional clean tangent space and retain the actual maps

\[
 \ell=\sigma|_{\mathcal T},\qquad
 w:\mathcal T\longrightarrow\mathcal R_2,\qquad
 \delta_i(L)=L_{ii}\quad(0\leq i\leq2).                     \tag{1}
\]

The full-nine physical equations and the polar clean equation do not act
on unrelated parameters. This note proves the exact comparison at a
fixed attainable scalar \(z\):

1. on \(\mathcal T_0=\ker\ell\), all three diagonal increments factor
   uniquely through the same response space
   \(\mathcal R_0=w(\mathcal T_0)\);
2. multiplication by \(A=q_0^{[h-1]}\) supplies the three induced
   diagonal coordinates on \(\mathcal R_0\);
3. multiplication by \(D_{\bar K}(z)\) supplies the clean equation on
   that identical response; and
4. active clean completion at \(z\) is equivalent to one polar-image
   incidence and three separate non-forcing tests.

Thus the original five-parameter linear system reduces source-faithfully
to

\[
 \boxed{\text{one class in }\operatorname{coker}m_D(z)
        \quad+\quad\text{three affine diagonal tests}.}      \tag{2}
\]

This proves a genuine positive subcase: if the polar residual lies in the
response image and no diagonal is forced to zero on its solution fibre,
then an active clean completion exists. In particular, if every induced
diagonal coordinate is nonzero on the kernel of the polar action, image
incidence alone gives an active completion at every nonzero attainable
scalar.

The note does not prove that the literal full-nine source always supplies
such a scalar. The remaining common-coloop problem is precisely to force
the image incidence and defeat the possible forced diagonal coordinates,
using the omitted full-nine or nonflat two-chart information before
contraction by \(A\).

## 1. The full-nine anchor difference

Retain the notation of the
[affine-fibre reduction](common-coloop-clean-cap-affine-fibre.md):

\[
 q=q_0+\rho,\qquad A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},
\]

and for \(K=K_0+L\),

\[
 z=\sigma(K),\qquad
 U=z\rho+\chi+w(L).
\]

The contracted full-nine physical equation is

\[
 \sum_{i=0}^2\kappa_i(K)X_i
       =UA+\bar r\,\rho B.                                  \tag{3}
\]

Fix an attainable scalar \(z\), choose \(L_z\in\mathcal T\) with
\(\ell(L_z)=z-\sigma_0\), and vary it by \(t\in\mathcal T_0\). Subtracting
(3) for \(L_z+t\) and \(L_z\) gives the coefficient-free identity

\[
 \boxed{\quad
 w(t)A=\sum_{i=0}^2\delta_i(t)X_i.
 \quad}                                                       \tag{4}
\]

The three pure tensors \(X_0,X_1,X_2\) are linearly independent. Hence

\[
                  \ker(w|_{\mathcal T_0})
                    \subseteq\bigcap_{i=0}^2\ker\delta_i.     \tag{5}
\]

Consequently each diagonal functional descends uniquely through the
response quotient. There are linear functionals

\[
 \partial_i^A:\mathcal R_0\longrightarrow\mathbb C
\]

such that

\[
 \delta_i(t)=\partial_i^A(w(t)),\qquad
 vA=\sum_{i=0}^2\partial_i^A(v)X_i
       \quad(v\in\mathcal R_0).                              \tag{6}
\]

This is the source-faithful action through \(A\). It retains the endpoint
labels and all three diagonal rows. A parameter direction invisible to
the response is also invisible to every diagonal; such a direction cannot
repair activity after cleanliness has been solved.

## 2. The polar action on the same response

Write

\[
 D(z)=D_{\bar K}(z),\qquad
 C(z)=C_{\bar K}(z),
\]

so the exact clean equation is

\[
                       C(z)+w(L)D(z)=0.                     \tag{7}
\]

For the chosen scalar lift put

\[
 w_z=w(L_z),\qquad
 \kappa_i^z=\kappa_i(K_0+L_z),\qquad
 b_z=-C(z)-w_zD(z).                                         \tag{8}
\]

Multiplication by the polar difference restricts to

\[
 m_D(z):\mathcal R_0\longrightarrow\mathcal R_{2h}(W),
 \qquad v\longmapsto vD(z).                                 \tag{9}
\]

Equations (4)--(9) give the exact response solution fibre

\[
 \mathcal S_z=\{v\in\mathcal R_0:m_D(z)v=b_z\}.              \tag{10}
\]

Every \(v\in\mathcal S_z\) lifts to a clean cap with scalar \(z\).
Conversely every clean cap at that scalar gives one such \(v\). Any two
parameter lifts of the same \(v\) have the same three diagonals by (5),
and those diagonal values are

\[
                 \kappa_i^z+\partial_i^A(v).                \tag{11}
\]

Thus (10) compares the \(A\)-anchor and \(D(z)\)-polar actions without
changing the scalar, freeing the response, or discarding a diagonal
activity locus.

## 3. Exact active-completion criterion

Suppose first that \(z\ne0\) and (10) is consistent. Choose one solution
\(v_0\), and put

\[
                   N_z=\ker(m_D(z)|_{\mathcal R_0}).         \tag{12}
\]

The \(i\)-th diagonal is forced to zero on the entire clean fibre exactly
when

\[
 \boxed{\quad
 \kappa_i^z+\partial_i^A(v_0)=0,
 \qquad
 \partial_i^A|_{N_z}=0.
 \quad}                                                       \tag{13}
\]

Condition (13) is independent of the chosen solution \(v_0\). If it fails,
the zero set of the \(i\)-th diagonal is a proper affine hyperplane in
\(\mathcal S_z\). Over \(\mathbb C\), three proper affine hyperplanes
cannot cover a nonempty affine space. Therefore:

> **Anchor--polar response-quotient theorem.**
> An attainable scalar \(z\) supports an active clean cap if and only if
> \(z\ne0\), the polar residual class
> \[
>                  [b_z]\in\operatorname{coker}m_D(z)
> \]
> vanishes, and (13) fails for each \(i=0,1,2\).

This is equivalent to the augmented row-span criterion in the original
five tangent parameters, but is smaller and exposes the source action:
the three affine functionals in (13) are exactly the coordinates of
multiplication by \(A\), while consistency uses multiplication by
\(D_{\bar K}(z)\).

Two useful positive subcases are immediate.

* If \(b_z\in\operatorname{im}m_D(z)\) and every
  \(\partial_i^A|_{N_z}\) is nonzero, an active clean cap exists.
* If \(m_D(z)\) is injective on \(\mathcal R_0\), its unique solution is
  active exactly when the three values in (11) are nonzero.

The scalar ledger remains literal. If \(\ell\ne0\), every scalar is
attainable; if \(\ell=0\), only \(z=\sigma_0\) is. The value \(z=0\) is
always inactive, even when (10) and all three diagonal tests pass.

## 4. Independence of the scalar lift

Replace \(L_z\) by \(L_z+t_*\) with \(t_*\in\mathcal T_0\), and put
\(v_*=w(t_*)\). Then

\[
 b_z\longmapsto b_z-m_D(z)v_*,
\qquad
 \kappa_i^z\longmapsto\kappa_i^z+\partial_i^A(v_*).          \tag{14}
\]

Translation \(v\mapsto v-v_*\) identifies the two solution fibres.
Under this translation the values (11) are unchanged. Hence the cokernel
class, the three forced-diagonal conditions, and active existence are all
independent of the representative \(L_z\). This also proves that the
comparison is intrinsic to the affine fibre rather than to a chosen
splitting of its scalar coordinate.

## 5. The square-zero response subcase

If \(\bar r^{[2]}=0\), the affine-fibre formula reduces to

\[
 \mathcal E(K_0+L)
       =z^{h-2}(\chi+w(L))\bar rB.                           \tag{15}
\]

The familiar response-cancellation condition \(w(L)=-\chi\) is therefore
sufficient for cleanliness. Equation (5) sharpens its activity ledger:
on a fixed scalar fibre, all parameter lifts with the same cancelling
response have the same diagonal increments. Kernel freedom in \(w\) cannot
move a cap off a diagonal base locus. The completion is active exactly
when its three induced anchor coordinates in (11) are nonzero (and
\(z\ne0\)), or when a larger polar solution fibre provides the variations
allowed by (13).

## 6. Exact checker

The dependency-free checker
[verify_common_coloop_anchor_polar_response_quotient.py](../computations/verify_common_coloop_anchor_polar_response_quotient.py)
uses exact rational row reduction on a five-parameter, three-response
model satisfying (4). It verifies:

* factorization of all three diagonal maps through the response quotient;
* equality of the original tangent-parameter and reduced response
  consistency/forced-axis tests;
* invariance under translating the scalar lift;
* explicit active witnesses in both positive rank strata;
* a polar-cokernel obstruction;
* each of the three forced diagonal strata separately;
* the inactive scalar and unattainable fixed-scalar strata.

Its frozen case-ledger SHA-256 is

    ddff27993f43fe3af46e0bcaac5bbbea82f8a7e34d60c29873af3a015c84f562

The checker is an audit of the exact linear reduction, not a synthetic
full-nine source. The theorem itself follows from the literal anchor
difference (4) and applies to every common-coloop fibre satisfying the
controlling hypotheses.

## 7. Remaining residue

The comparison between \(A\) and \(D_{\bar K}(z)\) is now exact at the
affine-fibre level. What remains is not a free-parameter ambiguity. One
must use the other full-nine rows or a nonflat source-provenant overlap to
produce some attainable \(z\ne0\) for which

\[
 [b_z]=0\text{ in }\operatorname{coker}m_D(z)
\]

and none of the three conditions (13) holds. The existing \(A\)-to-\(D\)
guard shows that the missing-row \(A\)-annihilations alone do not force the
first condition. This note neither removes that guard nor proves the
dashed clean-point implication.
