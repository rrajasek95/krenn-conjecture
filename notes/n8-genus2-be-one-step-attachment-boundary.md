# Genus-two BE one-step attachment boundary

Date: 2026-08-11

Checker: `computations/verify_n8_genus2_be_one_step_attachments.py`

Parent probe: `computations/verify_n8_genus2_arf_fullnine_syzygy_probe.py`
(`sha256 06c8aebe01e06d03f17203b617be65c5c7b9ff899a040209e27ee252e735d70e`)

## Question

The pinned sixteen-Pfaffian probe leaves every nontrivial odd-principal
Buchsbaum--Eisenbud row with one doubled physical site.  Can the first
genuinely physical attaching layer repair that defect using exactly one
already-audited operation?

The allowed one-step operations are:

1. insertion of one labelled physical cell, including a direct or diagonal
   full-nine cell; or
2. deletion/contraction of one physical pair, as in the audited cofactor
   operation.

This note does **not** compose the two operations.

## Complete physical-degree classification

For an odd set `T` and a BE row indexed by `i in T`, the physical degree is

```text
d_i = 2,  d_j = 1 (j in T - {i}),  d_j = 0 (j outside T).
```

There are `168`, `280`, and `56` such rows for `|T|=3,5,7`.

An insertion raises two physical degrees.  It therefore cannot remove the
doubled site.  Exhausting all 28 physical edges on all 504 rows gives 14,112
candidates and no squarefree candidate.  This covers every endpoint-colour
label on a direct/diagonal full-nine insertion because the label changes the
fine colour grade, not physical occupancy.

There are only five insertion degree types: the inserted edge contains `i`
and its other endpoint is inside or outside `T`; it misses `i` and has two,
one, or zero endpoints in `T`.  In the first two cases the degree at `i`
becomes three.  In the last three it remains two.  The checker records every
sorted degree signature and its multiplicity for each odd size.  For a
contraction there are only two types: a pair containing `i` is the
duplicate-free case below, while a pair in `T-{i}` leaves degree two at `i`.

A nonzero pair contraction lowers one incidence at each endpoint.  It is
duplicate-free exactly for a pair `{i,j}` with `j in T-{i}`.  The exhaustive
census is:

| `|T|` | valid contractions | duplicate-free | holes afterward |
|---:|---:|---:|---:|
| 3 | 504 | 336 | 6 |
| 5 | 2,800 | 1,120 | 4 |
| 7 | 1,176 | 336 | 2 |

Thus the 1,792 repaired rows are honest lower-site cofactor grades, but none
is a squarefree eight-site source row.  Even the closest `|T|=7` case still
needs insertion of the unique edge joining its two holes.  That is a
contraction **followed by** an insertion, hence belongs to the next two-step
layer rather than the task audited here.

## Decorated-word and Arf guards

The literal packet has the three decorated words

```text
00000000, 11111111, 01222222.
```

Comparing every duplicate-free contraction grade across these three words
gives pairwise empty intersections.  Hence a one-step lower cofactor does not
couple either pure diagonal anchor to the crossed row.

The fixed genus-two signing gives 12 physical edges with trivial spin
character and 16 with nontrivial character.  Among the duplicate-free
contractions, 768 are trivial-character and 1,024 are twisted.  The pinned
chart edges `01` and `02` both carry the nontrivial character `13` in the
chosen four-bit basis.  A nontrivial character takes both signs over the 16
sectors, so its sectorwise product is not a scalar multiple of the original
Arf aggregate.  This is an independent obstruction for those candidates;
the physical-degree obstruction applies to all of them.

For completeness, the exact four-bit-basis census is:

| Arf edge label | edges | insertions | valid contractions | duplicate-free contractions |
|---:|---:|---:|---:|---:|
| 0 | 12 | 6,048 | 1,920 | 768 |
| 1 | 1 | 504 | 160 | 64 |
| 2 | 2 | 1,008 | 320 | 128 |
| 4 | 2 | 1,008 | 320 | 128 |
| 6 | 2 | 1,008 | 320 | 128 |
| 7 | 1 | 504 | 160 | 64 |
| 8 | 1 | 504 | 160 | 64 |
| 12 | 3 | 1,512 | 480 | 192 |
| 13 | 3 | 1,512 | 480 | 192 |
| 15 | 1 | 504 | 160 | 64 |

## Exact consequence and scope

No single labelled insertion and no single pair/cofactor contraction repairs
a BE row into a literal squarefree K8 identity.  The duplicate-free lower
cofactors do not join the anchor and crossed source grades.  Therefore this
complete one-step layer reaches neither:

- the source-provenant Component-III residual annihilator; nor
- the weakened Component-II endpoint of `a67ec1d`, namely a scalar-zero cap
  with pure diagonal target and response supported on one physical edge.

This is a finite negative theorem only for the principal odd BE rows of sizes
3, 5, and 7 and exactly one of the two audited physical operations.  It says
nothing about a two-step contraction/reinsertion, a higher derived Pfaffian
construction, or a different source-resolution generator.
