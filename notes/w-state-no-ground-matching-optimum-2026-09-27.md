# Optimal W design at every even order when the ground support has no perfect matching

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** This permits arbitrary complex colored entries on every edge.
The remaining restriction is on the support of the ground-color entries.

[Replay](../computations/balanced-frontier-2026-09-27/README.md) ·
[Unrestricted response inequality](w-state-unrestricted-response-bound-2026-09-27.md) ·
[Guide](../explainers/BALANCED-FRONTIER.md)

## 1. The theorem and its scope

Let $n=2m\ge4$. Allow arbitrary complex edge blocks producing exact output
$H=\lambda W_n\ne0$. Let $D_{ij}=A_{ij}(a,a)$, and assume that the graph
of nonzero $D_{ij}$ has no perfect matching. Then

$$
 \boxed{R\le R_*:=\frac{n B_n}{(n-1)^2+1},\qquad
 B_n=\frac{((n-1)!!)^2}{\binom n2^m}.}                           \tag{1}
$$

The complete odd-core one-root construction attains equality for every even
$n$. Thus (1) is the exact optimum in this class, even with fully colored
completions and any number of sites carrying excitation entries.

The ground support of a feasible source in this class consists of exactly
two odd connected components. If both contain at least three sites, its
rate is strictly smaller than $R_*$. In particular, a maximizing source
in this class must have an isolated ground-color site. This does not say
its other colored entries necessarily have a one-root architecture.

The theorem does not require nonnegative ground weights. It applies whenever
the zero ground output follows from absence of a supported perfect matching.
Any design beating (1) must instead have a ground perfect matching, with
the ground hafnian vanishing by cancellation between matching terms.

## 2. A matching-theory support reduction

The following graph lemma is useful independently.

**Lemma.** Suppose an even graph $G$ has no perfect matching, but for every
vertex $v$ there is a vertex $w\ne v$ such that $G-\{v,w\}$ has a
perfect matching. Then $G$ is the disjoint union of exactly two odd
components, each of which has a perfect matching after deletion of any
one of its vertices.

