# The selected-witness N=8 reduction has one uncovered invariant packet

Dependency audit, not a new source search.  Within the selected-witness
framework, reciprocal counts `r=0,1,2,3` and the four-reciprocal matching
branch now have the desired exact alternative:

\[
 \boxed{\text{curved doubly-good rank-one overlap}}
 \quad\text{or}\quad
 \boxed{\text{contradiction to the exact source equations}}.       \tag{1}
\]

The theorem is not yet complete.  The shared-endpoint branch—`r=4` shared
and every `5<=r<=12`—has one precise missing implication.  The uniform
three-row unit of commit `f14fa11` proves that its two reciprocal witness
arms have a **nonflat** canonical transition.  Lemma E then proves that an
off-diagonal reciprocal coordinate unit is automatically good at both
endpoints.  What remains is the diagonal exception: one arm can still have
a rank-two deleted star only if it is a diagonal unit and its complementary
six-site hafnian is a nonzero pure tensor.  The low-rank, full-span, and
budget-thirteen theorems concern incident spaces in the two pair-deletion
charts and do not close that pure-deletion packet.

Thus the single uncovered exact packet is

\[
 \boxed{
 \begin{gathered}
  pq,pr\text{ shared reciprocal coordinate rank-one witnesses},\\
  \text{distinct outer target colours, nonflat transition},\\
  \text{residual full-span charts, and at least one diagonal }E_{kk}
       \text{ arm},\\
  \text{with deleted-star rank }2\text{ and Lemma-E pure colour-}k
       \text{ complement}.
 \end{gathered}}                                             \tag{2}
\]

Closing (2), or proving that it is contradictory, is the only missing step
in the proposed selected-witness N=8 theorem.  It is upstream of the curved
overlap gate: invoking that gate now would silently drop its doubly-good
hypothesis.

## 1. Reciprocal-count decision table

Every site selects three directed rank-one witnesses, one for each target
colour, with distinct physical neighbours.  Let `r` be the number of
physical pairs selected in both directions.

| reciprocal count | exact reduction | status |
|---|---|---|
| `0,1,2` | if every adjacent selected-good transition is flat, the refined essential/chord count is impossible | (1) proved |
| `3` | the sole all-flat equality packet has two nonadjacent cubic sites; its exact response packet is empty | (1) proved |
| `4`, no shared reciprocal endpoint | the reciprocal graph is a perfect matching; every all-flat good graph reduces to `2K2+4K1`, `3K2+2K1`, or `4K2`, and all three are pure-support empty | (1) proved |
| `4`, shared reciprocal endpoint | the shared reciprocal wedge is nonflat; every off-diagonal arm is doubly good, but a diagonal arm may carry a single-colour essential incidence | (2) open |
| `5,...,12` | a shared reciprocal endpoint is automatic; the same nonflat/goodness fork applies | (2) open |

The split at `r=4` is exhaustive: four reciprocal edges with no common
endpoint form a perfect matching on all eight sites (105 labelled choices),
while every set of at least five reciprocal edges has a common endpoint.

## 2. Why the closed ranges really close

### Counts zero through two

The source-labelled orientation theorem applies to the selected witness
graph itself.  If every wedge of adjacent doubly-good selected edges were
flat, the flat-row classification gives maximum good degree two, while each
distance-two good chord has rank at least two.  Combining the exceptional
chord budget with the refined essential-incidence count leaves no graph for
`r=0,1,2`.  Therefore some adjacent **selected** rank-one arms are good at
both endpoints and have nonzero transition.  This is already the curved
doubly-good alternative in (1), with no later goodness promotion required.

### Count three

The all-flat graph census initially leaves `3K2+2K1` and `4K2`.  Feeding the
essential equality back into the endpoints removes `4K2` and forces the
first shape to have two isolated literal coordinate-cubic sites, zero direct
block between them, and an outer `K6`.  The exact response theorem then
exhausts all neighbour-triple overlaps.  Overlap is inconsistent with the
common nonessential endpoint line or with site-square-zero; in the disjoint
case all 54 pure-cofactor matching terms vanish individually because each
would need a double-essential outer edge.  Hence the all-flat packet is
empty.  The complementary case is a nonflat wedge of good edges, so (1)
again holds.

