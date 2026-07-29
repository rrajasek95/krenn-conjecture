# The eighth split at \(k=5\): ten-double projective matching closure

## 1. Result

At \((h,k,M)=(8,5,23)\), the collision profile

\[
                              2^{10}1^3                    \tag{1}
\]

is impossible on the no-extra-singular stratum.

Four double values at formal role two and two singleton values at formal
role one give an exact relation pencil in the cubics.  Leave the third
singleton and six doubles outside.  After quotienting by the outside
singleton row, every two outside-double rows are proportional.  A fourth
Boolean difference over a perfect matching of the other eight doubles
then puts a homogeneous middle-coefficient equation on four projective
edge labels.

For every four/four split of those eight vertices, the nine matching
equations force one side to be projectively flat: its three opposite
edge-pairs have the same unordered pair of labels.  A finite equality-only
lemma forces a monochromatic \(K_5\).  Five double values would therefore
lie in one fibre of a nonconstant rational function whose cleared fibres
have degree at most four, giving the contradiction.  Projective labels
handle one-sided zero increments.  A separate finite pair-map argument
chooses the two fixed anchors so that no edge has both increments zero.

## 2. The mixed formal kernel

Let \({\cal D}\) be the ten double values and \({\cal R}\) the three
singleton values.  Choose

\[
             T\subset{\cal D},\quad |T|=4,
             \qquad R\subset{\cal R},\quad |R|=2,          \tag{2}
\]

and write \(r\) for the singleton outside \(R\).  Put

\[
\begin{aligned}
 Q_T(z)&=\prod_{t\in T}(z+t),&
 H_R(z)&=\prod_{s\in R}(z+s),\\
 C_T(z)&=\prod_{u\in{\cal D}\setminus T}(z-u),&
 A_T(z)&=C_T(z)^2(z-r).                                   \tag{3}
\end{aligned}
\]

Give the four members of \(T\) formal role two and the two members of
\(R\) formal role one.  Their total formal role is ten.  Lower any two
distinct layers.  A lowered double leaves a nonzero singleton mate, while
a lowered original singleton itself becomes a complement singleton.  If
both original singleton layers are lowered, at least one is nonzero.
Thus all fifteen pair-drop cores are legal, including when one exceptional
singleton value is zero.

Use the pairwise-coprime lift factors

\[
 f_t(z)=z^2-t^2\quad(t\in T),
 \qquad g_s(z)=(z-s)(z+s)^2\quad(s\in R).                 \tag{4}
\]

If \(b\in\{0,1,2\}\) lowered layers are original singletons, the
eight-label core represents \(6-b\) value classes.  Its Hermite residual
has degree at most \(3-b\), while its two lift factors have total degree
\(4+b\).  Every lift therefore lies in \(\mathbb C[z]_{\le7}\), and its
rational function has the common form

\[
 F_P(z)={A_T(z)P(z)\over
              (z+\mu)^6Q_T(z)^3H_R(z)^2},
              \qquad P\in\mathbb C[z]_{\le7}.             \tag{5}
\]

Both sides of (5) differ in degree by two.

Let \(K_T\) be the kernel of the four exact order-two selected-double rows
and the two exact order-one selected-singleton rows, and let \(W_T\) be
the span of the fifteen pair-drop lifts.  Then

\[
                         W_T=K_T,\qquad\dim K_T=4.          \tag{6}
\]

Here is the sharp dimension argument.  For a hypothetical \(d\ge5\)
dimensional kernel with unit gcd, the selected rows force Wronskian weight

\[
                         4(d-2)+2(d-1)=6d-10,              \tag{7}
\]

whereas the degree-seven cap is \(d(8-d)\).  Their difference is
\(d^2-2d-10>0\).  The standard gcd corrections only increase it.  The
pair-divisibility subspaces first give \(\dim W_T\ge3\).  If equality held,
the degree-thirteen parity minors would force
\(W_T=G(z){\cal E}(z^2)\).  If \(r_1\) selected-double nodes have gcd order
one, \(r_3\) are absorbed at order at least three, and \(m\) selected
singleton nodes are absorbed at order at least two, the reduced
square-variable Wronskian deficit is

\[
  (2-4+9)+5r_1+7r_3+2m=7+5r_1+7r_3+2m>0.                \tag{8}
\]

Thus dimension three is impossible, proving (6).

The six selected rows on the eight-dimensional polynomial space have
rank four and hence two relations.  Their principal denominator
\(Q_T^3H_R^2\) has degree sixteen.  Moment annihilation gives relation
numerators of degree at most seven.  For such a numerator \(N\), put

