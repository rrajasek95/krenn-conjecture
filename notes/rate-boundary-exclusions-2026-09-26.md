# Two non-prism limits cannot approach perfect GHZ fidelity

**Status:** new written proofs with exact finite checks; not independently
audited or admitted to the certified proof spine. The universal complex
square-root rate bound remains open.

The [previous result](complex-rate-bound-2026-09-26.md) controls cancellation
near the prism. This investigation tests genuinely different zero-output
limits and develops two ways to exclude them entirely from a sequence tending
to perfect GHZ fidelity.

| Limit or test | Result |
|---|---|
| Any candidate limit, viewed from one site | All six augmented core-response matrices must have rank at most 15 |
| A colored five-cycle with an isolated sixth site | Fidelity stays below 3/4 when the five-site core is within distance 1/200 of the specified core; all remaining-site edges are arbitrary |
| Eight identity blocks on a two-versus-four bipartite graph | Fidelity stays below 1/2 throughout coefficient distance 1/1000 of the specified zero-output source |
| More general two-versus-four limits | An injective 54-column response excludes perfect-fidelity approach; a possible limit must instead have a singular response |

The last example passes the single-site rank test. Thus the second exclusion
adds information; it is not another calculation of the same obstruction.

![Two excluded zero-output limits](../explainers/rate-boundary-assets/limits.svg)

## 1. Definitions and the problem being narrowed

There are six sites with three colors at each site. Each pair has an arbitrary
complex 3-by-3 matrix of source entries. Let \(H(A)\) be their matching tensor,
let \(\Delta=a^6+b^6+c^6\), and set

\[
 g=\Delta/\sqrt3,\qquad
 F(A)=\frac{|\langle g,H(A)\rangle|^2}{\|H(A)\|^2}
\]

whenever the output is nonzero. Coefficient norms are Euclidean; matrix norms
are Frobenius unless marked as operator norms.

Normalize source strength to \(\|A\|=1\). The exact six-site no-go theorem
implies that a sequence with \(F\to1\) must have \(\|H\|\to0\). Taking a
convergent subsequence gives a nonzero source \(A_0\) with \(H(A_0)=0\).
These are the zero-output limits relevant to a universal rate bound.

The question is not whether every zero-output source exists—it plainly can—but
which ones can be approached with nearly pure GHZ output. Excluding a
neighborhood from high fidelity removes it from the rate problem completely.

## 2. An exact best-fidelity formula after fixing five sites

Choose a site \(v\), and let \(Q\) be the source on the other five sites.
Define a matrix

\[
                       T_Q:\mathbb C^{15}\longrightarrow\mathbb C^{243}.
\]

Its columns are indexed by a core site \(p\) and its color \(i\). Column
\((p,i)\) is the tensor obtained by putting color \(i\) at \(p\) and the
four-site matching tensor on the other four core sites. Its coefficients are
quadratic in the entries of \(Q\).

For each color \(h\) at site \(v\), collect the 15 incident source entries
into \(z_h\). Expanding by the partner of \(v\) gives the exact identity

\[
                         H(A)=\sum_{h=a,b,c}h_v\otimes T_Qz_h.       \tag{1}
\]

There is no approximation in (1). All 45 incident entries are independent, so
the possible outputs at fixed \(Q\) form \(\mathbb C^3\otimes W_Q\), where
\(W_Q=\operatorname{im}T_Q\).

Let \(P_Q\) be the orthogonal projection onto \(W_Q\), and let
\(G=[a^5\ b^5\ c^5]\). Projection onto a subspace maximizes overlap with
a fixed unit vector. Therefore, when nonzero outputs exist,

\[
 \boxed{F_{\max}(Q)=\frac13\bigl(\|P_Qa^5\|^2+
                 \|P_Qb^5\|^2+\|P_Qc^5\|^2\bigr).}         \tag{2}
\]

This optimizes over every incident source matrix, including arbitrary complex
cancellation. If \(T_Q=0\), all such outputs vanish. In either case, a nonzero
output obeys the ceiling in (2).

