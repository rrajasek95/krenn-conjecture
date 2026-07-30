# The filtered selector cycle is missing an odd binary covariant

## 1. Outcome

Let \(U\) be the two-dimensional parameter space of the selector conic and
put

\[
                         D=2h-1\qquad(h\geq3).
\]

The completed 27-row colon cycle supplies a nonzero quadratic covector

\[
                  \vartheta_2\in(\operatorname{Sym}^2U^*)^*
                              \simeq\operatorname{Sym}^2U .       \tag{1}
\]

A clean rootless line, by contrast, can only be contradicted by a nonzero

\[
                  \Theta_D\in(\operatorname{Sym}^DU^*)^*
                              \simeq\operatorname{Sym}^DU          \tag{2}
\]

which kills every degree-\((h-1)\) shift of every clean coordinate.  There
is no nonzero \(SL(U)\)-natural, and hence no \(GL(U)\)-natural, linear map
from (1) to (2).  The obstruction is parity: the central element
\(-I\in SL(U)\) acts as \(+1\) on (1) and as \(-1\) on (2).

Clebsch--Gordan theory identifies the smallest effective auxiliary slot
for a transfer which is linear in the supplied quadratic and linear in one
irreducible auxiliary.  That slot is an odd covariant

\[
              \kappa_{D-2}\in\operatorname{Sym}^{D-2}U
                    =\operatorname{Sym}^{2h-3}U.                   \tag{3}
\]

At this smallest order the only \(SL(U)\)-equivariant **bilinear** map to
(2), up to scale, is the Cartan product

\[
 C:\operatorname{Sym}^{2}U\otimes\operatorname{Sym}^{D-2}U
                  \longrightarrow\operatorname{Sym}^{D}U,
 \qquad \vartheta\otimes\kappa\longmapsto\vartheta\kappa.       \tag{4}
\]

For the fixed source-derived \(\vartheta_2\), write
\(C_{\vartheta_2}(\kappa)=C(\vartheta_2\otimes\kappa)\).  This is a
data-dependent linear map, not by itself an \(SL(U)\)-intertwiner; its
construction is natural when \(\vartheta_2\) is transformed along with
the source.  For untwisted polynomial \(GL(U)\)-representations, (4) is
likewise the only possible minimal-order bilinear map.  At \(h=3\), the
missing covariant is a binary cubic.

This minimality concerns the effective bilinear slot in (4).  It does not
assert that a primitive source ingredient must itself have order
\(D-2\): a lower odd covariant together with already derived even
covariants could first be combined into \(\kappa_{D-2}\).  Such a
construction would be additional source data and would still have to pass
the coefficient cut below.

The currently audited static selector data do not contain (3).  The
diagonal anchors and every literal contracted row are quadratic in a
rank-one selector \(H=uv^{\mathsf T}\); the selected curvature is a
scalar; and the weighted \((b,e,a)\) cycle is selector-degree zero after
\(\vartheta_2\) is applied.  The companion

\[
                         \Gamma_bz^{[h-2]}                         \tag{5}
\]

does have odd **site degree** \(2h-3\), but it has binary parameter order
zero.  Site degree cannot be substituted for the representation in (3).

There is one plausible \(h=3\) source of the right parity.  If the three
literal pure-factor sites forced by the \(e,a,b\) anchor packets really
give nonzero linear coefficient functionals

\[
                         \ell_e,\ell_a,\ell_b\in U                 \tag{6}
\]

on one and the same clean cap line, then

\[
                         \chi_3=\ell_e\ell_a\ell_b                 \tag{7}
\]

is a source-derived cubic.  The existing pure-factor lemma does not yet
prove the common-line/gluing assertion in (6).  More importantly, even
after granting (6), neither the three anchors nor nonzero selected
curvature implies that

\[
                         \vartheta_2\chi_3                         \tag{8}
\]

satisfies the clean Hankel equations.  Section 5 gives an exact rootless
binary guard with three distinct nonzero lines, nonzero curvature, a
generic selector block, and (8) nonzero but not Hankel-annihilating.
For \(h>3\), the three-line product would additionally need a
source-derived even factor of order \(2h-6\); that raises its order to
\(2h-3\) but does not supply the Hankel cut.

Here \(\ell_i\in U\) means a linear **dual** covariant, as required for a
Hankel functional.  A scalar coefficient form on the cap parameter
naturally lies in \(U^*\).  The invariant alternating form identifies
\(U^*\simeq U\) for \(SL(U)\).  For \(GL(U)\), the canonical variance
statement is instead

\[
                         U^*\simeq U\otimes(\det U)^{-1}.
\]

Thus three raw coefficient forms produce
\(\operatorname{Sym}^3U\otimes(\det U)^{-3}\), not an untwisted
\(\operatorname{Sym}^3U\), unless the source supplies the corresponding
determinant-line trivialization (or the entire target is twisted
consistently).  The pure-site proposal therefore needs the correct
variance data, not just three nonzero scalar linear forms.

