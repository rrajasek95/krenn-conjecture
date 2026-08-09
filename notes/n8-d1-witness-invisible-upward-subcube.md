# N=8 D1: witness-invisible upward-subcube closure

The three-binomial certificate which killed the m=10 semantic support is
stable under a 107-dimensional upward support subcube.  The checker
`computations/verify_n8_d1_m11_six_candidate_closure.py` proves this directly
from the three full-output fibres and also closes the six support-shadow
extensions first encountered at m=11.

The m=10 semantic support has 77 localized cells.  Of the 140 other
E1-admissible cells, only 33 occur in any perfect-matching monomial of the
three witness words.  The remaining 107 cells are witness-invisible: 85 are
off Sigma and 22 are the Sigma cells absent from the base support.  Adding
an arbitrary subset of these 107 cells cannot alter any of

```text
u1 (a f + b d),   u2 (a e + b c),   u3 (c f + d e).
```

The exact identity

```text
a (c f + d e) - c (a f + b d) + d (a e + b c) = 2 a d e
```

therefore continues to give `U^3` in every localized coefficient ideal in
this subcube, over characteristic other than two.  The checker reconstructs
the witness polynomials at the maximal 184-variable support, verifies that
they are unchanged, and verifies the ordinary sparse-polynomial saturation
certificate there.  Every smaller subcube support follows by the same three
equations.

The six m=11 Boolean supports add one of
`x_67_01, x_67_02, x_67_10, x_67_12, x_67_20, x_67_21`.  All are inside the
invisible set.  The checker additionally evaluates all 8,100 fibres and
reconstructs the complete coefficient system separately for all six.

The checked ledger SHA-256 is
`3cee71ffa3c4d8965e16965dc1afeaeefef5ffe98e6f300b861c9c4192871507`.
The remaining boundary for this particular identity consists of the 33
witness-visible cells; alternate binomial identities may cover parts of that
boundary and enlarge the chart-wide closure.
