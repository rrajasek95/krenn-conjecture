# Balanced base locus: odd sets and bounded Luna/jet audit

Status: **exact bounded negative/obstruction PASS**.  Edmonds--Tutte theory
classifies only the leakage-free, no-perfect-matching diagonal branch.
Cross-colour energy leakage and complex cancellation give independent balanced
base mechanisms.  On the two canonical controls, the first normal images and
the cheapest higher jets do not produce a GHZ leading term; second variation
also has an explicit blind direction, so it is not a complete properness proof.

## 1. Exact fractional-matching scope

Fix a colour `c`.  If the source is diagonal in that colour and moment zero
gives common positive diagonal port degree `d_c`, then

```text
x_ij=|A_ij^(c,c)|^2/d_c,
sum_(j!=i) x_ij=1.
```

Thus `x` is a fractional one-factor.  The extreme points of the degree-only
fractional one-factor polytope are disjoint unit matching edges and half-weight
odd cycles.  If the support has no integral perfect matching, Tutte supplies
an odd-set obstruction; equivalently, an odd-set inequality needed for the
perfect-matching polytope fails.

The unit diagonal colour-zero point on

```text
C3(0,1,2) disjoint_union C5(3,4,5,6,7)
```

is the sharp control: every port has energy 2, edge weights `1/2` give a
fractional one-factor, and no perfect matching exists.

Two effects stop this from being a global carrier theorem.

First, total moment balance reads

```text
diagonal_degree_i,c = d_c - L_i,c,
```

where `L_i,c` is offdiagonal endpoint-colour energy.  It does not make
`L_i,c` site-independent.  On the same `C3 disjoint_union C5`, put all six
`a!=b` cells on every edge with unit value.  Every one of the 24 ports has
energy 4, the diagonal support is empty, and the top tensor is still zero.

Second, support can contain many integral perfect matchings while the
coefficient vanishes by phase cancellation.  This is made exact next.

## 2. Balanced phase-cancellation base

Use only diagonal colour-zero cells.  On the first K4 put

```text
A01=A23=A02=A03=1,  A13=omega,  A12=omega^2,
omega^2+omega+1=0.
```

Its three matching products are `1,omega,omega^2`, so its hafnian is zero.
On the second K4 put unit value on all six edges, whose hafnian is 3.  Every
site has port energy 3.  The full support has nine perfect matchings, but

```text
H_00000000=(1+omega+omega^2)*3=0.
```

This exact moment-zero base point has no leakage and no odd-set obstruction.
The absolute-square moment map has forgotten precisely the phases responsible
for the base equation.  Consequently fractional matching data cannot classify
all balanced leading supports.

Nor does a Tutte obstruction automatically give a clean cap.  Odd-set data
are support-only; carrier activity is a coefficient/rank row-space condition
and is not closed at rank drop.  No source-labelled implication from every
odd set to one of the 728 cap/descent antecedents is justified.

## 3. C3+C5 first and second normal data

At the unit colour-zero odd-cycle base `B0`, a derivative column is nonzero
exactly for one of the 15 cross-component edges, with any of its nine colour
cells.  Of the 252 source columns, 135 are nonzero, and their distinct output
words give

```text
rank(dH_B0)=77,  dim ker(dH_B0)=175.
```

The image consists of words differing from colour zero only at the endpoints
of one cross edge.

There is a literal quadratic cokernel obstruction.  Put

```text
X=A03^(1,0)-A04^(1,0),
Y=A45^(1,1).
```

Both are tangent to moment zero and satisfy `dH(X)=dH(Y)=0`, while exact
matching enumeration gives

```text
H(B0+sX+tY)=s*t e_10001100.
```

The word `10001100` is outside `im(dH_B0)`, so the mixed direction `X+Y`
cannot lift to second order inside the top base locus.

Second variation is not sufficient.  The tangent

```text
X0=A03^(0,0)+A14^(0,0)+A25^(0,0)-3A04^(0,0)
```

