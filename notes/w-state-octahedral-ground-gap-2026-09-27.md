# A strict W-rate gap for a cancelling octahedral ground core

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** This is an upper bound for a ground-core family, not the
unrestricted W optimum.

[Replay](../computations/w-ground-cancellation-2026-09-27/README.md) ·
[W project](../research/w-state-design/README.md)

## 1. A family with supported ground matchings that cancel

Use six sites. Sites $1,2,3,4$ form a cycle with common ground weight $s$.
The remaining sites are $0,5$, with ground entries

$$
D_{0i}=u,\qquad D_{5i}=\sigma_i v,\qquad
(\sigma_1,\sigma_2,\sigma_3,\sigma_4)=(1,-1,1,-1).
$$

The ground entries on $05$, $13$, and $24$ are zero. Thus, when $s,u,v$
are nonzero, the ground support is the octahedral graph: the complete
six-site graph with three disjoint edges removed. The parameters may be
arbitrary complex numbers. Norm-preserving site phases may also be applied.

Every other colored source entry is free. In particular no restriction is
placed on where entries exciting either or both endpoints may occur.

**Theorem.** Any such source producing exact nonzero uniform $W_6$ satisfies

$$
\boxed{
R<\frac{2}{135}=\frac{26}{27}\,\frac1{65}.
}
\tag{1}
$$

This excludes the entire family from competing with the known rate $1/65$.
We do not claim that $2/135$ is the sharp bound in this family.

The ground core of the earlier
[W shear-normalization obstruction](w-state-shear-normalization-obstruction-2026-09-27.md)
belongs to this family after relabelling sites. Thus the failure of that
normalization shortcut occurs in a family which already has a strict rate
gap by a different argument.

## 2. Response formulas

Put $a=|s|^2$, $b=|u|^2$, $c=|v|^2$. The ground strength is
$a_0=4(a+b+c)$. Direct matching expansion gives

$$
C_{05}=2s^2,\qquad C_{0i}=-2\sigma_i sv,\qquad C_{5i}=2su.
\tag{2}
$$

Among cofactors deleting two cycle sites, only $C_{13}$ and $C_{24}$ are
nonzero, with values $-2uv$ and $2uv$, respectively. Hence

$$
\operatorname{haf}(D)=\sum_i D_{0i}C_{0i}=0.
$$

The ground matching terms therefore cancel, with no assumption of absent
perfect matchings. The response-row norms are

$$
r_i^2=4bc+4a(b+c)\quad(i=1,2,3,4),\qquad
r_0^2=4a^2+16ac,\qquad r_5^2=4a^2+16ab.
\tag{3}
$$

Nonzero uniform W output requires every response row to be nonzero. Thus
$a>0$ and $b+c>0$ are necessary. These conditions also make all rows in
(3) nonzero.

## 3. Equal root strengths give the weakest response bound

For fixed $a$ and $b+c=2t$, the product $bc$ is at most $t^2$. Therefore
the four reciprocal cycle-row norms are smallest when $b=c=t$.
Convexity of the reciprocal also gives

$$
\frac1{4a^2+16ac}+\frac1{4a^2+16ab}
\ge\frac2{4a^2+16at}.
$$

The ground strength is unchanged in this comparison. Consequently, for
$\beta=\sum_i1/r_i^2$ and $y=a/t>0$,

$$
a_0^2\beta\ge
F(y):=(4y+8)^2\left(\frac1{1+2y}+\frac1{2y(y+4)}\right).
\tag{4}
$$

We claim $F(y)>60$ for all $y>0$. Clearing its positive denominator gives

$$
F(y)-60
=\frac{4P(y)}{y(y+4)(2y+1)},\qquad
P(y)=4y^4+6y^3-37y^2+28y+8.
\tag{5}
$$

Here is an elementary exact positivity certificate. On $0\le t\le1$, the
Bernstein polynomials $\binom4j t^j(1-t)^{4-j}$ are nonnegative and sum
to one. The coefficient lists in this basis are:

| Polynomial | Five Bernstein coefficients |
| --- | --- |
| $P(t)$ | $8,\ 15,\ 95/6,\ 12,\ 9$ |
| $P(1+t)$ | $9,\ 6,\ 23/6,\ 8,\ 28$ |

All coefficients are positive, proving $P>0$ on $[0,2]$. For the rest,

$$
P(2+t)=4t^4+38t^3+95t^2+80t+28>0\qquad(t\ge0).
$$

The [unrestricted response bound](w-state-unrestricted-response-bound-2026-09-27.md)
gives $R\le8/(9a_0^2\beta)$ at six sites. Combining it with (4)–(5)
proves (1), for every colored completion. ∎

## 4. A failed polynomial shortcut, with an exact counterexample

This family also separates the desired harmonic response inequality from
a tempting stronger polynomial statement. For a general six-site ground
matrix, let $d_i=\sum_j|D_{ij}|^2$. Since $\sum_i d_i=2a_0$,
Cauchy–Schwarz gives

$$
\beta\ge
\frac{26^2}{\sum_i(1+10d_i/a_0)^2r_i^2}.
$$

Thus the following polynomial bound would imply the desired
$a_0^2\beta\ge520/9$:

$$
\sum_i(a_0+10d_i)^2r_i^2
\ \le\ \frac{117}{10}a_0^4
\quad\text{when }\operatorname{haf}(D)=0.
\tag{6}
$$

**Statement (6) is false.** In the displayed octahedral family, choose
$s=6/5$ and $u=v=1$. Exact arithmetic gives

$$
\frac{\sum_i(a_0+10d_i)^2r_i^2}{a_0^4}
=\frac{647105833}{54700816}>\frac{117}{10}.
$$

The ground hafnian is zero and every response row is nonzero. This is
not a counterexample to the harmonic inequality: equation (4) proves the
stronger $a_0^2\beta>60$ for this very source. It rules out this particular
polynomial shortcut while leaving the unrestricted target open.

## 5. Evidence

The replay independently enumerates all six-site matching sums and
cofactors on rational and complex fixtures, verifies the row formulas,
checks both Bernstein polynomial expansions coefficient by coefficient,
and checks the rational shortcut counterexample. The general claims use
the explicit matching expansions and inequalities above. Independent
audit and unrestricted optimality remain outstanding.
