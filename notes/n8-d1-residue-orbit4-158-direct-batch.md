# O4 158-cell direct-Laurent batch

The four 159-cell coefficient orbits close the entire omission-34 layer.
The exact support census therefore moves to 35 omissions and 158 live cells.

A bounded coefficient-CEGAR batch closes the first two 158-cell maxima.  In
both cases the 54 unique plus-binomial rows have rank 20, an exact full-output
generator reduces directly to the same Laurent monomial shape, and expansion
back to the original equations gives an integral ordinary `U^1` identity.
Each certificate uses seven source records and 18 localized witnesses.  The
two faces give 16 distinct transported clauses.

The batch then freezes the first genuinely open direct-Laurent frontier:

- 158 localized cells and 4,321 exact coefficient generators;
- complete 8,100-fibre support shadow;
- 54 unique plus rows, rank 20, and 34 even-character dependencies;
- no odd dependency and no generator reducing directly to one Laurent class;
- generator SHA-256
  `7097b288a7a41be1fe4abb42ee8de20f49c5e69a2a1f720268ac7568b02aa9ce`.

This is a deliberately sharp stop: the next attack should iterate the 502
reduced two-class equations (with exact rational character tracking) or use a
common transfer/holonomy determinant.  The checker does not claim the open
face is coefficient-feasible.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_direct_batch.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_direct_batch.py
```
