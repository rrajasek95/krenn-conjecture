# The eighth split: all-order formal-five-layer duality

## 1. Uniform theorem

Fix the eighth split and allow arbitrary common-pole order:

\[
                         h=8,\qquad p=8+k,\qquad k\ge1,
 \qquad M=k+18.                                         \tag{1}
\]

Choose five distinct exceptional value classes of multiplicity at least
two and regard two labels from each as a formal double layer.  Suppose
all ten cores obtained by lowering two different layers from role two to
role one are legal for the simultaneous-Hermite reduction.

Subtract the two formal labels in each chosen class from its actual
multiplicity.  Let

\[
                         A(z)=\prod_{j=1}^{c}(z-y_j)^{m_j},
             \qquad \sum_jm_j=k+8                       \tag{2}
\]

be the polynomial formed by all complementary labels, including the
fixed excess in a chosen class of multiplicity greater than two.  Thus
\(c\) is the number of distinct roots of this complementary polynomial.

**Theorem 1.1.**  Vanishing of every isolated-star pivot produces an
injective two-dimensional relation space

\[
                         {\cal S}_T\subset
                         \mathbb C[z]_{\le c-4}.          \tag{3}
\]

At every simple root of \(A\), the Wronskian of this pencil vanishes.
Consequently the profile is impossible whenever

\[
 c<5\qquad\hbox{or}\qquad
 \#\{j:m_j=1\}>2c-10.                                   \tag{4}
\]

The striking point is that both the degree in (3) and the obstruction
(4) are independent of \(k\).  Increasing the common-pole order adds one
degree to both the distinguished denominator and the complementary
polynomial, and the two changes cancel exactly.

## 2. The common sextic kernel

Let \(T\) be the five formal layers and put

\[
                         Q_T(z)=\prod_{t\in T}(z+t).      \tag{5}
\]

For a pair \(\{x,y\}\subset T\), select one label at \(x,y\) and two
at the other three layers.  The five represented classes give a nonzero
residual \(q_{x,y}\in\mathbb C[z]_{\le2}\).  Factoring any fixed excess
\((z-t)^{\lambda_t-2}\) into \(A\), the identity

\[
 {z-t\over(z+t)^2}={z^2-t^2\over(z+t)^3}                 \tag{6}
\]

places all ten lifts

\[
                         P_{x,y}=(z^2-x^2)(z^2-y^2)q_{x,y} \tag{7}
\]

in \(\mathbb C[z]_{\le6}\).  Their rational functions are

\[
 F_P(z)={A(z)P(z)\over(z+\mu)^{k+1}Q_T(z)^3}.            \tag{8}
\]

The numerator and denominator degrees are \(k+14\) and \(k+16\), so
\(F_P=O(z^{-2})\) for every \(k\).

Let \(K_T\) be the kernel of the five exact order-two residue rows at
the selected value poles and let \(W_T\) be the span of (7).  Then

\[
                         W_T=K_T,\qquad\dim K_T=4.        \tag{9}
\]

Indeed, for a hypothetical \(d\ge5\) dimensional kernel with unit gcd,
the five order-two rows force Wronskian weight \(5(d-2)\), while the
degree-six cap is \(d(7-d)\).  Their difference

\[
                         d^2-2d-10                       \tag{10}
\]

is already positive at \(d=5\).  More explicitly, if the polynomial gcd
has order one at \(r\) of the five nodes and order at least three at
\(s\) others, the least possible corrected deficit is

\[
 d^2-2d-10+r(d+1)+s(2d+2)>0.
\]

Gcd order two would leave an exact value equation after removal of the
gcd and is impossible.  Thus \(\dim K_T\le4\), using only the five value
rows and no common-pole row.  The ten pair divisibilities in (7) give
\(\dim W_T\ge3\).  If
equality held, the five-plane intersection and parity-minor argument would
give \(W_T=G(z){\cal E}(z^2)\) with \(\dim{\cal E}=3\) and
\(\deg G\le2\); an exact order-two row cannot kill that whole even
three-space at five distinct squared nodes.  Hence (9).  This is precisely
the kernel lemma proved in the third-order formal-five note, and its proof
contains no occurrence of \(k\).