Equation (2) is also a practical reduction: 45 source variables can be removed
from a fidelity optimization analytically. Orthogonal projection can be
computed with a matrix of only 15 columns.

### A continuous certificate and a necessary condition on every limit

Form the augmented matrix

\[
                     M_Q=[T_Q\ G]\in\mathbb C^{243\times18},
\]

with singular values \(\sigma_1\ge\cdots\ge\sigma_{18}\). The matrix
\([T_Q\ P_QG]\) has rank at most 15, and its squared distance from \(M_Q\)
is \(3(1-F_{\max}(Q))\). The least squared Frobenius error of a rank-at-most-15
approximation is the sum of the squares of the last three singular values.
Consequently every source with this core satisfies

\[
 \boxed{1-F(A)\ge\frac{\sigma_{16}(M_Q)^2+
                         \sigma_{17}(M_Q)^2+\sigma_{18}(M_Q)^2}{3}.} \tag{3}
\]

Unlike an orthogonal projection at a rank change, these singular values are
continuous in \(Q\). Hence any limit of a sequence with \(F\to1\) must obey

\[
                     \operatorname{rank}[T_{Q_0}\ G]\le15          \tag{4}
\]

**at every one of the six choices of site**. One violated condition excludes
the limit and a whole neighborhood.

The exact six-site no-go gives an additional useful interpretation. If
\(T_{Q_0}\) had rank 15, (4) would put all three pure vectors in its image;
choosing their three preimages in (1) would give an exact forbidden source.
Thus every relevant limit also satisfies

\[
                         \operatorname{rank}T_{Q_0}<15              \tag{5}
\]

at all six sites. The dependence on the exact no-go is only needed for this
last inference; (2)–(4) are general linear-algebra statements.

There is an important limit to what (5) says by itself. At a site with any
nonzero incident row in \(A_0\), zero output already puts that row in the
kernel of \(T_{Q_0}\). Rank deficiency there is automatic. The additional
restriction is the **target-compatible augmented rank** in (4), and the
exclusion of full-rank cores at sites whose incident rows vanish. These tests
are not a classification of the remaining cancellation sources.

## 3. First excluded limit: a five-cycle and an isolated site

Take site 5 as the isolated site. The five core edges have unit weights and
the following endpoint colors:

\[
                  01:a,\quad12:b,\quad23:c,\quad34:a,\quad04:b.    \tag{6}
\]

Each notation means the indicated color at both ends; all other core entries
are zero. Call this core \(Q_0\). Removing any one cycle site leaves a path
with a unique perfect matching. The resulting 15 columns of \(T_{Q_0}\)
are 15 distinct coordinate vectors. Exactly two pure words, \(a^5\) and
\(b^5\), occur among them. Therefore

\[
 T_{Q_0}^*T_{Q_0}=I_{15},\qquad F_{\max}(Q_0)=2/3,
 \qquad\operatorname{rank}[T_{Q_0}\ G]=16.                  \tag{7}
\]

The augmented matrix has two singular values \(\sqrt2\), fourteen singular
values 1, and two zeros. In particular \(\sigma_{16}=1\).

This persists quantitatively under arbitrary complex core perturbations.
Suppose \(\|Q-Q_0\|\le\eta\le1/20\). Each four-site matching tensor is a
sum of three products of two disjoint edge blocks. The derivative of each
product has norm at most \(\|Q\|\|D\|\) in a direction \(D\), by
Cauchy–Schwarz on its two factors. Since \(\|Q_0\|=\sqrt5\),

\[
 \|H_4(Q)-H_4(Q_0)\|\le3(\sqrt5+\eta)\eta
\]

for every omitted core site. Grouping the 15 columns into five three-column
insertion maps and applying Cauchy–Schwarz again gives

\[
 \|T_Q-T_{Q_0}\|_{\rm op}
 \le3\sqrt5(\sqrt5+\eta)\eta<16\eta.                      \tag{8}
\]

Each singular value changes by at most this operator norm. Using (3),

