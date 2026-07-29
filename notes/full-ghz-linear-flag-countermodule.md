# Full GHZ equations do not make a linear flag average select a cut

## 1. Outcome

Imposing every mixed coefficient of the final GHZ tensor still does not
make any **linear** average of matching sectors select a good five-cut.  At
order eight there is an exact rational countermodule with one tensor `Z_M`
for each of the 105 perfect matchings such that

\[
                         \sum_M Z_M=\Delta_{8,3},          \tag{1}
\]

and, simultaneously for all 56 five-sets `U`,

\[
                         T_1^U+T_3^U=\Delta_{8,3},         \tag{2}
\]

but

\[
             \ker F_1^U\not\subseteq\ker\delta_U         \tag{3}
\]

with the full three-row defect on every cut.  Here

\[
 T_j^U=\sum_{M:\,|M\cap\delta(U)|=j}Z_M                 \tag{4}
\]

and `F_1^U` is the `U`-flattening of `T_1^U`.

The countermodule retains all full-output equations, all crossing-sector
overlap relations, and every fixed or weighted linear incidence average.
It deliberately forgets only the common-edge product condition

\[
                         Z_M=\bigotimes_{e\in M}A_e.       \tag{5}
\]

Therefore no proof using just linear combinations of the GHZ coefficient
equations and cut-sector incidence can force a good cut.  A successful
argument must use (5), or another nonlinear consequence of the shared edge
family.

There is a complementary obstruction for nonlinear product caps.  Two
genuine complete rational scalar `K_8` sources have the identical full
matching tensor `H_8=1` and nonzero scalar on every pair, but their sums of
the 28 top pair-cap corrections are respectively

\[
                         -80,
              \qquad -{2118320\over27783}.                \tag{6}
\]

Thus even the total nonlinear correction is not determined by the output
tensor.  This scalar comparison does not rule out a specifically ternary,
colour-sensitive nonlinear identity; it shows that such an identity must
use more than the final tensor and matching incidence.

The exact audit is
[`verify_full_ghz_linear_flag_countermodule.py`](../computations/verify_full_ghz_linear_flag_countermodule.py).

## 2. The maximal linear matching-term relaxation

Let `mathcal P` be the set of perfect matchings of `B`.  In an actual
aggregate source, matching `M` contributes the tensor

\[
                         Z_M(A)=\bigotimes_{e\in M}A_e.    \tag{7}
\]

The **formal matching-term relaxation** allows the tensors `Z_M` to be
arbitrary and independent.  It keeps the output and every crossing sector:

\[
 H^{\rm form}=\sum_{M\in\mathcal P}Z_M,
 \qquad
 T_j^U=\sum_{M\in\mathcal P}
     {f1}_{\{|M\cap\delta(U)|=j\}}Z_M.                 \tag{8}
\]

Only the nonlinear compatibility (7) is discarded.

This relaxation is universal for linear averaging.  Let `lambda_(U,j)` be
arbitrary scalar weights.  Directly from (8),

\[
 \sum_{U,j}\lambda_{U,j}T_j^U
   =\sum_M c_MZ_M,
 \qquad
 c_M=\sum_{U,j}\lambda_{U,j}
             {f1}_{\{|M\cap\delta(U)|=j\}}.            \tag{9}
\]

In particular, the weighted average is universally equal to
`kappa H^form` precisely when

\[
                              c_M=\kappa
                              \quad\text{for every }M.    \tag{10}
\]

Every universally valid fixed-weight flag identity is therefore valid in
the formal relaxation.  If (1) holds, (9)--(10) turn its right side into
`kappa Delta_(8,3)`, with every mixed coefficient zero.  More generally,
any tensorial identity obtained linearly from (1), (8), and incidence is
automatically respected.

This proves the relevant no-go statement independently of the particular
countermodule below:

**Linear-averaging no-go lemma.**  If a formal matching-term assignment
satisfies (1) and fails (3) on every five-set, then no linear combination
of the full GHZ coefficient equations and universal matching-incidence
identities can prove that some five-set satisfies the kernel inclusion.

