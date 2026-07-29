# The eighth split: order-two common-pole closure of \((4,4,3,3,3,3)\)

## 1. Result

Consider the smallest residual profile in the \(h=8,\ k=2\) collision
frontier,

\[
                 (h,k;\lambda)=(8,2;(4,4,3,3,3,3)).       \tag{1}
\]

Thus \(p=h+k=10\), the exceptional multiset has twenty labels, two value
classes \(A,B\) have multiplicity four, and four value classes

\[
                         X=\{x_1,x_2,x_3,x_4\}             \tag{2}
\]

have multiplicity three.  The six exceptional values are distinct,
pairwise nonopposite, and structurally separated from \(\pm\mu\).  The
standing cyclic three-zero reduction has \(\mu\ne0\).

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The argument proves the following slightly broader form.  At
\(h=8,\ k=2\), suppose four pairwise distinct and pairwise nonopposite
value classes each support three selected labels, and suppose every
\((3,3,2)\) assignment on every three of those four classes leaves a
singleton in the complement.  Then the profile is impossible.  The four
exact triple classes in (1) make all twelve legality hypotheses automatic.

The generic order-\(k\) moving-role theorem needs \(2k+1=5\) candidate
classes and therefore does not see this six-class profile after two roles
are fixed.  Here the twelve legal \((3,3,2)\) cores are compared instead.
Their exact first and second logarithmic jets force all four triple values
into one fibre of a degree-two rational function.

## 2. The twelve constant-residual cores

Assume for contradiction that every isolated-star pivot vanishes.  Choose
any three-element subset \(Y\subset X\), distinguish \(x\in Y\), and
select

\[
                         R_{Y,x}=x^2
                         \prod_{y\in Y\setminus\{x\}}y^3. \tag{3}
\]

This selects \(2+3+3=h\) labels in exactly three value classes.  Its
complement consists of the two quartic classes, the omitted triple class,
and the one label left at \(x\), so

\[
                   N_{Y,x}=A^4B^4(X\setminus Y)^3x,
                   \qquad |N_{Y,x}|=12=p+2.               \tag{4}
\]

In particular, \(x\) is a singleton row class in the complement.  The
simultaneous-Hermite lemma therefore gives a nonzero rational dependence

\[
 F_{Y,x}(z)={Q_{Y,x}(z)\over D_{Y,x}(z)},\qquad
 D_{Y,x}(z)=(z+\mu)^3
             (z+x)^3\prod_{y\in Y\setminus\{x\}}(z+y)^4. \tag{5}
\]

The exact degrees are

\[
 \deg D_{Y,x}=14,\qquad
 \deg Q_{Y,x}\le p+3-1=12.                               \tag{6}
\]

All twelve complementary row jets divide \(Q_{Y,x}\), counting
multiplicity.  Hence the residual has degree zero:

\[
                   Q_{Y,x}=q_{Y,x}P_{N_{Y,x}},
                   \qquad q_{Y,x}\in\mathbb C^*.          \tag{7}
\]

Consequently \(F_{Y,x}=O(z^{-2})\).  Every selected exceptional pole has
zero simple residue by construction, and there is no residue at infinity.
The residue theorem forces the residue at the only remaining pole,
\(-\mu\), to vanish.  This pole has exact order three, so the resulting
condition is the order-two coefficient of its regular cofactor.

There are four choices of \(Y\) and three choices of its distinguished
member.  Thus (3) supplies all twelve equations used below.

## 3. One universal common-pole background

Let \(m_v\) be the full multiplicity of an exceptional value \(v\), and
let \(r_v\ge1\) be its selected multiplicity when \(v\) occurs in a core.
For each selected class, equation (7) rewrites the regular part of (5)
using

\[
 { (z-v)^{m_v-r_v}\over (z+v)^{r_v+1}}
 =(z-v)^{m_v}
   {1\over (z-v)^{r_v}(z+v)^{r_v+1}}.                    \tag{8}
\]