obeys the exact identity

```text
H(B0+sX0)=s^3 e_00000000.
```

Thus both its linear and quadratic images vanish.  The first nonzero datum is
cubic and supplies only one pure colour, not GHZ.  This is an explicit
second-order blind direction.

## 4. K4+K4 first normal image and cross-jet obstruction

At the phase-cancellation base, only variations of the cancelling left K4
have nonzero first derivative; the right K4 hafnian supplies the nonzero
factor 3.  Exact support/cofactor enumeration gives

```text
54 nonzero derivative columns,
rank(dH)=33,
dim ker(dH)=219.
```

The image differs from colour zero only at two endpoints in the left block.
In particular neither pure colour one nor pure colour two belongs to the
linear image, so a GHZ first-order leading jet is impossible.

The cheapest way to generate a new pure colour is a first-order 4 by 4
cross-block matrix `X`.  At order two, every choice of two left and two right
sites produces a mixed coefficient equal, up to a nonzero complementary base
edge, to

```text
per_2(X[I,J]).
```

All 36 such mixed coefficients must vanish before an order-four pure term can
lead.  But the pure order-four coefficient is `per_4(X)`, and Laplace expansion
by two rows gives

```text
per_4(X)=sum_(|J|=2)
  per_2(X[{0,1},J]) per_2(X[{2,3},J^c])=0.
```

Hence the quadratic mixed shell kills the desired quartic pure coefficient.
This excludes the canonical four-cross-edge GHZ jet.

The same filtration excludes leading orders below six.  Order four is the
cross-permanent case above.  At order five, a `1+1+1+2` matching either uses
an order-one internal-left `(c,c)` cell, producing its unique forbidden linear
word, or contains an order-one cross pair already killed by the quadratic
mixed shell.  Thus `m < 6` is impossible.

## 5. First order-six channel and its finite obstruction

The first channel not covered by those lower-order guards has

```text
v(U_cross^(1,0))=1,  v(R_right^(1,1))=1,
v(L_left^(1,1))=2.
```

For left pairs `I` and right pairs `J`, write `per_2(U[I,J])` for the two
cross-edge permanent.  The six order-two equations eliminate the six `L_I`:

```text
3 L_I + sum_(|J|=2) per_2(U[I,J]) = 0.                 (E2_I)
```

The next source-labelled cokernel equations are

```text
R_J (per_2(U[I,J^c]) + L_I) = 0,                       (E3_IJ)
L_I Haf(R) = 0.                                        (E4_I)
```

There is one further order-four row with word `11110000`; it is redundant
for the following exclusion.  The candidate order-six pure coefficient is

```text
[t^6] H_11111111 = Haf(L) Haf(R).
```

If this is nonzero, then `Haf(R)` is nonzero.  The six `E4_I` rows force all
six `L_I` to vanish, contradicting `Haf(L) != 0`.  Thus the entire first
order-six valuation channel is impossible, before imposing any carrier
no-cap memberships.

The scope is exact but narrow: this is the oriented binary response channel
`U^(c,0)@1, R_right^(c,c)@1, L_left^(c,c)@2`, not an arbitrary-valuation
order-six theorem.  In contrast, the order-four and order-five exclusions
are closed inside each binary output alphabet `{0,c}`.  A source cell using
the third physical colour cannot contribute to, and hence cannot cancel, a
word using only `{0,c}`.  Therefore arbitrary third-colour coupling creates
no escape before order six.

As an exact control, take every `U` entry equal to one, `R_45=R_67=1`, and
the other `R` entries zero.  Equations `E2` give `L_I=-4`.  Literal matching
enumeration has zero output through order two, then exactly

```text
12 mixed rows at order 3,
 7 mixed rows at order 4,
H_11111111 = 48 t^6.
```

All 19 row labels and their coefficients in `Q(omega)` are frozen in the
JSON result.  The order-three rows split six each over the two live right
pairs `45` and `67`.  The six order-four words with two left ones and four
right ones already give the contradiction above; the seventh is
`11110000` with coefficient `-120` in this symmetric control.

