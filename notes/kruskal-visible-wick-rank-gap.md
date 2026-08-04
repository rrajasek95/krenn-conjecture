# Kruskal-visible Wick expansions have a global rank gap

## 1. Outcome

Let \(n=2m\geq6\), let every site space be \(\mathbb C^3\), and allow
arbitrary complex, endpoint-ordered \(3\times3\) aggregate blocks. Expand
each active block by a minimal matrix-rank factorization and then expand the
Wick power over decorated perfect matchings. If that displayed pure-tensor
expansion satisfies the usual \(n\)-way Kruskal inequality, then its tensor
cannot simultaneously have CP rank three and local mode rank three at every
site.

This is a genuine global rank gap. It is uniform in \(m\), uses neither the
\(E_1/E_2\) masks nor a clean-cap choice, and permits all complex coefficients
and endpoint asymmetry. A convenient support-side corollary is:

> If the decorated expansion has \(S\leq n\) terms and its \(S\) local
> factors have Kruskal rank three at every site, its output is not in the
> local \(GL(3)^n\)-orbit of \(\Delta_{n,3}\).

Grouping sites into three supermodes gives a second exact test that can reach
\(S>n\). Its unconditional consequence is a short linear circuit on some
shore, however, not yet a graph-density or clean-cap theorem.

## 2. Why a bare tensor-rank question is circular

Write

\[
                  \Delta_{n,3}=\sum_{r=0}^2e_r^{\otimes n}.
\]

**Lemma 2.1.** An \(n\)-tensor \(T\in(\mathbb C^3)^{\otimes n}\) has CP rank
three and mode rank three at every site if and only if it lies in the local
\(GL(3)^n\)-orbit of \(\Delta_{n,3}\).

**Proof.** In a minimal decomposition

\[
                       T=\sum_{r=0}^2
                       a_{1r}\otimes\cdots\otimes a_{nr},       \tag{1}
\]

the mode-\(v\) flattening has column space contained in
\(\langle a_{v0},a_{v1},a_{v2}\rangle\). Mode rank three therefore makes
these three vectors a basis at every site. An invertible local map sends
that ordered basis to \((e_0,e_1,e_2)\), giving \(\Delta_{n,3}\). The
converse is immediate. \(\square\)

Thus asking whether a Wick power can have CP rank exactly three and full
local ranks is already equivalent to the orbit form of the Krenn problem.
A useful rank argument must include source-relative information.

## 3. The decorated matching expansion

Let \(U_v\cong\mathbb C^3\) be the site spaces and write

\[
                 q=\sum_{u<v} A_{uv},\qquad
                 A_{uv}\in U_u\otimes U_v.                       \tag{2}
\]

Delete every edge that occurs in no perfect matching; this changes neither
the top Wick power \(q^{[m]}\) nor the discussion below. For each remaining
edge \(e=uv\), put \(\rho_e=\operatorname{rank}A_e\) and choose any minimal
factorization

\[
                 A_e=\sum_{a=1}^{\rho_e}
                    x^{(u)}_{e,a}\otimes x^{(v)}_{e,a}.           \tag{3}
\]

No symmetry between the endpoint vectors is assumed. Coefficients may be
absorbed into either endpoint vector.

For a perfect matching \(M\), choose one label
\(a_e\in\{1,\ldots,\rho_e\}\) on every \(e\in M\). The pair
\((M,(a_e)_{e\in M})\) is a decorated perfect matching and contributes one
nonzero pure tensor. Hence

\[
 q^{[m]}=
 \sum_{M\in\mathcal M(G)}
 \ \sum_{(a_e)\in\prod_{e\in M}[\rho_e]}
 \bigotimes_{v=1}^{n}x^{(v)}_{e_v,a_{e_v}},                       \tag{4}
\]

where \(e_v\) is the edge of \(M\) incident with \(v\). Its displayed length
is

\[
                         S=\sum_{M\in\mathcal M(G)}
                              \prod_{e\in M}\rho_e.              \tag{5}
\]

For each site \(v\), form the \(3\times S\) factor matrix \(F_v\) whose
columns are the local factors in (4), in the same decorated-term order.
Let \(k_v\) be its Kruskal rank.

All data in (3)--(5) are finite and exact. Different minimal factorizations
can give different \(k_v\), so the theorem is stated for a chosen
factorization. The block matrices themselves remain fully arbitrary.

## 4. The \(n\)-mode rank gap

**Theorem 4.1 (Kruskal-visible Wick rank gap).** Suppose (4) satisfies

\[
                         \sum_{v=1}^{n}k_v
                         \geq 2S+(n-1).                          \tag{6}
\]

Then \(q^{[m]}\) cannot have both CP rank three and mode rank three at every
site.

