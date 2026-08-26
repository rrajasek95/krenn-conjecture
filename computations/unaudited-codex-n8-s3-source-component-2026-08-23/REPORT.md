# The nonliteral S3 class has a three-row degree-five dual

The 66-term universal cubic kernel splits exactly into 14 literal mixed
cubics, all in the constant provider word `12012000` (code 3780), and a
52-row nonliteral residual.  The physical skeleton split is

```text
3P2 / P3+P2 / P4 = 28 / 28 / 10.
```

All 66 rows are squarefree matchings on six distinct site-colour ports, but
only 28 are physical matchings.  Neither an N4 degree-two leading fibre nor
an N6 degree-three leading fibre contains an S3 row.

In homogeneous total degree five, the complete `y<=3` component of every raw
mixed-source column `t*g` and `x*g` meeting the nonliteral residual has only
1,311 rows and 330 columns.  Its column rank is 330 over both GF(1009) and
GF(1013), while the residual is separated over Z by

```text
+ 0c4fcc  + 1557a7  - 3072a7.
```

The pairing is one.  Only two source columns meet this dual, and each meets
it in two rows with cancelling coefficients.  The support is minimal: the
exact incidence search finds no one-row stopping set and 13 two-row stopping
sets, none separating; at support three, 28 separators appear.

The 38 collision rows are not the archived physical path-forest/Bianchi
cells.  They are nonspanning `P3+P2` or `P4` triples, but polarization splits
every repeated physical site into distinct colour ports.  This is an exact
diagonal-Tor signature and truncated dual, not yet an identification with the
archived higher Bockstein class.

Reproduce with

```sh
python3 audit_s3_source_component.py --check-results
python3 -O audit_s3_source_component.py --check-results
python3 -I -S audit_s3_source_component.py --check-results
```

The checker/result are
[`audit_s3_source_component.py`](audit_s3_source_component.py) and
[`results_s3_source_component.json`](results_s3_source_component.json).
