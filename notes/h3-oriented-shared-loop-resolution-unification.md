# One oriented loop-resolution cell would close both labelled-residue gates

## Result

The odd Gate-I shared repairs and the generic even `tau_plus` residue repair
are two parity shadows of one local source operation.

Every label missed by the canonical collision collapse contains the repeated
edge `02`, and the collapse sends `0,2` to the same physical target site `4`.
The obstruction is therefore the forbidden loop `44`.  If the two other
matching edges have images `ab` and `cd`, the two canonical loop-free `C4`
resolutions are

```text
ab | 4c | 4d,       cd | 4a | 4b.
```

In the canonical faces-`(3,5)` six-column target, the complete table is

```text
shared label 3:  B0 or B3,
shared label 4:  B4 or B1,
shared label 5:  B2 or B5.
```

The physical involution fixes label `4` and exchanges `3,5`; on the target
it acts by `(B0 B5)(B2 B3)` and fixes `B1,B4`.  Hence the two coherent
oriented choices are

```text
fixed B4, paired (B0+B5)/2,
fixed B1, paired (B2+B3)/2.
```

These are exactly the two alternatives allowed by the Gate-I shared-loop
audit.  A single source-valid **oriented loop-resolution family** would
therefore construct both `d_fixed` and `d_pair`.

The even trace repair is the symmetric shadow of the same family.  Averaging
the two resolutions of the fixed shared label gives

\[
                         {B_1+B_4\over2}=d_{\rm even}.
\]

Thus the three formerly separate labelled-residue requests reduce to one
physical cell theorem.

Checker:
[`verify_h3_oriented_shared_loop_resolution_unification.py`](../computations/verify_h3_oriented_shared_loop_resolution_unification.py).

## Why a Hasse/Spencer construction is plausible

The collision identifies two occurrence factors.  For multi-affine factors

\[
                         f=x+ta,\qquad g=y+tb,
\]

the first diagonal term invisible to the ordinary site collapse is the
divided second Hasse cross term

\[
                    [t^2](fg)=ab.
\]

This is precisely the order at which the collapsed pair can be split into
the two `C4` resolutions above.  The complete Hasse source resolution is
closed under this product rule, and its alternating totalization is already
proved.  This identifies the correct construction to attempt: the comparison
from that diagonal Hasse cross term to the physical repeated-site correction
complex.

The coefficient identity alone is not the desired theorem.  One must still
construct a physical relative cell in the canonical word, fine, repeated
edge, and Rees grade, with one chosen oriented resolution as its labelled
ordinary-residue boundary and with zero protected `lower/W/target/ainc`
outputs.  Symmetrizing that cell must remain source-valid.  Declaring this
comparison would simply assume the missing loop-resolution cell.

## Consequences for the proof map

The immediate constructive target is no longer

```text
d_fixed + d_pair + d_even.
```

It is

```text
one oriented diagonal/loop-resolution relative C4 family.
```

Once it exists:

1. either oriented branch supplies Gate I's fixed and paired sections;
2. the even average supplies `d_even`;
3. the already proved anchor-fibre alternative removes the remaining
   target/anchor/residue cone obstruction; and
4. only the weighted denominator membership on the generic even route and
   the independent `beta=0` order-three selected-colour attachment remain.

This does not construct the weighted denominator transgression, and it does
not identify the `beta=0` third-cofactor cell with the loop-resolution
family.  Those are separate obligations until a higher relative Spencer
theorem proves otherwise.

## Verification

Run

```text
python3 computations/verify_h3_oriented_shared_loop_resolution_unification.py
python3 -O computations/verify_h3_oriented_shared_loop_resolution_unification.py
python3 -I -S computations/verify_h3_oriented_shared_loop_resolution_unification.py
```

Frozen ledger SHA-256:

```text
33813e438b4d3d51df6867f6f0df59ee018550f9bd741f69d41cc2b0bea58e1c
```
