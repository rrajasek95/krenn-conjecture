# Higher splits: the \(p=18\) two-triple six-simple/three-double cofactor closure

## 1. Result

On the no-extra-singular live-three-zero stratum, let

\[
                    p=h+k=18,\qquad13\leq h\leq17.               \tag{1}
\]

The middle packet of the two-triple block is impossible:

\[
 \boxed{\qquad
       3^2 2^b1^{h+14-2b}\text{ is impossible for }b=3,4,5.
 \qquad}                                                         \tag{2}
\]

Select \(b-3\) doubles in role two and enough singletons to leave the
common complement

\[
                              3^2 2^3 1^6.                        \tag{3}
\]

Its relation three-space lies in \(\mathbb C[z]_{\leq7}\).  The proof is
the mixed-jet counterpart of the
[twelve-simple cofactor closure](live-three-zero-higher-split-p18-two-triple-twelve-simple-cofactor-closure.md).
Four fixed simple rows and the two normalized jets at each of the three
double values have total effective weight ten.  They produce a six-space
in degree fourteen whose evaluation-hyperplane cofactor again reduces to
bidegree \((5,9)\).

## 2. Mixed principal parts

Let \(X=\{x_1,x_2\}\) be the two triple values.  Let \(D\) be the full
double set, choose the selected set \(Q\subset D\), \(|Q|=b-3\), and put

\[
                   B=D\setminus Q,\qquad |B|=3,\qquad
                   V(z)=\prod_{v\in B}(z-v).                    \tag{4}
\]

Let \(Y\) be the singleton set, so

\[
                         |Y|=h+14-2b.                             \tag{5}
\]

For a six-element complementary singleton set \(C\subset Y\), the
saturated relation space is

\[
                    {\cal S}_C\subseteq\mathbb C[z]_{\leq7}.     \tag{6}
\]

Its annihilator has dimension five.  At a simple value \(a\in C\), the
exact row has pole order two; at a double value \(v\in B\), the exact row
is

\[
             D_v^2+2\alpha_vD_v+\delta_vE_v,                    \tag{7}
\]

with pole order three in the principal-part model.

Fix \(A\subset C\), and take relations among the rows indexed by
\(A\cup B\).  Their common rational denominator is

\[
                         J_A(z)^2V(z)^3,
             \qquad J_A(z)=\prod_{a\in A}(z-a).                 \tag{8}
\]

If \(N\) is a relation numerator, annihilation of
\(\mathbb C[z]_{\leq7}\) gives

\[
                         \deg N\leq2|A|+9-9=2|A|.                \tag{9}
\]

At a simple pole, matching the two principal coefficients gives one
linear first-jet condition on \(N\).  At a double pole, write

\[
 {N(z)\over J_A(z)^2V(z)^3}={F_v(z)\over(z-v)^3}.
\]

Matching the three coefficients in (7) gives

\[
                     F_v'(v)=\alpha_vF_v(v),\qquad
                     F_v''(v)=\delta_vF_v(v).                   \tag{10}
\]

Thus every fixed simple row contributes one normalized condition and
every fixed double row contributes two.

If \(C=A\sqcup T\), multiply the numerator by

\[
                         \prod_{s\in T}f_s(z),\qquad
                         f_s(z)=(z-s)^2(z+s).                    \tag{11}
\]

The product rule and the exact local units cancel all dependence on
\(T\) in both (10) and the simple-root equations.  This defines a fixed
space

\[
                 {\cal K}_{A,B}\subseteq
                       \mathbb C[z]_{\leq18-|A|},                \tag{12}
\]

cut out by \(|A|+2|B|=|A|+6\) normalized jet equations.

For \(|A|=5\), the eight actual rows \(A\cup B\) have at least three
relations and (9)--(11) give

\[
 \dim\bigl({\cal K}_{A,B}\cap
       f_s\mathbb C[z]_{\leq10}\bigr)\geq3,qquad
                 {\cal K}_{A,B}\subseteq\mathbb C[z]_{\leq13}. \tag{13}
\]

For \(|A|=4\), the seven actual rows have at least two relations and

