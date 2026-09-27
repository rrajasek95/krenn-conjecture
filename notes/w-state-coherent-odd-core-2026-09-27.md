# W optimality with a uniform odd ground core and cancelling root couplings

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The global unrestricted W optimum remains open.

[Replay](../computations/w-ground-cancellation-2026-09-27/README.md) ·
[W project](../research/w-state-design/README.md) ·
[Unrestricted response inequality](w-state-unrestricted-response-bound-2026-09-27.md)

## 1. The theorem

Let $n=2m\ge6$ and $N=n-1$. Label one site $0$ and the others
$1,\ldots,N$. Allow arbitrary complex colored edge entries, with exact
nonzero output $H=\lambda W_n$. Suppose their ground-color entries satisfy

$$
D_{ij}=w\ne0\quad(1\le i<j\le N),\qquad D_{0i}=z_i.
\tag{1}
$$

The same statement holds after unit-modulus site scalings: multiplying
every entry on edge $ij$ by $g_i g_j$, with $|g_i|=1$, preserves source
strength and multiplies every output by the same phase.

Write $S$ for total source strength, and

$$
R=\frac{n|\lambda|^2}{S^m},\qquad
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}},\qquad
R_*=\frac{nB_n}{(n-1)^2+1}.
$$

Put

$$
q=m-1=\frac{N-1}{2},\qquad
\kappa=\frac{N-1}{N-2},\qquad
x=\frac{\sum_i|z_i|^2}{\binom N2 |w|^2}.
$$

**Theorem.** Every such source obeys

$$
\boxed{
R\le R_*\,G_N(x),\qquad
G_N(x)=
\frac{(N^2+1)(1+\kappa x)}
     {(1+x)^q(N^2+1+\kappa x)}.
}
\tag{2}
$$

For $N\ge5$, $G_N(0)=1$ and $G_N$ is strictly decreasing on $[0,\infty)$.
Thus $R_*$ is the attained optimum in this entire class, and every source
with any nonzero root ground coupling has strictly smaller rate.

The restriction is only (1). Excitation entries may occur on every edge,
including inside the odd core, and may use additional colors. No restriction
to a one-root or two-root colored architecture is made.

If every $z_i$ is nonzero and their sum is zero, the ground support is
complete and has perfect matchings that cancel. Consequently this theorem
settles a family outside the earlier
[no-ground-matching theorem](w-state-no-ground-matching-optimum-2026-09-27.md).
It does not cover arbitrary nonuniform odd cores.

## 2. Compute the ground responses

Define

$$
c=(N-2)!!\,w^{m-1},\qquad
d=(N-4)!!\,w^{m-2},\qquad c=(N-2)wd.
$$

Expansion by the partner of site $0$ gives

$$
\operatorname{haf}(D)=c\sum_i z_i.
$$

Exact W output has zero ground amplitude; since $c\ne0$,

$$
\sum_i z_i=0.
\tag{3}
$$

Let $C_{ij}$ be the hafnian after deleting sites $i,j$. Counting the
matchings of the remaining complete even core gives

$$
C_{0i}=c,\qquad
C_{ij}=d\sum_{k\notin\{i,j\}}z_k=-d(z_i+z_j)
\quad(i,j\ne0).
\tag{4}
$$

For $b=\sum_i|z_i|^2$, equation (3) implies

$$
\sum_{j\ne i}|z_i+z_j|^2=b+(N-4)|z_i|^2.
$$

The squared response-row norms are therefore

$$
r_0^2=N|c|^2,\qquad
r_i^2=|c|^2+|d|^2\bigl(b+(N-4)|z_i|^2\bigr).
\tag{5}
$$

In particular all rows are nonzero. Their sum over the core sites is

$$
\sum_{i=1}^N r_i^2=N|c|^2+2(N-2)|d|^2b.
$$

Cauchy–Schwarz on these $N$ positive row norms yields

$$
\begin{aligned}
\beta(D):=\sum_{i=0}^N\frac1{r_i^2}
&\ge \frac1{N|c|^2}
 +\frac{N^2}{N|c|^2+2(N-2)|d|^2b}\\
&=\frac1{|c|^2}
 \left(\frac1N+\frac{N}{1+\kappa x}\right).
\end{aligned}
\tag{6}
$$

For $N\ge5$, equality in this Cauchy–Schwarz step holds exactly when all
$|z_i|$ are equal, including the case $z_i=0$ for all $i$. Equality in
(6) need not make the other W output constraints feasible.

