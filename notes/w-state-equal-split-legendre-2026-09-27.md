# An all-even W-design gap from Legendre polynomials

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted global W optimum remains open.

[Exact replay](../computations/w-equal-split-legendre-2026-09-27/README.md) ·
[Illustrated guide](../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../research/w-state-design/README.md)

## 1. The family and the theorem

Let $n=2m\ge6$. Partition the sites into two sets of size $m$.
The scalar ground matrix has weight $a$ on edges within the first set,
$b$ within the second, and $c$ between the sets. These three numbers
are arbitrary complex numbers. All other colored entries are unrestricted.
Relabeling and unit-modulus site phases are also allowed.

For an exact output $\lambda W_n\ne0$, let $S$ be the total squared
source norm and $R=n|\lambda|^2/S^m$. The known attained rate is

$$
R_*=\frac{nB_n}{(n-1)^2+1},\qquad
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}}.
$$

**Theorem.** Every such colored source satisfies

$$
\boxed{R<\frac{80}{81}R_*.}
\tag{1}
$$

Thus the symmetric equal-size two-group family cannot improve the known
design at any even count from six onward. This includes complete-support
ground cancellations, every cancellation branch, arbitrary imbalance
between $|a|$ and $|b|$, and disconnected limiting cases.
The rate bound is not asserted to be attained or sharp for exact W sources.

The result follows from a sharp uniform comparison in the scalar
response relaxation. Define

$$
s=\sum_{i<j}|D_{ij}|^2,\quad
C_{ij}=\operatorname{haf}D[V\setminus\{i,j\}],\quad
r_i^2=\sum_{j\ne i}|C_{ij}|^2,\quad
F=s^{m-1}\sum_i r_i^{-2}.
$$

Every row is nonzero for an exact nonzero W output. Put $N=2m-1$ and

$$
F_*=\frac{[N(m-1)]^{m-1}(N^2+1)}
{N((2m-3)!!)^2}.
$$

Then, throughout the stated ground family,

$$
\boxed{F\ge\frac{81}{80}F_*.}
\tag{2}
$$

Equality in (2) occurs only at $m=3$, with
$ab=-2c^2/3$ and $|a|=|b|=\sqrt{2/3}|c|$.
The coefficient $81/80$ is therefore sharp uniformly over these
dimensions for the scalar relaxation.

There is also an explicit strengthening at large size. For $m\ge8$,

$$
\frac{R}{R_*}<\frac1{Q_m}
\le\frac{143015625}{167518208}
       \left(\frac23\right)^{m-8}
<\frac67\left(\frac23\right)^{m-8},
\tag{3}
$$

where

$$
Q_m=
\frac{2m^{m-1}((2m-3)!!)^2}
{((m-1)!)^2(2m-1)^{m-2}((2m-1)^2+1)}.
\tag{4}
$$

The increasing penalty in (3) is a proved bound, not an asymptotic
formula for the family's true optimal rate.

## 2. Why Legendre polynomials appear

Write $H_m(a,b,c)$ for the ground hafnian. A perfect matching with
$j$ edges inside the first group also has $j$ inside the second,
and $m-2j$ cross edges. Counting the choices gives

$$
H_m(a,b,c)=
\sum_{j=0}^{\lfloor m/2\rfloor}
\frac{m!^2}{(m-2j)!\,4^j(j!)^2}
(ab)^j c^{m-2j}.
\tag{5}
$$

Let $P_m$ be the usual Legendre polynomial, normalized by $P_m(1)=1$.
The classical integral representation

$$
P_m(x)=\frac1\pi\int_0^\pi
\bigl(x+i\sqrt{1-x^2}\cos\phi\bigr)^m\,d\phi
\qquad(-1\le x\le1)
\tag{6}
$$

