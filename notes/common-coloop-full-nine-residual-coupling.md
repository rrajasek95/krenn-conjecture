# Common-coloop full-nine residual coupling

## 1. Outcome

Let \(h\geq3\), let \(|W|=2h\), and suppose the literal fixed-label
pair equations are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                      \tag{1}
\]

Assume both endpoint maps are injective and that, at one site \(x\),
both off-\(x\) endpoint maps have rank two.  Let \(c,d\) span their
kernel lines.  The
[rank-two-shore theorem](full-nine-rank-two-shore-coordinate-support.md),
with its
[independent audit](residual-macaulay-and-rank-two-shore-independent-audit.md),
says that each of \(c,d\) has at most two fixed-coordinate entries.  Its
bilinear consequence routes the common-coloop chart to

* a zero, unary, or binary \(q^{[h]}\); or
* coordinate-disjoint supports of \(c,d\).

This note proves a uniform refinement of both branches.  Its formulas and
branch classification were checked independently in
[the accompanying audit](common-coloop-full-nine-residual-coupling-independent-audit.md).

Write

\[
 q=q_0+\rho
\]

where \(q_0\) is supported away from \(x\) and every term of \(\rho\)
uses \(x\).  Put

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 \Phi(z)=zA,qquad I=\operatorname {im}\Phi.                  \tag{2}
\]

Here \(I\) is a subspace of the top component on the odd set
\(W\setminus\{x\}\).  The main conclusions are as follows.

1. **Every kernel-supported label is liftable.**  If \(c_i\ne0\) or
   \(d_i\ne0\), then the off-\(x\) monochromatic tensor \(Y_i\) lies in
   \(I\).  Consequently, if

   \[
        \operatorname {supp}(c)\cup\operatorname {supp}(d)
             =\{0,1,2\},                                      \tag{3}
   \]

   one can choose \(z_i\) with \(z_iA=Y_i\) and form

   \[
      \widetilde q=q_0+\sum_i e_i^{(x)}z_i,
      \qquad \widetilde q^{[h]}=X_0+X_1+X_2.                  \tag{4}
   \]

   Thus (3) gives the exact \(N\mapsto N-2\) descent immediately.  More
   generally, the same descent follows whenever all three \(Y_i\) happen
   to lie in \(I\), whether or not their labels occur in the two kernels.

2. **The non-descent quotient is diagonal curvature.**  Every row of
   (1) has an exact, coefficient-free Taylor splitting

   \[
   a_{ij}Q+p_{i,x}H_j+s_{j,x}G_i+\Gamma_{ij}
        =\delta_{ij}e_i^{(x)}\otimes Y_i,                     \tag{5}
   \]

   where

   \[
   \begin{aligned}
     Q&=q^{[h]}=\rho A,\\
     H_j&=\bar s_jA,\qquad G_i=\bar p_iA,\\
     \Gamma_{ij}&=\rho\,\bar p_i\bar s_jB.
   \end{aligned}                                               \tag{6}
   \]

   Bars mean restriction away from \(x\).  Modulo
   \(V_x\otimes I\), the direct term, both first jets, and \(Q\) vanish,
   leaving

   \[
       \boxed{\quad
       \overline\Gamma_{ij}
          =\delta_{ij}e_i^{(x)}\otimes\overline Y_i.
       \quad}                                                   \tag{7}
   \]

   Hence the only surviving data are diagonal corners indexed by

   \[
        M=\{i:Y_i\notin I\}
          \subseteq\{0,1,2\}\setminus
          \bigl(\operatorname {supp}(c)\cup
                 \operatorname {supp}(d)\bigr).               \tag{8}
   \]

3. **The disjoint branch is almost closed.**  Disjoint supports of sizes
   \(2+1\) cover all three labels, so (4) gives descent.  A non-descending
   disjoint branch therefore has two singleton kernels on distinct labels,
   say

   \[
                  c=e_r,qquad d=e_s,qquad r\ne s,            \tag{9}
   \]

   after harmless kernel-line scalings.  If \(t\) is the third label and
   \(Y_t\notin I\), then the entire quotient packet is the rank-one
   endpoint-ordered table

   \[
   \begin{array}{c|cc}
        &\bar s_r&\bar s_t\\ \hline
    \bar p_s&0&0\\
    \bar p_t&0&e_t^{(x)}\otimes\overline Y_t .
   \end{array}                                                 \tag{10}
   \]

   The other five quotient rows and columns vanish.  This is the exact
   residual behind the two differently labelled anchors and their crossed
   target-zero row.

