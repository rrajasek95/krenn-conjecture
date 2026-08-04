# Fixed-star three-hole gauge dichotomy

## Outcome

The common-power condition supplies a new exact catalecticant one level
below the fixed-star map.  Its kernel always contains the image of a
transparent `2(|J|-1)`-parameter expansion gauge.  Under the stated
connected nonbipartite rank-three graph hypothesis that parametrization is
injective.  If its image is the whole kernel and the graph hypothesis holds
after deleting any site, then every one of the three star rows is supported
at a single site.
Equivalently, the common power has three pure constant cofactors.

Thus, at every odd order `|J|>=7`, a putative counterexample lies in one of
two explicit branches:

1. the fixed star is already the three-cell pure-cofactor form; or
2. some three-hole catalecticant has an extra kernel beyond expansion
   gauges, or some deleted rank-three graph is disconnected, nonspanning,
   or bipartite.

This is special to the fact that all cofactors come from
`q^(m-1)`.  It is not an arbitrary cofactor-module lemma.  The maximal-rank
branch is nonvacuous: exact finite-field minors prove that it is a nonempty
Zariski-open condition at `|J|=5,7,9`.

The theorem does not exclude the singular/low-rank branch.  At `|J|=5`,
the final two-centre counting step is unavailable; that order is already
excluded by the complete six-vertex theorem.

## 1. Common cofactors and three-hole cofactors

Let `J` have odd cardinality

\[
                         |J|=2m-1\ge5
\]

and work in the square-free site algebra

\[
 \mathcal R_J=\bigotimes_{j\in J}(\mathbb C\oplus V_j),
 \qquad \dim V_j=3,\qquad V_j^2=0.
\]

Let `q in (R_J)_2`.  For a site `j` and a triple of distinct sites put

\[
 C_j=H_{J\setminus\{j\}}(q),\qquad
 D_{ijk}=H_{J\setminus\{i,j,k\}}(q).                     \tag{1}
\]

These are exactly the indicated support components of
`q^(m-1)/(m-1)!` and `q^(m-2)/(m-2)!`.  Hafnian expansion at `k` gives,
for `i!=j`,

\[
                 C_i=\sum_{k\notin\{i,j\}}q_{jk}D_{ijk}. \tag{2}
\]

Suppose three linear elements `z_0,z_1,z_2` satisfy the fixed-star
equations

\[
 F_q(z_r):=z_r{q^{m-1}\over(m-1)!}
          =g_r:=e_r^{\otimes J},\qquad r=0,1,2.           \tag{3}
\]

Write `z_r=sum_j z_(j,r)` with `z_(j,r) in V_j`.

## 2. The quotient three-hole catalecticant

Fix a site `j` and a color `r`.  Put

\[
 \bar V_j=V_j/\mathbb Ce_r
\]

and put a bar on the endpoint-`j` factor of any tensor after applying this
quotient.  Define

\[
\begin{aligned}
 \Psi_{j,r}:\quad
 \bar V_j\oplus
 \bigoplus_{\{i,k\}\in\binom{J\setminus\{j\}}2}
       (V_i\otimes\bar V_j\otimes V_k)
 &\longrightarrow
 \bar V_j\otimes\bigotimes_{v\ne j}V_v,\\
 \Psi_{j,r}\bigl(u,(T_{ik})\bigr)
 &=u^{(j)}\otimes C_j+
   \sum_{i<k}T_{ik}^{(i,j,k)}\otimes D_{ijk}.             \tag{4}
\end{aligned}
\]

All tensor slots in (4) are restored to site order.  The map uses the
common one-hole and three-hole cofactors of the same quadratic `q`.

There is an unavoidable kernel.  For a tuple
`w=(w_i)_(i!=j)` with every `w_i in bar V_j`, define

\[
 \mathcal G_{j,r}(w)=
 \left(\sum_{i\ne j}w_i,
       \bigl(-(w_i+w_k)^{(j)}\otimes q_{ik}\bigr)_{i<k}
 \right).                                                \tag{5}
\]

**Lemma 2.1 (expansion gauges).**

\[
                         \operatorname {im}\mathcal G_{j,r}
                              \subseteq\ker\Psi_{j,r}.    \tag{6}
\]

**Proof.**  Expand `C_j` at a fixed site `i`:

\[
                         C_j=\sum_{k\notin\{i,j\}}q_{ik}D_{ijk}.
\]

Multiply by `w_i` in the restored `j` slot and sum over `i`.  Every
unordered pair `{i,k}` occurs twice and gives
`(w_i+w_k)q_ikD_ijk`, which cancels the second component in (5). `QED`

If `G_3(q)[J\setminus{j}]` is connected and nonbipartite, then
`G_(j,r)` is injective.  Indeed, a zero gauge has
`(w_i+w_k) tensor q_ik=0` on every rank-three edge, hence `w_i=-w_k` there;
connectedness and an odd cycle force every `w_i=0`.  Thus under the graph
hypothesis its image really has dimension `2(|J|-1)`.  Without that
hypothesis (5) is a parameterization of the unavoidable image, not a claim
that its parameters are always independent.

