# Every ordered 01/10 decorated perfect-matching chart has a source unit

## Result

The terminal possible matching degree in the ordered `01/10` filtration is
three.  On six residual sites, three contributing off-diagonal cells must
occupy a physical perfect matching.  There are

\[
                       15\cdot 2^3=120                 \tag{1}
\]

such decorated matchings.  Every one has an exact ordinary source-row unit
in the concentrated-spoke aggregate chart.

The order-four stabilizer

\[
                  \langle(0\,1)(2\,3),(4\,5)\rangle   \tag{2}
\]

has 32 orbits: 28 of size four and four of size two.  The checker constructs
one complete 48-variable source ideal per orbit representative, obtains an
exact lift of the normalized target product, and verifies the lift by
literal expansion.  Therefore no decorated perfect matching is a
coefficient-feasible cubic escape.

Checker:
[`verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py`](../computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py).

## The cubic symbol is already zero

Write the frozen diagonal identity as

\[
 T=F_{01}(1111)F_{23}(2222)H(000000)=\sum_r m_rg_r.   \tag{3}
\]

For a decorated perfect matching `x,y,z`, the cubic symbol is

\[
                       D_{xyz}=\sum_rm_r
                          \partial_x\partial_y\partial_zg_r. \tag{4}
\]

Only six-site top rows can have a nonzero derivative in (4); every cofactor
row has only four physical sites.  Direct substitution into the original
34 multipliers gives

\[
                              D_{xyz}=0                \tag{5}
\]

as a literal polynomial for all 120 decorations.  This is stronger than
vanishing in the diagonal quotient.

Equation (5) alone is not enough, because the nonzero quadratic defects
from `950c353` must be integrated compatibly.  The checker therefore builds
the full rows

\[
 g_r(x,y,z)=g_r+\sum_u u\,\partial_ug_r
  +\sum_{u<v}uv\,\partial_u\partial_vg_r
  +xyz\,\partial_x\partial_y\partial_zg_r             \tag{6}
\]

for every orbit representative and recomputes the source lift.  All 32
target remainders are zero.  The lifts use 34--36 source rows and their
standard bases have 251--704 elements.

There is no genuinely cubic multiplier in any lift.  Twenty-three orbit
lifts use none of `x,y,z`; eight use one quadratic parameter pair `yz`, and
one uses `xy`.  Thus every cubic chart is killed by a compatible diagonal
or quadratic source identity; no new cubic attaching generator is needed.

## Intersection with selected anchor unions

Choose one nonzero matching in each normalized pure coefficient:

* a six-site unary matching `Q0`;
* a colour-one matching `Q1` on the complement of holes `01`; and
* a colour-two matching `Q2` on the complement of holes `23`.

Among the `15*3*3*15=2025` choices of `(Q0,Q1,Q2,P)`, where `P` is the
physical matching underlying the three off-diagonal cells, exactly 245 have

\[
                              P\subseteq Q_0\cup Q_1\cup Q_2. \tag{7}
\]

Their edge-use multiplicity signatures are

```text
111 : 132       112 : 80       113 : 4
122 :  24       222 :  4       223 : 1.
```

Hence 132 all-anchor configurations have three uniquely used edges and 113
contain a multiply-used selected edge.  Adding the eight endpoint-colour
decorations gives 1,960 all-anchor configurations.  Every one belongs to
one of the 32 exact source-unit orbits above.

This is the coefficient-level supplement to the active-exit dichotomy
`c78fc9b`: neither its multiply-used incidence exception nor its possible
unique-edge trapped-concentration exception produces a source solution on
the minimal three-cell cubic chart.  The other 1,780 physical configurations
contain a nonanchor edge and are independently routed to the transverse
good active arm by the nonanchor theorem.

## Exact remaining scope

This closes arbitrary diagonal internal cells plus one specified decorated
`01/10` perfect matching, with arbitrary coefficients in its three cells.
It does **not** prove a unit for support containing multiple decorated
perfect matchings simultaneously.  Although source coefficients have
off-diagonal matching degree at most three, the orbitwise lifts need not be
compatible across overlapping triples.  That compatibility/Čech statement
is the remaining all-support issue in this colour sector.

It also does not cover `02/20`, `12/21`, or multisite endpoint stars.

Run

```sh
python3 computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py
python3 -O computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py
python3 -I -S computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py
```

Ledger digest:

```text
37353079ba50ba9706c52c6d0695e61a94b708c6cd086ed1ff10160f3455c1c5
```
