# Higher splits: \(p=28\) \(4^3 3^6\) \(q=5\) saturation

## 1. Result and exact scope

Continue from the independently audited
[critical moving-triple local-jet cap](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap.md).
At \(p=28\), consider either formal tuple

\[
                  (e,a,b,u)=(3,6,0,0),\qquad(3,6,1,-2),    \tag{1}
\]

whose restored moving-triple baseline is

\[
                              4^3 3^6.                       \tag{2}
\]

For each of the six triple values \(i\), the relation complement is

\[
                              4^3 3^5 1_i.                   \tag{3}
\]

Let \(q_i\in\{5,6\}\) be its selected-row-kernel dimension, let

\[
 {\cal S}_i\subseteq\mathbb C[z]_{\leq5},\qquad
 \dim{\cal S}_i=q_i-2,
\]

and put

\[
 B_i=(z-i)^2(z+i)^2,\qquad
 {\cal T}_i=B_i{\cal S}_i\subseteq{\cal K}
                         \subseteq\mathbb C[z]_{\leq9}.     \tag{4}
\]

All values are nonzero, distinct, and pairwise nonopposite.

**Theorem 1.1 (\(q=5\) saturation).** In this exact common-lift setup,

\[
             \boxed{\dim{\cal K}=6,\qquad q_i=5
                    \text{ for all six }i.}                 \tag{5}
\]

The proof retains all three exact order-four rows of (2), all six exact
order-three rows, the five complementary order-three rows in each
space (3), and its exact order-one row at \(i\). It does not replace
any local unit by a constant.

This is a selected-kernel normal-form theorem, not a closure of either
profile in (1). Section 5 states the exact residual alternatives.

## 2. The common kernel has dimension five or six

The exact rows of (2) exclude a seven-space. Its forced finite
Wronskian weight would be

\[
                    3(7-4)+6(7-3)=33,
\]

while the degree-nine cap is \(7(10-7)=21\). The exact-row gcd
correction is nonnegative, so

\[
                              \dim{\cal K}\leq6.             \tag{6}
\]

Every transported space in (4) has dimension at least three. If
\(\dim{\cal K}\leq4\), any three of them have common intersection of
dimension at least

\[
                         3+3+3-2\cdot4=1.                    \tag{7}
\]

A polynomial in that intersection is divisible by three pairwise
coprime quartics \(B_iB_jB_k\), of degree twelve, but has degree at most
nine. This is impossible. Therefore

\[
                         \dim{\cal K}\in\{5,6\}.             \tag{8}
\]

The previous local-jet cap says that at most one \(q_i\) is six. Thus
at least five choices are exactly \(q=5\).

## 3. A cleared Robin cubic excludes dimension five

Assume \(\dim{\cal K}=5\), and fix a \(q=5\) value \(i\). Then
\(\dim{\cal T}_i=3\). For every \(j\ne i\), including a possible sole
\(q=6\) value,

\[
                         {\cal T}_i\cap{\cal T}_j\ne0.       \tag{9}
\]

Coprimality gives the ambient intersection

\[
 B_i\mathbb C[z]_{\leq5}\cap B_j\mathbb C[z]_{\leq5}
                       =B_iB_j\mathbb C[z]_{\leq1}.          \tag{10}
\]

After division by \(B_i\), equation (9) puts in \({\cal S}_i\) a
nonzero member of \(B_j\mathbb C[z]_{\leq1}\).

Normalize the exact simple row of \({\cal S}_i\) as

\[
                          f'(i)+\kappa f(i)=0.               \tag{11}
\]

The restriction of (11) to \(B_j\mathbb C[z]_{\leq1}\) is nonzero:
the coefficient of the derivative of the linear factor is
\(B_j(i)=(i^2-j^2)^2\ne0\). Its kernel is consequently one line.
Put

\[
                         a=i^2,\qquad x=j^2.
\]

A generator of that line is

