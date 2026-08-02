# The shifted two-chart principal-parts square exists, but its cap landing does not

Positive partial construction and exact obstruction.  This note constructs a
source-resolution-relative two-chart principal-parts square and derives its
module shift and sector polar.  It does not construct geometric tangent
vectors to a hypothetical full source, an ordinary-residue-compatible cap
landing, or a proof of Krenn's conjecture.

## Outcome

For each deleted odd site \(v\), let \(c_v\) be zero on \(x,v,p,q\) and
equal to the `12112` word on \(F_v=D\setminus\{v\}\).  Put

\[
 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00},
 \qquad K_v=r_{c_v}^{pq}-r_{c_v}^{pr}.                  \tag{1}
\]

The two chart rows present the same direct-free global polynomial, so
\(dK_v=0\).  Prolonging this strict comparison through the two marked
principal-parts directions gives two relative presentation-jet cycles:

\[
 d\Xi_v=\partial_{u_v}H_{c_v}-\partial_{u_v}H_{c_v}=0,
 \qquad
 d\Eta_v=\partial_tH_{c_v}-\partial_tH_{c_v}=0.         \tag{2}
\]

The mixed global boundary also cancels, but the Rees sector filtration
remembers its placement:

\[
 \partial_t\partial_{u_v}H_{c_v}=h_v
 \quad\begin{cases}
 \text{in the \(pq\)-direct sector},\\
 \text{in the \(pr\)-two-star sector}.
 \end{cases}                                            \tag{3}
\]

Thus the source-resolution-relative principal-parts square and its polar
symbol are real; they are not formal cap columns.  Since \(c_v\) is mixed,
the strict physical target of (1)--(3) is zero.

The fine grading uniquely derives the cap shift.  The mixed derivative has
degree four, reinsertion of \(Y_0\) contributes the five zero-colour odd
slots, and the required EqSystem degree has three remaining slots.  Hence

\[
 \boxed{\sigma=e_{x,0}+e_{p,0}+e_{q,0}},\qquad
 \deg(h_vY_0)+\sigma=\lambda_v.                         \tag{4}
\]

No shift is declared in advance in this calculation: (4) is the unique
componentwise difference of the two displayed degrees.

The construction stops at the cap landing.  Ordered mixed-word reset
followed by pure reinsertion has chain-map commutator

\[
 \omega(d_{s,a})=
 \begin{cases}
 h_sY_0,&a=m_s,\\
 0,&a\ne m_s.
 \end{cases}                                            \tag{5}
\]

The five nonzero components in (5) have rank five modulo the old pure
denominator image.  Therefore the Rees polar cannot be landed in the old odd
quotient by the proposed reset.

There is a second obstruction to reaching the selected split-cap class.  A
minimal polynomial scalar comparison would have to carry the five
internal-\(q\)-degree-two coefficients \(h_s\) to the active
internal-\(q\)-degree-zero unit \(\kappa Y\).  But

\[
                 \kappa Y\notin(h_1,\ldots,h_5),         \tag{6}
\]

because \(q\mapsto0\) kills the ideal on the right and retains \(\kappa Y\).
Thus the exact minimal comparison class is

\[
                 [\kappa Y]\ne0
                 \quad\text{in }R/(h_1,\ldots,h_5).     \tag{7}
\]

Equations (5) and (7) isolate the smallest missing **type**: a shifted,
denominator-marked, two-edge Rees square whose lower cap face has a
\(q\)-degree-zero component, with zero target and zero ordinary residue.
One equivariant family may package its five labelled components; no lower
bound of five unrelated physical generators is claimed.

## 1. The typed principal-parts/Rees square

Let \(R\) be the universal direct-free labelled-edge ring and work in

\[
        R_{\epsilon,\delta}
           =R[\epsilon,\delta]/(\epsilon^2,\delta^2).    \tag{8}
\]

For a multi-affine hafnian row, substitution

\[
 u_v\longmapsto u_v+\epsilon,
 \qquad t\longmapsto t+\delta                           \tag{9}
\]

gives the literal principal-parts expansion

\[
 H_{c_v}(u_v+\epsilon,t+\delta)
 =H_{c_v}+\epsilon A_v+\delta B_v+\epsilon\delta h_v,
 \tag{10}
\]

where

\[
 A_v=\partial_{u_v}H_{c_v},\qquad
 B_v=\partial_tH_{c_v},\qquad
 h_v=\partial_t\partial_{u_v}H_{c_v}.                  \tag{11}
\]

The two difference operators commute, so the four vertices and two edge
directions of (10) form the usual cubical principal-parts bicomplex.  Apply
this construction to both entries of the strict comparison (1).  The
boundary map into the full-nine equation module sends the two first faces to

\[
                         (A_v,-A_v),\qquad(B_v,-B_v),    \tag{12}
\]