4. **The pure branch has the same quotient residual.**  If
   \(\beta=c^{\mathsf T}ad\ne0\) and \(Q\ne0\), then

   \[
        \beta Q=\sum_i c_id_iX_i.                              \tag{11}
   \]

   A binary \(Q\) forces both kernel supports to be its same two labels;
   the third label is the sole possible member of \(M\).  A unary \(Q\)
   has one common kernel label.  If both kernels use different additional
   labels, their union has size three and descent follows.  Otherwise one
   or two diagonal curvature corners remain, according to \(|M|\).

5. **Scalar-zero response does not remove the corner.**  For an
   off-diagonal direct entry \(\alpha=a_{ab}\ne0\), put

   \[
       \tau=\operatorname {tr}a,
       \qquad K_*=\tau E_{ab}-\alpha I.
   \]

   Contracting (7) gives, without cancelling a common power,

   \[
       \sum_{i,j}(K_*)_{ij}\overline\Gamma_{ij}
          =-\alpha\sum_{m\in M}
             e_m^{(x)}\otimes\overline Y_m.                   \tag{12}
   \]

   Thus the missing pure scalar-zero response is carried entirely by the
   curvature quotient.  The crossed zero row constrains a different entry
   of the same endpoint-ordered bilinear table, but it is invariant under
   the relative two-label torus.  It does **not** fix the relative gauge or
   identify this corner with an overlap minor.

These statements use the complete nine literal equations and the actual
consecutive powers through (2), except for the explicitly labelled guards
in Sections 8--9.  They close every common-coloop support pattern whose
kernel labels cover all three colours.  They do not yet exclude the
rank-one corner (10), the unary two-corner version, or the separately
defined endpoint-degenerate overlap/Omega bad strata.  No identification
between a local anchor scalar and an Omega column is assumed.  Closing
those residuals still requires source-faithful two-chart overlap
injectivity.

## 2. Ambient algebra and hypotheses

Work in

\[
 {\cal R}_W=\bigotimes_{y\in W}(\mathbb C\oplus V_y),
 \qquad V_yV_y=0,                                             \tag{13}
\]

with fixed physical bases
\(e_0^{(y)},e_1^{(y)},e_2^{(y)}\).  Put

\[
 X_i=\bigotimes_{y\in W}e_i^{(y)},
 \qquad
 Y_i=\bigotimes_{y\ne x}e_i^{(y)}.                           \tag{14}
\]

Let

\[
 P(e_i)=p_i,qquad S(e_j)=s_j                              \tag{15}
\]

be injective maps from their fixed three-dimensional row-index spaces.
Assume

\[
       \operatorname {rank}P_{\bar x}
       =\operatorname {rank}S_{\bar x}=2.                    \tag{16}
\]

Choose nonzero kernel vectors

\[
       c\in\ker P_{\bar x},qquad
       d\in\ker S_{\bar x},                                 \tag{17}
\]

and set

\[
       u=P_x(c),\qquad v=S_x(d).                              \tag{18}
\]

Global injectivity makes \(u,v\ne0\).  We use the audited conclusion

\[
       |\operatorname {supp}(c)|\le2,qquad
       |\operatorname {supp}(d)|\le2,                         \tag{19}
\]

and, when either support has size two, the corresponding local vector
\(u\) or \(v\) is proportional to one of its two fixed physical axes.
No change of the fixed row labels or physical colour axes is made below.

## 3. The uncancelled common-site Taylor identity

Decompose every source term at \(x\):

\[
 q=q_0+\rho,qquad
 p_i=\bar p_i+p_{i,x},qquad
 s_j=\bar s_j+s_{j,x}.                                      \tag{20}
\]

Every term of \(\rho\) contains one factor at \(x\).  Hence
\(\rho^{[2]}=0\).  Since \(W\setminus\{x\}\) has only \(2h-1\) sites,
\(q_0^{[h]}=0\).  Divided-power expansion therefore gives exactly

