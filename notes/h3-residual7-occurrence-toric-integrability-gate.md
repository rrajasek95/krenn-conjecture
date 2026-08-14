# The residual seven is normal to the physical occurrence torus

## Outcome

The diagonal seven-dimensional ambiguity left by the two root-labelled
response jets does **not** consist of physical first-order occurrence
redistributions on the active scalar-factor torus.  It stops before the
minimum-support and second-Hasse alternatives apply.

In the two literal complete rows `11111111` and `11211211`, write `I` for the
`180 x 40` incidence matrix from decorated source cells to matching
occurrences.  A support-preserving logarithmic variation of the physical
cell scalars has occurrence tangent

\[
             \delta(m)=\sum_{e\in m}z_e,
             \qquad \delta=Iz.                    \tag{1}
\]

Each of the seven residual vectors `r_j` obeys the already committed
single-cell equations

\[
                         I^T r_j=0.                \tag{2}
\]

The exact incidence rank is `32`; adjoining the residual seven raises it to
`39`.  Since the rational coordinate pairing is positive definite,

\[
              \operatorname{im}I\cap\ker I^T=0.   \tag{3}
\]

Thus no nonzero `r_j` solves the physical first-order lifting equation
`Iz=r_j`.

Exact checker:
[`verify_h3_residual7_occurrence_toric_integrability_gate.py`](../computations/verify_h3_residual7_occurrence_toric_integrability_gate.py).

## Exact residual reconstruction

The checker reconstructs the canonical two-word carrier over the rationals,
rather than importing the residual dimension as metadata:

```text
matching occurrences                              180
pair-shadow rank / kernel                     159 / 21
committed readout rank / residual               14 / 7
decorated source cells                               40
physical incidence rank                              32
rank after adjoining residual seven                  39
```

The seven basis supports, sorted, are

```text
12, 12, 36, 36, 48, 56, 60.
```

Every basis vector has integral coefficients, zero pair shadow, zero pure
and mixed row augmentation, zero four-corner value, zero incidence at each
of the forty decorated cells, and character `-1` under both endpoint swap
and the signed tail Weyl action.  These checks preserve the literal word,
matching/fine and source-cell labels.

## Why free occurrence integration is not physical

If the `180` occurrence coefficients are declared independent, then

\[
                         c_m(t)=1+t(r_j)_m         \tag{4}
\]

is a linear deformation preserving all of the linear shadows used above,
and one may scale `t` to kill a chosen nonzero occurrence coefficient.
But (4) is not induced by the factorized physical cell scalars: equation
(3) proves that it leaves the physical coefficient torus immediately.  In
the presentation-safe source this changes the scalar factorization and its
`H0` carrier.  Minimum occupied scalar support therefore supplies no
support-lowering contradiction.

This is an earlier obstruction than the known second-Hasse class.  A Hasse
calculation becomes meaningful only after a genuine non-toric relative
source operation has been constructed whose first boundary is `r_j`.

## The local dual and its limit

For each residual the normalized coordinate covector

\[
              \psi_j=\frac{r_j}{\langle r_j,r_j\rangle}             \tag{5}
\]

annihilates every column of `I` and satisfies `psi_j(r_j)=1`.  Hence there
are seven exact source-labelled local covectors detecting the failed Euler
lift.  They are not yet accepted augmented terminals: promotion still
requires extending a covector through the exhaustive augmented source map
while retaining target, Eq, q, anchor, word, fine, repeated-edge and
operation readouts.

The result is confined to the active coefficient torus.  It does not rule
out a non-toric relative source cell with first boundary `r_j`, nor does it
analyze boundary strata on which decorated scalar factors vanish.

## Consequence for the main construction

Interpreting the residual seven as ordinary occurrence redistributions does
not bypass the missing response-to-cap map.  The shortest positive datum
remains either:

1. a physical non-toric source operation whose literal first boundary is a
   residual `r_j`, followed by its Hasse and terminal tests; or
2. the termwise-faithful root-covariant `A_Gamma` landing that reads the
   residual seven in `AugP2`.

## Verification

```text
python3 computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode all
python3 computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode basis
python3 computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode toric
python3 computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode terminal
python3 -O computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode all
python3 -I -S computations/verify_h3_residual7_occurrence_toric_integrability_gate.py --mode all
```

Frozen ledger SHA-256:

```text
315ebeeee3552294fb5cec1c744bdbf1eb3c144456149a4a2071487b2cd2e94c
```
