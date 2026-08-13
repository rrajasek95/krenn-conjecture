# The odd/even loop repairs align in target but not yet in source grade

## Result

The odd Gate-I shared repairs and the generic even `tau_plus` repair have
the same target-space pattern, but they are not yet two parity shadows of
one constructed physical source operation.

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
audit.  Thus a single capped, source-valid **oriented loop-resolution
family** has exactly the fixed and paired tail labels needed by Gate I.

At target level, averaging the two resolutions of the fixed shared label
gives

\[
                         {B_1+B_4\over2}=v_{\rm even}.
\]

The table alone does not decide whether
the capped cell lands as a protected relative `U` lower cell or as the
labelled ordinary-residue section `d` used by the existing
target-normalization/anchor-fibre cone.  Either output is sufficient after
the corresponding already-proved assembly; confusing the tail label with
the augmented output row would overclaim the construction.

There is a second, load-bearing qualification for the generic even branch.
The actual maximal `tau_plus` collapse does not omit the shared repeated-02
packet.  Its two omitted labels have repeated-edge labels `01,04`, and both
matching graphs contain the distinct loop edge `25 -> 44`.  Their local
resolutions are

```text
omitted matching 2  -> B0 or B3,
omitted matching 10 -> B5 or B2.
```

Thus the complete local `tau_plus` resolution reaches only
`B0,B2,B3,B5`, never the deficient `B1,B4`.  The shared-02 fixed average
`(B1+B4)/2` equals the desired even target as a vector in the six-column
quotient, but it lies in a different source word/repeated grade.  Reusing
the Gate-I loop family for `tau_plus` requires an additional physical
tail/repeated-grade transport theorem.

That extra even transport is one explicit augmentation-zero direction, not
another six-column problem.  Averaging all four local resolutions of the
omitted rho-pair gives

\[
 w_{\rm nf}={B_0+B_2+B_3+B_5\over4}.
\]

The difference from the desired target is

\[
 \delta_{+}={B_1+B_4\over2}-w_{\rm nf}
   ={(B_1-B_0)+(B_1-B_2)+(B_4-B_3)+(B_4-B_5)\over4}.       \tag{1}
\]

It is rho-even and has augmentation zero.  Abstractly it lies in the
five-dimensional collision/`M_v` difference space.  The remaining theorem
is to realize this one vector in the **same tau-plus word and repeated
grade**; abstract augmentation-zero spanning does not provide that physical
nullhomotopy.

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
edge, and Rees grade, with one chosen oriented resolution carrying the
displayed `B` tail.  It must cap the formal Hasse top's anchor,
endpoint-ridge/Omega, and complementary-word faces.  Its surviving augmented
output must be either the protected relative lower cell or the labelled
ordinary-residue section.  Symmetrizing it must remain source-valid.
Declaring this comparison would simply assume the missing loop-resolution
cell.

## Consequences for the proof map

The immediate Gate-I constructive target is no longer

```text
two unrelated fixed/pair constructions.
```

It is

```text
one oriented diagonal/loop-resolution relative C4 family.
```

Once it exists:

1. either oriented branch supplies the two Gate-I tail directions;
2. capping/augmented typing decides whether the direct-`U` or labelled-`d`
   assembly applies;
3. a separate tail/repeated-grade comparison is required before its fixed
   average can supply `tau_plus`; and
4. the independent `beta=0` order-three selected-colour attachment remains.

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
4beb84aabd38f1a09774e1e3d72352a0f38548d47b98a20a55394daa0c6b2da6
```
