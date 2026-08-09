# The first two-centre pure-kernel product is impossible

## 1. Result

Continue in the five-site quotient of
[`the two-bad cofactor theorem`](shared-reciprocal-two-bad-cofactor-quotient.md).
Write `K=q^[2]` and `Phi(w)=wK`.  The atomic result in
[`shared-reciprocal-two-bad-atomic-kernel-exclusion.md`](shared-reciprocal-two-bad-atomic-kernel-exclusion.md)
closes one-site kernel rows.  The first genuine signed cancellation also
closes.

> **One-site/two-centre kernel lemma.**  Assume over an integral domain:
>
> 1. every internal cell of `q` has the same colour at its endpoints;
> 2. one of `U,V` is supported at one site and the other has a minimal
>    two-centre cofactor relation;
> 3. `X_a,X_c in im(Phi)` have distinct one-centre preimages; and
> 4. `T(P,U,V)=PUVq` has a nonzero `X_t` coefficient.
>
> Then the equations are inconsistent.

Together with the atomic lemma, a colour-diagonal survivor with one-centre
pure lifts must have both kernel rows genuinely supported on at least two
centres.  Equivalently, after the `45/180` same-hole split, neither one-site
side nor the first signed two-centre repair can carry the distinct-hole
pure grade.

## 2. Normal form

Choose a nonzero pure monomial and normalize its five sites as

```text
U at 0, selected V entry at 1, selected P entry at 2, q_34(t,t) != 0.
```

The one-site kernel gives `K_0=0`.  Write the other kernel relation as

\[
 w_1^{(1)}K_1+w_z^{(z)}K_z=0,                         \tag{1}
\]

If either inserted cofactor column is zero, a nonzero component of the
pure product reduces to the atomic lemma.  Hence minimality lets us assume
both are nonzero.  Here the local vectors `w_1,w_z` are arbitrary, while
the selected pure product says that the `t` component of `w_1` is nonzero.
The extra centre cannot be `0`, since `K_0=0`, and is therefore one of
`2,3,4`.

A one-centre lift of `X_a` makes its four-site cofactor a nonzero pure
`a` tensor; similarly for `c`.  First suppose their centres are disjoint
from `{0,1,z}`.  They are then the two complementary sites.  For each of
the three choices of `z`, two centre orders, and three matching terms in
each pure cofactor, there are

\[
                         3\cdot2\cdot3\cdot3=54          \tag{2}
\]

normalized configurations.

## 3. Unique-word contradiction

In a colour-diagonal four-site hafnian, a word with two occurrences of one
colour and two of another has exactly one compatible matching.  Therefore
two disjoint mandatory matching edges of different colours give a nonzero
coefficient which no additional diagonal support can cancel.

The checker exhausts (2).  Its deterministic first-witness histogram is

```text
K_0=0                         30
pure K_ha                     16
pure K_hc                      4
two-centre proportionality     4
```

In the first three rows the unique mixed coefficient directly contradicts
zero or purity.  For each of the last four cases, fix the known nonzero `t`
component at the selected centre `1`.  A mandatory 2+2 word in `K_1` has a
unique matching.  To cancel it in the other inserted cofactor column, (1)
forces another unique 2+2 matching.  Its target-colour repair edge then
forms a unique mixed word in one of the pure cofactors, a contradiction.
This allows completely arbitrary local vectors at the second centre; it
does not assume that the relation is axis-purified.  Deleting the
proportionality/repair test leaves exactly those four cases, auditing that
the new two-centre input is load-bearing.

This is a coefficient-independent matching argument, not a support SAT
calculation.  It handles arbitrary extra colour-diagonal cells and all
nonzero weights in an integral domain.

The checker then allows either pure centre to overlap `{1,z}`.  The first
implications close 308 of the 324 total configurations.  In 12 of the 16
remaining cases, (1) forces the two cofactors to share a three-site factor;
purity fixes that factor to one coordinate line, while a unique mixed word
on the opposite cofactor leaves the line.  In the final 4 cases both
relation centres are pure, in the two distinct colours `a,c`; their common
three-site factors disagree immediately.  Hence all 324 configurations
close, without any target-axis assumption on `w_1,w_z`.

## 4. Remaining boundary

The minimal unresolved pure-kernel packet must use at least one of:

- a mixed-colour internal cell;
- two genuinely multi-centre kernel rows; or
- a multi-centre lift of one of the two known pure tensors.

The source-faithful rational guard in the quotient note already exhibits
one multi-centre signed kernel, but its product is mixed.  The next sharp
case is therefore the `2 x 2` centre relation: compare four inserted
cofactor columns and ask whether their distinct-hole terms can carry a
pure quotient class.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_two_centre_kernel_exclusion.py
python3 -O computations/verify_shared_reciprocal_two_bad_two_centre_kernel_exclusion.py
```

The standard-library checker pins the atomic dependency and audits all 54
matching-witness configurations.
