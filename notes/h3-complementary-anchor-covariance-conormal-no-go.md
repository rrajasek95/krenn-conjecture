# Complementary pure-anchor covariance does not kill the attaching conormal

## Outcome

There are two natural ways to combine the two binary pure anchors in the
rootless `h=3` attaching problem.  Neither supplies the missing physical
chain.

1. On the six residual sites, opposite colour rotations cancel their
   three/three target coefficient because the two contributions have signs
   `+1,-1`.  But all twenty resulting literal rows are mixed eight-site
   words.  Their selected-`u` conormal is zero, so this is only another
   middle-word identity.
2. On the full eight sites, a selected binary word has four occurrences of
   each colour.  The two complementary pure anchors now contribute with
   signs `+1,+1`.  Therefore the linear combination which cancels the mixed
   target also cancels the normalized `w` boundary of their formal
   order-four Hasse/cap landings.

This remains true after arbitrary adjacent-chart or covariance comparisons:
those comparisons redistribute pure-anchor incidence but have total
incidence and `w` boundary zero.  Thus opposite-anchor covariance is already
covered by the conserved conormal augmentation; it cannot construct the
primitive attaching row.

This is a no-go for a tempting universal repair, not a no-go for a new
packet-conditioned source unit or genuinely new lower face.

## 1. Odd residual rotation

Use binary labels `c,e` and on six residual sites put

\[
             c\longmapsto c+t e,
       \qquad e\longmapsto e-t c .                    \tag{1}
\]

For every three-set `S`, the coefficient of the word
`e^S c^(S^c)` in the transforms of the two pure tensors is respectively

\[
                         1,\qquad (-1)^3=-1.           \tag{2}
\]

Hence the sum has zero target coefficient on each of the twenty middle
words.  With either diagonal endpoint pair adjoined, however, the complete
eight-site word is mixed.  The literal conormal census of
`h3-source-base-change-conormal-obstruction.md` says that only the selected
pure anchor contains the homogenizing variable `u` to first order.  Every
row in (2) therefore has conormal zero.

The odd cancellation is useful target bookkeeping, but it does not touch
the class `kappa[F_0]`.

## 2. Even full-anchor rotation

Rotate all eight sites by (1).  A balanced selected word has four `c` and
four `e` labels.  Its coefficients from the two pure anchors are

\[
                         1,\qquad (-1)^4=1.            \tag{3}
\]

Grant, more strongly than the committed physical module permits, the
complete formal order-four Hasse/cap candidate under each anchor.  In
coordinates

\[
                    ([F_c],[F_e],\widehat w)
\]

the two candidates and a complementary comparison have columns

\[
 N_c=(1,0,1),\qquad N_e=(0,1,1),\qquad E=(-1,1,0).     \tag{4}
\]

For coefficients `a,b`, equation (3) says that both the selected mixed
target and the normalized boundary equal `a+b`.  Thus target cancellation
forces `a+b=0`, and the `w` boundary vanishes at the same time.  Adding any
multiple of `E` cannot change this conclusion.

Equivalently, the primitive integral functional

\[
                       \lambda=(1,1,-1)                \tag{5}
\]

kills all three columns in (4) and evaluates to `-1` on the desired
invisible boundary `(0,0,1)`.  The available rank is two; adjoining the
desired boundary raises it to three.  This is the two-colour/two-anchor
version of the chart-incidence invariant in
`h3-signed-circuit-conormal-transport-no-go.md`.

## 3. Consequence for the proof search

Global colour covariance does not evade the source-provenance obstruction.
At odd residual order it never acquires anchor incidence; at the first
capable full order its target and boundary augmentations are locked.

Accordingly the next useful proof object cannot be another Ward identity,
opposite rotation, complementary Hasse cube, or ordinary chart difference.
It must be packet-conditioned: either an actual source unit/saturation, or a
new lower face with total anchor incidence `-1` and zero `w`, target, and
ordinary residue, before source base change.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_complementary_anchor_covariance_conormal_no_go.py
.venv/bin/python -O computations/verify_h3_complementary_anchor_covariance_conormal_no_go.py
```

The checker enumerates all `20` residual three/three words and all `70`
full eight-site four/four words, verifies the parity signs and literal
mixed-word conormal values, and checks the exact rank/separator statement in
(4)--(5).  It pins the two earlier conormal audits on which the source
interpretation depends.
