# The fixed dark plane survives two complete one-site jets

Research progress and a sharp negative guard only.  The complement-plane
alternative is already closed by
[`n8-rank11-scalar-fixed-plane-provenance-closure.md`](n8-rank11-scalar-fixed-plane-provenance-closure.md).
This note proves that the remaining fixed **dark** plane cannot be closed
from separate released-shore-site data, even after retaining two complete
nine-row contractions and the genuine consecutive powers of one six-site
quadratic.  The first joint five-site contraction does detect the packet.
Krenn's conjecture and `SP-CLEAN-BRIDGE` remain open.

## 1. Exact residual blocker census

Let the maximal dark shore be \(A=\{x,y,z\}\), and for each target colour
put

\[
 Z_c=\{u\in A:e_c^{(u)}\in\operatorname {span}(U_u,V_u)\}.
\tag{1}
\]

The preceding released-site theorem has already proved two facts.

1. Some site belongs to exactly two of the \(Z_c\)'s, or the coordinate
   plane occurs on the physical complement.  The latter branch is closed.
2. A release \(u\) with two live labels is also on the closed complement
   branch.  A label is live after releasing \(u\) exactly when
   \(Z_c=\varnothing\) or \(Z_c=\{u\}\).

Thus the fixed-dark-plane residue is described by

\[
 \max_u\#\{c:u\in Z_c\}=2,
 \qquad
 \#\{c:Z_c\in\{\varnothing,\{u\}\}\}\le1
 \quad(u=x,y,z).
\tag{2}
\]

There are \(189\) labelled ledgers and exactly \(11\) orbits under
\(S_3(A)\times S_3(\text{colours})\).  Writing a subset by its site digits,
canonical representatives and orbit sizes are

\[
\begin{array}{c|c}
(\varnothing,01,01)&9\\
(\varnothing,01,02)&18\\
(\varnothing,01,012)&18\\
(\varnothing,012,012)&3\\
(0,1,01)&18\\
(0,1,02)&36\\
(0,1,012)&18\\
(0,01,12)&36\\
(0,12,12)&9\\
(0,12,012)&18\\
(01,02,12)&6.
\end{array}
\tag{3}
\]

This is not an eleven-case proof program.  It records the exact quantifier
left after the complement closure: every remaining one-site jet has at most
one fixed target label.

## 2. Cap-plane contraction of the one-site rows

On the rank-\((1,1)\) shore write

\[
 p_i^A=\lambda_iU,\qquad s_j^A=\mu_jV,
 \qquad
 {\cal Q}=\{K:\lambda^{\mathsf T}K=0, K\mu=0\}.
\tag{4}
\]

Leave \(x\in A\) uncontracted and contract the other dark sites by a
coefficient \(\theta\).  In the notation of equations (60)--(63) of
[`endpoint-dark-shore-consecutive-power-jet.md`](endpoint-dark-shore-consecutive-power-jet.md),
write

\[
 E_x(\theta)=H_x(\theta)+T_x(\theta),
 \qquad T_x(\theta)\in V_x\otimes({\cal R}_B)_1.
\tag{5}
\]

Multiply the nine one-site rows by \(K_{ij}\) and sum.  The direct term
vanishes on \({\cal Q}\).  Both terms containing the local endpoint fields
vanish separately by the two annihilator equations in (4).  Therefore the
complete cap-plane contraction is

\[
 \boxed{
 R_KT_x(\theta)=
   \sum_{c=0}^2 K_{cc}\,
       \beta_{A\setminus\{x\},c}(\theta)
       e_c^{(x)}X_c^B,
 \qquad R_K=P_B^{\mathsf T}KS_B.}
\tag{6}
\]

In particular a target-free cap satisfies \(R_KT_x(\theta)=0\).  It is
tempting to infer \(R_K=0\), which would kill the scalar provenance
quotient.  The following packet proves that implication false even when
all the data before (6) are restored.

The corresponding two-site expansion identifies in advance what a joint
coefficient can add.  Leave \(x,y\) visible, contract the rest of the dark
shore, and decompose the resulting cubic cofactor by its intersection with
\(\{x,y\}\):

\[
 E_{xy}=H+T_x+T_y+T_{xy},
\quad
 H\in({\cal R}_B)_3,
\quad
 T_x\in V_x\otimes({\cal R}_B)_2,
\quad
 T_y\in V_y\otimes({\cal R}_B)_2.
\tag{6a}
\]