whose total global boundaries are zero.  These are source-resolution
cycles because they prolong the polynomial identity \(H^{pq}=H^{pr}\).
They are not being asserted to be coordinate tangent vectors
\(\xi,\eta\in\ker J\) on a geometric full-source locus; constructing such
vectors remains a separate Hasse--Schmidt problem.

The exact first-face counts are

\[
 \#A_v=\begin{cases}15,&v=r=3,\\12,&v\ne r,
       \end{cases}
 \qquad \#B_v=15,\qquad\#h_v=3.                        \tag{13}
\]

The three missing terms in \(A_v\) for \(v\ne r\) are exactly the three
six-vertex matchings containing the direct-free edge \(pr\); hence the count
is \(15-3=12\).  Across all five faces, the ten labelled first-face vectors
have exact rank ten and the five mixed symbols have rank five.  These ranks
describe the constructed square; they are not a lower bound on the number
of new physical generators.

Filter each chart row by direct versus two-star sector.  Every mixed term in
(10) contains \(pq\), so it is in the \(pq\)-direct piece.  Since the same
matching cannot also contain \(pr\), and the direct-free \(pr\) piece is
zero, it lies in the \(pr\)-two-star piece.  The strict global mixed
comparison is zero, while its associated Rees symbol is the sector transfer

\[
              (h_v)_{pq,\mathrm{direct}}
                 -(h_v)_{pr,\mathrm{two\text{-}star}}.  \tag{14}
\]

This is the precise positive construction supplied here.

## 2. Why the shift is forced

The row degree is

\[
 \deg H_{c_v}=e_{x,0}+e_{v,0}+e_{p,0}+e_{q,0}
              +\sum_{i\in F_v}e_{i,m_i}.                \tag{15}
\]

Contraction by the two marked variables removes

\[
 \deg u_v+deg t
   =e_{x,0}+e_{v,0}+e_{p,0}+e_{q,0},                   \tag{16}
\]

leaving \(\deg h_v=\sum_{i\in F_v}e_{i,m_i}\).  Pure
reinsertion contributes

\[
                        \deg Y_0=\sum_{i\in D}e_{i,0}.   \tag{17}
\]

The zero slot \(e_{v,0}\) removed in (16) has already been restored by
(17); the three endpoint slots have not.  Solving the homogeneity equation

\[
                  \deg(h_vY_0)+\sigma=\lambda_v         \tag{18}
\]

therefore gives exactly (4), uniformly for all five faces.  This derives the
module shift from the marked principal-parts square and the pure-output
degree.

## 3. Exact denominator chain-map obstruction

Let \(C_{\rm den}^1\to C_{\rm odd}^0\) be the universal odd denominator
presentation with fifteen generators \(d_{s,a}\).  Coefficient extraction at
`12112` followed by reinsertion of `00000` defines the proposed landing on
the free word module.  Its commutator with the denominator differential is
the map (5).

Because a commutator with a differential is automatically closed, (5)
defines the first obstruction class in the Hom complex of the attempted
landing.  At pure output, the old denominator image is spanned by the five
pure-colour face hafnians \(g_s\).  The exact degree-two ranks are

\[
 \operatorname{rank}\langle g_1,\ldots,g_5\rangle=5,
 \qquad
 \operatorname{rank}\langle g_1,\ldots,g_5,h_1,\ldots,h_5\rangle=10.
                                                               \tag{19}
\]

Thus \([\omega]\ne0\) in the old denominator Hom complex, with five
independent labelled initial components.  The sparse direct-free guard kills
them after specialization, but no guard is used here and that non-flat
vanishing supplies no universal homotopy.

An abstract symbol \(d\tau_v=h_vY_0\) would kill (5) by declaration.  It
would not explain why \(\tau_v\) comes from the full-nine source or why its
target and ordinary residue vanish.  The new cell must instead attach the
denominator face \(d_{v,m_v}\) to the already constructed marked square
(1)--(14).  This is why “denominator-marked two-edge Rees square,” rather
than a bare cap generator, is the minimal source-provenance type identified
by the obstruction.

## 4. Comparison with the split-cap module

The selected split-cap augmented module has existing columns

\[
 T=(-Y,1,0)^{\mathsf T},\qquad
 \rho=(1,0,1)^{\mathsf T},                              \tag{20}
\]

in boundary, physical-target, and ordinary-residue coordinates.  Its
curvature-weighted missing column is

\[
                         p=(\kappa Y,0,0)^{\mathsf T}.   \tag{21}
\]

The exact augmented minor is

\[
                         \det[T\ \rho\ p]=\kappa Y,      \tag{22}
\]