\[
 q^{[h]}=\rho q_0^{[h-1]}=\rho A,
 \qquad
 q^{[h-1]}=A+\rho B.                                        \tag{21}
\]

There are no binomial or factorial coefficients in (21).

In the product \(p_i s_jq^{[h-1]}\), the term
\(\bar p_i\bar s_jA\) has degree \(2h\) on only \(2h-1\) sites and
vanishes.  Terms containing both a local \(x\)-factor and \(\rho\) also
vanish by \(V_xV_x=0\).  The surviving terms are precisely

\[
 p_i s_jq^{[h-1]}
  =p_{i,x}(\bar s_jA)+s_{j,x}(\bar p_iA)
       +\rho\bar p_i\bar s_jB.                               \tag{22}
\]

This proves (5)--(6).  It is important that the last term in (22) is not
obtained by cancelling \(A\).  It is the literal second polar of the
same \(q_0\), with all endpoint order retained.

The kernel relations imply

\[
 \sum_i c_iG_i=0,qquad \sum_i c_i\Gamma_{ij}=0,
 \qquad
 \sum_j d_jH_j=0,qquad \sum_j d_j\Gamma_{ij}=0.             \tag{23}
\]

Thus \(\Gamma\) factors, as an endpoint-ordered tensor-valued bilinear
map, through the two quotient row spaces

\[
       \mathbb C^3/\mathbb Cc
       \quad\text{and}\quad
       \mathbb C^3/\mathbb Cd.                               \tag{24}
\]

Taking the \(c\)-combination of the rows and the \(d\)-combination of
the columns in (5) gives the two anchored identities

\[
 \boxed{
 \begin{aligned}
   b_jQ+u\otimes H_j&=c_j e_j^{(x)}\otimes Y_j,
      &b&=c^{\mathsf T}a,\\
   g_iQ+v\otimes G_i&=d_i e_i^{(x)}\otimes Y_i,
      &g&=ad.
 \end{aligned}}                                               \tag{25}
\]

Taking both combinations gives

\[
       (c^{\mathsf T}ad)Q=\sum_i c_id_iX_i,                  \tag{26}
\]

because \(P(c)S(d)=uv=0\) at the same square-zero site.  Equations
(22), (25), and (26) are the complete one-site ledger used below.

## 4. Kernel labels lie in the multiplication image

The definition of \(I\) in (2) gives

\[
       Q\in V_x\otimes I,qquad H_j,G_i\in I.                 \tag{27}
\]

If \(c_j\ne0\), equation (25) places

\[
        e_j^{(x)}\otimes Y_j\in V_x\otimes I.
\]

Contracting the first factor by any covector nonzero on
\(e_j^{(x)}\) proves \(Y_j\in I\).  The transposed equation proves the
same assertion when \(d_j\ne0\).  Hence

\[
 \boxed{\quad
   \{Y_j:c_j\ne0\text{ or }d_j\ne0\}\subseteq I.
 \quad}                                                       \tag{28}
\]

This argument does not inspect individual matchings and does not infer
termwise vanishing.  All complex cancellation has already been absorbed
in the exact vector \(A=q_0^{[h-1]}\).

Suppose now that \(Y_0,Y_1,Y_2\in I\).  Choose
\(z_i\in({\cal R}_{\bar x})_1\) such that \(z_iA=Y_i\), and put

\[
       \widetilde\rho=\sum_i e_i^{(x)}z_i,
       \qquad \widetilde q=q_0+\widetilde\rho.                \tag{29}
\]

Every term of \(\widetilde\rho\) uses \(x\), so the same calculation as
in (21) gives

\[
       \widetilde q^{[h]}
          =\widetilde\rho A
          =\sum_i e_i^{(x)}\otimes Y_i
          =X_0+X_1+X_2.                                      \tag{30}
\]

This is a literal exact ternary matching source on the \(2h\) sites
\(W\).  In a minimal-counterexample argument it is the desired two-site
descent.  No cleanliness test, selector choice, or root extraction is
needed on this branch.

## 5. The curvature quotient

Put

\[
       \overline Z=Z/I,
       \qquad Z=\bigotimes_{y\ne x}V_y.                       \tag{31}
\]

Reduce (5) modulo \(V_x\otimes I\).  Equation (27) kills \(Q\) and both
first jets.  This proves (7):