### Count four with no shared endpoint

Under global flatness, the good graph has maximum degree two.  The refined
chord/essential count leaves only

\[
            2K_2+4K_1,\qquad3K_2+2K_1,\qquad4K_2.         \tag{3}
\]

The `4K2` equality packet is killed by the independently replayed
three-pure RUP certificate.  Commit `dc1ac67` closes the other two shapes,
including every one-unit slack profile: eight frozen proof payloads cover
the two pure-matching union orbits `C8` and `C4+C4` and the four exhaustive
essential profiles.  The Boolean formulas are source-relaxing—they retain
arbitrary unselected pure edges—so unsatisfiability excludes the actual
source packets.  Consequently the all-flat matching branch is empty; a
nonflat branch already consists of adjacent doubly-good edges by definition
of the good graph.

## 3. What the shared-endpoint theorems prove

Fix shared reciprocal arms `pq,pr`.  Because both directions are selected,
the two arcs leaving `p` are among its one-per-colour witnesses, so their
outer target lines are distinct.  The exact four-cover theorem gives a
dichotomy for the two pair-deletion charts.

1. If all residual incident spaces in both charts have dimension at most
   two, their coordinate-plane omission packets lie among 477 exact
   head-labelled states.  Of these, 462 miss a pure row.  The remaining 15,
   after three pure-anchor choices each, have a mandatory unique mixed
   matching.  Thus the entire low-rank branch is contradictory over every
   field.
2. Otherwise there is a residual full-span site.  Independently, the exact
   budget-twelve layer is empty in each chart, so both chart budgets are at
   least thirteen.  The budget-thirteen and projective-compatibility checkers
   classify the first excess layer, but their coordinates are residual
   incident-space data, not the four direct-arm deletion ranks.

The theorem of `f14fa11` then removes **all flat shared wedges**, without a
budget or site-cover assumption.  Write

\[
 A_{pq}=x_q\otimes y_q,\qquad A_{pr}=x_r\otimes y_r,
 \qquad y_q\in\langle e_a\rangle,
        y_r\in\langle e_c\rangle,\quad a\ne c.             \tag{4}
\]

If `x_q,x_r` are proportional, flatness gives one common residual output;
if they are independent, it makes both restricted outer stars zero.  In
either case every equal-colour `q=r=i` slice forces the chord `qr`.  Three
literal source rows then satisfy the ordinary unit

\[
  1=F_i\bigl(D_{jj}G_{i\mid j}-D_{ii}G_j\bigr)-G_i.        \tag{5}
\]

Therefore an exact shared-endpoint source cannot be flat.  This is a strong
uniform conclusion, but (5) contains no deleted-star rank statement.
Indeed the checker and note for `f14fa11` explicitly distinguish

\[
 \text{nonflat doubly-good wedge}
 \quad\text{from}\quad
 \text{nonflat wedge with a named essential/rank-two endpoint}. \tag{6}
\]

Only the first arm of (6) feeds the existing curved doubly-good overlap
theorem.  Lemma E makes the second arm much sharper than an arbitrary rank
defect.  If `A_pq=lambda E_{b,a}` and the deleted star at either endpoint is
rank deficient, Lemma E's (E2) conclusion says its essential row is a
nonzero multiple of `e_k` with a live `(k,k)` diagonal entry.  A matrix unit
has only its `(b,a)` cell, so necessarily

\[
                         a=b=k.                            \tag{7}
\]

Hence every off-diagonal reciprocal unit is automatically good at both
ends.  For a deficient diagonal `E_kk` arm, Lemma E also gives (E1), the
vanishing of colour-`k` rows on every other incident block, and (E3),

