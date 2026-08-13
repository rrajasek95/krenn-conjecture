# The E14 word-change first fails on the unary S-pair target face

## Outcome

The exact decorated-core identification is real but is not the E14 landing.
In the canonical word-`000101` first-hit target, the promoted coordinate

```text
(p1_0_1,s1_1_1) u05_01 v24_11 v34_10
```

has coefficient `+1` and value **zero** under the 22-support first-hit dual.
The entire dual pairing `-1` comes instead from

```text
-(p1_0_1,s1_1_1) u05_01 v13_01 v24_11.              (1)
```

Thus mapping the relative carrier to the shared decorated `2K2` core does
not even kill the truncated E14 cokernel.  A physical word-changing column
must transport the whole unary S-pair remainder, including (1), rather than
one selected coefficient.

The checker is
[`verify_h3_relative_occurrence_e14_endpoint_word_change_spair_gate.py`](../computations/verify_h3_relative_occurrence_e14_endpoint_word_change_spair_gate.py).

## The companion is not an accidental chord obstruction

Set the whole `q13` chart to zero, not merely the single displayed factor.
The complete first-hit rank drops from `269` to `211`, but the target still
has a nine-coordinate remainder.  Every surviving coordinate is a literal
`target_unary` readout.  If both `q04` and `q13` are set to zero, the rank is
`185` and eight `target_unary` coordinates remain.

So the visible companion (1) can disappear without closing the class.  The
obstruction migrates from a coefficient companion to the target-normal row.
This is exactly the behaviour expected from a missing target-bearing
endpoint-word-change cone, and it rules out the tempting conclusion that the
decorated-core hit plus the chordless specialization constructs the landing.

## Why the physical Cartan prism stops here

The retained `t` carrier is endpoint-even.  The already source-provenant,
target-safe Cartan prism is the endpoint-odd combination

\[
                         (1-S)H_w .                   \tag{2}
\]

In the two-column Cartan orbit `(H_w,S H_w)`, the target map is `(1,1)`.
Its kernel is precisely the odd line `(1,-1)`, so there is no nonzero
endpoint-even target-safe combination inside the old orbit.

The correct even companion is `(1+S)H_w`, but it has target defect

\[
                         2(w-1)\Delta .               \tag{3}
\]

The diagonal trace identity supplies the right conditional repair:

\[
 J_*=-2\alpha\beta I,\qquad
 C_{2,+}=-\frac12(1+S)H_wP_2(I).                     \tag{4}
\]

After a source-labelled `P2/iota` placement, (4) cancels (3) exactly.  This
is not yet a construction, because that placement is the word/fine/repeated-
grade map being sought.  Its first principal-parts residual is

\[
 R_{2,+}=-\frac12(1+S)H_wd(P_2(I)),                  \tag{5}
\]

and the strongest current target cone exposes the next face

\[
                         +2D(H_0-u)e_{\rm Eq}.         \tag{6}
\]

Equations (3)--(6) isolate the first missing face beyond the rank-one
`t -> w_E14` landing: an endpoint-even, target-bearing unary-S-pair
comparison.  The old odd Cartan prism cannot supply it, and adjusting the
two old Cartan columns only returns to the odd line.

## Audit of the other physical rows

The obstruction occurs before the remaining augmented rows can be claimed
closed.

- **Target:** this is the first live row.  The new comparison must carry
  (3), with (6) as the first known reduced-Eq proper face.
- **Anchor:** a zero output anchor is not enough.  Pointedness still requires
  the literal conormal `d(u_f-u)`; the graph diagonal is not known to descend
  by a quasi-isomorphism to the original physical source.
- **Physical q:** once a fully augmented physical `P2/KEq` comparison exists,
  the committed q-defect alternative closes q.  It is not an independent
  new construction, but it is not defined before the placement.
- **Ridge:** the order-six Hasse/ridge commutator is zero.  What remains is
  the labelled shifted Kähler lift.  Multiplying by a common tail cannot
  repair its two distinct site degrees.
- **W:** the old `Yw=W` cap supplies the output readout only.  Endpoint-even
  projection doubles an even W row; it does not force W to vanish.

Hence the smallest honest positive theorem is one endpoint-even
target-bearing source cell whose principal boundary is the **full** E14 unary
S-pair remainder minus the word-`01211222` carrier.  Its first proper face is
the mixed target cone, not another occurrence coefficient.  Anchor, q,
ridge, and W are downstream faces of that same totalization.

## Scope

This is exact for the canonical `h=3` E14 first-hit packet and the generic
order-two even Cartan target normal.  It does not construct `P2/iota`, turn
the surviving target-normal row into a global Fredholm terminal, handle the
`beta=0` special fibre, or prove the all-order comparison.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
fffc345f161fe4331f4a7c34e152a3c705f03273d069164a336ec66f384f9638
```
