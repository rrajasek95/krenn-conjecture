# The dense mate cube closes on a top-null K4 factorization

## Exact verdict

The dense rank-one cancellation tensor forced by the repeated carrier is
coefficient-feasible in one genuine common quadratic `q`.  It does not by
itself contradict the one-bad packet.

Start with the doubled carrier

```text
M0 = 01|23|45
```

and its four missing recombination words `001,010,101,110`.  The single
aligned physical matching

```text
F0 = 01|24|35
```

supplies a `-1` mate in all four words and obeys the same exact Plucker
monomial relation.  Those four repairs export eight singleton mixed words.
There is a unique remaining perfect matching on the residual `K4`:

```text
C = 01|25|34.
```

Four decorated cells on `25,34`, with value matrix

\[
 \begin{pmatrix}1&-1\\-1&1\end{pmatrix}
   =\binom{1}{-1}(1,-1),                               \tag{1}
\]

cancel all eight exports.  The final 14-cell quadratic has exactly twelve
live top-word fibres, each a two-term sum `1-1=0`.  Hence

\[
                              q^{[3]}=0.                \tag{2}
\]

This is an exact full coefficient calculation, not a support census.  The
checker is
`computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py`.

## The Plucker square

Write the four frozen cube monomials as

\[
 m_{00},m_{01},m_{10},m_{11}.
\]

They are edgewise products of two independent decoration choices, so

\[
                         m_{00}m_{11}=m_{01}m_{10}.     \tag{3}
\]

Decorating `F0` by the same four words gives mate monomials `n_ab` with the
literal exponent identity

\[
                         n_{00}n_{11}=n_{01}n_{10}.     \tag{4}
\]

Set both decorated `24` cells to `-1` and every other cell to `1`.  Then
`m_ab=1`, `n_ab=-1` for all four indices.  Thus all four full mixed rows
vanish while the required Segre minors remain zero.  This uses the aggregate
coefficient coupling from `e3c52ae`; the four mates are not chosen
independently.

## Why the cross carrier is forced

After deleting the common edge `01`, the two physical carriers use

```text
23|45,   24|35
```

on sites `2,3,4,5`.  Their only third perfect matching is `25|34`.  The
eight new singleton words factor into the two decoration choices on `25`
and the two choices on `34`.  Matrix (1) gives exactly the negative of all
eight old singleton coefficients.  This is the smallest source-faithful
completion of the dense mate cube.

Relative to the canonical one-bad datum, this factorization is revealing:

- `24|35` is the aligned diagonal-hole matching;
- `25|34` is the cross-pair matching.

Thus the repeated-provenance orbit does not leave another free cube
coefficient.  It lands exactly on the interface between the diagonal and
ordered cross response rows.

## The precise missing theorem

The completed common quadratic (2) satisfies every one of its twelve live
mixed top rows, but it misses the one-bad unary equation in exactly the pure
row:

\[
                         q^{[3]}-X_0=-X_0.             \tag{5}
\]

It does not supply endpoint stars or the two diagonal response anchors.
Therefore it is not a one-bad packet or a Krenn counterexample.

The next carrier theorem must use (5) together with the genuine response
rows to show that adding a pure top carrier cannot preserve the rank-one
`24|35`/`25|34` cancellation, or else that this cancellation yields the
square-zero clean cap.  Another independent matching-mate or Plucker
identity cannot close the gap: the K4 factorization already realizes all of
them exactly.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py
```
