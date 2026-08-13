# Selected lower: the first full-row Spencer discrepancy

Commit `6fd2412` leaves one equation:

\[
 J_3(M_v)=A\,J_{\mathrm{col}}(u_{024}-u_{012}).                 \tag{1}
\]

The pinned left-side theorem reports 360 literal seven-edge features, zero
ordinary residue and zero `D/W/target/ainc`, together with the required eta
and sigma laws.  The right side is not yet a complete source-labelled row.
The selected occurrence/collapse projection alone does not define it.

This note identifies the first exact obstruction in the closest committed
attempt to build that row from the complete tangent--Hasse tower.  It does
not assert that (1) is impossible.

## The direct construction reaches the right secondary class

The order-six first-flat lift is source closed, has zero first Spencer
transfer, and has secondary shadow

\[
 D_2=-\delta=(-1,+1,+1,-1).
\]

That is the grade-forgotten residue class required by the selected lower.
Endpoint recolouring also produces two individually source-closed fine
components in one total source-module degree.  However, the two components
are not a coefficientwise physical source endomorphism: their extraneous
fine faces cancel only after the missing chart-nondiagonal relative gluing.

## A one-coordinate obstruction occurs immediately

On the second fine component, product 2 and direction `37:11`, the first
coefficient-prolongation face contains the singleton

\[
 \xi={4\over3}
 q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{35}^{12}q_{67}^{22}.       \tag{2}
\]

The nonmembership proof is literal.  The fine degree of (2) is doubled
only at sites 3 and 7.  Consequently a quartic complete row times one
decorated edge can have this degree only in the following two ways:

```text
word 01211222, multiplier q_37^11
word 01211221, multiplier q_37^12
```

Each resulting column has 90 monomials, and every monomial contains the
physical edge `37`.  The monomial in (2) contains no `37` edge.  Therefore

\[
 \lambda_\xi={3\over4}e_\xi^*
\]

vanishes on the entire compatible homogeneous full-row block and reads
one on (2).  This is a primitive coordinate dual, not merely a rank or
coarse-shadow mismatch.

## What the discrepancy proves

The current direct Cartan--Spencer construction cannot be declared to be
`J_col(l)`: it stops before the 360-feature comparison, at the private face
\(\xi\).  The smallest missing datum is a chart-nondiagonal relative
Spencer generator whose boundary contributes \(-\xi\) in this exact
word/fine/repeated grade, together with its transported mate and the
protected augmented rows.  After that correction, the remaining faces and
then the literal 360-feature equality still have to be checked.

The conclusion is deliberately local.  Since the complete
`J_col(u_024-u_012)` has not been defined, \(\lambda_\xi\) is not a dual
separating every possible right side of (1).  It separates the first face
of the committed direct constructor from every old complete homogeneous
full-row column.

## Relation to the external repair-1 probe

The unaudited repair-1 calculation agrees that the grade-forgotten
secondary shadow is the physical `K` shadow.  Its raw fine decomposition
has supports `39/24`, whereas one chosen physical `K` representative has
word supports `10/10`; it also finds a 153-dimensional nonphysical
coordinate image for the *whole* constrained operator module.

Those are not selected-line separators.  The `39/24` split belongs to one
raw operator representative and may change under precisely the missing
relative gluing, while the 153-dimensional result obstructs a uniform map
on the whole operator kernel rather than this one vector.  The coordinate
\(\lambda_\xi\) above is the committed, exact obstruction relevant to the
direct selected-line construction.

The same probe also finds seven dimensions of physical `K` freedom after
all currently committed coarse readouts.  This is an independent warning
on the *left* side of (1): a termwise construction of `H_w`, or literal
private full-row/triple-cell readouts in the corner grade, is still needed
to pin the declared `K` half of `M_v`.  It does not alter the coordinate
nonmembership proof for \(\xi\).

## Reproduction

```bash
python3 computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py
python3 -O computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py
python3 -I -S computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py
```

The checker pins the `6fd2412` one-chain theorem, the endpoint-recoloured
source theorem, the secondary-transfer interface, the physical `M_v`
construction, and the literal direct-free full-row constructor.
