# The second extremal localized chart has a seven-orbit boundary dual

## Exact result

Let \(P_{25}\) be the twelve-variable pure matching-triple monomial in chart
25 of the exact 31-chart ledger.  In the balanced 24-port, degree-twelve
Macaulay component of the full 252-variable ring, an exact rational
functional \(\Lambda_{25}\) satisfies

\[
       \Lambda_{25}(P_{25})=1,
       \qquad
       \Lambda_{25}(QH_w)=0
\]

for every mixed word \(w\) and every balanced degree-eight multiplier \(Q\).
Consequently

\[
                         P_{25}\notin I_{\rm mix}.
\]

This is an ordinary ideal-membership obstruction, not a radical or
localized nonmembership result.  It does not obstruct a certificate for
\(H_0H_1H_2\), nor one obtained after multiplying by a support power.

## Compact structure

Modulo the order-eight stabilizer of chart 25, the complete component through
off-support degree four has

\[
               2{,}870\text{ row orbits},
               \qquad9{,}516\text{ column orbits}.
\]

Its modular discovery rank is 2,864, but the final certificate is replayed
over \(\mathbb Q\).  The invariant dual uses only seven row orbits, with
coefficient multiset

\[
                         \{-2,-2,1,1,1,1,4\}.
\]

Expanding the orbit functional gives only 23 actual matching rows.  Their
values are one copy of \(1\), fourteen copies of \(1/2\), and eight copies
of \(-1/2\).  The union of their coordinate supports has size only 36:
twelve reference variables and 24 additional endpoint-colour variables.

This is substantially smaller than the 93-row, 60-coordinate dual on chart
26.  It isolates a normalized 24-variable chart on which to seek the analogue
of the chart-26 pure-product certificate.

## Completeness of the bounded closure

Every supported dual row has off-support degree at most four.  If a Macaulay
column can pair nontrivially with the functional, it contains one of these
rows, hence has minimum off-support degree at most four and lies in the
incidence component closed by the checker.  Columns of larger minimum degree,
and disconnected columns, pair with the zero extension of the functional.
Thus the bounded component replay proves annihilation of the entire balanced
Macaulay map, not only of a sampled submatrix.

## Relation to the two extremal charts

Charts 25 and 26 are the only pure matching-triple supports with just two
mixed support one-factors.  Chart 26 is the expanded-prism support used by
the existing 60-edge certificate and full-source filtration.  The present
dual shows that chart 25 has an even smaller natural coordinate carrier.
The next exact test is pure-product ideal membership on this normalized
36-coordinate chart, followed—if positive—by Laurent rehomogenization and
a full-source lift.

## Reproduction

```sh
python3 computations/verify_n8_chart25_boundary_dual.py
python3 -O computations/verify_n8_chart25_boundary_dual.py
python3 -I computations/verify_n8_chart25_boundary_dual.py
python3 -S computations/verify_n8_chart25_boundary_dual.py
```

The checker reconstructs the chart and its full stabilizer, closes the exact
component, replays all 9,516 invariant columns, expands the rational
functional, replays individual representative columns, and freezes the
complete ledger by SHA-256.
