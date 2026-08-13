# The literal residual-q image is an old cap plus the physical Cartan cell

## Result

On the normalized canonical `h=3` slice (`Y=1`), the complete desired
mapping-cone image is already physical.  Put

\[
 \alpha=(-1,+1,+1,-1),\qquad
 O_\alpha=\sum_j\alpha_j(-r_{0,j}+T_j+\rho_j).
\]

The old cap cells give

```text
O_alpha: literal B boundary = -sum alpha_j B_j
         Eq                = -alpha
         ordinary residue  = +alpha
         D,W,target,ainc    = 0.
```

Let `K` be the source-provenant endpoint-odd Cartan/HPL cell in the same
canonical labelled repeated `P3+K2` grade.  Its augmented signature is

```text
literal source output      = 0
D1 / first Spencer output  = 0
ordinary residue           = +alpha
protected D,W,target,ainc,Eq = 0
terminal                   = the -dOmega_v eta/sigma ridge.
```

Consequently

\[
                         M_v=-O_\alpha+K
\]

has literal boundary `+sum alpha_j B_j`, Eq row `+alpha`, zero ordinary
residue and protected rows, and exactly the required eta/sigma terminal.
This is the full output-side image required by the residual-q mapping cone.

Checker:
[`verify_h3_literal_mv_cap_cartan_composition.py`](../computations/verify_h3_literal_mv_cap_cartan_composition.py).

## Literal, not coarse, private cancellation

The four old cap summands are actual `r0,T,rho` source cells.  The complete
fine-degree census checks all five components and all fifteen choices of
four of the six pure corners in each component.  Every `-O_alpha` boundary
has 360 distinct literal terms; the 75 aggregates have distinct digests.

The claim that `K` contributes no private row is not the zero entered in the
older 32-row coarse probe.  It is the exact order-six statement that the
8580-column bounded physical operator has zero literal source output and
zero `D1`/first-Spencer transfer.  Its `D2` value is the required
`-delta=alpha`.  Physical source-orbit descent then realizes that operator
as a genuine Cartan cell, and the ridge theorem identifies its terminal.

Thus no presentation-only chart difference, free ULTRA unit, or unproved
private cancellation enters the construction.

## Normalization and scope

This theorem uses the clean-cap normalization `Y=1`.  A general-`Y` formula
would require rederiving the cap coefficients and is not asserted here.
It also does not construct the input comparison from the 15 physical
collision labels.  Gate I has therefore narrowed to a single input-side
problem: absorb the complementary word packet of the overlapping-root odd
Cartan prism (or construct the equivalent protected comparison `Phi`).

No inactive normal-grade or diagonal-Rees extension follows from this
canonical output construction.

## Verification

Run:

```text
python3 computations/verify_h3_literal_mv_cap_cartan_composition.py
python3 -O computations/verify_h3_literal_mv_cap_cartan_composition.py
python3 -I -S computations/verify_h3_literal_mv_cap_cartan_composition.py
```

```text
84904cfd9f434eb8ff36548a0b2e0b2e68b8ec562c6559a89acdefb94500eb64
```
