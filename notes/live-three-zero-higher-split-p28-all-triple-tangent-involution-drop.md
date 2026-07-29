# Higher splits: the \(p=28\) all-triple tangent-involution drop

## 1. Scope and result

Continue from the
[first selected six-kernel boundary](live-three-zero-higher-split-p28-six-kernel-boundary.md).
At \(p=h+k=28\), fix a moving-triple family whose restored common
baseline has profile

\[
                              3^{10}.                         \tag{1}
\]

For each of the ten triple values \(i\), selecting that triple in role
two leaves the relation-space complement

\[
                              3^9 1_i.                         \tag{2}
\]

This situation occurs for the residual tuple \((e,a,b,u)=(0,10,0,0)\).
It also occurs for \((0,10,1,-2)\) after the unique double is held fixed
in role two; that fixed layer is common to all ten selections and does
not change the complementary profile, its saturation ledger, or the
quartic moving-triple transport argument.

**Theorem 1.1 (all-triple tangent-involution drop).**  The ten selections
in such a moving-triple family cannot all have six-dimensional selected
row kernel.  Consequently at least one of them has selected kernel
dimension at most five.

This is a dimension-drop theorem, not a closure of either collision
profile.  In particular, no implication from the existence of one
five-dimensional selected kernel to impossibility of the original
profile is asserted here.

All values below satisfy the structural hypotheses already used in the
boundary theorem: the ten triple values are nonzero, distinct, and
pairwise nonopposite.

## 2. The ten saturated relation four-spaces

Suppose, for contradiction, that all ten selected row kernels have
dimension six.  Let \(\mathcal S_i\) be the relation space belonging to
the selection of the triple value \(i\).  The relation-space theorem and
(2) give

\[
             \mathcal S_i\subseteq\mathbb C[z]_{\leq6},
             \qquad \dim\mathcal S_i=4.                       \tag{3}
\]

An exact order-\(m\) row on a primitive four-space has its least
vanishing sequence by omitting \(m\) from \((0,1,2,3,4)\), and hence
least Wronskian weight \(4-m\) for \(m\leq4\).  Thus the selected simple
class at \(i\) contributes three units and each of the other nine triple
classes contributes one.  These twelve units equal the full cap

\[
                         4(7-4)=12.                            \tag{4}
\]

There is no hidden common gcd.  At an exact order-\(m\) row, a common
zero of order \(0<g<m\) changes the local lower bound to

\[
                    4g+\max(0,4-m+g)>4-m.                     \tag{5}
\]

If \(g=m\), the exact highest-jet coefficient kills the leading
coefficient after division and contradicts maximality of the gcd; if
\(g>m\), the contribution \(4g\) is already too large.  An unlisted gcd
root costs at least four new units.  Since (4) is exhausted, every
\(\mathcal S_i\) is primitive and its finite vanishing sequences are
exactly

\[
 \begin{array}{c|c}
  z=i &(0,2,3,4),\\
  z=j,\ j\ne i &(0,1,2,4),\\
  z\notin\{\text{the ten triple values}\}&(0,1,2,3).
 \end{array}                                                  \tag{6}
\]

There is no ramification at infinity.  Indeed, if the echelon degrees
of \(\mathcal S_i\) are \(n_0<\cdots<n_3\leq6\), then

\[
       12=\deg\operatorname {Wr}(\mathcal S_i)
          \leq\sum_r n_r-6\leq12.                             \tag{7}
\]

Hence the degrees are exactly \((3,4,5,6)\), and the leading Wronskian
coefficient is nonzero.  Structural nonopposition and (6) also show that
every point \(-j\) is an unlisted regular point of \(\mathcal S_i\).

## 3. Exact pair intersections give nine tangent identifications

For each triple value put

\[
                      B_i=(z-i)^2(z+i)^2.                     \tag{8}
\]

The exact moving-triple lift gives transported four-spaces