The first distinct order-six system has the same valuation partition
`1+1+2+2`, but reinserts direct coloured cross cells.  Besides `U,R,L` above,
let `X` and `V` be the 16 cross `(c,c)` cells at orders one and two.  There
are 60 coefficient variables, or 54 after eliminating `L`.  With
`P_(X,V)[I,J]` the coefficient of `t^3` in
`per_2(tX[I,J]+t^2V[I,J])`, the first finite rows are

```text
3L_I + sum_J per_2(U[I,J]) = 0,                              (6)
per_2(X[I,J]) = 0,                                          (36)
P_(X,V)[I,J] + R_J(L_I+per_2(U[I,J^c])) = 0,                (36)
L_I Haf(R) + sum_J R_(J^c)P_(X,V)[I,J] = 0.                 (6)
```

The last polar term occupies exactly the same left-pair/right-four word as
`L_I Haf(R)`, so it defeats the response-only `L=0` obstruction.  Its
order-one direct support is already small: the 36 two-by-two permanent
equations force `supp(X)` to be a row
star, a column star, or a single `2x2` cancellation block.  (Three nonzero
rows or columns in such a block give inconsistent pairwise sign ratios in
characteristic zero.)  The right block has literal `S4` symmetry; the phased
left block's exact site stabilizer is trivial.

On the minimum `Haf(R)!=0` support, right `S4` has one orbit, represented by
`R_45=R_67=1`.  The three `X` types resolve as follows.

- A row-star `X` is impossible: for every left pair `I` avoiding its centre,
  `P_(X,V)[I,J]=0`; `E4` forces `L_I=0`.  Every left perfect matching contains
  such a pair, hence `Haf(L)=0`.
- A column-star survives.  For arbitrary nonzero `z_0,...,z_3`, set

  ```text
  U_i4=U_i5=U_i6=z_i, U_i7=0,
  X_i4=z_i, V_i5=z_i,
  R_45=R_67=1, L_ij=-2 z_i z_j.
  ```

  All displayed `E2/E3/E4` rows vanish, while

  ```text
  Haf(L)Haf(R)=12 z_0 z_1 z_2 z_3,
  [t^6]H_11111111=-12 z_0 z_1 z_2 z_3.
  ```

- A `2x2` cancellation block is impossible on this minimum-`R` orbit.  Put
  its columns at `45`.  Then `E4` gives `L_23=0`; `E3` gives `q_45=-L` and
  `q_67=0`; and `E2` gives
  `B(a+b,c+d)=2B(a,b)` for the four columns of `U`.  The exact-Q ideal
  calculation in `verify_phase_m6_symmetrized_product.sing` proves

  ```text
  q_01 q_23 = q_02 q_13 = q_03 q_12.
  ```

  Since `q_23=0`, this forces `Haf(q_45)=Haf(L)=0`.  Denser `R` support in
  this stratum is not classified, but cannot beat the column-star branch's
  two-edge support.

At `z_i=1`, literal response-row enumeration gives positive valuation one
for every base-active rank-zero pivot:

```text
star: 24 at valuation 1,
triangle: 48 at valuation 1,
inactive: 0.
```

Thus the smallest finite branch survives both `E2--E4` and all 72 pivot
nonvanishing requirements.  It does **not** survive the full literal word
system.  For every left pair `I={i,k}`, the omitted binary word with colour
`c` on `i,k,4` has

```text
[t^2] H_(c on i,k,4) = 4 l_(I^c) z_i z_k.
```

The six labels for `c=1` are
`11001000,10101000,10011000,01101000,01011000,00111000`.
All complementary phase-base cells `l_(I^c)` are nonzero units, and the pure
coefficient requires every `z_i` nonzero.  These words have a coloured right
site and lie outside `im(dH)`; no order-two correction can cancel them.

