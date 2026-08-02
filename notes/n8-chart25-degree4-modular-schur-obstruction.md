# Chart-25 degree-four source-faithful modular Schur test

The complete degree-four chart-25 block has been tested without freezing the
degree-three certificate.  All 31,584 kernel directions of the coupled
degree-two/three source block are retained and transferred into the
degree-four quotient.  The result is identical modulo 1009, 1013, and 1019:
the degree-four target is not in the source-faithful image.

This note records a three-prime computation.  By itself it is not yet a
characteristic-zero obstruction; that requires an exact rational dual and an
exact replay against every source family.

## Zero-fill and weighted-core decomposition

The 913,608 leading degree-four column-orbits have support sizes only

```text
size:    1       2      3       4      6    9    12
count: 241134  284312  31837  317493  28656  384  9792
```

Zero-fill leaf peeling certifies 207,143 independent pivots and leaves a
270,600-row core.  Its 257,604 remaining two-support columns are contracted
by weighted union--find.  There are 100,085 balanced weighted components.
The projected higher-support columns have rank 64,221, so

\[
 \operatorname{rank} A_4
 =207143+(270600-100085)+64221
 =441879.
\]

Thus the leading degree-four cokernel has dimension 35,864.  The fixed
degree-four target has a 3,434-coordinate remainder in the deterministic
echelon order.

## Full lower-kernel transfer

The lower coupled block has rank 27,904 on 59,488 columns and therefore
kernel dimension 31,584.  Rather than materializing those kernel vectors,
the Schur calculation propagates each column's degree-four tail through the
lower elimination.  Every zero lower remainder produces one kernel
generator directly in the 35,864-dimensional degree-four quotient.

All 31,584 generators are processed.  Their transferred image has rank
17,224.  The complete coupled rank through degree four is therefore

\[
                 27904+441879+17224=487007,
\]

with dual dimension 20,440.  The source-faithful target remains inconsistent
and has a 3,306-coordinate deterministic remainder.  Every rank, pivot-count
trajectory, and remainder support is identical for all three primes.

## Reproduction and scope

The long-running analyzer is

```sh
python3 -u computations/analyze_n8_chart25_degree4_morse.py peel
```

After its transient census and peel caches exist, a single-prime state for
dual extraction is produced by

```sh
python3 -u computations/analyze_n8_chart25_degree4_morse.py state 1009
```

The compact structural ledger is checked by

```sh
python3 computations/verify_n8_chart25_degree4_modular_schur_ledger.py
```

Its digest is
`c8d8086cb97e5298300ac15b3e8fed6b0994a5d3b3bcdaf15b253ad5613a86af`.
The pickle caches are deliberately excluded from version control: they are
discovery accelerators, not proof artifacts.  A permanent theorem must use
the exact-dual checker, not this modular ledger alone.
