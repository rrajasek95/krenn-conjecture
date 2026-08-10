# The smallest active curved OO full-nine packet has a two-row source unit

## Outcome

The smallest source-faithful completion of the alternating-`C8` curved
doubly-good OO chart is coefficient-empty by an ordinary polynomial identity.
No Ward, jet, Hasse, cap-codomain, Gröbner, or finite-field argument is needed.

The two-anchor packet has eleven nonzero cells.  Its only old `11` cells are
`04:11` and `24:11`, which meet at site 4.  Consequently any pure-1 perfect
matching needs at least three new cells.  The exact pure-matching census is

```text
30 matchings need 3 new 11-cells,
75 matchings need 4 new 11-cells.
```

Among the thirty minimum completions, nineteen make both selected arm
cofactors nonzero.  Every one of those nineteen has a two-row ordinary source
certificate.  Hence there is no rational or complex full-row packet on the
minimum active completion stratum.

## Canonical certificate

Take

\[
 x=A_{03}(1,1),\qquad y=A_{15}(1,1),\qquad z=A_{67}(1,1).
\]

The pure target word `11111111` has the unique matching

```text
03 | 15 | 24 | 67
```

and therefore supplies the diagonal source row

\[
                         g_{\rm diag}=xyz-1.              \tag{1}
\]

The mixed word `11001111` has the unique matching

```text
04 | 15 | 23 | 67
```

and supplies

\[
                         g_{\rm mix}=yz.                  \tag{2}
\]

Relative to the two OO charts, (2) has endpoint labels

```text
pq=(0,2): 10, off-diagonal,
pr=(0,4): 11, diagonal.
```

Thus the desired diagonal/off-diagonal coupling is literally present in one
physical full-nine coefficient.  Equations (1)--(2) give the ordinary
Nullstellensatz certificate

\[
                   \boxed{xg_{\rm mix}-g_{\rm diag}=1}.   \tag{3}
\]

This is stronger than a torus monomial argument: after the eleven old packet
cells are normalized, (3) is an identity in `Q[x,y,z]`.  No division is used.
Neither source row is itself a scalar unit, so two rows are minimal for this
ordinary certificate.

## Structural audit

The three added cells do not weaken the OO hypotheses.  Direct-arm ranks stay
`(1,1)`, the four deleted-star ranks stay `(3,3,3,3)`, and the curvature is
still `-1`.  Both deleted-arm cofactors are explicitly active:

```text
pq cofactor classes: y, yz,
pr cofactor classes: y, yz.
```

The target-2 aligned rulings retain their nonzero sites `3` and `2`,
respectively.  Hence (3) closes the actual active curved doubly-good packet,
not the inactive two-anchor guard.

For each chart the checker also reconstructs all nine endpoint-colour labels
and all `3^6=729` residual words per label, i.e. all `3^8=6561` full-nine
rows.  Only nine residual polynomials are nonzero on the canonical sparse
support; all other rows are verified as literal zero equations.  Both the
diagonal and off-diagonal label sectors are therefore present before the
two-row certificate is selected.

The same construction is checked on all nineteen minimum active completions.
In each case a mixed monomial row divides the pure-anchor monomial, so
multiplying by the complementary one- or two-variable monomial and subtracting
the pure row gives 1.  Eighteen certificates use a degree-two mixed monomial
and a degree-one multiplier; the sole remaining chart uses degrees one and
two, respectively.

## Relation to the Lambda/Hasse no-go

The all-order Lambda theorem rules out manufacturing the missing class by
adding more Ward/Hasse/jet/cap objects inside the committed physical codomain.
Equation (3) does not attempt that.  It uses a genuinely additional literal
physical generator: the mixed full-nine row `11001111`, together with its
diagonal anchor.  This is exactly the kind of new source row permitted by the
no-go's scope.

## Scope

This closes the **minimum three-cell active completion stratum** of the frozen
alternating-`C8` OO chart.  It does not classify larger completions or prove
that an arbitrary active curved doubly-good overlap reduces to this support.
The remaining theorem-level gate is therefore a reduction/transport lemma to
a packet carrying a comparable diagonal/off-diagonal private factor—not a
new Ward or higher-jet construction.

## Verification

Run

```bash
uv run python computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py
uv run python -O computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py
```

The frozen ledger digest is

```text
1d03eb2c35c4a7194ebd5c95383b454d024bc7b7bdcc3830722a2f3ac3b70fe5
```
