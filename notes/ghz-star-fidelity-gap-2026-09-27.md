# Star products and support obstructions to high GHZ fidelity

September 27, 2026.

**Status: written proof with exact supporting checks; independent audit
pending.** This is a consequence of the approximate reflection and rotation
estimates in [the general complex rate proof](general-complex-rate-bound-2026-09-26.md),
especially equations (6) and (8). It is separate from the Lean formalization.
The unrestricted square-root rate law remains open.

## 1. Results

Use the three-color complex matching model on \(n=2m\ge4\) sites, with
arbitrary endpoint-color entries \(A_{pq}(i,j)=A_{qp}(j,i)\).
Let \(S=\sum_{p<q,i,j}|A_{pq}(i,j)|^2>0\), and write

\[
 H=\lambda\Delta+E,\qquad \Delta=a^n+b^n+c^n,\qquad
 \lambda=(H_{a^n}+H_{b^n}+H_{c^n})/3,
 \quad \ell=|\lambda|,\quad \varepsilon=\|E\|_2.
\]

For a root \(p\) and color \(a\), define its same-color star product

\[
 z_{p,a}(A)=\prod_{i\ne p}A_{pi}(a,a),\qquad
 \eta(A)=\max_{p,a}\frac{|z_{p,a}(A)|^2}{S^{n-1}}.
\]

**Theorem 1 (explicit star certificate).** With the positive rational
constant \(\kappa_n\) below,

\[
 \boxed{\varepsilon\ge \kappa_n\,\eta(A)\,\ell.}       \tag{1}
\]

Consequently, whenever \(H\ne0\),

\[
 \boxed{F\le \frac{3}{3+\kappa_n^2\eta(A)^2}.}         \tag{2}
\]

In particular, **any source with one nonzero same-color star has a
neighborhood with a fixed fidelity ceiling below one**. This excludes
every full-support single-color zero, at every even size at least four,
as a limit of sources whose GHZ fidelity tends to one. Full support is
more than is needed: one such star suffices.

There is also a stronger qualitative support test. For a root \(p\),
neighbor \(i\), and receiving palette \(B=\{a,b\}\), let

\[
 A_{pi}[:,B]=(A_{pi}(h,k))_{h\in\{a,b,c\},\,k\in B}
\]

be the \(3\)-by-\(2\) block, oriented with \(p\) first.

**Theorem 2 (necessary two-column zeros).** Suppose normalized sources
\(A_j\to A_0\) have nonzero output and \(F(A_j)\to1\). Then

\[
 \boxed{\text{for every }p\text{ and every two-color palette }B,
 \text{ some }i\ne p\text{ satisfies }A_{0,pi}[:,B]=0.} \tag{3}
\]

The neighbor can depend on the root and palette. Conversely, if a fixed
source fails this necessary condition, it has a neighborhood with a
fidelity ceiling below one, for all sources with nonzero output there.
This is not a sufficient condition for approaching fidelity one.

The target basis is fixed throughout. The statements do not allow
independent basis changes without also changing the target.

## 2. The inherited polynomial estimate

First normalize \(S\le1\). Put

\[
 D=m-1,\quad N=n-1=2D+1,\quad P=(n-1)!!.
\]

Let \(I_0=I_1=1\) and \(I_j=I_{j-1}+(j-1)I_{j-2}\), and set

\[
 \begin{split}
 M&=3^N I_N,\quad U_0=2^NM,\quad V_0=2(P+M),\\
 T&=(4D+1)(1+2^N)(P+U_0)(U_0+V_0),\\
 \kappa_n&=\frac{1}{3^m\,2^{2D}\,T}.
 \end{split}                                        \tag{4}
\]

These intentionally conservative constants are inherited from the
general rate proof; they are not practical fidelity estimates.

Fix an original root \(p\). Its three actual rows give a linear mean
\(L(s)=s_aY_a+s_bY_b+s_cY_c\) on the \(N\) remaining sites.
Let \(R_0\) be the retained quadratic source. The divided odd response is