\[
 B_i\mathcal S_i=\mathcal T_i\subseteq\mathcal K
                         \subseteq\mathbb C[z]_{\leq10}.       \tag{9}
\]

The common baseline has ten exact order-three rows.  A hypothetical
seven-space has forced Wronskian weight \(10(7-3)=40\), against cap
\(7(11-7)=28\).  Thus

\[
                              \dim\mathcal K\leq6.             \tag{10}
\]

For distinct \(i,j\), the factors \(B_i,B_j\) are coprime.  Therefore

\[
 B_i\mathbb C[z]_{\leq6}\cap B_j\mathbb C[z]_{\leq6}
              =B_iB_j\mathbb C[z]_{\leq2},                    \tag{11}
\]

while (9)--(10) give

\[
                    \dim(\mathcal T_i\cap\mathcal T_j)\geq2. \tag{12}
\]

Choose a basis \(f_0,\ldots,f_3\) of \(\mathcal S_i\) and write its
evaluation vector

\[
                         F_i(z)=(f_0(z),\ldots,f_3(z)).         \tag{13}
\]

After division by \(B_i\), (11)--(12) say that at least a two-space in
\(\mathcal S_i\) is divisible by \(B_j\).  Equivalently, the four-row
jet matrix

\[
 \begin{pmatrix}
 F_i(j)\\ F_i'(j)\\ F_i(-j)\\ F_i'(-j)
 \end{pmatrix}                                                \tag{14}
\]

has rank at most two.  Its first two rows are independent by the
sequence \((0,1,2,4)\) at \(j\), and its last two rows are independent
because \(-j\) is regular.  Hence (14) has rank exactly two and

\[
 \boxed{
  \langle F_i(j),F_i'(j)\rangle
       =\langle F_i(-j),F_i'(-j)\rangle
 }
                 \qquad(j\ne i).                              \tag{15}
\]

This also proves that every pair intersection in (12) has dimension
exactly two.  In particular \(\dim\mathcal K=6\): a smaller common
kernel would force the pair intersection to have dimension at least
three, contradicting the rank-two conclusion above.  For completeness,
three distinct transports have zero common intersection, since every
common member would be divisible by the degree-twelve product
\(B_iB_jB_k\) while having degree at most ten:

\[
                  \mathcal T_i\cap\mathcal T_j\cap
                         \mathcal T_k=0.                        \tag{16}
\]

The triple-intersection statement is consistent with, but is not needed
for, the argument below.

## 4. The tangent Pluecker map has degree nine

Fix \(i\).  For \(0\leq a<b\leq3\), put

\[
       G_{ab}(z)=f_a(z)f_b'(z)-f_b(z)f_a'(z),
       \qquad G=(G_{ab})_{a<b}.                                \tag{17}
\]

The echelon degrees \((3,4,5,6)\) show that every coordinate of \(G\)
has degree at most ten and that the coordinate formed from the degree
five and degree six basis members has degree exactly ten.  Thus (17) is
the degree-ten homogeneous Pluecker vector of the tangent-line map.