\[
                         F(A)\le1-\frac{(1-16\eta)^2}{3}.          \tag{9}
\]

At \(\eta=1/200\), the right side is \(1346/1875<3/4\).
**No smallness condition is imposed on the 45 incident source entries.**
Thus this excludes a whole tube of sources, not just one prescribed path
toward the isolated-site limit.

## 4. A different decomposition for two-versus-four limits

Split the sites into \(\{0,1\}\) and \(\{2,3,4,5\}\). Write

* \(B\) for the eight crossing edge blocks, with 72 entries;
* \(D\) for the six internal blocks on the four-site side, with 54 entries;
* \(Z=A_{01}\), with nine entries.

Every perfect matching either pairs sites 0 and 1 together, or matches each
to a different site on the other side. Hence exactly

\[
                     H(A)=L_B(D)+Z\otimes H_4(D),                   \tag{10}
\]

where \(L_B\) is linear in \(D\) and quadratic in \(B\). The first term
contains twelve matchings and the second contains three. This identity is
valid for all 135 complex entries.

There is a general boundary exclusion. Fix any \(B_0\) for which \(L_{B_0}\)
is injective, and any finite \(Z_0\). The source \((B_0,0,Z_0)\) has zero
output. The exact no-go says \(\Delta\notin\operatorname{im}L_{B_0}\):
otherwise take its preimage as \(D\) and set \(Z=0\) in (10) to obtain an
exact GHZ source.

Since this is a finite-dimensional closed subspace, its maximum GHZ fidelity
is strictly below 1. Injectivity gives \(\|L_{B_0}D\|\ge s\|D\|\) for
some \(s>0\). Near the base, the perturbation of \(L_BD\) is
\(o(\|D\|)\), and the second term in (10) is \(O(\|D\|^2)\).
The normalized output therefore stays close to that fixed subspace. Perfect
fidelity cannot be approached.

**Conclusion:** for a relevant limit with all four-site-side internal edges
zero, the 54-column map \(L_{B_0}\) must fail to be injective. This general
statement uses the exact no-go; the following explicit example does not.

## 5. Second excluded limit: eight identity blocks

Let every crossing block of \(B_0\) equal \(I_3\), and put \(D_0=Z_0=0\).
This is a complete bipartite graph with unequal shores, so it has no perfect
matching and \(H(A_0)=0\).

Let \(L_0=L_{B_0}\), let \(K=L_0^*L_0\), and let \(v=L_0^*\Delta\).
The exact integer calculation gives

| Eigenvalue of \(K\) | 8 | 12 | 20 | 40 | 60 |
|---|---:|---:|---:|---:|---:|
| Multiplicity | 9 | 12 | 18 | 9 | 6 |

In particular \(L_0\) is injective and

\[
                         \|L_0D\|\ge\sqrt8\|D\|.                 \tag{11}
\]

The vector \(v\) has value 2 at each of the 18 same-color entries of \(D\)
and zero at the other 36 entries. Also \(Kv=60v\). Solving the normal
equations gives the orthogonal projection of \(\Delta\) onto the response
image as \(L_0(v/60)\), with squared norm

\[
                            v^*v/60=72/60=6/5.
\]

Dividing by \(\|\Delta\|^2=3\) proves

\[
       \boxed{\sup_{D\ne0}F(L_0D)=2/5.}                          \tag{12}
\]

This is attained: take every same-color entry of \(D\) equal to \(1/30\)
and its other entries zero. For fixed \(B=B_0\) and \(Z=0\), (12) is exact
for arbitrary \(D\), not just an infinitesimal approximation.

### Full complex neighborhood estimate

Suppose \(\|A-A_0\|\le\eta=1/1000\). Then
\(\|B-B_0\|,d=\|D\|,z=\|Z\|\le\eta\).

For each choice of an internal edge on the four-site side, its coefficient
map in \(L_B\) is the sum of two products of crossing blocks. The difference
of each product has norm at most
\((\|B\|+\|B_0\|)\|B-B_0\|\). Sum the two products, then apply
Cauchy–Schwarz over the six internal edges to get