\[
       \overline\Gamma_{ij}
          =\delta_{ij}e_i^{(x)}\otimes\overline Y_i.          \tag{32}
\]

By (28), \(\overline Y_i=0\) for every label in the union of the two
kernel supports.  Therefore the quotient packet is the diagonal tensor

\[
       \overline\Gamma
          =\sum_{m\in M}E_{mm}\otimes
                  (e_m^{(x)}\otimes\overline Y_m),            \tag{33}
\]

with \(M\) as in (8).  It still has the left kernel \(c\) and right
kernel \(d\), by (23).

This is the promised coupling of anchors and curvature.  The diagonal
anchors on the kernel-supported labels do not themselves contradict the
common-coloop chart; they put their off-site monochromatic factors into
the lift image \(I\).  What remains is exactly the failure of the other
monochromatic factors to enter that same image, recorded by the second
polar \(\Gamma\).

For the scalar-zero matrix \(K_*\), one has

\[
       \sum_{i,j}(K_*)_{ij}a_{ij}=0,
       \qquad (K_*)_{ii}=-\alpha.                             \tag{34}
\]

Contracting (5) and then reducing modulo \(I\) gives (12).  In
particular, each missing pure response coefficient is nonzero in the
curvature quotient.  This is stronger than saying merely that some
uncancelled curvature term exists, but it is not an injectivity theorem
for the overlap complex.

## 6. Consequences for the two audited branches

Let

\[
       C=\operatorname {supp}(c),\qquad
       D=\operatorname {supp}(d),\qquad
       \beta=c^{\mathsf T}ad.                                 \tag{35}
\]

### 6.1 Coordinate-disjoint kernels

Suppose \(C\cap D=\varnothing\).  Both sets are nonempty and have size at
most two.  Hence either their sizes are \(2+1\), in which case
\(C\cup D=\{0,1,2\}\) and Section 4 gives descent, or their sizes are
\(1+1\).

In the non-descending case, scale the kernel lines so that

\[
             c=e_r,qquad d=e_s,qquad r\ne s,                 \tag{36}
\]

and let \(t\) be the remaining label.  Then

\[
       \bar p_r=0,qquad \bar s_s=0.                          \tag{37}
\]

The curvature map factors through rows \(s,t\) on the first endpoint
and columns \(r,t\) on the second endpoint.  If \(Y_t\notin I\), (32)
is exactly the table (10).  Thus the disjoint residual is not an arbitrary
rank-two tensor packet.  It is one rank-one mixed curvature corner, with
three adjacent zero entries in the endpoint-ordered quotient rectangle.

There is also a useful sharp local description before quotienting.  If
\(Q=0\), (25) forces

\[
       u\parallel e_r^{(x)},\qquad v\parallel e_s^{(x)},       \tag{38}
\]

and

\[
 \begin{array}{lll}
 H_r\ne0,&H_r\parallel Y_r,&H_j=0\ (j\ne r),\\
 G_s\ne0,&G_s\parallel Y_s,&G_i=0\ (i\ne s).
 \end{array}                                                   \tag{39}
\]

Indeed, each nonzero anchor in (25) is then an equality of pure tensors;
two active entries in either kernel would force the same nonzero local
vector onto two different fixed axes.  This is another direct proof that
the zero-power disjoint residual is necessarily singleton--singleton.

Its crossed target-zero row is the literal identity

\[
       p_{s,x}H_r+s_{r,x}G_s+\Gamma_{sr}=0.                   \tag{40}
\]

The third diagonal row is curvature-only:

\[
                         \Gamma_{tt}=X_t.                     \tag{41}
\]

Equation (40) does not force any of its three summands to vanish.

If \(Q\ne0\), put

\[
       b=c^{\mathsf T}a,qquad g=ad.                           \tag{42}
\]

If \(b_r=0\), the first anchor in (25) forces
\(u\parallel e_r\); if \(g_s=0\), the second forces
\(v\parallel e_s\).  These are endpoint-anchor degeneracies.

Suppose instead that \(b_r g_s\ne0\) and that neither local vector is
aligned with its own anchor axis.  Then the two anchor equations imply

\[
       \operatorname {span}\{u,e_r\}
        =\operatorname {span}\{v,e_s\}
        =\operatorname {span}\{e_r,e_s\},                    \tag{43}
\]