\[
 \Psi(s)=\sum_{j=0}^{D}
       \frac{L(s)^{2j+1}}{(2j+1)!}R_0^{[D-j]},
 \qquad \Phi(s)=L(s)R_0^{[D]}.
\]

Set \(\mathcal H=\Psi-\Phi\), \(\xi=\|E\|_1\), and suppose
\(\lambda\ne0\). Split the pure receiving word \(a^\Omega\) as

\[
 \mathcal H_{a^\Omega}=s_aW+V,
\]

where no monomial of \(V\) is divisible by \(s_a\). The polynomial
\(W\) is even, has degree at most \(2D\), and \(\|W\|_1\le M\).
Define \(g=1+W/\lambda\). The earlier estimates give

\[
 \left\|g(s/\sqrt2)^2-g(s)\right\|_1
       \le T\xi/\ell^3,                              \tag{5}
\]

and, on any receiving palette \(B=\{u,v\}\),

\[
 \Psi|_B=\lambda(s_u u^\Omega+s_v v^\Omega)g+\mathcal B_B,
 \qquad \|\mathcal B_B\|_1\le(P+U_0)\xi/\ell.          \tag{6}
\]

Norms here sum absolute coefficients in both the parameter and receiving
word bases. Both estimates hold before the earlier proof imposes
\(\xi/\ell\le1\). They require neither invertibility nor a rank hypothesis.
Their derivation uses reflection to compare pure responses, followed by
rotation and coefficient-wise division by a determinant polynomial.

## 3. Extract the last coefficient instead of the cubic response

Let \(W_{2D}\) be the homogeneous part of degree \(2D\).
Because \(D\ge1\), the degree \(4D\) part of the left-hand polynomial
in (5) is exactly

\[
 2^{-2D}W_{2D}(s)^2/\lambda^2.                       \tag{7}
\]

The subtracted polynomial \(g(s)\) has too low a degree to contribute.
No lower-degree term in the product can contribute either.

The coefficient of \(s_a^N\) in the pure receiving word
\(\Psi_{a^\Omega}\) is precisely

\[
 [s_a^N]\Psi_{a^\Omega}=\prod_{i\ne p} A_{pi}(a,a)
                          =z_{p,a}(A).              \tag{8}
\]

Indeed only the term \(L^N/N!\) has this parameter degree. Choosing the
one factor at each site gives \(N!\) equal contributions, canceled by
the denominator. Dividing the part divisible by \(s_a\) shows
\([s_a^{2D}]W_{2D}=z_{p,a}\).

Therefore the coefficient of \(s_a^{4D}\) in (7) is

\[
 \frac{z_{p,a}^{\,2}}{2^{2D}\lambda^2}.
\]

This is a complex square, whose absolute value is
\(|z_{p,a}|^2/(2^{2D}\ell^2)\); no positivity of the original entries
is used. Applying (5) to this single coefficient gives

\[
 \xi\ge \frac{|z_{p,a}|^2}{2^{2D}T}\ell.
\]

Since \(\xi\le3^m\varepsilon\), this proves (1) for \(S=1\) after
maximizing over roots and colors. For arbitrary \(S>0\), replace \(A\)
by \(A/\sqrt S\). The ratio \(\varepsilon/\ell\) is unchanged, and
the squared star product is divided by \(S^N\).
When \(\lambda=0\), (1) is automatic and \(F=0\) if \(H\ne0\).
Finally \(F=3\ell^2/(3\ell^2+\varepsilon^2)\) proves (2).

At a fixed \(A_0\ne0\) with \(\eta(A_0)>0\), continuity gives a
neighborhood with \(\eta(A)\ge\eta(A_0)/2\). Equation (2) then gives
the claimed uniform local ceiling. This also applies if \(H(A_0)=0\),
where fidelity itself is undefined: the statement concerns nearby
nonzero outputs.

## 4. Proof of the two-column support test

Consider a normalized sequence as in Theorem 2. Eventually \(\ell_j>0\),
and

\[
 x_j=\xi_j/\ell_j
 \le3^m\sqrt{3(1-F_j)/F_j}\longrightarrow0.
\]

