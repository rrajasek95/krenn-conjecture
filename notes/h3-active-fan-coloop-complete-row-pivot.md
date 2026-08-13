# One complete-row pivot types every saturated fan-coloop Hall shore

## Result

Let `e=uv` be one edge of a source-provenant active private-site fan, and
suppose `e` is a literal coloop of the pure-`c` target support.  Write

```text
alpha = A_e[c,c].
```

The pure-`c` target coefficient factors as

\[
                         \alpha C_c=1.                 \tag{1}
\]

In particular `alpha` is nonzero.  For any other pure target channel `i`,
compare its target word with the mixed word obtained by changing only the
two residual sites `u,v` from `i` to `c`.  Split both complete rows according
to whether their matching retains `e`:

\[
 d_iC_i+U_i=1,\qquad \alpha C_i+V_i=0,                \tag{2}
\]

where `d_i=A_e[i,i]`, `U_i` is the complete pure-`i` sum omitting `e`, and
`V_i` is the complete two-site-mixed sum omitting `e`.  The retained terms
have exactly the same complete cofactor `C_i`.  Eliminating it gives

\[
                 \boxed{\alpha U_i-d_iV_i=\alpha}.     \tag{3}
\]

Consequently `U_i` and `V_i` cannot both vanish.  A nonzero aggregate has a
nonzero literal term, so every other target channel supplies one of

```text
a pure target matching omitting the coloop edge, or
a fine-typed mixed exchange matching omitting the coloop edge.
```

This is the first complete-row lift missing from `32e07b5`.  It is uniform:
the same identity serves all six saturated `K6` tight-set types.  It does
not yet prove the final simultaneous affine/dependence alternative.

Checker:
[`verify_h3_active_fan_coloop_complete_row_pivot.py`](../computations/verify_h3_active_fan_coloop_complete_row_pivot.py).

## Why this is a physical common-`q` lift

Pair the terms of `U_i` and `V_i` by their physical perfect matching.  Since
the matching omits `e`, the sites `u,v` lie on two distinct matching edges.
The paired monomials differ only on those two cells.  They retain

* the same physical matching skeleton;
* the same `P` and `S` partners and their orientation;
* the same endpoint output heads `i,i`;
* every decorated cell away from `u,v`; and
* the exact pure or two-site-mixed fine output word.

Thus `V_i` is not an occurrence-module placeholder.  It is a literal term
of the same diagonal response tensor as the pure-`i` target, with the same
physical endpoint ports and common residual `q`.  No source coefficient is
changed, so every selected mutual anchor remains present at this step.
Using the new term later as a replacement anchor is a separate
anchor-preserving-switch question; (3) does not silently perform that
reselection.

At `h=3`, fix an internal coloop edge of the six residual sites.  Among the
`105` perfect matchings on the eight physical sites,

```text
15 retain the coloop edge,
90 omit it,
78 both omit it and have distinct endpoint ports.
```

Those `78` skeletons realize all fifteen unordered residual hole edges and
all thirty endpoint orientations.  Hence there is no incidence or
orientation type missing from the complete packet.  What (3) does not say
is which one of those terms is nonzero.

## Composition with the six closed Hall concepts

For a closed effective-hole shore `A`, let

\[
 T(A)=\{f:f\text{ meets every edge of }A\},\qquad
 \operatorname {cl}(A)=T(T(A)).                       \tag{4}
\]

The six closed concepts from `32e07b5` have shore sizes

```text
triangle / triangle                 3 / 3
matching / rectangle                2 / 4
path / path                         3 / 3
adjacent pair / six-edge shore      2 / 6
singleton / nine-edge shore         1 / 9
full star / full star               5 / 5.
```

Apply (3) in the relevant response channel and select one nonzero literal
omit-`e` term.  Its actual endpoint pair has an exact alternative.

1. If its hole is outside the current closed shore, adjoining it strictly
   enlarges `cl(A)`.  This is the already proved decreasing saturation
   potential.
2. If every term produced by the complete rows remains on the two closed
   shores, the pure/mixed word, endpoint orientation, response head, and
   common-`q` provenance above physically type that Hall concept.

No orbit-specific determinant or response identity is required.  The six
types enter only after the uniform source pivot, when the already committed
star/triangle/`K2,2` landing theorems inspect the trapped physical covector.
Reverse endpoint orientations are not formal holes: they are retained as
literal orientations, and the effective unordered-hole theorem removes an
orientation pair only when its complete common-cofactor aggregate cancels.

## What has and has not advanced

Equation (3) closes the gap between a hole-incidence shadow and a complete
source packet: a fan coloop necessarily produces a target or exchange
occurrence outside the coloop, with all word and endpoint data attached.
It also proves that common-`q` tail provenance and endpoint orientation can
be transported uniformly across the six closed types.

It does **not** prove any of the following stronger conclusions.

* `U_i!=0` is a selected pure target occurrence, not automatically a point
  of a one-site sequential affine fibre preserving all four responses.
* `V_i!=0` is a literal exchange occurrence, but (3) does not prescribe an
  exchange outside the saturated shore.
* If every carrier is trapped, (3) is not yet an anchor-safe dependence of
  complete endpoint columns.  The star/triangle/`K2,2` covector still needs
  that physical dependence or affine landing.
* The theorem retains the orientation of the selected nonzero term; it
  cannot prescribe in advance which of the two orientations is bright.

Thus the remaining active-fan tight-set theorem is smaller than the one in
`32e07b5`:

> **Trapped-carrier affine/dependence lift.**  For the physically typed
> pure/mixed omit-coloop carriers furnished by (3), either a complete
> endpoint column meets the sequential target fibre, a carrier leaves the
> saturated shore, or the trapped carrier relation lifts to an anchor-safe
> complete-column dependence (equivalently, the already typed Hall covector
> acts nontrivially on the protected circuit).

The source occurrence and its common-`q`, word, grade, endpoint, and Hall
shore typing no longer belong to that missing theorem.

## The proposed signless Cartan correction

There is a sharp compatibility check with the physical Cartan prism.  Let
`s` be the endpoint transposition disjoint from the two Weyl root sites.
The Weyl target defect is `s`-invariant, so

\[
 (1+s)(w-1)\Delta=2(w-1)\Delta,\qquad
 (1-s)(w-1)\Delta=0.                                  \tag{5}
\]

Within the natural two-dimensional operator span generated by `H_w` and
`sH_w`, target safety is exactly the odd line `a+b=0`.  Correcting the
signless prism by its own target defect therefore gives

\[
                 (1+s)H_w-2H_w=(s-1)H_w,              \tag{6}
\]

which is the endpoint-odd prism again.  Hence the signless boundary cannot
be retained by a target correction internal to the existing Weyl prism.
It needs an independent relative target/cone cell.  The odd prism may still
supply a typed external exchange, but it does not replace the trapped-
carrier affine/dependence lift above.

## Verification

Run

```text
python3 computations/verify_h3_active_fan_coloop_complete_row_pivot.py
python3 -O computations/verify_h3_active_fan_coloop_complete_row_pivot.py
python3 -I -S computations/verify_h3_active_fan_coloop_complete_row_pivot.py
```

Frozen ledger SHA-256:

```text
0dfc0d5b9ef6a0fcc4aaf21a25883edd4301f0495fe6cb90d7371cf6cf89f8a6
```
