# Physical Cartan descent closes the residual-q endpoint holonomy

## Result

The residual-q Kodaira--Spencer lift used conditionally in the older
five-lock/E14 landing theorem is now constructed by the physical
endpoint-odd Cartan prism.

Both objects live in the canonical labelled repeated `P3+K2` grade and word
`1211222` after deleting the distinguished endpoint.  Their complete
augmented signatures agree:

```text
ordinary residue             = (-1,+1,+1,-1) = -delta,
D,W,target,anchor,pure-Eq     = 0,
terminal ridge               = commuting -dOmega_v eta/sigma packet.
```

The older curvature-minus-bar near-hit has residue `+delta`.  Adding the
physical Cartan cell cancels that residue and gives

\[
 A=E_+-E_-+\Omega-q_{\rm comp}.                         \tag{1}
\]

The already physical bar is `B=-Omega+q_comp`, so

\[
                         A+B=E_+-E_-=:D.                \tag{2}
\]

Equation (2) kills the one-dimensional unequal-tail endpoint holonomy.  In
the exact all-five-row guard the row rank rises from six to seven.  Together
with the existing signless response `S=E_++E_-`, it also splits the two E14
endpoint orientations.

Checker:
[`verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py`](../computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py).

## Why this is now source-provenant

The Cartan prism is not an abstract four-corner relation.  The physical
descent theorem proves termwise on all complete matching rows that the local
colour root field on coefficient space is related to the output root field.
Cartan contraction therefore descends to the complete physical
principal-parts resolution.  Endpoint oddization uses the actual residual
site transposition and cancels the GHZ target defect functorially.

The order-six secondary transfer identifies the ordinary residue with
`-delta`; the ridge commutation theorem supplies the exact eta/sigma packet.
These are precisely the source type and terminal law demanded by the former
KS hypothesis.  No same-cell matching companion or formal chart-copy
difference is being reinterpreted as a physical column.

## The honest terminal alternative

The exhaustive six-term readout gives two branches.

1. If the physical terminal is nonzero on the protected correction kernel,
   normalize that kernel class.  This is already the required physical
   relative generator.
2. If the terminal kills the kernel, the Cartan cell is zero-indeterminate
   in the physical quotient.  Then (1)--(2) are source-valid and close the
   unequal-tail five-lock and E14 self-loop exactly as in the conditional
   landing theorem.

There is no third branch, even after arbitrary future relative extensions.
Thus “construct a residual-q KS lift” is removed from the proof frontier in
the canonical `h=3` packet.

## What remains

This composition resolves endpoint/tail provenance, not physical
transversality.  The endpoint difference `D` has zero target and anchor
readouts; it does not by itself create an avoiding pure matching or repair a
same-head deleted-star profile `(2,2,3,3)`.

On the active interference side, the remaining tasks are now:

1. prove that an arbitrary critical curved component enters the marked
   Cartan/fan component (source exhaustivity);
2. land the resulting carrier on a transverse physical head or obtain a
   support-reducing complete-column dependence; and
3. close the diagonal `2+2` four-site switch isolated by the equal-partition
   zero-holonomy reduction.

The first and third may be two views of the same statement: the unused K4
matching of the diagonal switch is exactly an off-diagonal conjugate route,
and physical Cartan transport supplies the endpoint-word change once that
route is present in the marked source component.

## Scope and verification

This is a theorem in the canonical `h=3` labelled repeated grade.  It does
not prove that every higher-row SCC is binomial or that every arbitrary
curved overlap maps into this grade.  It does not construct an active clean
cap.  Those global entry and transverse-landing statements remain the
conjecture-level work.

Run

```text
python3 computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py
python3 -O computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py
python3 -I -S computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py
```

Frozen ledger SHA-256:

```text
e7ec95b3b3494c5b656c42dd002c3c49a05e1bc28104383b626adb3207aebd91
```
