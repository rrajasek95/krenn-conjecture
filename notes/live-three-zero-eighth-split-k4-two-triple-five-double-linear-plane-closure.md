# The eighth split: two-triple five-double linear-plane closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                         3^2 2^5 1^6                    \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose two double values at formal role two and all six singleton values
at formal role one.  The 28 pair-drop lifts span the exact
four-dimensional kernel in \(\mathbb C[z]_{\le9}\).  Its two row
relations dualize injectively into the linear polynomials and therefore
fill that entire two-dimensional space.

At any outside double \(u\), the second-order residue row must consequently
kill every linear polynomial.  Testing it on \(z-u\) makes the first
logarithmic jet of its regular factor vanish.  Swapping one selected
double with one outside double then forces all four values other than
\(u\) into one fibre of

\[
                         \Phi_u(t)={5u+t\over u^2-t^2}, \tag{2}
\]

whose fibres have size at most two.

## 2. The formal pair-drop kernel

Write \({\cal A}=\{a,b\}\) for the triple values,
\({\cal V}\) for the five double values, and \({\cal R}\) for the six
singleton values.  Choose \(T=\{x,y\}\subset{\cal V}\), put
\(C={\cal V}\setminus T\), and define

\[
\begin{aligned}
 Q_T(z)&=(z+x)(z+y),&
 H(z)&=\prod_{r\in{\cal R}}(z+r),\\
 A_T(z)&=\prod_{u\in C}(z-u)^2
                  (z-a)^3(z-b)^3.                     \tag{3}
\end{aligned}
\]

The two double layers and six singleton layers have formal total role
ten.  Lower any two distinct layers.  Two lowered doubles leave two
nonzero mates; a double--singleton drop leaves a nonzero double mate; and
two omitted singletons leave at least one nonzero singleton.  Thus all
\(\binom82=28\) eight-label cores are legal, including a possible zero
singleton.  In the last case the two omitted singleton classes are
distinct, so at most one of them can be the zero value.

For a double layer \(v\) and singleton layer \(r\), use

\[
                         f_v=z^2-v^2,\qquad
                         f_r=(z-r)(z+r)^2.              \tag{4}
\]

If \(s=0,1,2\) of the lowered layers are singletons, the residual degree
is at most \(5-s\), while the two lift factors have total degree \(4+s\).
Hence every lift \(P_{ij}=f_if_jq_{ij}\) is nonzero of degree at most
nine.  They all lie in the value-row kernel \(K_T\) for

\[
 F_P(z)={A_T(z)P(z)\over
              (z+\mu)^5Q_T(z)^3H(z)^2}.                \tag{5}
\]

Both numerator and denominator degrees differ by two:
\(\deg(A_TP)\le12+9=21\) and the denominator has degree
\(5+6+12=23\).

The two selected-double rows have exact order two and the six singleton
rows exact order one.  For a \(d\)-dimensional subspace of
\(\mathbb C[z]_{\le9}\), their forced Wronskian weight minus the degree
cap is

\[
 2(d-2)+6(d-1)-d(10-d)=d^2-2d-10,                     \tag{6}
\]

positive for \(d\ge5\).  Every gcd correction is stricter, so
\(\dim K_T\le4\).

The 28 pair-drop lifts span at least four dimensions.  This is the exact
mixed-parity lemma: pairwise coprimality first excludes a line and a
plane.  If the span were three-dimensional, the eight divisibility
planes would make every parity minor odd of degree at most seventeen and
vanishing on the exact degree-seventeen divisor supplied by the eight
layer values, with a triple zero at the origin in the zero-singleton
case.  The cross-product identity then makes the primitive space even.
At each of the six singleton squares its vanishing sequence is at least
\((0,2,3)\), contributing weight two.  After \(m\) singleton nodes are
absorbed by the gcd one would need

\[
 2(6-m)\le
 3\left(\left\lfloor{9-m\over2}\right\rfloor-2\right), \tag{7}
\]

which fails for \(m=0,\ldots,5\); for \(m=6\) the square-variable degree
is too small.  Therefore

\[
                         \dim K_T=4.                    \tag{8}
\]

## 3. The dual space is all of \(\mathbb C[z]_{\le1}\)

The eight rows on the ten-dimensional space
\(\mathbb C[z]_{\le9}\) have rank six and hence two relations.  Their
principal-part numerators have the form

\[
 {N(z)\over Q_T(z)^3H(z)^2},\qquad \deg N\le7,          \tag{9}
\]

and the relation-to-\(N\) map is injective.

Put

