# Exact obstruction for the 26-cell selector candidate

The support produced by `search_selector_cancellation_support.py` cannot
realize the eight-party three-color diagonal tensor over any field.  This is
not a numerical conclusion: three of its coefficient equations already give
an immediate multiplicative contradiction.

Number the 26 allowed cells in the order used by
`computations/search_selector_candidate_weights.py`, and write their weights
as `x_0,...,x_25`.  Lossless enumeration of all 105 perfect matchings and all
allowed decorations gives

\[
 [1^8]H=
 (x_2x_{17}+x_4x_{14})(x_7x_{24}+x_{10}x_{21}),             \tag{1}
\]

\[
 [12112212]H=x_8x_{22}(x_2x_{17}+x_4x_{14}),                \tag{2}
\]

and

\[
 [2^8]H=x_3x_8x_{15}x_{22}.                                \tag{3}
\]

For the target `Delta_(8,3)`, equations (1) and (3) equal one, while
(2), being a mixed coefficient, equals zero.  Equation (1) makes

\[
                    A:=x_2x_{17}+x_4x_{14}
\]

nonzero.  Equation (3) makes `x_8x_22` nonzero.  Their product is therefore
nonzero in every field, contradicting (2).  Rescaling the three diagonal
target coefficients to arbitrary nonzero values does not change the proof.

The independent verifier

```text
uv run python computations/verify_selector_candidate_obstruction.py
```

materializes all `3^8=6561` coefficient fibers (including the identically
zero fibers), checks that there are exactly 41 nonzero formal fibers and 113
decorated matching monomials, and verifies the three displayed expansions
directly from the cell list.
