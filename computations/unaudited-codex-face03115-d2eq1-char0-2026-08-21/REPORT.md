# Face `0:31:15`, `d2=1` exact characteristic-zero gate

Status: **exact source interface and terminal timeout frozen; no algebraic
verdict.**

## Exact branch reduction

In the normalized parent chart, raw 16 specializes at `d2=1` to

```text
raw16 = K*(b4-1)+2,
K = a5*(d1+1)+1,
N = a5*(d1+1)-1.
```

Thus `K=0` is impossible on raw16 in characteristic zero, and the relation
is faithfully solved by `b4=N/K`. This denominator localization is forced by
the source equation rather than assumed. The irreducible `R=0` branch from
the parent fraction-free split is not used or altered.

## Full literal source and live interface

After substituting `d2=1,b4=N/K` and clearing only powers of `K`, the input
retains every literal raw row `6,...,21` except the solved identity raw 16:

```text
6,7,8,9,10,11,12,13,14,15,17,18,19,20,21.
```

In particular, all four rows omitted from the earlier square discovery core,
raw `6,9,10,11`, are restored. The ten remaining geometric variables are

```text
a0,a1,a2,a3,a4,a5,b3,b5,d1,d3.
```

The Rabinowitsch product retains exactly the surviving original factors

```text
H_num * a5*b3*N * a0*a1*a2*a3*d1*d3
      * (1+a0)*(1+a1*d1)*(1+a2)*(1+a3*d3),
```

and also `K` solely as the forced substitution-denominator guard. Its
expanded numerator has 5,234 terms and degree 28. The strict coefficient-
first characteristic-zero input has SHA-256
`641fc90f837dbfa02b8c6a105a35beadc436ec3c80138fba98450cfdb302c068`.

## Sole bounded exact run

The shared guarded parametrization runner launched exactly one msolve process
with 8 threads, deterministic seed 1, DRL, characteristic zero, and a
600-second cap. It reached the cap at 600.397 seconds and was terminated by
the runner (`returncode=-15`). The output is zero bytes; therefore there is
no empty, positive-dimensional, or RUR sentinel and no algebraic conclusion.
The terminal manifest logical digest is
`502a6c4d31fd902601d0ef48a44d0af7b018887232782f75ba7120f5b38817fa`.
No duplicate, alternate-order, modular, or further exact run was launched.

## Independent replay

The auditor reconstructs all 15 rows directly from the normalized parent
source, independently repeats the rational substitution and primitive-
numerator clearing, and compares every literal monomial/coefficient with the
frozen input. It also reconstructs the complete 5,234-term localizer, checks
`raw16=K*(b4-1)+2`, verifies the timeout manifest, rejects the zero-byte
output as a sentinel, and rejects a positive-dimensional sentinel as
emptiness. Source-sign and Rabinowitsch-constant mutations fire.

Three replay modes pass:

```text
standard  912d780cd316f585279cd57163acee6a4b1ce1022b5d5f2025fb13efb850ccd1
-O        4808c726f62e6aa84be6ae4e94717f6b8a5bb7ea1eb9ae3360b48e3c462f51b0
-I-S      8c8543661fb3d317a2b8dcd6373761d2332f304b61418868eeacc267d1dfae17
```

## Residual

The exact residual is the explicit 15-row, ten-variable localized source
interface above. The timeout is a resource terminal only: it neither closes
nor exhibits a component of the `d2=1` branch. The sibling irreducible
`R=0` branch remains untouched.