## 3. Insert the unrestricted response bound

Let $a_0=\binom N2|w|^2+b$ be the ground strength. Producing coefficient
$\lambda$ at site $i$ requires at least $|\lambda|^2/r_i^2$ in the source
entries with exactly that site excited. These are distinct entries for
different $i$, so

$$
S\ge a_0+|\lambda|^2\beta(D).
$$

Maximizing $n u/(a_0+\beta u)^m$ over $u\ge0$ gives

$$
R\le\frac{nq^q}{m^m a_0^q\beta(D)}.
\tag{7}
$$

This argument permits every colored completion; omitting the constraints on
unwanted outputs only increases its upper bound.

Since $\binom N2=Nq$, equation (6) gives

$$
a_0^q\beta(D)\ge
\frac{(Nq)^q}{((N-2)!!)^2}
(1+x)^q\left(\frac1N+\frac{N}{1+\kappa x}\right).
\tag{8}
$$

The value obtained by substituting $x=0$ in (7)–(8) is $R_*$, by direct
algebra. Dividing by that value gives (2).

To check monotonicity, both terms of

$$
(1+x)^q\left(\frac1N+\frac{N}{1+\kappa x}\right)
$$

are strictly increasing for $N\ge5$. For the second term, the sign of the
derivative is the sign of

$$
(q-\kappa)+\kappa(q-1)x,\qquad
q-\kappa=\frac{(N-1)(N-4)}{2(N-2)}>0.
$$

Thus (8) strictly exceeds its $x=0$ value whenever $b>0$.

Attainment at $b=0$ is explicit. Set $w=1$, all $z_i=0$, and use only the
additional entries

$$
A_{0i}(a,b)=\frac{N}{\sqrt{N^2+1}},\qquad
A_{0i}(b,a)=\frac1{\sqrt{N^2+1}}.
$$

Here the first color refers to site $0$. Each matching uses exactly one
such edge, so the only outputs are W words, all with coefficient
$\lambda=Nc/\sqrt{N^2+1}$. The ground strength is $Nq$, the excitation
strength is $N$, and $S=Nm$. Substitution gives $R=R_*$. ∎

The cancellation family is not vacuous away from the optimum. Keep these
excitation entries and add any root ground vector with zero sum. All desired
W coefficients stay the same, the added ground output cancels, and no matching
can contain two excitation edges because they all meet site $0$. This gives
exact W sources with complete ground support whenever every $z_i$ is nonzero.
The theorem also allows other completions that use excitation entries
throughout the core.

## 4. Six sites and the four-site boundary

At six sites the bound is particularly concrete:

$$
\boxed{
R\le\frac1{65}
\frac{13(3+4x)}{(1+x)^2(39+2x)},\qquad
x=\frac{\sum_i|z_i|^2}{10|w|^2}.
}
\tag{9}
$$

It proves the open scalar threshold $a_0^2\beta(D)\ge520/9$ throughout
this family, including its complete-support cancellation sources.

The restriction $n\ge6$ matters. For $n=4$, the same formulas give
$N=3$, $q=1$, and $\kappa=2$. The response lower-bound factor has minimum

$$
\min_{x\ge0}(1+x)\left(\frac13+\frac3{1+2x}\right)=\frac83,
$$

at $x=1$, compared with $10/3$ at $x=0$. In fact the difference from
$8/3$ is $2(x-1)^2/[3(1+2x)]$.
With $w=1$ and $(z_1,z_2,z_3)=(1,\omega,\omega^2)$, where
$\omega^2+\omega+1=0$, equation (6) is attained and the relaxed upper
bound is $1/8$. The minimum-strength single-excitation completion has
unwanted outputs. This is a scope check, not a four-site W design beating
$1/10$.

## 5. Evidence and remaining work

The proof above holds for all complex root couplings and every even
$n\ge6$. The replay separately enumerates ground matchings and cofactor
responses on complex fixtures through twelve sites, checks the row norm
formulas, and verifies the rate algebra and positive derivative coefficients
through eighty sites. These finite checks support the written all-orders
argument rather than replacing it.

The unrestricted problem still permits a nonuniform ground core after
deletion of every site. No rate-preserving reduction of those cores to (1)
is proved here. The six-site scalar inequality for all such cores and the
unrestricted all-even W optimum remain open.