Duplicating the family in colour two gives exactly 48 nonzero mixed words at
order two: six binary colour-one rows, six binary colour-two rows, and 36
cross-colour rows.  The binary rows alone are terminal because a cell using
the other physical colour cannot contribute to a `{0,c}` output word.  Thus
all four blocker choices on all 72 activated carriers are excluded upstream;
there is no need, and no sound reason, to branch over `4^72` memberships.

## 6. Exhaustive binary order-six valuation ledger

There are only two weak positive partitions of total pure valuation six,

```text
1+1+1+3,  1+1+2+2,
```

and a pure matching uses `k=0,2,4` cross-block edges.

- For `1+1+1+3`, `k=0` forces an uncancellable order-one left-internal
  cell; `k=2` has two order-one cross edges whose lower `per_2` row contains
  the pure factor; and `k=4` would require a size-three matching in the
  order-one cross support, impossible under `per_2(X)=0` (star or one
  `2x2` cancellation block).
- For `1+1+2+2`, `k=0` is precisely the oriented response channel, with a
  direct polar needed to rescue `E4`.  At `k=2`, the assignment with two
  order-one cross edges is killed by `per_2(X)`; the only remaining assignment
  is `L@2,R@1,X@1,V@2`.  At `k=4`, the degree-six permanent is a Laplace sum
  of the same degree-two `per_2(X)` and degree-three `P_(X,V)` factors, so it
  either vanishes or introduces `L@2,R@1` and reduces to the same coupled
  channel.

Hence every binary `m=6` topology is impossible or reduces to

```text
U@1, X@1, R@1, L@2, V@2.
```

On the minimum right support `R_45 R_67!=0`, row-star and `2x2-X` branches
are excluded as above.  A column-star with at least three nonzero entries is
also excluded after adding the omitted polar rows: the order-two `U-X` rows
force `sum_(j!=4) U_ij=0`; `E2/E3` then give
`U_4=-b/3, U_6+U_7=-b, L=B(b,b)/3, B(X,V)=-L`; the next order-three `U-V`
rows force `B(V,b)=0`, incompatible with `B(X,V)=-L` when `Haf(L)!=0`.
The explicit all-one family above is the specialization with six nonzero
`U-X` rows; the adjusted specialization killing them has twelve nonzero
order-three rows instead.

The smallest unresolved minimum-support branch is therefore a column-star
`X` with exactly two nonzero row entries.  For denser `R`, fix the live
matching `45|67`.  Its order-eight stabilizer has six orbits on subsets of the
four extra edges: none, one, two adjacent, two opposite, three, or all four.
After the two-entry minimum branch, these five denser orbits are the complete
next binary `m=6` support ledger—not an open-ended ansatz search.

These six branches are in fact empty on the response-component open
`Haf(L)Haf(R)!=0`.  Put the two-entry column on right site 4 and write
`a,b,c,d` for the four `U` columns.  If `x` is supported on left rows `0,1`,
set `B(u,v)_ik=u_i v_k+u_k v_i`.  The literal rows are

```text
R_67 B(x,b)=0, R_57 B(x,c)=0, R_56 B(x,d)=0,             (XUR)
R_67(q_45+L)=R_57(q_46+L)=R_56(q_47+L)=0,               (E3)
m_45 q_67 + m_46 q_57 + m_47 q_56=0,                    (E4)
```

where `m_45=R_45R_67`, etc., and
`Haf(R)=m_45+m_46+m_47`.  The `L` terms cancel exactly in the last line.
The first `XUR` equation makes
`b=mu(x_0,-x_1,0,0)`.  On the no-extra, one-extra, and two-adjacent orbits,
no new right matching product is completed, so `E4` gives `q_67=0` and
`P_45=-R_45L`.  Comparing `B(x,V_5)=R_45B(a,b)` in positions `02` and `12`
forces simultaneously `V_52=+R_45 mu a_2` and
`V_52=-R_45 mu a_2`; similarly at site 3.  Hence `Haf(L)=0`.

