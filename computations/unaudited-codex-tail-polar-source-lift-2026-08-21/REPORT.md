# Source-faithful lowest-tail polar lift

Status: **UNAUDITED exact three-mode PASS; full rank on a literal cofactor
principal open, with the remaining divisor stated explicitly.**

## Global first-Jacobian provenance audit

The complete `380 x 12` matrix is not a literal global Jacobian block away
from the diagonal locus.  Exact row/column replay gives the precise identity

```text
M_380x12(w,e) = (partial F_w / partial A_e) evaluated at T=0.
```

All 380 rows, 1,116 nonzero entries, and 1,620 matching occurrences replay.
The `6+1+1` pivot entries are individually stronger: differentiating the edge
joining the two singleton-colour sites leaves a monochromatic six-site
Hafnian, so those entries are literal global Jacobian coefficients.  Their
full `S8 x S3` transport gives a genuine `168 x 168` minor polynomial on all
off-diagonal source columns; its `T=0` leading term is the product of the 168
displayed pure-colour six-site cofactors.

The `3+3+2` entries are only associated-graded.  The lex-first discrepancy is

```text
row F_00011212, column A_06[0,1]:
retained at T=0: A_12[0,0] A_34[1,1] A_57[2,2],
also present in full J: A_12[0,0] A_35[1,2] A_47[1,2].
```

Thus the 126-orbit rescue/support closure controls the specialized leading
matrix, not the full Jacobian on a remote tail component.

Transporting every fixed-pair slice covers exactly the 168 off-diagonal
source coordinates, each with multiplicity twelve.  The global support graph
has maximum matching 168, already witnessed by the `6+1+1` pivot rows.  At a
diagonal source `im G_A` is supported entirely in the other 84 diagonal
coordinates, so quotienting by `T0` changes neither this rank nor its absolute
168-column cap.  Consequently these matrices cannot force
`rank(J_A)-s>=232`; they stop 64 columns short.  Adding a diagonal quotient
block is a new argument, and equivariance caps the full exact-GHZ quotient at
231.

The smallest possible promotion would be a global saturation proving that
the exact `X5+blocked` ideal forces `T=0`, followed by a separate diagonal
quotient-Jacobian calculation.  The frozen filtered-lift audit explicitly
shows why initial rank alone cannot supply that saturation.

Provenance checker logical digest:
`a7688fd03d986286152a38da3e329b65324648ae7b03a7d989b3b415b0841c30`.

## Exact theorem

Fix the ordered `01` endpoint-star columns

```text
y_a = a_a6^01,  z_a = a_a7^01,  0 <= a < 6,
```

and retain three independent same-colour diagonal graphs `G0,G1,G2`.
After taking the lowest off-diagonal weight and killing only the other
off-diagonal columns, the literal raw source rows with profiles `7+1`,
`6+1+1`, and `3+3+2` give a `380 x 12` matrix:

```text
7+1       8 rows
6+1+1    12 rows
3+3+2   360 rows
```

The matrix has rank 12 over `Q(G0,G1,G2)`.  More strongly, its twelve
`6+1+1` rows are already diagonal.  For `t in {6,7}` and `0 <= a < 6`, let

```text
h_at^(2) = Haf(G2 on {0,...,7}\{a,t}).
```

The exact source label having colour 0 at `a`, colour 1 at `t`, and colour
2 at the other six sites satisfies

```text
in_1(F_[a:0,t:1,others:2]) = h_at^(2) * (y_a or z_a).
```

Consequently the literal maximal minor is

```text
D611 = product_{a=0}^5 h_a6^(2) h_a7^(2).
```

On the principal open `D611 != 0`, all twelve endpoint-star cells lie in the
localized lowest source ideal.  This is the requested source-faithful tail
elimination lemma on that open; it uses actual eight-site coefficient rows,
not formal derivatives of one quadratic row.

An independent 105-perfect-matching engine replays all 1,620 retained
linear matching occurrences and matches every compact coefficient exactly.

The result JSON freezes all 380 source labels and every nonzero retained
coefficient.  It also freezes one explicit `12 x 12` `3+3+2` redundancy
minor:

```text
16 * product_a(g0_a6*g0_a7)
   * g1_01^6*g1_03^2*g1_13^2*g1_23^2
   * g2_23^2*g2_24^2*g2_25^2*g2_45^6.
```

This second minor proves generic rank independently, but its vanishing is
not asserted to be the rank-drop locus of the full 360-row submatrix.

## What the two `7+1` rows actually supply