\[
 \dim\bigl({\cal K}_{A,B}\cap
       f_sf_t\mathbb C[z]_{\leq8}\bigr)\geq2,qquad
                 {\cal K}_{A,B}\subseteq\mathbb C[z]_{\leq14}. \tag{14}
\]

## 3. Dimension forcing

Suppose a \(d\)-space of polynomials satisfies one common normalized
simple row.  Its Wronskian weight there is at least \(d-1\).  If its
three-jet image at a double value has rank at most one, a local gauge
gives vanishing sequence

\[
                         (0,3,4,\ldots,d+1),                     \tag{15}
\]

so the double contributes at least \(2(d-1)\).  Consequently the five
simple and three double anchors in (13) have total weight

\[
                         (5+2\cdot3)(d-1)=11(d-1).               \tag{16}
\]

Exactly as in the eleven-simple argument, (16), (13), and the degree
bound \(d(14-d)\) exclude every dimension except five:

- dimensions at least six violate the anchor Wronskian bound;
- in dimension three, five coprime moving cubic factors exceed degree
  thirteen;
- in dimension four, the fixed weights plus three moving weights give
  \(11\cdot3+3\cdot3=42>40\).

Thus

\[
                         \boxed{\dim{\cal K}_{A,B}=5}
                   \qquad(|A|=5).                               \tag{17}
\]

Now fix four nonzero singleton anchors \(A\), and put \(Z=Y\setminus A\).
The ten normalized conditions in (12) give dimension at least five, and
their Wronskian weights exclude dimensions at least seven.  For
\(s\in Z\), multiplication by \(z+s\) transports every first- and
second-jet equation, giving

\[
                 (z+s){\cal K}_{A\cup\{s\},B}
                              \subseteq{\cal K}_{A,B}.            \tag{18}
\]

If the right side had dimension five, equality for every \(s\in Z\)
would make all its members divisible by \(\prod_{s\in Z}(z+s)\).  In the
smallest case \(|Z|\geq13\), such degree-at-most-fourteen multiples form
at most a two-space.  Therefore

\[
                         \boxed{\dim{\cal K}_{A,B}=6}
                   \qquad(|A|=4).                               \tag{19}
\]

The six-space Wronskian already has fixed weight

\[
                         4\cdot5+3\cdot10=50.                    \tag{20}
\]

Hence it cannot have a common root away from \(A\cup B\), since a common
factor would contribute six more units beyond the degree cap \(54\).
For every \(s\in Z\), evaluation at \(-s\) is therefore nonzero, and

\[
 H_s:=\{P\in{\cal K}_{A,B}:P(-s)=0\}
                   =(z+s){\cal K}_{A\cup\{s\},B}.                \tag{21}
\]

## 4. The mixed cofactor

Choose a basis \(p_0,\ldots,p_5\) of the six-space in (19), and define

\[
 \Phi(z,t)=\det\begin{pmatrix}
 p_0(t)&\cdots&p_5(t)\\
 p_0(z)&\cdots&p_5(z)\\
 p_0'(z)&\cdots&p_5'(z)\\
 \vdots&&\vdots\\
 p_0^{(4)}(z)&\cdots&p_5^{(4)}(z)
 \end{pmatrix}.                                                  \tag{22}
\]

The evaluation hyperplane inherits four simple rows, of Wronskian weight
four each, and three double two-jet systems, of weight eight each.
Taylor expansion supplies the automatic diagonal factor.  Hence

\[
 \Psi(z,t)={\Phi(z,t)
       \over J_A(z)^4V(z)^8(t-z)^5}                              \tag{23}
\]

is a polynomial.  The removed fixed factor has degree
\(4\cdot4+3\cdot8=40\).  Therefore, exactly as before,

\[
                         \deg_z\Psi\leq5,\qquad
                         \deg_t\Psi\leq9.                        \tag{24}
\]

For \(s\in Z\), (21) and the additional simple row at \(s\) give

\[
                         (z-s)^4\mid\Psi(z,-s).                  \tag{25}
\]

Put \(\Theta(z,s)=\Psi(z,-s)\) and

\[
                  G_j(s)=\left.\partial_z^j\Theta(z,s)\right|_{z=s},
                  \qquad0\leq j\leq3.                           \tag{26}
\]

