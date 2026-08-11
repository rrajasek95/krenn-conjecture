# Every ordered 01/10 two-cell aggregate chart has a source unit

## Result

The first potentially nonzero correction to the 34-row diagonal aggregate
identity occurs in off-diagonal filtration degree two.  Its complete
ordered `01/10` symbol is nevertheless harmless.

Among the 180 decorated pairs on disjoint physical edges,

```text
raw quadratic defect identically zero       140
raw nonzero defects                           40
zero classes modulo the 71 diagonal rows     172
nonzero quotient classes                       8
stabilizer orbits of nonzero classes           2
exact two-cell source units                   180
```

The eight apparent quotient classes are monomials.  They are not
countermodels: rebuilding each corresponding 47-variable two-cell source
ideal gives an exact lift of the normalized target product.  The checker
also rebuilds all other 32 raw-nonzero charts.  All 40 exact lifts expand
literally to the target, with 34--36 nonzero source multipliers.  For the
140 raw-zero pairs, the original 34-row lift is already unchanged.

Checker:
[`verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py`](../computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py).

## The bilinear symbol

Retain the notation

\[
 T=F_{01}(1111)F_{23}(2222)H(000000)
   =\sum_r m_rg_r                                      \tag{1}
\]

from the pinned diagonal theorem.  For two ordered off-diagonal coordinates
`x=q_uv^(ab)` and `y=q_zw^(cd)`, with `ab,cd` in `{01,10}`, write

\[
 g_r(x,y)=g_r+x\dot g_{r,x}+y\dot g_{r,y}
                         +xy\ddot g_{r;x,y}.            \tag{2}
\]

The linear sums vanish identically by `b1cab97`.  If the physical edges
intersect, the mixed derivative in (2) is zero because no perfect matching
uses both.  For disjoint edges it is the labelled residual hafnian

\[
 \ddot g_{r;x,y}=
 \operatorname{haf}
   (q_w|_{V_r\setminus\{u,v,z,w\}}),                    \tag{3}
\]

provided the output word has the four prescribed endpoint colours, and is
zero otherwise.  The checker forms

\[
                   D_{x,y}=\sum_r m_r\ddot g_{r;x,y}    \tag{4}
\]

directly in the original 45-variable diagonal ring.  Thus no ring with 30,
much less all 90, off-diagonal coordinates is used.

## The two critical orbits

The labelled source packet is preserved by the order-four site stabilizer

\[
 \langle(0\,1)(2\,3),(4\,5)\rangle .                  \tag{5}
\]

It has 52 orbits on the 180 decorated disjoint pairs, with orbit-size
histogram

```text
size 1: 4 orbits
size 2: 8 orbits
size 4: 40 orbits.
```

Only two orbits survive in the diagonal quotient.  Representatives and
normal forms are

\[
\begin{array}{c|c}
(03{:}01,45{:}01)&q_{01}^{22}q_{13}^{00}q_{24}^{11}
                    q_{25}^{00}q_{45}^{22}\\
(04{:}01,35{:}10)&q_{01}^{22}q_{13}^{00}q_{24}^{00}
                    q_{25}^{11}q_{45}^{22}.
\end{array}                                             \tag{6}
\]

Each orbit has four members.  Exact two-cell source lifts kill all eight
classes.  Their reduced standard bases have sizes 367--370 and their lifts
use 35 source rows.  Hence (6) records the attaching classes needed to
integrate the diagonal identity, not an obstruction to integration.

There are 32 further raw-nonzero defects already in the diagonal source
ideal; their exact two-cell lifts are also checked.  The remaining 140
symbols vanish before quotienting.  Pairs on intersecting physical edges
are automatic by matching square-freeness, so the same conclusion covers
all unordered choices of at most two ordered `01/10` coordinates.

## Consequence for the decorated-anchor boundary

A completion with at most two ordered `01/10` internal coordinates cannot
attach the missing unary target: the fine-degree source ideal still contains
`T`, so the normalized source equations give an ordinary unit.

On six residual sites, the next filtration term must use three pairwise
disjoint off-diagonal cells, hence a decorated physical perfect matching.
If one of its physical edges lies outside the selected pure-anchor union,
the nonanchor reselection theorem returns it to the transverse good active
arm.  The sharp new boundary is therefore a three-cell ordered `01/10`
perfect matching entirely supported on selected anchor edges.

## Scope

This is an exact theorem for the concentrated-spoke, 71-row fine-degree
module and ordered `01/10` internal coordinates.  It does not cover the
cubic three-cell symbol, the `02/20` or `12/21` sectors, multisite endpoint
stars, or by itself complete the active clean-cap bridge.

Run

```sh
python3 computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py
python3 -O computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py
python3 -I -S computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py
```

Ledger digest:

```text
7611969cf0768b162f5182f2ebd2ab701a285baa4daa725992aba4c761c4d694
```