An unselected class already contributes just \((z-v)^{m_v}\).  Thus the
first factor in (8), taken over the full exceptional multiset, is
independent of the selected core.  Put \(w=z+\mu\), divide all factors by
their nonzero values at \(w=0\), and absorb the nonzero scalar
\(q_{Y,x}\) into a constant \(C_{Y,x}\).  Then every dependence has the
form

\[
 F_{Y,x}(-\mu+w)
 ={C_{Y,x}\over w^3}\,
 U(w)\prod_{v\in Y}\widehat\rho_{r_v,v}(w),               \tag{9}
\]

where \(C_{Y,x}\ne0\), the same unit \(U\) occurs for every core,
\(U(0)=1\), and

\[
 \widehat\rho_{r,v}(w)=
 \left(1-{w\over v+\mu}\right)^{-r}
 \left(1+{w\over v-\mu}\right)^{-(r+1)}.                 \tag{10}
\]

This full-multiset normalization is important: changing \(Y\), or changing
which member of \(Y\) has role two, does not move an unrecorded background
term.

Define the background logarithmic jets

\[
 \alpha=(\log U)'(0),\qquad \beta=(\log U)''(0),          \tag{11}
\]

and the role jets

\[
\begin{split}
 \phi_r(v)
  &:=(\log\widehat\rho_{r,v})'(0)
    ={r\over v+\mu}-{r+1\over v-\mu},\\
 \psi_r(v)
  &:=(\log\widehat\rho_{r,v})''(0)
    ={r\over(v+\mu)^2}+{r+1\over(v-\mu)^2}.              \tag{12}
\end{split}
\]

For any three-role core, twice the \(w^2\)-coefficient of the normalized
regular factor is

\[
 \left(\alpha+\sum_v\phi_{r_v}(v)\right)^2
       +\beta+\sum_v\psi_{r_v}(v).                        \tag{13}
\]

Thus the common-pole residue equation is exactly the vanishing of (13).
No first-order approximation is being made.

## 4. Dropping one triple role from three to two

The changes in the two logarithmic jets are

\[
\begin{split}
 d(v)&:=\phi_3(v)-\phi_2(v)
       =-{2\mu\over v^2-\mu^2},\\
 \Delta(v)&:=\psi_3(v)-\psi_2(v)
       ={1\over(v+\mu)^2}+{1\over(v-\mu)^2}\\
       &={2(v^2+\mu^2)\over(v^2-\mu^2)^2}
        =d(v)^2-{d(v)\over\mu}.                           \tag{14}
\end{split}
\]

For two admissible values \(v\ne w\),

\[
 d(v)-d(w)=
 {2\mu(v-w)(v+w)\over
  (v^2-\mu^2)(w^2-\mu^2)}.                               \tag{15}
\]

Every factor on the right of (15) is nonzero: \(\mu\ne0\), the values are
distinct and nonopposite, and \(v\ne\pm\mu\).  Hence the four values
\(d(x_i)\) are pairwise distinct.

Fix \(Y=\{x,y,z\}\subset X\), and introduce the all-role-three totals

\[
 T_Y=\alpha+\sum_{a\in Y}\phi_3(a),\qquad
 W_Y=\beta+\sum_{a\in Y}\psi_3(a).                        \tag{16}
\]

The all-role-three core would select nine labels and is not used.  The
notation in (16) is only a convenient common reference for the three legal
cores in (3).  If \(a\in Y\) is assigned role two, (13)--(14) give

\[
\begin{split}
 0
  &=(T_Y-d(a))^2+W_Y-\Delta(a)\\
  &=T_Y^2+W_Y+\left({1\over\mu}-2T_Y\right)d(a).          \tag{17}
\end{split}
\]

Subtract (17) for two members of \(Y\).  Their \(d\)-values are distinct,
so

\[
                         T_Y={1\over2\mu}.                \tag{18}
\]

Substitution back into (17) then gives

\[
                         W_Y=-{1\over4\mu^2}.             \tag{19}
\]

The proof does not divide by a possibly vanishing role difference:
equation (15) establishes its nonvanishing first.

## 5. Comparing the four three-subsets

