# Axis-purified Hessian provenance produces a flat carrier circuit

## Outcome

Let an axis-purified star row have occupied site components

\[
                         p=\sum_{u\in U}\lambda_u e_i^{(u)}
\]

and hold the opposite two star rows and the genuine common quadratic `q`
fixed.  Write `C_u` for the complete pair of response tensors contributed
by `e_i@u`.  If the presentation has minimum site support, the `C_u` are
linearly independent.  Since

\[
              \sum_{u\in U}\lambda_u C_u=(X_i,0),       \tag{1}
\]

their images modulo the target line have rank `|U|-1`, and the coefficients
`lambda_u` give the unique full-support circuit.

The genuine common Hessian recurrence

\[
 (h-1)F_{uv}=\sum_{f\cap\{u,v\}=\varnothing}q_fG_{uv,f} \tag{2}
\]

turns every nonzero entry of this quotient circuit into a literal physical
`q_f G_{uv,f}` carrier.  It does **not** make an occupied `C_u` zero.  In the
axis-purified branch, an exchange between two components has two endpoint
arms on the same target line, so its endpoint Pluecker minor is zero.  Thus
(2) supplies a flat carrier circuit, not by itself a joint-kernel deletion
or a curved doubly-good OO witness.

The exact checker is
`computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py`.

## 1. Minimum support gives the quotient circuit

Suppose the occupied `C_u` were dependent.  A nonzero relation among them
could be added to the coefficients in (1); choosing its scalar so that one
occupied coefficient becomes zero would preserve both response tensors and
strictly reduce support.  Hence support minimality makes the columns
independent.

Their span has dimension `k=|U|` and contains the nonzero target in (1).
Quotienting that span by the target line therefore has dimension `k-1`.
The kernel of the quotient presentation is one-dimensional and is spanned
by `(lambda_u)`.  Every `lambda_u` is nonzero by definition of occupied
support, so this is a full-support circuit.

Consequently a nonzero axis-star self-square at a minimum representative
does not first appear as a hidden kernel component.  It appears as a
nontrivial circuit among mixed response tails.  Proving concentration means
killing this circuit with additional source rows, not reading a zero column
from Hessian symmetry.

## 2. Smallest genuine physical boundary

The committed affine guard gives the exact `k=2` realization.  On six
residual sites take

```text
q = 13:11 + 24:11 + 12:10 - 02:10 + 34:00,
s = e1@5,
p = e1@0 + e1@1.
```

This is an ordinary decorated quadratic.  The checker constructs all 15
first cofactors and all 45 symmetric second cofactors directly from `q` and
verifies all 15 identities (2), together with the complete top Euler
identity.  The occupied response columns are

\[
                         C_0=X_1+Y,\qquad C_1=-Y.         \tag{3}
\]

They have rank two.  Neither occupied site component lies in even the
one-row response kernel, hence neither can lie in the ambient joint kernel
after a second opposite row is added.  Their sum is the exact target `X1`,
and `p^[2]=e_1^{(0)}e_1^{(1)}` is nonzero.

The three source matchings are

```text
X1:  P0:11, Q5:11, 13:11, 24:11,
+Y:  P0:11, Q5:11, 12:10, 34:00,
-Y:  P1:11, Q5:11, 02:10, 34:00.
```

The two debt matchings differ on the literal alternating cycle

```text
P - 0 - 2 - 1 - P
```

and share `Q5` and `34`.  Both arms at `P` are multiples of the same target
line `e1`; the endpoint matrix has rank one and determinant zero.  This is
the first physical reason that a Hessian carrier is not automatically the
curved OO route.

## 3. Exact remaining recurrence

The physical boundary above is not a one-bad source: its unary top is zero,
and it omits the second-colour diagonal/crossed packet.  Those omissions are
load-bearing.  In a genuine one-bad packet, (2) is already automatic; the
new theorem must couple the flat quotient circuit to

```text
q^[h] = X0,
p_2 s_2 q^[h-1] = X2,
p_1 s_2 q^[h-1] = p_2 s_1 q^[h-1] = 0.
```

Equivalently, the next actual physical recurrence is the mixed
companion/cancellation-mate row which changes the flat internal carrier
into either a crossed endpoint arm or a source-valid relation among the
occupied columns.  Another contraction of (2), or an abstract Pluecker
identity among its symmetric `G` labels, only reproduces the carrier
circuit and cannot close it.

## Scope and verification

This is a coordinate-free minimum-support normal form and an exact physical
counterguard to a Hessian-only deletion/OO inference.  It is not a full
one-bad packet and does not refute a theorem using all five one-bad tensors.

Run

```text
python3 computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py
python3 -O computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py
python3 -I -S computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py
```

The frozen ledger digest is

```text
3b0c0bf757f76884a2f3ff068209c9ae207002eed1a9b63d129ddc82082fa22f
```
