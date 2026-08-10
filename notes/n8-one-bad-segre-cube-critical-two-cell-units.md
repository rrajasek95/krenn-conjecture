# The nine primary critical two-cell deformations are top-empty

## Exact result

Consider the fixed Segre--K4 quadratic $H$, arbitrary cells of decorations
`00`, `11`, and `22`, and the 76 remaining decorated-cell directions.  For
the pinned six-row diagonal-carrier certificate, exactly nine of the

\[
                         \binom{76}{2}=2850
\]

mixed second variations are nonzero.  The other 2841 joint remainders
vanish identically.  The nine critical pairs are

```text
02:10 + 14:02        02:20 + 15:01
03:10 + 12:02        03:10 + 14:02
03:20 + 15:01        04:10 + 12:02
04:20 + 15:01        05:10 + 12:02
05:10 + 14:02.
```

Every one of these nine full two-cell top ideals is the unit ideal over
$\mathbb Q$.  Exact `liftstd` source certificates reconstruct the constant
`1` in three charts and `2` in six charts, using between 7 and 19 literal
output-word rows.  Thus none is a coefficient-feasible simultaneous escape;
the response equations are not needed.

## Small joint remainders

Put

\[
\begin{aligned}
Q_A&=d_1d_6+d_1d_7+d_2d_5+d_3d_5,\\
Q_B&=d_1d_6+d_1d_8+d_2d_5+d_4d_5,\\
Q_C&=d_1d_6+d_2d_5.
\end{aligned}
\]

After removing the two new cell variables, the nine mixed derivatives are

| pair | joint factor |
|---|---|
| `02:10 + 14:02` | $d_{13}Q_A$ |
| `02:20 + 15:01` | $-d_{12}Q_B$ |
| `03:10 + 12:02` | $-d_{14}Q_C$ |
| `03:10 + 14:02` | $d_{11}Q_A$ |
| `03:20 + 15:01` | $-d_{10}Q_B$ |
| `04:10 + 12:02` | $-d_{13}Q_C$ |
| `04:20 + 15:01` | $-d_9Q_B$ |
| `05:10 + 12:02` | $-d_{12}Q_C$ |
| `05:10 + 14:02` | $d_9Q_A$ |

Three have two terms and six have four terms.  The exact checker
`computations/verify_n8_one_bad_segre_cube_critical_two_cell_units.py`
derives this census from all 2850 labelled pairs, verifies the displayed
factorizations, exports every nonzero coefficient of $q^{[3]}-X_0$ in each
critical chart, and checks each source lift.

## Scope

This closes the nine nonzero second variations of the **primary** six-row
functional.  It does not claim that all 2841 other two-cell charts have been
closed by the one-cell certificate cover: when one direction required an
alternative or Singular one-cell unit, that unit can itself acquire a cross
variation under a second direction.  A complete two-cell theorem would need
the transition/cross-variation audit for that finite certificate cover.

The bounded result here nevertheless removes every new pair singled out by
the primary second derivative, with exact top-only units and no response or
support-depth search.

