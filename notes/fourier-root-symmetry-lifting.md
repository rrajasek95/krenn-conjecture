# Fourier root symmetry: a conditional lift and an active counterfamily

## Outcome

Let `B` have even size `n=2m`, let

\[
 \mathcal Z_B=\bigotimes_{v\in B}(\mathbb C\oplus V_v),
 \qquad V_v^2=0,
\]

and in the Fourier basis `f_0,f_1,f_2` put

\[
 \mathsf Z_B=\sum_{\sum_vs_v=0\pmod3}\prod_v f_{v,s_v}.
\tag{1}
\]

Write `g f_s=omega^s f_s`, where `omega` is a primitive cube root of
unity.  This note gives three exact conclusions about a hypothetical
quadratic `q` satisfying

\[
                         {q^m\over m!}=\mathsf Z_B.       \tag{2}
\]

1. The global charge symmetry cannot lift even **projectively** through the
   ordinary vertex-scalar gauge: there are no nonzero `t_v` such that

   \[
                           gq=(t_ut_vq_{uv})_{u<v}.       \tag{3}
   \]

   In particular no target-stabilizing change of local bases can make a
   source charge-homogeneous.  This strengthens Proposition 2.1 of
   `fourier-zero-sum-wick-obstruction.md`, which treated the strict lift
   `gq=q`.

2. Suppose the source Hessian at `q` has only the ordinary vertex-gauge
   kernel.  Then `q` and `gq` cannot lie on the same irreducible component
   of the fiber of (2).  Thus a gauge-rigid solution would force at least
   three distinct components, cyclically permuted by `g`.  This is a
   precise conditional symmetry-lifting lemma: componentwise uniqueness
   modulo gauges would finish the Fourier route.

3. Invariance of the top power cannot supply the missing componentwise
   statement.  For every `m>=3` there is an exact quadratic `q_(2m)` with
   connected underlying support and a nonzero cofactor at every supported
   edge such that

   \[
                    q_{2m}^m=(gq_{2m})^m\ne0,            \tag{4}
   \]

   but `gq_(2m)` is not a vertex-scalar gauge of `q_(2m)`.  The output is
   concise at every site, and `q_(2m)` has nonzero parts in all three charge
   sectors.  Its output is nevertheless a proper charge-zero face, not the
   full tensor (1).  Therefore the full transversal coefficient values in
   (2), rather than root-of-unity comparison, connected support, edge
   activity, conciseness, or sector nonvanishing alone, are indispensable.

The exact audit is
`computations/verify_fourier_symmetry_lifting.py`.

## 1. The unavoidable root-comparison annihilator

For every quadratic `q`, `g` acts on the site-square-zero algebra by an
algebra automorphism.  Since (1) is fixed by `g`, equation (2) gives

\[
                            q^m=(gq)^m.                  \tag{5}
\]

Factoring the difference in the commutative algebra gives

\[
 (gq-q)\,R_m(q,gq)=0,
 \qquad
 R_m(q,gq)=\sum_{j=0}^{m-1}(gq)^j q^{m-1-j}.             \tag{6}
\]

This is an equality in top site degree.  The algebra has many zero divisors,
so (6) has no cancellation implication.  Section 4 gives connected,
edge-active examples in which both factors relevant to (6) are nontrivial.
For an actual solution, Section 2 shows more: `gq-q` is nonzero and the two
quadratics are not even in the same vertex-scalar orbit.

## 2. Projective charge lifting is impossible

For a quadratic `q`, let `S(q)` be the graph on `B` whose edge `uv` is
present exactly when the aggregate matrix `q_uv` is nonzero.

**Lemma 2.1 (the support graph is connected).**  Every solution of (2) has
connected support graph.

**Proof.**  If a connected component of `S(q)` has odd order, there is no
supported perfect matching, so the top power is zero.  Hence every component
has even order.  If there are at least two components and `C` is one of
them, the matching tensor factors across `C | (B\C)` and consequently has
flattening rank one across that cut.

On the other hand,

\[
 \mathsf Z_B=\sum_{r\in\mathbb Z/3}
       \mathsf Z_C^{(r)}\otimes\mathsf Z_{B\setminus C}^{(-r)},
 \qquad
 \mathsf Z_C^{(r)}=
       \sum_{\sum_{v\in C}s_v=r}\prod_{v\in C}f_{v,s_v}. \tag{7}
\]

The three vectors on each nonempty shore are nonzero with disjoint supports,
so this flattening has rank three.  This contradicts the factorization.
`QED`

We use the following elementary graph cocycle fact.

**Lemma 2.2 (charge-shift strictification).**  Let `S` be a connected graph
with a perfect matching.  Suppose `t_v in C^*` and, for every edge `uv`,

\[
                         t_ut_v=\omega^{r_{uv}}           \tag{8}
\]

