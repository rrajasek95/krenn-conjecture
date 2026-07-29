# Higher splits: the \(p=18\) two-triple eight-double common-lift closure

## 1. Result

On the no-extra-singular live-three-zero stratum, let

\[
                         h+k=18,\qquad13\leq h\leq17.             \tag{1}
\]

The last two-triple equality family is impossible:

\[
                \boxed{\qquad3^2 2^8 1^{h-2}
                                  \text{ is impossible}.\qquad}  \tag{2}
\]

For every selected pair of double values, the complementary profile is
\(3^2 2^6\), whose exact relation multipliers form a three-space in
\(\mathbb C[z]_{\leq4}\).  Fix one member \(i\) of the selected pair.
Multiplying by the quintic exchange factor belonging to the other member
puts all seven pair spaces into one degree-nine kernel.  Any two of the
lifted three-spaces are disjoint, so this kernel has dimension at least
six.  Its seven exact second-order residue rows force dimension at most
five.

This uses the rank-two endpoint system retained in the
[endpoint audit](live-three-zero-higher-split-p18-two-triple-endpoint-frontier.md),
but it does not require elimination of its minors or the neighboring
selected-triple quintics.

## 2. The twenty-eight endpoint relation spaces

Let \(D\) be the eight-element set of double values, let
\(X=\{x_1,x_2\}\) be the triple set, and let \(H\) be the product of the
original singleton plus-pole factors.  Repeated values are nonzero, and
distinct exceptional values are neither equal nor opposite.
Standing structural admissibility also gives \(v+\mu\ne0\) at every
exceptional value used below.  Thus each displayed regular factor is a
genuine unit at its named evaluation point; none of the logarithmic
derivatives below divides by a possibly vanishing factor.

For every pair \(Q=\{i,j\}\subset D\), select the two double layers and
all singleton layers.  The complement is

\[
                              3^2 2^6.                            \tag{3}
\]

Simultaneous equality supplies a three-dimensional relation space

\[
                    {\cal S}_{i,j}\subseteq
                              \mathbb C[z]_{\leq4}.               \tag{4}
\]

For \(v\in D\setminus\{i,j\}\), remove the pole \((z-v)^{-3}\)
from the exact rational derivative and call its regular factor
\(U_{v,\{i,j\}}\).  Every \(S\in{\cal S}_{i,j}\) satisfies

\[
       J_{v,\{i,j\}}S=0,
       \qquad
       J_{v,Q}=D_v^2+2\alpha_{v,Q}D_v+\delta_{v,Q}E_v,            \tag{5}
\]

where \(\alpha=U'/U\) and \(\delta=U''/U\) at \(v\).  The coefficient
of \(D_v^2\) is one, including every special logarithmic-slope chart.

## 3. Fix one selected value and lift the other

Fix \(i\in D\).  Although selecting only \(i\) is not one of the
saturated endpoint selections, its regular units are perfectly
well-defined.  For \(v\ne i\), put

\[
 U_{v,\{i\}}(z)=
 { (z+\mu)^k(z+i)^2H(z)
  \over
   (z-x_1)^4(z-x_2)^4
   \displaystyle\prod_{w\in D\setminus\{i,v\}}(z-w)^3},         \tag{6}
\]

and let \(J_{v,\{i\}}\) be its normalized second-order row as in
(5).  Define

\[
                 {\cal K}_i=
     \bigcap_{v\in D\setminus\{i\}}\ker J_{v,\{i\}}
                    \subseteq\mathbb C[z]_{\leq9}.               \tag{7}
\]

For \(j\ne i\), set

\[
                         g_j(z)=(z-j)^3(z+j)^2.                   \tag{8}
\]

At every \(v\notin\{i,j\}\), the exact regular units obey

\[
                         U_{v,\{i,j\}}=g_jU_{v,\{i\}}.           \tag{9}
\]

The product rule therefore gives, without division by a relation
multiplier,

\[
        J_{v,\{i\}}(g_jS)=g_j(v)J_{v,\{i,j\}}S=0.               \tag{10}
\]

At \(v=j\), the factor \((z-j)^3\) kills the value, first derivative,
and second derivative of \(g_jS\), so (10) remains true with the right
side interpreted as zero.  Consequently

\[
             {\cal T}_{i,j}:=g_j{\cal S}_{i,j}
                         \subseteq{\cal K}_i,
             \qquad\dim{\cal T}_{i,j}=3.                         \tag{11}
\]

All polynomials in (11) have degree at most nine.

## 4. Two lifted spaces force dimension six

Choose distinct \(j,k\in D\setminus\{i\}\).  The two quintics \(g_j\)
and \(g_k\) are coprime: their roots are \(\{j,-j\}\) and
\(\{k,-k\}\), and structural distinctness and nonopposition make these
sets disjoint.  If a nonzero polynomial belonged to both
\({\cal T}_{i,j}\) and \({\cal T}_{i,k}\), it would be divisible by
\(g_jg_k\), of degree ten, while having degree at most nine.  Hence

\[
                  {\cal T}_{i,j}\cap{\cal T}_{i,k}=0.            \tag{12}
\]

Equations (11)--(12) imply

\[
                              \dim{\cal K}_i\geq6.                \tag{13}
\]

Only two of the seven partners are needed for this lower bound.

## 5. Seven second-order rows force dimension at most five

Let \(d=\dim{\cal K}_i\).  At each of the seven values
\(v\in D\setminus\{i\}\), equation (7) puts the order-two jet image of
\({\cal K}_i\) in the kernel of one functional whose \(D_v^2\)
coefficient is nonzero.  The jet image therefore has rank at most two.
If \(\nu_0<\cdots<\nu_{d-1}\) is the local vanishing sequence, at most
two entries can be smaller than three.  The least possible sequence is

\[
                         (0,1,3,4,\ldots,d),                     \tag{14}
\]

so each value contributes Wronskian weight at least \(d-2\).  This
argument already includes every possible polynomial gcd; a common zero
only increases the vanishing sequence.

The seven double values are distinct.  A \(d\)-space in
\(\mathbb C[z]_{\leq9}\) has Wronskian degree at most \(d(10-d)\), and
hence

\[
                             7(d-2)\leq d(10-d).                  \tag{15}
\]

For \(d=6\), the two sides are \(28\) and \(24\), and the deficit

\[
                    7(d-2)-d(10-d)=d^2-3d-14                    \tag{16}
\]

is strictly increasing for \(d\geq6\).  Thus

\[
                              \dim{\cal K}_i\leq5,                \tag{17}
\]

contradicting (13).  This proves (2).

## 6. Exact audit and ledger consequence

[verify_live_three_zero_higher_split_p18_two_triple_eight_double_common_lift_closure.py](../computations/verify_live_three_zero_higher_split_p18_two_triple_eight_double_common_lift_closure.py)
checks all twenty-eight selected-pair complements, the exact quintic
unit transport, coprimality and the direct-sum lower bound, every local
vanishing sequence, and the degree-nine Wronskian inequality.

Together with the three cofactor theorems, this closes every two-triple
family \(3^2 2^b1^{h+14-2b}\), \(0\leq b\leq8\).  Hence twenty-nine of
the original fifty \(p=18\) equality families are closed, and the
twenty-one remaining families have at most one triple value.
