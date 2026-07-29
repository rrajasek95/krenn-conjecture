# Two two-term colour components still have no common-power lift

## 1. Result

Let \(U\) be a six-set.  At every site \(u\), let \(V_u\) contain three
distinguished independent vectors

\[
e_0^{(u)},e_1^{(u)},e_2^{(u)}.
\]

For a pair \(P\subset U\), put

\[
 E_i(P)=\bigotimes_{u\notin P}e_i^{(u)},
 \qquad X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

Choose two distinct pairs \(A_0,A_1\), two distinct pairs \(B_0,B_1\),
and one further pair \(C\).  Repetitions between the three colour blocks
are allowed.  For five nonzero complex numbers, set

\[
 F=\alpha_0E_0(A_0)+\alpha_1E_0(A_1)
   +\beta_0E_1(B_0)+\beta_1E_1(B_1)+\gamma E_2(C).       \tag{1}
\]

The six star rows

\[
 p_0,p_1,p_2,s_0,s_1,s_2\in\bigoplus_{u\in U}V_u
\]

may have arbitrary multi-site support, arbitrary local components, and
arbitrary complex cancellation.  Retain the nine literal products

\[
                         p_i s_jF=\delta_{ij}X_i.       \tag{2}
\]

All multiplication takes place in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                      \tag{3}
\]

**Theorem 1.1 (two-two-one obstruction).**  Under (1)--(2), there is no
quadratic \(q\) such that

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.    \tag{4}
\]

In fact, the conclusion is stronger: (1) and (4) alone are inconsistent
for every choice of the five supports, including all cross-colour
repetitions.  The products are not used in the final obstruction.

The exact checker
[`verify_two_two_one_monomial_common_power_obstruction.py`](../computations/verify_two_two_one_monomial_common_power_obstruction.py)
audits all support and response orbits, constructs the complete rational
kernel of \(qF=0\) without dividing by any target coefficient, freezes the
generator streams, and replays the unsaturated affine ideals over
\(\mathbb Q\).

## 2. The tempting distinct-support reduction is false

For a pair \(P=\{a,b\}\), multiplication by \(p_i s_j\) retains both
endpoint orders:

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
              +s_{j,a}\otimes p_{i,b}.                 \tag{5}
\]

It is not true that (2) forces all five pairs to be distinct.  Take unit
coefficients and

\[
 (A_0,A_1)=(01,02),\qquad (B_0,B_1)=(01,03),\qquad C=45. \tag{6}
\]

Thus the pair \(01\) is shared by colours zero and one.  Define

\[
\begin{array}{c|cc}
 i&p_i&s_i\\ \hline
0&e_0^{(0)}&e_0^{(2)}\\
1&e_1^{(3)}&e_1^{(0)}\\
2&e_2^{(4)}&e_2^{(5)}
\end{array}                                             \tag{7}
\]

The three diagonal products select respectively the private pairs
\(02,03,45\), and hence equal \(X_0,X_1,X_2\).  The six ordered off-diagonal
site pairs are

\[
 00,\ 05,\ 23,\ 35,\ 24,\ 04.
\]

The first is killed by the square-zero relation and none of the other five
is a support in (6).  Therefore every off-diagonal product vanishes.  This
is an exact response table satisfying all nine equations (2), and it
falsifies the naive pairwise-distinct claim.

## 3. Target-colour separation and simultaneous weight normalization

For a colour \(k\) and pair \(P\), let \(W_k(P)\) be the full-support
subspace obtained by inserting arbitrary factors at \(P\) and the fixed
\(e_k\)-factors outside \(P\).  If \(k\ne l\), then

\[
                         W_k(P)\cap W_l(Q)=0            \tag{8}
\]

for all pairs \(P,Q\).  Indeed, \(P\cup Q\) has at most four sites, so at
least two sites remain outside it.  Every coordinate word in the first
space has letter \(k\) there, while every word in the second has letter
\(l\).  Consequently the response equations may be separated by target
colour even when \(P=Q\).  After normalization, their literal form is

\[
 \sum_{P\in\mathcal S_k}\iota_{k,P}B_{ij}(P)
       =\delta_{ik}\delta_{jk}X_k,                     \tag{9}
\]

where

\[
 \mathcal S_0=\{A_0,A_1\},\quad
 \mathcal S_1=\{B_0,B_1\},\quad
 \mathcal S_2=\{C\}.
\]

Equation (9) retains all cancellation between the two lifts of one colour.
It does not separate those two summands coefficientwise.

The five nonzero weights in (1) can be normalized simultaneously.  For
each colour \(i\), independently scale its six local axes by

\[
 e_i^{(u)}\longmapsto t_{i,u}e_i^{(u)},\qquad
 t_{i,u}\in\mathbb C^*,\qquad \prod_{u\in U}t_{i,u}=1. \tag{10}
\]