\[
 F_x(z)=(z^2-x)^2
 \left((\kappa(a-x)+4i)(z-i)-(a-x)\right).                 \tag{12}
\]

Indeed,

\[
             F_x(i)=-(a-x)^3,\qquad F_x'(i)=\kappa(a-x)^3. \tag{13}
\]

For fixed \(i\), (12) is cubic in \(x\). Write

\[
                            F_x=\sum_{r=0}^3x^rC_r(z).       \tag{14}
\]

In the coefficient rows \(1,z,z^4,z^5\), the determinant of
\(C_0,C_1,C_2,C_3\) is exactly

\[
                               16i^2\ne0.                   \tag{15}
\]

Hence four distinct squared values give four independent \(F_x\)'s:
their determinant is (15) times their Vandermonde. There are five
choices \(j\ne i\), but all their \(F_{j^2}\) lie in the three-space
\({\cal S}_i\), a contradiction. Thus

\[
                              \dim{\cal K}=6.               \tag{16}
\]

There is no exceptional value of \(\kappa\). The sole coefficient-rank
drop in (15) is \(i=0\), excluded structurally.

## 4. The same family excludes the sole \(q=6\) choice

Suppose now that \(q_i=6\). Then \({\cal S}_i\) and \({\cal T}_i\)
have dimension four. Each of the other five choices has \(q=5\), so
inside the six-space (16),

\[
                 \dim({\cal T}_i\cap{\cal T}_j)
                              \geq4+3-6=1.                  \tag{17}
\]

Equations (10)--(15) apply again. Four of the five \(F_{j^2}\)'s are
independent, and therefore

\[
                         {\cal S}_i=\langle C_0,C_1,C_2,C_3\rangle.
                                                                  \tag{18}
\]

An exact symbolic calculation gives the ordinary Wronskian

\[
 \operatorname {Wr}(C_0,C_1,C_2,C_3)
       =-384iz(z-i)^3R_{i,\kappa}(z),                       \tag{19}
\]

where

\[
\begin{aligned}
R_{i,\kappa}(z)={}&\kappa^2z^3-(i\kappa^2+4\kappa)z^2\\
 &+(i^2\kappa^2+6i\kappa+5)z\\
 &-(i^3\kappa^2+10i^2\kappa+25i).                          \tag{20}
\end{aligned}
\]

This Wronskian is nonzero and has degree at most seven. If
\(\kappa\ne0\), the leading coefficient of \(R\) is \(\kappa^2\); if
\(\kappa=0\), then \(R=5(z-5i)\ne0\).

For every \(j\ne i\), the complement (3) retains \(j\) as an exact
triple. Thus a regular unit \(U_{i,j}(j)\ne0\) gives

\[
                         (U_{i,j}f)'''(j)=0
                         \qquad(f\in{\cal S}_i).            \tag{21}
\]

Equation (21) is a nonzero linear relation among the four ordinary jet
rows \(f(j),f'(j),f''(j),f'''(j)\), because the coefficient of the last
row is \(U_{i,j}(j)\ne0\). It forces the Wronskian in (19) to vanish at
all five distinct values \(j\ne i\). Those values avoid both zero and
\(i\). Together with the factors \(z(z-i)^3\), this gives at least

\[
                                1+3+5=9                     \tag{22}
\]

zeros with multiplicity, contradicting the degree bound seven. Hence
no \(q=6\) choice exists, proving (5).

## 5. The strict residual normal form

Since \({\cal K}\) is six-dimensional, the three quartic and six triple
rows force Wronskian weight

\[
                         3(6-4)+6(6-3)=24,
\]

equal to the degree-nine cap \(6(10-6)=24\). Thus the common space is
saturated: its echelon degrees are \(4,5,6,7,8,9\), and there is no
unlisted Wronskian zero.

For a basis evaluation vector, write

\[
                         F(z)=E(t)+zO(t),\qquad t=z^2.
\]