For two-opposite, three-extra, and four-extra supports, each newly completed
matching supplies the corresponding `XUR` row.  Its `U` columns are
proportional to the same vector `(x_0,-x_1,0,0)`, and `E3` makes their
scalars equal.  Therefore the nonzero terms in `E4` all multiply the same
quadratic `q`, giving `Haf(R)q=0`.  The localization forces `q=0`, reducing
again to the preceding contradiction.

Thus all six frozen support branches are empty.  Binary word closure means
that adding colour two or any of the four blocker memberships cannot rescue
them, so pivot/no-cap branching is again killed upstream.  The exact scope
guard is important: a separate coefficient divisor with `Haf(R)=0` but a
nonzero direct `k=2` or `k=4` order-six polar was not part of this six-branch
response-component antichain and remains the next `m=6` target.

That final `Haf(R)=0` divisor closes structurally.  The complete degree-six
pure coefficient is

```text
H6 = Haf(L)Haf(R)
   + sum_(I,J) L_(I^c) R_(J^c) P_(X,V)[I,J]
   + [t^6] per_4(tX+t^2V).                                (H6)
```

The minimum support orbits are: empty `R` for the direct `k=4` term; one
`R` edge for `k=2`; and, for a genuine coefficient cancellation in
`Haf(R)`, the union of two right perfect matchings (one `C4` orbit) with
`m_1+m_2=0`.  The following proof is independent of this support size.

On `Haf(R)=0`, the six literal `E4` rows become

```text
sum_J R_(J^c) P_(X,V)[I,J] = 0  for every left pair I.
```

Multiplying by `L_(I^c)` and summing `I` kills exactly the middle `k=2`
summand of `(H6)`.

More generally, without setting `Haf(R)` to zero, the same contraction gives

```text
k2 = -Haf(R) sum_I L_I L_(I^c) = -2 Haf(L)Haf(R).
```

For `k=4`, the 36 order-two rows say `per_2(X[I,J])=0`.  Thus `X` is a row
star, column star, or one `2x2` permanent-cancellation block.  In the row-star
case choose two left rows avoiding its centre; in the `2x2` case choose the
two complementary left rows; in the column-star case choose two right columns
avoiding its centre.  Laplace-expand `per_4(tX+t^2V)` across that fixed pair.
The selected `2x2` factor has no degree-three polar because `X` is zero there,
while the degree-two coefficient of every complementary factor is one of the
vanishing `per_2(X)` rows.  Hence its degree-six coefficient is zero.

All three terms of `(H6)` now vanish.  Consequently **every binary total
order-six pure jet at the phase `K4+K4` base is impossible**, including
arbitrary `R` support on the `Haf(R)=0` divisor.  The conclusion precedes
carrier pivots and blocker memberships, and binary word closure makes it
stable under addition of the third physical colour.

Indeed the `k=4` proof is independent of `Haf(R)`, so the general contraction
reduces `(H6)` to `-Haf(L)Haf(R)`.  The whole product-zero complement,
including `Haf(L)=0,Haf(R)!=0`, therefore has `H6=0`; the preceding six-branch
argument excludes the product-nonzero open.  This is the exhaustive `m=6`
split.

## 7. Order-independent contraction and the exact order-seven ledger

There is one useful order-independent identity.  Regard the binary `(c,c)`
left, right, and cross cells as formal series `L_I(t),R_J(t),C_ij(t)`.  The
literal output word coloured on a left pair `I` and all four right sites is

```text
E_I(t)=L_I(t) Haf(R(t))
      +sum_J R_(J^c)(t) per_2(C[I,J](t)).
```

On the mixed-word ideal, multiply by `L_(I^c)` and sum all six `I`.  This gives
coefficientwise

```text
k2 = -2 Haf(L)Haf(R),
H_pure = per_4(C)-Haf(L)Haf(R).                            (OI)
```