The vector \(G(a)\) vanishes exactly when \(F_i(a),F_i'(a)\) are
dependent.  By (6), this occurs at the finite point \(a=i\) and nowhere
else.  In a local basis with orders \((0,2,3,4)\), the minor formed from
the order-zero and order-two members vanishes exactly to first order.
There is no common zero at infinity by the exact echelon degrees.
Consequently

\[
                         \widetilde G={G\over z-i}              \tag{18}
\]

is a primitive, everywhere nonzero polynomial Pluecker vector of degree
nine.  It represents the tangent-line morphism

\[
       \tau_i:\mathbb P^1_z\longrightarrow
          \operatorname {Gr}(2,4),\qquad
       \tau_i(z)=\langle F_i(z),F_i'(z)\rangle.                \tag{19}
\]

For two coordinates of (18), consider the cross-minor

\[
 H_{ab,cd}(z)=\widetilde G_{ab}(z)\widetilde G_{cd}(-z)
       -\widetilde G_{cd}(z)\widetilde G_{ab}(-z).             \tag{20}
\]

It is odd and has degree at most eighteen (in fact at most seventeen).
Equation (15) makes it vanish at the eighteen distinct points

\[
                         \{\pm j:j\ne i\}.                     \tag{21}
\]

Equivalently, using the coarser degree-eighteen bound, oddness supplies
the additional root zero.  In either count, (20) vanishes identically.
Primitivity of \(\widetilde G\) therefore gives

\[
                         \boxed{\tau_i(z)=\tau_i(-z)}           \tag{22}
\]

as an identity of morphisms.

## 5. Classification of the tangent-involution identity

Put \(t=z^2\) and decompose the polynomial vector uniquely as

\[
                  F_i(z)=E(t)+zO(t),\qquad
                  F_i(-z)=E(t)-zO(t).                          \tag{23}
\]

There are two exhaustive generic cases.

### 5.1 The two points are generically distinct

If \([F_i(z)]\ne[F_i(-z)]\) generically, their span is the tangent line
in (22), so

\[
                   \tau_i(z)=\langle E(t),O(t)\rangle.         \tag{24}
\]

Both \(F_i'(z)\) and \(F_i'(-z)\) belong to this plane.  Their sum and
difference are

\[
 \begin{aligned}
 F_i'(z)-F_i'(-z)&=4zE'(t),\\
 F_i'(z)+F_i'(-z)&=2O(t)+4tO'(t).
 \end{aligned}                                                \tag{25}
\]

For generic nonzero \(t\), (24)--(25) imply

\[
              E'(t),O'(t)\in\langle E(t),O(t)\rangle.          \tag{26}
\]

The derivative of the Pluecker point \([E(t)\wedge O(t)]\) is therefore
zero.  In characteristic zero the resulting rational map to
\(\operatorname {Gr}(2,4)\) is constant.  Hence all values of \(F_i\)
lie in one fixed two-dimensional vector subspace of \(\mathbb C^4\).
This gives two constant linear relations among the four basis
polynomials \(f_0,\ldots,f_3\), contradicting their independence.

### 5.2 The two points are generically equal

Suppose instead that \(F_i(-z)=\rho(z)F_i(z)\) projectively.  The vector
\(F_i\) is primitive.  Bezout applied to its four coordinates shows
that \(\rho\) is a polynomial; applying the same argument after the
involution shows that its inverse is a polynomial.  Thus \(\rho\) is a
nonzero constant.  Applying the involution twice gives
\(\rho=\pm1\).  The minus sign would make all four coordinates odd and
therefore divisible by \(z\), contrary to primitivity.  Hence

\[
                            F_i(-z)=F_i(z).                     \tag{27}
\]

All four basis polynomials are even.  Since they are independent of
degree at most six, they form the complete four-space

\[
                       \langle1,z^2,z^4,z^6\rangle.            \tag{28}
\]

At the nonzero selected triple value \(i\), the change of parameter
\(t=z^2\) is etale.  The complete cubic system
\(\langle1,t,t^2,t^3\rangle\) has local vanishing sequence
\((0,1,2,3)\), so (28) has the same sequence at \(i\).  This contradicts
the exact selected-simple sequence \((0,2,3,4)\) in (6).

Both cases are impossible, proving Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_higher_split_p28_all_triple_tangent_involution_drop.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_tangent_involution_drop.py)
checks the mass and Wronskian equalities, the exact omission sequences,
the unique echelon degree profile, every pair and triple transport
degree, the tangent Pluecker gcd orders, the signed-root count, the
even/odd derivative identities, and the nonzero-point local sequence of
the full even cubic system.

The
[independent audit](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop-independent-audit.md)
reconstructs the proof without importing the primary checker and verifies
both covered residual tuples, every homogeneous and proportionality branch,
and the dimension-drop-only scope.
