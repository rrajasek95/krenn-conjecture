# Projective height does not select an active clean cap

## 1. Outcome

Let \(U\) be six ternary boundary sites and let

\[
 {\cal V}=\left(\bigotimes_{w\in W}V_w\right)^*,
 \qquad N=\dim{\cal V}=3^{|W|},
\]

be the space of cap covectors.  The denominator-cleared cap condition is a
homogeneous cubic map

\[
 D:{\cal V}\longrightarrow\bigotimes_{u\in U}V_u,
\]

with at most \(3^6=729\) coordinate equations.  When \(N>729\), projective
height therefore guarantees many nonzero zeros of \(D\).  It does **not**
guarantee a zero satisfying

\[
                         s\kappa_0\kappa_1\kappa_2\ne0. \tag{1}
\]

There are two exact reasons.

1. For every boundary-signature map, \(D\) vanishes on the large linear
   space \(\ker(s,C_2)\), which lies in the forbidden hyperplane \(s=0\).
2. Even the complete linear GHZ contraction identity does not prevent all
   components of \(V(D)\) from lying in the four forbidden hyperplanes.
   An explicit signature below has

   \[
      V(D)=V(s)\ \cup\ V(\kappa_0,\kappa_1,\kappa_2).
                                                               \tag{2}
   \]

Thus dimension or height cannot prove the direct cap-selection theorem.
The exact remaining gate is a **saturated common-edge theorem**:

\[
       (D_\gamma:\gamma\in\{0,1,2\}^U):
       (s\kappa_0\kappa_1\kappa_2)^\infty\ne(1).         \tag{3}
\]

Any proof of (3) must use nonlinear relations saying that all boundary
components come from the same aggregate edge family.  The top GHZ identity,
the size of the cap space, and independence of the four displayed linear
forms are insufficient.

## 2. Denominator clearing

Work in the square-free commutative tensor algebra on \(U\).  Write

\[
 x=\sum_{u<v\in U}A_{uv},\qquad
 C=C_0+C_2+C_4+C_6,\qquad C_0=s.                         \tag{4}
\]

Every \(C_j=C_j(K)\) and \(s=s(K)\) depends linearly on the cap covector
\(K\).  On \(s\ne0\), put \(c_j=C_j/s\).  The logarithmic cumulants are

\[
\begin{aligned}
 L_2&=c_2,\\
 L_4&=c_4-\tfrac12c_2^2,\\
 L_6&=c_6-c_2c_4+\tfrac13c_2^3.                         \tag{5}
\end{aligned}
\]

Because all displayed elements have even site degree, they commute.  A
direct substitution into \(L_6+L_4(x+L_2)\) gives

\[
 L_6+L_4(x+L_2)
 =\frac{C_6+C_4x}{s}
   -\frac{C_2^2x}{2s^2}
   -\frac{C_2^3}{6s^3}.                                 \tag{6}
\]

Consequently the unnormalized condition is exactly

\[
 \boxed{
 D(K)=6s^2(C_6+C_4x)-3sC_2^2x-C_2^3=0.}                \tag{7}
\]

It consists of at most 729 homogeneous cubic equations on \({\cal V}\).
No denominator, choice of affine chart, or genericity assumption occurs in
(7).

Suppose now that the boundary data obey the contraction of the full GHZ
identity for every \(K\):

\[
 C_6+C_4x+\tfrac12C_2x^2+\tfrac16s x^3
      =\sum_{i=0}^2\kappa_iX_i,
 \qquad X_i=e_i^{\otimes U}.                            \tag{8}
\]

Substitution in (7) yields the useful cube form

\[
 \boxed{
 D(K)=6s^2\sum_{i=0}^2\kappa_iX_i-(sx+C_2)^3.}          \tag{9}
\]

Indeed, the four terms in the cube are
\(s^3x^3,3s^2C_2x^2,3sC_2^2x,C_2^3\).  On the open set
(1), equation \(D=0\) is precisely

\[
 H_U\left(x+\frac{C_2}{s}\right)
   =\sum_{i=0}^2\frac{\kappa_i}{s}X_i.                  \tag{10}
\]

Thus a point of the saturated variety in (3) would give the forbidden
ternary six-site source after a one-site diagonal normalization.

## 3. The universal bad linear space

Let

\[
 {\cal Z}_0=\ker\!\left(
        {\cal V}\xrightarrow{(s,C_2)}
        \mathbb C\oplus{\mathscr S}_U^{(2)}\right).      \tag{11}
\]

Every term in (7) contains either \(s\) or \(C_2\), so

\[
                         {\cal Z}_0\subseteq V(D)\cap V(s). \tag{12}
\]

There are \(\binom62 3^2=135\) coordinates in \(C_2\).  Hence

\[
\begin{aligned}
 \operatorname{codim}_{\cal V}{\cal Z}_0&\le136,\\
 \dim\mathbb P({\cal Z}_0)&\ge N-137                    \tag{13}
\end{aligned}
\]

whenever the kernel is nonzero.  By comparison, 729 homogeneous equations
in \(\mathbb P^{N-1}\) give only the crude Krull lower bound

\[
                         \dim V(D)\ge N-730.             \tag{14}
\]

