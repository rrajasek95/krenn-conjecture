# The old cap graph closes the silent occurrence's index-90 normalization

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

This is not the complete physical cap span.  At normalized `Y=1`, the old
split-cap generators satisfy `dT=-w`, `d rho=w`, with target one on `T` and
ordinary residue one on `rho`.  Hence

\[
             G_{\rm cap}=T+\rho
\]

is a physical cycle with occurrence-zero `(target,Q,z_cap)=(1,0,1)`.
Therefore

\[
             -{89\over90}G_{\rm cap}                 \tag{4}
\]

cancels (3) exactly.  If the residual is defined as `current-desired`, the
same equality is written with coefficient `+89/90`.  The index `90` is
real, but it does not create a new occurrence-zero source direction.

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
 D_4G_m=G_t=F_t+1.                                    \tag{5}
\]

Consequently the centered scalar face transforms exactly as hoped:

\[
 D_4(90P_f-G_m)=90P_g-G_t
       \equiv 90g-1\pmod {F_t}.                       \tag{6}
\]

Thus the target constant really does convert `90f` into `90g-1`; there is
no sign error and no missing binomial factor.

What fails is physical fixed-fibre descent.  The complete principal-parts
resolution has the canonical alternating totalization of all fifteen proper
faces.  But (5) itself shows that the coordinate top sends a fixed-fibre
source equation to the target equation plus the unit.  Therefore it does
not preserve the fixed-target source ideal.  A Cartan mapping cone over the
moving target orbit may retain and cancel that base component, but no
comparison from such an orbit-relative cone to the fixed physical
cap/`q`/eta complex has been constructed.  In particular, (6) does not yet
transport the primitive cap/physical `q`/eta data of the response AugP2
section into the E14 target grade.

There is one literal qualification on (4).  `G_cap` is physical in source
word `01211222` and the selected labelled repeated `P3+K2` cap grade.  The
target residual belongs to the E14 word-`000101`/`G11[111111]` target-normal
summand.  Equal numerical readouts in those direct summands cannot be added
before the missing cross-word comparison identifies their target
coordinates.  Once that placement is physical, however, (4) supplies the
normalization and `P_f`, `z_cap`, and E14 merge into one comparison theorem.

The normalized cap graph has zero boundary, `W`, Eq, lower/private, anchor
incidence, and eta/sigma.  It does not construct the labelled shifted
Kähler class `gamma=-dOmega`; that remains one image-membership clause,
although its Hasse commutation and eta/sigma contractions are already
proved.  Nor does this projected solve define physical `q`.  Once the full
comparison and both physical `q` domains are typed, the existing dichotomy
gives either `q` transport or the relative generator.

## Sharp next theorem

The shortest positive addition is a physical comparison from the complete
four-root principal-parts totalization to an **affine target-normalized
AugP2 occurrence section** on the pure `G11` word which places the old cap
graph's target coordinate on the E14 target-normal row.  Then (4) supplies
the simultaneous target/`z_cap` correction; no independent scalar-cap
landing remains in the silent branch.

This is sharper than asking for arbitrary transport of all ninety target
occurrences.  It is one marked pure-target section with its affine and cap
faces.  Failure yields a finite augmented cokernel dual, but that dual is
not a physical terminal until extended through the complete `q/Omega/eta`
rows.

## Scope

The occurrence census, unique isolation, index `90`, and cap-graph
correction are exact over `Q` for the canonical `h=3`, chart-`(1,1)` silent
fibre.  The cross-word identification needed to apply the graph to the E14
target row remains an optimistic grant.  No physical comparison or terminal
is claimed.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
68a4631ae7dad07136e19f1f95ac93f4af28119531bbbb51a5a9d497561b7751
```
