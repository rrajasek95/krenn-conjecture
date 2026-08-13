# The coloop pivot supplies the common tail, but darkness does not imply axis-purity

## Exact result

The proposed direct normalization has a genuine positive part.  Let `e` be
a pure-colour coloop edge and write `alpha=A_e[c,c]`.  From

\[
                         \alpha C_c=1                 \tag{1}
\]

and the complete pure/mixed rows in any other channel `i`, one has

\[
 d_iC_i+U_i=1,\qquad \alpha C_i+V_i=0,
\]

hence

\[
                 \boxed{\alpha U_i-d_iV_i=\alpha}.   \tag{2}
\]

Choosing a nonzero literal term from `U_i` or `V_i` is physically valid.
The exact matching census confirms that it carries all of the requested
normalization data:

- the same physical matching skeleton and residual `q` tail;
- the same `P/S` partners, endpoint heads, and orientation;
- the exact pure or two-site-mixed fine output word; and
- every remote decoration and selected mutual anchor.

Among 105 eight-site matchings, 90 omit the coloop and 78 also have two
distinct endpoint ports.  They realize all 15 unordered holes and all 30
orientations.  The same pivot works for all six closed Hall types.  Thus
common-`q`/endpoint/fine provenance is no longer the obstruction.

Checker:
[verify_h3_active_fan_coloop_direct_normalization_axis_pure_no_shortcut.py](../computations/verify_h3_active_fan_coloop_direct_normalization_axis_pure_no_shortcut.py).

## The remaining row is the complete endpoint-odd packet

Equation (2) is the physical signless row.  In coordinates

```text
(U+,U-,V+,V-,target,private protected residue)
```

take the exact guard

```text
S          = ( 2, 2,-3,-3,-2,0),
D_near     = ( 2,-2,-3, 3, 0,1),
D_required = ( 2,-2,-3, 3, 0,0).
```

The target-safe odd Cartan/private-site near-hit may retain the last private
row.  The first two columns have rank two; adjoining `D_required` raises it
to three.  The primitive covector

```text
(1/2,0,0,0,1/2,-1)
```

kills `S,D_near` and reads one on `D_required`.  All common-tail, head,
orientation, and fine labels survive this counterguard.  Therefore those
labels do not determine the protected odd packet.

If the private row is removed, the ordinary split works:

\[
 {S+D\over2}=\alpha U_+-dV_+-\alpha/2,
 \qquad
 {S-D\over2}=\alpha U_--dV_--\alpha/2.               \tag{3}
\]

After a physical `Phi` exists, `7a3ad78` identifies the private obstruction
with `[q-q0 Phi]`: a nonzero class gives the typed exit/generator, and a zero
class gives (3) after protected-row correction.  Before `Phi`, that quotient
class is not defined, so the local fan identity cannot invoke the dichotomy.

## Why axis-pure emptiness does not force the comparison

The active-fan theorem is proved on the principal open where a named
offdiagonal reference cell

\[
                         e=A_{vu}^{ba}\ne0            \tag{4}
\]

is nonzero.  Equivalently, adjoin `s=e^{-1}` with relation `es-1=0`.  The
axis-pure ideal contains `e`.  In the active localization,

\[
                         1=es-(es-1),                 \tag{5}
\]

so the axis-pure locus is empty inside this chart for the elementary reason
`D(e) cap V(e)=empty`.

This is not the global emptiness theorem `22c2e5c`; it is the variance
boundary between the two branches.  A comparison defect is a protected-row
class at a point of `D(e)`.  It supplies no deformation of the source
coordinate `e`.  An exact direct-sum guard extends the packet by `e`: the
packet separator has coefficient zero on `e`, while the axis-purity
functional reads one on the normalized active point.  Hence packet darkness
does not delete even the selected offdiagonal cell, much less all of them.

To use global axis-pure emptiness positively, one would first need a new
theorem:

> A nonfillable private packet defect produces a source-flat,
> anchor-preserving family whose special fibre has every offdiagonal cell
> zero.

Such a family necessarily leaves the localization (4).  Neither Maschke
duality, protected-row nonmembership, nor the private-site identity supplies
it.  Therefore the implication

```text
dark/missing fan-grade Phi -> axis-pure exact source
```

is not currently valid.

## Shortest frontier

The arbitrary-coloop common-tail normalization is constructed by (2).  The
remaining direct theorem is only the fan-grade protected odd `Phi/q`
comparison.  An alternative proof could replace it by the source-flat
axis-boundary degeneration above, but that is a new theorem of comparable or
greater strength.  The centered cross-word attachment is a possible source
of `Phi`; it is not needed for the already-complete matching provenance.

This is exact for the canonical `h=3` active-fan localization.  The protected
row guard is not asserted to be a new full GHZ source counterexample.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
