# The unary scalar arm closes the co-located Hall-star lock

## Result

The two-neighbour residual of `19bc055` is empty on the actual one-bad
packet.  Its apparent outer-neighbour terms disappear coefficientwise, and
the remaining Hall-centre terms repair the second good arm.

More precisely, let the same off-anchor block `P-u` carry the nonzero
reciprocal cells

```text
x12 = A_Pu(1,2),        x21 = A_Pu(2,1),
```

with the nonzero complete crossed cofactors supplied by the Hall-star
theorem.  The one-bad outer block is

\[
                         A_{PS}=\lambda E_{00}.       \tag{1}
\]

Consequently the private-site transition from `P-u` to `P-S` is zero in
both directions.  If all free companions have already been excluded as in
`19bc055`, the two exact private identities force

\[
 \Delta^{12}_{uc}C^{12}_c=-x_{12}\ne0,
 \qquad
 \Delta^{21}_{uc}C^{21}_c=-x_{21}\ne0.               \tag{2}
\]

The pair `P-u` was already off-anchor, active, and rank `(3,3)`.  Equation
(2), together with the original crossed cofactors, makes `P-c` rank
`(3,3)` at both ends and gives a nonzero transition between the two pairs.
Thus they form the certified distinct-head active four-good overlap.  The
co-located Hall-star branch is closed uniformly, without a support census.

Checker:
`computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py`.

## Why the outer terms vanish

For `x12`, use the pure/mixed private comparison with neighbour colour `2`
and endpoint colours `2/1`.  Its outer determinant uses exactly

\[
 A_{PS}(2,2),\qquad A_{PS}(1,2).
\]

Both entries vanish by (1).  For `x21`, the corresponding entries are

\[
 A_{PS}(1,1),\qquad A_{PS}(2,1),
\]

and again both vanish.  Hence

\[
             \Delta^{12}_{uS}=\Delta^{21}_{uS}=0.     \tag{3}
\]

This is stronger than the incidence-only `{S,c}` reduction.  It uses the
literal scalar-unit direct block furnished by the anchor-safe one-bad
retraction; a merely selected pure-0 cell would not justify (3).

The complete source identity in either direction is

\[
 p_uG_{\rm mixed}-xG_{\rm pure}
   =x+\sum_s(p_uq_s-xp_s)C_s.                         \tag{4}
\]

In the residual under discussion every summand outside `{S,c}` is zero.
Substitution of (3) into (4) gives (2).  Since the base field is a domain,
each determinant and its cofactor in (2) are separately nonzero.

## The repaired deleted-star ranks

Delete `P-c`.  At `P`, three surviving coordinates are

```text
row 0: P-S:00,        row 1: P-u:12,        row 2: P-u:21.
```

They occupy distinct row and output coordinates, so the deleted `P`-star
has rank three.

At `c`, choose one nonzero matching monomial in each of the original active
crossed cofactors at `P-u`:

* the `x21` cofactor has colour 1 away from the Hall centre and supplies a
  nonzero colour-2 cell incident to `c`;
* the `x12` cofactor has colour 2 away from the Hall centre and supplies a
  nonzero colour-1 cell incident to `c`;
* the unary equation `q^[h]=X0` supplies a nonzero pure-0 matching and hence
  a colour-0 cell incident to `c`.

The crossed cofactors delete `P,u`, and the unary matching uses `P-S`.
None of these three cells is the deleted edge `P-c`.  Their physical
neighbours may coincide, but their neighbour-colour labels are respectively
`0,2,1`, so the three output coordinates are distinct (and their `c`-rows
are respectively `0,1,2`).  The deleted `c`-star therefore also has rank
three.

The selected diagonal matchings already make `P-c` active.  Equation (2)
is the nonzero source-provenant transition between `P-u` and `P-c`.
Accordingly the two adjacent pairs satisfy exactly the four-good,
distinct-head active-overlap hypotheses used by the existing wedge theorem.

## Scope

This is uniform for `h>=3` on the anchor-safely retracted scalar-unit
one-bad packet.  It uses all of the following load-bearing data:

* the exact outer block `A_PS=lambda E00`, not only a selected unary cell;
* both nonzero reciprocal cells at `P-u`;
* their genuine complete nonzero crossed cofactors;
* the unary pure matching and the two diagonal selected matchings; and
* the prior reduction that every free transition product is zero.

It does not close the separate opposite-side anchor triangle or the
triangle/`K2,2` Hall-family strata.

Run

```text
python3 computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py
python3 -O computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py
python3 -I -S computations/verify_uniform_multisite_hall_star_colocated_unary_wedge_closure.py
```

Frozen ledger SHA-256:

```text
0aa7d13eb0ccc868820c6c4c5dea95a620dc00fcbf0b0e14fb2cd6becfc58396
```
