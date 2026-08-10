# A large target-axis mixed escape must contain a colour two-cycle

## 1. Result

The large diagonal-kernel argument has a coefficient-free extension to
arbitrary binary endpoint blocks up to one sharp obstruction.

> **Mixed-cycle gate.**  Suppose the target-coordinate part of a kernel row
> is itself a nonzero kernel row supported on at least three of the five
> common sites, while the two other pure tensors lie in the common-cofactor
> image.  Then every mixed-colour escape contains two nonzero off-diagonal
> cells with the same unordered colour transition.

Thus the target-axis branch does not escape through one mixed cell.  Its
first possible correction is exactly a doubled colour edge, matching the
quadratic correction in the unary-top off-diagonal filtration theorem.

## 2. Three zero binary cofactors

Let `a,c` be the bright colours and `t` the missing target.  For a genuinely
target-axis kernel row

\[
                       \sum_xu_xe_t^{(x)}K_x=0,          \tag{1}
\]

an output word with its unique `t` at `x` receives no contribution from a
different inserted hole.  Hence, if `u_x != 0`, the projection `K_x^B` to
the two bright colours is zero.  For support size at least three, at most
two binary cofactors remain.

Unlike the diagonal proof, no colour-parity claim about an arbitrary
kernel row is made here.  Equation (1) is an explicit hypothesis.  A mixed
cell can couple a non-target kernel component into the target sector; the
committed first-transgression guard shows that this distinction is real.

## 3. The abstract two-hole split is still pure

The two remaining cofactors are arbitrary binary tensors.  Nevertheless,
if their two-hole common-cofactor map contains both `X_a,X_c`, they split.

In the pure-`d` equation, using hole `h` forces `K_h^B` to have factor
`e_d` at the other hole `k`: a word with the other colour at `k` cannot be
cancelled by the term inserted at `k`, whose `k` coordinate is fixed to
`d`.  A nonzero cofactor cannot have both factors `e_a,e_c` at that site.
Consequently one bright row uses only `h`, the other only `k`, and after
exchange

\[
                K_h^B=\lambda e_a^{\otimes4},\qquad
                K_k^B=\mu e_c^{\otimes4}.                \tag{2}
\]

This tensor split uses no diagonal assumption on the internal cells.

## 4. The first possible cancellation is a two-cycle

Choose a nonzero all-`a` matching monomial in `K_h^B` and an all-`c`
matching monomial in `K_k^B`.  As in the diagonal proof, some selected
`aa` edge and selected `cc` edge are disjoint.  They define a `2a+2c`
coefficient of another cofactor.

There are exactly three compatible physical matchings of those four sites.
One is the named nonzero product

\[
                         q_{ij}^{aa}q_{kl}^{cc}.          \tag{3}
\]

The other two pair `a` sites to `c` sites.  Each is a product of two
off-diagonal cells, both carrying the unordered transition `ac`.  Since
the cofactor in question is either zero or pure by (1)--(2), its mixed
coefficient vanishes.  The nonzero term (3) must therefore be cancelled by
at least one alternate matching.  This forces a nonzero `ac,ac` two-cycle.

The checker audits all ten pairs of bright holes and all `3*3` pairs of
pure matching monomials.  Each of the 90 coefficients has exactly the
selected diagonal term and two off-diagonal two-cycle alternatives.

The obstruction is sharp locally.  On the word `0011`, the cells

```text
01:00=1, 23:11=1, 02:01=1, 13:01=-1
```

make the selected diagonal product cancel one two-cycle product exactly.
This four-site packet is not a full source; it guards against promoting the
cycle necessity to a contradiction without additional rows.

## 5. Consequence and scope

The full mixed two-bad problem now has two distinct first mechanisms:

1. a genuinely target-axis large kernel requires a colour two-cycle by the
   present theorem;
2. a tilted kernel may receive a first-order transgression from a
   non-target diagonal kernel component.

The second mechanism occurs with one mixed cell and is not covered here.
The next uniform proof must kill that transgression using the two bright
rows, or show that its first nonlinear completion again lands in the
two-cycle gate.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_target_axis_mixed_cycle_gate.py
python3 -O computations/verify_shared_reciprocal_two_bad_target_axis_mixed_cycle_gate.py
```

The checker uses only the Python standard library.