This fixes every \(X_i\), while a coefficient \(\lambda E_i(P)\) becomes

\[
 \lambda\prod_{u\notin P}t_{i,u}E_i(P)
       ={\lambda\over\prod_{u\in P}t_{i,u}}E_i(P).    \tag{11}
\]

For two distinct pairs \(P,Q\), prescribe their two pair products to be
the two desired weights.  If they meet, put value \(1\) at the common
endpoint and the two weights at the two private endpoints; if they are
disjoint, put each weight at one endpoint of its pair.  In both cases a
site outside \(P\cup Q\) corrects the total product to \(1\).  For the
single pair, prescribe its pair product and correct the total at any site
outside it.  Colours zero, one, and two use disjoint sets of axis-scaling
variables.  Hence a repeated *physical* pair in different colours creates
no coupling between these three normalizations.

This target-preserving algebra automorphism takes all five coefficients to
one, carries \(p_i,s_j,q\) with it, preserves (2), and commutes with bracket
powers.  No genericity, division by a possibly zero response, or choice of
a root is involved.  From now on all target coefficients are one.

Projection of every \(V_u\) onto the displayed three-dimensional subspace,
fixing its three axes, induces an algebra homomorphism fixing \(F\).  Thus a
solution in larger local spaces would project to a three-dimensional
solution.  The exact calculations lose no generality by using three local
coordinates.

## 4. Complete response census

There are 15 missing pairs.  The lifts within each two-term block are
unordered, but the two blocks are initially colour-labelled.  Hence there
are

\[
                         {15\choose2}^2\,15=165{,}375   \tag{12}
\]

labelled-site supports.  Swapping the entire colour-zero and colour-one
blocks fixes the \(105\cdot15=1{,}575\) choices with the two blocks equal,
so Burnside gives

\[
                 {165{,}375+1{,}575\over2}=83{,}475    \tag{13}
\]

supports modulo that swap.  Quotienting further by \(S_6\) leaves exactly
195 orbits.  Their orbit-size histogram is

\[
\begin{array}{c|rrrrrrr}
\text{orbit size}&45&60&90&120&180&360&720\\ \hline
\text{number}&3&2&8&2&31&85&64.
\end{array}                                             \tag{14}
\]

The response checker expands (9) in all coordinate words.  For every pair
of rows \(i,j\), every target colour \(k\), and every local word at a
missing pair, it inserts both monomials in (5), first collecting equal
six-site words across the two same-colour lifts.  Thus its ideals allow
arbitrary rows, zeros, dependencies, and complex cancellation.

Among the 101 repeated-support orbits, exactly twelve admit a response.
All twelve have four distinct physical pairs: one pair is shared by the
two two-term colours, and each colour has a private pair.  The following
table gives all twelve orbit representatives and a coordinate response.
An arrow \(a\to b\) means that \(p_i\) is placed at \(a\), \(s_i\) at \(b\),
both on colour axis \(i\).

| orbit | support \((A_0,A_1;B_0,B_1;C)\) | private arrows for colours \(0,1,2\) | orbit size |
|---:|---|---|---:|
| 13 | `(01,02;01,03;45)` | `0->2, 3->0, 4->5` | 180 |
| 24 | `(01,02;01,13;24)` | `0->2, 1->3, 2->4` | 720 |
| 25 | `(01,02;01,13;45)` | `0->2, 1->3, 4->5` | 180 |
| 32 | `(01,02;01,23;14)` | `0->2, 2->3, 1->4` | 720 |
| 36 | `(01,02;01,23;45)` | `0->2, 2->3, 4->5` | 360 |
| 40 | `(01,02;01,34;05)` | `0->2, 3->4, 5->0` | 360 |
| 42 | `(01,02;01,34;13)` | `0->2, 3->4, 1->3` | 720 |
| 43 | `(01,02;01,34;15)` | `0->2, 3->4, 1->5` | 360 |
| 45 | `(01,02;01,34;25)` | `0->2, 3->4, 2->5` | 360 |
| 47 | `(01,02;01,34;35)` | `0->2, 3->4, 5->3` | 720 |
| 161 | `(01,23;01,24;05)` | `2->3, 4->2, 0->5` | 360 |
| 167 | `(01,23;01,45;02)` | `2->3, 4->5, 0->2` | 360 |

Their orbit sizes sum to \(5{,}400\) supports modulo the block-colour swap.
For each table row, the checker verifies all coordinate coefficients of all
nine products.  For the other 89 repeated-support orbits, the full
unsaturated response ideal is the unit ideal over \(\mathbb Q\).  In
particular, the repeated-support classification has no hidden non-coordinate
or zero/cancellation branch.

Across all 195 orbits, the complete response census is:

