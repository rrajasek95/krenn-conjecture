# Gate-I shared-repair source scope guard

The shared-repair anchor-fibre theorem in `8e1f858` is conditional in exactly
one place.  Its six multiplier-labelled pure ordinary-residue columns are an
explicit strengthening, not columns constructed in the physical relative
source.  The committed source inventory supplies one aggregate scalar
ordinary-residue column only.

The Cartan side is physical.  Commit `f746560` constructs the endpoint-odd
Cartan cell from source orbits, with ordinary residue

\[
(-1,+1,+1,-1)
\]

and zero protected `D/W/target/anchor/Eq` output in the canonical
endpoint-recoloured faces-`(3,5)` repeated grade.  Commit `271df91` places
that packet in the complete literal correction component.  All four repair
directions of `f59bbc6` are pure multiplier labels in this same homogeneous
component, so the bordered alternative has the required placed physical
Cartan column; it does not require four independently constructed Cartan
cells.

The pure-residue side is not yet physical labelwise.  Commit `d7ff17d` has
one `ores` row and one scalar pure-`ores` column in its nine-row clean
inventory.  Commit `c094bbb` likewise uses the coarse scalar symbol
`d_ores` in

\[
x=R-T-Y\rho+Yd_{\mathrm{ores}}.
\]

Neither result defines a section from this scalar row to the six pure
multiplier labels.  Even granting the strongest natural diagonal lift, the
diagonal together with the physical Cartan residue line has rank two and
contains none of

\[
B_1,\quad B_4,\quad \tfrac12(B_0+B_5),\quad
\tfrac12(B_2+B_3).
\]

Thus the sharp missing source statement is:

> In the canonical faces-`(3,5)` grade, construct two rho-equivariant
> relative source chains `d_fixed` and `d_pair` with zero
> `lower/W/target/ainc` output and labelled ordinary residue equal to one
> fixed direction (`B1` or `B4`) and one paired direction
> (`(B0+B5)/2` or `(B2+B3)/2`), modulo the already physical Cartan residue
> line.

Until those two chains are constructed, the formula
`x_v=R_v-T_v-rho_v+d_ores,v` is not source-typed.  Consequently
`U_v-x_v` is not yet a genuine `J0`-kernel element, and the otherwise exact
generator/separator dichotomy from `8e1f858` cannot be assembled into Gate I.
This is not a nonexistence theorem: the two sections may occur in a larger
relative source resolution.

## Reproduction

Run:

```text
python3 computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py
python3 -O computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py
python3 -I -S computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py
```

The frozen ledger digest is
`bdad46b583b0fcab4065314bf8bb957bd79b5b502e2e76680d438519857b671a`.
