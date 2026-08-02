# The higher Koszul row supplies the missing chain in the formal jet cone

Research construction only.  The construction below is exact in a selected
principal-parts/endpoint-jet symbol complex.  It does not yet descend that
complex to the physical EqSystem, construct the second chart, or prove
Krenn's conjecture.

## 1. Outcome

Let

\[
 K_m^{\rm phys}=u r_m+H_mr_0-H_0r_m,
 \qquad m=01211222,                                      \tag{1}
\]

be the verified two-row physical Koszul cell.  For every deleted internal
site \(v\in\{1,2,3,4,5\}\), the Reynolds operator followed by the minimal
direct endpoint-\((22\to00)\) operator selects

\[
 (H_mr_0-H_0r_m)\longmapsto r_0.                        \tag{2}
\]

Call this selected pure-row symbol \(s_v\).  It is closed in the selected
symbol complex: since \(d_{\rm Eq}r_0=H_0-u\), the same exact selector gives

\[
                         d s_v=\Psi_v(H_0-u)=0.          \tag{3}
\]

Now take the split cap block

\[
 dT_v=-Y_0w_v,\qquad d\rho_v=w_v,
 \qquad
 \begin{array}{c|cc}
       &\operatorname {tgt}&\operatorname {ores}\\ \hline
 T_v   &1&0\\
 \rho_v&0&1
 \end{array}.                                           \tag{4}
\]

Define the **formal selected jet/cap direct sum** by adjoining \(s_v\) with

\[
 ds_v=0,\qquad
 (\operatorname {tgt},\operatorname {ores})(s_v)=(1,0). \tag{5}
\]

Here the ordinary-residue value in (5) is structural only inside this
definition: ordinary residue is the cap response projection, extended by
zero on the formal Eq-symbol summand.  It is not a claim that the physical
ordinary-residue map has already been extended through principal parts.

The missing chain is then forced, including its sign:

\[
 \boxed{n_v=s_v-T_v},\qquad
 dn_v=Y_0w_v,qquad
 \operatorname {tgt}(n_v)=\operatorname {ores}(n_v)=0. \tag{6}
\]

Thus \(\kappa n_v\) has boundary \(\kappa Y_0w_v\).  Moreover

\[
 z_v=\kappa(n_v-Y_0\rho_v)
     =\kappa(s_v-T_v-Y_0\rho_v)                         \tag{7}
\]

is a target-zero cycle with ordinary response \(-\kappa Y_0\).  Equations
(6)--(7) derive the desired response from the higher Koszul row and the old
cap differential; they do not assume a new chain with prescribed coordinate
\((\kappa Y_0,0,0)\).

This is the first positive combined assembly in the finite formal model.  Its
remaining obstruction is equally explicit: the selector is a genuine
second-order differential operator, not an \(R\)-linear map.  Therefore
\(s_v\), and hence (6), has not yet been promoted from a selected jet symbol
to a physical chain.

## 2. Exact Reynolds and endpoint operators

Put \(D=\{1,2,3,4,5\}\) and \(F_v=D\setminus\{v\}\).  If \(e,f\) are the
two coloured edge variables of a perfect matching of \(F_v\), define

\[
 L_v={1\over3}\sum_{\{e,f\}\in\operatorname {PM}(F_v)}
                   \partial_e\partial_f.                \tag{8}
\]

For the four-site complement hafnian \(C_v^m\), matching factorization gives

\[
 L_v(H_m)=C_v^m,\qquad L_v(H_0)=0.                      \tag{9}
\]

Write the direct mixed and pure endpoint variables as

\[
 \widetilde u_v=a_{xv}^{0m_v},\quad
 \widetilde t=a_{pq}^{22},\quad
 u_v=a_{xv}^{00},\quad t=a_{pq}^{00}.                  \tag{10}
\]

The minimal direct-sector endpoint bridge is

\[
 E_v=M_{u_vt}\partial_{\widetilde u_v}
                    \partial_{\widetilde t}.            \tag{11}
\]

The \(pq\)-direct term of \(C_v^m\) is uniquely
\(\widetilde u_v\widetilde t\).  The other two complement matchings are
endpoint-star terms, so exact expansion gives

\[
 E_v(C_v^m)=u_vt,qquad
 \partial_{u_v}\partial_tE_v(C_v^m)=1.                \tag{12}
\]

Consequently

\[
 \Psi_v=\partial_{u_v}\partial_tE_vL_v,qquad
 \Psi_v(H_m)=1,\quad\Psi_v(H_0)=\Psi_v(u)=0,           \tag{13}
\]

which proves (2) coefficientwise.  Equation (11) is the direct polynomial
shadow of the endpoint-\((22\to00)\) curvature side.  It is not yet the
full side: its \(pr\)-chart mate and their chart-difference boundary have
not been constructed.

## 3. The exact Leibniz commutators

The Reynolds operator obeys

\[
 L_v(AB)=L_v(A)B+A L_v(B)+\Gamma_v(A,B),                \tag{14}
\]

where

\[
 \Gamma_v(A,B)={1\over3}\sum_{\{e,f\}}
 \left((\partial_eA)(\partial_fB)
       +(\partial_fA)(\partial_eB)\right).              \tag{15}
\]

Similarly,

