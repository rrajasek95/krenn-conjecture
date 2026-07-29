# Source derivatives force a Hessian-degenerate or row-sparse chart

## Outcome

Keeping the actual source quadratic gives a uniform conditional obstruction
which is invisible in the target's apolar algebra.  Delete two vertices and
let `q` be the quadratic on the remaining sites.  Multiplication by
`q^(m-2)` is the Hessian block of the matching-power map.  It always has a
vertex-scaling kernel.  If it has *only* that kernel, and the rank-three
edges of `q` contain a connected spanning nonbipartite graph, then every
color row from either deleted vertex is supported on at most two of the
remaining sites.

Consequently, a putative solution in a dense full-matrix chart must lie on
the explicit determinantal locus where this source Hessian has an extra
kernel.  Equivalently, a gauge-rigid pair deletion forces severe row
sparsity.  This does not yet rule out the singular/sparse escape, but it is
a genuine relative invariant of `(Q,Q^m)`, rather than a target-only
Hessian test.

## 1. The three first derivatives are the whole equation

Let

\[
 \mathcal Z_B=\bigotimes_{v\in B}(\mathbb C\oplus V_v),
 \qquad V_vV_v=0,
\]

let `|B|=n=2m`, and let

\[
 Q=\sum_{u<v}A_{uv}\in(\mathcal Z_B)_2.                    \tag{1}
\]

The matching equation is

\[
                         Q^m=m!\Delta_{B,3}.                \tag{2}
\]

Fix `v`.  There is a unique decomposition

\[
 Q=Q_{-v}+\sum_{c=0}^2x_{v,c}L_{v,c},                     \tag{3}
\]

where `L_(v,c)` is a linear element on `B\{v}` whose component at `u`
is the color-`c` row of `A_(vu)`.  Since two terms using `v` multiply to
zero,

\[
 Q^m=m\sum_c x_{v,c}L_{v,c}Q_{-v}^{m-1}.                  \tag{4}
\]

Thus (2) is equivalent, already at this one fixed vertex, to the three
factorizations

\[
 L_{v,c}Q_{-v}^{m-1}
   =(m-1)!\prod_{u\ne v}x_{u,c},\qquad c=0,1,2.            \tag{5}
\]

There cannot be an exact `Q` satisfying all three full tensor equations
(5) but not (2): every top-support monomial contains exactly one variable
at `v`, so its three contractions determine it.  The new information must
therefore come from resolving the common power in (5), not from treating
the equations as independent output tests.

## 2. Exact second-contraction identity

Fix distinct `u,v`, put

\[
 W=B\setminus\{u,v\},\qquad |W|=2m-2,
\]

and decompose (1) as

\[
 Q=q+\sum_cx_{v,c}p_c+\sum_dx_{u,d}s_d
       +\sum_{c,d}a_{cd}x_{v,c}x_{u,d}.                   \tag{6}
\]

Here `q` is the quadratic internal to `W`; `p_c,s_d` are linear elements
on `W`; and `a_cd=A_(vu)(c,d)`, with endpoint order understood.
Extracting the coefficient of `x_(v,c)x_(u,d)` in (2) gives

\[
 \boxed{\quad
 \bigl(a_{cd}q+(m-1)p_cs_d\bigr)q^{m-2}
  =(m-1)!\delta_{cd}\prod_{w\in W}x_{w,c}.
 \quad}                                                     \tag{7}
\]

The two terms correspond respectively to using the direct edge `uv`, or
one star edge at each of `u,v`.  Formula (7) retains all complex
cancellation and all asymmetric endpoint matrices.

Define the source-Hessian block

\[
 \mathcal H_q:(\mathcal Z_W)_2\longrightarrow(\mathcal Z_W)_{|W|},
 \qquad Z\longmapsto Zq^{m-2}.                             \tag{8}
\]

It is, up to the nonzero scalar `m-1`, the derivative at `q` of the
top matching power `q -> q^(m-1)`.

## 3. Its unavoidable gauge kernel

For `alpha=(alpha_w)_(w in W)` with `sum_w alpha_w=0`, define