For the frozen support-six response chart, write `Pz=C*y`, `Py=C*z`.
The tail-edge cofactor is zero, so the seventh possible cross cell does not
contaminate the quotient.  The two majority-zero rows are exactly

```text
in_1(F_00000010) = -4*y1 = d7^T*Pz = Pz0+Pz2+Pz4,
in_1(F_00000001) =  4*z0 = d6^T*Py = -Py1-Py3-Py5.
```

Their rank in the twelve polar coordinates is 2 and their kernel has
dimension 10.  Thus they do not justify treating all twelve formal polars
as source rows.  The `6+1+1` rows repair exactly this provenance gap on
`D611 != 0`.

The stored `C^{-1}` gives all twelve conditional identities

```text
z = C^-1*Py,  y = C^-1*Pz.
```

Here `det(C)=-64`.  After endpoint-orientation pairing, the symmetric and
antisymmetric blocks are `C` and `-C`; the `12 x 12` Hessian has determinant
`4096`, rank 12, and zero kernel.

## Covariance and the remaining boundary

All 384 elements of `C2^4 semidirect S4` were replayed, including entrywise
`C -> P*C*P^T`; every determinant is `-64`.  The twelve factors of `D611`
form one orbit under the fixed-tail stabilizer (and under full `B4`
transport).  Therefore the complement reduces to one representative
cofactor-zero divisor, but it is not yet closed generically.

The support-six point lies on this complement: ten of its twelve fixed-tail
cofactors vanish.  Its existing arbitrary-mate unit separately excludes a
compatible diagonal mate.  There is no frozen compatible three-colour
diagonal triple on which to specialize the remaining symbolic rank problem;
setting all three graphs equal to support-six would be unsound.  The precise
remaining tail-lift gate is therefore the generic single-cofactor divisor,
where the `7+1/3+3+2` rank depends on the other two independent diagonal
graphs and must be combined with the diagonal packet.

Mutation guards delete one `6+1+1` row, alter one `7+1` direction, alter one
selected `3+3+2` coefficient, and change the response determinant from
`-64` to `-36`; all fire.

## Generic single-cofactor boundary

The first complement stratum is now exact at the source-row level.  By the
fixed-tail stabilizer take the missing factor to be

```text
h2_06 = Haf(G2 on {1,2,3,4,5,7}) = 0
```

and invert the other eleven `h2_at`; call their product `Dhat`.  Those rows
give eleven coordinate pivots.  Modulo their span, every other row is
measured only by its coefficient in the missing column `y0`.

The complete missing-column ideal is

```text
J06 = (h0_06, h1_06,
       g0_A*g1_B*g2_C for all 90 ordered pair partitions
       A sqcup B sqcup C = {1,2,3,4,5,7}).
```

The first two generators come from the literal rows `F_00000010` and
`F_01111111`; the other 90 come from exactly the `3+3+2` words containing
`a_06^01`.  An independent 105-matching extraction replays every
coefficient.  For every generator `q`, adjoining its row to the eleven
pivots gives the exact maximal minor

```text
+/- Dhat*q.
```

Therefore, on `h2_06=0,Dhat!=0`, the source map has rank 12 exactly off
`V(J06)` and rank 11 exactly on `V(J06)`.

The 92 coefficients have gcd one.  In particular the generic
single-cofactor divisor has no divisorial rank-drop component: `J06` already
contains the coprime independent-colour cofactors `h0_06,h1_06`.  The first
possible rank-drop locus is codimension at least two inside `h2_06=0`
(codimension at least three in the independent-graph ambient space), not a
next divisor.

After normalizing the four anchor edges, the 90 tricolour coefficients give
87 distinct monomials:

```text
degree 1: 3,   degree 2: 24,   degree 3: 60.
```

The three linear generators are `g0_17,g1_17,g2_17`, each with two literal
source labels.  If they also vanish, exactly 72 monomial conditions remain:
24 quadrics and 48 cubics.  Thus the sharp residual is

```text
h2_06=h0_06=h1_06=g0_17=g1_17=g2_17=0,
72 remaining normalized 3+3+2 monomials = 0,
Dhat != 0.
```

This description transports to all twelve single missing factors.  It is a
rank theorem, not yet a proof that the diagonal packet avoids the displayed
codimension-at-least-two residual.  The companion checker/result logical
digest is

```text
e98ff441ead785676089d2986ef62704467f0bd93a9db117836524e9d42639fe
```

## Exact closure of the one-missing-cofactor chart

The normalized 90 matching monomials have now been classified without a
Groebner basis.  The three singleton generators first force
`g0_17=g1_17=g2_17=0`; the remaining 72 minimal monomials form a hypergraph
with exactly 6,635 minimal transversals.  Including the three forced
variables, their prime-height census is