The precise missing coefficient cut is therefore

\[
 \boxed{
 \ker\bigl(\mu_{\mathcal E}^{*}\circ C_{\vartheta_2}\bigr)\ne0,}
 \qquad
 \mu_{\mathcal E}^{*}:(\operatorname{Sym}^{D}U^*)^*
     \longrightarrow(\mathcal E\otimes\operatorname{Sym}^{h-1}U^*)^* .
                                                                    \tag{9}
\]

At \(h=3\), (9) says that one explicit four-column matrix has rank at
most three.  A preselected cubic (7) must satisfy the stronger vector
equation

\[
                  \mu_{\mathcal E}^{*}
                     (\vartheta_2\ell_e\ell_a\ell_b)=0.           \tag{10}
\]

No currently proved static full-nine, two-chart, anchor, curvature, or
weighted-cycle identity gives (9) or (10).  This is a naturality no-go
and a sharp target for the next coefficient calculation, not a proof of
the conjecture.

## 2. The parity obstruction

For every \(d\geq0\), the central element \(-I\in SL(U)\) acts on
\(\operatorname{Sym}^dU\) as multiplication by \((-1)^d\).  If

\[
                  F:\operatorname{Sym}^2U\longrightarrow
                    \operatorname{Sym}^{D}U
\]

is \(SL(U)\)-equivariant, then

\[
                     F(v)=F((-I)v)=(-I)F(v)=-F(v),
\]

because \(D\) is odd.  Hence \(F=0\).  The same proof applies after
tensoring the input with any collection of selector scalars or even-order
covariants.  Every tensor construction from such inputs still has central
character \(+1\).

For \(GL(U)\), scalar matrices already rule out the map: \(cI\) acts with
weights \(c^2\) and \(c^D\).  An integral determinant twist does not rescue
a map from the quadratic alone.  Indeed
\(\operatorname{Sym}^2U\otimes(\det U)^m\) has highest weight
\((m+2,m)\), whereas \(\operatorname{Sym}^DU\) has highest weight
\((D,0)\); equality would force \(m=0\) and \(D=2\).

There is an additional issue before this parity test can even be applied.
The selector conic and the canonical clean cap line a priori have
different parameter spaces, say \(U\) and \(W\).  Static selector data are
trivial under \(SL(W)\), so

\[
 \operatorname{Hom}_{SL(U)\times SL(W)}
   (\operatorname{Sym}^2U,\operatorname{Sym}^{D}W)=0.              \tag{11}
\]

A positive transfer must first derive a projective comparison \(U\simeq W\)
from the common source.  Choosing similarly named coordinates in two
charts is not such a derivation.

## 3. Clebsch--Gordan gives the minimal missing order

For \(d\geq2\), the Clebsch--Gordan decomposition for \(SL(U)\) is

\[
 \operatorname{Sym}^2U\otimes\operatorname{Sym}^dU
   \simeq
 \operatorname{Sym}^{d+2}U\oplus
 \operatorname{Sym}^{d}U\oplus
 \operatorname{Sym}^{d-2}U.                               \tag{12}
\]

For \(d=1\) it is
\(\operatorname{Sym}^3U\oplus\operatorname{Sym}^1U\), and for \(d=0\)
it is \(\operatorname{Sym}^2U\).  For completeness, the highest-weight
vector in the first summand is the product of highest-weight vectors.
Contracting once or twice with the invariant alternating form lowers the
highest weight by two or four and gives the other two summands.  For
\(d\geq2\), their dimensions

\[
                    (d+3)+(d+1)+(d-1)=3(d+1)
\]

sum to the dimension of the tensor product, so these maps exhaust it.

Consequently, for a bilinear transfer from the quadratic and one
irreducible auxiliary,

\[
 \operatorname{Hom}_{SL(U)}
 (\operatorname{Sym}^2U\otimes\operatorname{Sym}^dU,
  \operatorname{Sym}^{D}U)\ne0
\]

only for

\[
                         d=D-2,\quad D,\quad D+2.          \tag{13}
\]

The smallest order is \(d=D-2=2h-3\), and its multiplicity is one.  The
corresponding bilinear map is the zeroth transvectant, namely the Cartan
product (4).  After inserting a particular \(\vartheta_2\), it becomes
the linear map \(C_{\vartheta_2}\) used in (9), without becoming an
intertwiner on its remaining argument alone.  The positive-order
transvectants require the larger auxiliary orders in (13); they do not
manufacture odd order from the quadratic alone.

For polynomial \(GL(U)\)-representations the refined decomposition is

