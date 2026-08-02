# Chart-25 source-faithful degree-four census

The degree-four continuation cannot be tested after freezing the existing
1,634-column certificate.  The complete source-faithful block must retain
all 3,690 degree-two column-orbits and all 55,798 degree-three column-orbits,
including their 1,638-dimensional degree-two kernel and all subsequent
degree-three kernel freedom.

Starting with the degree-four residual and the degree-four tails of every
one of those earlier columns gives 290,127 row-orbits.  Closing under every
mixed column whose first nonzero `K`-degree is four gives:

| closure layer | new row-orbits | new column-orbits |
|---:|---:|---:|
| 1 | 135,724 | 632,519 |
| 2 | 45,754 | 225,805 |
| 3 | 4,922 | 47,720 |
| 4 | 1,216 | 5,836 |
| 5 | 0 | 1,728 |

Thus the coupled filtered block has row dimensions

```text
(2264, 27440, 477743)
```

and column dimensions

```text
(3690, 55798, 913608).
```

This is an exact orbit census, not a rank claim.  A global sparse Gaussian
elimination on the 477,743 by 913,608 last block would invite catastrophic
fill.  The next computation instead uses target-directed closure and a
Schur--Bockstein separator loop: solve the target component, scan all omitted
degree-four source directions and all transferred tails of the complete
lower-layer kernel, and add every direction detected by the separator.

The lightweight ledger audit is

```sh
python3 computations/verify_n8_chart25_degree4_census_ledger.py
```

The full (long-running) census can be reconstructed with

```sh
python3 -u computations/analyze_n8_chart25_degree4_bockstein.py census
```

Its structural ledger digest is
`e87b47332355db290841b80afff95c32d6519efe4bc0f6ac08d10273a83c70e1`.
The 39 MB transient pickle cache is deliberately not a proof artifact and is
not committed.
