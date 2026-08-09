# N=8 orbit transfer is not a chart-local certificate

The filtered plateau calculations beginning with the 31 pure root types are
exact in the `S8 x S3` **orbit-compressed incidence module**.  They do not yet
lift to an individual localized chart.

The decisive provenance audit replays the seven root-plateau kernel
representatives.  Their support sizes are

```text
6, 8, 6, 8, 11, 5, 5.
```

For every representative, the intersection of the root charts incident to
all of its support columns is empty.  In particular, none of the seven
relations is assembled entirely from columns available in one common
`P_j` chart.  The representative associated with kernel source column 26,
for example, mixes eleven support-column orbits touching root charts
`1,2,3,4,5,6,10,13,14,19,22`; their common intersection is empty.

Canonicalization is also genuinely many-to-one.  Each physical fibre has 105
labelled terms, while its canonical outputs occupy only 7 through 65 orbit
types in this root census, with multiplicities as high as 48.  Thus the orbit
matrix is not the labelled Macaulay matrix with rows retained separately.

Consequently, the diagonal-12 through diagonal-8 transfers are useful global
orbit-incidence evidence and exact/modular counterguards, but they prove
neither chart-26 membership nor membership in any other individual localized
source ideal.  This lane stops here.

The smallest missing certificate is one of:

1. a labelled Macaulay relation constructed wholly inside one `P_j`
   localization; or
2. an explicit multiplication by that chart's anchor product that provides a
   common-denominator lift of every cross-chart column and replays the target
   relation before orbit compression.

The checker is
`computations/verify_n8_orbit_transfer_localization_guard.py`.  Its frozen
ledger SHA-256 is
`edfcf65d948469317b5cac65a443e09879572cf536aa52e8704504ad0b45bb7c`.
