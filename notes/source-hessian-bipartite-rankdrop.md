# The connected rank-three boundary forces a zero star row

## 1. Outcome

The source-Hessian dichotomy of
[`source-derivative-hessian-dichotomy.md`](source-derivative-hessian-dichotomy.md)
used a connected **nonbipartite** graph of rank-three internal blocks.  On
that chart, gauge rigidity forces every row of either deleted star to meet
at most two internal sites.  This note closes the complementary connected
bipartite rank-drop branch whenever the two deleted stars are row-full.

More precisely, delete two vertices `p,q` and let `q_0` be the quadratic on
the remaining even set `W`.  If

1. the source Hessian of `q_0` has only its vertex-gauge kernel;
2. the graph of rank-three blocks of `q_0` is connected; and
3. every color row of every block from `p` or `q` to a site of `W` is
   nonzero,

then the nine two-deletion equations are impossible.  Gauge rigidity first
makes every off-diagonal polarized star product vanish on every rank-three
edge.  Those zero blocks force the six star rows into one common
bipartite-antipodal family.  Consequently the full `pq|W` flattening is a
sum of two simple tensors and has rank at most two, whereas ternary GHZ has
rank three.

Thus, for every deleted pair of a hypothetical source, at least one of the
following must occur: an extra source-Hessian kernel, a disconnected
rank-three internal graph, or a zero color row on one of the deleted stars.
This is an exact all-even restriction.  It does not by itself eliminate the
three remaining escape branches.

## 2. Pair equations and notation

Let `|W|=2r` and work in the square-free site algebra

\[
 \mathcal R_W=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
 \qquad V_iV_i=0.
\]

Write

\[
 Q={q_0^r\over r!},\qquad
 \mathcal H_{q_0}(Z)={Zq_0^{r-1}\over(r-1)!}.             \tag{1}
\]

Orient every incident block toward its named deleted endpoint, independently
of the numerical ordering of the vertices:

\[
 A_{p\mid i}\in V_p\otimes V_i,
 \qquad A_{q\mid i}\in V_q\otimes V_i,
 \qquad A_{p\mid q}\in V_p\otimes V_q.                  \tag{2a}
\]

Thus, if a stored unordered block has the reverse endpoint order, it is
transposed before (2a) is used.  Let `p_c` be the color-`c` row from `p` to
`W`, let `s_d` be the color-`d` row from `q` to `W`, and let `a_cd` be the
`(c,d)` entry of `A_(p|q)`.  Explicitly,

\[
 p_c=\sum_{i\in W}p_{c,i},\quad
 p_{c,i}=(e_c^*\otimes\operatorname{id})A_{p\mid i},
 \qquad
 s_d=\sum_{i\in W}s_{d,i},\quad
 s_{d,i}=(e_d^*\otimes\operatorname{id})A_{q\mid i},    \tag{2}
\]

with `p_(c,i),s_(d,i) in V_i`.  Extracting the two deleted slots from a
hypothetical identity `H_B=Delta_(B,3)` gives the exact nine equations

\[
 \boxed{\quad
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q
       =\delta_{cd}X_c,
 \qquad 0\le c,d\le2,
 \quad}                                                   \tag{3}
\]

where

\[
                       X_c=\bigotimes_{i\in W}e_c^{(i)}. \tag{4}
\]

The normalization in (3) follows directly by sorting a perfect matching
according to whether it uses `pq` or sends `p,q` to two distinct sites of
`W`.  It retains arbitrary asymmetric endpoint matrices and all complex
cancellation.

For scalars `alpha_i` with `sum_i alpha_i=0`, the vertex gauge is

\[
 (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)(q_0)_{ij}.           \tag{5}
\]

Call `q_0` **gauge-rigid** if

\[
                  \ker\mathcal H_{q_0}
                    =\{Z^\alpha:\sum_i\alpha_i=0\}.      \tag{6}
\]

Let `G_3(q_0)` be the graph on `W` whose edge `ij` is present exactly when
the `3 by 3` block `(q_0)_ij` has rank three.

## 3. Off-diagonal products vanish on every rank-three edge

