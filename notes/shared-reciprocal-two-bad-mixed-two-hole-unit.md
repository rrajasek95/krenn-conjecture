# The arbitrary binary two-hole square is a characteristic-zero unit

## 1. Result

The mixed-colour repair allowed by the target-axis cycle gate does not
exist once the complete two-hole coefficient system is imposed.

> **Mixed two-hole unit theorem.**  Let `q` be an arbitrary binary
> endpoint-block quadratic on five sites; every physical edge carries an
> unrestricted ordered `2 x 2` block.  If
>
> \[
> K_0=K_1=K_2=0,\qquad K_3=X_0,\qquad K_4=X_1,            \tag{1}
> \]
>
> coefficientwise, then the equations generate the unit ideal over
> `QQ`.  An exact source identity uses only 18 of the 80 coefficient rows.

Combined with the abstract two-hole tensor split in
[`shared-reciprocal-two-bad-target-axis-mixed-cycle-gate.md`](shared-reciprocal-two-bad-target-axis-mixed-cycle-gate.md),
this excludes every `>=3`-centre **genuinely target-axis** kernel component
in the two-bad common-cofactor packet, even with arbitrary mixed-colour
internal cells.

This does not close the whole two-bad cokernel problem.  A general mixed
kernel row need not have its target-coordinate part separately in the
kernel: off-diagonal cells can transgress a non-target component into the
target sector.  That tilted/transgression branch is outside the hypothesis
of this theorem.

## 2. Reduction to the normalized square

Suppose a target-axis kernel component

\[
                    \sum_x u_xe_t^{(x)}K_x=0             \tag{2}
\]

has support `S` of size at least three.  A five-site word with its unique
target colour at `x in S` isolates the binary projection of `K_x`, hence
that projection is zero.  At most two holes remain to carry the two bright
pure tensors.

The pinned two-hole rank lemma allows arbitrary local preimage vectors.
It proves that the only possible two-hole allocation, after exchanging the
holes and bright colours, is

\[
                    K_3=\lambda X_0,qquad K_4=\mu X_1,
                    \qquad \lambda\mu\ne0.                \tag{3}
\]

There is no square-root or gauge assumption in normalizing (3).  Scale
every cell incident to site `4` by `lambda^-1`, every cell incident to site
`3` by `mu^-1`, and leave sites `0,1,2` unchanged.  A four-site cofactor
scales by the product of the site factors outside its hole.  Consequently

```text
K3 scales by lambda^-1,
K4 scales by mu^-1,
```

while the three zero cofactors remain zero.  This gives (1).  The swapped
allocation is transported by the binary colour involution.

Support sizes four and five leave one or zero holes and are already
impossible in the tensor split.  Thus (1) is exactly the remaining
three-centre target-axis case, not an inferred normal form for tilted
kernels.

## 3. The exact polynomial system

For each edge `uv`, `u<v`, use the four ordered variables

\[
                         q_{uv}^{ij},\qquad i,j\in\{0,1\}.
\]

There are `10*4=40` variables.  For a word `w` on the four sites outside
hole `x`, the literal cofactor coefficient is the three-matching sum

\[
 K_x(w)=\sum_{M\in\operatorname{PM}(\{0,\ldots,4\}\setminus\{x\})}
             \prod_{uv\in M}q_{uv}^{w_u w_v}.             \tag{4}
\]

The ideal has 80 source rows:

```text
48 rows: all 16 coefficients of K0,K1,K2 are zero,
16 rows: K3 has only coefficient 0000 equal to one,
16 rows: K4 has only coefficient 1111 equal to one.
```

No support localization, determinant, or nonzero variable is added.

## 4. The 18-row source certificate

Singular computes `liftstd(I,L)` over `QQ`, obtains `G=[1]`, and verifies

\[
                         \operatorname{matrix}(I)L=[1].   \tag{5}
\]

Only the following source multipliers are nonzero.  Variable names in the
table follow the checker convention `qUVij=q_uv^(i,j)`.

| row | source equation | multiplier |
|---:|---|---|
| 7 | `K0(0110)=0` | `q0111*q0200` |
| 11 | `K0(1010)=0` | `q0100*q0211` |
| 15 | `K0(1110)=0` | `-q0110*q0200-q0100*q0210` |
| 23 | `K1(0110)=0` | `q0111*q1200` |
| 27 | `K1(1010)=0` | `q0100*q1211` |
| 31 | `K1(1110)=0` | `-q0101*q1200-q0100*q1210` |
| 39 | `K2(0110)=0` | `q0211*q1200` |
| 43 | `K2(1010)=0` | `q0200*q1211` |
| 47 | `K2(1110)=0` | `-q0201*q1200-q0200*q1201` |
| 49 | `K3(0000)=1` | `-1` |
| 55 | `K3(0110)=0` | `q0311*q1200` |
| 59 | `K3(1010)=0` | `q0200*q1311` |
| 61 | `K3(1100)=0` | `q0100*q2311` |
| 63 | `K3(1110)=0` | `-q0301*q1200-q0200*q1301-q0100*q2301` |
| 72 | `K4(0111)=0` | `q0410*q1200` |
| 76 | `K4(1011)=0` | `q0200*q1410` |
| 78 | `K4(1101)=0` | `q0100*q2410` |
| 80 | `K4(1111)=1` | `-q0400*q1200-q0200*q1400-q0100*q2400` |

Expanding the sum of these multiplier-row products gives exactly `1`.
This is an ordinary polynomial identity; the checker verifies it inside
the original 40-variable ring before accepting the lift.

The compact rows also explain why the earlier local two-cycle guard was
not a counterexample.  Its mixed cancellation can repair one `2+2`
coefficient, but the linked `0110`, `1010`, `1100`, and `1110` rows at all
five holes cannot be repaired simultaneously.

## 5. Consequence and remaining boundary

The theorem closes all large-support target-axis components:

```text
support size 3: the two-hole unit (this note),
support size 4: one hole cannot carry two distinct pure images,
support size 5: no hole remains.
```

Together with the previously committed one- and two-centre target-axis
exclusions, no genuinely target-axis kernel row can carry the two-bad pure
kernel product.

The exact remaining mixed branch is a tilted kernel relation whose target
coordinate is coupled to non-target coordinates by off-diagonal internal
cells.  The unit theorem must not be quoted for that branch until a
source-valid filtration or transgression argument produces a separate
target-axis kernel component.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_mixed_two_hole_unit.py
python3 -O computations/verify_shared_reciprocal_two_bad_mixed_two_hole_unit.py
```

Normal and optimized runs reconstruct all 80 rows and verify the same
source identity:

```text
source lift SHA-256:
4aafbfa5d93804089447f4667db845419ff4acd99c11051ba61c4f8eca9a272c

ledger SHA-256:
9908daa3de09c9bea768c1163aba70ddc9605b3c6a68a8918f0c8b7b1b800dbf
```
