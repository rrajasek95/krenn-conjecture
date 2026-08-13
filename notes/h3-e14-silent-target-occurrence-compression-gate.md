# Silent-target occurrence compression has an index-90 augmented defect

## Exact verdict

On the silent fibre `v04_00=0`, the E14 private return

\[
 g=(p_{1,0}^1s_{1,1}^1)u_{35}^{11}v_{24}^{11}
\]

is literally the tagged `G11[111111]` occurrence with endpoints `0,1` and
residual matching `24|35`.  There are ninety such endpoint/matching
occurrences.  Hence, in the tagged occurrence module,

\[
 c_g=90e_g-\mathbf1_{90},\qquad
 T=\mathbf1_{90}-\tau
\]

give

\[
 \boxed{\frac{c_g+T}{90}=e_g-\frac1{90}\tau.}       \tag{1}
\]

This is the unique combination supported on `c_g` and the complete target
row whose occurrence part is `e_g`.  Thus the tempting compression is exact
coefficientwise, but its affine target normalization is forced to `-1/90`,
not the primitive `-1` of the normalized E14 mixed cell.

Checker:
[`verify_h3_e14_silent_target_occurrence_compression_gate.py`](../computations/verify_h3_e14_silent_target_occurrence_compression_gate.py).

## Complete optimistic augmented signature

Grant more than is currently proved: suppose the response AugP2 centered
section transports to `c_g` in the pure target word and carries the same
primitive cap

\[
                         p=(-Q,-\operatorname{ores}).
\]

Use row order

```text
(marked occurrence, common unmarked occurrence, target, cap Q, cap ores).
```

Then

```text
c_g lift       (89,-1, 0,-1,-1)
target row     ( 1, 1,-1, 0, 0)
--------------------------------
(c_g+T)/90     ( 1, 0,-1/90,-1/90,-1/90).
```

The physical invisible `K_Eq` face cancels the `Q` coordinate, leaving

```text
(g, target, Q, z_cap)=(1,-1/90,0,-1/90).             (2)
```

The normalized desired mixed face is `(1,-1,0,-1)`.  It raises the rank of
the two granted columns from two to three.  The exact remaining residual is

\[
                (0,-89/90,0,-89/90).                 \tag{3}
\]

Equivalently, integrally `c_g+T` has signature

```text
(principal g, target, Q, cap ores)=(90,-1,-1,-1).
```

The target and cap faces are primitive only when the principal occurrence
has coefficient 90.  Dividing to coefficient one divides both augmented
faces.  No linear combination of these two columns changes that ratio while
retaining exactly one `g`.

## The four-root route converts the scalar face exactly—but is only formal

The current AugP2 theorem is itself conditional and is natural in the
marked lower response occurrence, its ordered root directions, and
reinsertion.  Its centered response word is `110000`.  The new occurrence
is in the affine pure target word `111111`.

A site permutation preserves colour multiplicities.  A global colour
permutation only permutes them.  The two multiplicity profiles are

```text
110000 : (four 0, two 1, zero 2)
111111 : (zero 0, six 1, zero 2).
```

Therefore neither allowed symmetry transports the response occurrence
section to the pure target block.

There is nevertheless an exact formal root route.  Choose the mixed
occurrence with the same endpoints and residual matching `24|35` as `g`.
The fourth divided Hasse coefficient of the global root `0 -> 1` changes
the four zero output sites to one.  Its Boolean face profile is

```text
1,4,6,4,1,
```

and its top coefficient on the marked occurrence is one.  If `G_m` is the
complete mixed response coefficient, `G_t` the complete pure coefficient,
and `F_t=G_t-1` the normalized target source row, then

\[
 D_4G_m=G_t=F_t+1.                                    \tag{4}
\]

Consequently the centered scalar face transforms exactly as hoped:

\[
 D_4(90P_f-G_m)=90P_g-G_t
       \equiv 90g-1\pmod {F_t}.                       \tag{5}
\]

Thus the target constant really does convert `90f` into `90g-1`; there is
no sign error and no missing binomial factor.

What fails is physical fixed-fibre descent.  The complete principal-parts
resolution has the canonical alternating totalization of all fifteen proper
faces.  But (4) itself shows that the coordinate top sends a fixed-fibre
source equation to the target equation plus the unit.  Therefore it does
not preserve the fixed-target source ideal.  A Cartan mapping cone over the
moving target orbit may retain and cancel that base component, but no
comparison from such an orbit-relative cone to the fixed physical
cap/`q`/eta complex has been constructed.  In particular, (5) does not yet
transport the primitive cap/physical `q`/eta data of the response AugP2
section into the E14 target grade.

Even if that missing comparison is granted, the index-90 calculation
(1)--(3) remains: normalizing the principal occurrence to one normalizes
the target and `z_cap` faces to `1/90`.  Therefore the four-root route does
not by itself merge `P_f`, `z_cap`, and E14 into the required primitive
mixed cell.

## Sharp next theorem

The shortest positive addition is a physical comparison from the complete
four-root principal-parts totalization to an **affine target-normalized
AugP2 occurrence section** on the pure `G11` word.  It must preserve the
marked principal coefficient while supplying an occurrence-zero correction
of `-89/90` simultaneously in the target and scalar cap-residue rows.  In
integral normalization, it must realize signature `(1,-1,-1)` rather than
the `(90,-1,-1)` forced by `c_g+T`.

This is sharper than asking for arbitrary transport of all ninety target
occurrences.  It is one marked pure-target section with its affine and cap
faces.  Failure yields a finite augmented cokernel dual, but that dual is
not a physical terminal until extended through the complete `q/Omega/eta`
rows.

## Scope

The occurrence census, unique isolation, index `90`, and augmented rank
failure are exact over `Q` for the canonical `h=3`, chart-`(1,1)` silent
fibre.  The cap row in the calculation is deliberately an optimistic grant
of the unproved cross-word AugP2 transport.  No physical source section or
terminal is claimed.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
5d3b0862aa8fa23d68b57820a21fdfa6bc09d7c195cda2075c46c3d04bfc507d
```
