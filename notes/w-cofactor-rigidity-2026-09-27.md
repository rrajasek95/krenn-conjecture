# Rigidity of maximum cofactor response and W optimality near that regime

September 27, 2026. **Written proofs with exact supporting checks; independent
audit pending.** The unrestricted exact W optimum remains open.

[Replay](../computations/w-cofactor-rigidity-2026-09-27/README.md) ·
[Illustrated guide](../explainers/W-GLOBAL-GUARANTEE.md) ·
[Previous universal bound](w-state-universal-factor-two-2026-09-27.md)

Throughout, $n=2m\ge6$, $N=n-1$, and $q=m-1$.
For a scalar ground source $D$, use independent unordered edge coordinates:

$$
a=\sum_e|D_e|^2,\quad P(D)=\operatorname{haf}(D),\quad
C_e=\frac{\partial P}{\partial D_e},\quad
T=\sum_e|C_e|^2,\quad
K_n=B_n\frac{m^m}{q^q},\quad
\eta=\frac{T}{K_na^q}.
$$

When $P(D)=0$ and $a>0$, the previous theorem gives $0\le\eta\le1$.
The sharp bound alone did not describe all its equality cases.

## 1. Three conclusions

**Rigidity theorem.** If $P(D)=0$, $a>0$, and $\eta=1$, then after
relabeling the sites,

$$
D_{0i}=0,\qquad
D_{ij}=r\zeta_i\zeta_j\quad(1\le i<j\le N),
\qquad r>0,\quad |\zeta_i|=1.
\tag{1}
$$

Conversely all these sources have $\eta=1$.
Thus maximum cofactor response forces the known complete odd core with
one isolated site. This holds without a support hypothesis.

**Local scalar optimality theorem.** Put

$$
r_i^2=\sum_{j\ne i}|C_{ij}|^2,\qquad
F(D)=a^q\sum_i r_i^{-2},\qquad
F_*=\frac{(Nq)^q(N^2+1)}{N((N-2)!!)^2}.
$$

Near each source (1), on the manifold $P(D)=0$, all rows are nonzero
and $F(D)\ge F_*$. Equality holds locally only on (1), including
scaling and site phases. After fixing $a$, the excess bounds squared
distance to that equality family by a positive constant.

**High-efficiency consequence.** For each even $n\ge6$, there is
$\delta_n>0$ such that every exact W source with

$$
\eta>1-\delta_n
$$

satisfies $R\le R_*$, with every complex colored entry unrestricted.
No closeness of the full colored source to the construction is needed.
Any better design must stay a definite distance below maximum cofactor
efficiency. No explicit value of $\delta_n$ is supplied.
Equality in this regime forces the known one-root design, up to
overall scaling and site phases.

The four-site restriction matters: its scalar relaxation has counterexamples,
and its cofactor equality family is larger.

## 2. Scalar hafnian norm equality at every even size from six onward

Let $x$ have squared edge norm $s$ and let
$Q_4(x)=\sum_{|U|=4}|\operatorname{haf}(x[U])|^2$.
Put $M=\binom n2$ and

$$
L_n=\frac{9\binom n4}{M^2}
=\frac{3(n-2)(n-3)}{2n(n-1)}.
$$

We first prove

$$
Q_4(x)\le L_n s^2.
\tag{2}
$$

This reproduces the $k=2$ case of the known subhafnian bound and
makes its equality and a useful slack explicit.
Write $z_e=|x_e|$. Expanding each quartet square gives one product
$z_e^2z_f^2$ for every disjoint edge pair, and three cross terms
per quartet, one for each four-cycle.

For a cycle with magnitudes $z_1,\ldots,z_4$, define

$$
A_n=\frac{3}{2n(n-1)},\qquad
B'_n=\frac{3(n-2)}{n(n-1)},\qquad
C_n=\frac{n^2-7n+9}{n(n-1)}.
$$

All three are positive for $n\ge6$, and
$4A_n+4B'_n+2C_n=2$. Weighted AM--GM gives

$$
2z_1z_2z_3z_4
\le A_n\sum_i z_i^4
+B'_n\sum_i z_i^2z_{i+1}^2
+C_n(z_1^2z_3^2+z_2^2z_4^2).
\tag{3}
$$

Indices in the middle sum are cyclic. The counts over all four-cycles
are $(n-2)(n-3)$ for an edge, $n-3$ for an adjacent edge pair,
and $2$ for a disjoint edge pair. Adding the diagonal matching terms
therefore gives coefficient $L_n$ on each fourth power and $2L_n$
on each edge-pair square, proving (2).

