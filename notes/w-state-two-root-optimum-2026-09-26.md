# The optimal W-state rate in the two-root architecture at every even site count

September 26, 2026. **Written proof, with exact supporting checks; independent
audit pending. No claim of historical priority or unrestricted colored-core
optimality is made.**

[Illustrated guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/w-state-two-root-2026-09-26/README.md) ·
[Connected-case proof](two-root-w-connected-reduction-2026-09-26.md)

## 1. Statement

Let \(n=2m\ge4\). Choose two root sites. All source entries incident to
either root may be arbitrary complex endpoint-color weights. Edges between
the other \(N=n-2\) sites carry only the ground color \(aa\), with arbitrary
complex weights \(D_{ij}\). The source must have exact nonzero output
\(H=\lambda W_n\), where each single-excitation word has amplitude
\(\lambda\). Write \(S\) for total squared source norm and

\[
 R=\frac{n|\lambda|^2}{S^m},\qquad
 B_n=\frac{((n-1)!!)^2}{\binom{n}{2}^{m}}.
\]

**Theorem.** Without any connectedness, rank, phase, or support assumption,
the exact optimum in this architecture is

\[
 \boxed{R_* =\frac{n B_n}{(n-1)^2+1}.}                    \tag{1}
\]

The complete-core one-root construction attains it. At \(n=2\), the only
source edge is the output tensor itself, so \(R_*=1\), also as in (1).

For \(n\ge6\), an exact W design with a disconnected cofactor graph has
the quantitative gap

\[
 \boxed{R\le\left(1-
    \frac{1}{(m-1)(2m^2-4m+1)}\right)R_*<R_*.}            \tag{2}
\]

Thus every optimal two-root design has a connected cofactor graph. This
does not assert that every optimal design is the same source, or that the
disconnected bound is sharp. At six sites the previously proved \(1/144\)
bound is stronger than (2).

Arbitrary colored cores remain outside this theorem. The result completes
the two-root extension of the one-root optimum, not the optimization over
all matching sources.

## 2. Reduce the remaining task to disconnected cofactor graphs

Define the symmetric zero-diagonal cofactor matrix

\[
 C_{ij}=\operatorname{haf}(D\setminus\{i,j\}),\qquad i\ne j.
\]

The [connected-case theorem](two-root-w-connected-reduction-2026-09-26.md)
replaces any exact W source with connected cofactor graph by a one-root
source of the same output and no greater norm. Its proof includes bipartite
graphs and singular matrices. The argument in its sections 2--3 also applies
when the core has two vertices: \(C_{12}=1\), so it covers \(n=4\).
The [one-root theorem](w-state-optimal-design-2026-09-26.md) then gives (1).

It remains to prove a strict bound for disconnected cofactor graphs when
\(m\ge3\). Projecting onto the two target colors preserves W and decreases
source norm, so additional colors may be discarded first.

As in the connected proof, let \(u,v\) be the two root-ground/core-excited
vectors and \(x,y\) the two root-ground/core-ground vectors. Every core-site
target coefficient satisfies

\[
                  u_i(Cy)_i+v_i(Cx)_i=\lambda.            \tag{3}
\]

Hence no cofactor row is zero. All graph components have sizes \(s_j\ge2\).
Since there are at least two components, each \(s_j\le N-2\).

## 3. A core-dependent rate bound from component responses

Let \(\rho_j>0\) be the operator norm of the cofactor block on component
\(j\), and let \(E_j\) be the squared norm of the restrictions of
\(u,v,x,y\) to that component. Summing absolute values in (3), then using
Cauchy--Schwarz and \(2ab\le a^2+b^2\), gives

\[
 s_j|\lambda|\le\rho_j
   (\|u_j\|\|y_j\|+\|v_j\|\|x_j\|)
                  \le\tfrac12\rho_j E_j.
\]

For \(a=\sum_{i<j}|D_{ij}|^2>0\) and
\(b=2\sum_j s_j/\rho_j\), we obtain

\[
                         S\ge a+b|\lambda|.
\]

The other root-color entries and the direct root edge only add nonnegative
source energy. Maximizing over \(|\lambda|\ge0\), at
\(|\lambda|=2a/((m-2)b)\), yields

\[
 R\le\frac{n(m-2)^{m-2}}
  {m^m a^{m-2}(\sum_j s_j/\rho_j)^2}.                    \tag{4}
\]

This bound can be used for a specified core before introducing the uniform
estimates below. It does not require exact cancellation of the other outputs.

## 4. Bound all cofactor responses together

Put \(T=\sum_{i<j}|C_{ij}|^2\). Hölder's inequality gives

\[
 \left(\sum_j s_j^{2/3}\right)^3
       \le\left(\sum_j s_j/\rho_j\right)^2\sum_j\rho_j^2.
\]

The block operator norms obey \(\sum_j\rho_j^2\le\|C\|_F^2=2T\).
Since every \(s_j\le N-2\),
\(\sum_j s_j^{2/3}\ge N/(N-2)^{1/3}\). Therefore

\[
                 (\sum_j s_j/\rho_j)^2
                       \ge\frac{N^3}{2(N-2)T}.            \tag{5}
\]

The published subhafnian inequality of
[Roos, Theorem 2.3, equations (38) and (40)](https://arxiv.org/html/1906.06176)
gives

\[
 T\le K_N a^{m-2},\qquad
 K_N=\frac{((N-3)!!)^2}{\binom{N}{2}^{m-3}}.             \tag{6}
\]

Indeed, take \(k=m-2\) on the \(N=2m-2\) vertex scalar core and partition
\(k\) into ones. The normalized average squared hafnian of its
\(N-2\) vertex submatrices is at most \((a/\binom N2)^{m-2}\).
There are \(\binom N2\) such submatrices and each normalization factor is
\((N-3)!!\), which gives exactly (6). Complex cancellation is allowed.

Combining (4)--(6),

\[
 R\le U_m:=\frac{2n(N-2)(m-2)^{m-2}K_N}{m^m N^3}.       \tag{7}
\]

## 5. A strict gap at every order

Write \(d=(m-1)(2m-3)>1\). Substituting the definitions of \(K_N,B_n\)
and cancelling the double factorials in (7) gives

\[
 \frac{U_m}{R_*}=
 \frac{m-2}{m-1}
 \left(1+\frac{3m-2}{d}\right)
 \left(1-\frac1d\right)^{m-2}.                           \tag{8}
\]

For integer \(r=m-2\ge1\), Bernoulli's inequality implies
\((1-1/d)^r\le d/(d+r)\). Hence the right side of (8) is at most

\[
 \frac{(m-2)(d+3m-2)}{(m-1)(d+m-2)}
   =1-\frac1{(m-1)(2m^2-4m+1)}<1.                       \tag{9}
\]

The last equality follows because the denominator minus numerator is
exactly one. This proves (2), so disconnected cores cannot beat or attain
the one-root optimum. Together with the connected reduction and the known
attaining design, it proves the theorem.

The exact replay checks the algebraic factorization in (9), the original
and simplified constants at many orders, exact disconnected examples, and
the previously recorded proof dependencies. The all-orders conclusion
rests on the analytic argument above, not on the finite list of checks.