Apply (18) to each set \(Y=X\setminus\{x_i\}\).  All four equations have
the same background \(\alpha\), so for any \(i,j\),

\[
 0=T_{X\setminus\{x_i\}}-T_{X\setminus\{x_j\}}
   =\phi_3(x_j)-\phi_3(x_i).                              \tag{20}
\]

Thus all four triple values lie in one fibre of

\[
 \phi_3(x)
   ={3\over x+\mu}-{4\over x-\mu}
   =-{x+7\mu\over x^2-\mu^2}.                            \tag{21}
\]

For a scalar \(\lambda\), clearing the structurally nonzero denominator
in \(\phi_3(x)=\lambda\) gives

\[
                   \lambda(x^2-\mu^2)+x+7\mu=0.          \tag{22}
\]

This is a nonzero polynomial of degree at most two.  Even if
\(\lambda=0\) makes the quadratic term disappear, its coefficient of
\(x\) is one.  A fibre of (21) therefore contains at most two admissible
values, whereas (20) supplies the four distinct values in \(X\).  This
contradiction proves Theorem 1.1.

## 6. Independent consecutive-swap check

There is a shorter three-core check using the quartic classes.  Fix any
triple value \(x\) and compare the legal cores

\[
                  A^4B^2x^2,\qquad
                  A^3B^3x^2,\qquad
                  A^2B^4x^2.                             \tag{23}
\]

The label left at \(x\) makes all three complements legal.  In the
first-log-jet sum, each transfer of one label from \(A\) to \(B\) has the
same increment

\[
                         D=d(B)-d(A),                     \tag{24}
\]

and the second-log-jet sum likewise has the same increment
\(E=\Delta(B)-\Delta(A)\).  If
\(\mathcal E_0,\mathcal E_1,\mathcal E_2\) denote the three expressions
in (13), direct expansion gives

\[
       (\mathcal E_2-\mathcal E_1)
        -(\mathcal E_1-\mathcal E_0)=2D^2.                \tag{25}
\]

All three \(\mathcal E_i\) vanish, hence \(D=0\).  Since \(\mu\ne0\),
(15) forces \(A^2=B^2\), contrary to distinctness and nonoppositeness.
This independently closes the profile without the four-subset fibre
argument.

Formally allowing \(\mu=0\) creates no hidden edge in this cross-check.
Then \(D=0\) identically, but the first difference of the equations gives
\(E=0\); at \(\mu=0\),

\[
                         E={2\over B^2}-{2\over A^2},     \tag{26}
\]

which again forces \(A^2=B^2\).  The actual cyclic stratum already has
\(\mu\ne0\).

## 7. Zero, gcd, and denominator audit

All six exceptional classes in (1) are repeated, and a repeated
exceptional value is structurally nonzero.  Thus the possible zero
exceptional singleton does not occur.  More importantly, every argument
above only divides by the structural factors \(v-\mu\), \(v+\mu\),
\(\mu\), and the explicitly nonzero difference (15).

There is no residual-polynomial gcd case.  Equation (7) has a nonzero
constant residual, so different cores can change only the harmless scalar
\(q_{Y,x}\).  Every normalized role factor in (10) is a unit at \(w=0\);
there is no common zero which could lower the order-three pole or turn its
order-two residue functional into a lower-order condition.

The no-opposite hypothesis is used exactly in (15) and in the final
consecutive-swap contradiction.  The degree-two fibre contradiction also
retains the possible degree drop at \(\lambda=0\).

## 8. Exact audit

[verify_live_three_zero_eighth_split_443333_order_two_common_pole.py](../computations/verify_live_three_zero_eighth_split_443333_order_two_common_pole.py)
checks all twelve legal \((3,3,2)\) cores, the Hermite and infinity
degrees, the universal full-multiset baseline, the exact order-three local
residue, both logarithmic jets, identities (14)--(17), the nonopposite
factorization (15), the rank-three four-subset comparison, the degree-two
fibre including \(\lambda=0\), and the independent consecutive-quartic
swap including the formal \(\mu=0\) edge.
