# Two-group W designs: exact reduction and certified optima through forty sites

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted W optimum remains open.

[Replay and certificates](../computations/w-two-group-reduction-2026-09-27/README.md) ·
[Illustrated guide](../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../research/w-state-design/README.md)

## 1. Results and scope

Partition $n=2m\ge6$ sites into nonempty groups of sizes $p\le q$, $p+q=2m$.
The ground weights are constant: $a$ inside the first group, $b$ inside
the second, and $c$ across the groups. Allow arbitrary complex values,
site phases, and relabeling. **All other colored entries are unrestricted.**
For exact nonzero output $\lambda W_n$, use the usual rate
$R=n|\lambda|^2/S^m$ and the known attained rate

$$
R_*=\frac{nB_n}{(n-1)^2+1},\qquad
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}}.
$$

This note proves three statements.

1. **All-size reduction.** For any specified $p,q\ge2$, every nondegenerate
   cancellation branch is a root of a Gegenbauer polynomial. On that
   branch the exact scalar response cost is a rational function of one
   positive real variable. Its stationary points satisfy a polynomial
   of degree **six**, independently of the site count.
2. **All-even two-site gap.** If $p=2$ and $q\ge4$ is even, every colored
   exact-W completion has
   $$
   \boxed{R<\frac56R_*.}
   \tag{1}
   $$
3. **Finite range with all splits.** For every even $6\le n\le40$, the
   exact optimum among all two-group ground sources is $R_*$.
   Every split with $p,q\ge2$ has $R<(80/81)R_*$.
   A one-site group and a complete odd core attain $R_*$.

The third claim covers arbitrary imbalance, every complex cancellation
branch, and disconnected ground sources in its stated finite range.
It is supported by 615 rational interval certificates for 171 unequal
splits, together with the earlier all-even equal-split theorem.
There is **no extrapolation beyond forty sites** for general unequal
splits. The first claim is a reduction of the scalar relaxation, not
an exact optimization of its colored completions.

Write

$$
C_{ij}=\operatorname{haf}D[V\setminus\{i,j\}],\quad
r_i^2=\sum_{j\ne i}|C_{ij}|^2,\quad
s=\sum_{i<j}|D_{ij}|^2,\quad
F(D)=s^{m-1}\sum_i r_i^{-2}.
$$

For $N=2m-1$, set

$$
F_*=\frac{[N(m-1)]^{m-1}(N^2+1)}
{N((2m-3)!!)^2}.
$$

The [unrestricted response inequality](w-state-unrestricted-response-bound-2026-09-27.md)
is $R/R_*\le F_*/F$. It permits every colored completion.
Thus all subsequent scalar lower bounds immediately give rate upper bounds.

## 2. Gegenbauer polynomials classify every cancellation branch

Assume $2\le p\le q$ and put $d=(q-p)/2$. Counting matchings gives

$$
\operatorname{haf}D=b^d G_{p,q}(ab,c),\qquad
G_{p,q}(z,c)=\sum_{j=0}^{\lfloor p/2\rfloor}
\frac{p!q!}{(p-2j)!\,2^{d+2j}j!(d+j)!}\,z^j c^{p-2j}.
\tag{2}
$$

