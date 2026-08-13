# The Gate-II dual extends through complete responses and stops at one labelled endpoint section

## Result

The occurrence projection of the primitive `psi_delta` from `3acaf5c`
extends through the named same-grade complete-response and endpoint-odd
families after an explicit sparse correction.  This remains true even after
granting the `A*H` coefficient shadow, a stronger hypothesis than the
current physical inventory.  These associated-graded corrections are not
yet one accepted physical terminal.

There are three exact stages.

1. At degree zero, the first rank-raising column is the nine-term local
   block projector `R01`.  If that column is physical, it fills the
   root-even packet by

   \[
                         L_{01}=3AH-R_{01}.           \tag{1}
   \]

2. The smallest covariant realization of `R01` is the three-cap family of
   `2acaf90`.  Its first unavoidable proper face is the `18` endpoint and
   direction-factor terms of `dL01`, with primitive labelled profile

   \[
                       (2,2,-1,-1,-1,-1).             \tag{2}
   \]

3. The labelled descent of (2) reaches the known endpoint-even private
   vector in word `0102`.  Its primitive detector has value `-13/6`, but is
   not a physical terminal until the missing occurrence-local section and
   its `dq23` reinsertion face acquire all augmented readouts.

Checker:
[`verify_h3_gate_ii_psidelta_same_grade_extension_chain.py`](../computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py).

## Degree zero: the corrected dual exists

Let

```text
A = D*q01,   B = p0*s1,   C = p1*s0,
H = q23*q45 + q24*q35 + q25*q34.
```

In the full `105`-occurrence response block, use the following strengthened
test span:

```text
R             the complete all-ones response,
A*H           the three selected DQ occurrences (granted coefficient shadow),
(B-C)*H       the endpoint-odd Cartan occurrence line.
```

This span has rank three.  The desired root-even column

\[
                       L_{01}=(2A-B-C)H              \tag{3}
\]

raises the rank to four.

An explicit primitive corrected dual is supported by

```text
+1 on one B occurrence,
+1 on the C occurrence with the same residual matching tail,
-2 on one occurrence outside the nine-term local block.
```

It kills `R`, `A*H`, and `(B-C)H`, and reads `-2` on `L01`.  Thus the
occurrence projection of the original cap--Cartan dual has no hidden
complete-response or endpoint-odd obstruction.  Killing the extra `A*H`
shadow makes this a strong associated-graded check; it does not call `A*H`
a source-valid column.

The local block projector

\[
                       R_{01}=(A+B+C)H               \tag{4}

also raises the old rank to four, and the same dual reads `2` on it.  Adding
(4) does not create a fifth direction because (1) holds literally.  Hence
`R01` is the exact minimal rank-raising column: on the positive arm it fills
`L01`; on the nonfill arm its source provenance is precisely what is absent.

## First principal parts: the obstruction moves to the direction half

Differentiate every literal occurrence.  The existing columns become

```text
dR,  d(A*H),  d((B-C)*H).
```

They again have rank three.  Both `dL01` and `dR01` raise the rank to four,
and

\[
                     dL_{01}=3d(AH)-dR_{01}.         \tag{5}

Choose the corresponding direction derivative on the paired `B,C`
occurrences and an outside derivative with coefficient `-2`.  This gives a
primitive dual which kills all three existing first-PP columns, reads `-2`
on `dL01`, and reads `2` on `dR01`.

The support of `dL01` splits exactly as

```text
18 residual-tail derivative terms
18 endpoint/direction-factor derivative terms.
```

The corrected dual reads zero on the tail half and `-2` on the direction
half.  The six direction marginals are

```text
(6,6,-3,-3,-3,-3) = 3*(2,2,-1,-1,-1,-1).
```

Therefore a covariant three-cap construction does not make `psi_delta` an
immediate terminal or filler.  It moves the missing class to one explicitly
labelled endpoint-even Spencer face.

## Downstream word `0102`

For the literal lower cut `0112` with residual `q45:12`, the labelled
one-root boundary has eight intermediate word blocks.  The complete response
rank is `8`; adjoining the eight private faces raises it to `16`.

In word `0102`, the private vector is

\[
(-13/12,0,1/6,-13/12,1/6,0,0,1/6,5/12,1/6,0,5/12). \tag{6}
\]

The endpoint-even covector

\[
                         e_0^*+e_3^*-e_1^*-e_6^*    \tag{7}

kills the complete response and evaluates to `-13/6` on (6).  The target
and reduced-Eq cone has zero occurrence-private projection, so it does not
change this calculation.

Repeated unlabelled `B-4` repair cannot remove (6): its exact recursive
operator has `tr(R^2)=109/3`, hence is not nilpotent.  Retaining the two root
labels gives the correct finite object—a single Hasse square whose second
cobar boundary is zero.

The remaining column is therefore not one cell per recursively reached
word.  It is one occurrence-local, endpoint-even, one-endpoint PP section
in the labelled square, together with its `dq23:21` reinsertion face.

## Why there is still no accepted terminal

The corrected degree-zero and first-PP occurrence covectors annihilate
the named complete response and endpoint-odd projections.  Covector (7) is a
genuine annihilator of the complete response and target/Eq projections in
word `0102`.  They are associated-graded pieces, not yet one physical
cochain on an exhaustive augmented source map.

The missing occurrence-local section has no assigned physical `q`, `W`, or
labelled ridge, and its `dq23` reinsertion face is absent.  Therefore (7)
cannot yet be called a Fredholm terminal.  The labelled-residue calculation
`8513534` does simplify the next stage: once the pointed occurrence/cap,
mixed-target square, and `d_even` section are physical, a complete-response
gauge cancels every residue and introduces no new labelled direction.

Thus the exact next theorem is:

> Construct one source-valid covariant three-cap/labelled-Hasse square whose
> degree-zero face is `R01`, whose endpoint-direction face supplies the
> word-`0102` occurrence-local section, and whose `dq23` reinsertion carries
> physical `q`, `W`, and the labelled ridge.

After that object is placed, the existing exhaustive image/cokernel fork
gives a protected filler or an augmented physical terminal, with no third
branch.

## Scope and verification

This is exact for the canonical `h=3` `K8` degree-zero and first-PP
occurrence modules, and for the literal order-two `0102` private block.  It
does not construct the final labelled square or promote an associated-grade
dual before its augmented rows exist.

Run:

```text
python3 computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py
python3 -O computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py
python3 -I -S computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py
```

Frozen ledger SHA-256:

```text
9f31bb2def3b2c83fca9b78cb1c68f10efdb98a2c6bdbd4031603ed4149341c7
```