\[
 \operatorname{Sym}^2U\otimes\operatorname{Sym}^dU
 \simeq
 \operatorname{Sym}^{d+2}U
 \oplus(\operatorname{Sym}^{d}U\otimes\det U)
 \oplus(\operatorname{Sym}^{d-2}U\otimes(\det U)^2),       \tag{14}
\]

with the evident truncations for \(d<2\).  Thus an untwisted target
\(\operatorname{Sym}^{D}U\) occurs only in the first summand with
\(d=D-2\).  Formula (4) is not merely a convenient choice: at minimal
order it is forced by naturality.

## 4. Why the present selector packet has only even order

Write the rank-one direct-zero selector as

\[
                          H=uv^{\mathsf T}.
\]

The factorization has the Segre gauge

\[
                  (u,v)\longmapsto(\lambda u,\lambda^{-1}v).       \tag{15}
\]

Every literal contracted coefficient is a function of \(H\), hence is
gauge neutral.  Polynomially, a gauge-neutral monomial has the same
number of \(u\)- and \(v\)-factors.  Its binary parameter order is
therefore even.  This accounts for all of the presently available data.

* The direct-zero equation \(u^{\mathsf T}Tv=0\), the two diagonal
  targets \(u_ev_e,u_av_a\), and the fixed-\(b\) row family are of
  bidegree \((1,1)\), hence binary order two.
* The pure target tensors \(X_e,X_a,X_b\), the fixed matrices \(P,R,T\),
  and selected curvature are binary order zero.  Curvature may be a
  relative invariant carrying a determinant-line weight under \(GL(U)\),
  but every determinant character is trivial on the central
  \(-I\in SL(U)\) and cannot repair the parity mismatch.  Independence
  of the three target labels likewise does not change the central
  character.
* The third conic covector \(\vartheta_2\) is dual to an order-two family
  and is still even under the centre.
* Applying \(\vartheta_2\) to the quadratic family produces the filtered
  site-algebra cycle

  \[
       x_b\omega z^{[h-2]}+\Gamma_bz^{[h-1]}=0,
  \]

  which has binary order zero.  The exponents in the site algebra do not
  alter its \(SL(U)\)-type.
* A second chart supplies another collection of even-order modules.  An
  overlap of two such collections remains even unless it provides a
  source-derived comparison of the two odd tautological factors.

One may write \(u=(s,t)\) and thereby display linear forms \(s,t\).  But
using \(u\) alone fails to descend through (15): it chooses a
trivialization of one Segre factor.  Such a trivialization, compatible
with the clean cap line and with every chart change, would be legitimate
new odd source data.  It is not a consequence of the contracted static
rows.

This also locates the status of (7).  A literal pure-factor site gives a
physical local axis.  To obtain \(\ell_i\in U\), one must prove that its
coefficient along the moving clean cap is a nonzero linear form and that
the three choices live on the same \(U\).  If that gluing is proved, the
product in (7) is gauge-compatible odd input.  It is then an admissible
candidate for (3), but Section 5 shows that it still needs the coefficient
cut (10).

## 5. The exact Hankel cut and a three-line guard

Let \(S_h=\operatorname{Sym}^hU^*\), and let
\(\mathcal E\subseteq S_h\) be the scalar coordinate space of the clean
error.  Multiplication is

\[
 \mu_{\mathcal E}:\mathcal E\otimes S_{h-1}\longrightarrow S_D.
                                                                    \tag{16}
\]

For

\[
 f_\alpha(s,t)=\sum_{r=0}^h c_{\alpha,r}s^{h-r}t^r,
 \qquad
 \Theta=(\Theta_0,\ldots,\Theta_D)\in S_D^*,
\]

the equation \(\mu_{\mathcal E}^*(\Theta)=0\) is exactly

\[
             \sum_{r=0}^h c_{\alpha,r}\Theta_{r+j}=0
 \quad\text{for every }\alpha\text{ and }0\leq j\leq h-1. \tag{17}
\]

Here is a coordinate form of the minimal Cartan block.  Let
\(\epsilon_i^{(n)}\) be dual to \(s^{n-i}t^i\), write

\[
 \vartheta_2=\sum_{i=0}^2q_i\epsilon_i^{(2)},\qquad
 \kappa=\sum_{l=0}^{D-2}k_l\epsilon_l^{(D-2)}.
\]

Realize the dual symmetric powers by divided differential operators,

\[
       \epsilon_i^{(n)}=
       {\partial_s^{\,n-i}\partial_t^{\,i}\over(n-i)!i!}.
\]

Then \(\Theta=C_{\vartheta_2}(\kappa)\) has exact coordinates

\[
 \boxed{
 \Theta_m=\sum_{\substack{0\leq i\leq2\\0\leq m-i\leq D-2}}
   {D-m\choose2-i}{m\choose i}\,q_i k_{m-i}.}             \tag{18}
\]