and \(u,v\) are independent.  Write

\[
 u=A_0e_r+B_0e_s,qquad
 v=C_0e_r+D_0e_s,qquad
 \Delta=A_0D_0-B_0C_0\ne0.                                  \tag{44}
\]

Indeed, the two anchor equations first put

\[
 Q\in\bigl(\operatorname {span}\{u,e_r\}\otimes Z\bigr)
       \cap
       \bigl(\operatorname {span}\{v,e_s\}\otimes Z\bigr).     \tag{44a}
\]

If the two planes in (44a) were distinct, their intersection would be a
line and \(Q\) would have local tensor rank one.  The first anchor would
then force its off-site factor to be proportional to \(Y_r\), while the
second would force the same factor to be proportional to \(Y_s\), which
is impossible.  Hence the planes agree and must be the fixed coordinate
plane through \(e_r,e_s\).  If \(u,v\) were proportional, projecting the
two anchors modulo their common line would force both \(e_r\) and \(e_s\)
onto that line, another contradiction.  This proves (43)--(44).

Then comparison of the two local-factor coefficients gives the unique
crossed two-fibre form

\[
 \boxed{
 Q=-{B_0\over b_r\Delta}\,v\otimes Y_r
   -{C_0\over g_s\Delta}\,u\otimes Y_s.}                    \tag{45}
\]

Both displayed coefficients are nonzero under the unaligned hypothesis.
Consequently every zero-target anchor equation outside \(r,s\) has zero
first jet, and the label \(t\) again survives only in curvature modulo
\(I\).  If one coefficient in (45) disappears, the corresponding local
axis is aligned and \(Q\) is an endpoint-fibre degeneration.  Thus the
nonzero disjoint branch routes uniformly to

* an endpoint-anchor/fibre degeneration; or
* the two-sided crossed form (45) with the same rank-one quotient corner
  (10).

No enumeration of supports or matching terms is involved.

### 6.2 Unary or binary \(q^{[h]}\)

If \(\beta=0\), equation (26) gives \(c_id_i=0\) for every \(i\), so this
is already the disjoint branch.  Suppose \(\beta\ne0\) and \(Q\ne0\).
Then (26) gives

\[
       Q=\sum_{i\in C\cap D}{c_id_i\over\beta}X_i,            \tag{46}
\]

and every coefficient in the displayed intersection is nonzero.

If \(Q\) is binary on labels \(r,s\), then

\[
                       C=D=\{r,s\}.                           \tag{47}
\]

Thus \(Y_r,Y_s\in I\), and the third label \(t\) is the only possible
member of \(M\).  If it also lies in \(I\), descent follows.  Otherwise
the whole residual is the single curvature corner

\[
            \overline\Gamma_{tt}
               =e_t^{(x)}\otimes\overline Y_t.                \tag{48}
\]

The rank-two-shore coordinate theorem gives a little more.  If
\(u=\eta e_r^{(x)}\), write

\[
       Q=\lambda_rX_r+\lambda_sX_s,
       \qquad \lambda_r\lambda_s\ne0.                         \tag{49}
\]

Projecting the first equation of (25) modulo \(\mathbb Cu\) yields

\[
 \begin{aligned}
  b_r&=b_t=0,& b_s&={c_s\over\lambda_s},\\
  H_r&={c_r\over\eta}Y_r,&
  H_s&=-{b_s\lambda_r\over\eta}Y_r,&H_t&=0.
 \end{aligned}                                                \tag{50}
\]

There is a transposed formula for \(v\) and \(G\).  Thus each binary
shore has a star-only anchor on its locally aligned label.  This is a local
anchor-scalar degeneration, not yet an identification with a zero Omega
column.  The missing diagonal row is

\[
              \Gamma_{tt}=X_t-a_{tt}Q.                        \tag{51}
\]

Its \(Y_t\)-quotient is (48).

If \(Q=\lambda X_r\) is unary, both kernel supports contain \(r\).  There
are only three structural possibilities.

* If both kernels have distinct extra labels, their union has size three
  and Section 4 gives immediate descent.