Indeed, the assignment is a simultaneous model of all the premises and of
the negation of every proposed conclusion.

## 3. Exact incidence algebra at eight sites

It is convenient to index a five-cut by its three-site complement `C`.
Let `A` be the `56 by 105` matrix

\[
 A_{C,M}={\bf1}_{\{|M\cap\delta(C)|=1\}}.                \tag{11}
\]

A three-set has one crossing edge exactly when it contains one whole edge
of `M`.  Hence

\[
 A_{C,M}=\sum_{e\subset C}{\bf1}_{\{e\in M\}}.           \tag{12}
\]

Writing `P` for edge-versus-matching incidence and `Q` for
triple-versus-contained-edge incidence gives the exact factorization

\[
                              A=QP.                       \tag{13}
\]

The span of perfect-matching incidence vectors in `Q^28` is the space of
edge weights having equal weighted degree at all eight vertices.  It has
dimension `28-7=21`.  One inclusion is immediate because every perfect
matching has degree one at every vertex.  For the reverse inclusion,
differences of perfect matchings contain the elementary alternating
four-cycle vectors; these span the zero-degree kernel of the unsigned
vertex-edge incidence matrix, of dimension 20, and adjoining one perfect
matching gives dimension 21.

The map `Q` is injective.  If edge weights `a_e` have zero sum on every
triangle, then for four distinct vertices

\[
 (a_{ij}+a_{ik}+a_{jk})+(a_{ij}+a_{i\ell}+a_{j\ell})
 -(a_{ik}+a_{i\ell}+a_{k\ell})
 -(a_{jk}+a_{j\ell}+a_{k\ell})
               =2(a_{ij}-a_{k\ell})=0.                  \tag{14}
\]

All disjoint edge weights agree; the disjointness graph on the edges of
`K_8` is connected, so all edge weights are one constant, and a triangle
sum makes that constant zero.  Therefore

\[
                         \operatorname{rank}A=21.         \tag{15}
\]

Every column of `A` sums to 24, recovering

\[
                         \sum_{|U|=5}T_1^U=24H^{\rm form}.\tag{16}
\]

Every row sums to 45.  At order eight the only odd crossing counts for a
three-versus-five cut are one and three, giving (2) whenever (1) holds.
Thus the countermodule below satisfies not only the average (16), but the
complete sector decomposition on every individual cut.

## 4. A simultaneous full-GHZ countermodule

Order the 105 perfect matchings lexicographically as `M_0,...,M_104` and
encode a ternary word `w=(w_0,...,w_7)` by

\[
                         d(w)=\sum_{i=0}^7w_i3^{7-i}.      \tag{17}
\]

The checker uses a fixed integer mixing map

\[
\begin{aligned}
 h(x)&=x+\mathtt{9E3779B97F4A7C15},\\
 h(x)&=(h(x)\mathbin{\mathtt{xor}}(h(x)\!\gg\!30))
                    \mathtt{BF58476D1CE4E5B9},\\
 h(x)&=(h(x)\mathbin{\mathtt{xor}}(h(x)\!\gg\!27))
                    \mathtt{94D049BB133111EB},\\
 h(x)&=h(x)\mathbin{\mathtt{xor}}(h(x)\!\gg\!31),
\end{aligned}                                             \tag{18}
\]

with every operation reduced modulo `2^64`.  Take the 120 nonconstant
words having the smallest values of

\[
                    h(d(w)+14\cdot\mathtt{123456789ABCDEF}).\tag{19}
\]

For each selected word and `0<=i<104`, put

\[
 z_{i,w}=h(14\cdot1000003+1009d(w)+9176i)\bmod7-3,
 \qquad
 z_{104,w}=-\sum_{i=0}^{103}z_{i,w}.                     \tag{20}
\]

For unselected mixed words put `z_(i,w)=0`, and define