\[
 (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.                \tag{9}
\]

Every perfect-matching monomial in the derivative acquires the factor

\[
 \sum_{ij\in M}(\alpha_i+\alpha_j)=\sum_{w\in W}\alpha_w=0.
\]

Hence

\[
 \mathcal G_q:=\{Z^\alpha:\sum_w\alpha_w=0\}
       \subseteq\ker\mathcal H_q.                          \tag{10}
\]

Call `q` **gauge-rigid** when equality holds in (10).  This is the largest
rank its Hessian block can have; failure is an explicit determinantal
condition on the entries of `q`.

## 4. A linear annihilator lemma

For a linear element `p=sum_i p_i` on a square-zero site algebra, define
its site support by

\[
                    \operatorname {supp}_s(p)=\{i:p_i\ne0\}.
\]

**Lemma 4.1.**  Over a field of characteristic different from two, the map

\[
 (\mathcal Z_W)_1\longrightarrow(\mathcal Z_W)_2,
 \qquad s\longmapsto ps                                   \tag{11}
\]

is injective if and only if `|supp_s(p)|>=3`.

**Proof.**  If `ps=0`, then for every `i ne j`,

\[
                         p_i\otimes s_j+s_i\otimes p_j=0.  \tag{12}
\]

On three sites where `p` is nonzero, the equality of the two simple tensors
forces `s_i=lambda_i p_i` and `lambda_i+lambda_j=0` for every pair.
Three such equations give `2lambda_i=0`, hence all three scalars vanish.
Pairing any other site with one of these three then gives `s_j=0`.

Conversely, if `p` is supported at one site, any nonzero vector at that
same site annihilates it.  If it is supported at two sites `i,j`, the
linear element with components `s_i=p_i,s_j=-p_j` is a nonzero annihilator.
The zero case is immediate. `QED`

## 5. Gauge-rigid mixed curvature forces sparse rows

Let `G_3(q)` be the graph on `W` whose edge `ij` is present when the matrix
`q_ij in V_i tensor V_j` has rank three.

**Theorem 5.1 (source-Hessian dichotomy).**  Suppose (2) holds with
`m>=3`.  Fix `u,v` and use (6).  If

1. `q` is gauge-rigid, and
2. `G_3(q)` is connected, spanning, and nonbipartite,

then

\[
 |\operatorname {supp}_s(p_c)|\le2,
 \qquad |\operatorname {supp}_s(s_c)|\le2
 \quad(c=0,1,2).                                           \tag{13}
\]

**Proof.**  First fix `c ne d`.  The mixed instance of (7) says

\[
                    a_{cd}q+(m-1)p_cs_d\in\ker\mathcal H_q.
\]

Gauge rigidity supplies `alpha` with `sum_i alpha_i=0` such that, on each
pair `ij`,

\[
 (\alpha_i+\alpha_j-a_{cd})q_{ij}
  =(m-1)(p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}).  \tag{14}
\]

The right side has matrix rank at most two.  On every edge of `G_3(q)`,
the scalar on the left must therefore vanish:

\[
                         \alpha_i+\alpha_j=a_{cd}.          \tag{15}
\]

Put `beta_i=alpha_i-a_cd/2`.  Along every edge of `G_3(q)`, (15) says
`beta_i=-beta_j`.  Connectedness and an odd cycle force every `beta_i=0`.
Thus `alpha_i=a_cd/2` on all of `W`; summing and using characteristic zero
gives `a_cd=0` and `alpha=0`.  Equation (14) now says simply

\[
                              p_cs_d=0.                    \tag{16}
\]

By Lemma 4.1, if `p_c` has support at least three, then `s_d=0`.

It remains to use all three colors.  At most one of `s_0,s_1,s_2` can be
zero.  Indeed, if `s_d=0`, the `d,d` instance of (7) gives

\[
                  a_{dd}q^{m-1}=(m-1)!\prod_{w\in W}x_{w,d}, \tag{17}
\]

so `q^(m-1)` is a nonzero scalar multiple of the color-`d` pure tensor.
The same conclusion for a second color would make two linearly independent
pure tensors proportional.  Hence, if some `p_c` had support at least
three, (16) for the two colors `d ne c` would force two of the `s_d` to
vanish, a contradiction.  This proves the first half of (13).  Interchange
`u,v` to prove the second half. `QED`

The proof uses only mixed second contractions plus the three diagonal ones
needed for the final two-zero exclusion.  No positivity, symmetry, or
termwise matching inference occurs.

## 6. Consequences and exact limitation

If all matrices in the pair-deleted internal chart have rank three, then
`G_3(q)` is complete and satisfies hypothesis 2.  If the Hessian is also
gauge-rigid, (13) says that each of the six endpoint color rows reaches at
most two internal sites.  In particular, a source with full-rank matrices
on every pair cannot solve (2) in a gauge-rigid chart: its endpoint rows
are nonzero at every one of the at least four sites in `W`.

Thus every fully dense hypothetical solution must have an extra source-
Hessian kernel after every applicable pair deletion.  More generally, the
only escapes from Theorem 5.1 are concrete:

* an extra kernel vector beyond vertex scaling;
* a rank-three graph which is disconnected, nonspanning, or bipartite; or
* the row-sparse conclusion (13).

The theorem does not yet exclude those singular and low-rank regimes.  The
connected bipartite escape in the displayed list is sharpened in
[`source-hessian-bipartite-rankdrop.md`](source-hessian-bipartite-rankdrop.md):
if `G_3(q)` is merely connected and every color row of both deleted stars
is nonzero at every internal site, the complete pair/output flattening has
rank at most two, a contradiction.  Thus the gauge-rigid connected branch
always forces an actual zero star row; bipartiteness alone is not an
all-row-full escape.

The theorem also explains why an injective-Hessian assumption would be incorrect:
the `|W|-1` vertex gauges (10) are always present.

The singular kernel also cannot simply be integrated away:
`notes/source-hessian-nonintegrability-countermodel.md` gives an
entry-minimal exact Hamilton family whose pair Hessians are all
extra-degenerate and an explicit full-fiber tangent which is obstructed at
second order.

`computations/verify_source_hessian_dichotomy.py` constructs exact integer
specializations, certified modulo `1000003`, on four and six internal sites
for which every internal edge has rank three and

\[
 \dim\ker\mathcal H_q=|W|-1.
\]

It also constructs the independent gauge vectors and verifies directly
that all are killed.  Hence the gauge-rigid/full-rank hypotheses are
nonvacuous (and define nonempty Zariski-open charts in those orders), rather
than a formal condition which can never occur.
