# The universal `S3` transfer has a surviving collision/Tor class

Status: **UNAUDITED exact bounded negative result**. No `C10`, `D9`, or full
degree-six frontier was constructed.

## Literal cubic output test

The frozen packet has exactly

```text
28  3P2 (matching on six vertices),
28  P3+P2,
10  P4.
```

Across all 6,558 normalized mixed generators there are 111,826 cubic
monomials, each with global multiplicity one. Exactly 14 of the 28 matching
rows occur. All 14 belong to the single source word
`12012000` (code 3780); its cubic layer has 32 terms. Their `S3` signs are
13 minus and one plus, whereas every source coefficient is plus one. The
other 14 matching rows do not occur in any literal cubic output; the
lex-first is `0491ae`.

Therefore the often-suggested “cancel the 14 literal rows and retain a
52-row class” is not source-faithful. The 14 rows cannot be selected
individually from their common 32-term source layer, and their signs are not
proportional to it.

There is a second constant-one provider, word `21000012` (code 5108). With
the same frozen linear section its transfer has 58 terms and overlaps the
66-term transfer in only `0491ae,089bcc`, both with coefficient one. The
constant-cancelling difference has 120 terms, 60 of each sign. With the
exact stabilizer-equivariant linear section the corresponding counts are
`68,60,124`, again with a balanced `62/62` difference.

This extra provider does not kill the nonliteral residue. The independent
complete raw-degree-five low-source audit gives the minimal exact dual

```text
lambda = delta_0c4fcc + delta_1557a7 - delta_3072a7.
```

It annihilates all 330 raw low-source columns on the 1,311-row component,
pairs the 52-row residue to one, and annihilates
`S3(5108)-S3(3780)` for both the frozen and equivariant sections. No
one- or two-row low-source separator exists. Thus the second provider is an
exact additional cell, but not the missing filler.

## Existing cell attachment

A complete stream through all 84,005 degree-five Buchberger cells gives:

```text
38 collision rows,
 8 rows incident to 4 degree-five cells,
30 rows absent every degree-five cell.
```

All four incident cells are Hamming-two direct-double cells, have 180 terms,
and contain the `S3` rows away from their leading pivots. The four canonical
Bianchi star cells are already included in this complete scan and have zero
intersection. Closing the associated `y^3` component gives only 187 rows and
10 columns (8 degree-five and 2 literal cubic columns); it does not absorb
`S3`.

The independent complete audit of all 529,440 degree-one PM4 translates has
zero cells incident to `S3`. The first three frozen degree-six cells, the two
explicit path-bearing weighted representatives, and the two explicit
branched/collision representatives also have zero collision-row incidence.

The smallest exact survivor for these cell families is

```text
row        0e4faa
coefficient +1
skeleton   P3+P2 on edges 02,13,34.
```

The one-row functional `delta_0e4faa` annihilates every cell family just
listed and pairs with the collision packet to one. This is a bounded Tor
certificate, not a claim about the unenumerated full degree-six frontier.

## Canonical triangle coupling: one valid dual channel

Fix cap pair `67` and residual triangle `012`. A source-faithful normalized
response coordinate requires both endpoint orientations, a disjoint common
spectator, and the omitted fourth matching edge among the normalized support
cells. Among the 38 collision rows:

```text
28 have no formal 6/7 response-spoke factorization;
10 have at least one formal factorization;
 0 give a valid normalized response coordinate.
```

The apparent complete pair `5893de+589cd5` repeats physical site `4`: its
third edge is not a disjoint spectator. The apparent internal half-packet
`316fb7` repeats cap site `6`: its third edge is `36`, so it is likewise not
a response coordinate. This corrects the weaker formal-factor audit; the
primal 66-term packet has no response attachment.

The primal 66-term packet still supplies no complete internal response.
However, the minimal **dual** has a sharper nonzero restriction. Its rows are

```text
0c4fcc : edges 02,13,45                 coefficient +1
1557a7 : edges 03,14,34 (a simple P4)   coefficient +1
3072a7 : edges 06,17,34                 coefficient -1.
```