```text
15:2, 18:4, 19:27, 20:420, 21:708, 22:624,
23:1416, 24:912, 25:1836, 26:624, 27:62.
```

Under the order-16 stabilizer of the unordered pair `{0,6}`, these are 527
orbits, with orbit-size histogram

```text
1:3, 2:8, 4:38, 8:148, 16:330.
```

Every representative was filtered against the literal monomial supports of
all six permanent and four reduced triangle rows in each colour, and against
the already-imposed zero-target cofactors `h0_06,h1_06,h2_06`.  A nonzero-
target row with no live monomial, or a zero-target row with exactly one live
monomial, cannot vanish.  This rejects 526 of the 527 orbits.

The sole packet-level survivor has height 18, orbit size four, and the same
six zeros in every colour:

```text
{12,14,17,24,27,47}.
```

For each colour, every permanent then has one live product, every triangle
has two live monomials, and `h_c,06` has no live monomial.  But the chart also
inverts the other eleven colour-2 pivots.  A literal 15-matching replay gives

```text
(h2_06,h2_16,h2_26,h2_36,h2_46,h2_56) live-term counts
    = (0,6,6,0,6,0),
(h2_07,h2_17,h2_27,h2_37,h2_47,h2_57) live-term counts
    = (6,12,12,6,12,6).
```

Thus `h2_36=h2_56=0` identically on the last support, contradicting the
`Dhat != 0` localization.  Hence **no minimal-prime orbit meets the declared
single-cofactor chart**.  This closes the generic exactly-one-zero cofactor
stratum source-faithfully; no coefficient solve or arbitrary-mate unit is
needed.  The minimal-prime and support-filter logical digests are

```text
af23ec140df2b126af7195b65aff62f9f489805e4509328794438c98a80efc8c
a8a02aad70e39345ae578dd8c67c332e6ee04dc36a2428fb79100ccaeb50f100
```

## Two- and three-missing-cofactor generic screen

The fixed-tail stabilizer has order 96.  Its action on the twelve cofactor
columns has five orbits on two-element zero sets and seven on three-element
zero sets.  In column order `y0,...,y5,z0,...,z5`, representatives and
labelled orbit sizes are

```text
size 2:
  (y0,y1)/6, (y0,y2)/24, (y0,z0)/6,
  (y0,z1)/6, (y0,z2)/24.

size 3:
  (y0,y1,y2)/24, (y0,y1,z0)/12, (y0,y1,z2)/24,
  (y0,y2,y4)/16, (y0,y2,z0)/48, (y0,y2,z1)/48,
  (y0,y2,z4)/48.
```

A bounded exact finite-field screen specializes each representative at
`p=1009` and `p=1013`.  For each specialization it solves precisely the
chosen Hafnian equations as a linear system in pairwise-incident graph
edges, rejects samples where any remaining `6+1+1` cofactor vanishes, and
then ranks the literal `7+1` plus `3+3+2` source rows on the missing columns.
Every size-two representative has rank two and every size-three
representative has rank three; there are no generically rank-deficient
representatives in this screen.

This is deliberately not a Fitting-ideal closure.  It proves a full-rank
open on the sampled cofactor-intersection components, but does not exclude
lower-rank closed subvarieties or certify that every irreducible component
was sampled.  The three-mode logical digest is

```text
03a01ad9f8793dac8bd6c06242831ced622e10a72bf5e7735e3f1c2f60c3a844
```

The modular observation has an exact source-row lift.  For every one of the
twelve representatives, literal `7+1` rows alone give a permutation-
triangular missing-column minor.  Each determinant is a product of two or
three irreducible six-site Hafnians from `G0,G1`, hence is independent of the
selected `G2` cofactor equations.  The expanded term counts for the five
size-two representatives are `210,210,225,222,222`; for the seven size-three
representatives they are `2500,3150,3021,2500,3150,3021,3021`.  Multiplying
only by the remaining localized `G2` pivots gives the literal full `12 x 12`
minor.  The exact three-mode digest is

```text
083275d38d883473e55310818205a17d23ead605b7a6c3e86251526a2632ccfc
```

## Global `6+1+1` plus `7+1` Hall criterion

Write `h^c_at=Haf(Gc on V\{a,t})`.  The complete twenty-row submatrix has
the following sparse form:

```text
Dya: h2_a6*y_a                 (six diagonal 611 rows)
Dza: h2_a7*z_a                 (six diagonal 611 rows)
Y:   sum_a h0_a6*y_a           (F_00000010)
Z:   sum_a h0_a7*z_a           (F_00000001)
Ea:  h1_a6*y_a+h1_a7*z_a       (six exceptional-site 71 rows).
```

The `Y` and `Z` channels are each one shared row, not six independent
pivots.  After quotienting the live `611` rows, a missing `y_a` is adjacent
to `Y,Ea`, while a missing `z_a` is adjacent to `Z,Ea`.  If `d` is the
number of residual sites for which both columns are missing, the structural
missing-column rank with all displayed channel cofactors live is exactly

```text
|S| - max(0,d-2).
```

Equivalently an SDR exists exactly when `d<=2`.  At specialized coefficient
points Hall's inequalities are applied after deleting every zero-labelled
edge.  An SDR is a generic support criterion: cyclic matchings can still
cancel numerically.  For two doubled sites `a,b` the controlling literal
minor is

```text
Delta_ab = h0_a6*h0_b7*h1_a7*h1_b6
         - h0_b6*h0_a7*h1_a6*h1_b7.
```

It has raw degree 12 and 91,368 expanded terms.  The 4,096 missing-column
sets form 126 fixed-tail orbits: 66 have `d<=1`, 33 have `d=2` and are full
off a `Delta_ab` divisor, and 27 have the structural Hall defect `d>=3`.

Four exact `3+3+2` rescue minors are frozen.  For the two minimal doubled
patterns they are

```text
{0,1}:  g0_23*g1_14*g2_57*h0_16*h0_17*h1_07,
{0,2}:  g0_13*g1_24*g2_57*h0_26*h0_27*h1_07,
```

each with 3,150 expanded terms.  The two smallest Hall-defect orbits are
the three doubled residual sites `{0,1,2}` and `{0,2,4}`.  One literal 332
row restores the missing sixth rank generically, with determinants

```text
{0,1,2}: -g0_34*g1_12*g2_57*h1_07*Delta_12,
{0,2,4}: -g0_13*g1_24*g2_57*h1_07*Delta_24.
```

Each expands to 1,226,124 terms.  These name the next exact factor divisors;
they do not close them or the larger Hall-defect patterns.  The source,
formal-determinant, term-profile, orbit, mutation and three-mode digest is

```text
6d55fe4a761cc60665268e1ebfa61215390b6994134749b7fa6fe5610f2b4ad2
```

## Terminal generic tail-response coverage

The four seed rescues and their literal order-96 fixed-tail transports cover
all 33 two-double orbits and all 16 three-double Hall orbits on their named
factor opens.  The two minimal four-double shapes have exact two-rescue
minors

```text
Theta_220 = M_220 * Delta_23,
Theta_211 = M_211 * Delta_24.
```

Adding one transported rescue row at each subsequent layer gives

```text
Theta_221 = M_221 * Delta_23 * Lambda^UV_04,
Theta_222 = M_222 * Delta_23 * Omega_015,
```

where `Omega_015` is the literal seven-term primitive stored in
`results_332_larger_rescue_thetas.json`. Sparse exact full determinants of
sizes 8, 10, and 12 replay the reduced determinants; no sampled rank screen
is used. Therefore all 126 missing-pattern orbits have a finite exact
principal-open certificate: 66 SDR, 33 Delta-layer, and Hall layers
`16+8+2+1` for `d=3,4,5,6`.

The remaining recursion is the finite four-family antichain

```text
support monomials, Delta_sep, Lambda^UV_sep, Omega_015.
```

The support family has four factor orbits and routes to smaller support
charts, with existing mate units firing only when their exact joint
signatures match. The other three are genuinely new coefficient boundaries
and are not declared closed. The terminal three-mode theorem digest is

```text
c7c0c3144efca8ad4181e94cd11127c27e64defea9c73c08a2889a38bee46dbf
```

## Exact closure of the nonmonomial tail boundaries

The preceding `Delta/Lambda/Omega` antichain was an artifact of retaining
both 7+1 channel rows in every maximal minor.  Literal full-source minors
which retain only one channel row give support monomials for every canonical
Hall shape with three, four, or five doubled sites.  In particular, the
simultaneous `Delta` locus is harmless: the redundant channel row is omitted
and one additional 332 row restores rank.

For all six doubled sites, one channel plus five literal 332 rows gives

```text
M * Xi_05,
Xi_05 = U0*V5*g0_07*g0_56 - U5*V0*g0_06*g0_57.
```

Six literal 332 rows and no channel row give, after one exact order-96
transport,

