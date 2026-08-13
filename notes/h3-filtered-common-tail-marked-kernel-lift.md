# Determinant-dark common-tail profiles have a filtered marked lift

## Result

On the balanced six-site word `001122`, the positive
marked-coordinate-preserving lift can be constructed in the full
tangent-Hasse filtration.

Let `V` be the fifteen-dimensional perfect-matching occurrence module.  For
each unoriented `3|3` site cut `S`, let `P_S` be the cut-permanent profile and
`D_S` the alternating cut-determinant covector.  If a **complete** ordinary
occurrence profile `v` satisfies

\[
       \sum_\mu v_\mu=0,
       \qquad D_S(v)=0\quad\text{for every }S,          \tag{1}
\]

then `v` has a unique expansion in the nine centered cut profiles

\[
                        v=\sum_{S\ne S_0}a_S(P_S-P_{S_0}). \tag{2}
\]

Each `P_S-P_S0` is the top distinct-edge face of a difference of two
source-valid colour-diagonal tangent-Hasse cubes.  Its complete lower Hasse
face is the negative top profile.  Therefore (2) constructs the filtered
source cycle

\[
                         (v,-v),                       \tag{3}
\]

where the first entry is ordinary squarefree matching grade and the second
is repeated-site collision grade.

If `h_mu` is the marked **ordinary occurrence** covector and is zero on the
lower collision grade, then

\[
                         h_\mu(v,-v)=v_\mu.             \tag{4}
\]

Thus every profile satisfying (1) with `v_mu != 0` has a constructive
marked kernel lift in the filtered total source map.

Checker:
[`verify_h3_filtered_common_tail_marked_kernel_lift.py`](../computations/verify_h3_filtered_common_tail_marked_kernel_lift.py).

## Proof of the exact criterion

The ten cut permanents span rank ten in `V`; their centered differences span
rank nine in the augmentation hyperplane.  The ten alternating determinants
span rank five and annihilate every cut permanent.  Augmentation is
independent of those five covectors.  Hence

\[
 \operatorname{rank}\langle\mathbf1,D_S\rangle=6,
 \qquad
 \dim\bigcap\ker(\mathbf1,D_S)=15-6=9.                \tag{5}
\]

The nine independent centered cut profiles lie in this kernel, so equality
holds.  This proves (1)--(2) without a support census.  The checker also
reconstructs the unique coefficients for all `3^9=19,683` combinations with
coefficients in `{-1,0,1}`.

For one explicit marked profile, take the difference of the cut permanents
for `024|135` and `012|345`.  It has eight nonzero ordinary occurrences and
coefficient one at

```text
01|23|45.
```

The difference of the two complete physical Hasse cubes has top equal to
this profile and lower equal to its negative.  Its total boundary is zero,
while the ordinary marked readout is one and the collision-grade readout is
zero by fine-grade typing.

This is a genuine positive advance: the contaminating complete-row terms
need not be removed individually.  When their whole profile is
determinant-dark, they are exactly the additional terms that permit the
tangent-Hasse lift.

## Why a bare common-tail pair is insufficient

The isolated frame-circuit pair is never in the positive sector.  The exact
six-site classification is

```text
45 C4 pairs: each has six nonzero determinant readings;
60 C6 pairs: each has six nonzero determinant readings.
```

Thus no difference `e_mu-e_nu` of two distinct perfect matchings satisfies
(1), even when the two occurrences share a literal tail.  Complete-row
contamination is not disposable noise: it must cancel the determinant
coordinates before the tangent correction exists.

For a full source row this cancellation can happen across the other
thirteen matching occurrences.  The theorem tests that **complete** profile,
not merely the protected frame pair.

## Exact remaining physical obstruction

Equation (3) is already closed in the Hasse-filtered total source map.  To
descend it to the underived physical presentation, one needs a
Cartan--Spencer comparison which nullhomotopes the lower collision face
`-v`.  Equivalently, it must provide the relative correction which kills
that face while

