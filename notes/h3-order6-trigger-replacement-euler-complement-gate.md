# Trigger-labelled replacement detects the entire rank-77 response complement

## Outcome

The frozen rank-`77` complement has one uniform response-side constructor:

\[
 T_{i\mid j}=I_jD_i,
 \qquad T_{i\mid j}(M)=x_j(M/x_i).                    \tag{1}
\]

Here the deleted trigger `i` and replacement `j` remain separate labels.
For every one of the `159` fixed-grade pair coordinates the checker chooses
a literal pure or mixed matching parent, applies (1), and verifies that
deleting `x_j` and reinserting `x_i` recovers that parent.  The ordered-pair
readout is therefore rank `159`; on the canonical complement its
non-diagonal projection already has rank `77`.

This is a positive response-carrier theorem, not yet the missing physical
cap map.  Collision triangles and the full-star Euler generator give the
proper response-side chain completion, but all present replacement
operators lie in `End(response)`.  No operation currently sends them to the
selected `P3+K2` faces or sends the Euler carrier to `r0/E`.

Checker:
[`verify_h3_order6_trigger_replacement_euler_complement_gate.py`](../computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py).

## Exact census

The `159` pair coordinates split by their literal trigger/replacement
geometry as follows.

| type | full support | complement pivots |
|---|---:|---:|
| one-site transvection | 148 | 72 |
| same-edge recolouring | 4 | 1 |
| diagonal Euler face | 7 | 4 |

No disjoint replacement occurs in the constrained fixed-grade support.
Projection ranks of the `77` complement vectors are

```text
one-site transvection                     77
same-edge recolouring                       4
diagonal Euler                              7
all non-diagonal replacements              77.
```

Thus the one-site transvection part alone detects the whole quotient.  The
same-edge and diagonal coordinates are nevertheless coupled proper faces of
the literal boundary; they cannot be discarded when constructing a chain
map.

## Common Euler carrier

The pinned full-star calculation supplies the exact homogenized carrier

\[
 G_0=\sum_i x_{0i}\iota_{0i}(e)+u\iota_u(e),
 \qquad dG_0=H-u.                                    \tag{2}
\]

All `35` collision triangles telescope, the `21` star-pair outputs have
rank seven, and the full-star coefficient debt is zero.  Equations (1)--(2)
therefore assemble into a chain-level response object once the universal
collision-triangle and Spencer faces are retained.

The smallest such common domain is

\[
                  \mathrm{TrigEulerSpencer}_{rep}.    \tag{3}
\]

It has generators `g_(M;i|j)` for each literal matching parent and allowed
trigger/replacement, together with the homogenizer branch.  Its defining
relations are deletion/reinsertion, the collision triangle

\[
 x_kdC_{ij}-x_jdC_{ik}+x_idC_{jk}=0,                 \tag{4}
\]

and the Euler boundary (2).  Mapping `g_(M;i|j)` to its ordered pair
recovers the divided Taylor--Spencer pair shadow, including its full
rank-`77` quotient.

## Exact remaining operation

Pair-readout surjectivity does not say that arbitrary frozen `D0/D1/D2`
vectors are freely generated without their proper Spencer faces.  The
shortest genuinely new datum is a word/fine/repeated-labelled dg-bimodule
map

\[
 \mathrm{TrigEulerSpencer}_{rep}
       \longrightarrow C_{AugP2}                     \tag{5}
\]

with

```text
trigger deletion/reinsertion  -> selected P3+K2 face,
G0                             -> r0/E.
```

It must change the operation idempotent from `response` to `cap`.  The
current exact data construct the source of (5) and prove that one uniform
`I_jD_i` schema has enough rank; they neither construct nor obstruct the
landing in (5).

## Verification

```text
python3 computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py --mode full
python3 computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py --mode structural
python3 -O computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py --mode structural
python3 -I -S computations/verify_h3_order6_trigger_replacement_euler_complement_gate.py --mode structural
```

Frozen ledger SHA-256:

```text
bcee1254be7d60b08d5eed983141b04e7c68e6fca51aa7c35619afb4a0b36faf
```

The rank calculations are over the first pinned prime.  Literal parent
recovery and the imported Euler/triangle identities are exact
combinatorial statements.