If equality holds in (2) and $s>0$, every cycle containing a nonzero
edge must attain equality in (3). Its fourth-power term forces all
four edges to be nonzero; AM--GM then makes their magnitudes equal.
Every two edges occur together in some four-cycle, so all edge
magnitudes are equal and positive. Equality in the complex cross
terms also forces

$$
x_{ij}x_{kl}=x_{ik}x_{jl}=x_{il}x_{jk}
\quad\text{for every four distinct sites}.
\tag{4}
$$

These relations give $x_{ij}=r\zeta_i\zeta_j$ with $|\zeta_i|=1$.
For example, fix sites $0,1$. The ratio $x_{1j}/x_{0j}$ is constant
for $j\notin\{0,1\}$ by (4); substitution into another instance of
(4) factors every edge. Taking a square root of the common factor
gives the site phases.

To pass to the full hafnian, apply
[Roos's Theorem 2.3](https://arxiv.org/html/1906.06176) with the
partition $m=2+1+\cdots+1$:

$$
|P(x)|^2
\le ((n-1)!!)^2\frac{Q_4(x)}{9\binom n4}
                 \left(\frac{s}{M}\right)^{m-2}
\le B_n s^m.
\tag{5}
$$

Nonzero equality in the last bound forces equality in (2).
Consequently the scalar norm equality sources are precisely the
complete equal-magnitude sources with site phases. Their direct
matching expansion verifies the converse.

### An explicit magnitude slack

The fourth-power portion of (3) satisfies

$$
\sum_i z_i^4-4z_1z_2z_3z_4
\ge\frac14\sum_{i<j}(z_i^2-z_j^2)^2.
$$

Indeed $4z_1z_2z_3z_4\le(\sum_i z_i^2)^2/4$ by AM--GM.
The adjacent and opposite portions of (3) separately have
nonnegative slack. Counting each pair at least twice yields

$$
L_ns^2-Q_4(x)\ge
\frac38\sum_e\left(|x_e|^2-\frac{s}{M}\right)^2.
$$

Equation (5) now implies

$$
B_ns^m-|P(x)|^2\ge
B_n\kappa_n s^{m-2}
\sum_e\left(|x_e|^2-\frac{s}{M}\right)^2,\qquad
\kappa_n=\frac{M^2}{24\binom n4}
=\frac{n(n-1)}{4(n-2)(n-3)}.
\tag{6}
$$

## 3. Follow equality around the derivative circle

Normalize $a=1$. At $\eta=1$, let $v=\overline C/\sqrt T$ and
$t=1/\sqrt q$. The zero-hafnian Euler identity makes $v$ orthogonal
to $D$. In the circle argument from the
[previous proof](w-state-universal-factor-two-2026-09-27.md),
every inequality must be an equality. Thus:

- $P(D+zv)$ has only its linear coefficient;
- for every $\theta$, $D+t e^{i\theta}v$ attains the scalar norm bound.

The second statement follows also by continuity: the nonnegative scalar
norm slack has zero circle average. Section 2 makes every edge of
each circle source have one common magnitude. Since its total norm
is constant, that magnitude is independent of $\theta$.
The Fourier coefficient of $e^{i\theta}$ in each squared edge
magnitude is therefore zero. Hence

$$
\overline{D_e}v_e=0,\qquad
|D_e|^2+t^2|v_e|^2=\frac{1+t^2}{M}
\quad\text{for every edge }e.
\tag{7}
$$

Every edge belongs to exactly one of the supports of $D$ and $v$.
At $\theta=0$, write the circle source as $r\zeta_i\zeta_j$.
For general $\theta$, edges in the support $E_v$ are multiplied
by $e^{i\theta}$, and the other edges stay unchanged. Thus

$$
P(D+t e^{i\theta}v)
=r^m\left(\prod_i\zeta_i\right)
\sum_{M'\in\operatorname{PM}(n)}e^{i|M'\cap E_v|\theta}.
$$

All coefficients of this last sum count matchings and are
nonnegative integers. Since the polynomial has only frequency one,
every perfect matching meets $E_v$ in exactly one edge.

We use the following elementary graph fact.

**Lemma.** For even $n\ge6$, an edge set of $K_n$ meeting every
perfect matching exactly once is a full star.

To prove it, let $w_{ij}\in\{0,1\}$ be its indicator.
Swap the two edges on any four sites while retaining a matching
on the remaining sites. This gives the additive four-point equations

$$
w_{ij}+w_{kl}=w_{ik}+w_{jl}=w_{il}+w_{jk}.
$$

They imply $w_{ij}=s_i+s_j$: fixing sites $0,1$ makes
$w_{1j}-w_{0j}$ constant, and substitution constructs the $s_i$.
The numbers $s_i$ have at most two distinct values, since three
different ones, added to a fourth, would give three different
values of $w$. If both value classes had size at least two, their
internal sums would force the two values to be $0,1/2$; their
cross sum $1/2$ is forbidden. Thus one class is a singleton.
The only nonconstant possibilities are a star or its complement.
Their matching counts are respectively $1$ and $m-1$.
Since $m\ge3$, only the star has count one. Constant indicators
have matching count zero or $m$, so cannot occur. This proves the lemma.

Applying it to $E_v$ proves that $D$ is precisely (1).
The converse was checked in the previous sharp response theorem.
This proves rigidity.

At four sites, a star's complement is a triangle and also meets
every perfect matching once. The scalar norm equality argument also
has further degeneracies there; we do not extend this classification
to four sites.

### A quantitative diagnostic before exact equality

For arbitrary normalized zero-hafnian $D$ with $T>0$, put
$u_e=|D_e|^2$ and $p_e=|C_e|^2/T$, so both sum to one.
Average (6) along the same circle, and use its linear output coefficient.
The result is

$$
\boxed{
\sum_e\left(u_e+\frac{p_e}{q}-\frac{m}{qM}\right)^2
+\frac2q\sum_e u_ep_e
\le \frac{m^2}{q^2\kappa_n}(1-\eta).
}
\tag{8}
$$

Thus near-maximal cofactor efficiency quantitatively forces near-disjointness
of the ground and cofactor strengths, and nearly constant combined edge
strength. Equation (8) alone is not a complete quantitative distance bound
to the equality family.

## 4. The scalar response cost increases in every transverse direction

It suffices to work at the unit odd core in (1).
Write its first core perturbation as $d_{ij}$ and its first root
perturbation as $z_i$. The linearized zero-hafnian condition is
$\sum_i z_i=0$.
Let $k=N-2$, $g=N^2+1$, and decompose

$$
d_{ij}=\alpha+u_i+u_j+h_{ij},\qquad
\sum_i u_i=0,\quad \sum_{j\ne i}h_{ij}=0.
$$

Explicitly, if $L=\sum_{i<j}d_{ij}$ and $t_i=\sum_{j\ne i}d_{ij}$,
then $\alpha=L/(Nq)$ and
$u_i=(t_i-(N-1)\alpha)/(N-2)$.
For a smooth real path in the zero-hafnian manifold with these complex first
derivatives, the quadratic coefficient is

$$
\frac{F(D(t))}{F_*}=1+t^2\mathcal Q(d,z)+O(t^3),
$$

where

$$
\begin{aligned}
\mathcal Q(d,z)={}&
\frac{2(N^3-N^2+N-3)}{N(N^2+1)}
                   \|\operatorname{Re}u\|^2\\
&+\frac{N-3}{N(N-2)}\|\operatorname{Re}h\|^2
+\frac{N-1}{N(N-2)}\|\operatorname{Im}h\|^2\\
&+\frac{(N-4)N^2+N-2}{N(N-2)(N^2+1)}\|z\|^2.
\end{aligned}
\tag{9}
$$

The $h$ norms count unordered edges; the $u,z$ norms count sites.
Every coefficient is positive for $N\ge5$.
The omitted $\operatorname{Re}\alpha$ direction is overall scaling.
The omitted $\operatorname{Im}\alpha,\operatorname{Im}u$ directions
are precisely the core site phases.

### Derivation of the quadratic form

First keep the root ground entries zero. The root cofactors are
the odd-core deletion hafnians. With $c=(N-2)!!$, their expansions are

$$
C_{0i}=c(1+t\ell_i+t^2b_i)+O(t^3),\qquad
\ell_i=\frac{L-t_i}{k},\quad
b_i=\frac{\sum_{\{e,f\}\text{ disjoint},\,i\notin e\cup f}d_ed_f}
           {k(N-4)}.
$$

Therefore $\sum_i\ell_i=L$ and
$\sum_i b_i=k^{-1}\sum_{\{e,f\}\text{ disjoint}}d_ed_f$.
The core strength is $Nq+2t\operatorname{Re}L+t^2\|d\|^2$.
Also

$$
\beta=\frac1{\sum_i|C_{0i}|^2}+\sum_i\frac1{|C_{0i}|^2}.
$$

Expanding the reciprocals cancels all first-order terms in $a^q\beta$.
Let $J$ be the adjacency matrix of disjoint unordered core edges,
and write $d=x+iy$ with $x,y$ real. The remaining core form is

$$
\begin{aligned}
\mathcal Q_{\rm core}={}&\frac{\|x\|^2+\|y\|^2}{N}
+\frac{3N^2-1}{Ng}\|\ell(x)\|^2-\frac{\|\ell(y)\|^2}{N}\\
&-\frac{x^{\mathsf T}Jx-y^{\mathsf T}Jy}{Nk}
+\left(-\frac{2(q+1)}{N^2q}+\frac4{N^2g}\right)
                    \left(\sum_e x_e\right)^2.
\end{aligned}
$$

On the constant, site-sum, and zero-row subspaces, $J$ acts by
$\binom{N-2}{2}$, $-(N-3)$, and $1$, respectively.
These follow by summing the edges disjoint from a fixed pair.
The decomposition is orthogonal, with
$\|d\|^2=Nq|\alpha|^2+(N-2)\|u\|^2+\|h\|^2$.
Substitution gives the first three terms of (9), with zero
coefficient on scaling and phases.

For the root perturbation, $C_{0i}$ is independent of $z$ and,
to first order on $\sum_i z_i=0$,
$C_{ij}=-c(z_i+z_j)/k$ for $i,j\ne0$.
Thus the strength increases by $\|z\|^2$, while the reciprocal
sum decreases to second order by $2\|z\|^2/(c^2k)$.
Their normalized net coefficient is

$$
\frac1N-\frac{2N}{k(N^2+1)}
=\frac{(N-4)N^2+N-2}{N(N-2)(N^2+1)}.
$$

There are no mixed core/root quadratic terms: each internal cofactor
vanishes at the base, and its first variation uses only root edges.
The first derivative of $F$ at the base is zero in every source direction,
so the second-order correction enforcing $P(D(t))=0$ does not change
the quadratic form. This completes the derivation.

### From the form to the local inequality

The zero-hafnian set is a smooth manifold here: its differential is
$c\sum_i z_i$, which is nonzero. All response rows stay nonzero nearby,
so $F$ is smooth. Fix the ground norm and use the $N$ core site
phases to choose a transverse local slice. Equation (9) is positive
definite on its tangent space. Taylor's theorem therefore gives
$F-F_*\ge c_n$ times squared distance to (1) in a sufficiently
small normalized neighborhood.

The necessary normalization and phase slice exist by the implicit
function theorem: their tangent directions are independent.
This proves local scalar optimality without using any multi-excitation
output constraint. At six sites the four coefficients in (9) are
$102/65,\ 2/15,\ 4/15,\ 14/195$.

## 5. Exclude all sufficiently efficient competing ground sources

Normalize $a=1$. The set of zero-hafnian sources is compact, and
$\eta$ is continuous on it. By rigidity, its maximum set $\eta=1$
consists exactly of the finitely many root choices and their compact
site-phase orbits. Cover it by finitely many neighborhoods from
the local scalar theorem.

On the compact complement, $\eta$ has maximum strictly less than one.
Choose $\delta_n>0$ accordingly, and smaller than $1-1/\gamma_n$ if
needed, where $\gamma_n=2((n-1)^2+1)/n^2>1$.
If $\eta>1-\delta_n$, the ground source is inside one of these
neighborhoods and $F\ge F_*$. The unrestricted response inequality
then gives $R\le R_*$ for every colored completion.

Equality requires $F=F_*$, hence a ground source (1). It also requires
equality in each single-excitation Cauchy--Schwarz bound, zero source
strength in all other colored entries, and the optimizing relative
ground/excitation scale. These conditions give exactly the known
one-root construction with overall scaling and site phases.

As a corollary there is also a strict, though non-explicit,
improvement of the universal bound:

$$
R\le(1-\delta_n)\frac{2B_n}{n}<\frac{2B_n}{n}.
$$

Indeed the efficient region has $R\le R_*\le(1-\delta_n)2B_n/n$,
and outside it the efficiency-refined bound gives the result directly.
No numerical improvement to the published interval $[1/65,1/45]$
is claimed without an explicit $\delta_6$.

The remaining global task is the response-strength/row-imbalance
inequality on ground sources bounded away from (1). The new theorems
exclude the maximum-response region; they do not prove that all
other ground sources have larger harmonic cost.
