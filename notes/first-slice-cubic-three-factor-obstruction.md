# First-slice cubic contact detects every three-factor source

## Outcome

The first-slice component maps add genuine information to the global
colour-torus filtration.  Let three edge-disjoint perfect matchings
`P_0,P_1,P_2` on `n=2m>=6` sites carry nonzero same-colour cells, and
suppose every pairwise union is a Hamilton cycle.  Although the first
global genuinely ternary term can occur in colour degree four, some
**normalized one-site slice** always has a genuinely ternary term by degree
three.

More precisely, for every colour `r` there is an extra perfect matching
`M_r` with

\[
                         1\leq |M\cap P_r|\leq2           \tag{1}
\]

Its induced colouring is a singleton fibre.  If `v` is an endpoint of an
`r`-edge of `M_r`, scale colour `r` by `t` at
every site and form the normalized component

\[
 t^{-1}(e_r^*\otimes\operatorname{id})H(A(t)).            \tag{2}
\]

Then (2) has a nonzero forbidden coefficient in degree

\[
                         2|M\cap P_r|-1\leq3.             \tag{3}
\]

Thus the family of first-slice cubic equations rules out the entire
pairwise-Hamilton three-factor chart, uniformly in the number of sites.
This is a source-relative strengthening of the global torus count: it uses
which local source row carries the extra matching, not merely the final
tensor's colour histogram.

The bound is sharp.  The twelve-site balanced triple in
`torus-osculation-bottom-top-collision.md` has five extra matchings, all
with factor-edge counts `(2,2,2)`.  Every global defect begins in degree
four and every affected normalized first slice begins in degree three.
That support is 3-vertex-connected and has no factor-closed six-set, so
quadratic first-slice contact still gives no six-site restriction; the
cubic Bianchi layer is the first one which detects it.

## 1. A one- or two-chord matching

The combinatorial input is slightly stronger than the three-one-factors
lemma.

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017), published as Thm 1 of Chandran-Gajjala,
arXiv:2202.05562, and in multigraph form as Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

**Lemma 1.1 (two-chord witness).**  Let `P_0,P_1` be the alternating
perfect matchings of a Hamilton cycle on `2m>=6` vertices, and let `P_2`
be an edge-disjoint perfect matching.  Then `P_0 union P_1 union P_2`
has a perfect matching `M`, different from all three selected factors,
such that

\[
                              1\leq |M\cap P_2|\leq2.     \tag{4}
\]

**Proof.**  Number the cycle vertices cyclically by
`0,1,...,2m-1`, so every cycle edge joins opposite parities.

If some edge `uv` of `P_2` joins opposite parities, the two open cycle
arcs between `u` and `v` contain even numbers of vertices.  Match
consecutive vertices along both arcs and adjoin `uv`.  This gives a perfect
matching using exactly one edge of `P_2`.

It remains to suppose that every `P_2` edge joins equal parities.  Then
`P_2` separately matches the even and odd cycle positions.  An even chord
and an odd chord must interlace.  Here is a short proof which retains the
possible crossings within either one of the two chord families.

Assume no even chord interlaces an odd chord.  Divide the even vertex
labels by two, and index an odd vertex `2j+1` by `j`.  For a chord in one
family, every endpoint of the other family lying on one open arc must be
paired inside that arc.  Hence the number of such endpoints is even.  It
follows first that both endpoint matchings preserve index parity.  If they
preserve every residue class modulo `2^a`, count the other-family endpoints
in each residue class on the same arc.  Every count is even, so the chord's
two endpoint indices are congruent modulo `2^(a+1)`.  Induction makes every
matched index pair congruent modulo every power of two, impossible for two
distinct indices.  Thus an interlacing even/odd chord pair exists.

The four open cycle arcs between their alternating endpoints each contain
an even number of vertices.  Match consecutively on those four arcs and
adjoin the two chords.  The result uses exactly two edges of `P_2`.

In either case the constructed matching contains an edge outside the
Hamilton cycle and at least one cycle edge, so it is different from
`P_0,P_1,P_2`. `QED`