Thus (9) is an explicit homogeneous linear system in the \(2h-2\)
unknowns \(k_0,\ldots,k_{2h-3}\).  Equivalently, every
\((2h-2)\times(2h-2)\) minor of its coefficient matrix vanishes.  This is
the exact additional coefficient cut.

At \(h=3\), formula (18) is the \(6\)-by-\(4\) block

\[
 \begin{pmatrix}
 10q_0&0&0&0\\
 4q_1&6q_0&0&0\\
 q_2&6q_1&3q_0&0\\
 0&3q_2&6q_1&q_0\\
 0&0&6q_2&4q_1\\
 0&0&0&10q_2
 \end{pmatrix}.                                           \tag{19}
\]

For each clean cubic \(c_{\alpha,0}s^3+\cdots+c_{\alpha,3}t^3\), its
three Hankel rows multiply (19).  Existence of some cubic is precisely
rank at most three for the resulting matrix.  For the proposed fixed
\(\chi_3\), its four-coordinate vector must lie in that kernel.

The following guard shows that nonzero anchor lines and curvature do not
force this.  Take

\[
 \mathcal E=\langle s^3,t^3\rangle,
 \quad
 T=\begin{pmatrix}1&1\\1&2\end{pmatrix},
 \quad
 \vartheta_2=(-2,1,-1),                                  \tag{20}
\]

where the last formula is
\((-DC,BC,-AB)\) and \(\det T=1\).  The two selector anchors are

\[
                    f_e=-s^2-2st,\qquad f_a=st+t^2,
\]

and \((-2,1,-1)\) annihilates both coefficient triples.  Grant the three
distinct nonzero
coefficient lines

\[
                         \ell_e=X,\qquad
                         \ell_a=Y,\qquad
                         \ell_b=X+Y                              \tag{21}
\]

in the dual binary space, and grant selected curvature equal to \(1\).
Then

\[
                         \chi_3=XY(X+Y)\ne0,\qquad
                         \vartheta_2\chi_3\ne0.             \tag{22}
\]

But

\[
 s^3S_2=\langle s^5,s^4t,s^3t^2\rangle,\qquad
 t^3S_2=\langle s^2t^3,st^4,t^5\rangle,                  \tag{23}
\]

so \(\mathcal ES_2=S_5\) and
\(\ker\mu_{\mathcal E}^*=0\).  Hence the nonzero quintic in (22) cannot
satisfy the six Hankel equations.  In the normalization (18), the cubic
has coordinate vector proportional to \((0,1,1,0)\), and (19) sends it
to a nonzero vector with nonzero coordinates proportional to
\((-12,3,-6)\).  The failure is exact.

The same guard works for every \(h\geq3\): with

\[
                         \mathcal E=\langle s^h,t^h\rangle,       \tag{24}
\]

the first form forces \(\Theta_0,\ldots,\Theta_{h-1}=0\), and the
second forces \(\Theta_h,\ldots,\Theta_D=0\).  Since the symmetric algebra
is a domain, multiplication by nonzero \(\vartheta_2\) is injective, so
(9) has only \(\kappa=0\).  Thus no rule depending only on the static
selector packet and freely attachable clean coordinates can establish
the required transfer.

This guard is representation-theoretic, not a Krenn-source
counterexample.  It deliberately tests exactly the proposed implication

\[
 \{\text{quadratic selector cycle, three nonzero coefficient lines,
       nonzero curvature}\}
 \Longrightarrow
 \vartheta_2\chi_3\in\ker\mu_{\mathcal E}^*.
\]

It leaves open a literal decorated coefficient identity which couples the
same three lines to every clean coordinate and forces (10).  Formulae
(18)--(19) state that missing identity without conflating site degree,
selector degree, or chart coordinates.

## 6. Checker and exact scope

The dependency-free checker
[verify_odd_covariant_filtered_hankel_naturality_obstruction.py](../computations/verify_odd_covariant_filtered_hankel_naturality_obstruction.py)
audits:

* the central parity signs and the Clebsch--Gordan list (13);
* minimal auxiliary order \(2h-3\) for \(3\leq h\leq30\);
* the exact Cartan matrix (18), including its injective rank;
* the full-rank pure-axis Macaulay guard (24); and
* the \(h=3\) three-line calculation (20)--(23).

In the last guard it also checks the two-anchor matrix has rank two,
\(\vartheta_2\) is its exact cross-product null covector, the Cartan block
has rank four, its leading \(4\)-by-\(4\) minor is \(2880\), and the
pure-axis Macaulay matrix has rank six.  The three coefficient lines and
curvature in that check are explicitly granted formal inputs; the checker
does not claim to derive them from a Krenn source.

The proofs of parity, Clebsch--Gordan decomposition, polynomial
injectivity, and the all-\(h\) pure-axis guard are uniform.  The finite
checker loop is only an implementation audit.
