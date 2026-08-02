# The rank-\((1,1)\) coordinate gate enters the one-bright cofactor

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Continue with a maximal \(b=3\), rank-\((1,1)\) shore

\[
 W=A\sqcup B,\qquad |B|=3,\qquad
 p_j^A=\lambda_jU,\qquad s_j^A=\mu_jV.                    \tag{1}
\]

Suppose the left coordinate gate occurs, say \(\lambda=e_i\).  Choose

\[
 x_i=0,\qquad \mu^{\mathsf T}y=0,\qquad
 x(\tau)=x+\tau e_i,\qquad
 K_\tau=x(\tau)y^{\mathsf T}.                              \tag{2}
\]

At \(\tau=0\), \(K_0\) lies in the clean double-annihilator plane but
misses the \(i\)-th diagonal activity coordinate.  For \(\tau\ne0\), the
same line can activate that coordinate.

Because \(S_A(y)=0\), write

\[
 L_\tau=P(x(\tau)),\qquad R=S_B(y).
\]

The response factors literally as

\[
                         r_\tau=L_\tau R.                   \tag{3}
\]

Since \(R\) is supported on three sites,

\[
 r_\tau^{[j]}=j!\,L_\tau^{[j]}R^{[j]},
 \qquad r_\tau^{[j]}=0\quad(j\ge4).                         \tag{4}
\]

Thus the entire homogeneous clean error on this normal line has only two
terms:

\[
\begin{aligned}
{\cal E}(K_\tau)
={}&2\sigma(K_\tau)^{h-2}q^{[h-2]}
            L_\tau^{[2]}R^{[2]}\\
 &+6\sigma(K_\tau)^{h-3}q^{[h-3]}
            L_\tau^{[3]}R^{[3]}.
\end{aligned}                                               \tag{5}
\]

At \(\tau=0\), both \(L_0=P_B(x)\) and \(R\) are supported on \(B\), so
\({\cal E}(K_0)=0\).  Its exact first normal derivative is

\[
\boxed{
 \frac{d}{d\tau}{\cal E}(K_\tau)\bigg|_{\tau=0}
 =2\sigma(K_0)^{h-2}
   \bigl(Uq_A^{[h-2]}\bigr)
   \otimes
   \bigl(P_B(x)S_B(y)^{[2]}\bigr).}                         \tag{6}
\]

There is no hidden derivative of the direct scalar in (6): it multiplies
the already-zero error at \(\tau=0\).  The cubic-response term begins at
order three because its three right factors consume all of \(B\), forcing
all three left factors onto \(A\).

Equation (6) turns the fixed-coordinate residue into the literal
one-bright data already isolated on the endpoint-dark branch.  The
inactive clean plane has a simple transverse clean-error zero whenever all
three factors

\[
 \sigma(K_0),\qquad Uq_A^{[h-2]},\qquad
 P_B(x)S_B(y)^{[2]}                                        \tag{7}
\]

are nonzero.  If the first normal vanishes, it does so for one of these
source-visible reasons, not by cancellation among unrelated error terms.
The endpoint-transposed statement handles \(\mu\parallel e_i\).

This does not close the coordinate gate: a nonzero first derivative rules
out only a higher-multiplicity contact at the inactive member, not a
second clean point elsewhere on the normal line.  Formula (5) is the exact
bounded polynomial which remains.  A closure can now couple its quadratic
and cubic response terms to the complete one-bright four-site rows rather
than analyzing an unrestricted clean error.

## Exact derivation

For any commuting site-square-zero elements \(L,R\),

\[
 (LR)^{[j]}=\frac{L^jR^j}{j!}
            =j!\,L^{[j]}R^{[j]}.
\]

This proves (4) and hence (5).  Differentiate (5) at zero.  Every term
containing \(r_0^{[2]}\) vanishes because a quadratic supported on three
sites has square zero.  The only surviving derivative is

\[
 \sigma(K_0)^{h-2}q^{[h-2]}
       \bigl(r_0\,\dot r_0\bigr).
\]

Here

\[
 r_0=P_B(x)S_B(y),\qquad
 \dot r_0=P(e_i)S_B(y).
\]

The two copies of \(S_B(y)\) consume two sites of \(B\), while \(P_B(x)\)
consumes the third.  Therefore only the shore part \(U=P_A(e_i)\) of the
remaining left star survives, and every factor of \(q^{[h-2]}\) lies in
\(A\).  Since \(S_B(y)^2=2S_B(y)^{[2]}\), this is exactly (6).

## Exact audit

The standard-library checker
[verify_rank_one_rank_one_coordinate_gate_first_normal_cofactor.py](../computations/verify_rank_one_rank_one_coordinate_gate_first_normal_cofactor.py)
reconstructs the site-square-zero algebra over exact rationals.  It
interpolates the full degree-at-most-\(h\) clean-error polynomial from
\(h+1\) exact values and independently compares its linear coefficient
with (6).  All three physical coordinate gates, \(h=3,4,5\), and 81
deterministic rational specializations pass; every audited first normal is
nonzero.  One aggregate SHA-256 digest pins the complete ledger.  The
checker passes normally, with -O, and with -I -S.
