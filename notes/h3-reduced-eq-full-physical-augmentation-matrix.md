# The placed Cartan packet physically completes the full odd alpha face

## Exact row solve

Separate all augmented coordinates in the canonical six-label component:

```text
lower_6, Eq_6, Yw_6, physical-W_6, target_6, ores_6,
ainc, eta/sigma_7, q.
```

For each multiplier label, write `B_i=r0_i-T_i` and let `rho_i` be the
split-residue column.  With

\[
 \alpha=(1,0,1,-1,0,-1),\qquad
 \tau=(1,1,1,1,1,1,-1),
\]

the placed endpoint-odd Cartan packet is

\[
 K_\alpha=(\operatorname{ores}=\alpha,
            \operatorname{terminal}=\tau),             \tag{1}
\]

with every protected row zero.  Direct substitution, with `Yw` and
physical `W` retained separately, gives

\[
 O_u=-B_u+\rho_u
   =(-u,-u,0,0,0,u,\sum u,0,0).                        \tag{2}
\]

Here the last entries are `(ainc,terminal,q)`.  A granted primitive anchor
column has

```text
ainc=-1, q=1,
```

not `q=0`: this is forced by the physical relation

\[
                 q+\sum_i\operatorname{lower}_i
                       +\operatorname{ainc}=0.          \tag{3}
\]

Consequently the anchor coefficient needed in (2) is `sum(u)`, and the
resulting physical `q` is also `sum(u)`.

The exact membership criterion is

\[
 \boxed{
 D(u,\zeta,q_0)\in\langle r_0,T,\rho,K_\alpha,A\rangle
 \iff
 u=c\alpha,\quad \zeta=-c\tau,\quad q_0=\sum u.}       \tag{4}
\]

Checker:
[`verify_h3_reduced_eq_full_physical_augmentation_matrix.py`](../computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py).

## The positive full-alpha conclusion

Taking `u=alpha` in (4) requires no primitive anchor because
`sum(alpha)=0`.  The identity is exactly

\[
                         O_\alpha-K_\alpha=-M_v.        \tag{5}
\]

Thus the committed physical cell `M_v=-O_alpha+K_alpha` already supplies
the complete **output-side odd projection** of the central reduced-Eq
cell.  Its literal lower boundary has 360 seven-edge features; its Eq
coefficient is `alpha`; ordinary residue, target, protected `W`, anchor,
and physical `q` vanish; and its eta/sigma packet is `tau` (with signs
reversed in (5)).

This materially shortens the odd/Interface-II frontier.  There is no
remaining output augmentation theorem for the selected full-alpha packet.
What remains is the input chain-map equation

\[
          J_3(M_v)=A J_{\rm col}(u_{024}-u_{012}),      \tag{6}
\]

or its occurrence-Hessian version.  The left side is the physical
360-feature boundary.  The completed sixteen-term Hessian symbol and
transpose groupoid do not expose the complete source-labelled right side.
The previously isolated private `xi` face is the first failure of the
direct constructor.  Hence (5) is a physical output cell, not by itself a
proof of (6).

## The residual primitive cokernel

The two rho-pair directions are

\[
 u_{05}=e_0-e_5,\qquad u_{23}=e_2-e_3,qquad
 \alpha=u_{05}+u_{23}.                                 \tag{7}
\]

Neither individual pair lies in `Q alpha`.  For `u05`, take
`w=e0+e3`; for `u23`, take `w=e2+e5`.  In both cases

\[
 w\cdot\alpha=0,\qquad w\cdot u=1.
\]

The primitive covectors

\[
 \lambda_w^{Y}=-\operatorname{Eq}_w+Yw_w
              +\operatorname{target}_w-\operatorname{ores}_w,\qquad
 \lambda_w^{W}=-\operatorname{Eq}_w+W_w
              +\operatorname{target}_w-\operatorname{ores}_w             \tag{8}
\]

kill every old cap, split-residue, placed-Cartan, and granted primitive
anchor column, but read one on the desired residue-zero dressing.  The same
test for the even direction

\[
                         v=(B_1+B_4)/2                 \tag{9}
\]

uses `w=e1+e4`.  Granting the primitive anchor family removes the old
`sum(lower)+ainc` obstruction for (9), with forced `q=1`, but leaves the
labelled-residue class untouched.  Therefore the exact remaining quotient
is still

\[
                         [u]\in\mathbb Q^6/\mathbb Q\alpha.                \tag{10}
\]

This independently confirms the signs and sharpens the conclusion of the
Koszul/Tate audit: the full alpha line is solved, while a single rho pair
or the even `B1/B4` direction needs another physically placed
Cartan/residue line.

## Separate `Yw` and physical `W`

A one-row model called `W` cannot by itself establish two different maps.
Keeping `Yw(rho_i)=e_i` while changing only physical `W(rho_i)` to zero
leaves every row of that collapsed model unchanged, but changes the
physical-W value of (5) by `-alpha`.  For the selected full-alpha packet
this ambiguity is removed by the committed `M_v` theorem, which directly
asserts protected physical `W=0` on the aggregate.  Any future construction
using an individual rho section still has to prove its columnwise physical
`W` typing; it cannot inherit it merely from a `Yw` boundary identity.

## Scope

The primitive-anchor column in (4) is a conditional source family; this
note proves its forced `q` value and the fact that it does not alter the
residue quotient.  The full-alpha conclusion is unconditional because its
anchor coefficient is zero and (5) is already source-provenant.  The note
does not construct (6), another Cartan orbit, the primitive anchor family,
or the missing pair/even labelled-residue sections.

Run:

```text
python3 computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py
python3 -O computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py
python3 -I -S computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py
```

Frozen ledger SHA-256 is
`4afd82854e324bfa9dba434600555b33e0b276b9f26af4a841a3996d04edf657`.