**Proof.** Use Tutte's perfect-matching theorem: a graph has a perfect
matching exactly when every vertex set $S$ satisfies
$o(G-S)\le |S|$, where $o$ counts odd connected components. The result
is classical; see [Tutte's original paper](https://doi.org/10.1112/jlms/s1-22.2.107)
and [Halton's combinatorial proof](https://doi.org/10.1017/S0305004100040342).

Since $G$ has no perfect matching, choose $S$ with $q=o(G-S)>|S|$.
Parity strengthens this to $q\ge |S|+2$. If $S\ne\varnothing$, take
$v\in S$. For any $w\in S\setminus\{v\}$, the graph $G-\{v,w\}$
fails Tutte's test using $S\setminus\{v,w\}$. For any $w\notin S$,
delete $S\setminus\{v\}$ from $G-\{v,w\}$. Removing one vertex can
decrease the odd-component count of $G-S$ by at most one, leaving at least
$q-1\ge |S|+1>|S|-1$ odd components. Again there is no perfect matching.
This contradicts the hypothesis at $v$, so the violating set must be empty.

There are therefore at least two odd components of $G$. There cannot be
four or more, since deleting two vertices leaves at least two odd components.
There cannot be any even component: deleting a vertex in it and a second
vertex anywhere either leaves the original two odd components, or replaces
one of them by the new odd remainder of that even component. In either case
a perfect matching is impossible.

Exactly two odd components remain. A perfect matching after deleting $v,w$
requires one deleted vertex in each component, and a perfect matching in
each remaining component. The hypothesis for every $v$ gives the final
claim. ∎

For an exact uniform W source, every scalar cofactor row is nonzero by
equation (2) of the [response theorem](w-state-unrestricted-response-bound-2026-09-27.md).
A nonzero cofactor implies a supported perfect matching after the corresponding
two vertex deletions. Thus the lemma applies to its ground support. This
deduction allows complex cancellation within the cofactors; only their
nonvanishing is needed.

## 3. Factor the response through the two odd components

Let their sizes be $p=2\alpha+1$, $q=2\beta+1$, with
$\alpha+\beta=m-1$. Let $a_L,a_R$ be their ground strengths and set

$$
 h_i=\operatorname{haf}(D_L\setminus i),\quad
 k_j=\operatorname{haf}(D_R\setminus j),\quad
 T_L=\sum_i|h_i|^2,\quad T_R=\sum_j|k_j|^2.
$$

All $h_i,k_j$ are nonzero, since every full cofactor row is nonzero.
There are no within-component cofactors: deleting two sites from the same
odd component leaves the other odd component untouched. The cross cofactors
factor as $C_{ij}=h_i k_j$. Consequently

$$
 b(D)=\frac1{T_R}\sum_{i\in L}\frac1{|h_i|^2}
       +\frac1{T_L}\sum_{j\in R}\frac1{|k_j|^2}
       \ge\frac{p^2+q^2}{T_LT_R}.                              \tag{2}
$$

For a singleton component, its empty hafnian is one and its ground strength
is zero. For $\alpha\ge1$, the sharp odd-core response bound proved from
Roos's hafnian inequality in the
[one-root theorem, section 3](w-state-optimal-design-2026-09-26.md), is

$$
 T_L\le \kappa_\alpha a_L^\alpha,\qquad
 \kappa_\alpha=
 \frac{((2\alpha+1)!!)^2}{(2\alpha+1)^{\alpha+1}\alpha^\alpha}.
                                                                    \tag{3}
$$

The same holds on the right. Maximizing
$a_L^\alpha a_R^\beta/(a_L+a_R)^{\alpha+\beta}$ gives
$\alpha^\alpha\beta^\beta/(\alpha+\beta)^{\alpha+\beta}$.
Combining (2)--(3) with the unrestricted response bound yields

$$
 R\le\frac{n}{m^m}\frac{f_\alpha f_\beta}{p^2+q^2},\qquad
 f_s=\frac{((2s-1)!!)^2}{(2s+1)^{s-1}}\ (s\ge1),\quad f_0=1. \tag{4}
$$

The singleton case follows directly, or by the convention $0^0=1$ in
the preceding maximization. Formula (4) allows all colored completions;
no assumption about their supports was introduced.

## 4. The singleton split is optimal at every size

Put $s=m-1$. When $\alpha=0,\beta=s$, the right side of (4) is

$$
 \frac{n f_s}{m^m(1+(2s+1)^2)}=R_*.
$$

It remains to show a strict gap when $\alpha,\beta\ge1$. The ratios

$$
 g_s=\frac{f_s}{f_{s-1}}=
          \frac{(2s-1)^s}{(2s+1)^{s-1}}
$$

increase with $s\ge1$. One elementary verification treats $s$ as real.
Writing $x=2s-1\ge1$,

$$
 \frac{d}{ds}\log g_s
   =-\log(1+2/x)+\frac1x+\frac3{x+2}
   >-\frac2x+\frac1x+\frac3{x+2}
   =\frac{2(x-1)}{x(x+2)}\ge0.
$$

Thus $f_s$ is log-convex. Moving one unit from the smaller positive
index to the larger increases the product, so
$f_\alpha f_\beta\le f_1f_{s-1}=f_{s-1}$.

For $s\ge3$, compare (4) with the singleton value. Since
$p+q=2s+2$,

$$
 \frac{R_{p,q}^{\rm bound}}{R_*}
 \le \frac{1+(2s+1)^2}{p^2+q^2}\frac1{g_s}
 <\frac2{g_s}\le\frac2{g_3}=\frac{98}{125}<1.               \tag{5}
$$

Here $p^2+q^2\ge(p+q)^2/2$ proves the strict factor-two bound, and
$g_3=125/49$. At $s=2$, the only non-singleton split is $3+3$;
direct substitution gives $R\le1/81=(65/81)R_*$. At $s=1$, there
is no split with both components of size at least three. This proves (1)
at every even $n\ge4$, with attainment by the known one-root source. ∎

## 5. What is still needed for the unrestricted theorem

Every exact W source has zero ground hafnian. The theorem settles the case
where this follows from support alone. The remaining case is a ground
support containing perfect matchings whose complex products cancel.

The scalar response inequality in the preceding note is one possible route
through this case. If it is insufficient, the multi-excitation completion
equations must contribute an additional cost. We have not proved that a
general W source can be transformed into the no-ground-matching class
without increasing its source norm.