Call `Psi_(j,r)` **gauge-rigid** when equality holds in (6).

The large line-parabolic stabilizer of the individual equation (3) does
not automatically enlarge this kernel.  At the quotient site it acts by an
endomorphism of `bar V_j`, and the image in (5) is closed under every such
endomorphism; at other sites it changes `Psi` itself rather than producing
a kernel vector of the fixed map.  See
`fixed-star-parabolic-gauge-audit.md` for the exact tangent calculation and
a five-site symbolic audit.  The common stabilizer of all three equations
is only the diagonal target torus.

The quotient of (3) at site `j` has zero right side.  Using (2) and grouping
the ordered pairs `(i,k)` and `(k,i)` gives the exact common-power identity

\[
 \left(
   \bar z_{j,r},
   \bigl(z_{i,r}\otimes\bar q_{jk}
          +\bar q_{ji}\otimes z_{k,r}\bigr)_{i<k}
 \right)\in\ker\Psi_{j,r}.                               \tag{7}
\]

This is the extra information absent from an arbitrary assignment of the
one-hole tensors `C_j`.

## 3. Gauge rigidity makes every row coordinatewise

Let `G_3(q)` be the graph on `J` whose edge `ik` is present when the
`3 by 3` matrix `q_ik` has rank three.

**Lemma 3.1.**  Fix `j,r`.  Suppose `Psi_(j,r)` is gauge-rigid and
`G_3(q)[J\setminus{j}]` is connected, spanning, and nonbipartite.  Then

\[
                         z_{j,r}\in\mathbb Ce_r,          \tag{8}
\]

and, for every distinct `i,j,k`,

\[
 z_{i,r}\otimes\bar q_{jk}
       +\bar q_{ji}\otimes z_{k,r}=0.                    \tag{9}
\]

**Proof.**  Gauge rigidity writes the vector in (7) as
`G_(j,r)(w)`.  Hence its `{i,k}` component is

\[
 z_{i,r}\otimes\bar q_{jk}+\bar q_{ji}\otimes z_{k,r}
             =-(w_i+w_k)^{(j)}\otimes q_{ik}.             \tag{10}
\]

Contract the barred `j` slot by an arbitrary functional.  The left side,
viewed as a matrix between `V_i` and `V_k`, has rank at most two.  On an
edge of `G_3(q)`, the right side is a scalar multiple of the rank-three
matrix `q_ik`.  Its scalar must vanish.  Since the functional was
arbitrary,

\[
                         w_i+w_k=0
\]

on every rank-three edge.  Connectedness and an odd cycle force every
`w_i=0` over characteristic different from two.  Equations (5), (7), and
(10) now give (8)--(9). `QED`

Assume the hypotheses of Lemma 3.1 for every pair `(j,r)`.  Write

\[
                         z_{j,r}=a_{j,r}e_r.              \tag{11}
\]

Then (9) becomes, after quotienting the endpoint at `j`,

\[
 a_{i,r}e_r^{(i)}\otimes\bar q_{jk}
 +a_{k,r}\bar q_{ji}\otimes e_r^{(k)}=0                 \tag{12}
\]

for all distinct `i,j,k`.

## 4. The common-power support collapse

For a fixed color `r`, put

\[
                         S_r=\{j:a_{j,r}\ne0\}.           \tag{13}
\]

It is nonempty because the right side of (3) is nonzero.

**Lemma 4.1.**  If all three equations (3) hold, then

\[
                              |S_r|\le2                  \tag{14}
\]

for every `r`.

**Proof.**  Suppose `S_r` contains three distinct sites and fix a site
`j` outside `S_r`.  For active `i,k`, equation (12), first quotienting the
`i` slot by `Ce_r` and then the `k` slot, shows

\[
                 \bar q_{ji}=u_i^{(j)}\otimes e_r^{(i)}
                 \quad(i\in S_r).                        \tag{15}
\]

Equation (12) then says

\[
                         a_{i,r}u_k+a_{k,r}u_i=0.          \tag{16}
\]

Applying (16) to three active indices and using `2!=0` forces all their
`u_i` to vanish.  Pairing one active index with any inactive `k` in (12)
also gives `bar q_jk=0`.  Thus every edge incident with `j` has its
endpoint-`j` factor in `Ce_r`.

If `J\setminus S_r` has at least two sites, two sites have this forced
property.  In any term of either equation (3) for a different color, the
star deletes only one site; at least one of those two sites is covered by a
`q`-edge and therefore has color `r`, not the required different constant
color.  The other target equation would be zero, a contradiction.

If the complement is empty, every `j` has at least three active indices
different from it, so the same argument makes every endpoint of every
`q`-edge color `r`.  If the complement is the singleton `{t}`, apply the
argument first at `t` and then at every active `j`, which still has at least
three other active indices because `|J|>=5`.  Again `q` is everywhere
color `r`.  Both cases contradict either of the other two equations in
(3).  This proves (14). `QED`

The last possibility disappears once there are at least seven sites.