\[
 Z_{M_i}={1\over105}
       \left(\Delta_{8,3}+\sum_w z_{i,w}e_w\right).       \tag{21}
\]

Equation (20) makes every mixed coefficient sum to zero, while the 105
constant contributions in (21) sum to one.  Thus (1) holds coefficient by
coefficient over `Q`; this is not a modular construction.

For each cut, form `F_1^U` from (4) and append the three rows of
`delta_U`.  Exact rational row reduction gives

\[
\begin{array}{c|c|c}
\operatorname{rank}F_1^U&
\operatorname{rank}\binom{F_1^U}{\delta_U}
        -\operatorname{rank}F_1^U&\#\text{ cuts}\\\hline
27&3&46\\
26&3&8\\
25&3&2.
\end{array}                                               \tag{22}
\]

The common denominator 105 is cleared before row reduction and cannot
affect any rank.  The second column is three for every cut, proving (3)
simultaneously.  In particular, even the entire target three-row space is
independent modulo the one-crossing row space on every cut.

This is an exact falsifier to every linear selection argument in the sense
of the no-go lemma.  It is not an aggregate matching source: no matrices
`A_e` satisfying (5) are asserted.  Its purpose is to prove that common-edge
factorization is essential, rather than merely convenient.

## 5. The nonlinear cap sum is not output-determined

The cumulant correction is outside the formal linear relaxation because it
uses powers of the induced edge response.  Even so, its sum cannot be
recovered from the final matching tensor alone.  This already fails for
one-dimensional vertex spaces.

For scalar edge weights `a_e` on `K_8`, write

\[
 h(a)=\sum_{M\in\operatorname{PM}(8)}\prod_{e\in M}a_e.  \tag{23}
\]

For a deleted pair `p,q`, put `s=a_pq` and, on the other six vertices,

\[
 J_{uv}=a_{up}a_{vq}+a_{uq}a_{vp},\qquad
 R_{uv}=a_{uv}+{J_{uv}\over s}.                           \tag{24}
\]

The scalar specialization of the exact top correction is

\[
                         E_{pq}=h(a)-s\,h(R).             \tag{25}
\]

Consider the following two complete rational systems.

1. Start with `a_e=1` on every edge.
2. On the canonical matching `01|23|45|67`, put weights
   `-63,1,1,1`, respectively, and put `-1` on every other edge.

Finally, in each system divide all seven edges incident to vertex zero by
105.  Every matching uses exactly one such edge.  The first unnormalized
hafnian is 105.  In the second system the 105 matching products have value
census

\[
\begin{array}{c|rrrr}
\text{value}&1&-1&63&-63\\\hline
\text{multiplicity}&66&24&8&7,
\end{array}
\]

whose sum is also 105.  Hence both normalized systems satisfy exactly

\[
                              h(a)=1,                     \tag{26}
\]

and every pair scalar `s` is nonzero.

For the first system, (24)--(25) give

\[
                       E_{pq}=-{20\over7}
                       \quad\text{for all 28 pairs},      \tag{27}
\]

so their sum is `-80`.  For the second system, exact enumeration gives

\[
              \sum_{p<q}E_{pq}=-{2118320\over27783},      \tag{28}
\]

and every one of its 28 corrections is nonzero.  Equations (26)--(28)
prove that neither the individual corrections nor their unweighted sum are
functions of the full output tensor.

## 6. Consequence for the uniform reduction

The full GHZ mixed equations annihilate the sum of the formal matching
terms, but a linear cut average only changes the incidence coefficient with
which each term is counted.  The countermodule shows that those two facts
are compatible with maximal failure on every cut.  Meanwhile the scalar
pair shows that passing to nonlinear cumulants introduces information not
recoverable from the output tensor.

Thus a viable all-even reduction must couple the mixed GHZ equations to the
shared edge factors in (5).  Pure sector averaging, even simultaneously
over every five- and six-cut and with arbitrary universal weights, cannot
do so.

Run the audit with

```sh
python computations/verify_full_ghz_linear_flag_countermodule.py
```