* leaving the marked ordinary occurrence readout zero;
* preserving target and fine grade;
* carrying the required ordinary-residue and physical terminal values; and
* respecting the source-labelled common tail.

This is now the first construction on the determinant-dark branch.  The
positive tangent theorem reduces the entire correction problem to one
repeated-site collision profile; it does not yet manufacture its physical
Cartan--Spencer nullhomotopy.

## The determinant-bright branch is only conditionally physical

If some `D_S(v)` is nonzero, it obstructs the tangent-Euler correction.  It
is an exact dual coordinate in the occurrence module, but two further
identifications must not be made silently.

First, `D_S(v) != 0` does not imply that the decorated `3 x 3` cross-cut
minor evaluates nonzero at the optical source.  The checker freezes a
literal `C4` pair on the balanced cut `024|135` for which the abstract
determinant reading is two.  Setting the entire cross-cut coordinate matrix
to one keeps both matching monomials nonzero but makes the evaluated
determinant zero.

Only if

\[
                    D_S(m(A))=\det B_S(A)\ne0          \tag{6}
\]

does the determinant become a physical Fitting carrier.  Even then it still
needs the existing head, support, anchor, and cofactor landing theorem.

Second, an alternating determinant is a cokernel coordinate for the
tangent-cut correction space, not automatically the row-space separator
of the **complete** source map.  It becomes a literal coordinate pivot only
if the full lift-or-separator calculation produces

\[
                         e_\mu^*=\lambda^TM.            \tag{7}
\]

Then (7) isolates the nonzero localized matching monomial and is a genuine
source-unit exit.  Absent (6) or (7), a determinant-bright profile has only
identified which correction direction is missing.

## Coordinate marker versus physical anchor

The ordinary occurrence marker `e_mu^*` in (4) is a legitimate auxiliary
domain covector, but it is not automatically the physical pure-anchor row
used in the rectangular anchor--Cartan augmentation.

This variance matters:

* if the full source correction fails and (7) holds, the separator branch
  closes by a localized source pivot;
* if the filtered kernel exists, `e_mu^*(c) != 0` proves occurrence
  visibility, but does not by itself prove that the physical pure-anchor
  covector has nonzero value on `c`;
* adjoining `e_mu^*` as though it were a physical source row would make the
  bright rectangular minor formal rather than source-provenant.

Consequently the rectangular theorem can consume (3) immediately only when
its `h` is defined as this grade-diagonal occurrence marker in the actual
protected augmented map.  With the presently intended pure/target `h`, one
still needs a source comparison proving that the physical anchor sees the
filtered kernel.

## Updated branch map

```text
literal common-tail frame pair
        |
        v
complete 15-occurrence profile v
        |
        +-- augmentation=0 and all D_S(v)=0
        |       |
        |       `--> tangent-Hasse filtered cycle (v,-v)
        |                    |
        |                    `--> Cartan-Spencer nullhomotopy of lower -v
        |
        `-- some D_S(v)!=0
                |
                +-- evaluated decorated minor !=0 --> physical Fitting route
                +-- full M-row separator (7) -------> localized source pivot
                `-- neither ------------------------> dual correction debt
```

The no-common-tail and initially repeated-site branches remain the previously
identified Tutte/Hall and principal-parts/Cartan--Spencer exits.

## Scope

This theorem is exact for the canonical balanced six-site word and its
site/colour symmetries.  It constructs a filtered lift, not a uniform
all-order comparison.  It does not construct the collision nullhomotopy,
prove nonzero physical anchor charge, identify every abstract determinant
with an evaluated Fitting minor, or land that minor at four-good rank.

## Verification

Run:

```text
python3 computations/verify_h3_filtered_common_tail_marked_kernel_lift.py
python3 -O computations/verify_h3_filtered_common_tail_marked_kernel_lift.py
python3 -I -S computations/verify_h3_filtered_common_tail_marked_kernel_lift.py
```

Frozen ledger SHA-256:

```text
75ae40a75fc7419cd64f84e9c4e72b2243bec229658e82ea7087a6403a8275d6
```
