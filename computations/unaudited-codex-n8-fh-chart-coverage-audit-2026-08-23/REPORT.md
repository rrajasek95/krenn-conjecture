# Global coverage audit for normalized pure-product calculations

## Exact conclusion

For the **pure-matching localization strategy**, the current smallest
authoritative checklist has all 31 `S8 x S3` orbit representatives.  There
is no proved descent between distinct chart orbits.  A certificate on chart
26 transports only to its own labelled orbit, not to the other 30.

This is not a claim that every proof must use 31 charts.  The independently
certified nonzero-cross-cell theorem gives a different single 251-variable
affine cover of the literal exact fibre.  But a proof organized by selected
pure matching monomials must close the 31 representatives or prove a new
descent that replaces some of them.

## Cover theorem

Put

```text
I = ideal of the 6,558 mixed X5 amplitudes,
F = H0*H1*H2,
P(M0,M1,M2) = p(0,M0)*p(1,M1)*p(2,M2).
```

At an exact X5 point the three pure amplitudes equal one.  Since each `Hc`
is a sum of 105 perfect-matching monomials, for each colour one summand is
nonzero.  Hence one of the `105^3` products `P` is nonzero.  Their exact
`S8 x S3` census has 31 orbits, pinned by ledger digest

```text
8b6dc91610d0e4a8663d067211c1cdf7be2c3615027b49c81e144e99a400c0a9.
```

The orbit sizes sum to `105^3 = 1,157,625`, so the list is exhaustive.
Consequently, for one representative `Pj` of every orbit, any of the
following equivalent chart certificates suffices:

1. in the original ring,
   `Pj^Nj * F^rj in I` for some `Nj >= 0`, `rj >= 1`;
2. after localizing at `Pj` and setting all twelve selected support cells to
   one by the full port torus,
   `Fbar_j^rj in Ibar_j`;
3. after degree-four homogenization with `t`,
   `t^kj * (Fh_j)^rj in Ih_j` for some `kj >= 0`;
4. equivalently, the affine Rabinowitsch unit certificate
   `1 in (Ibar_j, z*Fbar_j - 1)`.

The exponents may differ among charts.  Because the cover is finite, no
uniform exponent is needed for the pointwise contradiction, although maxima
can be taken afterward if a uniform global identity is desired.

## Smallest exact checklist

The representatives are chart IDs `1,...,31` from
`verify_n8_target_triple_localization_orbits.py`.  For each ID the required
record is:

```text
(chart ID, representative Pj, exact source multipliers,
 support-clearing exponent Nj, target exponent rj,
 homogenizing exponent kj, characteristic-zero replay digest).
```

Current completion count is **0/31**.  The useful structural partition does
not reduce the checklist:

| charts | exact structure | coverage status |
|---|---|---|
| 1--24, 27--31 | at least three mixed support factors | open; no proved descent |
| 25 | two mixed factors, both `(4,4)` with Hamilton-cycle complement | restricted/carrier identities only; full chart open |
| 26 | two mixed factors, both `(4,2,2)` with `(5,3)` complement | exact normalization and filtered computations; full chart open |

Chart 26 is the unique orbit with no even complementary two-factor.  The
proposed signed exchange contraction from the other 30 charts to a smaller
critical set is not proved; the exact Bockstein audit instead found seven
global syzygies.  It therefore cannot currently remove entries from the
31-item checklist.

## Localizers and the two normalization interfaces

There are two sound but different interfaces.

### Radical/pure-product interface

For proving the stronger statement `F in sqrt(I)`, the full port torus may
set all twelve factors of `Pj` to one.  This leaves 240 off-support variables.
It preserves mixed zero equations and pure **nonvanishing**, although it need
not preserve the literal values `H0=H1=H2=1`.  That is harmless: excluding
the larger locus `I=0, F!=0` already excludes the exact fibre.

Here `Pj` is the only geometric chart localizer.  In the normalized ring it
disappears; lifting a certificate back merely requires a power of `Pj` to
clear Laurent denominators.  The variable `t` is a homogenization device,
not a geometric chart coordinate.  Saturation by `t` is exactly what recovers
inhomogeneous affine membership.

### Literal target-preserving fibre interface

If the equations `H0=H1=H2=1` must be retained during normalization, the
target stabilizer has only enough freedom to set nine selected cells to one.
Three invariant anchors `u0,u1,u2` remain.  The authoritative chart has 243
source variables and must localize at

```text
Uj = u0*u1*u2
```

using an inverse equation or saturation.  A literal-fibre closure is

```text
1 in (mixed rows, H0-1, H1-1, H2-1, v*Uj-1).
```

The old files imposing all twelve support cells **and** all three pure values
equal to one are special subcharts and are not exhaustive.

## What degree-12 chart-26 membership would mean

An exact source-faithful certificate

```text
Fh_26 in Ih_26
```

at homogeneous degree 12 would be enough to close chart 26 with
`r26=1,k26=0`; setting `t=1` gives affine membership and Laurent lifting
clears a power of `P26`.  It would not close any other orbit.

Conversely, degree-12 **nonmembership** has no chart-level consequence:
`t^k Fh_26` may enter the homogeneous ideal for `k>0`, and radical closure
may require `(Fh_26)^r` with `r>1`.  The current fixed `C10` slice is not
congruent to `Fh`; its missing y11/y12 tail cancels the displayed dual.
Thus neither `C10` membership/nonmembership nor a fixed-degree monomial
standardness result fills any checklist entry.

## Mandatory counterguards

- Do not target `Pj in sqrt(I)`: an exact rational mixed-zero point has every
  selected anchor nonzero and all three pure hafnians zero on every chart.
  A pure-target factor is essential.
- Do not target `1 in Ibar_j`: mixed-zero points with `Fbar_j=0` exist.
- Do not replace `t^k(Fh)^r` by a raw constant class `t^k`; that asks the
  strictly stronger and generally false unit-ideal question.
- Do not infer affine membership from fixed-degree nonmembership; `t`-torsion
  is precisely the missing saturation.
- Do not count associated-graded, restricted-coordinate, support-SAT, or
  modular-only identities as one of the 31 characteristic-zero certificates.
- Do not transport chart 26 to another chart without an explicit
  `S8 x S3` equivalence or a separately proved source-labelled descent.

## Proof-spine consequence

The clean global target is the finite disjunction

```text
for every j=1..31, find rj,kj with
t^kj*(Fh_j)^rj in Ih_j.
```

Equivalently, produce 31 affine Rabinowitsch unit certificates.  The current
chart-26 degree-12 work is a valid local laboratory but has not yet completed
even its own entry, and completion of that one entry would leave 30 chart
orbits unless a new descent theorem is supplied.