The signed first-jet four-wedge is, up to a nonzero scalar and the
standard factor \(z^4\),

\[
                         P(t)=E\wedge O\wedge E'\wedge O'. \tag{23}
\]

Optimizing over the saturated parity degrees gives

\[
                              \deg_tP\leq12.                \tag{24}
\]

Every one of the six \(q=5\) divisibility kernels makes \(P\) vanish at
the distinct point \(t=i^2\). Consequently there are two exact
alternatives:

1. \(P\equiv0\), the developable signed-line branch; or
2. for \(C_6(t)=\prod_i(t-i^2)\),

\[
                    P(t)=C_6(t)Q(t),\qquad
                    0\ne Q(t)\in\bigwedge^4\mathbb C^6[t],
                    \quad\deg Q\leq6.                       \tag{25}
\]

Every nonzero value of \(Q\) is decomposable. Remove the scalar gcd of
its coordinates and homogenize to the actual projective degree \(d\).
The rank-two annihilator bundle splits as

\[
                 {\cal A}\simeq{\cal O}(-\alpha)
                          \oplus{\cal O}(-\beta),
                 \qquad\alpha\leq\beta,\quad\alpha+\beta=d\leq6.
                                                                  \tag{26}
\]

A constant annihilating covector would be a constant relation among the
basis polynomials. A linear annihilator \(\rho(t)\) is also impossible:
differentiating \(\rho E=\rho O=0\) and using
\(\rho E'=\rho O'=0\) makes the nonzero constant covector \(\rho'\)
annihilate both \(E\) and \(O\). Therefore \(\alpha\geq2\), leaving
exactly

\[
                    (\alpha,\beta)\in
                    \{(2,2),(2,3),(2,4),(3,3)\}.            \tag{27}
\]

Equations (23)--(27) are a strict residual frontier, not a contradiction.
In particular, pairwise intersection dimensions of two \(q=5\)
three-spaces inside the common six-space have lower bound zero. A profile
closure must eliminate the developable branch and all four primitive
splittings using the retained exact rows or another common-lift incidence.

## 6. The generic tangent-rank-two residual has degree six

There is a further exact reduction in the nondevelopable alternative.
Let \(V=\mathbb C^6\), let \(W\) be the rank-four bundle represented by
the primitive residual \(\widetilde Q\), and retain its annihilator
\({\cal A}\). Thus

\[
 0\longrightarrow W\longrightarrow V\otimes{\cal O}
   \longrightarrow{\cal A}^*\longrightarrow0,
 \qquad \deg W=-d.                                        \tag{28}
\]

Consider the second fundamental map

\[
 \theta:W\longrightarrow (V/W)\otimes\Omega_{\mathbb P^1}
             \simeq{\cal A}^*\otimes\Omega_{\mathbb P^1}.  \tag{29}
\]

Assume that \(\theta\) has generic rank two. Let \(L=\ker\theta\), and
let \(\delta\geq0\) be the length of its torsion cokernel. Since
\(\deg({\cal A}^*\otimes\Omega)=d-4\), the exact sequence gives

\[
                         \deg L=4-2d+\delta.                \tag{30}
\]

Differentiation inside \(W\) induces

\[
             L\longrightarrow (W/L)\otimes\Omega.          \tag{31}
\]

Its determinant is nonzero because the four-wedge \(P\) is nonzero.
Its divisor, denoted \(\kappa\), has degree

\[
\begin{aligned}
 \deg\kappa
 &=\deg(W/L)+2\deg\Omega-\deg L\\
 &=3d-12-2\delta.                                          \tag{32}
\end{aligned}
\]

Write the scalar-gcd decomposition in (25) as

\[
                         P=C_6\,g\,\widetilde Q.            \tag{33}
\]

If \(s=\deg g\), then \(s+d\leq6\). Locally choose a frame of \(L\)
and write \(E,O\) in that frame with coefficient determinant \(D\).
The ordinary derivative-wedge calculation gives, up to a local unit,

\[
                         P=D^2\kappa\,\widetilde Q.          \tag{34}
\]

At a moving root where \(g\) does not vanish, the scalar on the
right side of (33) has order exactly one. Equation (34) then forces
\(\kappa\), rather than the square \(D^2\), to vanish there. The
polynomial \(g\) can vanish at at most

\[
                         s\leq6-d
\]

of the six distinct moving roots. Consequently \(\kappa\) has at least
\(d\) distinct zeros. Combining this with (32) gives

\[
                         3d-12-2\delta\geq d.               \tag{35}
\]

Since \(d\leq6\), equation (35) forces

\[
                         \boxed{d=6,\qquad\delta=0.}         \tag{36}
\]

In particular \(g\) is constant, \(\kappa\) has exactly the six moving
roots, and the only generic tangent-rank-two splitting types are

\[
                              (2,4),\qquad(3,3).             \tag{37}
\]

The two vector polynomials \(E,O\) have degree at most four and lie in
\(L\). They therefore give a generically injective bundle map

\[
                         {\cal O}(-4)^2\longrightarrow L.   \tag{38}
\]

Both sides have degree \(-8\) by (30) and (36). A torsion cokernel would
increase the degree of the target, so (38) is an isomorphism:

\[
                              L\simeq{\cal O}(-4)^2.         \tag{39}
\]

Thus \(E,O\) are a global frame of \(L\), the square \(D^2\) in (34)
is a nonzero constant, and the surviving rank-two branch has the exact
sequence

\[
 0\longrightarrow{\cal O}(-4)^2\longrightarrow W
 \longrightarrow{\cal A}^*\otimes\Omega\longrightarrow0.  \tag{40}
\]

The induced derivative map (31) consequently has one of the two
homogeneous matrix forms

\[
\begin{array}{c|c|c}
(\alpha,\beta)&W/L&(W/L)\otimes\Omega\\ \hline
(2,4)&{\cal O}\oplus{\cal O}(2)&{\cal O}(-2)\oplus{\cal O}\\
(3,3)&{\cal O}(1)^2&{\cal O}(-1)^2 .
\end{array}                                                \tag{41}
\]

Relative to the frame (39), its rows consist respectively of
quadratic/quartic entries or two rows of cubic entries, and its
determinant is the squarefree sextic \(C_6\), up to scale.

This does not by itself exclude either type in (37).

## 7. The identically zero four-wedge is impossible

It remains to audit the first alternative after (24). Suppose

\[
                         E\wedge O\wedge E'\wedge O'=0.     \tag{42}
\]

The proportional-point branch would make the primitive six-space even
or odd; the even and odd degree-nine systems each have dimension at
most five, and the odd one also has the common factor \(z\). A constant
line \(\langle E,O\rangle\) would put all six coordinate polynomials in
a fixed two-space. Both branches are impossible.

Otherwise the nonconstant line curve

\[
                  \ell(t)=\langle E(t),O(t)\rangle
                         \subset\mathbb P^5                 \tag{43}
\]

is developable. Its actual Pluecker degree is at most eight, including
every scalar gcd and degree drop at infinity. The standard
characteristic-zero classification leaves a cone or the tangent-line
curve of a nonconstant edge.

### 7.1 The cone

In the cone branch, projection away from the fixed vertex gives a
direction curve spanning \(\mathbb P^4\); a smaller span would give a
constant relation among the six basis polynomials. Let its degree be
\(e\). The Pluecker degree of the cone lines is also \(e\), and
nondegeneracy gives \(e\geq4\).

The degree-nine point section \(F(z)\), after the square cover
\(t=z^2\), has a nonzero projection

\[
                         {\cal O}(-9)\longrightarrow
                         {\cal O}(-2e).                     \tag{44}
\]

Thus \(2e\leq9\), forcing \(e=4\). The direction is the rational normal
quartic, so after a constant target change the common six-space contains

\[
                         A(z)\mathbb C[z^2]_{\leq4},        \tag{45}
\]

where \(A\ne0\) has degree at most one. If \(A(0)\ne0\), the five-space
in (45) has local orders \(0,2,4,6,8\). Inserting one further independent
section gives Wronskian weight at least that of

\[
                         (0,1,2,4,6,8),
\]

namely six. If \(A(0)=0\), the five orders are \(1,3,5,7,9\);
the minimum completed sequence is

\[
                         (0,1,3,5,7,9),
\]

of weight ten. Either way the Wronskian vanishes at \(z=0\), an unlisted
point. This contradicts saturation.

### 7.2 Tangent lines

In the tangent branch, the edge spans \(\mathbb P^5\). Let \(e\) be its
degree, \(d\leq8\) the actual Pluecker degree of its tangent-line curve,
and

\[
                         R_1=\sum_x(a_1(x)-1)
\]

its total first ramification. Cancellation of the tangent-wedge base
divisor gives

\[
                         d=2e-2-R_1.                        \tag{46}
\]

The total ramification of a nondegenerate \(g^5_e\) is \(6(e-5)\).
Each unit of \(R_1\) raises at least the last five vanishing orders, so

\[
                         5R_1\leq6(e-5).                    \tag{47}
\]

Equations (46)--(47), \(e\geq5\), and \(d\leq8\) leave only

\[
                         (e,d,R_1)=(5,8,0).                 \tag{48}
\]

The edge is therefore the rational normal quintic. In binary coordinates
every degree-at-most-nine section of its square-pulled tangent lines is

\[
              (X+tY)^4\bigl(A(z)X+B(z)Y\bigr),\qquad
              t=z^2,\quad\deg A,\deg B\leq1.               \tag{49}
\]

Writing \(A=a_0+a_1z\) and \(B=b_0+b_1z\), the exact six-coordinate
Wronskian has the form

\[
  \operatorname {Wr}=141557760\,z^6
       (a_0b_1-a_1b_0)\,H(z),                              \tag{50}
\]

where \(H\) is a polynomial of generic degree twelve. Its degree is at
most twelve and may drop after
specialization, but it cannot vanish identically when
\(a_0b_1-a_1b_0\ne0\): a constant relation would have the form
\(A(z)P(z^2)+B(z)Q(z^2)=0\), and its even and odd parts give an
invertible two-by-two system for \(P,Q\). If
\(a_0b_1-a_1b_0=0\), the six coordinate polynomials are
dependent and cannot be a basis of \({\cal K}\). Otherwise (50) gives
Wronskian weight at least six at the unlisted point \(z=0\), again
contradicting saturation.

Thus (42) is impossible. The residual four-wedge in (25) is nonzero,
and the only remaining branches are the primitive Grassmannian
splittings in (27), narrowed in generic tangent rank two to (37).

## 8. Exact executable audit

[verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation.py)
checks both profiles on all six equality splits, every dimension and
Wronskian count, the cleared Robin orientation, the \(16i^2\) coefficient
minor and Vandermonde, the exact Wronskian (19)--(20), the regular-unit
third-jet implication, the parity-degree optimization, and the complete
splitting ledger (27). It also checks the two bundle-degree formulas
(30), (32), the scalar-gcd root accounting, and the unique surviving
rank-two pair (36), including the homogeneous matrix ledger (39)--(41).
It also enumerates every cone and tangent degree, computes both cone
vanishing-sequence weights, and reconstructs the exact \(z^6\) factor
in (50) with arbitrary linear \(A,B\).

The
[independent audit](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation-independent-audit.md)
reconstructs the common lift without importing the primary checker,
classifies the sole cubic-rank exception, checks the bundle degrees and
scalar-gcd root accounting, and independently solves both developable
normal forms through their exact Wronskians.
