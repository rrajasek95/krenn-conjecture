# The fixed and paired shared-loop repairs miss the full augmented image

## Exact finite problem

In the canonical `h=3`, faces-`(3,5)`, normalized `Y=1` grade, the complete
repeated component has 288 columns and rank 288.  Its six pure columns have
pairwise disjoint 90-term literal boundaries

\[
                         B_0,\ldots,B_5.
\]

Each has 45 or 46 features private against all 288 columns.  The two Gate-I
shared-loop orbits require one of

```text
fixed:  B1 or B4                         (90 literal features),
paired: (B0+B5)/2 or (B2+B3)/2          (180 literal features),
```

with all augmented `Eq`, `W`, target, `ainc`, labelled ordinary residue,
and the seven canonical eta/sigma rows zero.

The checker is
[`verify_h3_shared_loop_full_augmented_membership_dual.py`](../computations/verify_h3_shared_loop_full_augmented_membership_dual.py).
It retains the literal 90/360-term boundary data and uses the six private
pivots only for the final exact quotient certificate.

## Strong inventory search

The finite source envelope contains the actual `r0,T,rho` cap columns and
grants all 15 recorded `M_v` alpha signatures and all Cartan alpha signatures
with the terminal packet

```text
eta1_constant,...,eta5_constant = 1,
eta1_U1                          = 1,
sigma_qpq22                     = -1,
```

the endpoint bare-`Q` differences, and the scalar ordinary-residue column.
It is enlarged further by granting:

- six multiplier-labelled pure-residue sections, although only their scalar
  aggregate is physically constructed; and
- all 15 complete literal collision differences with protected rows zero.

Thus failure in this envelope implies failure in the smaller committed
inventory.  This is deliberately an overgrant: the separate repair-1 scope
audit shows that termwise Cartan/private/terminal physicality is not pinned
by the grade-forgotten order-six shadow.  The negative result therefore does
not depend on treating those recorded signatures as constructed columns.
The exact Hasse product rule does produce the correct fixed and
paired directions at occurrence level, but its order-three carrier is not a
source column: it lies first in word `222000`, its rho mate is in a
complementary word, and the formal totalization has `ainc=-1` plus the
endpoint/Omega defects.  The order-six Spencer/Cartan alpha packet has
augmentation zero and does not change the calculation.

## Primitive physical dual

Let `private_Bi` denote the oriented mapping-cone coordinate selected from
the literal boundary of `B_i`.  Then

\[
                  \nu=\sum_{i=0}^{5}\operatorname{private}_{B_i}
                       +\operatorname{ainc}                         \tag{1}
\]

kills every column in the enlarged augmented envelope, including the
eta/sigma-bearing `M_v` and Cartan columns.  With the lower boundary oriented
as minus the literal matching row, (1) is `-Lambda`, where the pinned
first-flat theorem constructs the physical covector

\[
                  \Lambda=\sum_i m_i-\operatorname{ainc}.
\]

Every normalized fixed or paired target has value one under `nu`.  Adjoining
any one of the four targets raises the exact reduced rank by one.  Hence none
is an image of the known physical/product-rule/Spencer/third-Bianchi
inventory.

## Smallest missing column

After granting the unproved labelwise pure-residue sections, the strongest
old near-hit for a normalized target vector `u` is

\[
 x_u=R_u-T_u-\rho_u+d_{\mathrm{ores},u}.
\]

It has the desired literal `B_u`, but retains

```text
Eq   = u,
ainc = -1.
```

Therefore the smallest remaining correction is exactly

```text
literal boundary = 0,
Eq                = -u,
ainc              = +1,
W,target,ores,eta/sigma = 0.                         (2)
```

Without the granted residue sections, (2) must also cancel the corresponding
labelled residue.  No currently physical product-rule or third-Bianchi cell
has (2): the formal Hasse tail has the opposite anchor sign and is not
source-valid.

This is also the sharp generator/separator interface.  A future relative
column with nonzero `nu` pairing is the physical relative-generator branch;
if every new column is killed by `nu`, the same covector descends as the
bounded Fredholm separator.  The statement is exact for the named canonical
inventories and does not claim to annihilate arbitrary future higher cells.

## Verification

```text
python3 computations/verify_h3_shared_loop_full_augmented_membership_dual.py
python3 -O computations/verify_h3_shared_loop_full_augmented_membership_dual.py
python3 -I -S computations/verify_h3_shared_loop_full_augmented_membership_dual.py
```

Frozen ledger SHA-256:

```text
da3a04511fb4695bf6921c47be2b20d017823a8fc01a3057c9daa462424ccd5f
```