The last component lies in
\(V_x\otimes V_y\otimes({\cal R}_B)_1\).  Expanding the endpoint product
with

\[
 p_i^{Bxy}=p_i^B+\lambda_i(U_x+U_y),\qquad
 s_j^{Bxy}=s_j^B+\mu_j(V_x+V_y),
\]

and deleting every repeated-site term gives the exact identity

\[
\begin{aligned}
 p_i^{Bxy}s_j^{Bxy}E_{xy}
={}&p_i^Bs_j^BT_{xy}\\
 &+\lambda_i\bigl(U_xs_j^BT_y+U_ys_j^BT_x\bigr)\\
 &+\mu_j\bigl(p_i^BV_xT_y+p_i^BV_yT_x\bigr)\\
 &+\lambda_i\mu_j
       \bigl(U_xV_y+U_yV_x\bigr)H.
\end{aligned}
\tag{6b}
\]

The last line is the only term which uses newly exposed endpoint fields at
both sites.  Contracting either \(x\) or \(y\) by a dark covector kills it,
while summing over \(K\in{\cal Q}\) kills its response-label matrix by
\(\lambda^{\mathsf T}K\mu=0\).  Thus separate one-site rows and the joint
cap-plane contraction are structurally blind to precisely this scalar
normal term.  An individually labelled joint row is the first place it can
be forced to vanish.

## 3. A rational full-row survivor

Use residual sites

\[
 B=\{0,1,2\},\qquad A=\{x,y,z\}.
\]

At the dark sites take

\[
\begin{array}{c|ccc}
 &x&y&z\\ \hline
 U&e_1&e_1&e_2\\
 V&e_2&e_1&e_2.
\end{array}
\tag{7}
\]

Thus \(\operatorname {span}(U_x,V_x)=\Pi_0\).  The blocker ledger is

\[
                  (Z_0,Z_1,Z_2)=(\varnothing,\{x,y\},\{x,z\}),
\tag{8}
\]

the second orbit in (3).  Contract \(y,z\) by their \(e_0\)-covectors.
Put

\[
 \lambda=(1,1,-1),\qquad \mu=(1,-1,-1).
\tag{9}
\]

On \(B\), with `site:colour` notation, define

\[
\begin{aligned}
 L_0&=0{:}0+1{:}2+2{:}1,&
 L_1&=1{:}2+2{:}0,\\
 M_0&=1{:}1+1{:}2+2{:}0,&
 M_1&=1{:}0,\\
 t&=1{:}0-1{:}1-1{:}2+2{:}0.
\end{aligned}
\tag{10}
\]

Take

\[
 p^B=(L_0,L_1,0),\qquad s^B=(0,M_0,M_1),
 \qquad a=e_0\mu^{\mathsf T}.
\tag{11}
\]

The two annihilator bases may be chosen as

\[
 h_0=(1,0,1),\quad h_1=(0,1,1),
 \qquad
 g_0=(1,1,0),\quad g_1=(1,0,1).
\tag{12}
\]

They satisfy \(\lambda^{\mathsf T}h_r=0\),
\(\mu^{\mathsf T}g_s=0\), and their four physical responses are the
linearly independent quadratics

\[
                  C_{rs}=L_rM_s\qquad(0\le r,s\le1).
\tag{13}
\]

Direct multiplication gives

\[
 C_{00}t=X_0^B,qquad C_{01}t=X_0^B,qquad
 C_{10}t=C_{11}t=0.
\tag{14}
\]

The diagonal map on the cap plane has rank three.  Its kernel is generated,
in the ordered basis \((00,01,10,11)\), by

\[
                         (-1,1,0,-1).
\tag{15}
\]

Hence

\[
 R_*=-C_{00}+C_{01}-C_{11}\ne0,
 \qquad R_*t=0.
\tag{16}
\]

This already keeps the nonzero scalar provenance class.  The next section
checks that it is not an artefact of independent \(E_x,F_x\).

## 4. Genuine consecutive powers and all nine rows

Let

\[
 q_C=L_0M_1
\tag{17}
\]

on \(B\), and define one actual six-site quadratic

\[
             q=q_C+(y{:}0)(x{:}0)+(z{:}0)t.
\tag{18}
\]