**Lemma 3.1 (rank-three zero blocks).**  Suppose `q_0` is gauge-rigid and
the equations (3) hold.  For every `c != d` and every edge
`ij in G_3(q_0)`,

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}=0.         \tag{7}
\]

**Proof.**  Since `H_(q_0)(q_0)=rQ`, the off-diagonal equation in (3)
says

\[
 p_cs_d+{a_{cd}\over r}q_0\in\ker\mathcal H_{q_0}.       \tag{8}
\]

By (6), there are scalars `alpha_i`, of sum zero, for which the `ij` block
of (8) is

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}
 =\left(\alpha_i+\alpha_j-{a_{cd}\over r}\right)
                    (q_0)_{ij}.                           \tag{9}
\]

The left side has matrix rank at most two.  On an edge of `G_3(q_0)`, a
nonzero scalar multiple of the right-hand block has rank three.  Therefore
the scalar in parentheses is zero, and then (9) gives (7).  No division by
an entry or minor of either star is used.  \(\square\)

## 4. Connected off-diagonal zero blocks synchronize all six rows

The following elementary lemma is the new bipartite-boundary input.  The
spaces `V_i` need not be identified with one another.

**Lemma 4.1 (six-row antipodal synchronization).**  Let `F` be a connected
graph with at least one edge.  Suppose vectors

\[
 p_{c,i},s_{d,i}\in V_i
 \qquad(i\in V(F),\ 0\le c,d\le2)                         \tag{10}
\]

are all nonzero and satisfy

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}=0
 \quad(ij\in E(F),\ c\ne d).                             \tag{11}
\]

Then `F` is bipartite.  There are a sign `sigma_i in {+1,-1}` which changes
across every edge, nonzero local vectors `z_i in V_i`, and nonzero scalars
`t_c,u_d`, independent of `i`, such that

\[
             p_{c,i}=t_cz_i,
 \qquad      s_{d,i}=u_d\sigma_i z_i.                    \tag{12}
\]

**Proof.**  Fix `c != d` and an edge `ij`.  Rearranging (11) equates two
nonzero simple tensors.  Uniqueness of the factors of a nonzero simple
tensor gives unique nonzero scalars `lambda_i^(cd),lambda_j^(cd)` with

\[
 s_{d,i}=\lambda_i^{cd}p_{c,i},\qquad
 s_{d,j}=\lambda_j^{cd}p_{c,j},\qquad
 \lambda_j^{cd}=-\lambda_i^{cd}.                         \tag{13}
\]

At a vertex incident with several edges the scalar in (13) is unique, so
connectivity propagates it through all of `F`.  It alternates sign across
each edge and never vanishes.  Hence `F` is bipartite and, for a fixed
bipartition sign `sigma`,

\[
             s_{d,i}=\lambda_{cd}\sigma_i p_{c,i}        \tag{14}
\]

with one nonzero scalar `lambda_cd` independent of `i`.

For two colors `c,c'`, choose the third color `d`, so that
`d != c,c'`.  Comparing the two expressions (14) for the same nonzero
vector `s_(d,i)` shows that `p_(c,i)` and `p_(c',i)` differ by a scalar
which is independent of `i`.  Thus all three `p` rows have the form
`p_(c,i)=t_cz_i`.  Substitution into (14), choosing any `c != d`, gives
the second formula in (12), with a scalar depending only on `d`.
\(\square\)

The availability of a third color is essential in the comparison step.
For two colors, (14) couples only the two crossed pairs and need not put all
four rows on one common family.

## 5. The rank-two flattening contradiction

**Theorem 5.1 (connected rank-three pair obstruction).**  Suppose the
nine equations (3) hold.  Assume

1. `q_0` is gauge-rigid;
2. `G_3(q_0)` is connected; and
3. `p_(c,i)` and `s_(d,i)` are nonzero for every `i,c,d`.

Then a contradiction follows.

**Proof.**  Lemma 3.1 supplies (11) on `F=G_3(q_0)`, and Lemma 4.1 gives
(12).  Put

\[
 z=\sum_i z_i,\qquad z^\sigma=\sum_i\sigma_i z_i,
 \qquad R=\mathcal H_{q_0}(zz^\sigma).                   \tag{15}
\]