for some `r_uv in Z/3`.  Then there are `k_v in Z/3` such that

\[
                         r_{uv}=k_u+k_v                  \tag{9}
\]

on every edge.  If additionally `product_v t_v=1`, they may be chosen with

\[
                         \sum_vk_v=0.                    \tag{10}
\]

**Proof.**  Work first in the quotient group `C^*/mu_3`.  Equation (8)
says that endpoint classes are mutual inverses.  If `S` is bipartite, choose
a representative `tau` for the common class on one shore.  Then

\[
 t_v=\tau\omega^{j_v}\quad(v\in L),
 \qquad
 t_v=\tau^{-1}\omega^{j_v}\quad(v\in R),                \tag{11}
\]

and `k_v=j_v` gives (9).

If `S` is not bipartite, an odd cycle says that the common quotient class
equals its inverse.  Choose a representative `tau` and write

\[
                \tau^2=\omega^h,
 \qquad t_v=\tau\omega^{j_v}.                            \tag{12}
\]

Choose `c in Z/3` with `2c=h` and put `k_v=j_v+c`; this again gives (9).
These two cases exhaust connected graphs.

Finally choose a perfect matching `M` of `S`.  Equations (8)--(9) give

\[
 \prod_vt_v=\prod_{uv\in M}t_ut_v
    =\omega^{\sum_{uv\in M}(k_u+k_v)}
    =\omega^{\sum_vk_v}.                                \tag{13}
\]

Thus `product t_v=1` implies (10). `QED`

**Theorem 2.3 (no projective charge lift).**  If (2) holds for `n>=4`,
then (3) is impossible for every collection of nonzero vertex scalars
`t_v`.

**Proof.**  Comparing top powers in (3) gives

\[
                  \mathsf Z_B=H(gq)=\left(\prod_vt_v\right)H(q),
\]

so `product_v t_v=1`.  For every nonzero scalar entry `q_uv(a,b)`, equation
(3) says

\[
                         t_ut_v=\omega^{a+b}.             \tag{14}
\]

Lemma 2.1 makes `S(q)` connected, and a nonzero top coefficient supplies a
perfect matching.  Lemma 2.2 therefore gives charges `k_v` of sum zero such
that every supported cell obeys

\[
                             a+b=k_u+k_v.                \tag{15}
\]

Now translate the Fourier labels at site `v` by `-k_v`.  Because their sum
is zero, these local translations permute the summands of (1) and hence are
a target stabilizer.  In the translated basis every supported covariance
cell has endpoint-charge sum zero by (15).  The transformed source still
realizes (1), but it is now strictly `Z/3`-invariant.

For completeness, take `z in {0,1,2}` congruent to `n` modulo three and
choose a coloring having `z` shifted charges zero and `n-z` shifted charges
one.  Its total charge is zero and `n-z>0`, so its target coefficient is
nonzero.  Yet a charge-zero covariance must pair every charge one with a
charge two, and this coloring has no charge-two site.  Every matching term
therefore vanishes, a contradiction. `QED`

If an arbitrary target-stabilizing local change of bases made `q`
charge-homogeneous, its transformed quadratic would itself contradict the
last paragraph.  Thus Theorem 2.3 also covers the phrase "up to target
stabilizer"; the nontrivial content of the theorem is that even the weaker
projective relation (3) can be strictified by a target stabilizer.

## 3. A componentwise lifting lemma

Let `Q_B` be the affine space of block-off-diagonal quadratics and let

\[
 \Phi:Q_B\longrightarrow (\mathcal Z_B)_n,
 \qquad \Phi(q)={q^m\over m!}.                           \tag{16}
\]

The ordinary vertex torus

\[
 T=\{(t_v)\in(\mathbb C^*)^B:\prod_vt_v=1\}             \tag{17}
\]

acts on quadratics by `(t.q)_uv=t_ut_vq_uv` and fixes every top-degree
output.  Its tangent space at `q` is

\[
 \mathfrak g_q=
 \{((a_u+a_v)q_{uv})_{u<v}:\sum_va_v=0\}.               \tag{18}
\]

The differential of (16) is multiplication by `q^(m-1)/(m-1)!`.

**Theorem 3.1 (componentwise symmetry lifting).**  Suppose (2) holds and

\[
                         \ker(d\Phi_q)=\mathfrak g_q.    \tag{19}
\]

If `q` and `gq` lie on the same irreducible component of the
scheme-theoretic fiber `Phi^(-1)(Z_B)`, then `gq` belongs to the vertex-torus
orbit `Tq`.

Consequently the hypotheses are incompatible with (2).  Equivalently, at
any hypothetical solution satisfying (19), the three points

\[
                              q,\quad gq,\quad g^2q       \tag{20}
\]

lie on three distinct irreducible components, cyclically permuted by `g`.

