# O4 second incidence frontier: signed-Laurent oracle

After transporting the first 159-cell odd-circuit clause, the exact O4
support CEGAR still has a 159-cell maximum.  Relative to the killed face it
exchanges just two support bits: `x02_10` is restored and `x12_10` is
removed.  Its frozen coefficient system has 4,321 generators.

The generic exact coefficient oracle takes every plus binomial, constructs
its maximal Laurent exponent lattice, checks the sign character over
`GF(2)`, and reduces every coefficient generator modulo the resulting
character.  On the new face it finds:

- 306 plus binomials of rational exponent rank 20;
- 286 reconstructed dependency generators, all even-character;
- a direct `GF(2)` solution to all 306 sign equations; and
- no coefficient generator reducing to a single nonzero Laurent class.

As a positive control, the same code sees 315 plus binomials on the prior
face, an exponent rank of 21 but augmented signed rank 22, and recovers the
odd dependency on records 2471, 3648, and 3738.  Thus the one-cell exchange
removes exactly the signed-holonomy obstruction used by the preceding
certificate.  The new face remains coefficient-open: the next atom must use
a multi-class syzygy or a tensor/rank quotient, not another plain odd circuit
or one-class Laurent reduction.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_laurent_oracle.py
python3 -O computations/verify_n8_d1_residue_orbit4_second_incidence_frontier_laurent_oracle.py
```