\[
                         G_N(z)={(z+\mu)^6N(z)\over A_T(z)}. \tag{9}
\]

After removing the repeated-root gcd of \(A_T\), differentiation has
nominal leading coefficient

\[
                              \deg N+6-13.                 \tag{10}
\]

It cancels at degree seven.  Contact at the selected poles contributes
the degree-ten divisor \(Q_T^2H_R\), so the two relation vectors inject
into an exact plane

\[
                         {\cal S}_T\subset\mathbb C[z]_{\le3}. \tag{11}
\]

Injection follows as usual by evaluating a hypothetical constant
\((z+\mu)^6N/A_T\) at \(-\mu\).

## 3. The Boolean middle coefficient

At the outside singleton \(r\), every \(S\in{\cal S}_T\) satisfies one
exact first-order row.  At an outside double \(u\), it satisfies

\[
 S''(u)+2Y_T(u)S'(u)+\bigl(Y_T(u)^2+J_T(u)\bigr)S(u)=0.   \tag{12}
\]

Restrict the cubic space to the three-dimensional kernel of the singleton
row and use \(w=z-r\).  With \(x=u-r\), \(p=Y_T(u)\), and
\(U=p^2+J_T(u)\), the last two coordinates of the restricted double row
are

\[
 \ell_{2,u}=2+4xp+x^2U,\qquad
 \ell_{3,u}=6x+6x^2p+x^3U.                               \tag{13}
\]

At distinct nodes the singleton residue row and a double residue row are
independent (Hermite interpolation on cubics prescribes the corresponding
jets independently).  Thus every restricted outside-double row is nonzero.
It annihilates the same plane (11), so the restricted rows are proportional.
In particular, for outside doubles \(u,v\),

\[
                         M_T(u,v)=\ell_{2,u}\ell_{3,v}
                                  -\ell_{3,u}\ell_{2,v}=0. \tag{14}
\]

The logarithmic jet is affine in the selected double set:

\[
 Y_T(u)=\kappa_u+\sum_{t\in T}\Phi_u(t),qquad
 \Phi_u(t)={2\over u+t}+{3\over u-t}
           ={5u+t\over u^2-t^2}.                          \tag{15}
\]

Fix \(u,v\), pair the other eight double values into four edges
\(e_i=a_ib_i\), and independently select one endpoint of every edge.
These sixteen choices are precisely the legal four/six double partitions
with \(u,v\) outside.  Set

\[
 \alpha_i=\Phi_u(a_i)-\Phi_u(b_i),\qquad
 \beta_i =\Phi_v(a_i)-\Phi_v(b_i).                         \tag{16}
\]

The exact fourth mixed difference of (14) is

\[
 -4(u-r)^2(v-r)^2(u-v)
 \sum_{i<j}\alpha_i\alpha_j
                 \prod_{k\notin\{i,j\}}\beta_k=0.       \tag{17}
\]

All derivative-jet increments cancel because they have Boolean degree at
most three.  The prefactor is structurally nonzero.  Thus every perfect
matching \({\cal M}\) of the remaining \(K_8\) obeys

\[
 H({\cal M})=
 \sum_{\{e,f\}\subset\mathcal M}\alpha_e\alpha_f
          \prod_{g\in\mathcal M\setminus\{e,f\}}\beta_g=0. \tag{18}
\]

## 4. Choosing anchors without a common-zero edge

Equation (15) gives, for distinct \(a,b\),

\[
 \Phi_u(a)-\Phi_u(b)=
 { (a-b)\bigl(ab+5u(a+b)+u^2\bigr)\over
   (u^2-a^2)(u^2-b^2)}.                                  \tag{19}
\]

If one edge \(\{a,b\}\) has both its \(u\)- and \(v\)-increments zero,
then

\[
                         a+b=-{u+v\over5},\qquad ab=uv.    \tag{20}
\]

In particular, there is at most one such edge for fixed \(u,v\).

We can choose \(u,v\) so that there is none.  On the 45 unordered pairs of
double values, define \(\tau(\{u,v\})=\{a,b\}\) whenever the common
collision (20) exists among the other values.  In sum/product coordinates,

\[
                              \tau:(s,p)\longmapsto(-s/5,p). \tag{21}
\]