Literal matching separation gives

\[
\begin{aligned}
 E_x&=\iota_{y{:}0}\iota_{z{:}0}q^{[2]}
       =(x{:}0)t,\\
 F_x&=\iota_{y{:}0}\iota_{z{:}0}q^{[3]}
       =(x{:}0)tq_C
       =(x{:}0)X_0^B.
\end{aligned}
\tag{19}
\]

Thus (19) is exactly the common-power form
\(E_x=dq_C+r_yr_z,\ F_x=dq_C^{[2]}+r_yr_zq_C\), with

\[
 d=0,\qquad r_y=x{:}0,\qquad r_z=t.
\tag{20}
\]

On \(C_x=B\cup\{x\}\), restore the local endpoint pieces

\[
 p_i^{C_x}=p_i^B+\lambda_i(x{:}1),qquad
 s_j^{C_x}=s_j^B+\mu_j(x{:}2).
\tag{21}
\]

Because \(E_x\) already uses \(x\), every local endpoint term in (21)
collides.  Equations (11), (14), and (19) now give all nine literal rows

\[
 a_{ij}F_x+p_i^{C_x}s_j^{C_x}E_x
 =\delta_{i0}\delta_{j0}X_0^{C_x}.
\tag{22}
\]

The complete endpoint maps on all six sites have rank three, the direct
functional \(a\) annihilates the whole cap plane, the response family has
dimension four, and (16) survives.  No localization, finite-field
specialization, independently assigned cofactor, or omitted one-site row
is involved.

There is a further exact strengthening.  Contracting \(x,z\) by their
\(e_0\)-covectors instead leaves \(y\) visible, and the same global
\((q,p,s,a)\) satisfies all nine rows again.  Thus the packet passes two
distinct complete one-site jets, eighteen rows in total.  It is not a
global packet: the release of \(z\) has six residual rows.  More
importantly, contract only \(z\), leaving \(x,y\) simultaneously visible.
Then all nine five-site rows have nonzero two-term residuals.  The first
new information is therefore exactly the joint two-site coefficient, not
another separate one-site contraction.

The residual is even sharper.  Put

\[
 W=X_0^B\bigl((x{:}1)(y{:}1)+(x{:}2)(y{:}1)\bigr).
\tag{23}
\]

For every response label its joint-row error is

\[
                        {\mathscr R}_{ij}=\lambda_i\mu_jW.
\tag{24}
\]

Thus the complete error matrix is the single scalar-shore normal
\(\lambda\mu^{\mathsf T}\) tensored with \(W\).  Every cap
\(K\in{\cal Q}\) annihilates it:

\[
          \sum_{i,j}K_{ij}{\mathscr R}_{ij}
             =(\lambda^{\mathsf T}K\mu)W=0.
\tag{25}
\]

In particular the nonzero target-free response in (16) still obeys the
joint cap equation \(R_*E_{xy}=0\).  The five-site obstruction is visible
only before summing the labelled rows over the clean cap plane.

There is a second sharp equality which prevents overinterpreting that
obstruction.  The complete dark coefficient space is

\[
 \mathcal K_A=\langle e_0^*\rangle_X\otimes
   \langle e_0^*,e_2^*\rangle_Y\otimes
   \langle e_0^*,e_1^*\rangle_Z,
 \qquad \dim\mathcal K_A=4.                                \tag{26}
\]

On its four coordinate tensors, the genuine maps
\(E_A=\iota_Aq^{[2]}\) and \(F_A=\iota_Aq^{[3]}\) are nonzero only at
\(e_0^*\otimes e_0^*\otimes e_0^*\).  The fixed-target map \(\beta_A\)
has exactly the same support.  Consequently

\[
 \operatorname {rank}E_A=operatorname {rank}F_A
 =\operatorname {rank}\beta_A=1,
 \qquad \ker E_A=\ker\beta_A,\quad\dim\ker E_A=3.          \tag{27}
\]

Thus the packet attains equality in the dark-shore kernel theorem.  The
joint labelled carrier detects that this particular \(q\) cannot extend,
but it does not by itself construct a coefficient in
\(\ker E_A\setminus\ker\beta_A\).

There is a further exact all-inactive boundary inside the cap plane.  For
\(K\in\mathcal Q\), put