Taking the whole degree \(4D\) part in (5), rather than one coefficient,
gives

\[
 \|W_{j,2D}^{\,2}\|_1\le2^{2D}T x_j\longrightarrow0. \tag{9}
\]

The coefficients of \(W_{j,2D}\) depend polynomially on \(A_j\):
forming \(W\) just selects monomials and removes one \(s_a\).
Thus \(W_{j,2D}\to W_{0,2D}\). Equation (9) implies
\(W_{0,2D}^2=0\), hence \(W_{0,2D}=0\), since the ordinary complex
polynomial ring has no nonzero element with square zero.

Taking degree \(N\) in (6) now shows that the highest response
\(\Psi_{j,N}|_B\) tends to zero on every binary receiving palette.
There is no division by \(\lambda_j\) in this step: its model term is
\((s_u u^\Omega+s_v v^\Omega)W_{j,2D}\), and its error is \(O(x_j)\).
Continuity of the original response gives

\[
 \left.\frac{L_0(s)^N}{N!}\right|_B=0.                \tag{10}
\]

Introduce ordinary commuting variables \(y_{i,k}\), one per receiving
site \(i\ne p\) and color \(k\in B\). The tensor polynomial in (10)
is represented injectively by

\[
 \prod_{i\ne p}
 \left(\sum_{h\in\{a,b,c\},\,k\in B}
       A_{0,pi}(h,k)s_h y_{i,k}\right).              \tag{11}
\]

It is multilinear in the receiving sites, so this passage to an
ordinary polynomial ring preserves every tensor coefficient.
That ring has no zero divisors. A zero product (11) therefore has a
zero factor. Its monomials \(s_hy_{i,k}\) are distinct, so that factor
vanishes exactly when \(A_{0,pi}[:,B]=0\). This proves (3).

If a fixed nonzero source fails (3) but had no local fidelity ceiling,
choose sources at distance at most \(1/j\) with nonzero output and
fidelity greater than \(1-1/j\). Normalize them by continuity of \(S\).
The conclusion just proved is a contradiction. This establishes the
local converse without asserting sufficiency of (3).

## 5. Consequences for the research frontier

At every possible high-fidelity limit, the same-color support graph of
each target color has degree at most \(n-2\) at every vertex. Its missing
edges must cover all vertices, so at least \(n/2\) same-color cells vanish.
Theorem 2 is stronger: it requires an entire pair of receiving columns
to vanish on some incident edge for each root and palette.

For a single-color source with ground color \(a\), choose any palette
containing \(a\). Condition (3) says that every root has a missing
ground edge. Thus every full-support single-color source is excluded.
In particular the recorded full-support rank-25 zero is excluded:
its six ground star products are \(1,1,1,1,-2,-2\).

The earlier [uniform fifth-power onset theorem](full-support-ghz-onset-2026-09-27.md)
remains true and supplies reusable local response estimates. For the
GHZ rate question near this boundary, (1) is stronger: it directly
gives \(\varepsilon\ge c|\lambda|\), without a source-distance remainder.
There are no high-fidelity sequences near a fixed such zero to analyze.
The earlier frozen packages are retained as records of their own claims.

This does not prove a universal fidelity gap. The star products may
vanish as the limiting support becomes sparse, and the necessary block
zeros in (3) allow many configurations. The prism has such zeros.
The unrestricted square-root law still requires
\(\varepsilon\ge c|\lambda|^3\) uniformly through the remaining
normalized zero-output limits. Rank-deficient two-triangle limits
and other cancellation configurations satisfying (3) remain relevant.

## 6. Reproduction and scope of checking

The [exact replay package](../computations/ghz-star-fidelity-gap-2026-09-27/README.md)
pins the inherited proof and arithmetic. It checks highest-degree
coefficients with complex phases, literal star products on several
sizes, the rank-25 fixture, two-column support controls, and normalized
inequalities on exact source examples. Corrupt scaling factors are
rejected. The arbitrary-size inequalities and limit arguments above
are supplied by the written proof, not by finite testing.
