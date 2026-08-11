# The diagonal aggregate unit has no ordered 01/10 linear defect

## Result

The exact 34-row identity from
`n8-lemma-e-unary-top-diagonal-aggregate-identity.md` extends unchanged
through one arbitrary ordered `01` or `10` internal coordinate.  This holds
on every one of the fifteen residual physical pairs, including selected
anchor edges.

More precisely, let `I_diag` be the pinned 71-row source ideal in the 45
colour-diagonal variables, let

\[
 T=F_{01}(1111)F_{23}(2222)H(000000),
 \qquad T=\sum_{r=1}^{71}m_r g_r                         \tag{1}
\]

be its exact 34-nonzero-multiplier lift, and adjoin one coordinate
`x=q_uv^(01)` or `q_uv^(10)`.  Write the same labelled source coefficients
as

\[
                         g_r(x)=g_r+x\,\dot g_{r,x}.     \tag{2}
\]

Literal expansion gives the stronger polynomial identity

\[
                  \sum_r m_r\dot g_{r,x}=0              \tag{3}
\]

for all 30 choices of `(uv,01/10)`.  Hence the original multipliers, without
any correction, satisfy

\[
                         T=\sum_r m_rg_r(x).             \tag{4}
\]

Thus the one-cell chart has an ordinary source-row unit over `QQ[x]`; the
coefficient of `x` does not merely vanish in a quotient.  Singular returns
the same 251-element standard-basis size, the same 34 nonzero multipliers,
and the same lift digest as in the diagonal identity for every probe.

Checker:
[`verify_uniform_diagonal_aggregate_offdiagonal_first_correction.py`](../computations/verify_uniform_diagonal_aggregate_offdiagonal_first_correction.py).

## Source-labelled calculation

The checker reconstructs the original fine token sets and all 71 labelled
rows.  For a row on vertices `V` and output word `w`, the derivative in the
ordered cell `x=q_uv^(ab)` is exactly

\[
 \dot g_{r,x}=
 \begin{cases}
 \operatorname{haf}(q_w|_{V\setminus\{u,v\}}),
       &u,v\in V,\ (w_u,w_v)=(a,b),\\
 0,&\text{otherwise}.
 \end{cases}                                             \tag{5}
\]

This retains the ordered endpoint colours, the holes of each cofactor row,
and top-versus-response provenance.  Substituting (5) into the frozen
34-row lift yields zero as a literal polynomial for every physical pair and
both orientations.  The checker separately rebuilds each 46-variable
one-cell ideal, asks for a lift of `T`, and verifies its expansion exactly.

The census is

```text
ordered probes                         30
identically zero raw first corrections 30
zero quotient classes                  30
exact one-cell source units             30
standard-basis size in every chart     251
nonzero source multipliers in every     34
```

## Consequence for the remaining lock branch

The common-provenance boundary `746d5df` showed that the full four-response
packet can carry a one-sided crossed lock, while its unary top is the sole
missing row.  The present identity proves that adding one ordered `01/10`
cell—on an anchor edge or elsewhere—cannot attach that unary row: it leaves
the same ordinary unit (4).

Consequently a surviving off-diagonal completion needs filtration degree at
least two.  If one of those cells lies off the selected anchor multigraph,
the pinned nonanchor reselection theorem supplies the transverse active
rank-`(3,3)` arm.  After that routing, the genuinely new boundary is at least
two simultaneous ordered off-diagonal decorations supported on selected
anchor edges.  Their matching products are quadratic filtration terms and
are not addressed here.

## Scope

This theorem uses the concentrated ordered spokes `(p1,s1)=(0,1)` and
`(p2,s2)=(2,3)` and the same 71 compatible source rows as the diagonal
aggregate identity.  It covers an arbitrary coefficient in one `01` or
`10` internal coordinate at a time.  It does not cover two simultaneous
off-diagonal coordinates, the `02/20` or `12/21` filtrations, multisite
endpoint stars, or prove the full one-bad reduction.

Run

```sh
python3 computations/verify_uniform_diagonal_aggregate_offdiagonal_first_correction.py
python3 -O computations/verify_uniform_diagonal_aggregate_offdiagonal_first_correction.py
python3 -I -S computations/verify_uniform_diagonal_aggregate_offdiagonal_first_correction.py
```

The ledger digest is

```text
ae8e1687db2e12237528a64e8c92c74e5f3b4b1b6528e387725448f4edfc1bcc
```
