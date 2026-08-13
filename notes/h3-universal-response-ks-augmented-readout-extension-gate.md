# The universal response KS seed does not yet carry physical terminal rows

## Exact result

Differentiating the universal response family constructs the centered
relative Kodaira--Spencer seed

\[
                       d\epsilon_s=-c_f.
\]

It also determines the scaled formal anchor conormal and the aggregate
matching action.  It does **not** canonically extend the physical rows
`ainc/q`, `W`, or the labelled shifted ridge to `epsilon_s`.  Consequently a
`q` defect on the formal generator cannot yet be promoted to the physical
relative generator or Fredholm alternative.  Word/fine/repeated-grade
landing in the complete AugP2/E14 domain remains prior.

Checker:

```text
computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py
```

Frozen ledger digest:

```text
0deb498dc7249280d35d825a205061c93da1dcf6d2bee3bd9644e845a7a6e1df
```

## Formal anchor: positive

In coordinates consisting of the marked occurrence `z_f`, the aggregate of
the other 89 occurrences, and the target anchor `u`, put

\[
 B=(1,1,-1),\qquad c_f=(89,-1,0).
\]

Then exactly

\[
                  c_f+B=(90,0,-1)=90,dz_f-du.       \tag{1}
\]

Thus the response family plus the old aggregate response/target conormal
does canonically supply the scaled anchor law.  This agrees with the pinned
all-occurrence identity and is enough for anchor visibility over the
characteristic-zero theorem field.  It remains a conormal identity: it does
not place the source class in the E14 word/fine/repeated grade.

## Physical `q`: aggregate matching is not enough

Endpoint/matching naturality fixes the aggregate matching part `M` of

\[
                         q=M-\operatorname{ainc}.     \tag{2}
\]

But differentiation of the response equation supplies no `ainc` row on the
new generator.  Holding `M(epsilon_s)=1` fixed, the two choices
`ainc(epsilon_s)=0,1` give `q(epsilon_s)=1,0`.  They have the same response
differential and the same coefficient naturality.  Therefore response
naturality alone does not define physical `q`.

This is an instance of a five-dimensional augmented ambiguity.  Fixing the
principal column `d epsilon_s=-c_f` leaves independent possible values in

```text
ainc/q, W, labelled ridge, eta, sigma.
```

The formal response presentation does not select among them.

## The toric shear obstruction is not yet a `q` packet

The constant occurrence shear has the exact differential value

\[
 (p_1s_0-p_0s_1)(q_{23}q_{45}-q_{24}q_{35}).        \tag{3}
\]

In the four-corner order

```text
p1s0*q23q45, p1s0*q24q35, p0s1*q23q45, p0s1*q24q35
```

its coefficient vector is

\[
                           \xi=(1,-1,-1,1).           \tag{4}
\]

Rows which depend only on endpoint orientation or only on residual matching
span a rank-three subspace of `Q^4`.  The line `Q xi` is exactly its
annihilator.  In particular,

```text
aggregate matching shadow on xi = 0,
anchor-incidence shadow on xi    = 0,
q=M-ainc shadow on xi            = 0.
```

Thus (3) is a genuinely mixed endpoint-by-matching conormal.  It is not
already one of the physical fan-coloop `q` rows.  Such a fan row is a
terminal on a complete relative source domain in its literal repeated
grade; (3) is presently a degree-zero response conormal.  Identifying them
would require precisely the missing occurrence-local, word/fine/repeated
physical comparison.  The shear obstruction therefore sharpens the landing
gate but does not trigger the `q` generator alternative by itself.

## Why the `q` dichotomy cannot be invoked early

The physical defect theorem requires a protected comparison between two
complete physical relative domains, with physical `q` on both sides.  The
small exact guard is:

```text
L_phys = <e0>,       J_phys(e0)=1;
L_formal = L_phys + <epsilon_s>,
J(epsilon_s)=0,      q(epsilon_s)=1.
```

The formal extension has a nonzero `q` defect witnessed by `epsilon_s`, but
the physical map is an isomorphism.  Hence its physical kernel and left
cokernel are both zero.  The witness is not physical, so neither a relative
generator nor a Fredholm separator follows.

Once an augmented physical placement of `epsilon_s` is constructed, this
guard disappears and the existing defect theorem applies exactly: zero
defect transports `q`; nonzero defect produces a physical relative generator
on one endpoint.

## `W` and eta/sigma

`W` remains the independent occurrence-to-E14 landing equation already
isolated as `w_E14=t`.  A coefficientwise response deformation neither
constructs nor removes that rank-one word-changing condition.

The response parameter admits a formal trivial eta/sigma extension.  That is
not the required terminal packet.  The required values are contractions of
the separately labelled shifted Kähler class

\[
                          \gamma=-d\Omega.
\]

Naturality proves that, once a physical labelled copy of `gamma` exists, its
eta/sigma values transport uniquely and add no mixed curvature.  Naturality
does not construct that labelled copy.

## Exact remaining interface

The source KS object is the centered occurrence in response word
`11:110000`.  The physical comparison must reach both the E14 unary word
`000101` and the cap object

```text
01211222 / t*q_(v,N) / repeated P3+K2.
```

These are distinct graded summands.  No equality of coefficient shadows or
response naturality creates the off-diagonal map.

The shortest remaining theorem is therefore:

> Construct one protected, endpoint/D4-equivariant augmented placement of
> `epsilon_s` in the complete physical AugP2/E14 domain.  Then (1) handles
> anchor visibility, matching naturality supplies the aggregate part of
> `q`, the physical defect alternative finishes `q`, the independent `W`
> equation is checked on the same cell, and the labelled ridge uniquely
> supplies eta/sigma.

This is a sharp typing counterguard, not a no-go theorem for such a physical
placement.  Scope is canonical `h=3` over a characteristic-zero field.
