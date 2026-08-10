# The response anchors force departure from the pure-additive K4 chart

## Exact verdict

Let $H$ be the fourteen-cell Segre--K4 quadratic from `772290e`.  Every
cell of $H$ has a zero-colour endpoint.  This remains true after adding an
arbitrary pure-zero quadratic $d$, and even after adding arbitrary further
cells of colours

\[
                         00,01,02,10,20.                \tag{1}
\]

No quadratic supported in this larger 75-cell class can satisfy either
diagonal one-bad response row at $h=3$:

\[
 p_1s_1q^{[2]}=X_1,\qquad p_2s_2q^{[2]}=X_2.          \tag{2}
\]

Both target coefficients on the left of (2) are identically zero for
arbitrary endpoint-star linear forms and arbitrary source coefficients.
Thus the four response rows do **not** normalize an arbitrary Segre
completion into the pure-additive form $H+d$.  They force it to leave that
chart.

## Coefficientwise proof

Fix an ordered pair of distinct response holes $u,v$.  A literal source
monomial contributing to

\[
                         [p s q^{[2]}]_{111111}
\]

must use the colour-1 components of $p$ and $s$ at $u,v$.  The four
remaining sites are covered by two disjoint $q$-cells, and the output word
forces both to have decoration `11`.  There are three residual perfect
matchings, so over all thirty ordered hole pairs the coefficient has ninety
source-labelled monomials.  Every one contains two disjoint `11` cells.

The same argument for `222222` says that every monomial contains two
disjoint `22` cells.  Neither kind of cell occurs in (1), hence both
coefficients vanish.  This uses no genericity, support minimality, or choice
of star coefficients.

Consequently a genuine one-bad completion has the sharp necessary support
condition

```text
X1 response: at least two disjoint 11 cells of q;
X2 response: at least two disjoint 22 cells of q.
```

The first response row already failing on the pure-additive chart is
$p_1s_1q^{[2]}=X_1$; the second diagonal row fails identically as well.
The crossed-zero rows impose no repair of this absence.

## Consequence for the Segre route

The pure-unary certificate `76e5f56` for $H+d$ closes every all-zero repair
of the top row.  The present response calculation is complementary and stronger
as a normalization counterguard: even before the unary equation is used,
$H+d$ cannot carry the required responses.  Any remaining completion must
simultaneously introduce pure `11` and `22` matching carriers and then
re-solve the mixed top fibres.  Therefore the next bounded object is the
four-carrier deformation (two disjoint cells in each colour), not a proof
that response equations reduce arbitrary mixed support back to $H+d$.

The checker
`computations/verify_n8_one_bad_segre_cube_response_defect_obstruction.py`
retains all ordered hole, physical matching, and endpoint-colour labels.

## Scope

This is an exact $h=3$ coefficient theorem for the whole
one-zero-endpoint support class, not merely the pinned fourteen weights.  It
does not classify or exclude completions after `11` and `22` cells are
added, and hence does not prove one-bad emptiness or Krenn's conjecture.