```text
N * Sigma_05,
Sigma_05 = U0*V5*g0_07*g0_56 + U5*V0*g0_06*g0_57.
```

Thus `Xi_05=Sigma_05=0` would force twice a live support monomial to vanish,
which is impossible over Q.  The cross-block pairs form one 12-element orbit,
and all coefficients of every selected row were replayed under all 96
fixed-tail actions.  Consequently `Delta_sep`, `Lambda^UV_sep`, and
`Omega_015` are removed entirely from the recursive divisor antichain.  The
only remaining tail boundaries are the four support-monomial orbits, routed
to the smaller cofactor/edge-support charts.  The exact audit is
`audit_tail_nonmonomial_boundary_closure.py` and its frozen digest is recorded
in `results_tail_nonmonomial_boundary_closure.json`.

## Replay

```sh
.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_polar_source_lift.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_polar_source_lift.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_polar_source_lift.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_cofactor_boundary.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_cofactor_boundary.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_cofactor_boundary.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_boundary_monomial_primes.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_boundary_monomial_primes.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_single_boundary_monomial_primes.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_prime_support_filter.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_prime_support_filter.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_prime_support_filter.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_generic_rank_screen.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_generic_rank_screen.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_generic_rank_screen.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_exact_minors.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_exact_minors.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_multi_cofactor_exact_minors.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_611_71_sdr_and_332_rescue.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_611_71_sdr_and_332_rescue.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_611_71_sdr_and_332_rescue.py

.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_332_rescue_orbit_cover.py --write-results
.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_332_two_rescue_thetas.py --write-results
.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_332_larger_rescue_thetas.py --write-results
.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_response_rescue_theorem.py --write-results
.venv/bin/python computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_nonmonomial_boundary_closure.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_nonmonomial_boundary_closure.py
.venv/bin/python -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_nonmonomial_boundary_closure.py
```

All three runs return logical digest

```text
273c321313d8bea2dcd3ea19fe282c078dcfa481d956839607db35100a7612b9
```

## Exhaustive support-boundary terminal

`audit_tail_support_boundary_orbits.py` closes the four support-factor
orbits left by the nonmonomial tail theorem.  The representative faces and
routes are:

```text
h2_06 = 0 : frozen 6,635-prime / 527-orbit chain, 0 localized survivors
g0_01 = 0 : empty because g0_01 is a normalized anchor
g0_02 = 0 : exact cross-support / triangular-source census
g0_06 = 0 : exact cross-support / triangular-source census
```

In one colour the six permanent and four reduced-triangle support rules
leave 112,473 exact cross supports.  Their upward-closed family has 1,224
minimal members, in 19 order-96 fixed-tail orbits, with sizes
`12:8, 13:96, 14:864, 15:256`.  Every size-13-or-larger minimum exposes all
twelve 6+1+1 pivots.  Fixing the unique size-12 orbit for the third colour
leaves exactly 125,956 simultaneous `(G0,G1)` orbit representatives; 125,955
have a unique triangular 12-row literal source minor.  The one deficient
representative is the aligned size-12 triple.

The labelled size-12 census is `504` full-rank nonaligned triples and `8`
rank-six aligned triples.  On each of the eight aligned supports the reduced
triangles form four reciprocal Laurent binomials `Y-Y^-1=2`.  The exact
relation leaves six root branches per support, hence **48**, not 24.  A
must-fire mutation rejects the old count.  All 48 have pure Hafnian `H=4`,
and every full `(X,C,Q,H)` record is explicitly transported and
anchor-preserving-gauged to the frozen support-six point.  The existing
fixed-left arbitrary-mate unit therefore excludes the aligned triple.

Thus every chartwise tail-rank support boundary is closed.  No tail-response
divisor survives on the anchor-normalized diagonal chart; the remaining
proof obligation is the global carrier/idempotent lift.

Frozen artifacts:

```text
audit_tail_support_boundary_orbits.py
results_tail_support_boundary_orbits.json
results_tail_support_boundary_orbits_modes.json
logical SHA 0c3b6f7afc1cafdb0e6f516c8cd1d0295e194a4a87203f2ddc206c5bc9373392
matching-ledger SHA 9fd83c462cee829fac3c8d6854448491216e0621a34548f6bb80e49d7823c311
```

Replay:

```text
python3 computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_support_boundary_orbits.py --rank-scan joint --write-results
python3 -O computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_support_boundary_orbits.py --rank-scan joint
python3 -I -S computations/unaudited-codex-tail-polar-source-lift-2026-08-21/audit_tail_support_boundary_orbits.py --rank-scan joint
```
