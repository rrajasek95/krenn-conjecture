# Face `0:31:15`, `R=J=U=0` exact characteristic-zero gate

Status: **exact full-source interface and terminal timeout frozen; no
algebraic verdict.**

## Branch and source interface

This package takes only the `J=0` side of the prior sound split, inside

```text
d2-1 != 0,  R=0,
a2 = -B/[b4*(d2-1)].
```

It imposes

```text
J = a4*b4*d3-b3 = 0,
U = 2*a3*d3+a5^2*b4^2*d3^2-2*a5*b4*d3+1 = 0.
```

Every literal source numerator after the `a2` solve is present: raw
`6,...,21` except solved raw 16. Raw 11 is retained as the irreducible
resultant `R`, and raw 9 is retained even though its exact identities with
`J,U` make it redundant after using the already-live `b3,d3`. Thus the input
has 15 literal rows plus branch rows `J,U`, not a pruned discovery core.

The 11 remaining geometric variables are

```text
a0,a1,a3,a4,a5,b3,b4,b5,d1,d2,d3.
```

The exact Rabinowitsch row retains every surviving original live numerator:
the Hafnian numerator, `a5,b3,b4,a0,a1,a3,d1,d2,d3`, the transformed `a2`
numerator `B`, and the transformed `c2` numerator `A-B*d2`, together with
the unaffected `c` factors. It also retains `d2-1` as the explicit branch
guard. The expanded localizer has 18,446 terms. The strict coefficient-first
characteristic-zero input SHA-256 is
`b50c04801f8d63f8251fbd9f05b4b082219ff26b93822ed5570f61657d0ae727`.

## Sole exact gate

Exactly one guarded msolve parametrization was launched: characteristic zero,
DRL, 8 threads, deterministic seed 1, and a 600-second cap. It reached the
cap at 600.555 seconds and was terminated by the runner (`returncode=-15`).
The output is zero bytes and contains no empty, positive-dimensional, or RUR
sentinel. The terminal manifest logical digest is
`1eedd0fae291307b4755cf4e9d046432c54ddf5eeec1b8dde888876cd63118b9`.
No alternate or duplicate run was made.

## Independent replay

The auditor independently reconstructs all 15 source numerators from the
normalized parent packet, verifies raw 11 equals `R`, replays both raw 9
`J,U` identities, and compares canonical polynomial hashes for every source
and branch row. It separately reconstructs the full 18,446-term localizer,
verifies the timeout manifest, and rejects the zero-byte output as a
sentinel. Source-sign and Rabinowitsch-constant mutations fire.

Three modes pass:

```text
standard  21df79f3ac363e242bfb91cc90af8ff09df9fddc83d13bb7960227fcc276c813
-O        3dacfbc2905e3cc9941509a9f0e010a86f05ea531367532973fa8871e54ee3c7
-I-S      dd2e83e49dafee1106e3a3512fbb33fd009120dd2f37ec81540ed440c507d00f
```

The exporter, auditor, input, and manifest file SHA-256 values are
`fe693508659fc91ee457567bdaccfd704ca7bd6712dfbdf4f00dd87b6c5113db`,
`f5f60f3c78668ec2b99cf4f8811ac7da13dd1db872c94b18fed365847a302d70`,
`b50c04801f8d63f8251fbd9f05b4b082219ff26b93822ed5570f61657d0ae727`,
and `e7e51707c49c10e267224c6f398143e12af030c18bea203a46d9a34b3715ad54`.

## Residual and next target

This timeout is a resource terminal only. It neither closes nor exhibits a
component of `R=J=U=0`. The `J!=0` branch was untouched; because raw 9 then
solves `b5`, it remains the cleanest next ten-variable reverse-certificate
target. The previously exported `d2=1` ten-variable branch also remains open
after its own exact timeout.