This does not yet prove the all-order theorem.  The four-coloured-site rows
which would control every `per_2(C[I,J])` also contain oriented
`(c,0)/(0,c)` response products.  No source-faithful identity has yet removed
that contamination at arbitrary valuation.

At total order seven, there are three—not two—weak positive partitions of
four edge valuations:

```text
1114, 1123, 1222.
```

The `1114` partition is empty.  For `k=0` it forces a left-internal edge of
valuation one; for `k=2` the only remaining assignment is
`L4,R1,C1,C1`, killed by `per_2(X)`; and for `k=4` it needs three disjoint
order-one cross edges, impossible in the star/`2x2` support classification.

After the same linear-left and `C1,C1` exclusions, `1123` leaves exactly

```text
k0: L(2,3), R(1,1),
k2: L2, R1, C(1,3),
k2: L3, R1, C(1,2),
k4: C(1,1,2,3).
```

The additional `1222` partition cannot be omitted without another lemma.  It
leaves

```text
k0: L(2,2), R(1,2),
k2: L2, R1, C(2,2),
k2: L2, R2, C(1,2),
k4: C(1,2,2,2).
```

Thus order seven is reduced to eight exact primitive binary signatures.
Cells using the third physical colour cannot cancel any of their binary
output rows.

A bounded algebraic fallback is now source-labelled.  Translate the binary
source at the phase base and use the 112 endpoint cells with colours `{0,c}`.
In the completed local ring at the perturbation maximal ideal, let
`I_binary_mixed` be generated by the 254 binary output amplitudes other than
`0^8,c^8`.  The desired all-order statement is

```text
H_(c^8) in radical(I_binary_mixed) in the completed local ring.
```

The frozen `m=4,5,6` identities are its first initial layers.  A local
standard-basis or finite truncation certificate for this 112-variable target
would be appropriate; no global 252-variable Gröbner computation was run.

## 8. Bounded order-seven support and exact coefficient replay

The eight primitive packets were screened with literal binary matching
monomials through valuation seven.  The source-faithful mutation combines
base completions over `Q(w)`, `w^2+w+1=0`, *before* testing whether a row has
one live Laurent monomial.  The hostile raw-term mutation fails this guard:
it admits size-15 `k4` supports because it counts the three right-K4 base
completions separately, although their common source monomial has coefficient
`3`.  Those false supports acquire the literal singleton rows
`00110000`, `10010000`, or `10100000` at degree one.

Under the 20-orbit cap, the exact-aggregation repair screen found 20 minimum
supports in each of the four `k2` packets.  Their cell counts are ten.  Exact
`Q(w)` gates localized every listed source coefficient and the two-term
`pure7` polynomial.  All 80 gates are units, with zero timeout:

```text
1123 k2 L2,R1,C(1,3): 20/20 unit
1123 k2 L3,R1,C(1,2): 20/20 unit
1222 k2 L2,R1,C(2,2): 20/20 unit
1222 k2 L2,R2,C(1,2): 20/20 unit
```

The repair search is not an UNSAT engine: even with exhaustive repair choices
the `1222 k4 C(1,2,2,2)` queue had no model after 1,820 visits but timed out
with 34,424 states seen.  A complete SMT encoding therefore replaced it.
The encoding has 696 Boolean valuation atoms, all 256 binary words and every
coefficient of valuation `0..7`, 1,408 nonempty literal polynomial rows,
1,381 mixed `active-count != 1` clauses after exact phase aggregation, 1,575
earlier-pure exclusions, and the four fixed pure-seven seed atoms.  It was
emitted from 1,387,353 matching terms; the SMT source is 81,947,884 bytes.

Plain complete feasibility is **SAT**.  Its independently checked model has
252 live atoms.  Deterministic exact deletion gives an inclusion-minimal
82-atom witness in two passes: no mixed row has exactly one live monomial, no
pure-one matching occurs below order seven, and all four seed atoms remain
live.  Literal coefficient replay on this witness has 1,220 mixed equations,
term counts from 2 through 24, and ten pure-seven monomials.  This is a
support witness only, not a coefficient solution.  The cardinality-15 SMT
gate and the optimizing SMT gate both hit their 120-second caps without a
sentinel; no UNSAT inference is made.  Since the smallest sound witness has
82 live variables, the promised `<=20` exact-gate guard forbids a broad solve.

