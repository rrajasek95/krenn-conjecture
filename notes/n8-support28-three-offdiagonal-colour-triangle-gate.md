# Three-cell colour triangles cannot repair the affine support-28 orbit

## Result

The parity-minimal three-cell off-axis packet is

\[
 A_{e_0}[0,1],\qquad A_{e_1}[1,2],\qquad A_{e_2}[2,0],       \tag{1}
\]

up to reversing endpoint orientations and permuting the three colour-pair
types among three disjoint physical edges.  Its colour-incidence graph is a
triangle, so every colour has even degree.  Unlike one off-diagonal cell,
and unlike a non-Eulerian three-cell set, (1) can occur in an all-even source
word.

Nevertheless every packet (1) leaves a permanent-triangle Laurent unit
unchanged on both affine support-28 target charts.  Hence an exact source
must lower the 48-cell diagonal support or contain a larger simultaneous
off-axis support.

Checker:
`computations/verify_n8_support28_three_offdiagonal_colour_triangle_gate.py`.

## Labelled packets and marked-support orbits

There are 420 matchings of three edges on six of the eight sites.  Assigning
the three unordered colour pairs has `3!` choices, and orienting their
endpoints has `2^3` choices.  Therefore

\[
                          420\cdot6\cdot8=20160             \tag{2}
\]

literal packets occur in each target chart.

The exact fixed-support orbit census is:

| target chart | support stabilizer | packet orbits | orbit sizes |
|---|---:|---:|---|
| pair target `12` | 4 | 5,040 | all size 4 |
| full target `012` | 12 | 1,731 | 3 size 2, 3 size 4, 93 size 6, 1,632 size 12 |

Every representative retains its physical edges and ordered endpoint-colour
labels.  The checker freezes the complete representative registry by hash.

## The covering lemma

Let `C` denote the 96 permanent-triangle certificates.  Their 288 row slots
use 96 distinct even words.  The exact word-incidence histogram is

```text
24 words occur in 2 certificates,
48 words occur in 3 certificates,
24 words occur in 4 certificates.
```

In particular one word can spoil at most four certificates.

For an arbitrary off-axis matching packet `P`, let `W(P)` be the set of
even words in which all marked cells of `P` occur and the remaining sites
are completed by supported diagonal cells.  Then the certificates spoiled
by `P` are contained in

\[
                    \bigcup_{w\in W(P)} C_w,               \tag{3}
\]

where `C_w` is the set of certificates containing `w`.  Consequently

\[
             \#\operatorname{Spoil}(P)\le4\,|W(P)|.        \tag{4}
\]

This is the reusable packet-to-word covering lemma.  It is independent of
the packet size; only the computation of `W(P)` changes.  It also gives a
global necessary condition: any simultaneous off-axis repair that meets all
96 permanent triangles must generate at least 24 distinct certificate
words.

## Application to three-cell colour triangles

Packet (1) fixes the colours of six sites.  The two remaining sites form one
physical edge, which must be diagonal.  The affine support of that edge has
one, two, or three available colours, so

\[
                              |W(P)|\le3.                   \tag{5}

Across the 20,160 packets the exact word-count histogram, identical in both
charts, is

```text
|W(P)|=1: 8,640 packets
|W(P)|=2: 8,640 packets
|W(P)|=3: 2,880 packets.
```

Equations (4)--(5) prove immediately that at most 12 certificates can be
spoiled.  The exhaustive literal calculation attains the bound: the worst
packets spoil 12, so every packet leaves at least

\[
                              96-12=84                     \tag{6}

complete Laurent-unit certificates.

The checker additionally computes the augmented hafnian on every packet
word and finds exactly one new monomial containing all three marked cells.
It then chooses an untouched certificate, verifies its full augmented rows
equal the original diagonal rows, and replays the characteristic-zero unit

\[
 cvwF_1+buwF_2-auvF_3=2bcduvw.                             \tag{7}

Thus (6) is not only an incidence shadow: every packet has a literal
source-row coefficient certificate.

## Proof consequence

The one-cell, two-cell, and parity-minimal three-cell neighborhoods of the
unique affine diagonal orbit are now closed without cap selection.  The
endpoint-polarized evaluation remains available and source-labelled, but
these sparse packets are inconsistent before activity or cleanliness is
tested.

The next productive object is not another isolated packet orbit.  It is a
simultaneous off-axis support whose compatible word union can hit all 96
certificates.  The covering lemma gives its first exact necessary datum:
at least 24 distinct certificate words.  A SAT/set-cover search on the
packet-word incidence hypergraph can now seek the minimum support generating
such a cover; any smaller union is excluded automatically by (4).

## Reproduction

```text
python3 computations/verify_n8_support28_three_offdiagonal_colour_triangle_gate.py --mode structural
python3 -O computations/verify_n8_support28_three_offdiagonal_colour_triangle_gate.py --mode full
python3 -I -S computations/verify_n8_support28_three_offdiagonal_colour_triangle_gate.py --mode exhaustive
```

All modes return the same frozen ledger digest.
