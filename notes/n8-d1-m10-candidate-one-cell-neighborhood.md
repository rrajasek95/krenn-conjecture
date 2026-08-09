# N=8 D1: exact one-cell neighborhood of the m=10 candidate

The 77-cell semantic support first found in branch `334:63` has no
coefficient point after any single E1-admissible cell is added.  The exact
checker
[`verify_n8_d1_m10_candidate_one_cell_neighborhood.py`](../computations/verify_n8_d1_m10_candidate_one_cell_neighborhood.py)
closes all 140 additions over every field of characteristic other than two.

The split is structural.  The previously proved three-binomial certificate
is unchanged by 107 cells: 85 outside Sigma and all 22 absent Sigma cells.
For each of the remaining 33 witness-visible cells, the checker reconstructs
the enlarged coefficient system and finds three full-output binomials.  After
orienting their Laurent exponent differences, their leading and trailing
monomial products agree.  It verifies the ordinary polynomial identity

```text
(a1+b1)a2a3 - b1(a2+b2)a3 + b1b2(a3+b3) = 2a1a2a3.
```

Every factor on the right is localized nonzero.  The checker also multiplies
this compact identity by an exact monomial quotient and verifies that a power
of the product of all 78 localized variables belongs to the original
coefficient ideal.  Thus no Laurent solver or Groebner-basis verdict is
trusted.

This closes the complete immediate admissible neighborhood of the m=10
support, not its whole upward closure.  Several visible cells added
simultaneously can introduce extra matching terms into a selected binomial.
The next structural target is an extension-robust finite circuit cover of all
subsets of the 33 visible cells, or a chart-wide saturation certificate.

The frozen ledger SHA-256 is
`bf2eab98ffb22213c7cce1951670ab5d13d36e22c3e2400eacfa767dd17db899`.