## 3. Dual degree cancellation at every order

The five rows on the seven-dimensional sextic space have rank three, so
they have two relations.  The principal parts of a relation have the form

\[
                         H_c(z)={N_c(z)\over Q_T(z)^3},
                         \qquad\deg N_c\le7.             \tag{11}
\]

Distinct pole supports make \(c\mapsto N_c\) injective.  Divide by the
cofactor in (8):

\[
                         G_N(z)={(z+\mu)^{k+1}N(z)\over A(z)}. \tag{12}
\]

Write

\[
 g=\prod_j(z-y_j)^{m_j-1},\qquad R_A=A/g,\qquad D_A=A'/g. \tag{13}
\]

Then \(\deg R_A=c\), \(\deg D_A=c-1\), and the leading coefficient of
\(D_A\) is \(\deg A=k+8\).  Direct differentiation gives

\[
 G_N'={(z+\mu)^kg\over A^2}\,{\cal E}_{A,k}(N),          \tag{14}
\]

where

\[
 {\cal E}_{A,k}(N)=
 R_A\bigl((z+\mu)N'+(k+1)N\bigr)-(z+\mu)D_AN.            \tag{15}
\]

For \(n=\deg N\le7\), its nominal leading coefficient is

\[
                         n+(k+1)-(k+8)=n-7.              \tag{16}
\]

It vanishes at \(n=7\); for \(n\le6\) the nominal degree is already at
most \(c+6\).  Contact of order three at all five selected poles gives

\[
                         {\cal E}_{A,k}(N)=Q_T^2S_N,
                         \qquad\deg S_N\le c-4.          \tag{17}
\]

The map \(N\mapsto S_N\) is injective.  A zero image makes \(G_N\)
constant, hence

\[
                         (z+\mu)^{k+1}N=\gamma A;         \tag{18}
\]

evaluation at \(-\mu\), where \(A(-\mu)\ne0\), forces
\(\gamma=N=0\).  This proves (3).

At a simple root \(r\) of \(A\), equation (14) has a double pole.  Its
zero residue is one common Robin row on \({\cal S}_T\), so the nonzero
Wronskian of a basis has \(r\) as a root.  Its degree is at most
\(2(c-4)-2=2c-10\), proving (4).

## 4. The first fourth-order increment

At \((h,k)=(8,4)\), the frozen H/S/C/L/Q census has 46 residual profiles.
Theorem 1.1 immediately closes the following six:

\[
\begin{gathered}
 4\,3^6,\qquad 3^4 2^5,\qquad 3^5 2^3 1,\\
 3^3 2^6 1,\qquad 3^4 2^4 1^2,\qquad
 3^3 2^5 1^3.                                           \tag{19}
\end{gathered}
\]

For \(4\,3^6\), choose five triple layers.  The complementary polynomial
has \(c=7\) roots, five simple, and \(5>2c-10=4\).  For
\(3^4 2^5\), choose the five doubles; the four complementary triple roots
give \(c=4\).  For \(3^5 2^3 1\), choose all three doubles and two
triples, giving \((c,s_{\rm simple})=(6,3)\).  The last three profiles
give respectively \((5,1),(6,3),(6,3)\).  For each of these six fixed
choices, all ten ways to lower two of the five formal layers are legal:
either a singleton remains outside, or a partial exact double or a full
exact triple leaves a singleton mate.

## 5. Exact audit

[verify_live_three_zero_eighth_split_all_order_formal_five_layer_duality.py](../computations/verify_live_three_zero_eighth_split_all_order_formal_five_layer_duality.py)
checks the all-\(k\) degrees and leading cancellation, the sextic kernel
bound, every formal lift and legality condition, the simple-root
Wronskian criterion, and the six fourth-order profiles in (19).