Let $g_p^{(d)}(t)=C_p^{d+1/2}(t)/C_p^{d+1/2}(1)$ denote the normalized
Gegenbauer polynomial. The classical integral representation
[DLMF 18.10.4](https://dlmf.nist.gov/18.10.E4), with parameter $\alpha=d$,
expresses it as the average of
$(t+i\sqrt{1-t^2}\cos\phi)^p$ with density proportional to
$\sin^{2d}\phi$. The even moments of $\cos\phi$ are
$(2j)!d!/(4^j j!(d+j)!)$. Expanding proves

$$
G_{p,q}(z,c)=
\frac{q!}{2^d d!}(c^2-z)^{p/2}
g_p^{(d)}\!\left(\frac{c}{\sqrt{c^2-z}}\right).
\tag{3}
$$

This is a polynomial identity, with no branch choice needed after expansion.
The normalized polynomial is orthogonal on $(-1,1)$ with positive weight
$(1-t^2)^d$. The
[Jacobi Rodrigues formula](https://dlmf.nist.gov/18.5#ii), normalized at one,
is

$$
g_p^{(d)}(t)=
\frac{(-1)^p}{2^p p!\binom{p+d}p}(1-t^2)^{-d}
\frac{d^p}{dt^p}(1-t^2)^{p+d}.
$$

Integrating by parts $p$ times proves orthogonality to every polynomial
of degree below $p$. Multiplying by the product of its
sign-changing linear factors proves that all $p$ roots are simple
and interior, just as in the
[Legendre argument](w-state-equal-split-legendre-2026-09-27.md#2-why-legendre-polynomials-appear).
Parity gives $\lfloor p/2\rfloor$ distinct positive roots.

Suppose $c\ne0$. A zero within-group weight is impossible for a nonzero
W output. For $a=0,b\ne0$, (2) is nonzero. For $b=0$ and $p=q$, the
all-cross term is nonzero. For $b=0$ and $q>p$, every cofactor incident
to the smaller group vanishes, so those response rows are zero.
The case $a=b=0$ is covered by the same alternatives.

Consequently every admissible branch has

$$
\boxed{ab=-k c^2,\qquad
k=t^{-2}-1>0,\qquad g_p^{(d)}(t)=0,\quad 0<t<1.}
\tag{4}
$$

The roots in (4) exhaust the degree-$\lfloor p/2\rfloor$ polynomial
in $ab/c^2$, including its complex roots.
After overall scaling and site phases, every source on the branch has
the real ground representative

$$
b=1,\qquad c=\sqrt{x},\qquad a=-kx,\qquad x>0.
\tag{5}
$$

These operations preserve $F$ and the rate.

## 3. Exact scalar cost and a sextic stationary equation

Fix a root $k$ and let $\gamma=\partial_z G_{p,q}(-k,1)\ne0$.
Differentiation of (2), with its zero-ground constraint, gives

$$
C_A=\frac{\gamma x^{(p-2)/2}}{\binom p2},\qquad
C_B=-\frac{k\gamma x^{p/2}}{\binom q2},\qquad
C_\times=\frac{2k\gamma x^{(p-1)/2}}{pq}.
\tag{6}
$$

For the cross term use $2zG_z+cG_c=pG=0$.
Define the positive polynomials

$$
\begin{aligned}
s(x)&=\binom q2+pqx+\binom p2 k^2x^2,\\
U(x)&=q+(p-1)k^2x,\qquad V(x)=q-1+px,\\
H(x)&=p^2(p-1)k^2xV(x)+q^2(q-1)U(x).
\end{aligned}
\tag{7}
$$

The two response-row values, occurring $p$ and $q$ times, are

$$
r_A^2=\frac{4\gamma^2}{p^2}x^{p-2}
  \left(\frac1{p-1}+\frac{k^2x}{q}\right),\qquad
r_B^2=\frac{4k^2\gamma^2}{q^2}x^{p-1}
  \left(\frac1p+\frac{x}{q-1}\right).
$$

Here $\gamma$ is real because $k$ and the matching coefficients are real.
Combining the reciprocal rows gives, with $r=m-1$,

$$
\boxed{
F_{p,q,k}(x)=
\frac{pq}{4k^2\gamma^2}
\frac{s(x)^r H(x)}{x^{p-1}U(x)V(x)}.}
\tag{8}
$$

Let $D(x)=U(x)V(x)$. After multiplication by positive factors,
the stationary equation is

$$
J(x)=r x s'(x)H(x)D(x)+x s(x)H'(x)D(x)
-(p-1)s(x)H(x)D(x)-x s(x)H(x)D'(x)=0.
\tag{9}
$$

This has degree six. Its constant coefficient is negative, and its
leading coefficient is $(q-1)$ times the product of the leading
coefficients of $s,H,D$, hence positive.
Also $F(x)\to\infty$ as $x\downarrow0$ or $x\to\infty$:
its orders are $x^{-(p-1)}$ and $x^{q-1}$.
Its minimum is therefore attained at one of the finitely many positive
roots of (9).

All coefficients lie in the real algebraic field $\mathbb Q(k)$.
Together with (4), this is an exact finite algebraic procedure for
minimizing the scalar cost at any specified group sizes. No uniqueness
of the stationary point is asserted.

## 4. Degenerate cases and a one-site group

If $c=0$, the ground support consists of two cliques. For even $p,q$,
zero ground amplitude forces a within-group weight to vanish; some
response rows then vanish, excluding nonzero W output.
For odd $p,q\ge3$, both weights must be nonzero. Only cross cofactors
survive, and weighted arithmetic-geometric mean gives the sharp scalar
minimum

$$
\boxed{
F_{\rm disc}(p,q)=
\frac{p^2+q^2}{pq}\,
\frac{r^r p^{(p-1)/2}q^{(q-1)/2}}
{((p-2)!!(q-2)!!)^2},\qquad r=\frac{p+q-2}{2}.}
\tag{10}
$$

Indeed, with $u=|a|^2,v=|b|^2$, the common cross cofactor squared is
$((p-2)!!(q-2)!!)^2u^{(p-1)/2}v^{(q-1)/2}$.
Minimize $(\binom p2u+\binom q2v)^r/(u^{(p-1)/2}v^{(q-1)/2})$.
Equality in (10) occurs at $pu=qv$.

For $p=1$ and $q=n-1$, a nonzero core weight makes the ground hafnian a
nonzero constant times $c$. Thus $c=0$, giving the known isolated-root
ground. A zero core weight would leave zero response at the root for
$n\ge6$. The earlier
[no-ground-matching optimum](w-state-no-ground-matching-optimum-2026-09-27.md)
therefore proves the attained optimum $R_*$ for this remaining split.

## 5. An all-even strict five-sixths gap when the smaller group has two sites

For $p=2$, (2) gives the unique branch $ab=-qc^2$.
Normalize as in (5), so $k=q$. Put $h=(q-1)!!$.
The ground strength and reciprocal response sum simplify to

$$
s=q^2x^2+2qx+\frac{q(q-1)}2,\qquad
\beta=\frac1{h^2}
\left(\frac2{1+qx}+\frac{q(q-1)}{2x(q-1+2x)}\right).
$$

Writing $M=(q+1)^2+1$ and $A=q-1+4x+2qx^2$ gives

$$
\frac{F}{F_*}=
\left(\frac{A}{q+1}\right)^{q/2}
\frac{q+1}{M}
\left(\frac2{1+qx}+\frac{q(q-1)}{2x(q-1+2x)}\right).
\tag{11}
$$

We prove $F/F_*>6/5$ for every even $q\ge4$ and every $x>0$.
For $q\ge10$, discard the first positive reciprocal-row term in (11).
The resulting lower bound exceeds $6/5$ if

$$
\left(\frac{A}{q+1}\right)^{q/2}>
\frac65\,\frac{2x(q-1+2x)M}{q(q-1)(q+1)}.
\tag{12}
$$

For real $q\ge4$, $((q-1)/(q+1))^{q/2}\ge9/25$.
To see monotonicity, differentiate its logarithm and put $z=1/q$:
the derivative is positive because
$\int_0^z(1-t^2)^{-1}\,dt<z/(1-z^2)$.
Bernoulli's inequality now bounds the left side of (12) below by

$$
\frac9{25}\left(1+\frac{2qx+q^2x^2}{q-1}\right).
$$

Subtracting the right side leaves $\alpha+\beta_1x+\chi x^2$, where

$$
\begin{aligned}
\alpha&=\frac9{25},\\
\beta_1&=-\frac{6(7q^3+7q^2-20)}{25q(q-1)(q+1)},\\
\chi&=\frac{3(3q^4+3q^3-40q^2-80q-80)}{25q(q-1)(q+1)}.
\end{aligned}
$$

Its discriminant has the required sign:

$$
4\alpha\chi-\beta_1^2
=\frac{36N(q)}{625q^2(q-1)^2(q+1)^2},
$$

$$
N(q)=9q^7-40q^6-227q^5-298q^4+160q^3+520q^2+240q-400.
$$

The coefficients of $N(10+y)$, in ascending order, are

$$
(24534000,\ 26516640,\ 10456520,\ 2111240,\
243352,\ 16273,\ 590,\ 9).
$$

They are all positive, so the quadratic is strictly positive for all
real $x$ when $q\ge10$. This proves the infinite tail.

For $q=4,6,8$, clear the positive denominators in (11). Put
$U_0=8x^2+(q-1)(q^2+4)x+q(q-1)$ and
$D_0=2x(q-1+2x)(1+qx)$. The required polynomial is

$$
(q+1)A^{q/2}U_0-\frac65(q+1)^{q/2}M D_0.
\tag{13}
$$

Its positive multiples and coefficient lists, in ascending powers of
$x$, are supplied in the replay. For example, at $q=4$ it is 20 times

$$
27-27x-522x^2+576x^3+1280x^4+1088x^5+128x^6.
$$

The exact Bernstein certificates described in section 6 prove positivity
on $x\ge0$. After $t=x/(1+x)$, they use respectively these subintervals:

| $q$ | Subdivision of $0\le t\le1$ |
| --- | --- |
| 4 | $[0,1/8], [1/8,3/16], [3/16,1/4], [1/4,1/2], [1/2,1]$ |
| 6 | $[0,1/4], [1/4,1/2], [1/2,1]$ |
| 8 | $[0,1/2], [1/2,1]$ |

All Bernstein coefficients on every listed interval are strictly positive.
Thus $F>(6/5)F_*$ at all even sizes, proving (1).
The discarded-row bound is used only for $q\ge10$; the three smaller
cases retain both response rows.

## 6. Exact certificates for every split through forty sites

For $2\le p<q$ and even $6\le p+q\le40$, define, using (7),

$$
L_{p,q,k}(x)=pq\,s(x)^rH(x)
-4k^2\gamma^2\frac{81}{80}F_*x^{p-1}U(x)V(x).
\tag{14}
$$

All its coefficients are rational polynomials in $k$.
Strict positivity proves $F>(81/80)F_*$ for the whole branch.
The saved certificates cover every positive root of
$G_{p,q}(-k,1)$, with no sampled-root assumption:

1. A rational Sturm sequence counts all positive roots and isolates each
   one in a rational interval $[\ell,u]$ whose endpoints are not roots.
   Root counts show that no cancellation branch is omitted.
2. If a coefficient of (14) is $\sum_j a_j k^j$, replace it by
   $\sum_{a_j\ge0}a_j\ell^j+\sum_{a_j<0}a_j u^j$.
   This gives a rational lower polynomial $\underline L(x)\le L(x)$
   for every $x\ge0$ and every $k\in[\ell,u]$.
3. For $D=\deg\underline L$, transform
   $\underline L(t/(1-t))(1-t)^D$ to $0\le t\le1$.
   Its initial Bernstein coefficients are
   $\underline L_j/\binom Dj$.
   Exact de Casteljau subdivision takes adjacent averages.
   Every coefficient on every retained subinterval is strictly positive.
   Since the Bernstein basis is nonnegative and sums to one, this proves
   the required positivity for every $x\ge0$.

The replay covers **171 unequal splits and 615 cancellation branches**.
Every branch needs at most two subdivision levels. No floating-point
root, optimizer, tolerance-based sign, or asymptotic extrapolation enters.
The odd disconnected cases use (10); their exact ratios also exceed
$81/80$ throughout the finite range.

Equal splits use the earlier
[all-even Legendre theorem](w-state-equal-split-legendre-2026-09-27.md),
including its strict six-site completion obstruction.
The one-site split attains $R_*$ by section 4. These facts prove the
finite-range exact optimum stated in section 1.

## 7. What remains

The polynomial reduction is valid at every even count, and the two-site
and equal-size exclusions are proved for all counts. The finite
certificate catalog establishes the other splits only through forty
sites. Extending the latter to an all-size analytic bound remains open.
The same certificate generator can test larger specified finite ranges;
failure to obtain a positive certificate would be inconclusive.

More importantly, general ground sources need not be constant on two
groups at all. This result does not settle the unrestricted W optimum,
nor does optimizing (8) guarantee that its minimum-row colored completion
cancels every unwanted output.
