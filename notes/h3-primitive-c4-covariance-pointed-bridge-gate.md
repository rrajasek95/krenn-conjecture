# Full-site covariance gives all four C4 mates, but only as a relative endpoint-choice bar

## Outcome

The direct primitive-`C4`/covariance idea has a genuine positive core.  On
the four direction sites `P,S,0,1`, write

```text
A = PS|01 = Hasse[2](D,Q01),
B = P0|S1 = Hasse[2](P0,S1),
C = P1|S0 = Hasse[2](P1,S0).
```

The physical site transpositions

```text
sigma_B=(P 1),       sigma_C=(P 0)
```

send `A` to `B` and `C`, respectively.  Both fix the response word
`11110000` because the exchanged sites all have colour `1`, and both fix the
literal tail `2345`.  Root-order and endpoint-chart transpose therefore send
one formal seed

```text
A_[a|b] -> B
```

to all four edges of the required `K2,2`.  Their incidence rank is three,
their alternating charge is `(1,1,-1,-1)`, and their three-chart projection
has the two row types `A+B` and `A+C`.

This is exactly the missing coefficient geometry.  In the canonical
48-coordinate fixed-window packet,

```text
old physical span               rank 46,
+ one projected switch          rank 47,
+ both switch families          rank 48.
```

The bridge nevertheless does **not** descend to a physical absolute switch.
The first obstruction is pointed endpoint-choice descent, before either
root word section or the mixed `K_Eq` square.

Exact checker:
[`verify_h3_primitive_c4_covariance_pointed_bridge_gate.py`](../computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py).

## 1. The covariance bar and its two folds

Site covariance gives an honest two-object action-groupoid bar.  For
`sigma_B`, its degree-zero module has two copies of `(A,B,C)` and its three
bar boundaries have rank three:

```text
C0 dimension  6,
bar rank       3,
H0 dimension  3.
```

There are two inequivalent ways to return this bar to the fixed endpoint
object.

1. **Canonical transport.**  Transport the second object back with
   `sigma_B^{-1}`.  Its `B` label becomes `A` again, so every bar boundary
   maps to zero.  This is a valid descent functor, but it supplies no
   `A -> B` operation-changing face.
2. **Raw fold.**  Forget the object tag without transporting the occurrence
   label.  The selected bar then has boundary `B-A`.  This is the desired
   coefficient row, but it is not a chain map to the original pointed
   source: it lowers `H0`.

The failure is visible on the smallest mixed-target quotient.  Set

```text
(A,B,C)=(1,-1,0).
```

Then the complete response has value `A+B+C=0`, while `B-A=-2`.  Hence the
mixed target equation does not make the raw fold pointed.

The unique monic presentation-safe repair retains new carrier coordinates:

\[
 d\Gamma_B=t_B-(B-A),\qquad
 d\Gamma_C=t_C-(C-A).
\]

With the complete response row, this extended five-coordinate presentation
has rank three and `H0` dimension two, exactly the old chart quotient.
Setting `t_B=t_C=0` raises the rank to five and kills that `H0`.  Thus the
relative graph organizes the two missing switches; it does not construct
them as absolute boundaries.

## 2. Why the full-site coinvariant theorem does not contradict this

The full `S8` direction-tag theorem proves that the centered coefficient tag
module has zero coinvariants after one endpoint--residual swap.  That theorem
is conditional on a termwise, source-valid PP comparison natural in the
choice of response endpoints.  The calculation above identifies precisely
the missing clause: coefficient covariance acts between endpoint-choice
objects, while a fixed-source pointed fold must either transport the label
back (zero boundary) or retain the normal `t`.

Equivalently, Maschke contraction proves uniqueness of a descent *after the
comparison functor exists*; it does not supply the augmentation of the
action-groupoid bar into one fixed physical fibre.

## 3. Downstream word and `K_Eq` interfaces remain independent

Even granting the two raw operation switches, site covariance stays in the
response word.  The root-labelled response-to-cap word quotient remains

```text
old relative cross-word rank       0,
+ paired diagonal section          1,
+ both root-labelled sections      2.
```

After both word sections are granted, the two-root augmented quotient is

```text
D4 return + objectwise clean Eq     rank 4,
+ paired mixed K_Eq incidence       rank 5,
+ paired shifted ridge              rank 6.
```

The normalized mixed and ridge detectors each read one.  Multiplying an
honest relative covariance bar by the central `K_Eq` cone is a strict square
and has `d^2=0`, but it preserves the endpoint-choice/bar, fine, repeated and
operation idempotents.  Its literal projection to the required
response-to-`AugP2` `Gamma_*` cell is zero/off-grade.  Thus neither the two
word sections nor the mixed `K_Eq` incidence is hidden in the covariance
bridge.

## 4. Exact label and readout scope

The positive covariance calculation retains:

- response word `11110000`;
- fixed tail/window `2345` and all three of its matchings;
- the literal direction-pair change
  `Hasse[2](D,Q01) -> Hasse[2](P0,S1)` or
  `Hasse[2](P1,S0)`; and
- mixed-target safety of the honest two-object bar.

The first failure is the fixed-source endpoint-choice/operation idempotent.
There is therefore no physical column yet on which to infer values of
physical `q`, anchor, `W`, ordinary or labelled residue, shifted ridge,
eta, or sigma.  Assigning those values would skip the obstruction rather
than solve it.

## Sharp positive datum

The shortest new theorem is a pointed endpoint-choice descent/augmentation
functor whose fixed-source fold sends the honest covariance bars to `B-A`
and `C-A` while preserving `H0`—equivalently, a physical landing for the
retained carriers `t_B,t_C`.  Once one seed landing is natural under root
and endpoint transpose, all four `K2,2` mates and the coefficient
`46 -> 48` completion follow automatically.  The two root word sections,
mixed `K_Eq` square, and ridge then remain the next typed faces of that same
schema.

This is an exact `h=3` obstruction, not a terminal theorem and not a
nonexistence claim for an unwritten higher operation.

## Verification

```text
python3 computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode all
python3 computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode chart
python3 computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode groupoid
python3 computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode downstream
python3 -O computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode all
python3 -I -S computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py --mode all
```

Frozen ledger SHA-256:

```text
3fca6419d4bced6bb90220af649da2bb63ea079e210f34b2dfe18cb4d98ad822
```
