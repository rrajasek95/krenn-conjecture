# Higher splits: a dense-double common-lift closure at (p=19)

## 1. Uniform statement

Suppose a collision profile admits the following family of formal
selections.  There is a set ({\mathscr D}) of (b\) exact double value
classes; the same fixed singleton layers are selected each time; and every
pair ({i,j}\subset{\mathscr D}) can be selected in role two.  Assume
that every resulting selected-row kernel is five-dimensional.  Its formal
complement has (c) value classes and six-capped mass

\[
                         M_6=\sum_{r=1}^c\min(m_r,6).           \tag{1}
\]

**Theorem 1.1 (dense-double common lift).**  If (M_6\leq27), then the
configuration is impossible in either of the following ranges:

\[
 \boxed{
 \begin{array}{c|c}
 c+1\leq9&b\geq3,\\
 c+1=10&b\geq6.
 \end{array}}                                                  \tag{2}
\]

This theorem is uniform in the multiplicities and values of every fixed
complementary class.  The first line is a pure coprime-degree obstruction;
the second is the sharp equality case and uses only exact second-order
rows at the double values.

At (p=19), condition (1) is automatic with (M_6=19).  The theorem
closes fourteen boundary families, seven of each symbolic type:

\[
\boxed{
\begin{array}{c|l}
3^a2^b1^{h+21-3a-2b}
 &(a,b)=(1,10),(2,8),(3,6),(3,7),(4,5),(5,3),(5,4),\\
4\,3^a2^b1^{h+17-3a-2b}
 &(a,b)=(0,9),(1,7),(1,8),(2,6),(3,4),(3,5),(4,3).
\end{array}}                                                  \tag{3}
\]

These fourteen are disjoint from the fifty-seven families closed by the
[singleton-parity common-lift theorem](live-three-zero-higher-split-p19-singleton-parity-common-lift-closure.md).
Thus the two new routes close seventy-one of the ninety-four (p=19)
boundary families.

## 2. Put every moving partner in one kernel

For a selected pair ({i,j}\subset{\mathscr D}), let

\[
                  {\cal S}_{i,j}\subseteq
                         \mathbb C[z]_{\leq c-4},
                  \qquad \dim{\cal S}_{i,j}=3                 \tag{4}
\]

be its exact relation space.  Fix (i).  Retain (i) and all fixed
selected singleton layers in the baseline normalization, but allow the
second selected double to move.  Put

\[
                         g_j(z)=(z-j)^3(z+j)^2.                 \tag{5}
\]

At every fixed complementary row, multiplication by (g_j) is the exact
regular-unit transport.  At the moving double (j), the cube
((z-j)^3) kills the complete two-jet of the baseline exact order-two
row.  Therefore

\[
 {\cal T}_{i,j}:=g_j{\cal S}_{i,j}\subseteq{\cal K}_i
       \subseteq\mathbb C[z]_{\leq N},\qquad
                    \dim{\cal T}_{i,j}=3,qquad N=c+1,         \tag{6}
\]

where ({\cal K}_i) is the common kernel of the baseline rows and is
independent of (j).  The units used in those rows depend on the fixed
baseline (i) and the tested complementary value, not on the moving
partner.

## 3. The common kernel has dimension at most five

If ({\cal K}_i) contained a six-space, the moving-double baseline would
have one more value class than the formal complement.  Its rows consist
of the fixed complementary rows plus one exact order-two row.  Their
forced six-space Wronskian weight is

\[
 6(c+1)-\bigl(M_6+2\bigr)=6c+4-M_6.                            \tag{7}
\]

The degree-(N=c+1) cap is

\[
                         6(N+1-6)=6c-24.                       \tag{8}
\]

Equations (7)--(8) require (M_6\geq28), contrary to (1).  The standard
gcd correction for exact jet rows is nonnegative, so common factors
cannot evade this count.  Hence

                            \dim{\cal K}_i\leq5.                \tag{9}

## 4. Degrees below ten

For distinct (j,k\ne i), the quintics (g_j,g_k) are coprime by
structural nonopposition.  Inside (mathbb C[z]_{\leq N}),