* If exactly one shore has support \(\{r,k\}\), while the other has
  support \(\{r\}\), then \(Y_r,Y_k\in I\); only the third label can
  remain in \(M\).  On the expanded shore its local kernel vector is
  forced onto the extra axis \(e_k\), and that extra anchor is star-only.
* If both supports equal \(\{r\}\), then \(p_r,s_r\) are supported only
  at \(x\), so their product is zero and the active diagonal equation is

  \[
                         a_{rr}Q=X_r.                          \tag{52}
  \]

  The two other labels may give a two-corner diagonal curvature packet
  in \(\overline Z\).

This exhausts the pure common-site branch at the level of support and
first-jet geometry.  It leaves no unbounded support census.

## 7. Why the crossed zero row is not yet overlap injectivity

In the disjoint singleton normalization (36), the two kernel contractions
give differently labelled anchors \(r,s\).  The original \((s,r)\) row
is their crossed target-zero equation (40).  Nevertheless, (40) remains
invariant under the relative diagonal action on the two aligned label
axes.  In the notation of transported selector flags, the character
\(g_s/g_r\) can change while the two diagonal anchors and their zero target
remain fixed; the curvature correction \(\Gamma_{sr}\) changes with the
same character and absorbs the first-jet leakage.

Accordingly, the four-index coefficient-dark row used in a literal
four-cut must not be identified with a transported matrix unit
\(E_{rs}\).  Two anchors give partial flag alignment, while the zero row
only gives (40).  Fixing the relative gauge requires the additional
source-faithful overlap comparison.  This distinction is visible already
in the guard below.

## 8. A formal full-nine rank-one-corner guard

The following uniform packet shows that all nine site-graded response
rows, endpoint injectivity, disjoint singleton kernels, two anchors, their
crossed zero row, and scalar-zero response do not by themselves kill the
corner.  It deliberately omits only the existence of one quadratic \(q\)
whose consecutive divided powers are the displayed \(Q,F\).

Choose distinct sites \(x,a,b,c,d\in W\) and put

\[
 \begin{array}{lll}
 p_0=e_0^{(x)},&p_1=e_1^{(a)},&p_2=e_2^{(b)},\\
 s_0=e_0^{(c)},&s_1=e_1^{(x)},&s_2=e_2^{(d)}.
 \end{array}                                                  \tag{53}
\]

Define degree-\((2h-2)\) tensors

\[
 \begin{aligned}
 F_0&=\bigotimes_{y\in W\setminus\{x,c\}}e_0^{(y)},\\
 F_1&=\bigotimes_{y\in W\setminus\{a,x\}}e_1^{(y)},\\
 F_2&=\bigotimes_{y\in W\setminus\{b,d\}}e_2^{(y)},\\
 F&=F_0+F_1+F_2,qquad Q=0.
 \end{aligned}                                                \tag{54}
\]

The holes of \(F_i\) are exactly the two sites occupied by \(p_i,s_i\).
Therefore

\[
                         p_i s_jF=\delta_{ij}X_i              \tag{55}
\]

for all nine ordered pairs.  For \(i\ne j\), either one port collides
with \(F_k\) for every \(k\), or \((i,j)=(0,1)\) and the two ports
already collide at \(x\).  Thus (55) is a full tensor equality, not a
selected-word check.

Both endpoint triples are injective.  Away from \(x\), the first has
kernel \(e_0\) and the second has kernel \(e_1\).  The restriction of
\(F\) away from \(x\) contains the first two lift rows but loses \(F_2\):
the labels \(0,1\) are in the formal analogue of \(I\), while the
\(X_2\) row is supplied by the sole mixed corner \(p_2s_2F_2\).
Explicitly,

\[
 e_0^{(c)}F_0=Y_0,\qquad e_1^{(a)}F_1=Y_1,
\]

whereas the off-\(x\) restriction has no all-colour-\(2\) component.

Take, for example, \(a=E_{01}\).  Then \(\alpha=1\),
\(\operatorname {tr}a=0\), and \(K_*=-I\).  Contracting (55) gives the
exact scalar-zero row

\[
           -\sum_i p_i s_iF=-(X_0+X_1+X_2).                  \tag{56}
\]

At the abstract Taylor-table level, one may also add arbitrary local
leakage to the crossed row and absorb it in its tensor-valued curvature
entry.  This is not asserted to modify the concrete packet (53)--(55).
For arbitrary \(\xi,\eta\in V_x\), the assignments