The role of the pairwise-Hamilton hypothesis is now transparent.

**Corollary 1.2 (small colour in a singleton ternary fibre).**  If all
three pairwise unions `P_r union P_s` are Hamilton cycles, then for every
colour `r` some extra matching `M_r` has (1), uses all three factors, and
is the unique matching compatible with its induced vertex colouring.

**Proof.**  Fix `r` and apply Lemma 1.1 after naming the other two factors
as the Hamilton cycle and the remaining factor as `P_r`.  The witness is not a selected
factor.  If it used only two factor colours, it would be a third perfect
matching of their Hamilton union, which is impossible.  At every vertex
there is exactly one incident edge of each factor colour.  Its induced
colour therefore forces its incident edge at every vertex, proving
uniqueness. `QED`

## 2. The normalized first-slice obstruction

Let `A` put an arbitrary nonzero multiple of `e_r tensor e_r` on every
edge of `P_r`.  Under the local torus

\[
 e_r\longmapsto t e_r,
 \qquad e_s\longmapsto e_s\quad(s\ne r),                 \tag{5}
\]

a matching using `k` edges of `P_r` acquires degree `2k`.  Let `M` and
`r` be supplied by Corollary 1.2 and choose a vertex `v` on one of its
`P_r` edges.  Its singleton word `w_M` has colour `r` at `v`.  Contracting
the output at `v` by `e_r^*` and dividing the component by its unavoidable
local factor `t` leaves

\[
                         t^{2k-1}e_{w_M|_{B\setminus\{v\}}}.          \tag{6}
\]

The omitted scalar in (6) is the product of the selected nonzero edge
weights.  No other matching contributes to this coordinate, by singleton
uniqueness.  On the torus-scaled diagonal target, the same normalized
component is only

\[
                         t^{n-1}e_r^{\otimes(B\setminus\{v\})}.       \tag{7}
\]

Since `k<=2` and `n>=6`, the nonconstant word (6) occurs in degree at most
three, strictly below the pure degree `n-1`.  It cannot cancel.  This proves
the stated first-slice cubic obstruction.

Equivalently, in the pure-endpoint Maurer--Cartan hierarchy, the global
degree-four balanced error becomes a cubic connection error after resolving
the source component at any one of its scaled-colour endpoints.  Merely
recording the unsliced degree misses exactly this one local factor.

## 3. Sharp twelve-site boundary

For the balanced twelve-site factors

\[
\begin{aligned}
P_0={}&01|23|45|67|89|(10,11),\\
P_1={}&(0,11)|12|34|56|78|(9,10),\\
P_2={}&02|17|35|(4,10)|68|(9,11),
\end{aligned}                                             \tag{8}
\]

the complete support has five extra perfect matchings and every one has
edge-count vector `(2,2,2)`.  Hence every forbidden normalized slice in
(6) has degree exactly three, never one or two.  The same support has no
six-set closed under all three factors.  It is therefore an exact
countermodule to either of the weaker implications

\[
\begin{split}
 &\text{global contact through degree three}
       \Longrightarrow\text{a factor-closed six-set},\\
 &\text{all normalized first-slice components through degree two}
       \Longrightarrow\text{a factor-closed six-set}.
\end{split}                                               \tag{9}
\]

The cubic first-slice layer is both necessary and sufficient to eliminate
this complete three-factor boundary.  This does not yet treat sources with
parallel cells, higher-rank edge matrices, or cancellation between several
matchings of one colouring; those are precisely the branches in which
singleton uniqueness in Corollary 1.2 fails.

## 4. Exact audit

Run

```text
python computations/verify_first_slice_cubic_three_factor.py
```

The checker exhausts every cycle-edge-disjoint third factor through twelve
vertices and verifies the constructive one-/two-chord witness.  It then
audits the twelve-site sharp example: all three binary faces, the complete
matching list, singleton fibres, the `(2,2,2)` edge counts, normalized
first-slice degree three, and absence of a factor-closed six-set.
