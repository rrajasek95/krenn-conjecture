# O4 third 158-cell face: integral direct unit

After promoting the second-layer collision on the first direct-oracle-open
face, the exact O4 downset CEGAR remains at 35 omissions and returns a new
158-cell support.  Its complete 8,100-fibre shadow passes.

The three-tier coefficient oracle stops at its second tier.  The 64 unique
plus binomials have integral exponent rank 24 and all 40 dependencies have
consistent character.  Reducing all 4,321 generators gives 39 one-class
rows.  Record 3306 is a coefficient-one Laurent monomial, and expanding its
six parent relations gives a 12-term ordinary `U^1` identity using five
original generators.  Thus the face is empty over every field.  Eight
distinct O4 transports of its support-faithful witness clause are emitted.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_third_face_direct_unit.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_third_face_direct_unit.py
```
