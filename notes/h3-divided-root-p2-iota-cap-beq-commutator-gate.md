# The marked P2 map names B1/B4 but the cap landing remains tied B=Eq

## Result

The divided-root marked comparison now removes the old word/fine/operation
ambiguity in the two lower faces.  The missing-site mark and cofactor recover
the deleted edge, and the literal lower coefficient map gives

```text
0112/q23:21 -> B1,       0121/q45:12 -> B4.
```

Endpoint reversal is killed by the coefficient quotient.  With

\[
 c_i^+=6e_i-\mathbf 1,
\]

the two normalized cut images are `c_1^+/8` and `c_4^+/8`; their sum is

\[
 \delta_+=\tfrac14(-1,2,-1,-1,2,-1).
\]

Thus the **coefficient labels** `B1/B4` are now canonical and
source-provenant in the marked-derived category.  The marks do not,
however, distinguish the protected `B` copy from the `Eq` copy in the cap
totalization.

The exact checker is
[`verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py`](../computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py).

## First protected commutator

The physical cap top is internally tied `B=Eq`.  Therefore the actual and
required readouts are

```text
actual composite       (delta_plus,delta_plus),
required landing       (delta_plus,0).
```

Orienting the comparison boundary as required minus actual gives

\[
 C_{23}=(0,-c_1^+/8),\qquad
 C_{45}=(0,-c_4^+/8),\qquad
 C=(0,-\delta_+).
\]

The two cut commutators have rank two.  The integral covector

\[
 (D_6,-D_6),\qquad D_6=(-1,2,-1,-1,2,-1),
\]

kills the actual tied composite and reads `3` on both the required landing
and `C`.  Target already commutes, and the transported first PP face retains
the private detector `35/72` and ordinary residue zero.  Hence the first
failure is protected copy separation, not coefficient, word, fine,
restriction, reinsertion, or target naturality.

## Existing corrections do not fill it

After the target/root-reduced-Eq cone, the complete Eq residual remains
`-delta_plus`.  At root-word resolution the required hidden proper face is

\[
 H=(\operatorname{lower},\operatorname{Eq},\operatorname{ores})
   =(-E,0,+E),\qquad
 E=2D_{\rm root}\otimes (B_1+B_4)/2.
\]

The correction test grants more than the existing inventory: arbitrary
residue endpoints `K_u=(0,0,u)`, arbitrary tied endpoints
`M_u=(u,u,0)`, and every root-word bar between them.  Their span stays
`{(x,x,z)}` of rank 48.  Four lower-minus-Eq covectors pair with `H` by
`(+2,-2,+2,-2)`.  Equivalently,

\[
 H=-M_E+K_E+C_{Eq},\qquad C_{Eq}=(0,E,0).
\]

The first two terms are covered by the generous endpoint grant; the clean
Eq-only `C_Eq` is independent.  Target columns cannot change these
covectors.  A relative `dK=(H_0-u)E` is also insufficient: after
normalization it leaves `(H0,H1)=(1,1)`, while an absolute `dK=E` would make
both vanish.

So no existing `K_Eq`, target-cone, labelled-ores/Cartan endpoint, or
root-word endpoint bar supplies the correction.  This is a no-go for the
current inventory, not for an unmodelled absolute bright primitive.

## Weakest remaining physical statement

For the constructive clean-pair branch, a quasi-isomorphism of the entire
marked resolution with the cap is unnecessary.  It is enough to construct
one normalized endpoint-even, source-labelled lift on the selected carrier
which:

1. extends the divided-root comparison through `q23/q45` and first PP;
2. has the above `B1/B4` coefficient augmentation;
3. supplies the absolute protected correction `(0,-delta_plus)` together
   with the hidden `(-E,+E)` lower/ores faces; and
4. preserves the already checked target and private/nonzero readouts.

The tied map is a literal counterexample to anything weaker: it has the
right coefficient, word, fine, `q/dq`, target and ordinary-residue shadows,
but the normalized `B-Eq` covector reads zero instead of `3`.

Terminal/Fredholm promotion is strictly stronger.  It must additionally
prove that the resulting protected covector extends over **every** actual
same-grade physical primitive (or that the displayed physical generators
are exhaustive).  The local no-go above neither assumes nor proves that
essential-surjectivity statement.

## Verification

```text
python3 computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py --mode structural
python3 -O computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py --mode full
python3 -I -S computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
5b3702348c3a49e8e73e104c2553afaef708f3bcc7019bd815d04a9b358ff73c
```