The partial map \(\tau\) is injective.  All double values are nonzero on
this stratum.  Its value at
\(U=\{u,v\}\) cannot overlap \(U\): the product equation would then force
\(\tau(U)=U\), and the sum equation would force \(u+v=0\), contrary to the
no-opposite condition.  If \(\tau\) were defined on all 45 pairs, it would
be a permutation and hence would contain a cycle.  A cycle of length \(m\)
would give \(s=(-1/5)^m s\), so \(s=0\), the same contradiction.  Hence
choose \(\{u,v\}\notin\operatorname{dom}\tau\).  Then every edge of the
remaining \(K_8\) has

\[
                         (\beta_e,\alpha_e)\ne(0,0).       \tag{22}
\]

## 5. The projective \(K_8\) lemma

**Lemma 5.1.**  Give every edge \(e\) of \(K_8\) a nonzero vector
\(L_e=(\beta_e,\alpha_e)\).  If (18) holds on every perfect matching, then
some five vertices have proportional edge vectors on all ten of their
edges.

For disjoint edges \(e,f\), let

\[
 q_{ef}=(\beta_e\beta_f,
          \alpha_e\beta_f+\beta_e\alpha_f,
          \alpha_e\alpha_f).                              \tag{23}
\]

This is the coefficient vector of the nonzero binary quadratic
\((\beta_eX+\alpha_eY)(\beta_fX+\alpha_fY)\).  For a four-set \(X\), put
the three vectors (23), one for each perfect matching of \(X\), into a
matrix \(U_X\), and write \(d_X=\operatorname{rank}U_X\ge1\).

For a four/four split \(X\mathbin{\dot\cup}Y\), the nine unions of a
matching of \(X\) and a matching of \(Y\) are perfect matchings of \(K_8\).
Equation (18) says exactly

\[
 U_X
 \begin{pmatrix}0&0&1\\0&1&0\\1&0&0\end{pmatrix}
 U_Y^{\mathsf T}=0.                                      \tag{24}
\]

The middle matrix is nonsingular, hence

\[
                              d_X+d_Y\le3.                 \tag{25}
\]

At least one side has rank one.  On that side, the three nonzero binary
quadratics are proportional.  Unique factorization says that its three
opposite edge-pairs have the same unordered pair of projective labels.
Equivalently, for one of the four vertices, the three star edges have one
label and the complementary triangle edges have one label.  The two labels
are allowed to coincide.

It remains only the following finite equality lemma.

**Lemma 5.2.**  Suppose that for every four/four split of \(K_8\), one side
has a star/triangle equality pattern as above.  Then \(K_8\) contains a
monochromatic \(K_5\).

The lemma is an equality-only finite statement.  For transparency, the
companion checker proves it by a solver-free exhaustive backtrack.  Start
with the 28 edge labels unrelated.  By vertex symmetry, normalize one side
of the first split and one of its four possible star centres.  For each of
the remaining 34 splits not already satisfied, branch over the eight
possible side/centre choices, merge the two triples of equal edges, and
discard a state as soon as a monochromatic five-set appears.  Canonicalizing
the resulting equivalence relation leaves 1,883 visited states and 1,725
distinct dead states; there is no surviving leaf.  Every branch is just one
of the alternatives forced by (25), so this is exhaustive and proves the
lemma without numerical or genericity assumptions.

Lemmas 5.1--5.2 applied to (18) give five double values on whose edges the
vectors (22) are proportional, say

\[
                    B\alpha_{ab}-A\beta_{ab}=0            \tag{26}
\]

for fixed \((A,B)\ne(0,0)\).  Thus all five values lie in one fibre of

\[
                              B\Phi_u(z)-A\Phi_v(z).        \tag{27}
\]

After clearing denominators, a fibre of (27) is a polynomial of degree at
most four.  It is not the zero polynomial: if \(B\ne0\), the poles at
\(\pm u\) cannot be cancelled by \(\Phi_v\), and if \(B=0\), use the poles
at \(\pm v\).  The four poles are distinct by the structural hypotheses.
Five distinct fibre points are impossible.  This contradiction proves
(1).

## 6. Exact audit

[verify_live_three_zero_eighth_split_k5_ten_double_three_singleton_projective_matching_closure.py](../computations/verify_live_three_zero_eighth_split_k5_ten_double_three_singleton_projective_matching_closure.py)
checks all mixed-layer degrees and inequalities, the quotient-row formulas,
the complete fourth Boolean difference, the common-zero pair map, the
nondegenerate binary-quadratic pairing, the four star/triangle patterns,
the exact 35-split equality backtrack, and the quartic fibre bound.
