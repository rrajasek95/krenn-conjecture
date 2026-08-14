# Full unsigned shears close algebraically but are only relative KS curvature

## Verdict

The proposed unsigned augmented-vertex pair has exact and unexpectedly
clean coefficient algebra.  Let

```text
X : 0 -> S on every incident off-diagonal edge,
Y : S -> 0 on every incident off-diagonal edge.
```

On the complete `K8` hafnian response `R`,

\[
 X(R)=C_{0,S},\qquad Y(R)=C_{S,0},                    \tag{1}
\]

where each `C` is the symmetric 45-term collision row with coefficient two.
Their complete first-PP boundaries are natural, and the two orders satisfy

\[
 YX(R)=XY(R)=2\bigl(R-s_0\partial_{s_0}R\bigr).       \tag{2}
\]

The right side of (2) is already in the complete-response plus coordinate-
Euler span.  On the selected chart `A=Dq01`, both orders give `A+B`.

Nevertheless this is **not an absolute physical source construction**.
`P,S` are operation/head roles, not physical GHZ tensor sites.  The full
physical coefficient inventory is squarefree and projects identically to
zero in the missing-`0`/doubled-`S` collision degree.  Thus (1) is the
curvature of an augmented-role shear.  It is only a KS/tangent face unless a
new non-diagonal Spencer generator is adjoined.

Exact checker:
[`verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py`](../computations/verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py).

## 1. First face and PP completion

The projected shear sends an edge `0j` to `Sj`.  It sends `0S` to zero,
because the unprojected congruence action would create the absent loop
`SS`.  Of the 105 perfect matchings, 90 do not contain `0S`.  Their images
collect two-to-one onto 45 collision monomials, giving coefficient two.

Every term has operation degree

```text
(1,2,0,1,1,1,1,1) in the order P,S,0,1,2,3,4,5.
```

This is disjoint from the squarefree physical degree `(1,...,1)`.

There are exactly 180 first-PP flags.  The identity

\[
                         d(XR)=X(dR)                  \tag{3}
\]

holds literally, provided `X` acts both on retained factors and on the
removed-edge/Kähler label.  If the varied `0j` edge is itself removed, the
right side contains `d(0j)->d(Sj)`; omitting this reinsertion term would
give a false PP failure.

The 180 flags split as

```text
6 complete unary-cofactor groups,       15 flags each,
15 complete repeated-edge groups,        6 flags each.
```

Thus the complete collision inventory fully classifies every PP descendant.
It does not turn `C_(0,S)` into an old physical boundary.

## 2. Exact second order

Apply the opposite shear to one collision monomial.  It may move either of
the two edges incident to doubled `S`.  One move returns the original
matching; the other makes its four-cycle partner.  Summed over the complete
response, the partner involution gives every matching not containing `s0`
twice.  Hence (2).

In the 105 matching-occurrence coordinates, let `E_s0(R)` be the 15-term
indicator of matchings containing `s0`.  Then

```text
YX(R)=XY(R)=2R-2E_s0(R),
rank(R,E_s0)=2,
rank(R,E_s0,YX(R))=2.
```

So the second-order response debt closes by the old response row and the
constant logarithmic coordinate Euler row.  This is a genuine positive
identity.  It also explains the selected return:

\[
                   YX(A)=XY(A)=A+B.                  \tag{4}
\]

For the analogous `1<->S` pair, (4) becomes `A+C`.

## 3. Why second-order closure does not authorize the path

The obstruction is at first order.  The exhaustive full-word degree audit
proves that every physical decorated coefficient generator is squarefree
and has zero projection to `C_(0,S)`.  Differentiating the response by an
external augmented-role vector field proves that `C_(0,S)` is a tangent
curvature; it does not prove that it is a boundary in the fixed source
presentation.

The smallest linear models make the distinction explicit:

```text
absolute declaration       d kappa = C       gives H0: 1 -> 0,
presentation-safe graph    d kappa = C - t   gives H0: 1 -> 1.
```

The second formula retains a carrier `t`.  Equation (2) describes its
ordered image modulo response/Euler rows, but supplies no absolute boundary
for `t`.

Nor does taking an even product repair the target typing.  Even products of
sitewise physical Weyl actions may fix GHZ.  Here `P,S` label response-head
operations; they are not sites and there is no induced GHZ transvection to
multiply.

## 4. Sharp criterion

The unsigned route becomes positive under exactly one new hypothesis:

> There is a source-labelled non-diagonal Spencer/Tate generator with
> absolute boundary `C_(0,S)`, all 180 PP/reinsertion flags, and the complete
> target, Eq, `q`, anchor, `W`, ordinary-residue and ridge boundary.

Under that hypothesis, the PP boundary is already classified and (2) closes
the response/Euler second order; the two selected orders give the desired
`A+B` and `A+C` switches.

Without it, the unsigned construction is a particularly clean relative
carrier, not a proof.  It bypasses the signed 24-term residual algebraically
but does not bypass source authorization.

## Verification

Run

```text
python3 computations/verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py
python3 -O computations/verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py
python3 -I -S computations/verify_h3_unsigned_augmented_vertex_shear_authorization_gate.py
```

The checker reconstructs the complete `K8` response, both collision faces,
the Kähler PP action, the ordered second return, the Euler-span rank, and the
selected `A+B` identity using exact rational arithmetic.