\[
 \begin{split}
 E_v(AB)={}&E_v(A)B+A E_v(B)\\
 &+u_vt\left((\partial_{\widetilde u_v}A)
                 (\partial_{\widetilde t}B)
             +(\partial_{\widetilde t}A)
                 (\partial_{\widetilde u_v}B)\right).
 \end{split}                                            \tag{16}
\]

These correction terms are not bookkeeping artifacts.  For either matching
\(\{e,f\}\) occurring in (8),

\[
 L_v(e)=L_v(f)=0,\qquad L_v(ef)=\frac13.                \tag{17}
\]

At the endpoints,

\[
 E_v(\widetilde u_v)=E_v(\widetilde t)=0,
 \qquad E_v(\widetilde u_v\widetilde t)=u_vt.           \tag{18}
\]

The composite itself has the even sharper witness

\[
                         \Psi_v(1)=0,\qquad\Psi_v(H_m)=1. \tag{19}
\]

Thus \(\Psi_v\) cannot be an \(R\)-linear map on the original coefficient
module: \(R\)-linearity would make the second value in (19) equal to
\(H_m\Psi_v(1)=0\).  Formulas (15)--(16) are the first nonzero Taylor
components that a principal-parts, Hasse--Schmidt, or \(A_\infty\)
comparison must absorb.

## 4. Signs, homological degree, and fine degree

In the presentation convention, both the Eq row \(r_0\) and the cap
generator \(T_v\) lie in homological degree one.  The coefficient selector
does not change that row degree, so the subtraction in (6) is typed.  Its
boundary sign is not optional:

\[
 d(s_v-T_v)=0-(-Y_0w_v)=+Y_0w_v.                       \tag{20}
\]

For fine degree, let

\[
 \mu(0)=\sum_{i=0}^7e_{i,0},\qquad
 \deg Y_0=\sum_{i=1}^5e_{i,0},\qquad
 \sigma=e_{x,0}+e_{p,0}+e_{q,0}.                       \tag{21}
\]

The selected row has degree \(\deg s_v=\deg r_0=\mu(0)\), while the shifted
cap generator has degree

\[
                    \deg Y_0+\sigma=\mu(0).             \tag{22}
\]

Hence (6) also passes the fine-degree gate.  At the selected-symbol level,
if \(d_Jj_v=y_v\), the proposed attaching components

\[
 \Phi_0(y_v)=Y_0w_v,\qquad \Phi_1(j_v)=s_v-T_v          \tag{23}
\]

satisfy the literal chain equation

\[
                         d\Phi_1(j_v)=\Phi_0d_J(j_v).    \tag{24}
\]

This is an equality in the formal selected-symbol cone, not a declaration of
a physical comparison map.

## 5. Why this does not contradict the same-power target--residue lock

Inside the old cap block, the closed same-power graph generator is

\[
                         g_v=T_v+Y_0\rho_v,              \tag{25}
\]

with

\[
 (\operatorname {tgt},\operatorname {ores})(g_v)=(1,Y_0). \tag{26}
\]

Every old cap cycle is a multiple of \(g_v\).  Since target projection is
injective on this line, no nonzero old cap cycle is both target-zero and
residue-active.  That is the same-power lock.

The new symbol is outside its hypotheses.  It uses the adjacent-power
principal-parts summand \(Rs_v\), not another vector in
\(R\langle T_v,\rho_v\rangle\).  Indeed (7) is simply

\[
                         z_v=\kappa(s_v-g_v).            \tag{27}
\]

The old common graph cancels against a source-provenant selected symbol.  No
linear combination internal to the old cap block has been claimed.

What remains open is precisely whether this escape survives descent.  The
formal assignment \(\operatorname {ores}(s_v)=0\) must be induced by an
actual comparison, and the \(pq\)-direct selected jet must glue to its other
chart without introducing an ordinary-residue or same-power component.  If
either fails, the physical construction can fall back under the lock even
though the formal direct sum does not.

## 6. The remaining mathematical problem

The finite calculation changes the next question.  One no longer needs to
guess the missing cap coordinate: (6) gives its only compatible formal
source, sign, target, and response cancellation.  The needed new mathematics
is to realize that symbol functorially.

Concretely, a successful construction must do all of the following:

1. replace \(L_v\), \(E_v\), and \(\Psi_v\) by an \(R\)-linear map out of an
   actual principal-parts or jet resolution;
2. use the cross terms (15)--(16) as higher Taylor components so that the
   EqSystem differential satisfies the full \(A_\infty\) chain identities;
3. identify the \(pr\)-chart mate of (11) and prove that the chart difference
   has zero target and physical ordinary residue; and
4. show that evaluation from the jet resolution sends the formal class
   \(s_v-T_v\) to a genuine source-provenant chain, rather than killing it or
   adding a same-power graph component.

The first failure is already exact and finite: the product witnesses
(17)--(19) rule out an ordinary \(R\)-linear mapping cone.  They do not rule
out the principal-parts/\(A_\infty\) repair; rather, they specify its first
commutators.

## 7. Exact verification

Run

```sh
.venv/bin/python computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py
```

The dependency-free checker uses exact sparse rational polynomials.  For all
five faces it verifies the two Leibniz identities, the literal nonlinearity
witnesses, the three-term complement hafnian, the unique direct endpoint
term, the values (13), and the closure (3).  It then constructs the formal
four-generator complex, checks (6)--(7), the fine and homological degrees,
and the attaching equation (24).  Its terminal line is

```text
PASS: exact formal higher-Koszul coupling and descent obstruction
```
