# The reduced-Eq/cap factorization does not lift through private source rows

## Exact factorization

At the level of the augmented cap quotient, the residual-q
Kodaira--Spencer target factors through the reduced-Eq face.  The factorization
is exact, but literal private matching-boundary rows prevent promoting it to
a physical source chain.  In one fixed endpoint orientation and tail corner,
use
the augmented row order

\[
 (\operatorname{Eq},\operatorname{ainc},W,
   \operatorname{tgt},\operatorname{ores}).
\]

The existing pure row and cap columns are

\[
 r_0=(1,-1,0,1,0),\quad
 T=(0,0,-1,1,0),\quad
 \rho=(0,0,1,0,1).
\]

The zero-anchor reduced-Eq face isolated by the collision audit has

\[
 C=(-1,0,0,0,0).
\]

Consequently

\[
 \boxed{K=-r_0+T+\rho-C=(0,1,0,0,1).}                 \tag{1}
\]

The coefficients in (1) are unique.  The old three-column block has rank
three, adjoining \(C\) raises it to four, and the primitive covector
\(\operatorname{Eq}+\operatorname{ainc}\) kills the old block while reading
\(-1\) on \(C\) and \(+1\) on \(K\).

Thus, **if the four columns really occur in the same labelled physical
grade**, a reduced-Eq face combines with the old cap block to give a cell
with zero Eq, \(W\), and target, and with one unit each of physical anchor
incidence and ordinary residue.  This quotient calculation does not yet
include the \(E_\pm,\Omega,q_{\rm comp}\) boundary rows.

## The endpoint-odd aggregate cancels the anchor

Keep the four residue corners separately in the order

```text
P+q00, P-q00, P+q11, P-q11.
```

The correction required by the curvature/bar near-hit is

\[
 -\delta=(-1,1,1,-1).                                \tag{2}
\]

Take the same linear combination of four copies of (1).  Since the
coefficients in (2) sum to zero, their anchor incidences cancel.  Eq, \(W\),
and target already vanish cornerwise, while the four labelled residue
coordinates remain exactly (2).  Hence the result has

```text
main boundary = 0,
W = target = ainc = 0,
ordinary residue = -delta.
```

Conversely, uniqueness in the one-corner calculation forces the reduced-Eq
coefficients to be

\[
 (1,-1,-1,1).
\]

Therefore, in the cap quotient and conditional on the same-grade lift,
the residual-q residue class is **equivalent** to the endpoint-odd
reduced-Eq aggregate

\[
 C_{P+q00}-C_{P-q00}-C_{P+q11}+C_{P-q11}.             \tag{3}
\]

This gives the only possible way the proposed new cell can escape the
standard graph law \(R=D\): the escape must come from the separated reduced
conormal face.  It does not prove that the physical main-boundary coordinate
\(D\) vanishes.

## Why the quotient factorization does not lift

The five displayed rows are a quotient of the literal matching-boundary
module.  The pure row \(r_0\) is not merely its five-coordinate signature:
in the complete repeated-degree full-nine module it has at least 42 literal
matching monomials owned by no other row/multiplier column.  Retain one such
private coordinate.  Then

\[
 r_0^{\rm lit}=(1,-1,0,1,0;1),
\]

while the projected \(T,\rho,C\) and desired \(K\) have private coordinate
zero.  The covector

\[
             \operatorname{ainc}+\operatorname{private}             \tag{4}
\]

kills \(r_0^{\rm lit},T,\rho,C\) and reads one on \(K\).  Equivalently,
the four old/projected columns have rank four and adjoining \(K\) raises the
rank to five.  Thus (1) ceases to be an identity as soon as one literal
private boundary row is restored.

This is a structural counterguard, not an arbitrary extra coordinate: the
complete full-nine audit proves injectivity using precisely these private
pivots.  In four tail corners the forced coefficients leave four distinct
private residues \((1,-1,-1,1)\), so endpoint-odd summation does not cancel
them.

For a general cap parameter \(Y\), there is another qualification.  With
\(T=(0,0,-Y,1,0)\), the forced coefficients give ordinary residue \(Y\),
not one.  The displayed quotient formula is therefore normalized at \(Y=1\);
a general construction also needs a source-valid normalization or a separate
pure-residue correction.

Consequently (3) is an equivalence only inside the normalized five-row cap
quotient.  An arbitrary higher Kodaira--Spencer cell need not factor through
the projected \(C\), and the quotient computation cannot be reversed.

## Source typing and the remaining physical datum

Equation (1) is to be used independently in each literal corner.  All four
terms \(r_0,T,\rho,C\) must be multiplied by the **same** endpoint orientation,
decorated tail, complementary matching, and incident-cycle factor in the
labelled repeated \(P_3\sqcup K_2\) grade.  No multiplication by \(t-u_v\),
no mixing of unequal multidegrees, and no relabelling of source words is
being used.  This avoids the direct-product obstruction in the one-cell
fiber-product audit.

The factorization does not construct \(C\).  A positive relative cell must
carry the negative of the private full-nine boundary just exposed, rather
than only the projected reduced-Eq coordinate.  Moreover, physical promotion
still requires the comparison terminal laws

\[
 dr_v(\eta_z)=-d\Omega_v(\eta_z)
       =1+\delta_{vz}u_z/t,\qquad
 \sum_v dr_v(\eta_z)=5+u_z/t,                         \tag{5}
\]

and the additional facewise stabilizer correction \(-q_{pq}^{22}\).  These
values must be carried by the same physical reduced-Eq/comparison family;
the scalar affine primitive does not supply them.

The exact frontier is therefore:

> Construct one relative cell in the exact word `1211222` and labelled
> repeated grade which cancels the complete private matching boundary of the
> pure row, realizes the endpoint-odd reduced-Eq/residue correction, and
> carries the eta/sigma terminal comparison.

Conditional on that stronger construction, `2593831` closes the unequal-tail
five-lock and E14 endpoint holonomy and decreases the typed-component
potential.  Transverse four-good rank remains a later theorem.

This is an exact quotient factorization and an exact obstruction to lifting
it through the pinned literal module.  It is not a physical construction and
not a proof of Krenn's conjecture.

Run:

```text
python3 computations/verify_h3_residual_q_reduced_eq_cap_factorization.py
python3 -O computations/verify_h3_residual_q_reduced_eq_cap_factorization.py
python3 -I -S computations/verify_h3_residual_q_reduced_eq_cap_factorization.py
```

Frozen ledger SHA-256:

```text
ed2be2dd157747104cf454b0062a6818689aa0562cc6484171e0f90aa52b9b88
```