\[
 g_j\mathbb C[z]_{\leq N-5}
       \cap g_k\mathbb C[z]_{\leq N-5}
   =g_jg_k\mathbb C[z]_{\leq N-10}.                            \tag{10}
\]

If (N\leq9), the right side is zero.  But (6) and (9) force

\[
             \dim({\cal T}_{i,j}\cap{\cal T}_{i,k})
                  \geq3+3-5=1.                                \tag{11}
\]

When (b\geq3), two moving partners (j,k) exist, and (10)--(11) are a
contradiction.  This proves the first line of (2).

## 5. The sharp degree-ten complete graph

Now let (N=10).  Equations (10)--(11) show that, for all distinct
(j,k\ne i),

\[
                         g_jg_k\in{\cal K}_i.                   \tag{12}
\]

Fix a tested double (v\ne i), and put

\[
                    \Omega={\mathscr D}\setminus\{i,v\}.
                                                                    \tag{13}
\]

The baseline row at (v) has the form

\[
                       J_{v,i}(T)=(U_{v,i}T)''(v),
                       \qquad U_{v,i}(v)\ne0,                  \tag{14}
\]

with one unit (U_{v,i}) common to every pair (j,k\in\Omega).
Applying (14) to (12), dividing by the nonzero undifferentiated factors,
and setting

\[
 \begin{aligned}
 A_j&={g_j'(v)\over g_j(v)},\\
 B_j&={g_j''(v)\over g_j(v)}
           +2{U_{v,i}'(v)\over U_{v,i}(v)}A_j,\\
 C&={U_{v,i}''(v)\over U_{v,i}(v)},
 \end{aligned}                                                \tag{15}
\]

gives the complete-graph equations

                         C+B_j+B_k+2A_jA_k=0                   \tag{16}

for every distinct (j,k\in\Omega).  Comparing (16) first with fixed
(j), then with a second fixed index, shows that four distinct indices
(i_1,i_2,i_3,i_4\in\Omega) obey

                (A_{i_1}-A_{i_2})(A_{i_3}-A_{i_4})=0.          \tag{17}

Thus among any four or more (A)-values, all but at most one are equal:
two distinct values each occurring twice violate (17), and three distinct
values also violate it.  In particular, if (|\Omega|\geq4), at least
three of them are equal.

But the first logarithmic jet is

\[
             A_x={3\over v-x}+{2\over v+x}
                    ={5v+x\over v^2-x^2}.                      \tag{18}
\]

Every fibre of this rational map contains at most two structurally
allowed values (x\ne\pm v), because (A_x=a) is the nonzero polynomial
equation

\[
                       a(v^2-x^2)-(5v+x)=0                     \tag{19}
\]

of degree at most two, with coefficient of (x) equal to (-1).
Therefore (|\Omega|\geq4) is impossible.  Since
(|\Omega|=b-2), this proves the second line of (2) for (b\geq6).

## 6. Exact (p=19) specialization

Select two exact doubles and (h-2) singleton layers.  If (e=0) for
the no-quartic type and (e=1) for the one-quartic type, the number of
leftover singleton classes is

\[
                 L=u+2=23-4e-3a-2b.                            \tag{20}
\]

Thus

\[
 c=e+a+(b-2)+L,qquad
 N=c+1=
 \begin{cases}
 22-2a-b,&e=0,\\
 19-2a-b,&e=1.
 \end{cases}                                                  \tag{21}
\]

The formal selection exists exactly in the range used here because every
family in (3) has (b\geq2) and (u\geq-2).  Substituting (21) into (2)
gives exactly the fourteen pairs in (3).

As in the singleton-parity theorem, the (p=19) (q=6) gap is strict,
and a four-dimensional selected-row kernel is excluded by the audited
low-role incidence argument.  Hence every pair selection used above has
the asserted relation three-space (4).

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_double_common_lift_closure.py](../computations/verify_live_three_zero_higher_split_p19_double_common_lift_closure.py)
checks the common-kernel six-space inequality, all fourteen formal
selections and degree formulas, coprime-intersection dimensions, the
complete-graph subtraction identity, the exact logarithmic jet and its
degree-two fibre bound, disjointness from the singleton closure, and the
combined (71/94) ledger.