The last row is one orientation of
`K00*R_01[1,2]*A_34[1,2]`; the other orientation is `3969a7`, on which the
dual has weight zero. Therefore evaluation on the complete response packet
is `-1`. Its omitted fourth matching edge is exactly the normalized anchor
`A_25[00]=1`, so this is literally the `xy=01`, `t=2`, `O=345` response
coordinate, not a merely formal monomial match. The tiny class maps
nontrivially to exactly the `K00` internal triangle channel.

All 28 deletion-minimal exact three-row duals in the complete raw
degree-five low-source component were then replayed. Sixteen have a valid
internal response restriction, with 20 packet occurrences in three
templates:

```text
edge 01, output 12, K-cell 00 : 8
edge 02, output 10, K-cell 00 : 6
edge 12, output 02, K-cell 00 : 6
```

Thus the fixed-chart channel image has rank `1` in `Mat_3^*`, with the other
eight cells missing. Global colour transports on the corresponding
colour-permuted charts give only the three diagonal cells, rank `3`, leaving
the six off-diagonal cells missing. In particular, the naive direct-blocker
HPL lift

```text
<K,A_67> = K00 + sum_(a,b)!=(0,0) y_67[a,b] K_ab
```

fails at its first correction if one asks the minimal dual module itself to
supply all nine channels.

## The four blockers collapse on the authoritative open

That rank defect is **not** an interior obstruction. The independently
replayed pure-word quotient theorem gives, in
`Mat_3^*/rowspan(L_T)`,

```text
[K00] = H0 [<K,A_67>]
[K11] = H1 [<K,A_67>]
[K22] = H2 [<K,A_67>].
```

Its literal hypotheses match the tiny response exactly: cap `67`, triangle
`012`, response edge `xy=01`, opposite vertex `t=2`, five-set
`W=01345`, spectator `A_34[12]`, and implicit support edge
`A_25[00]=1`. The quotient identity is source-universal; the rank-nine
five-set maps absorb the response rows, so it need not have the same output
colours as the pure row used to derive the identity.

Consequently, when all nine cyclic/colour five-set response increments are
`9` and `H0*H1*H2 != 0`, the four **evaluated blocker classes**

```text
K00, K11, K22, <K,A_67>
```

are equivalent. Any one of the 560 triangle-membership branches therefore
puts the **response image** of `K00` in the same quotient class. This does
not annihilate the inverse-system `S3` class. The two orientations
`3072a7` and `3969a7` are separate degree-six singleton source columns;
the dual reads them as `-1` and `0`. The quotient theorem supplies no source
syzygy joining/cancelling them. Likewise, the sixteen off-support direct
corrections are sixteen independent degree-seven singleton columns.

Thus the exact quotient identity supersedes nine-channel HPL lifting only
for the blocker **disjunction**, not for chain filling. The remaining
obligations are:

1. even on the common open, crossed-half/source-chain coherence for the
   completed response packet;
2. a five-set determinantal boundary: at least one of the nine `(c,t)`
   response increments is at most `8`; and
3. the pure-cofactor divisor `H0*H1*H2=0`.

This is a conditional attachment, not yet a contradiction on either
boundary. The quotient replay passes at both audit primes and reconstructs
all `756` literal `15+90` identities per source/prime.

It is not the cap-error polynomial: the dual is cubic in source cells,
whereas `s*r^2*x` and `r^3` have source degree six. Nor is it the familiar
`C4`/parallel Bockstein: its three physical skeletons are simple
`3P2,P4,3P2`, with no cycle and no parallel edge.

## Scope

This retires a direct attachment of `S3` to the currently frozen cubic,
degree-five, Bianchi, PM4-translate, and named path/collision cells. It does
not prove all-higher-degree nonmembership. The tiny dual's response image
attaches to the collapsed triangle blocker on the simultaneous five-set
rank-nine/pure-cofactor open, but the source-complex class is not thereby
filled. The genuine remaining obligations are crossed-half/chain coherence
on that open and the stated determinantal/cofactor boundary; the four-way
blocker disjunction itself is retired there.

Replay:

```sh
python3 computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py --write-results
python3 computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py --check-results
python3 -O computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py --check-results
python3 -I -S computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py --check-results
python3 computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22/check_results.py
```

Hostile `--mutate` must fail. The logical digest is frozen in the result.
