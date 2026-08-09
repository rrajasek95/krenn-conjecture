# The frozen sharp `r=4` selected-20 chart is coefficient-complete empty

## Outcome

Take the minimum-reciprocity-four packet frozen in
[`n8-r4-matching-incidence-frontier.md`](n8-r4-matching-incidence-frontier.md)
and impose the all-flat consequence proved there: no unselected physical
block can be nonzero.  The remaining source support consists of the twenty
selected witness blocks.

This labelled chart is empty before any nonlinear elimination.  Even after
relaxing every endpoint factor not fixed by an incoming witness arc to an
arbitrary ternary vector, there is no pure-colour perfect matching for
colour zero or colour one.  Therefore the literal pure-zero GHZ equation is

\[
                  [H_8(A)]_{00000000}-1=0-1=-1.             \tag{1}
\]

Thus the coefficient ideal is the unit ideal already over the integer
polynomial ring in arbitrary edge weights and arbitrary free endpoint
entries.  Nonzero localization, signed Laurent reduction, modular search,
and saturation are unnecessary.  This is a source-faithful structural
certificate, not a numerical specialization.

## Why the relaxation is valid

For every chosen arc `u->v` of colour `c`, the rank-one witness theorem fixes
the endpoint factor at its head `v` to the target axis `e_c`.  At the other
endpoint the checker allows all three colours, whether that factor is an
essential line or a common nonessential line.  This strictly enlarges the
actual source chart: it forgets common-line equalities and any additional
coordinate zeros.

The checker enumerates every perfect matching of the selected twenty-edge
physical support and every endpoint-colour word compatible with these
maximal endpoint supports.  The pure-row census in this enlarged chart is

\[
       \#\mathcal M_{0^8}=0,\qquad
       \#\mathcal M_{1^8}=0,\qquad
       \#\mathcal M_{2^8}>0.                                \tag{2}
\]

Since arbitrary scalar weights and arbitrary free endpoint entries can only
change coefficients of existing matching monomials, neither can create a
term in the first two empty rows.  Equation (1) is therefore invariant under
all allowed coefficient choices and in every characteristic.

For comparison, the concrete `(1,1,1)` line realization from the frontier
checker is enumerated separately and its word rows are verified to be a
subsystem of the maximal relaxation.

## Scope and next finite coverage step

This closes the exact labelled selected-20 orbit frozen in `b369357`.  It
does **not** classify every `r=4` reciprocal matching, every assignment of
the 24 head colours, or the other possible selected-good graphs.  The
uniform equality argument still reduces any all-flat `4K2` good-graph chart
to its selected twenty blocks; what remains is a finite orbit classification
of those support/head-label packets.  Each orbit can first be tested by the
same three pure-row matching census.  Only an orbit supporting all three
pure rows needs a signed Laurent or higher coefficient calculation.

## Reproduction

```sh
python3 computations/verify_n8_r4_selected20_full_source_empty.py
python3 -O computations/verify_n8_r4_selected20_full_source_empty.py
```

The checker pins both files of the frontier certificate, enumerates the
complete sparse output system on all `3^8` words, verifies the maximal and
realized row histograms, and freezes the literal integer unit (1).
