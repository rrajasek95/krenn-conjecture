# Equivariant degree-two Macaulay compression screen

Status: **exact negative screen; retire the unrestricted symmetry-adapted
degree-two membership test**.

The frozen degree-one packet is only `B4 x S3`-stable.  Its 1,872 mixed
rows contain only 144 of the 168 `6+1+1` words, so an `S8 x S3` character
calculation first has to adjoin 24 rows.  The resulting permutation module
has 1,896 rows, and

```text
D2 = Q[1896 rows] tensor Sym^2(Q[252 cells])
dim(D2) = 60,440,688.
```

Under the enlarged group the four frozen target orbits merge in pairs.  The
endpoint target has orbit size 336 and stabilizer order 720; its induced
permutation module contains 12 irreducible types.  The third-colour target
has orbit size 168 and stabilizer order 1,440; its induced module contains 9
irreducible types.

Exact character decomposition and two independent stabilizer Burnside sums
give

| target module | `dim Hom_G(target,D2)=dim D2^H` | degree-one analogue |
|---|---:|---:|
| endpoint | 269,064 | 4,644 |
| third-colour | 134,782 | 2,342 |
| combined | 403,846 | 6,986 |

Thus even the smallest exact target-relevant coefficient interface has
403,846 entries before monomial-row expansion, over fifteen times the
frozen 25,901-orbit degree-two lower-bound screen.  The complete target
irrep multiplicities and predicted multiplicity-space block sizes are in
`results_equivariant_syzygy_compression.json`; all 12 endpoint and 9
third-colour blocks are nonzero.

There is also a hard grading obstruction: the frozen targets `a_tail*H_k`
have ordinary degree five, whereas `F_w*q` has degree six.  A same-grade
degree-two test would require a new audited linear homogenizer/localizer or
a separately specified quadratic target.  Character theory does not supply
that choice.

No expanded 60-million-object matrix or Groebner basis was assembled.  The
finite character calculation, stabilizer histograms, decomposition, and
Frobenius-reciprocity checks agree in standard, optimized, and isolated
no-site modes at logical SHA
`fefad32d70bdac7ec83315b7762665da4bd8f71ab1f381d1d66637719693edfe`.