\[
 \|(L_B-L_0)D\|
 \le2\sqrt6(2\sqrt{24}+\eta)\eta d<50\eta d.               \tag{13}
\]

Here \(\|B_0\|=\sqrt{24}<49/10\) and \(\sqrt6<5/2\) justify the
displayed rational constant. The three four-site matchings also give

\[
                \|Z\otimes H_4(D)\|\le\tfrac32zd^2
                                          <2\eta^2d.       \tag{14}
\]

If \(D=0\), the output is zero. Otherwise write \(H=L_0D+W\). Equations
(11), (13), and (14) imply

\[
 \frac{\|W\|}{\|L_0D\|}
 \le\frac{50\eta+2\eta^2}{\sqrt8}
 <\frac38(50\eta+2\eta^2)<\frac1{50}.                       \tag{15}
\]

By (12), the overlap amplitude of \(L_0D\) with unit GHZ is at most
\(\sqrt{2/5}\|L_0D\|<(2/3)\|L_0D\|\). The triangle inequality and
(15) therefore yield the explicit bound

\[
 \boxed{F(A)\le
 \left(\frac{2/3+1/50}{1-1/50}\right)^2
       =\left(\frac{103}{147}\right)^2<\frac12.}            \tag{16}
\]

This allows arbitrary complex perturbations on every physical pair. It rules
out every path to perfect fidelity in that neighborhood.

### Why the second test was necessary

At this same base, the single-site response and augmented ranks are

| Chosen site | \(\operatorname{rank}T_{Q_0}\) | \(\operatorname{rank}[T_{Q_0}\ G]\) |
|---|---:|---:|
| 0 or 1 | 0 | 3 |
| 2, 3, 4, or 5 | 9 | 12 |

Every augmented rank is below 15. Thus the necessary condition (4) passes
this limit, although (16) excludes it. The different decomposition in (10)
is essential to the progress here.

## 6. What remains for a universal rate theorem

The new results remove regular single-site cores and regular two-versus-four
limits from consideration. They do not classify all zero-output sources.
In particular, two-versus-four limits with a nontrivial response kernel and
dense sources whose output vanishes through cancellation still require work.

A surviving candidate must satisfy all six conditions (4)–(5), and any
applicable two-versus-four response must be singular. The prism remains a
legitimate candidate, with its already proved local square-root bound: at each
site its response rank is 9 and its augmented rank is 11, so the filter passes
it as it must.

The augmented condition is more selective near the largest allowed ranks.
If \(r=\operatorname{rank}T_{Q_0}\), then

\[
 \dim\bigl(\operatorname{im}T_{Q_0}\cap
              \operatorname{span}\{a^5,b^5,c^5\}\bigr)\ge r-12.
\]

Thus rank 14 requires at least two independent target directions already in
the response image; rank 13 requires at least one. These need not be individual
pure-color vectors. The exact no-go prevents all three from lying in the image.

These fidelity gaps do not extend that rate theorem to all sources. They
instead narrow the set of boundaries where its exponent could fail. The next
substantive target is a singular response class, where higher-order output can
escape the first-order image. More computation on the regular examples would
not answer that question.

## 7. Evidence and replay

```sh
python3 computations/rate-boundary-gate-2026-09-26/verify.py
```

The [package](../computations/rate-boundary-gate-2026-09-26/README.md) reconstructs
the maps from perfect matchings, independently checks the two-versus-four
decomposition, and verifies the Gram matrix's annihilating polynomial and
spectral multiplicities using integer arithmetic. It also checks the exact
projection equations, all six root ranks, every rational norm constant, and
rejection of a corrupted Gram matrix.

The general boundary statements use the
[exact six-site no-go](../proofs/six-site-arbitrary-complex-obstruction.md).
The two numerical fidelity ceilings have self-contained proofs above and do
not assume that theorem. The linear-algebra and continuity arguments remain
written proofs requiring independent audit. No historical priority is claimed.
