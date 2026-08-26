# Normalized pure rows do not activate the reciprocal X5 guard

Status: **exact support-restricted lemma proved; general bicoloured X5 arrow
remains open.** No D12 file was read and no ideal/CEGAR solve was run.

## Outcome

The three normalized pure rows do **not** exclude the inactive reciprocal
covector from the sealed parent package.  The covector is `L=E00`, so its
target coordinates are intrinsically

```text
(kappa_0,kappa_1,kappa_2)=(1,0,0),
```

independent of the source coefficients.  A minimal four-cell extension of
the formal guard makes all three pure amplitudes exactly one while retaining

```text
s_L=<E00,A_12>=0,
R_12^67(I)=I,
R_67^12(E00)=E00,
r^2=0.
```

Thus the reciprocal covector stays clean but inactive after exact pure-row
normalization.  This extension is not an X5 point: it has 78 nonzero mixed
amplitudes.

## Minimal source-labelled extension

The original guard has

```text
A_16=A_27=A_67=I3,  A_03=A_45=E00,
all other cells zero.
```

Its pure amplitudes are `(1,0,0)`.  Add exactly

```text
A_03[1,1]=A_03[2,2]=A_45[1,1]=A_45[2,2]=1.            (1)
```

Then all five displayed blocks are diagonal identities and the pure
amplitudes are `(1,1,1)`.  Four new cells are minimal within the frozen
physical support: for either missing colour the old graph has matching number
two (`16,27`), so a four-edge perfect matching needs at least two new cells.

The cap-67 triangle data are unchanged.  For `K=I`, only the internal
triangle response `R_12(K)=I` is nonzero; all twelve outside responses remain
zero.  The five-set functional `beta=eval_00000` still induces `L=E00` on
edge `12`.  For the switched cap `12`, its response is supported only on
edge `67`, hence `r^2=0`, but activity fails at both `s_L=0` and
`kappa_1*kappa_2=0`.

## Exact support-restricted full-X5 contradiction

There is nevertheless a terminal lemma for every extension which keeps this
physical support.  Write

```text
u_c=A_03[c,c],  v_c=A_45[c,c].
```

The only physical perfect matching is `03|16|27|45`; the edge `67` cannot
participate because the remaining vertices `1,2` have no edge.  Therefore

```text
Phi(c^8)=u_c v_c.                                      (2)
```

If all pure amplitudes are one, every `u_c` and `v_c` is a unit.  For
`c!=d`, the mixed word carrying colour `c` on sites
`{0,1,2,3,6,7}` and colour `d` on `{4,5}` has

```text
Phi(c,c,c,c,d,d,c,c)=u_c v_d !=0.                     (3)
```

This proves over every integral domain that normalized full X5 is impossible
in the frozen support class.  In the minimal extension (1), the first literal
failure is

```text
word 00001100, matching 03|16|27|45, amplitude +1.
```

This is a direct source identity, stronger for this support than invoking the
certified block-diagonal theorem.

## Why this does not finish the general branch

The first mixed equation can already be cancelled without changing any of the
formal triangle/five-set data.  Add two off-support source cells

```text
A_04[0,1]=+1,  A_35[0,1]=-1.                           (4)
```

For word `00001100`, (4) contributes the second matching
`-04|16|27|35`, exactly cancelling `+03|16|27|45`.  The three pure amplitudes
remain one, `K=I` remains in the triangle kernel, `R_12^67(I)=I`, all five
`beta=00000` internal cofactors remain zero, and the switched `L=E00` remains
clean but inactive.

This two-cell guard is still not X5: 69 mixed amplitudes remain nonzero, the
first at `00002200`.  It proves that equation (3) is support-dependent and
cannot be promoted to an arbitrary bicoloured source by silently discarding
same-source cancellations.

Hence the exact boundary is:

- pure normalization alone does not activate `L`;
- full X5 contradicts every support-preserving extension of the formal guard;
- an arbitrary bicoloured extension is not routed to an existing terminal
  theorem by the retained identities.  It still needs a source-labelled
  identity controlling all off-support mixed cancellations, or a different
  reciprocal covector whose four activity factors are forced nonzero.

The parent reciprocity manifest is
`05e85e32252a31f55c85f6a8ec1e08e6aa2c02674dc98b523c6b99f56509cced`.

