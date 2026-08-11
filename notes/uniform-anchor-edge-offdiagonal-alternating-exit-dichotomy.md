# A repaired decorated anchor has only a two-neighbour active escape

## Result

Choose nonzero pure target matchings `Q_0,Q_1,Q_2`.  Let `e=vu` be an
edge of `Q_c` carrying a nonzero off-diagonal internal cell `q_u`, and let
`Q_c'` be a second nonzero pure-`c` matching which avoids `e`.  The component
of `Q_c triangle Q_c'` through `e` is exactly the alternating repair cycle
needed to preserve the colour-`c` target when `e` is selected as a direct
physical pair.

The target-augmented private-site identity supplies

\[
 q_u+\sum_{s\ne u,v}\Delta_{us}C_s=0.                \tag{1}
\]

Since `q_u!=0`, some literal product `Delta_us C_s` is nonzero.  If

\[
 e\notin Q_d\quad\hbox{and}\quad vs\notin Q_d
       \qquad(d\ne c),                                \tag{2}
\]

then matching reselection gives the desired physical landing:

* select `Q_c',Q_d,Q_e` on the decorated pair `e`; and
* select `Q_c,Q_d,Q_e` on the active companion pair `vs`.

All three selected matchings avoid the relevant deleted pair in each line,
so all four deleted-star ranks are three.  The nonzero determinant
`Delta_us` says precisely that the two centre heads are distinct, while
`C_s!=0` makes the companion active.  No source coefficient is changed.

Thus the decorated-anchor escape of `746d5df` has the exact incidence
reduction

\[
 \boxed{\text{four-good active arm exchange}\quad\text{or}\quad
 \begin{array}{l}
 e\text{ is used by another selected colour, or}\\
 \operatorname{supp}(\Delta C)\text{ lies on the at most two}\\
 \text{other-colour anchor neighbours of }v.
 \end{array}}                                         \tag{3}
\]

Checker:
`computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py`.

## Why the rank repair is source-valid

For a deleted pair `ab`, a pure matching `Q_d` which avoids `ab` supplies
at endpoint `a` the literal coordinate column `(Q_d(a),d)`.  The three
colour labels make these columns independent even if two physical
neighbours coincide.

On `e`, the repaired matching `Q_c'` replaces the lost `Q_c` column.  If
`e` is absent from the other two target matchings, the selected triple
`(Q_c',Q_d,Q_e)` gives ranks `(3,3)`.  On `vs`, the original `Q_c` avoids
that pair because it uses `vu`; if `vs` is absent from the other two target
matchings, `(Q_c,Q_d,Q_e)` gives ranks `(3,3)`.  These are already nonzero
source monomials, so this is only a change of selected witnesses.

The direct decorated cell and (1) put the first pair in the exact
target-augmented active-minor route.  For the chosen `s`, the actual
transition minor and common cofactor are both nonzero.  Hence the arm pair
`vu,vs` is shared, distinct-head, active, and four-good.

## The finite obstruction is concentration, not pair type

Assume `e` is used only by `Q_c`.  At the centre `v`, each of `Q_d,Q_e`
blocks exactly one possible companion neighbour.  Therefore among the
`N-2` possible sites `s`, at most two are trapped and at least

\[
                              N-4                         \tag{4}
\]

are free.  Equation (1) closes the branch unless **every** nonzero
`Delta_us C_s` is concentrated on those one or two trapped neighbours.
This is the complete incidence dichotomy, rather than another list of
physical pair types.

At `N=8`, fixing `Q_c`, `e`, and its endpoint leaves `90` possible repair
matchings and `105^2` ordered choices of the other target matchings.  The
complete `992,250`-configuration audit gives

```text
multiply-used decorated anchor                       263250
unique anchor with four free possible active sites  607500
unique anchor with five free possible active sites  121500
```

The first alternating exit of `Q_c'` is free in `506,250` configurations
and trapped in `222,750`.  Those counts are diagnostic only: the theorem
uses whichever product in (1) is actually nonzero.

## Why the alternating exit alone is insufficient

The nonzero pure matching `Q_c'` makes its exit cofactor nonzero, but it
does not force the corresponding transition minor.  The checker freezes
the exact scalar guard

```text
p_u=q_u=p_exit=q_exit=C_exit=1,       Delta_exit=0,
p_trap=0, q_trap=-1, C_trap=1,        Delta_trap*C_trap=-1.
```

It satisfies `q_u + sum Delta*C = 0`, while the only active product lies on
an edge selected by another target colour.  Hence matching incidence, both
diagonal targets, and one alternating repair do not themselves force the
repair exit to be active.  The next source theorem must rule out this
one/two-neighbour concentration or provide an alternate target matching
for the trapped colour.

If `e` belongs to another selected target matching, one repair `Q_c'`
likewise restores only colour `c`; the displayed selected data guarantee
rank two on `e`.  A second target-colour repair or a source unit is then
indispensable.

These rank-two statements are guarantees from the selected monomials, not
claims about the complete source stars.  Extra source columns may raise the
ranks, and doing so is precisely a source-valid arm exchange beyond the
current incidence packet.

## Coefficient closure of the quadratic concentrated chart

The independent exact lift `950c353` meets this incidence boundary at its
first coefficient layer.  In the concentrated-spoke ordered-`01/10`
module, every chart with at most two off-diagonal internal coordinates has
an ordinary source-row unit.  This includes all eight nonzero quadratic
quotient defects (two stabilizer orbits); exact 47-variable lifts kill all
eight, and in fact all `180` disjoint decorated pairs.

Consequently neither the multiply-used nor the trapped-active alternative
can be coefficient-feasible with only one or two ordered `01/10` cells in
that module.  The first coefficient residual there needs three pairwise
disjoint off-diagonal cells.  If any physical edge lies outside the selected
anchor union, the nonanchor theorem routes it; hence the sharp concentrated
boundary is a three-cell decorated physical perfect matching entirely on
selected anchor edges.

This is a complete landing through quadratic filtration, not a claim about
arbitrary multisite stars or the other ordered colour sectors.  The cubic
anchor-perfect-matching symbol remains the next coefficient calculation.

## Verification

Run

```text
python3 computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py
python3 -O computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py
python3 -I -S computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py
```

The checker pins the one-sided crossed-lock boundary, the nonanchor active-
minor theorem, the diagonal-mate rank audit, and the complete quadratic
aggregate lift.  It verifies alternating repair cycles, literal deleted-
star matrices, the active determinant landing, both sharp guards, and the
complete normalized incidence census.

Frozen ledger SHA-256:

```text
78c6744f5b1f91ff3344ab77eb91191be55144335c05dbf074c0eda9290693f4
```
