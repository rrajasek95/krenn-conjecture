# Exact four-qubit `Q`-tensor invariant probe

Status: **exact evaluation on two frozen controls; the proposed invariant
route does not recover the recurring nonconstant chart splits.**

With `Q_s=Q_{i0i1i2i3}` in binary order, the standard quadratic invariant is

```text
sum_{s=0}^7 (-1)^popcount(s) Q_s Q_{15-s}
```

(half the full epsilon contraction).  The three determinants use the
`01|23`, `02|13`, and `03|12` flattenings.

- On the exact support-six point over `Q(r), r^2=2`, the quadratic is `4`
  and the determinants are `(-32,-32,0)`.
- On the entire exact one-dimensional branch-1 chart over
  `Q(z), z^2-14z-1=0`, they are `(4;32,0,-32)`, independent of its parameter
  `T`.  The repository's unsigned complementary pairing is also `4`.

Thus these restrictions do not detect `T=0` versus `T!=0`, and none supplies
a nonconstant factor.  The zero flattening records a rank pattern whose
position changes with orientation, not the branch divisor.  In particular,
this concrete test gives no evidence that factors such as `A`, `B`, or `R25`
are restrictions of these standard invariants.

Standard, `-O`, and `-I -S` replay share digest
`87a79e5fc2c734eca55da963013acc45b4cc182ff454912d1e5585794c02c2a7`;
the coordinate mutation fires with digest
`8d679d7a897618cf9f9da94512d5b91ab01bd7d35741da1155fc6cd43caa7c45`.

## Sextic invariant and exact orbit audit

`audit_luque_thibon_dxt_orbit.py` implements the Luque--Thibon sextics from
the literal biquadratic determinant definition

```text
b_xt = det(partial^2 A / partial y_i partial z_j),
b_xt = [x0^2,x0x1,x1^2] B_xt [t0^2,t0t1,t1^2]^T,
D_xt = det(B_xt).
```

It independently verifies `L+M+N=0` and
`HL=Dxz-Dxt`, `HM=Dxt-Dxy`, `HN=Dxy-Dxz`.  The exact values are

| tensor | H | L | M | N | Dxy | Dxz | Dxt |
|---|---:|---:|---:|---:|---:|---:|---:|
| support 6 | 4 | -32 | 32 | 0 | 64 | 64 | 192 |
| support 8 | 4 | -32 | 32 | 0 | 64 | 64 | 192 |
| branch 1, `z^2-14z-1` | 4 | 32 | 0 | -32 | 64 | 192 | 64 |
| branch 1, `z^2+2z-1` | 4 | -32 | 32 | 0 | 64 | 64 | 192 |

The full `(H,L,M,Dxt)` permutation orbit has size three in every case and
is exactly the same set.  Thus the complete polynomial invariant tuple is
constant up to qubit permutation.  This is equality in the categorical
quotient; it is **not** an orbit-equivalence certificate.

The exact `sl2^4` action supplies the missing distinction.  On each branch,
the `T=0` weight-two endpoint has action rank 11 (stabilizer dimension 1),
whereas a generic point has rank 12 (stabilizer dimension 0).  Stabilizer
dimension is orbit-invariant, so no finite `SL(2)^4` transformation takes a
generic branch point to its support-six/`T=0` endpoint.  This is the precise
obstruction requested by the bounded equivalence test.

The generic tangent nevertheless lies in the orbit tangent, with generator
`h_i=1/(2T), e_i=f_i=0` for all four qubits.  It integrates explicitly: for
nonzero `T,T'`, choose `s^2=T'/T` and apply `diag(s,s^-1)` on each qubit;
this maps `q(T)` exactly to `q(T')`.  Hence the punctured parameter line is a
single orbit and `T=0` is its singular orbit-closure limit.  The script also
gives an explicit diagonal normalization of the endpoint to the standard
`G_abcd` weight-two form over a finite square-root extension.  A separate
upper-unipotent ansatz fits every weight-one coordinate but leaves one exact
quadratic `Q0` residual, consistent with the stabilizer obstruction.

Standard, `-O`, and `-I -S` replay share logical digest
`bf55b44a20c5dc9d3b8a98429060be9429b9d39fec94c46716f9b543b64458e1`;
the coordinate mutation fires with logical digest
`9c62ec5c3cc2f9dd40645435a0fcdbcb2a04f9b0edf7053c131b0cad9bf9d6d7`.
The script SHA-256 is
`3a74f028976e86026776d45bf20fa7ec07e2add7b82982a7e6a4f5644123de41`.

Scope guard: this is an exact audit of the frozen 16-entry `Q` tensors.  It
does not transform or identify the underlying 24-cell `X`/cofactor charts
and therefore cannot replace the source-row partner arguments.
