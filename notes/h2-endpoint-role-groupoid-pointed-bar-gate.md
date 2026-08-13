# The endpoint-role bar exists between objects but not inside the pointed physical fibre

## Outcome

Retaining the endpoint labels produces an honest two-object groupoid.  If
`+` denotes the original ordered endpoint object and `T` its `P<->S`,
response-head-transposed object, then the normalized groupoid bar has

\[
                 d b_i=(T,\tau i)-(+,i).              \tag{1}
\]

This does **not** construct the desired physical occurrence boundary.  The
canonical transport from `T` back to `+` applies `tau^{-1}` to the retained
label, so both endpoints of (1) become `(+,i)` and the boundary is zero.
If one instead forgets the object tag without transporting its endpoint
label, (1) becomes

\[
                         e_{\tau i}-e_i.               \tag{2}
\]

But that fold is not a chain map to the fixed physical complex unless the
promoted-occurrence column `W` with boundary (2) is already supplied.  The
groupoid bar therefore organizes the comparison; it does not prove it.

Checker:
[`verify_h2_endpoint_role_groupoid_pointed_bar_gate.py`](../computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py).

## The exact categorical obstruction

Let `V` be the twelve-dimensional order-two occurrence module.  The full
two-object bar has

```text
C0 dimension                 24,
bar rank                     12,
H0 dimension                 12.
```

Thus it is the expected descent from two isomorphic labelled objects to one.
Canonical transport sends every bar boundary to zero.  By contrast,
adjoining one raw relation `d b=e_tau_f-e_f` directly to `V` lowers
`dim H0` from 12 to 11.  It imposes a new occurrence equality instead of
resolving the original source.  This is why a homotopy-orbit symbol cannot
be silently promoted to a physical relative cell.

The constant transpose has `d tau=0`, so there is no hidden first-principal-
parts diagonal that could supply (2).  Its exact role is transport between
the two labelled objects.  The desired nontransported fold is a separate
comparison functor.

## The first pointed/basepoint obstruction

At a physical source point `x`, a pointed differential must satisfy

\[
                           \epsilon_x(d b)=0.          \tag{3}
\]

For the raw fold this is

\[
                          f_\tau(x)-f(x)=0.            \tag{4}
\]

The complete response equation does not force (4).  In the literal
two-orientation quotient, the evaluation

```text
f(x)=1,  f_tau(x)=-1,  all other occurrences=0
```

has complete response sum zero but odd defect `-2`.  This is a quotient of
the literal complete response row, not an asserted full unary-compatible
source point; it proves exactly that the aggregate target equation alone
does not force (4).  The physical mixed target sees the complete endpoint-
even sum, and consequently reads zero on `e_tau_f-e_f`.  Hence there is no
existing target coordinate which absorbs the pointed defect.

One new endpoint-odd graph normal is the minimal rank-preserving extension:

\[
                    d b=(f_\tau-f)-u^-.               \tag{5}
\]

With `V plus k u^-`, the single relation in (5) leaves `H0` dimension 12.
The new coordinate must have value `f_tau(x)-f(x)` and carry the exact lower
word, endpoint decoration, repeated grade, and physical augmented readouts.
It is precisely an occurrence-normalization coordinate; the global GHZ
target does not contain it.  Killing `u^-` afterward would again assume the
comparison, so (5) is a finite interface rather than a completed proof.

## Terminal alternative

There are two different levels of the odd fork.

1. If the scalar odd value is nonzero and the retained-label occurrence is
   identified with the literal same-tail offdiagonal physical cell, the
   committed private-site fan theorem gives four-good or a pure-colour
   coloop.
2. If the scalar value is zero, the pointed scalar obstruction vanishes,
   but the groupoid bar still has no boundary in the fixed physical complex.
   The complete augmented column must still be tested.

At the second level exact duality is exhaustive: the desired odd column is
in the complete physical image, or a full augmented cokernel covector
detects it.  A nonzero physical-`q` value on the protected kernel normalizes
to the relative generator; if `q` kills that kernel, it descends as the
Fredholm separator.  The occurrence coordinate difference alone is not
such a terminal because it has not been extended over every protected
physical column.

## Comparison with the inactive root-even `C_plus` family

There is a genuine common pattern.  The order-two even operator `B-4` is the
top symbol of an endpoint-even Cartan/product-rule prism, whose first target
problem is the signless defect

\[
                            2(w-1)\Delta.              \tag{6}
\]

The inactive route's `C_plus` is exactly a root-even target-cone correction
to a defect of the form (6).  This makes `B-4` a plausible new lower face of
one shared construction theorem.

They are not, however, the same committed literal source family:

| datum | lower `B-4` family | inactive `C_plus/iota` |
|---|---|---|
| source words | `0112`, `0121` | `001122` |
| reinsertion/top | `01211222`, repeated `P3+K2` | canonical collision faces-`(3,5)` packet |
| involution | endpoint-role `tau` at fixed sites | site `rho=(1 4)` plus two-local `0<->2` Weyl |
| coefficient module | rank-five even hole quotient | one rho-even omitted-label orbit |
| target | not physically defined | `-2 D tensor v` |
| reduced Eq | not physically defined | `+2 D (H0-u)Eq tensor v` |
| ordinary residue | not physically defined | labelled `v=(B1+B4)/2` |
| Rees | no beta family defined | generic beta-linear family; beta-zero `D0` separate |

The word histograms already differ: the lower words have `(1,2,1)`, while
`001122` has `(2,2,2)`.  More importantly, the involutions act in different
labelled source categories and the forced augmented rows exist only on the
`C_plus` side.  The committed `iota` is incomplete precisely at the one
rho-even orbit that would be needed for an identification.

Thus the safe unification is conditional:

> Construct one source-labelled target-corrected even family whose lower
> endpoint-occurrence faces are the two `B-4` packets and whose inactive
> projection has `delta_plus`, mixed target, reduced Eq, labelled residue,
> Rees/beta, ridge, and `W` values of `C_plus`.

That would close both lanes with one family.  No current equality of literal
columns proves it, and the beta-zero selected `D0` Bockstein remains a
separate projection.

## Verification

```text
python3 computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py
python3 -O computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py
python3 -I -S computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py
```

Frozen ledger SHA-256:

```text
8ecf499ff8f9be532a7bbd8b72970bd04899c64efe46be581c6603a98058651c
```