**Proof.**  Put `d=dim(Tq)`.  The orbit lies in the fiber, so the local
dimension of the fiber at `q` is at least `d`.  By (19), its Zariski tangent
space has dimension exactly `d`.  Hence `q` is a regular point, lies on a
unique irreducible component `C` of dimension `d`, and `Tq` is a dense open
orbit in `C`.

The charge action is an automorphism of the fiber.  It carries (19) to the
same statement at `gq`, so `T(gq)` is likewise a dense open orbit in the
component through `gq`.  If that component were `C`, the two open torus
orbits would intersect and hence would be equal.  This would give
`gq in Tq`, contrary to Theorem 2.3.  Thus `C,gC,g^2C` are distinct. `QED`

Theorem 3.1 identifies the exact global input missing from a Hessian-only
argument.  Gauge-only tangent kernel proves local orbit rigidity, but a
discrete target symmetry may still permute different components of the
source fiber.

## 4. Connected active counterexamples to root cancellation

The missing component statement does not follow from (5), even after
connectedness, edge activity, mode conciseness, and nonvanishing of all
three source charge sectors are imposed.  We give an exact counterfamily at
every even order at least six.

Start on vertices `0,1,2,3`.  Put

\[
 u_r=\sum_{s=0}^2\omega^{rs}f_s
\]

and use the three one-factors

\[
 M_0=01\mid23,\qquad M_1=02\mid13,\qquad M_2=03\mid12.  \tag{21}
\]

On both edges of `M_r`, put `u_r tensor u_r`.  The only three perfect
matchings are (21), and Fourier orthogonality gives

\[
 H_4(Q)=\sum_{r=0}^2u_r^{\otimes4}
       =3\sum_{s_0+\cdots+s_3=0}f_{s_0}f_{s_1}f_{s_2}f_{s_3}
       =3\mathsf Z_{\{0,1,2,3\}}.                       \tag{22}
\]

For every additional pair `a,b`, put

\[
                         J_{ab}=\sum_{s=0}^2f_{a,s}f_{b,-s}             \tag{23}
\]

on the edge `ab`, and add four cross matrices:

\[
\begin{array}{c|c}
 0a&f_0\otimes f_1,\\
 1b&f_1\otimes f_1,\\
 0b&f_0\otimes f_1,\\
 1a&-f_1\otimes f_1.
\end{array}                                               \tag{24}
\]

All unlisted new edges are zero.  A perfect matching either uses `ab`, or
matches `a,b` across to `0,1`.  The latter case has exactly the two choices

\[
                         0a\mid1b,
 \qquad                 0b\mid1a,                       \tag{25}
\]

and their four-site tensors are equal and opposite.  With several added
pairs, at most one pair can use (25), so the same cancellation is independent
for every pair.  It follows exactly that

\[
 H_{2m}(q_{2m})
   =3\mathsf Z_{\{0,1,2,3\}}
       \otimes\bigotimes_{j=2}^{m-1}J_{2j,2j+1}.         \tag{26}
\]

This tensor is nonzero and fixed by the global charge action, proving (4).
It is concise at every site.  Indeed, on the first four sites its three
mode slices have disjoint supports indexed by the residue of the other
three charges, while on either endpoint of a new pair the three slices of
`J` force three different colors at the mate.  All three charge components
of the quadratic are nonzero already on
`A_01=u_0 tensor u_0`, which has all nine scalar entries.

The support graph is connected: every new vertex is joined to `0` or `1`
(and also to its mate).  Every supported edge has a nonzero cofactor.  For
an old edge, use its old complementary matching and choose the `(0,0)` cell
on all the new `J` edges; the resulting coefficient has charge zero at every
new site, whereas every cross term in (24) uses charge one there, so it
cannot cancel.  For `ab`, use any old matching and the other new `J` edges.
For a cross edge, its partner in (25), the edge `23`, and all other new `J`
edges give a nonzero completion.  Thus the construction has no cofactor-dead
bridge or hidden zero edge.

Finally `A_01=u_0 tensor u_0` has all nine entries equal to one.  The
corresponding entries of `gA_01` are `omega^(a+b)`, which are not a common
scalar multiple.  Hence no vertex scalars can satisfy (3).  In particular,
the nonzero factor `gq-q` in (6) is a genuine nongauge top-degree
annihilator.

The output (26) has `27*3^(m-2)=3^(m+1)` nonzero coefficients, while the
desired `2m`-site tensor (1) has `3^(2m-1)`.  For example, at six sites the
globally zero-sum coloring `(1,0,0,0,1,1)` is absent: its first four charges
sum to one and its last pair sums to two.  This construction is therefore
not a Krenn counterexample.  Its role is exact and narrower: it rules out
every attempt to deduce symmetry lifting merely by cancelling the factors
in (6), even after connectedness, nonzero edge cofactors, mode conciseness,
and nonvanishing of all three source charge sectors have been imposed.