Thus the bounded 20-orbit antichains in the first seven packets are empty
after literal coefficient replay, but support feasibility alone does not
close order seven: the final `1222 k4` packet has the explicit
82-variable/1,220-row coefficient target.  Third-colour rows still cannot
cancel these binary output words.

### Toric closure of the first complete-SMT witness

The 82-variable target contains 125 binomial rows.  Their exponent matrix has
rank 59, and its Smith form has 59 unit invariant factors, so ignoring
constants would leave a 23-dimensional Laurent torus.  The constants are not
compatible: 13 zero Smith rows have nontrivial transformed constants.  The
smallest relation uses only two literal rows:

```text
word 00000100, degree 2:
  (14:00@1)(25:01@1) + (25:01@1)(37:00@1) = 0,

word 10000100, degree 2:
  (05:11@1)(14:00@1) + (-1-w)(05:11@1)(37:00@1) = 0.
```

All four displayed support atoms are required nonzero.  The first equation
gives `(14:00@1)/(37:00@1)=-1`, while the second gives the same ratio as
`1+w`.  Hence `-1=1+w`, with contradiction scalar `-2-w != 0` in
`Q(w)`.  The five-variable localized verifier returns a unit (`std` size one,
`reduce(1,G)=0`).  The full 82-variable localized binomial basis timed out at
120 seconds, but it is unnecessary: the two-row Laurent certificate is exact.

This kills the first sound complete-SMT support witness without a broad
82-variable Gröbner basis.  It does not prove that every SAT support model in
the `1222 k4` packet contains the same two-row obstruction; a sound global
closure would enumerate further canonical SAT models with coefficient
nogoods or derive this ratio conflict from the support clauses.

### Sound gain-circuit CEGAR and complete-gain scaling guard

The learned no-goods are support-conditional.  A circuit cut requires its
literal rows to have *exactly* the two displayed active monomials; a support
which activates an additional monomial in any circuit row is not removed.
This guard is essential, since a bare ban on the union of circuit atoms would
be unsound under support enlargement.

Seven complete-SMT support witnesses have now been checked.  Under the trivial
fixed-seed stabilizer they give seven distinct circuit orbits:

```text
cuts before solve    inclusion-minimal support    mixed rows    toric result
0                    82                            1220          2-row circuit
1                    84                            1186          3-row circuit
2                    85                            1172          3-row circuit
3                    83                            1214          3-row circuit
4                    80                            1126          3-row circuit
5                    86                            1184          3-row circuit
6                    85                            1204          3-row circuit
```

Every target is Laurent-inconsistent before any nonbinomial solve.  The six
three-row certificates have relation `L1` norm three and transformed constant
`-1`.  The sixth post-cut target uses literal rows `01010100@2`,
`01011000@2`, `11000001@4`; the seventh uses `00000011@2`,
`01010101@3`, `01100101@3`.  Thus all observed certificates are inconsistent
gain cycles: one parallel-edge two-cycle and six triangles.  The seventh cut
is frozen; the next cached-base support solve is the only changing bounded
step.

The complete coefficient-gain census is also exact.  Literal coefficients are

```text
1, w, -1-w, 3, 3w, -3-3w,
```