is [DLMF 18.10.5](https://dlmf.nist.gov/18.10.E5).
Expanding the integrand and using
$\pi^{-1}\int_0^\pi\cos^{2j}\phi\,d\phi=\binom{2j}j/4^j$ gives

$$
P_m(x)=\sum_j
\frac{m!}{(m-2j)!\,4^j(j!)^2}
x^{m-2j}(x^2-1)^j.
$$

Consequently, as a polynomial identity,

$$
H_m(a,b,c)=m!(c^2-ab)^{m/2}
P_m\!\left(\frac{c}{\sqrt{c^2-ab}}\right).
\tag{7}
$$

The right side means its polynomial expansion; no square-root choice
or singular expression is needed when $c^2=ab$.

The $m$ roots of $P_m$ are simple, real, and in $(-1,1)$.
For completeness, Rodrigues' formula

$$
P_m(x)=\frac1{2^m m!}\frac{d^m}{dx^m}(x^2-1)^m
$$

makes $P_m$ orthogonal to every polynomial of degree below $m$:
integrate by parts $m$ times. If there were fewer than $m$ sign-changing
roots in $(-1,1)$, multiply $P_m$ by the product of their linear factors.
The integrand would have a constant nonzero sign, contradicting that
orthogonality. This proves the root assertion, including simplicity.
Parity gives $\lfloor m/2\rfloor$ positive roots.

For $c\ne0$, scale to $c=1$ and write $p=ab$. The polynomial in
$p$ in (5) has degree $\lfloor m/2\rfloor$. Equation (7) supplies
that many distinct roots:

$$
p=-k,\qquad k=x^{-2}-1>0,\qquad P_m(x)=0,\quad 0<x<1.
\tag{8}
$$

These exhaust all complex cancellation branches.

## 3. Imbalance cannot help on any branch

Fix a branch (8). Regard $H_m$ as a polynomial in $p,c$, and put
$L=H_p/\binom m2$ at $p=-k,c=1$. Simplicity of the root gives $L\ne0$.
Differentiating with respect to the three edge weights, and using
$2pH_p+cH_c=mH=0$, gives the three cofactors

$$
C_A=bL,\qquad C_B=aL,\qquad
C_\times=-\frac{m-1}{m}pL.
\tag{9}
$$

Set $u=|a|^2$, $v=|b|^2$, $z=u+v\ge2k$, and
$d=(m-1)k^2/m$. Then $uv=k^2$ and

$$
s=\frac{m(m-1)}2z+m^2,\qquad
\sum_i r_i^{-2}
=\frac{m}{(m-1)|L|^2}
\frac{z+2d}{k^2+dz+d^2}.
\tag{10}
$$

Only $z$ varies within this branch. With $A=2m/(m-1)$,

$$
\frac{d}{dz}\log F
=\frac{m-1}{z+A}
+\frac{k^2-d^2}{(z+2d)(k^2+dz+d^2)}.
\tag{11}
$$

If $d\le k$, this is positive. If $d>k$, then
$k>m/(m-1)$ and $z\ge2k>A$. The last two terms before combination
in (11) are $1/(z+2d)-d/(k^2+dz+d^2)>-1/z$.
Therefore

$$
\frac{d}{dz}\log F>
\frac{m-1}{z+A}-\frac1z
=\frac{(m-2)z-A}{z(z+A)}>0,
$$

where $m\ge3$ was used. Every branch is minimized precisely at
$u=v=k$. Phases do not affect the objective in (10).
A balanced representative is $a=b=i\sqrt{k},c=1$.

## 4. The exact scalar cost is a quadrature weight

Define the polynomial kernel and its reciprocal at a Legendre root:

$$
K_m(x)=\frac12\sum_{j=0}^{m-1}(2j+1)P_j(x)^2,\qquad
w_m(x)=\frac1{K_m(x)}.
\tag{12}
$$

The three-term recurrence telescopes to the Christoffel--Darboux
identity

$$
2K_m(x)=m\bigl(P_m'(x)P_{m-1}(x)
                 -P_m(x)P_{m-1}'(x)\bigr).
$$

At a root of $P_m$, the derivative identity
$(1-x^2)P_m'=m(P_{m-1}-xP_m)$ gives

$$
K_m(x)=\frac12(1-x^2)P_m'(x)^2,\qquad
w_m(x)=\frac2{(1-x^2)P_m'(x)^2}.
\tag{13}
$$

These reciprocals are the usual Gauss--Legendre quadrature weights;
the name is not needed for the proof.
The underlying orthogonal-polynomial kernel identities are recorded
in [DLMF §18.2(v)](https://dlmf.nist.gov/18.2#v).

Differentiate (7) at the balanced representative
$a=b=\zeta=i\sqrt{k}$. The common internal cofactor is

$$
C_A=C_B=(m-2)!\,\zeta\,x^{3-m}P_m'(x).
$$

Thus

$$
|C_A|^2=2((m-2)!)^2x^{4-2m}K_m(x),\qquad
s=\frac{m(m-1+x^2)}{x^2}.
$$

All $2m$ response rows are equal. Also
$T=\sum_{i<j}|C_{ij}|^2=(m-1)s|C_A|^2/m$, so
$\sum_i r_i^{-2}=2m^2/T$. Substitution gives the exact branch minimum

$$
\boxed{
F_m(x)=
\frac{m^{m+1}}{(m-1)((m-2)!)^2}
\frac{(m-1+x^2)^{m-2}}{K_m(x)}.
}
\tag{14}
$$

If $c=0$ and $m$ is even, the zero-hafnian condition forces $ab=0$.
There are then at least four isolated ground vertices; every cofactor
is zero. Such a ground source cannot produce nonzero W output.
If $c=0$ and $m$ is odd, nonzero rows require $ab\ne0$. Only cross
cofactors are nonzero and their common squared magnitude is
$((m-2)!!)^4(|a|^2|b|^2)^{(m-1)/2}$.
The arithmetic-geometric mean inequality gives the sharp minimum

$$
F_{\rm disc}
=\frac{2[m(m-1)]^{m-1}}{((m-2)!!)^4}.
\tag{15}
$$

This is exactly (14) evaluated at $x=0$, using
$P_m'(0)=mP_{m-1}(0)$ and
$|P_{m-1}(0)|=(m-2)!!/(m-1)!!$.
Thus the exact family minimum is the minimum of (14) over the
**nonnegative** roots of $P_m$, including zero for odd $m$.
There is no claim here that the largest root always minimizes it.

## 5. A dimension-independent bound and the infinite tail

The integrand in (6) has modulus at most one, hence $|P_j(x)|\le1$.
For $-1<x<1$ and $m\ge2$, the $j=1$ term makes

$$
K_m(x)<\frac{m^2}{2}.
$$

Equation (14), also at $x=0$, therefore gives

$$
F_m(x)>
L_m:=\frac{2m^{m-1}(m-1)^{m-3}}{((m-2)!)^2}.
\tag{16}
$$

The ratio $L_m/F_*$ is precisely $Q_m$ in (4).
Direct cancellation of factorials gives

$$
\frac{Q_{m+1}}{Q_m}
=\frac{2m+1}{m}
\left(1-\frac1{m(2m+1)}\right)^m
\frac{2m^2-2m+1}{2m^2+2m+1}.
\tag{17}
$$

Bernoulli's inequality bounds the middle factor below by
$1-1/(2m+1)$. Thus the ratio is at least
$2(2m^2-2m+1)/(2m^2+2m+1)$.
For $m\ge8$ this exceeds $3/2$, since
$2m^2-14m+1=2(m-8)^2+18(m-8)+17>0$.
Finally

$$
Q_8=\frac{167518208}{143015625}>\frac76>\frac{81}{80}.
$$

This proves (2) for every $m\ge8$ and the quantitative tail in (3).
No finite truncation or numerical extrapolation is used.

## 6. Five finite degrees with rational certificates

It remains to check $m=3,4,5,6,7$. Put $y=x^2$,
$A_m=m^{m+1}/((m-1)((m-2)!)^2)$, and let
$q_m(y)=P_m(x)/x^{m\bmod2}$, expressed as a polynomial in $y$.
At every positive Legendre root, (2) is equivalent to

$$
H_m(y):=A_m(m-1+y)^{m-2}
-\frac{81}{80}F_*K_m(\sqrt y)\ \ge0.
\tag{18}
$$

The polynomial remainder of $H_m$ on division by $q_m$ is zero for
$m=3$. For the other four degrees the following table gives the
remainder, with a positive denominator $d$. Each numerator is
strictly positive throughout $0\le y\le1$.

| $m$ | Numerator | $d$ |
| --- | --- | ---: |
| 4 | $91064+14765(1-y)$ | $280$ |
| 5 | $15158361426+3212873471y$ | $2857680$ |
| 6 | $35532440345+25123412335y+18859616167y(1-y)$ | $758912$ |
| 7 | $324694581459728736+326549099390321627y+123689938153268938y(1-y)$ | $757954454400$ |

The exact replay reconstructs these divisions from Rodrigues' formula
and checks every rational coefficient. At the additional zero root
for odd $m$, (15) gives respectively

$$
\frac{F_{\rm disc}}{F_*}
=\frac{81}{65},\quad
\frac{765625}{269001},\quad
\frac{6277868289}{788997625}
\qquad(m=3,5,7),
$$

all strictly above $81/80$. For $m=3$, the sole positive squared root
is $3/5$, giving $F_3=117/2=(81/80)F_*$.
Strict increase under imbalance in section 3 completes the equality
classification in (2).

## 7. Return to colored W sources

The [unrestricted response bound](w-state-unrestricted-response-bound-2026-09-27.md)
allows arbitrary colored completions and gives

$$
R\le\frac{2m(m-1)^{m-1}}{m^m F},\qquad
R_*=\frac{2m(m-1)^{m-1}}{m^m F_*}.
$$

Equation (2) proves (1) non-strictly. Equality could occur only at
the balanced six-site source. The
[six-site completion obstruction, section 5](w-state-balanced-three-plus-three-2026-09-27.md#5-why-equality-in-the-rate-bound-is-impossible)
excludes it: minimum-norm single-excitation entries leave a nonzero
two-excitation coefficient sum. Hence the rate inequality is strict.
Equations (16)--(17) likewise prove (3) for every colored completion.

This is an all-even exclusion of a specified ground family, not the
unrestricted design theorem. Ground weights varying independently within
either group, unequal group sizes, and general nonuniform cancellation
cores are not covered by this result. Nor does it extend the six-site
local-minimum theorem to higher dimensions.

## 8. Reproducibility and scope of the evidence

The exact replay uses rational arithmetic only. It checks:

- Matching counts and individual cofactor polynomials by a separate
  endpoint recursion through $m=12$.
- Rodrigues, integral-expansion, recurrence, kernel, and derivative
  identities through degree 16.
- The branch-cost formula against independently counted cofactors in
  polynomial quotient rings through $m=12$.
- Every small-degree certificate above, the disconnected costs, the
  exact tail base case, and the positive polynomial behind the
  all-size induction.

These checks support the stated written proof. They do not replace its
arguments about all degrees, complex cancellation branches, imbalance,
or passage from the scalar relaxation to colored outputs. No numerical
root approximation or optimizer is part of the proof package.