Linearity of the Hessian and (12) turn every equation in (3) into

\[
            \delta_{cd}X_c=a_{cd}Q+t_cu_dR.              \tag{16}
\]

Package the nine equations as one tensor in
`(V_p tensor V_q) tensor (tensor_(i in W)V_i)`.  Its left side is the
ternary target flattening

\[
                  \sum_{c=0}^2E_{cc}\otimes X_c,         \tag{17}
\]

which has Schmidt rank three: both triples in (17) are linearly
independent.  Its right side, by (16), is

\[
             (a_{cd})_{c,d}\otimes Q
              +(t_cu_d)_{c,d}\otimes R,                  \tag{18}
\]

a sum of at most two simple tensors.  It has Schmidt rank at most two,
contradicting (17).  \(\square\)

**Corollary 5.2 (pair rank-drop trichotomy).**  For every pair `p,q` in a
hypothetical exact ternary source, with internal quadratic `q_0` on `W`, at
least one of the following holds.

1. `ker H_(q_0)` properly contains the vertex-gauge space;
2. `G_3(q_0)` is disconnected; or
3. for some internal site `i` and color `c`, the color-`c` row of
   the endpoint-oriented block `A_(p|i)` or `A_(q|i)` is zero.

In particular, the formerly open connected bipartite rank-three branch
cannot be an all-row-full escape from the source-Hessian argument.

## 6. Scope and audit

The theorem is uniform in `|W|` and uses the complete complex tensor
equations.  It does not assume same colors at the two ends of an edge,
rank-one source cells, positivity, or termwise vanishing of a mixed
coefficient.  Gauge rigidity is still a genuine hypothesis, and the
extra-kernel branch is known not to integrate automatically.

There is no hidden nonzero-block localization in the argument.  A zero
internal block `(q_0)_ij` simply is not an edge of `G_3(q_0)` and is never
divided by.  Rank-one and rank-two internal blocks are treated the same
way.  If an entire deleted-star block is zero, or merely one of its three
endpoint rows is zero, alternative 3 of Corollary 5.2 holds literally.
Otherwise all local vectors required by Lemma 4.1 are nonzero.  Hence the
three alternatives exhaust zero blocks, rank drops, and asymmetric endpoint
orders without an omitted boundary case.

[`verify_source_hessian_bipartite_rankdrop.py`](../computations/verify_source_hessian_bipartite_rankdrop.py)
performs two exact checks over a large prime.  It finds a rational
four-site internal quadratic whose rank-three graph is exactly `K_(2,2)`
while its Hessian kernel is precisely the three-dimensional vertex-gauge
space, proving that the bipartite rank-drop hypotheses are nonvacuous.  It
then constructs the antipodal family (12), checks all six off-diagonal
zero-block systems, and verifies directly that the nine responses have
output-span rank at most two.

For reference, with shores `{0,2}` and `{1,3}`, the integer specialization
found on the first deterministic trial is

\[
\begin{array}{c|c}
01&\begin{psmallmatrix}15&18&1\\22&13&14\\6&15&8\end{psmallmatrix}\\[2mm]
02&\begin{psmallmatrix}134&69&98\\252&150&272\\230&129&214\end{psmallmatrix}\\[2mm]
03&\begin{psmallmatrix}5&10&21\\6&4&22\\17&2&9\end{psmallmatrix}\\[2mm]
12&\begin{psmallmatrix}10&15&13\\2&3&12\\17&13&19\end{psmallmatrix}\\[2mm]
13&\begin{psmallmatrix}20&104&80\\48&242&172\\54&296&256\end{psmallmatrix}\\[2mm]
23&\begin{psmallmatrix}20&12&18\\18&3&18\\1&22&19\end{psmallmatrix}.
\end{array}                                                \tag{19}
\]

The `02,13` blocks have rank two and the other four have rank three.
Modulo `1000003`, the `81 by 54` Hessian has rank `51`; the three
independent vertex gauges give the matching characteristic-zero upper
bound.  Hence (19) is an exact rational, not numerical, nonvacuity
certificate.