so (21) is absent on the active open.  Landing the Rees symbol before any
curvature comparison would instead give the coefficient \(h_v\), of
internal \(q\)-degree two.  A rank-one polynomial comparison
\(h_v\mapsto\kappa Y\) would require a polynomial \(g\) with

\[
                              g h_v=\kappa Y.             \tag{23}
\]

This is impossible by \(q\)-augmentation.  Allowing all five polars merely
replaces (23) by membership in their ideal, and (6)--(7) give the same
answer.

This is an exact obstruction only for the minimal polynomial comparison.
A larger source construction could use curvature/direct lower faces, a
controlled localization involving internal \(q\)-data, or a non-flat
transgression.  But it must contain a lower component whose
\(q\)-augmentation is nonzero; operations built solely from the quadratic
polars cannot reach the active unit class.

## 5. GHZ-stabilizer torus: formal contraction, no old-source lift

The actual infinitesimal stabilizer of the four-site ternary GHZ tensor is
the six-dimensional abelian diagonal algebra

\[
 \mathfrak a_F=left\{(\lambda_{x,a}):
  \sum_a\lambda_{x,a}=0,\quad
  \sum_x\lambda_{x,a}=0\right\}.                       \tag{24}
\]

The face polar is a weight vector.  Under the identification
\(h_mY_0\leftrightarrow\bigotimes_xE_{0m_x}\), its weight is

\[
 \chi_m(\lambda)=\sum_{x\in F}
                    (\lambda_{x,0}-\lambda_{x,m_x}).    \tag{25}
\]

Every one of the five face words uses both colours 1 and 2.  Choose two face
sites \(i,j\) with \(m_i\ne m_j\), put
\(H=\operatorname{diag}(0,1,-1)\) at \(i\), \(-H\) at \(j\), and zero at
the other sites.  This element \(z_v\in\mathfrak a_F\) preserves all three
GHZ colour sums, and the exact audit gives

\[
                         \chi_m(z_v)=\pm2\ne0.            \tag{26}
\]

Therefore the abelian CE/Koszul complex on the polar's weight summand is
contractible.  The direction of that statement matters.  In cohomological
orientation,

\[
                 h_{\rm CE}(d_{\rm CE}p_v)=p_v.          \tag{27}
\]

In homological/Spencer orientation one may write

\[
 d_{\rm CE}\left(z_v\otimes
             {p_v\over\chi_m(z_v)}\right)=p_v.          \tag{28}
\]

Equation (28) is a genuine boundary only in the **enlarged** Spencer complex.
Its preimage explicitly contains the polar coefficient \(p_v=h_vY_0\) and a
new degree-one ghost \(z_v\).  Neither the ghost nor the polar-valued source
generator occurs in the old full-nine resolution.  The torus action on that
resolution makes its existing differential equivariant, but equivariance
does not insert the missing element in (28).

Thus the exact answer is: the nonzero weight gives a formal Spencer
contraction, but it gives no typed old-source chain homotopy.  Using (28) as
the desired lift would already assume the polar generator.  To become useful,
the Spencer ghost must be identified with a source-provenant cell such as
the denominator-marked square below, and its cap, target, and ordinary-
residue faces must be proved to commute.

## 6. Smallest remaining generator type and nonclaims

The calculation specifies, but does not construct, one new family

\[
 \mathsf J_v=
 [\,K_v;\ d_{v,m_v};\ u_v,t;\ \sigma\,],
 \qquad v=1,\ldots,5,                                  \tag{29}
\]

with the following required faces:

- the strict two-chart comparison \(K_v\);
- its two marked principal-parts faces \(\Xi_v,\Eta_v\);
- the denominator face \(d_{v,m_v}\), canceling (5);
- the derived cap-module shift \(\sigma\);
- zero physical target and zero ordinary residue; and
- a lower cap/curvature face with nonzero \(q\)-augmentation, eventually
  producing the unit coefficient \(\kappa Y\).

One equivariant generator type may package all five labels.  Rank (19) says
that its associated graded must still contain five independent face
components; it does not prove five unrelated physical cells are necessary.

The ordinary-residue map on (24), geometric Hasse--Schmidt tangent vectors,
the curvature lower face, and the full differential square are not
constructed here.  Consequently (24) is a sharp source-generator
specification, not a completed comparison morphism.

The dependency-free checker
[`verify_h3_shifted_principal_parts_comparison_obstruction.py`](../computations/verify_h3_shifted_principal_parts_comparison_obstruction.py)
reconstructs all five rows, their first and mixed principal parts, both
chart-sector placements, the derived shift, the denominator commutator
ranks, the split-cap/augmentation obstruction, and the exact nonzero-weight
GHZ-stabilizer counterguard.  Its frozen digest is

```text
14e7143d6de13609e9cf2001ba37c09e654b785abb1c9b49bc9fa4f5e6a1e659
```