Then

\[
                              \deg G_j\leq14-j.                  \tag{27}
\]

For \(b=3\), \(|Z|=h+4\geq17\), and for \(b=4\),
\(|Z|=h+2\geq15\).  Thus all four polynomials in (26) vanish
identically.  The last family needs the same two-point correction as the
twelve-simple packet.

## 5. Complementary-double correction for \(b=5\)

Let the two selected doubles be \(q_1,q_2\), so

\[
                         D=B\sqcup\{q_1,q_2\}.                   \tag{28}
\]

Select only \(q_2\), leave \(q_1\) complementary, and leave the four
singleton anchors \(A\) complementary.  The neighboring complement is

\[
                              3^2 2^4 1^4,                       \tag{29}
\]

whose relation space lies in \(\mathbb C[z]_{\leq6}\) and has
four-dimensional annihilator.  Take relations among the same seven fixed
rows \(A\cup B\), omitting the new double row at \(q_1\).  There are at
least three relations.  Their denominator still has degree seventeen, so
their numerators have degree at most

\[
                              17-(6+2)=9.                         \tag{30}
\]

At every fixed simple or double node, multiplication by

\[
                         g_{q_1}(z)=(z-q_1)^3(z+q_1)^2           \tag{31}
\]

removes the complementary negative-pole cube and inserts the selected
plus-pole square, transporting both normalized double jets by the product
rule.  Thus \({\cal K}_{A,B}\) contains three independent degree-at-most
fourteen members divisible by \(g_{q_1}\).  Interchanging \(q_1,q_2\)
gives the companion three-space for \(q_2\).

After the common factor \(z+q_i\) is removed from the evaluation
hyperplane at \(-q_i\), three independent members vanish to order at
least three at \(q_i\).  Their Wronskian weight is at least three, so

\[
                         (z-q_i)^3\mid\Theta(z,q_i),
                         \qquad i=1,2.                           \tag{32}
\]

For \(b=5\), \(|Z|=h\).  The singleton roots and the two distinct double
roots give exactly the interpolation counts

\[
\begin{array}{c|c|c}
j&\text{roots available}&\deg G_j\\ \hline
0&h+2\geq15&\leq14\\
1&h+2\geq15&\leq13\\
2&h\geq13&\leq12\\
3&h\geq13&\leq11.
\end{array}                                                       \tag{33}
\]

Thus \(G_0=G_1=G_2=G_3=0\) for \(b=5\) as well.

## 6. Diagonal contradiction

The four identities imply

\[
                         \Psi(z,t)=(z+t)^4L(z,t),\qquad
                         \deg_zL\leq1,\quad\deg_tL\leq5.         \tag{34}
\]

The exact cofactor diagonal is

\[
 \Psi(z,z)=-{1\over120}
       {\operatorname {Wr}({\cal K}_{A,B})(z)
        \over J_A(z)^4V(z)^8}.                                  \tag{35}
\]

The six-space satisfies four simple rows and two independent normalized
jet equations at each of the three doubles.  Hence

\[
          J_A(z)^5V(z)^{10}mid
                        \operatorname {Wr}({\cal K}_{A,B})(z).   \tag{36}
\]

Equations (34)--(36) imply

\[
                         J_A(z)V(z)^2\mid z^4L(z,z).              \tag{37}
\]

The four chosen singleton anchors and all repeated values are nonzero, so
the degree-ten polynomial \(J_AV^2\) is coprime to \(z\).  But
\(\deg L(z,z)\leq6\).  Thus (37) forces \(L(z,z)=0\), and (35) makes the
Wronskian of a six-dimensional polynomial space vanish identically.  This
contradiction proves (2).

## 7. Exact audit

[verify_live_three_zero_higher_split_p18_two_triple_six_simple_three_double_cofactor_closure.py](../computations/verify_live_three_zero_higher_split_p18_two_triple_six_simple_three_double_cofactor_closure.py)
checks the common selections, mixed denominator and numerator degrees,
first- and second-jet normalization, dimension inequalities, cofactor
bidegree, complementary-double correction, interpolation counts, and the
degree-ten diagonal divisor.