\[
 g_T=\prod_{u\in C}(z-u)(z-a)^2(z-b)^2,\qquad
 R_T={A_T\over g_T},\qquad D_T={A_T'\over g_T}.         \tag{10}
\]

Thus \(\deg R_T=5\), \(\deg D_T=4\), and \(D_T\) has leading
coefficient twelve.  Differentiating

\[
                         G_N={(z+\mu)^5N\over A_T}
\]

gives

\[
 G_N'={(z+\mu)^4g_T\over A_T^2}\,{\cal E}_T(N),         \tag{11}
\]

where

\[
 {\cal E}_T(N)=R_T\bigl((z+\mu)N'+5N\bigr)
                         -(z+\mu)D_TN.                 \tag{12}
\]

For \(n=\deg N\le7\), the nominal leading coefficient is
\(n+5-12=n-7\).  It cancels at \(n=7\), and
\(\deg{\cal E}_T(N)\le11\).  Contact at the two selected double poles and
six singleton poles gives

\[
                         {\cal E}_T(N)=Q_T^2H\,S_N,
                         \qquad S_N\in\mathbb C[z]_{\le1}, \tag{13}
\]

because \(\deg(Q_T^2H)=4+6=10\).  The map \(N\mapsto S_N\) is injective:
a zero image makes \(G_N\) constant, and evaluation at \(-\mu\) forces
\(N=0\).  Since both spaces in (13) have dimension two,

\[
                         {\cal S}_T=\mathbb C[z]_{\le1}. \tag{14}
\]

More precisely, the relation space maps injectively through
\(c\mapsto N_c\mapsto S_{N_c}\).  Its dimension is two, so this
composite is an isomorphism onto (14).  For every linear \(S\), choose
its relation numerator \(N(S)\).  The following is then the exact
derivative of the rational function \(G_{N(S)}\), not merely a rational
expression with the same local factors:

\[
 G_{N(S)}'=
 { (z+\mu)^4Q_T(z)^2H(z)S(z)\over
   \displaystyle\prod_{u\in C}(z-u)^3
                  (z-a)^4(z-b)^4}.                    \tag{15}
\]

Consequently every finite pole in (15), including every complementary
double and triple value not used to define \(K_T\), has zero residue.

## 4. Outside rows and the quadratic fibre

Fix \(u\in C\), and remove \((z-u)^{-3}\) from (15):

\[
 B_u^T(z)=
 { (z+\mu)^4Q_T(z)^2H(z)\over
   \displaystyle\prod_{v\in C\setminus\{u\}}(z-v)^3
                  (z-a)^4(z-b)^4}.                    \tag{16}
\]

It is a unit at \(u\).  Since (15) is an exact rational derivative, its
outside-double zero residue is

\[
                         (B_u^TS)''(u)=0
                         \qquad(S\in{\cal S}_T).        \tag{17}
\]

By (14), \(S=z-u\) is available.  Equation (17) then gives
\(2(B_u^T)'(u)=0\), or

\[
\begin{aligned}
0=Y_u(T):={}&{4\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 +\sum_{r\in{\cal R}}{1\over u+r}\\
&-3\sum_{v\in C\setminus\{u\}}{1\over u-v}
 -4\left({1\over u-a}+{1\over u-b}\right).             \tag{18}
\end{aligned}
\]

The construction applies to every selected pair \(T\).  Fix \(u\), and
take distinct \(x,v\in{\cal V}\setminus\{u\}\).  Choose a two-set \(T\)
which contains \(x\) but not \(v\), and swap \(x\) for \(v\), keeping
\(u\) outside.  Such a \(T\) exists: its second member can be either of
the two values outside \(\{u,x,v\}\).  Subtracting the two versions of
(18) cancels every
nuisance term and yields

\[
 {2\over u+x}+{3\over u-x}
             ={2\over u+v}+{3\over u-v}.               \tag{19}
\]

Thus all four members of \({\cal V}\setminus\{u\}\) have the same image
under

\[
                         \Phi_u(t)
 = {2\over u+t}+{3\over u-t}
 = {5u+t\over u^2-t^2}.                                \tag{20}
\]

A fibre value \(\lambda\) gives the cleared polynomial

\[
                         \lambda(u^2-t^2)-5u-t=0.       \tag{21}
\]

It is nonzero of degree at most two because its coefficient of \(t\) is
\(-1\).  It cannot have four distinct roots.  This contradiction proves
(1).

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_two_triple_five_double_linear_plane_closure.py](../computations/verify_live_three_zero_eighth_split_k4_two_triple_five_double_linear_plane_closure.py)
checks all 28 cores, the mixed-parity kernel equality, the dual leading
cancellation and linear target, the exact-derivative transfer to every
complementary pole, the outside-double unit and its first jet, all 60
swap witnesses, and the division-free quadratic fibre bound.  The
updated census checker separately audits all 280 legal cores over the
ten choices of selected double pair.