| distinct physical pairs | all orbits | coordinate-response orbits | proper non-coordinate ideals | unit response ideals | coordinate-response labelled supports |
|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 0 | 0 | 2 | 0 |
| 3 | 23 | 0 | 0 | 23 | 0 |
| 4 | 76 | 12 | 0 | 64 | 5,400 |
| 5 | 94 | 40 | 0 | 54 | 19,395 |
| **total** | **195** | **52** | **0** | **143** | **24,795** |

Thus every response-feasible orbit has an explicit coordinate witness;
there is no orbit known feasible merely because its ideal is proper.  The
other 143 full unsaturated nine-product ideals are unit over \(\mathbb Q\).
The checker freezes and replays this full census before the common-power
calculation.

## 5. The simultaneous \(qF=0\) kernel

Bracket powers satisfy

\[
                          q q^{[2]}=3q^{[3]}.            \tag{15}
\]

Therefore (4) implies the necessary linear equation

\[
                               qF=0.                    \tag{16}
\]

Write \(q_P(a,b)\) for the local coordinate of the quadratic block on the
unordered pair \(P=\{u,v\}\), ordered by \(u<v\).  For every full word
\(w\in\{0,1,2\}^U\), the complete coefficient equation in (16) is

\[
 \sum_{k=0}^2\ \sum_{\substack{P\in\mathcal S_k\\
                      w|_{U\setminus P}\equiv k}}
       q_P(w|_P)=0.                                    \tag{17}
\]

This is the simultaneous incidence kernel.  Formula (17) neither assumes
distinct physical pairs nor divides by a target coefficient.  If a pair is
used by several colours, its same nine \(q_P(a,b)\) columns occur in each
relevant colour system, so row reduction takes the intersection of the
constraints automatically.  The target-colour word separation (8) remains
valid, but shared columns are not duplicated.

There are 135 quadratic coordinates.  Exact rational RREF of (17) gives:

| distinct physical pairs | labelled supports modulo block swap | orbits | \(\operatorname{rank}(qF) / \dim\ker(qF)\) (number of orbits) |
|---:|---:|---:|---|
| 2 | 210 | 2 | `18 / 117` (2) |
| 3 | 5,460 | 23 | `27 / 108` (23) |
| 4 | 32,760 | 76 | `33 / 102` (23), `35 / 100` (23), `36 / 99` (30) |
| 5 | 45,045 | 94 | `39 / 96` (35), `41 / 94` (40), `43 / 92` (19) |

For every orbit the checker constructs one basis vector for every free RREF
column, verifies all basis vectors against every row of (17), verifies
rank plus nullity equals 135, and then uses those basis vectors as the
affine coordinates of \(q\).

## 6. All 195 common-power ideals are unit

For a four-set \(S=\{u_0,u_1,u_2,u_3\}\) and a local word
\(c\in\{0,1,2\}^S\), the coefficient of \(q^{[2]}\) is the literal
three-matching sum

\[
\begin{aligned}
 &q_{u_0u_1}(c_0,c_1)q_{u_2u_3}(c_2,c_3)
 +q_{u_0u_2}(c_0,c_2)q_{u_1u_3}(c_1,c_3)\\
 &\hspace{35mm}
 +q_{u_0u_3}(c_0,c_3)q_{u_1u_2}(c_1,c_2).             \tag{18}
\end{aligned}
\]

The checker substitutes the complete kernel (17) into all
\({6\choose4}3^4=1{,}215\) coefficients of \(q^{[2]}-F\), omitting only
polynomials that simplify literally to zero.  It sends the resulting
quadratic generators to Singular over \(\mathbb Q\), with no saturation and
no nonvanishing side condition.  Every one of the 195 Gröbner bases is
\([1]\).  Thus there is no solution over \(\mathbb C\), including every
zero, cancellation, repeated-support, and exceptional branch.

The frozen support-orbit ledger has SHA-256

```text
68f24f11d160d5600efec4972f314da8ee6e1ab560e08f17901a63bb7102eb12
```

and the ordered \(qF\)-RREF/common-power generator ledger has SHA-256

```text
1cbb10f5acc01724fff0d44e981c0dbb1d731d8eff4e6a8ac7d92afb59d70a36
```

The 52 positive response witnesses and the 143 response-unit ideals have
separate frozen ledgers in the verifier, with SHA-256 values

```text
f787c6ae228981d10d6a53f93ffbe4da26d8c40d686dbc0642c64cc91b033145
79bbf6ff63fa8192b2b2b3787e93c7d4fbe9d61cebd1f7767622ff36d67038e9
```

The logical cover is simple: a response-unit support cannot satisfy (2),
while every one of the 52 supports left by the response census is excluded
by its full common-power unit ideal.  In fact, because the latter ideals are
unit on all 195 orbits, the common-power conclusion is independent of the
response classification.

This closes exactly the pure multiplicity profile \((2,2,1)\).  It does not
cover larger multiplicities, non-pure four-site target tensors, or the
unconditional global descent to this six-site model.
