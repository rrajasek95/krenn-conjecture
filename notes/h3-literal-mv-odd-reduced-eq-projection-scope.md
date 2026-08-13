# The physical `M_v` column closes the odd Eq output, but not its input comparison

## Result

The already constructed physical cell

\[
                         M_v=-O_\alpha+K                 \tag{1}
\]

is exactly the odd physical **output dressing** of the central reduced-Eq
cone on the normalized canonical `h=3` slice.  Its signs and all exposed
augmented rows match.  The remaining odd issue is not another Eq cell: it is
the input-side Cartan--Spencer comparison, equivalently physical `q`
transport.

Put

\[
 \delta=(1,-1,-1,1),\qquad
 \alpha=-\delta=(-1,1,1,-1).                           \tag{2}
\]

The underived Gate-I cap packet has

```text
O_alpha:
  literal boundary   -sum_j alpha_j B_j
  Eq                  -alpha = delta
  labelled ores       +alpha
  D,W,target,ainc     0.
```

Commit `271df91` proves that (1) has

```text
M_v:
  literal boundary   +sum_j alpha_j B_j     (360 features)
  Eq                  +alpha = -delta
  labelled ores       0
  D,W,target,ainc     0
  eta_z               1+delta_(vz) u_z/t
  sigma               -q_pq^22.
```

Therefore

\[
       J_{\rm private/Eq}(O_\alpha+M_v)=0               \tag{3}
\]

coefficient by coefficient.  The Eq sign in (3) is precisely the sign
needed to cancel the odd cylinder's underived residual.  This is not a
coarse occurrence equality: `M_v` carries the complete 360-feature private
boundary forced by the literal full-nine rows.

The source word and grade also agree exactly:

```text
word       1211222 after deleting the distinguished endpoint
grade      canonical labelled repeated P3+K2 /
           endpoint-recoloured faces-(3,5) bridge.
```

Thus no new odd reduced-Eq output generator is needed.  The generic even
projection and beta-special Bockstein are not obtained: they require the
other parity of a regular `rho` orbit and its integral family.

## 1. What is closed

The central cone separated three questions which had previously been mixed.
For the odd canonical packet, (1) now answers the first two.

1. **Does a physical source column carry the correction `-delta E`?** Yes.
   Its Eq entries are `alpha=-delta`.
2. **Can that correction be dressed without labelled residue, target, `W`,
   or anchor leakage, while retaining the endpoint terminal?** Yes.  The
   cap residue in `-O_alpha` cancels the physical Cartan residue in `K`, and
   `K` supplies exactly the objectwise eta/sigma ridge.
3. **Is this output column the image of the selected collision lower chain
   under a complete physical comparison?** Not yet proved.

The first two statements are what “odd physical output cell closed” means.
They are enough to remove construction of an odd Eq column from the central
theorem.  They do not make the whole Gate-I chain map automatic.

## 2. The exact remaining row

The selected marked lower vector is

\[
                         \ell=u_{024}-u_{012}.          \tag{4}
\]

The complete output census and twelve-label occurrence collapse pick (1)
as its unique candidate, but the required chain equation is still

\[
                  \boxed{J_3(M_v)=A J_{\rm col}(\ell).} \tag{5}
\]

The left side of (5) is completely exposed: 360 private features, four Eq
entries, zero labelled residue and protected rows, and the eta/sigma ridge.
Only the occurrence projection of the right side is exposed.  The first
undefined comparison face is the pinned coefficient-prolongation monomial
`xi`, detected by

\[
                         \lambda_\xi={3\over4}e_\xi^*.  \tag{6}
\]

Equivalently, the missing square is

\[
                         \Pi_1d_{\rm PP}=d_{\rm corr}\Pi_0 \tag{7}
\]

on this first relative Spencer face.  Polynomial Cartan naturality does not
define the comparison functor `Pi` between these two physical complexes.

## 3. Physical `q`: output terminal versus transport

There are two distinct statements called “residual `q`” in the surrounding
maps.

The output terminal packet is closed: `M_v` carries the exact objectwise
eta/sigma laws, and the existing six-term theorem gives the
generator-or-zero-indeterminate alternative on that physical output.

But the `271df91` augmented module has rows

```text
private, Eq, W, target, labelled residue, ainc, eta, sigma
```

and no input comparison row for physical `q`.  Transport across the grade
cylinder is the separate quotient condition

\[
 o_q(\Phi)=[q_{xv}\Phi-q_{pq}]=0
       \quad\text{in }D_{pq}^*/\operatorname{row}(J_{pq}). \tag{8}
\]

Vanishing in (8) constructs the augmented `q` homotopy; nonvanishing gives
the protected-kernel generator once both rows are physical.  Either branch
requires the comparison `Phi`, and for the selected chain its construction
is exactly (5).  Hence `M_v` does not have a wrong `q` value—the transport
row is absent from its theorem.

This is the single scope correction needed when composing `271df91` with
the central cone:

```text
odd reduced-Eq physical output cell                CLOSED
odd selected input comparison / physical q        OPEN: one equation (5)
generic even physical rho orbit                    OPEN
beta-special integral Bockstein projection         OPEN.
```

## Scope and verification

The output identification is on the explicitly normalized `Y=1` canonical
slice.  No general-`Y` scaling is asserted.  This note does not weaken the
physical Cartan construction or the terminal theorem; it prevents their
output-side membership from being mistaken for the input chain-map equality.

Run

```text
python3 computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py
python3 -O computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py
python3 -I -S computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py
```

All modes print ledger digest
`8bc87fa4289fe08f15649a9c127d0c0e815f6d9127399015a980d3d2876ebc96`.