so every binomial gain belongs to
`<3> times mu_6`, isomorphic to `Z times Z/6`; no other norm prime occurs.
There are nine gain values but 1,440,076,617 possible guarded term-pair
states.  A sound linear-size selector/potential SMT was emitted instead: one
real log-3 and one real phase potential per relevant source atom, and one
selector/modular slack packet per literal row.  It contains 690 support
Booleans, 1,367,016 exact monomial definitions, 1,381 mixed selectors, 4,142
Real potentials and 1,381 Int slacks; its byte size is 478,948,314.  Z3 hit the
120-second cap with no output (`exit 124`).  Hence static complete-gain
compilation is sound but not a bounded acceleration; lazy exact SNF-circuit
CEGAR remains the practical route.  Its 81.95 MB support/activation base is
cached byte-for-byte between iterations, so only the guarded circuit
assertions change.

## 9. Carrier-rank and properness scope

Neither base point is pure-normalized, and carrier ranks drop on their sparse
supports.  The archived no-cap locus is torus-invariant at finite points but
not closed under precisely such rank drops.  Therefore attaching a bare
`no-cap` bit to either limit would be unsound.  A valid Luna/Rees branch must
retain a nonzero response minor, its valuation, and the corresponding blocker
membership throughout the arc.

The exact carrier census makes this boundary issue finite.  At `C3+C5`, the
star response ranks have histogram `0:28,1:140`, the triangle ranks have
`0:85,1:475`, and 108 live-pair/rank-zero carriers are active (`28+80`).  At
the phase `K4+K4` base the histograms are

```text
star:     rank 0:24, rank 1:144,
triangle: rank 0:48, rank 1:512.
```

All 72 rank-zero carriers are active.  Their source labels and distinct
positive pivot-valuation variables are frozen in the result.  Consequently
every no-cap arc to the phase base must pass through 72 response-pivot rank
drops; fixed-rank row-space incidence alone cannot follow the limit.

The bounded conclusions are:

- no GHZ leading jet occurs in either first normal image;
- `C3 disjoint_union C5` has a genuine quadratic mixed obstruction but also a
  cubic second-order-blind direction;
- the phase K4 control's quartic and quintic routes are excluded, and its
  first order-six internal/cross response channel is killed by six literal
  order-four cokernel rows;
- direct-polar reinsertion creates a reduced-system column-star point which
  activates all 72 formerly rank-zero carrier pivots, but six omitted literal
  order-two rows kill it; the adjusted polar branch is killed at order three.

Thus neither graph support nor a universal second-variation argument proves
mixed-norm coercivity.  Both the frozen `Haf(L)Haf(R)!=0` antichain and its
`Haf(R)=0` complement are empty, so the phase base admits no binary leading
pure jet through total order six.  The next boundary target begins at order
seven; second-colour and blocker analysis is unnecessary below that order.

## Replay

```sh
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_balanced_base_oddset_luna.py --write-results
python3 -O computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_balanced_base_oddset_luna.py
python3 -I -S computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_balanced_base_oddset_luna.py
Singular computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/verify_phase_m6_symmetrized_product.sing
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/screen_phase_m7_support.py --output computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/results_phase_m7_support_screen_exact.json
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_phase_m7_support_coefficients.py --input computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/results_phase_m7_support_screen_exact.json --output computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/results_phase_m7_support_coefficients_exact.json
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/emit_phase_m7_1222_k4_support_smt.py --satisfy-only --output computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/phase_m7_1222_k4_support_exact_sat.smt2 --manifest computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/manifest_phase_m7_1222_k4_support_exact_sat.json
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/run_phase_m7_1222_k4_sat_witness.py
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_phase_m7_1222_k4_sat_coefficients.py
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_phase_m7_1222_k4_toric.py
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/run_phase_m7_1222_k4_toric_snf.py
Singular computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/verify_phase_m7_1222_k4_two_binomial_unit.sing
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/audit_phase_m7_gain_group.py
python3 computations/unaudited-codex-balanced-base-oddset-luna-2026-08-21/emit_phase_m7_complete_gain_smt.py
# bounded terminal: timeout 120 z3 -smt2 computations/.../phase_m7_1222_k4_complete_gain.smt2
```

Frozen logical digest:
`ea1fced7b806352e982a527da2054c3709a2314cfc5245845748fc4d2fabe1ac`.