\[
 p_{1,x}=\xi,qquad s_{0,x}=\eta,qquad
 \Gamma_{10}=-\xi\otimes Y_0-\eta\otimes Y_1                \tag{57}
\]

preserve the crossed zero equation.  The curvature table still factors
through the two rank-two quotient shores.  This is the relative-torus
freedom which a crossed target-zero row alone cannot remove.

The packet is not a Krenn source: no \(q\) with

\[
                       q^{[h-1]}=F,qquad q^{[h]}=0            \tag{58}
\]

is supplied.  Its role is exact and limited.  Any proof which replaces
the consecutive powers by independent tensors, or which retains only the
nine response products and the anchored quotient table, cannot close the
rank-one corner.

## 9. A literal consecutive-power curvature guard

Conversely, consecutive divided powers alone do not make a second-polar
corner vanish.  This can be seen uniformly with an actual quadratic.

On five off-\(x\) sites \(0,1,2,3,4\), use one fixed physical axis and
take the single edge

\[
                              q_\circ=z_3z_4.                  \tag{59}
\]

For \(h=3\), put \(q_0=q_\circ\).  For \(h>3\), add \(h-3\) disjoint
unit edges on the remaining \(2h-6\) off-\(x\) sites and call their sum
\(m\); put

\[
                              q_0=q_\circ+m.                   \tag{60}
\]

There are only \(h-2\) mutually disjoint supported edges, so

\[
                         q_0^{[h-1]}=0.                        \tag{61}
\]

But, with \(B=q_0^{[h-2]}\),

\[
 z_0z_1z_2B
   =z_0z_1z_2z_3z_4
      \prod_{e\text{ in the padding}}e\ne0.                  \tag{62}
\]

Now put \(\rho=e^{(x)}z_0\), \(\bar p=z_1\), and \(\bar s=z_2\).  Then

\[
 \rho q_0^{[h-1]}=0,qquad
 \bar p q_0^{[h-1]}=\bar s q_0^{[h-1]}=0,qquad
 \rho\bar p\bar s q_0^{[h-2]}\ne0.                           \tag{63}
\]

Thus even three first-stage annihilations do not imply vanishing of the
literal second polar.  This guard does not satisfy the diagonal anchors
or the full nine rows; Section 8 supplies that complementary half.  The
two guards together show why the remaining proof must use the full-nine
rows and the faithful overlap of their actual consecutive-power
representatives simultaneously.

## 10. Exact remaining gap

The common-coloop residual is now smaller than an arbitrary anchored
Macaulay or Omega problem.

* In the coordinate-disjoint branch, all \(2+1\) support patterns descend.
  The only non-descending support is singleton--singleton, and its quotient
  is the rank-one corner (10).
* In the binary pure branch, the two active labels lie in \(I\), the third
  label is the only possible missing lift, and both shores are already on
  endpoint-degenerate anchor strata as in (50).
* In the unary branch, the three-label union descends.  A two-label union
  leaves one curvature corner; a singleton union leaves at most two
  diagonal corners and has the direct-only active anchor (52).

On two overlapping physical charts, the raw source representatives obey
the power-free connection and four-cut curvature equations, including the
nonzero physical minor \(AU-BF\).  What is still needed is the following
source-relative statement.

> **Common-coloop curvature-corner injectivity target.**  On the open
> overlap locus with nonzero physical curvature and the required good
> endpoint stars, the literal full-nine connection cannot carry the
> nonzero diagonal quotient packet (33), together with its crossed zero
> rows, on both charts while both clean-error/Omega pencils remain in
> their independent or endpoint-degenerate bad strata.

This target must compare the actual representatives before multiplication
by \(q_0^{[h-2]}\).  It cannot cancel that common power, identify the
four-index dark coefficient with \(E_{rs}\), or infer the relative gauge
from the crossed zero row.  The formal guard in Section 8 blocks the first
two shortcuts, and the literal guard in Section 9 blocks the third-stage
annihilator shortcut.

No contradiction for the final rank-one or unary two-corner overlap
packet is claimed here.  The proved advance is the uniform image-lift
descent (28)--(30) and the exact reduction of every remaining common-coloop
branch to the diagonal curvature quotient (33).
