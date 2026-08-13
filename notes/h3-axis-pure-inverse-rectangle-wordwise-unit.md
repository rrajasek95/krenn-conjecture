# Full polarization kills every axis-pure inverse rectangle

## Result

The rational countermodel of `855b2c5` does not merely suggest an active
carrier.  Once the physical site-word grading is restored, it contradicts
literal mixed unary rows.  The same argument closes its whole parametric
inverse-rectangle family.

The underlying source theorem is broader:

> On six sites with an axis-diagonal quadratic, every `(2,2,2)` word has
> exactly one compatible perfect matching.  Therefore a cross-colour `2x2`
> minor complementary to a nonzero pure-colour edge must vanish at an exact
> source.  If the minor is nonzero, one of its two terms is a literal nonzero
> mixed full-word coefficient.

This is stronger than an untyped active-minor conclusion: it is an immediate
source contradiction.

Checker:

```text
computations/verify_h3_axis_pure_inverse_rectangle_wordwise_unit.py
```

Frozen ledger SHA-256:

```text
d29c557055e410f31432c306daf1de0b776b7bd07b28141be061d27eb1d8c099
```

## The complementary-minor identity

Use the notation of `855b2c5`.  The first response rectangle has

\[
 U=\begin{pmatrix}a&f\\h&c\end{pmatrix}.
\]

Its determinant terms become unary matching monomials after multiplication
by the occupied pure-zero edge `q23:0`:

```text
a*c*q23  on word 210012, matching 05:2 | 14:1 | 23:0,
f*h*q23  on word 210021, matching 04:2 | 15:1 | 23:0.
```

These are different physical words.  Each word has two sites of each colour,
so its compatible axis-diagonal matching is forced.  Its target is zero;
therefore each displayed product vanishes separately.  After localizing the
pure edge, `ac=fh=0` and hence `det(U)=0`.

The opposite rectangle is identical.  With

\[
 V=\begin{pmatrix}b&e\\g&d\end{pmatrix},
\]

and complementary edge `q01:0`, its terms occupy

```text
b*d*q01  on word 002121, matching 01:0 | 24:2 | 35:1,
e*g*q01  on word 002112, matching 01:0 | 25:2 | 34:1.
```

Thus every source-exact complementary cross-colour determinant vanishes.
This is a wordwise determinant-to-terminal theorem, not a commutative
cohafnian identity.

## The entire inverse-rectangle family is empty

The selected response normalization is exactly

\[
                         UV=I.                         \tag{1}
\]

Consequently

\[
 ac-fh=\det U\ne0,
 \qquad bd-eg=\det V=(\det U)^{-1}\ne0.               \tag{2}

At least one word in each of the two pairs above has a nonzero coefficient.
Hence every normalized inverse rectangle violates at least two literal mixed
unary rows.  The checker verifies the symbolic formulas and all `496`
invertible integer matrices `U` with entries in `[-2,2]`; the proof is (2),
not the finite audit.

For the rational instance in `855b2c5`, all four residues are visible:

```text
210012 :  1
210021 : -1
002121 :  1/4
002112 : -1/4
```

The apparent cancellations occurred only after identifying distinct site
words with the commutative monomial `x0*x1*x2`.

## Relation to four-good and coloop landings

The fastest landing is the literal mixed-row unit, so no active-fan rank
upgrade is required.  The private-site active-minor theorem is not directly
typed here: every quadratic cell is colour-diagonal, while that theorem
starts from an off-diagonal endpoint cell.

Support-theoretically, the displayed pure-zero family is the single matching
`01|23|45`, so its three edges are literal pure-zero coloops.  This places the
model on the coloop side as well, but coloop normalization is downstream of
the stronger wordwise contradiction.

The remaining general axis-pure incidence statement is now precise:

> From an arbitrary normalized response packet, force a nonzero cross-colour
> `2x2` minor complementary to an occupied pure-zero edge, or route failure
> of all such minors into the existing star/triangle/`K2,2` Hall and literal-
> coloop normal forms.

That is the generalization still needed; the inverse-rectangle stratum itself
is closed without a support enumeration.