For the first range in which the proposed count is large,
\(|W|=8\) and \(N=6561\), equations (13)--(14) read

\[
       \dim\mathbb P({\cal Z}_0)\ge6424,
       \qquad \dim V(D)\ge5831.                         \tag{15}
\]

Thus the bad linear locus alone is more than large enough to account for
every zero whose existence follows from the generator count.

This also identifies the flaw in a finite-hyperplane-avoidance argument.
A projective variety has a point outside a finite union of hyperplanes only
if some irreducible component is not contained in that union.  Height gives
no such component.  It controls codimension before saturation, while (1)
asks whether anything remains after saturation.

## 4. Exact GHZ-compatible abstract countermodel

The failure persists after imposing (8) and making
\(s,\kappa_0,\kappa_1,\kappa_2\) independent.

Let \({\cal V}\) have any dimension \(N\ge4\), choose four independent
linear forms

\[
                         s,\kappa_0,\kappa_1,\kappa_2
                         \in{\cal V}^*,
\]

and fix an arbitrary degree-two boundary element \(x\).  Define the linear
boundary-signature maps

\[
\begin{aligned}
 C_0&=s,\\
 C_2&=-s x,\\
 C_4&=0,\\
 C_6&=\sum_{i=0}^2\kappa_iX_i+\tfrac13s x^3.            \tag{16}
\end{aligned}
\]

These maps obey (8), since the coefficient of \(sx^3\) on its left is

\[
                         \tfrac13-\tfrac12+\tfrac16=0.  \tag{17}
\]

Moreover \(sx+C_2=0\), so (9) becomes

\[
                         D=6s^2\sum_{i=0}^2\kappa_iX_i. \tag{18}
\]

The three tensors \(X_i\) are independent.  Therefore

\[
 D(K)=0
 \quad\Longleftrightarrow\quad
 s(K)=0\ \ \text{or}\ \
 \kappa_0(K)=\kappa_1(K)=\kappa_2(K)=0,                 \tag{19}
\]

which proves (2).  Every zero violates (1), although the complement of the
four hyperplanes is nonempty and can have arbitrarily large dimension.

The failure has a one-line ideal certificate.  In coordinates containing
the four chosen linear forms, the nonzero coordinate ideal of \(D\) is

\[
 I_D=(s^2\kappa_0,s^2\kappa_1,s^2\kappa_2),\qquad
 h=s\kappa_0\kappa_1\kappa_2.                           \tag{20}
\]

Then

\[
 h^2=(s^2\kappa_0)
          (\kappa_0\kappa_1^2\kappa_2^2)\in I_D,        \tag{21}
\]

so \(h\in\sqrt{I_D}\) and

\[
                         I_D:h^\infty=(1).              \tag{22}
\]

Adding any number of dummy cap coordinates leaves (20)--(22) unchanged.
Thus no projective dimension threshold can repair the argument.

Nor does imposing the four affine normalizations first.  On the nonempty
affine space

\[
                         s=\kappa_0=\kappa_1=\kappa_2=1,
\]

equation (18) is the fixed nonzero tensor
\(6(X_0+X_1+X_2)\).  Thus the restricted coordinate ideal is the unit
ideal even when this affine slice has arbitrarily large dimension.  The
usual “more variables than equations” heuristic has no affine existence
content here.

To realize the four linear forms with the intended cap notation, take
\(|W|\ge2\), let \(g_i=e_i^{\otimes W}\), choose
\(h_W\notin\operatorname{span}\{g_0,g_1,g_2\}\), and set

\[
                 \kappa_i(K)=K(g_i),\qquad s(K)=K(h_W). \tag{23}
\]

Then (16) is an exact linear abstract boundary-signature family whose top
contraction is the right side of (8) for every covector \(K\).  It is not
claimed to arise from one aggregate matching edge family.

## 5. What common-edge input must accomplish

The qualification in the last sentence is the entire remaining opening.
For an actual source, \(C_0,C_2,C_4,C_6\) are not independent linear maps:
they are contractions of matching cofactors built from the same internal,
cross, and boundary edge blocks.  The GHZ equation supplies (8), but the
formal construction (16) proves that (8) alone does not encode those
nonlinear common-edge relations.

Accordingly, a dimension-based continuation needs a theorem of the
following exact form.

**Required gate.**  For every boundary-signature map arising from a common
aggregate edge family and satisfying (8), prove that the pulled-back cubic
ideal \(I_D\) has a component outside
\(V(s\kappa_0\kappa_1\kappa_2)\); equivalently, prove (3).

The pair-adjugate identity is an example of genuinely relevant common-edge
information: it places a nondecomposable alternating cubic in the mixed
kernel by using shared-star product relations.  It does not by itself put a
decomposable cube in that kernel.  Any successful height argument must
convert such common-edge identities into a statement about the **saturated**
ideal, not merely add more unsaturated equations or count their number.

The companion checker
[verify_cap_condition_projective_height_obstruction.py](../computations/verify_cap_condition_projective_height_obstruction.py)
verifies (17)--(22) symbolically, including a Gröbner saturation certificate,
and audits the dimension counts in (13)--(15).
