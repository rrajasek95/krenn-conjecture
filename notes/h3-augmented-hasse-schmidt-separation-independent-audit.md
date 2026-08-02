# Independent audit of the corrected Hasse--Schmidt/split-cap separation

Audit of commit `77b284b`.  No flaw was found in the corrected statement or
checker.  This audit is deliberately a verification of two **uncomposed**
calculations; it does not supply the missing first jets or the comparison
from the polar module to the selected split-cap quotient.

## Outcome

The corrected note now draws the required logical boundary accurately.

1. The augmented Hasse--Schmidt theorem is a general conditional
   membership criterion.  With already constructed invisible first jets
   \(\xi,\eta\), the mixed correction equation is

   \[
             \widehat J\zeta+\widehat H(\xi,\eta)=0.       \tag{A1}
   \]

   The sign and normalization are correct: there is no factor two.

2. The five exact derivatives are genuinely the quadratic polars \(h_v\),
   with the stated `pq`-direct and `pr`-two-star chart placement.

3. Independently, the selected split-cap matrix has ranks \(2\to3\), and
   five formal block copies have ranks \(10\to15\), for the class

   \[
                         (\kappa Yw_v,0,0).                \tag{A2}
   \]

4. Nothing in the polar reconstruction constructs invisible first jets or
   a source-valid augmented comparison

   \[
       (h_vY_0,0,0)\longmapsto(\kappa Yw_v,0,0).           \tag{A3}
   \]

   Therefore the split-cap ranks prove neither failure of polar membership
   nor a five-generator lower bound in the full source module.  The
   corrected note and checker now say this explicitly throughout.

5. The stated zero-indeterminacy condition is exact: after existence of a
   lift, a landing map \(q\) is independent of the chosen lift precisely
   when it kills \(\ker(\widehat Ja)\).

## 1. Mixed Hasse--Schmidt sign and normalization

Work in

\[
 D=S[\epsilon,\delta]/(\epsilon^2,\delta^2)
\]

and substitute

\[
 x_i'=x_i+\epsilon\xi_i+\delta\eta_i
                    +\epsilon\delta\zeta_i.               \tag{A4}
\]

For one polynomial constraint \(F\), Taylor expansion gives

