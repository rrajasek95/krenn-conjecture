# Phase-hyperfield / orthogonal-tract Wick screen

Status: **exact negative screen; signless hafnian cancellation is not Wick
orthogonality and does not force a clean pair**.

The strong tract axiom is the alternating quadratic relation `W2` between
principal Wick coordinates (Jin--Kim, Definition 3.1). A vanishing signless
hafnian supplies only a phase-hyperfield zero among its own perfect-matching
monomials. These are different relations.

The smallest exact counterguard has four ports:

```text
A01*A23 = 1,  A02*A13 = -2,  A03*A12 = 1,
H = 1-2+1 = 0.
```

Thus the matching-term phases `(+,-,+)` contain zero in their hyper-sum.
But the literal four-point Wick packet

```text
p_empty*p_0123 - p_01*p_23 + p_02*p_13 - p_03*p_12
```

has phases `(0,-,-,-)` when `p_0123` is the signless `H`; its hyper-sum
does not contain zero. Replacing `p_0123` by the genuine signed Pfaffian
gives `4-1-2-1=0`, confirming that the test distinguishes Wick structure
from ordinary signless cancellation. Unit tail edges `45,67` embed the same
example in an eight-site fibre: exactly three of the 105 matching terms are
live, with coefficients `1,-2,1`.

The exact four-site ternary-GHZ control is exceptional. Its 12-port live
graph is six disjoint edges. In site-major order its literal pure-colour
W4 tests are `PASS, FAIL, PASS`; after adding source-dependent edge-adjacent
ordering/orientation, the matrix is block diagonal and all 2,048 even
principal coordinates are genuine Pfaffians. This proves existence of a
Pfaffian presentation for that sparse source, not a canonical Wick
interpretation of signless hafnians.

The six-site obstruction does not transport through the phase tract. A full
18-port Wick vector has 131,072 even principal coordinates, while the GHZ
system fixes only 729 one-hot rows. Orthogonal exchange may leave the one-hot
code through hole/double-occupancy sets. The characteristic-two certificate
also cannot map to the phase hyperfield: `1+1=0` in `F2`, whereas zero is not
in `1 boxplus 1`. The characteristic-zero proof additionally uses matrix
ranks, minors, and shared Laurent magnitudes, none of which follows from the
phase-Wick support axioms.

The eight-site Laurent control again has a 24-port graph of 12 disjoint
edges, hence an exact oriented field-Wick presentation (4,096 union
coordinates checked). At nonzero `t`, however, its top tensor has three
valuation-zero pure terms and two valuation-one mixed terms. All five have
phase `+`; the phase shadow never records that the latter two tend to zero.
A tropical extension could retain that valuation, but ordinary phase data
cannot distinguish the boundary from nearby non-GHZ tensors.

Therefore the 105-term equations yield no tract orthogonality beyond their
own ordinary polynomial zeros. Where an independent Pfaffian orientation is
available, it still forgets the shared magnitudes, valuations, and labelled
cap-response incidence needed for active cleanliness.

Primary definition: [Jin--Kim, *Orthogonal matroids over tracts*, W2](https://arxiv.org/html/2303.05353v2#S3.SS1).
Standard, optimized, and isolated/no-site modes agree at logical SHA
`139f05d4fdc9071c71b8555639a7068aef911819d38284492a528871ba580cd4`.