\[
 H_{B\setminus\{p,q\}}(A)=\lambda^{-1}
          e_k^{\otimes(B\setminus\{p,q\})}.                \tag{8}
\]

The exact gap is therefore (8) coupled to the other nonflat reciprocal arm
and to the residual full-span response—not an unrestricted failure of
goodness.

## 4. Exact structural counterguard to the missing promotion

The meta-checker reuses the committed `r5_shared` endpoint-axis model from
the `r>=4` classification.  Normalize its shared reciprocal arms to
`p=2,q=1,r=4`.  It has

```text
outer target colours                 (0,1)
shared-p coordinate factors          (0,2)
deleted ranks (p\q,q\p,p\r,r\p)      (2,3,3,3)
pq-deletion residual dimensions      (3,2,3,3,3,3), budget 17
pr-deletion residual dimensions      (3,3,3,3,3,3), budget 18
```

The shared factors are independent and both restricted outer stars are
nonzero.  By the same exact flat-star dichotomy used in `f14fa11`, its
canonical transition is nonflat.  Both pair-deletion charts contain a
three-dimensional residual incident space and exceed the minimum budget,
yet the `pq` arm has rank two at `p` after deleting `q`.  That bad arm is
the diagonal coordinate unit `E_00`, so unlike the earlier off-diagonal
guard it passes the necessary row-shape conclusion (E2) of Lemma E.

This model also has all 24 labelled witnesses, one outgoing head of every
colour at every site, the exact five shared-reciprocal count, complete
rank-three endpoint spans, and literal rank-one coordinate blocks on all
physical pairs.  It is **not** an exact GHZ matching source.  Its role is
precise: it refutes any attempt to derive the missing goodness rank merely
from selected-witness, endpoint-incidence, residual full-span, rank-budget,
nonflatness, and the diagonal row-shape (E2).  It is not asserted to satisfy
the pure complementary tensor (E3).  That exact source consequence is the
remaining datum which must be used to close (2).

## 5. The missing theorem

A complete selected-witness N=8 reduction needs exactly the following
statement, or a stronger contradiction theorem:

> **Shared nonflat goodness lemma (missing).**  In an exact eight-site
> ternary GHZ hafnian source, let `pq,pr` be shared reciprocal selected
> witness arms.  If their canonical transition is nonzero and the
> low-rank pair-deletion alternative is absent, then all four stars obtained
> by deleting the corresponding direct arm have rank three; alternatively,
> any deficient diagonal arm, together with its Lemma-E pure complementary
> tensor, is inconsistent with the other nonflat arm and residual full span.

Because deleting one rank-one block drops a full endpoint star by at most
one, the uncovered failure is exactly rank two, equivalently a named
single-colour essential incidence.  Lemma E already supplies its diagonal
cell and pure six-site cofactor.  A viable proof should couple that pure
cofactor to the full-span response of the second reciprocal arm or to a
mixed matching coefficient.  It cannot be obtained by another flat-star or
budget-thirteen classification: flatness is already impossible and budgets
17/18 still exhibit the diagonal rank defect structurally.

## 6. Reproduction and scope

Run

```text
.venv/bin/python computations/audit_n8_selected_witness_global_dependency.py
.venv/bin/python -O computations/audit_n8_selected_witness_global_dependency.py
```

The checker SHA-pins the exact closure checkers, including the Lemma-E
source theorem, audits the reciprocal-count
partition and all-flat survivor shapes, verifies all eight lower-`r4` proof
payload hashes, and reconstructs the full-span/nonflat/rank-deficient
counterguard.  The individual lower-`r4` checker remains responsible for
independently replaying every RUP/LRAT step.  Frozen meta-ledger:

```text
089ad3e94d8bfc4dacbafbb7ebd72074e9b16531b52a70abf06fed2e716bd99c
```

This audit is conditional on the selected-witness framework and its pinned
dependencies.  It neither proves nor disproves the remaining shared
nonflat rank-deficient packet, the curved overlap theorem downstream of a
doubly-good pair, the full N=8 source theorem, or Krenn's conjecture.