\[
\begin{aligned}
 F(x')={}&F(x)
 +\epsilon\sum_iF_i\xi_i
 +\delta\sum_iF_i\eta_i\\
 &+\epsilon\delta\left(
       \sum_iF_i\zeta_i+
       \sum_{i,j}F_{ij}\xi_i\eta_j\right).               \tag{A5}
\end{aligned}
\]

The mixed Hessian in (A5) has coefficient one.  In the usual Taylor
formula the factor \(1/2\) is cancelled by the two ordered cross terms
\((\epsilon\xi,\delta\eta)\) and
\((\delta\eta,\epsilon\xi)\).  Equivalently, direct multiplication in
\(D\) gives the same formula monomial by monomial.  Applying (A5) to every
component of \(\widehat F\) gives exactly

\[
 \widehat J\xi=0,\qquad \widehat J\eta=0,\qquad
 \widehat J\zeta+\widehat H(\xi,\eta)=0.                  \tag{A6}
\]

Thus a correction exists if and only if

\[
             -\widehat H(\xi,\eta)\in\operatorname{im}\widehat J.
                                                                    \tag{A7}
\]

If allowed corrections are restricted by \(a:L\to S^N\), replacing
\(\widehat J\) by \(\widehat Ja\) is also correct.  This restriction is
essential: the theorem cannot infer that a formal coordinate vector comes
from a source-provenant full-nine row.

The independent checker verifies (A5) directly in the truncated
dual-number algebra on all 120 three-variable monomials of degree at most
seven, at two exact rational packets.  These 240 checks independently catch
both a wrong sign and an erroneous factor of two.

## 2. Formal symbol complex and zero indeterminacy

For a fixed polar symbol let

\[
 P(s_v)=(h_vY_0,0,0),
 \qquad
 d_2(\ell,s)=\widehat Ja(\ell)+P(s).                     \tag{A8}
\]

A cycle with symbol \(s_v\) satisfies

\[
                 \widehat Ja(\ell)=-P(s_v).               \tag{A9}
\]

Since an image is closed under multiplication by \(-1\), (A9) is
equivalent to the stated membership
\(P(s_v)\in\operatorname{im}(\widehat Ja)\).  The sign in the formal
repair is consistent as well: if \(d n_v=P(s_v)\), then
\((-n_v,s_v)\) has boundary \(-P(s_v)+P(s_v)=0\).

Suppose \(\ell\) and \(\ell'\) are two corrections for the same symbol.
Subtracting (A9) gives

\[
                       \ell-\ell'\in\ker(\widehat Ja).     \tag{A10}
\]

Conversely, adding any kernel element produces another correction.  Hence
a linear landing \(q:L\to Q\) is constant on the affine set of corrections
if and only if

\[
                         q(\ker(\widehat Ja))=0.            \tag{A11}
\]

This proves both directions of the zero-indeterminacy criterion, conditional
on existence of at least one lift.  The audit checker also tests (A11) on an
exact rank-two map with a one-dimensional kernel, using one landing which
kills the kernel and one which does not.

## 3. Independent reconstruction of the five polars

There are 105 perfect matchings of eight labelled sites.  Exactly 15 contain
the direct-free edge \(pr=(6,3)\), leaving 90 monomials in each specialized
full row.  For a deleted odd site \(v\), the word \(c_v\) is zero at
\(x,v,p,q\) and has the `12112` colours on the other four odd sites.

A surviving matching contributes to

\[
 {\partial^2H_{c_v}\over
   \partial a_{xv}^{00}\partial a_{pq}^{00}}              \tag{A12}
\]

exactly when it contains both marked edges \(xv\) and \(pq\).  Removing
those edges leaves a perfect matching on
\(D\setminus\{v\}\), and every such matching extends uniquely.  There are
three, so (A12) is exactly

\[
           \operatorname {Haf}(q_{12112}|_{D\setminus\{v\}})=h_v.
                                                                    \tag{A13}
\]

Every term selected by (A12) contains \(pq\), so the entire polar is in the
`pq`-direct sector.  Since the same matching already uses site \(p\) in
\(pq\), it cannot contain \(pr\); it lies in the corresponding `pr`
two-star sector.  The exact five records are

\[
\begin{array}{c|c|c}
v&c_v&D\setminus\{v\}\text{ word}\\ \hline
1&00211200&2112\\
2&01011200&1112\\
3&01201200&1212\\
4&01210200&1212\\
5&01211000&1211.
\end{array}                                               \tag{A14}
\]

Deletion labels make their fine-edge supports pairwise disjoint.  This
proves the polar reconstruction and sector placement, but supplies no
tangent lift and no morphism (A3).  The corrected note now preserves that
distinction.

## 4. Independent split-cap matrix and sign audit

Write

\[
 D=\begin{pmatrix}A&B\\F&U\end{pmatrix},
 \qquad \kappa=AU-BF.
\]

The four contraction identities have the stated signs:

\[
\begin{array}{ll}
 (-F,A)(A,F)^{\mathsf T}=0,&
 (U,-B)(B,U)^{\mathsf T}=0,\\
 (-F,A)(B,U)^{\mathsf T}=\kappa,&
 (U,-B)(A,F)^{\mathsf T}=\kappa.
\end{array}                                               \tag{A15}
\]

The selected split-cap columns are

\[
 T=(-Y,1,0)^{\mathsf T},\qquad
 \rho=(1,0,1)^{\mathsf T},\qquad
 p=(\kappa Y,0,0)^{\mathsf T}.                            \tag{A16}
\]

The existing columns have rank two: the target and ordinary-residue rows
already contain the identity minor.  On boundary alone, and on boundary
plus target, one has \(p=\kappa Y\rho\).  With all three rows, an equation
\(aT+b\rho=p\) forces \(a=0\) from the target row and \(b=0\) from the
ordinary-residue row, contradicting the nonzero boundary \(\kappa Y\).
Equivalently,

\[
                      \det[T\ \rho\ p]=\kappa Y,           \tag{A17}
\]

a unit on the declared active open.  This proves exactly the rank jump
\(2\to3\).

The cap-graph and response signs also agree:

\[
 T+Y\rho=(0,1,Y),\qquad
 -\kappa(T+Y\rho)+\kappa(T+Y\rho)=0,                      \tag{A18}
\]

and

\[
 -\kappa Y\rho=(-\kappa Y,0,-\kappa Y),\qquad
 p-\kappa Y\rho=(0,0,-\kappa Y).                         \tag{A19}
\]

Direct-summing five formal copies of (A16) gives the rank jump
\(10\to15\).  This is a taut block-diagonal consequence of (A17).  Its
labels are not the fine-monomial supports in (A13), and without (A3) it says
nothing about the polar obstruction map.

## 5. Scope and wording audit

The post-fix primary checker records all three relevant facts as false:

\[
\begin{array}{c|c}
\text{comparison map constructed}&\texttt{False}\\
\text{first jets constructed}&\texttt{False}\\
\text{augmented Jacobian composition checked}&\texttt{False}.
\end{array}                                               \tag{A20}
\]

Its printed result also says that \(h_vY_0\) is **not composed** with
\(\kappa Yw_v\).  The corrected note repeatedly states that:

- the polar membership can only be tested after the actual tangent lifts,
  correction module, and augmented Jacobian are specified;
- the split-cap ranks prove no polar failure or necessity statement;
- five blockwise missing cap directions give no lower bound in a full
  source module which can couple faces; and
- the finite rank calculation neither evaluates polar membership nor proves
  that existing full-source rows fail it.

The independent checker guards these statements and checks that the
superseded claims equating cap rank with polar failure are absent.  Thus
there is no residual wording in the audited artifacts which promotes the
split-cap ranks into a conclusion about the polars.

## Exact verification

The dependency-free checker
[audit_h3_augmented_hasse_schmidt_separation_independent.py](../computations/audit_h3_augmented_hasse_schmidt_separation_independent.py)
uses a separately written matching enumeration, truncated-dual-number
arithmetic, rational row reduction, and explicit scope guards.  It passes
normal, optimized, isolated, and no-site-library execution.  Its frozen
ledger digest is

    739e60f8070d60d2441d748e5f42860ff8e51f984a6bbb601801b51302f9b87d

The sound conclusion remains conditional: the Hasse--Schmidt criterion is
ready to evaluate a source-provenant comparison once one is constructed;
the corrected work does not construct it.