\[
 \mathscr S(K)=R_Kq^{[2]}-\sum_{i=0}^2K_{ii}X_i.
\tag{28}
\]

In the ordered basis \((h_0g_0^{\mathsf T},h_0g_1^{\mathsf T},
h_1g_0^{\mathsf T},h_1g_1^{\mathsf T})\), the map
\(\mathscr S:\mathcal Q\to\mathcal R_6\) has rank two and

\[
 \ker\mathscr S=
 \left\langle
   h_0g_0^{\mathsf T},
   -h_0g_0^{\mathsf T}+h_0g_1^{\mathsf T}-h_1g_1^{\mathsf T}
 \right\rangle .                                           \tag{29}
\]

The first generator has diagonal \((1,0,0)\); the second is the
target-free \(K_*\) of (15).  This is the **contracted source-row
residual**, not the canonical clean error of the descent theorem.

The actual distinction is stronger.  The direct functional \(a\) vanishes
on all of \(\mathcal Q\), so at \(h=3\) the canonical homogeneous clean
error is

\[
                       \mathcal E_{p,q}(K)=R_K^{[3]}.       \tag{30}
\]

Every one of the twenty polarized triple products of the four basis
responses \(C_{rs}\) in (13) is zero in the site-square-zero algebra.
Therefore

\[
              \boxed{\mathcal E_{p,q}|_{\mathcal Q}=0.}    \tag{31}
\]

The entire four-dimensional vector cap plane, or projective three-space,
is canonically clean and every point is inactive because \(a|_{\mathcal
Q}=0\).  The packet therefore does not merely preserve one target-free
response: it realizes an exact inactive clean plane.  The missing overlap
theorem must leave this scalar plane, force a source contradiction/descent,
or produce activity on another chart; existence of another clean cap in
\(\mathcal Q\) is vacuous.

## 5. Proof impact and exact scope

The fixed dark plane is **not** another branch on which a one-site
assignment-sum row should be sought.  Equations (6) and (22) show that two
complete one-site packets can remain rank-one aligned while a nonzero
target-free response survives.

The next nonredundant theorem is therefore the **labelled joint five-site**
compatibility of two released dark sites, or an equivalent two-chart row
which compares their two common-power factorizations.  Merely imposing two
separate contractions of the same global \(q\) is still insufficient, and
even the joint cap-plane contraction loses the class by (25).  A positive
theorem must use an individual labelled coefficient in which both sites
remain visible, or the original source-labelled overlap which supplies
that comparison.  By (31), its conclusion must be activity, a source
contradiction, or descent; a clean point alone already exists on the guard.

That labelled coefficient has now been evaluated exactly in
[`n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md`](n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md).
All three natural 24-coordinate completion fibres have ordinary units using
at most three labelled rows.  With all 135 \(q\)-cells restored, each cut
leaves twelve pure-zero matching carriers, together with a small explicit
mixed ledger.  Thus the next theorem is no longer the existence
of a joint detector; it is the source-minimal/two-chart routing of these
three overlapping carrier ledgers.

This packet is **not** a six-site source and not a counterexample to the
conjecture.  Only the two displayed one-site contractions are claimed; the
joint five-site coefficient already fails.  Its role is to rule out the
proposed separate-one-site closure at the strongest honest local scope and
to locate the first missing coefficient exactly.

## 6. Exact audit

[`verify_n8_rank11_scalar_dark_plane_one_site_guard.py`](../computations/verify_n8_rank11_scalar_dark_plane_one_site_guard.py)
uses exact `Fraction` arithmetic in the full six-site square-zero algebra.
It reconstructs \(q^{[2]},q^{[3]}\), both sets of nine one-site rows, the
joint five-site residual, its factorization (24), the cap invisibility
(25), the endpoint and response ranks, the rank-three diagonal map, and the
nonzero kernel response (16).  It also exhausts all
\(8^3=512\) blocker triples, retaining
the \(189\) admissible labelled ledgers and their eleven symmetry
orbits.  It finally separates the linear cap-row residual (28) from the
canonical cubic clean error (30), verifies all twenty polarized cubic
products, and proves the inactive clean plane (31).  The deterministic ledger
digest is

```text
44ce6b13ef9cd36a95aeb963bf812bb183996c5125436d98ba8779bbd7243e24
```