**Proof.** The \(n\)-way Kruskal theorem says that (4) is a minimal,
essentially unique CP decomposition. In particular,

\[
                         \operatorname{rank}_{CP}(q^{[m]})=S.    \tag{7}
\]

Assume for contradiction that the left side is three and all local mode
ranks are three. Then \(S=3\). For a physical perfect matching \(M\), let

\[
                              d_M=\prod_{e\in M}\rho_e           \tag{8}
\]

be its number of decorated terms. If \(d_M>1\), then \(d_M\leq S=3\).
Since every \(\rho_e\) is a positive integer, exactly one edge of \(M\) has
rank \(d_M\in\{2,3\}\), while every other edge has rank one. The different
decorated terms above \(M\) therefore have proportional local factors at
the endpoint of any other edge. Two columns of some \(F_v\) are
proportional, so \(\operatorname{rank}F_v\leq2\). The mode-\(v\) rank of
(4) is at most \(\operatorname{rank}F_v\), contradicting local mode rank
three. Thus \(d_M=1\) for every \(M\).

Equation (5) now says that the active support has exactly three physical
perfect matchings, and every edge in each has matrix rank one. If two
matchings shared an edge, their columns in \(F_v\) would be proportional at
either endpoint of that rank-one edge. Again the local mode rank would be
at most two. The three matchings are therefore pairwise edge-disjoint.

*Attribution.*  The three-one-factors lemma, stated and proved next, is
**Bogdanov's observation** (Bogdanov 2017),
published as Thm 1 of Chandran-Gajjala, arXiv:2202.05562, and in
multigraph form as Thm 1.7 of Chandran-Gajjala-Illickan,
arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  **No priority
is claimed**: the self-contained proof below is given only because the
audit discipline of this repository requires every consumed statement to
be either cited to a checked source or proved inside the artifact.

The standard three-one-factors lemma says that three pairwise edge-disjoint
perfect matchings on \(n\geq6\) vertices have a fourth perfect matching in
their union. Here is a short proof. Superpose the first two. If their union
has at least two alternating cycles, flip just one. Otherwise it is a
Hamilton cycle \(C\), and the third matching consists of chords. A chord
joining opposite cycle parities cuts \(C\) into two even paths and gives a
new matching.

It remains to consider chords joining equal parities. Label the cycle
\(A_0,B_0,A_1,B_1,\ldots,A_{m-1},B_{m-1}\). If no \(A\)-chord crossed a
\(B\)-chord, a parity descent would be possible.  Indeed, an \(A_iA_j\)
chord separates the \(B\)-vertices on its two open arcs: a \(B\)-chord
joining the arcs would interlace it.  Each arc must therefore contain an
even number of \(B\)-vertices, so \(i-j\) is even modulo \(m\).  The same
argument applies to every \(B\)-chord.  Inductively, suppose all chords of
either type join indices equal modulo \(2^t\).  Each residue class is
internally perfectly matched, so \(2^{t+1}\) divides \(m\).  On either arc
of an \(A_iA_j\) chord, the \(B\)-vertices in each residue class modulo \(2^t\)
must again be paired internally.  In the residue class of \(i\), their
number is the cyclic index difference divided by \(2^t\), so that quotient
is even.  Thus the endpoints agree modulo \(2^{t+1}\); the same argument
applies to a \(B\)-chord.  Iterating beyond \(m\) forces the two endpoints
of every chord to have the same index, a contradiction.  Hence an
\(A\)-chord and a \(B\)-chord interlace. Those two chords cut \(C\) into
four even paths, again giving a new matching. The only exception is the
four-vertex one-factorization.

Every edge of the new matching is active, so it contributes at least one
additional decorated term to (5), contradicting \(S=3\). \(\square\)

**Corollary 4.2.** If \(S\leq n\) and \(k_v=3\) for all \(v\), then the
conclusion of Theorem 4.1 holds.

Indeed,

\[
                 \sum_vk_v=3n\geq2S+n-1.                         \tag{9}
\]

More generally, (6) uses the actual \(k_v\)'s. Conversely, since
\(k_v\leq3\), inequality (6) is impossible when \(S\geq n+1\).

## 5. Three-supermode strengthening

Fix any tripartition into nonempty shores

\[
                              B=P\sqcup Q\sqcup R.                \tag{10}
\]

Group every decorated term in (4) into a three-way pure tensor in
\(U_P\otimes U_Q\otimes U_R\). Write \(F_P,F_Q,F_R\) for the grouped factor
matrices and \(k_P,k_Q,k_R\) for their Kruskal ranks.

**Proposition 5.1 (three-supermode diagnostic).** Suppose \(q^{[m]}\) has
CP rank three and local mode rank three at every original site. For every
tripartition (10), one of the following holds:

1. \(S=3\), and the three decorated terms are, up to scaling and a common
   permutation, the three aligned GHZ summands; or