**Lemma 4.2.**  If `|J|>=7`, then `|S_r|!=2`.

**Proof.**  Suppose `S_r={a,b}` and put `T=J\setminus{a,b}`.  For distinct
`j,k in T`, use (12) with the active index `a` and the inactive index `k`.
It gives `bar q_jk=0`.  Interchanging `j,k` shows

\[
                         q_{jk}\in
             \mathbb C(e_r^{(j)}\otimes e_r^{(k)})
             \qquad(j,k\in T).                           \tag{17}
\]

Consider a term contributing to the all-`s` coefficient of (3), where
`s!=r`.  After its one star site is chosen, the remaining sites are covered
by a perfect matching of `q`.  Such a matching cannot use an edge internal
to `T`, by (17).  Hence every remaining vertex of `T` must be paired to
one of the two sites `a,b`.  At most two can be paired this way, whereas
at least

\[
                         |T|-1=|J|-3\ge4
\]

remain after deleting the star site.  No such matching exists, so the
all-`s` coefficient is zero, contradicting (3). `QED`

Combining the lemmas proves the main result.

**Theorem 4.3 (fixed-star three-hole gauge dichotomy).**  Let `|J|>=7` be
odd and suppose (3) holds.  Assume, for every site `j` and color `r`, that

1. `Psi_(j,r)` is gauge-rigid; and
2. `G_3(q)[J\setminus{j}]` is connected, spanning, and nonbipartite.

Then there are three distinct sites `j_0,j_1,j_2` and nonzero scalars
`alpha_r` such that

\[
 z_r=\alpha_re_r^{(j_r)},\qquad
 C_{j_r}=\alpha_r^{-1}e_r^{\otimes(J\setminus\{j_r\})}
 \quad(r=0,1,2).                                         \tag{18}
\]

**Proof.**  Lemmas 3.1, 4.1, and 4.2 say that every `S_r` is a singleton.
Substitution in (3) gives (18).  The sites are distinct because one nonzero
tensor `C_j` cannot be proportional to two different constant-color
tensors. `QED`

In particular, full rank of every matrix `q_ik` supplies hypothesis 2.
The theorem says that a counterexample without a pure fixed star must lie
on the explicit union of the extra-kernel determinantal loci of the maps
(4), or on a low-rank graph locus.

There is an unconditional global consequence for a full source.

**Corollary 4.4 (the everywhere-generic branch is impossible).**  Let
`B` have even cardinality at least eight and suppose hypothetically that
`H_B(A)=Delta_(B,3)`.  Then some vertex `p` has the following property.
For the internal quadratic `q=A|_(B\setminus{p})`, either

1. some `Psi_(j,r)` has a kernel strictly larger than its expansion-gauge
   image; or
2. some graph `G_3(q)[(B\setminus{p})\setminus{j}]` is disconnected,
   nonspanning, or bipartite.

**Proof.**  Otherwise apply Theorem 4.3 at every vertex `p`.  Every color
row at `p` then consists of one nonzero cell, its color at the opposite
endpoint is the same, and the three centers are distinct.  Hence the cells
of colors zero, one, and two form three edge-disjoint perfect matchings
`P_0,P_1,P_2` of `B`, with no other cells present.

The standard three-one-factors lemma gives a fourth perfect matching in
`P_0 union P_1 union P_2`.  It is not one of the `P_r`, so coloring each
vertex by the color of its fourth-matching edge gives a mixed coloring.
At every vertex that color has exactly one compatible incident cell, making
the fourth matching the unique compatible matching.  Its nonzero product
contradicts the vanishing mixed coefficient of `Delta_(B,3)`. `QED`

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017), published as Thm 1 of Chandran-Gajjala,
arXiv:2202.05562, and in multigraph form as Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

## 5. Exact audit and nonvacuity

Run

```text
uv run python computations/verify_fixed_star_three_hole_dichotomy.py
```

The checker works over `F_1000003` and independently:

1. enumerates all matchings defining `C_j` and `D_ijk`;
2. verifies the factorization identity (7) for random `q,z`;
3. constructs all expansion gauges (5) and verifies that they lie in the
   kernel; and
4. finds full-rank-edge integer specializations with

\[
\begin{array}{c|c|c|c}
|J|&\dim\operatorname{dom}\Psi&\operatorname{rank}\Psi&
\dim\ker\Psi\\ \hline
5&110&102&8=2(|J|-1)\\
7&272&260&12=2(|J|-1)\\
9&506&490&16=2(|J|-1).
\end{array}
\]

A maximal-rank minor nonzero modulo the prime is a nonzero integer minor.
Thus, at each audited order, the gauge-rigid locus is nonempty Zariski open
over `C`.  Site and color symmetry makes this true for every `(j,r)`; the
finite intersection of these opens, together with the full-rank edge locus,
is nonempty in the irreducible affine space of quadratics.  Hence the
hypotheses of Theorem 4.3 describe a genuine generic branch at `|J|=7,9`,
not a formally impossible one.  No all-order generic-rank assertion is used
in the theorem.
