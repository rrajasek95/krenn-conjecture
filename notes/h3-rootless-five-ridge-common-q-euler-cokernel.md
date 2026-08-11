# Common-(q) Euler and two-chart identities leave the five ridge sums primitive

## Outcome

In the exact five-ridge response module of commit b7e3dbd, put

\[
 h_v=\operatorname {Haf}
 \left(q_{12112}\big|_{D\setminus\{v\}}\right),
 \qquad D=\{1,2,3,4,5\}.
\]

Adding every literal first- and second-cofactor Euler/incidence identity on
the four-site face (D\setminus\{v\}) does **not** kill any linear
combination of the five (h_v). The conclusion remains true after granting
the strongest possible componentwise identification of the two chart copies.
The resulting integral module has rank (105) in rank (110) and primitive
cokernel

\[
                              \mathbb Z^5.                 \tag{1}
\]

Thus the genuine common-(q) cofactor identities already present in the
rootless construction do not supply the reduced ridge augmentation with
signature

\[
       (\operatorname{ainc},\widehat w,\operatorname{tgt},
         \operatorname{ores})=(-1,0,0,0).                 \tag{2}
\]

This is a primitive counterguard, not a proof that the augmentation cannot
exist. A successful operation must be a new source-resolution/Tor face (or
another nonlinear source identity outside the displayed linear cofactor
module). It is not another Euler expansion or chart Bianchi difference.

## 1. The complete four-site Euler packet

Fix (v), let (F_v=D\setminus\{v\}), and retain all physical labels. For
each edge (e\subset F_v) and perfect matching (M\) of (F_v), set

\[
 H_v=h_v,\qquad
 A_{v,e}=q_e\partial_e h_v,\qquad
 B_{v,M}=q_M.                                             \tag{3}
\]

There are six (A)'s and three (B)'s. Every edge of (K_4(F_v)) lies in
a unique perfect matching (M(e)), so coefficientwise

\[
 A_{v,e}=B_{v,M(e)},\qquad
 \sum_e A_{v,e}=2H_v,\qquad
 \sum_M B_{v,M}=H_v.                                    \tag{4}
\]

The first equality is the literal edge/cofactor incidence; the last two are
the first and second four-site Euler identities. No abstract cofactor is
inserted: the checker reconstructs all three decorated matching monomials
of every (h_v), differentiates them, and verifies (4) term by term.

The response-companion route of b7e3dbd adds, for each matching,

\[
                         -r_v+B_{v,M}.                    \tag{5}
\]

Here (r_v) is the ridge class represented there by (Omega_v). Equations
(4)--(5) are the entire literal (K_4) matching/Euler closure of that
module in the selected fine degree.

## 2. Integral two-chart computation

Make two source-labelled copies, (D) and (L), of

\[
       (r_v,H_v,(A_{v,e})_{e\subset F_v},(B_{v,M})_M),    \tag{6}
\]

so there are (22) coordinates per (v), (110) in total. In each chart
adjoin the three route rows (5), six incidence rows, and both Euler rows in
(4). Then, as a deliberate strengthening, identify **every** corresponding
coordinate in the two charts. This contains the committed literal
two-chart comparison rows; proving survival in this larger quotient is a
valid no-go for their actual submodule.

For each (v), the covector

\[
 \lambda_v(r_v)=1,\qquad \lambda_v(H_v)=3,\qquad
 \lambda_v(A_{v,e})=\lambda_v(B_{v,M})=1                 \tag{7}
\]

on both charts, and zero on the other four faces, annihilates every row.
It reads (-1) on a clean ridge column (-r_v), and (3) on (H_v).
The five (lambda_v) are independent.

This is not just a rational rank count. For each (v), select:

* the three route rows;
* the six edge-to-matching rows;
* the second Euler row;
* the same ten rows in the second chart; and
* the chart difference of (r_v).

These (21) columns have rank (21) in the local rank-(22) module.
Adjoining (-r_v) gives a square matrix of determinant (pm1) (the five
recorded signs are checked exactly). Hence the local cokernel is
torsion-free (mathbb Z), and their direct sum is (1). Globally,

\[
 \operatorname{rank}R=105,\qquad
 \operatorname{rank}(R+\langle-r_v\rangle)=110,
 \qquad
 \operatorname{rank}(R+\langle H_v\rangle)=110.          \tag{8}
\]

In particular

\[
       R_{\mathbb Q}\cap
       \operatorname{span}_{\mathbb Q}\{H_1,\ldots,H_5\}=0. \tag{9}
\]

So neither Euler layer nor any componentwise chart comparison produces the
needed nonzero relation among the five companion sums.

## 3. Common-(q) does not secretly relate the sums

Although the (h_v) arise from the same (q), they are algebraically
independent. This has a short exact specialization proof. Keep only the
five decorated physical edges

\[
                    12,23,34,45,15                       \tag{10}
\]

and set every other edge on (D) to zero. Then

\[
\begin{array}{lll}
 h_1=q_{23}q_{45},&h_2=q_{15}q_{34},&h_3=q_{12}q_{45},\\
 h_4=q_{15}q_{23},&h_5=q_{12}q_{34}.&
\end{array}                                               \tag{11}
\]

The (5\times5) exponent matrix of (11), in the edge order (10), has
determinant (2). The induced torus monomial map is therefore dominant in
characteristic zero. Consequently there is no polynomial identity in the
five aggregate (h_v) caused merely by their sharing (q).

This does not deny the usual Koszul syzygies with (q)-dependent
coefficients; those are identities among expressions already equal to zero
and do not create a constant-coefficient ridge augmentation. A new
source-valid face would have to carry nonzero (lambda_v)-mass and at the
same time have zero target, cap boundary, and ordinary residue. None of the
operations in (4)--(6) does that.

## 4. Scope and next dependency

The result is finite and source-labelled at (h=3), word `12112`, in the
five selected ridge degrees of b7e3dbd. It covers:

1. all three labelled matching routes per deleted site;
2. every first/second (K_4) cofactor incidence and Euler relation;
3. matching switches and their Bianchi differences; and
4. more than the known two-chart rows, by quotienting componentwise.

It does not compute the full nonlinear source resolution and does not rule
out the third-cofactor/higher-Tor face isolated by the pure-unary cofactor
tower. The proof-completing rootless dependency is therefore now precise:
construct a genuinely new source-labelled relative face with nonzero value
under (7), or prove that the full source resolution contains no such face.
The existing common-(q) Euler and two-chart identities cannot be renamed
as that construction.

## Verification

Run

~~~text
python3 computations/verify_h3_rootless_five_ridge_common_q_euler_cokernel.py
python3 -O computations/verify_h3_rootless_five_ridge_common_q_euler_cokernel.py
~~~

The checker pins b7e3dbd's ridge-companion module, the cofactor-tower
attachment, the full-nine connecting-class rigidity, the ordinary-residue
lock, and the one-Koszul-cell no-go. It verifies every decorated polynomial
identity in (4), the five-cycle determinant, the complete doubled integral
matrix, the five primitive covectors, and five local unimodular
determinants. Its frozen ledger digest is

~~~text
2d614b0889a3a76f1786bb31e699fa2fd3574df75ce74a9e86eec41715da5aae
~~~