2.
   \[
                         k_P+k_Q+k_R\leq2S+1.                     \tag{11}
   \]

**Proof.** If the reverse inequality held, the three-way Kruskal theorem
would make the grouped \(S\)-term expansion minimal and unique. Grouping
the rank-three decomposition from Lemma 2.1 gives a three-term
decomposition whose three factors are independent on every nonempty shore.
Thus grouped CP rank is three, forcing \(S=3\). Uniqueness identifies the
three grouped terms with the GHZ terms. Equality of nonzero pure tensors on
each shore identifies their individual site factors up to reciprocal
scalings, so the original decorated terms are aligned as well. \(\square\)

The contrapositive has an exact circuit consequence. Put
\(\delta_X=S-k_X\). In every nonaligned chart and for every tripartition,

\[
             \delta_P+\delta_Q+\delta_R\geq S-1,\qquad
             \min(k_P,k_Q,k_R)\leq
             \left\lfloor\frac{2S+1}{3}\right\rfloor.            \tag{12}
\]

For \(S\geq3\), at least one shore therefore contains a linearly dependent
subfamily of at most

\[
                    \left\lfloor\frac{2S+1}{3}\right\rfloor+1   \tag{13}
\]

decorated matching products. This reaches beyond the \(n\)-mode length
cutoff. If the grouped columns are in linear general position, then

\[
 \min(S,3^{|P|})+\min(S,3^{|Q|})+\min(S,3^{|R|})\geq2S+2         \tag{14}
\]

certifies the chart. For example, a \(2+2+2\) split at six sites rejects
nonaligned general-position expansions with \(4\leq S\leq12\), whereas
(6) can never certify \(S>6\). A \(2+3+3\) split at eight sites similarly
reaches \(4\leq S\leq30\).

This strengthening is presently a diagnostic, not a support-density
theorem. A short linear circuit among grouped Segre products need not come
from repeated edges or repeated matching restrictions; complex
dependencies can occur with all factors distinct. Turning (12) into a
forced sparse cut, shared edge, or clean cap requires an additional
classification of these grouped circuits. Without such a lemma, (11) does
not itself advance the dense cancellation chart.

## 6. Exact boundary: balanced flattenings do not replace local ranks

There is a six-site rank-one example showing why “at every site” in Theorem
4.1 cannot be weakened to balanced-cut rank tests. Take

\[
\begin{aligned}
 M_0&=01\mid23\mid45,\\
 M_1&=01\mid24\mid35,\\
 M_2&=02\mid34\mid15,
\end{aligned}
\]

and put \(E_{00}\) on \(01,23,45\), \(E_{11}\) on \(24,35\), and
\(E_{22}\) on \(02,34,15\). These are exactly the supported perfect
matchings, and

\[
 T=e_0^{\otimes6}
   +(e_0\otimes e_0\otimes e_1^{\otimes4})
   +e_2^{\otimes6}.                                      \tag{15}
\]

The local Kruskal ranks are \((1,1,3,3,3,3)\), whose sum \(14\) exceeds the
six-way rank-three threshold \(11\). Thus (15) has CP rank three and a
unique decomposition. Every one of its twenty balanced \(3|3\)
flattenings also has rank three. Nevertheless its single-site mode ranks
are \((2,2,3,3,3,3)\). The exact escape is the repeated \(e_0\) factor at
sites \(0,1\). Thus CP uniqueness plus all balanced flattening ranks is not
a substitute for the target's full local geometry.

## 7. Relation to clean-cap descent

Theorem 4.1 bypasses clean-cap descent on a real, uniform chart: once a
source has a Kruskal-visible decorated expansion, global CP rank forces
\(S=3\), and the one-factor argument ends the chart without choosing a cap
or enumerating exceptional masks. It strictly extends the rank-one,
exactly-three-matching observation: any number of physical matchings and
arbitrary block ranks are allowed before (6) forces the collapse.
Proposition 5.1 supplies a longer-range rejection test after grouping, but
only conditionally on the absence of the forced circuits in (12).

This is not a global replacement for descent. Dense supports and
higher-rank blocks make \(S\) grow multiplicatively, while repeated endpoint
factors lower the \(k_v\)'s. The resulting long, cancellation-prone
expansions are precisely where the clean-cap/\(E_1/E_2\) program carries
information not visible to Kruskal's theorem.

The lightweight verifier
[verify_kruskal_visible_wick_rank_gap.py](../computations/verify_kruskal_visible_wick_rank_gap.py)
uses only the Python standard library. It audits the threshold arithmetic,
the three-supermode ranges and circuit bounds, the \(S=3\) block-rank
rigidity, the six-site one-factor boundary, and every balanced flattening
of (15), without constructing a dense \(3^6\) tensor.
