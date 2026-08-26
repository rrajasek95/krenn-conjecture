# Source-level audit and attack synthesis

Status: **UNAUDITED WORKING SYNTHESIS, 2026-08-20.**  This document does not
change the certified spine.  It records the outcome of a deliberately
adversarial proof-search wave conducted directly in the endpoint-ordered
matching coefficient system.

## 1. What is genuinely available

The reliable global skeleton is short:

1. Palette restriction reduces every upper-bound question to three colours.
2. The arbitrary bicoloured `N=6,d=3` system is empty.
3. An active clean pair gives exact descent `N -> N-2`.
4. Therefore a source-level theorem producing an active clean pair, or a
   literal source contradiction, from every minimal counterexample would
   finish the induction.

The general bicoloured `N=8,d=3` case is still open.  The diagonal `N=8`
case, the six-site base, and clean-pair descent do not fill this gap.  The
uniform `PAComp(h)` architecture in `PROOF-SKETCH.md` is conditional: its
physical comparison, branch coverage, and promotion back to the actual
source ideal are precisely the unproved arrows.  Auxiliary homological
classes are not accepted terminals unless a literal map to a source unit,
an active clean cap, or a valid support reduction is displayed.

## 2. Audit corrections that change the attack

* Extremality must be ordered as global minimum occupied-cell support first,
  then maximum anchors inside that stratum.  No audited theorem identifies
  this with the repository's frequent maximum-anchor-first choice.
* The stored A1 13-cell phase object is only a partial mixed-row solution with
  pure values `(1,0,0)`, and a pure-neutral one-parameter subgroup deletes
  two of its cells.  It does not refute all-moduli-one on a hypothetical
  minimum full exact source.  The correct verdict is that phase-only
  normalization is unproved and its stored justification is invalid.
* Three compatible exact binary restrictions do not force ternary exactness.
  The W40 four-torus satisfies all three binary systems and all 4,881 level-4
  rows, while exactly three `(3,3,2)` rows fail.  Any proof consuming only
  binary rows is therefore impossible.
* The advertised 13-exit lift is not a closed 13-term packet.  Its raw
  eight-site expansion has two parent terms, 13 tail-sector exits, and 90
  crossing occurrences grouped into 45 physical responses.

These corrections remove the two easiest-looking normalization shortcuts
and force the next theorem to use genuine trichromatic equations.

## 3. First-wave exact results

### 3.1 Binary compatibility route: refuted

There is an explicit four-dimensional Laurent torus of compatible exact
binary restrictions satisfying all level-4 equations.  Its only full-system
defects are

```text
01110222 = 1/(s*a*b),   12221000 = s*b,   20002111 = -a.
```

Thus binary/nullgraph compatibility cannot be a standalone obstruction.
The raw 105-matching and independent recursive engines agree on all 6,561
words.  See
`../unaudited-codex-binary-compat-2026-08-20/REPORT.md`.

### 3.2 Fixed twisted-4+4 branch: obstructed over every field

For the displayed W33-D5 endpoint-ordered binary representative, no ternary
completion can satisfy the full eight-site equations.  A division-free
triangular proof uses 21 word equations: twelve literal zeros and one
binomial kill thirteen auxiliary variables; seven rows then kill
`A_0j[2,2]` for every `j`; the pure `22222222` row becomes `0=1`.  Exactly
two of the seven pivots have profile `(3,3,2)`.

An independent checker rebuilt the 105 matchings and the 21 equations from
scratch and verified the 781-term integer certificate in standard, `-O`,
and `-I -S` modes.  It found one required metadata correction: the stored
multipliers certify the equations after canonical per-generator sign
normalization.  Applied literally to `H_w-delta_w`, they leave a 346-term
residual.  Multiplying equations by these recorded unit signs leaves the
theorem unchanged, but the certificate metadata must be fixed before
promotion.

The audited scope is the fixed representative and its target-preserving
diagonal-gauge, site-permutation, and global-palette-relabeling orbit.  A
separate classification is required before calling the whole combinatorial
twisted-4+4 stratum closed.  See
`../unaudited-codex-audit-twisted44-2026-08-20/REPORT.md`.

### 3.3 The W40 boundary has many explicit caps

Every point of the W40 Laurent four-torus has six active response-star caps
with `K=I_3`.  At the integral point, exact saturation finds seven active and
ten blocked live pairs.  In particular, for pair `67`, all response cells
are incident with residual site `5`; hence `r^2=0` and the exact clean error
vanishes.  W25-F8 remains the calibrated all-blocked lower-rung object, but
it is only level 3 and fails 78 level-4 rows, so it is not a counterexample
to the new target.

### 3.4 W40 is locally rigid modulo gauge (independently audited)

At the integral W40 point the raw level-4 Jacobian has rank `240/252`, with
a displayed rank minor of determinant `2^33`.  The normalized
target-preserving diagonal-gauge orbit has dimension 12, its tangent lies in
the Jacobian kernel, and a gauge rank minor has determinant `-1`.  A no-import
independent reconstruction confirmed these ranks, cap covariance, and the
algebraic-geometric inference in standard, `-O`, and `-I -S` modes.  Thus
W40 is a smooth characteristic-zero point whose local level-4 scheme germ is
its gauge-orbit germ.  A nearby all-blocked deformation cannot be obtained
from W40; a falsifier must be remote, singular, or on another component.
See `../unaudited-codex-audit-x4-local-rigidity-2026-08-20/REPORT.md`.

### 3.5 The fixed W40 support is globally one capped torus

Fix the twenty live endpoint-ordered cells of W40, set the other 232 cells to
zero, and invert those twenty values.  A fresh all-row reconstruction leaves
only twelve nonzero binomials, reducing to ten Laurent relations of rank
eight.  Eight relations have an exponent minor of determinant `+1`, while
the two remaining relations have explicit integer dependencies.  Hence over
every field the entire open fixed-support X4 stratum is a split
12-dimensional torus with no hidden torsion component.  A complementary
gauge minor has determinant `-1`, so this torus is exactly the
target-preserving diagonal-gauge orbit, globally rather than only near the
integral point.

Every point of this torus has the structural active cap `(67,K=I_3)`: its
four response cells lie on the residual star at site 5 and its direct scalar
is the inverted cell `A_67[0,0]`.  All 729 clean-error coefficients vanish.
This closes the open fixed support, but says nothing about activating any of
the other 232 cells.  See
`../unaudited-codex-w40-support-global-2026-08-20/REPORT.md`.

## 4. The immediate theorem to attack

Define `X4` at `N=8` by the three pure equations and all mixed equations of
off-count at most four.  Full exactness implies `X4`.  The cleanest sufficient
statement is

> **X4-to-cap.** Every endpoint-ordered ternary `N=8` point of `X4` has an
> active clean pair.

This is strictly stronger than needed but correctly calibrated: W25 is below
the hypothesis, while the nonempty W40 torus satisfies the conclusion.  A
proof of X4-to-cap plus certified descent and the six-site theorem settles
the general bicoloured `N=8,d=3` case.

For pair `p,q`, let `R_ab(K)` be the response block, linear in the nine cap
coordinates.  If its residual-edge support has matching number at most one,
then every two response terms meet, so `r^2=0` and the full cap error is zero.
An intersecting edge family is contained either in a star or in a triangle.
For each of the 168 pair/star choices and 560 pair/triangle choices, killing
all response cells outside that support is a linear map `L: F^9 -> F^m`.
Over an infinite field its kernel contains an active cap exactly when none of

```text
K_00, K_11, K_22, <K,A_pq>
```

belongs to `rowspan(L)`.  This converts the cubic cap search into 728 finite
row-space alternatives.  W40 passes six star alternatives; W25 passes none
of the star or triangle alternatives.  The universal residual is now exact:
prove from the raw X4 rows that at least one alternative passes, or construct
an X4 point on which every alternative fails.

### 4.1 Branch-free form of the blocker residual

The four-way blocker choice at each carrier can be removed.  Let `W_C` be
the carrier row space in the nine-dimensional cap dual and put

```text
q_pq = K_00 K_11 K_22 <K,A_pq>.
```

Over the target infinite field, carrier `C` fails exactly when

```text
q_pq in W_C * Sym^3((F^9)*).                           (B)
```

Restriction to `ker L_C` turns `q_pq` into a product of four linear forms in
a polynomial domain; it vanishes identically exactly when one factor
vanishes.  Simultaneous failure is therefore 728 single quartic membership
conditions, not `4^728` blocker assignments.  Site and colour covariance
reduce the formulas to two templates: `(01; star-centre 2)` and
`(01; triangle 234)`.

Literal X4 expansion also gives 219 shared slice identities for each pair.
For a residual six-letter word `z` having a colour of multiplicity at least
four,

```text
delta_z = H6(z) s_pq
          + sum_ab H4(z without a,b) rho_ab(z_a,z_b).  (S)
```

Modulo `W_C`, only the five star edges or three triangle edges allowed by the
carrier survive.  For a globally minimum full exact source the resulting
honest residual is

```text
X4 intersect R_car intersect BAL intersect PURE-LIVE
   intersect NO-SINGLETON-(3,3,2).
```

The compression and all `28*219=6,132` slice identities pass exact W40/W25
calibrations in three execution modes.  This is an exact reduction, not an
emptiness theorem.  See
`../unaudited-codex-x4-blocker-compressor-2026-08-20/REPORT.md`.

### 4.2 The full-only shell is exactly 510 response packets

For each fixed pair, the 510 residual six-site words not covered by `(S)`
carry all 1,680 missing full-source coefficients exactly once.  Their packet
types are

```text
(3,3,0):  60 packets x 1 missing endpoint slot,
(3,2,1): 360 packets x 3 missing endpoint slots,
(2,2,2):  90 packets x 6 missing endpoint slots.
```

Equivalently, the full-only rows are precisely the eight-site words of
profile `(3,3,2)`.  Over an integral domain an exact source cannot have one
of these rows supported by exactly one perfect matching, since its amplitude
would then be a product of four nonzero source cells.  This gives the exact
support condition `NO-SINGLETON-(3,3,2)` used above.

The condition is useful but not globally decisive.  It kills the W40 open
support with any one of three unit monomial rows and kills the W25 open
support with twenty such rows.  On the other hand, the four named endpoint-
cell supports `m=25,26,27,28` from the W8/W15 family satisfy balance, pure
liveness, and have no mixed singleton at all; their smallest central fibre
sizes are respectively `8,11,12,16`.  Thus the residual cannot be closed by
support-only refinements of these three conditions.  Coefficient-level X4
or carrier equations are indispensable.  See
`../unaudited-codex-n8-trichromatic-residual-2026-08-20/REPORT.md`.

The first of those four support survivors is now closed at precisely that
coefficient level.  On the full 129-cell `m=25` open support, five literal
mixed X4 rows give a Laurent-unit certificate.  Three matched rows force

```text
D = A_56[y5,0] A_67[1,y7] - A_56[y5,1] A_67[0,y7] = 0
```

because `D` times a live four-cell prefactor lies in their row ideal.  Two
more X4 rows give `D*Q` plus a live five-cell monomial.  Eliminating `D`
therefore puts a product of nine inverted support cells in the ideal.  The
combined sparse identity has zero residual and is valid over every integral
domain.  It closes only this named open support, but demonstrates the needed
coefficient mechanism despite every raw mixed fibre having at least eight
matching terms.

### 4.3 What quotient rank and pure skeletons do -- and do not -- force

W40 has blocked star/triangle carriers in every quotient dimension from zero
through seven.  Consequently no theorem depending only on the rank of one
carrier quotient can force activity in those dimensions; the projected
identities must be coupled across carriers or with source coefficients.

A weaker global support consequence survives.  Choose one live pure perfect
matching in each colour.  If all carriers are blocked, then for every edge
of the selected triple the potential response-arm graph on the other six
sites must contain two disjoint edges.  Otherwise that graph is contained in
a star or triangle, all forbidden atomic response blocks are support-zero,
and a generic cap is active.  Across the 31 `S8 x S3` pure-matching orbits,
exact monotone augmentation gives minimum occupied physical-pair counts
between 12 and 16.  This closes only the very sparse physical graphs; it is a
necessary support floor, not the missing coefficient theorem.

The selected matching triples admit a sharper response-geometry split.
For a selected edge, the other two colours force zero, one, or two residual
response edges.  Two response edges may coincide, meet in one vertex, or be
disjoint.  Exactly four zero-based `S8 x S3` orbits, numbered
`25,26,27,28` in the fresh quotient census, have two disjoint forced
responses at all twelve selected occurrences.  These correspond to legacy
one-based chart numbers `28,29,30,31`, not legacy charts 25/26.  The other
27 charts have at least one selected occurrence whose forced response graph
fits a star or triangle and should be attacked by the complete family of
containing carriers.

Chart coordinates must retain one further invariant.  Target-preserving
site-colour diagonal gauge cannot set all twelve selected pure cells to one:
the product of the four selected cells in each colour is gauge-invariant.
One may normalize three cells per colour and retain the fourth product
`m_c != 0`, or keep all twelve anchors as named nonzero variables.  Setting
all twelve to one is sound only under an additional unique-pure/product-one
hypothesis and is not used here.

### 4.4 Two proposed bridges have now been sharply separated

The local slice-rank shortcut is false.  An isolated three-row packet with
one live spike forces the associated `3 x n` slice matrix to have full row
rank, but there is no certified map from its column relation to a nine-entry
cap covector.  A raw `m=26` specialization over `F_13`, with all 138 support
cells nonzero, realizes a full-rank `3 x 3` packet while the natural
pair/star forbidden-response matrix has rank nine.  Its cap kernel is zero.
Thus neither full slice rank nor the presence of a canonical star supplies
an active clean cap without additional global X4 coupling.

The source-ideal filtration does make exact progress on the four all-disjoint
charts.  Let `K` be the ideal of the 240 non-anchor endpoint cells, retaining
the twelve selected pure cells as named units.  For zero-based charts
`25,26,27,28`, exact integer source-labelled certificates first give

```text
H0 H1 H2 in I_mix + K^3
```

using respectively `55,41,41,41` columns.  Their signed degree-three
residuals have respectively `227,170,164,164` rows.  Charts 25--27 admit
direct literal pivots; chart 28 needs one exact two-column degree-two kernel
correction before the remaining rows pivot.  This yields

```text
H0 H1 H2 in I_mix + K^4
```

with integral certificates of `282,211,205,207` generators.  Most new
coefficients are `+/-1`, with three `-2` coefficients on chart 25.  This is
not yet localized emptiness: degree four may contain a dual obstruction or
require a target/support power.  It is, however, a
source-faithful contraction through the first three off-anchor layers and is
currently the strongest uniform mechanism on the genuinely dangerous charts.

The next layer also lifts after the complete lower-kernel transfer is kept.
Literal integral certificates now prove

```text
H0 H1 H2 in I_mix + K^5
```

on all four charts.  The certificate sizes for zero-based `25,26,27,28`
(legacy `28,29,30,31`) are respectively
`1,958,1,721,3,793,1,971` terms.  Before the lower transfer their hard
degree-four quotient dimensions are `126,0,190,2`; the nonzero quotients are
therefore genuine coupling interfaces, not terminal dual obstructions.  The
producer's exact replay digest is
`f67388de6f1af3321937ac01077e781bca6b72ccae1f7d1fae8160f726d0beeb`.
An independent raw reconstruction found different, smaller integral
certificates of sizes `2,113,1,635,1,963,1,696` and replayed them under
standard, `-O`, `-I`, and `-S` modes with ledger digest beginning
`e457af40`; see
`../unaudited-codex-dangerous-chart-d4-independent-2026-08-20/REPORT.md`.

Zero-based chart 26 / legacy chart 29 has advanced one layer farther.  An
orbit-weighted Schur calculation, after correcting both a lost-multiplicity
bug and the historical early-stop quotient bug, gives an exact labelled
certificate for

```text
H0 H1 H2 in I_mix + K^6.
```

The coupled degree-five quotient has 257 row orbits and rank 215, leaving 42
Schur coordinates.  The cumulative Schur system has rank `1239/1243` modulo
1009 with the target in its image; a centered solution expands to literal
rational rows.  The final certificate uses 2,041 orbit-average terms and
passes standard, `-O`, and `-I -S` replay with digest
`2c7e35f08ed2932cd99e4df4deb603625f55439281a69ac15759f7ad9b412f5c`.
Anchor degrees six through twelve remain open.
An independent referee expanded all 2,041 orbit averages over the sixteen
stabilizer elements and checked exact equality on 3,049 actual target rows;
sign and orbit-deduplication mutations both fire (independent ledger prefix
`a5f84c09`).

The anchor ladder itself has also been independently audited.  The complete
degree-twelve source family consists implicitly of all 6,558 mixed generators
times all degree-eight monomials in 252 cells.  Multiplicity-aware incident
closure is sufficient on each connected component, invariant quotients lift
over `Q`, and `K_anchor^13` has no degree-twelve part.  Therefore a lift
through `K_anchor^13` is literal exponent-one membership, not merely a formal
statement.  Executable regressions reject set-valued orbit outputs and staged
early-stop reduction.  See
`../unaudited-codex-anchor-k-methodology-referee-2026-08-20/REPORT.md`.

Legacy chart 27 / zero-based chart 30 now also reaches `K_anchor^6`.
Its direct degree-five extension leaves 226 bipartite quotient components,
80 of which meet the frozen tail, but the full lower-syzygy transfer repairs
them.  A 3,905-by-13,818 augmented sparse system has exact rank 3,864; an
exact 331-by-331 core minor has determinant 32.  The resulting 549-term
Schur solution completes to a 4,293-term six-transform certificate and
replays every labelled monomial row over `Q` (digest
`1dc739a4ef4ef5c2e0e6d89d3621d15e0c547a0eaf4802bcc1f87b800e6a3097`).
Standard, `-O`, and `-I -S` runs have identical labelled replay digest
`03f30aed3c24f99b38da050a1c5f1cec3a15089e4ad51aa1d29444781dbb9b45`.
Anchor degrees six through twelve remain open here as well.

### 4.5 Rust acceleration keeps discovery separate from proof

The large orbit closures and sparse Schur systems are now passed through a
deterministic JSONL interface to a dependency-free Rust common-echelon
engine.  On the real 3,905-by-13,818 legacy-27 augmented matrix, modular
rank/membership takes about 0.015 seconds and selects a 1,659-column support;
Python then reconstructs the rational core and performs the accepted
labelled replay.  On chart 26's degree-six direct component Rust agrees over
primes 1009 and 1013 that the 7,149-by-8,889 matrix has rank 5,579 and that
the frozen tail is outside its image.  A one-cell exact dual annihilates all
8,889 columns and pairs `-8` with the target, but this is only a restricted
direct-extension dual.  It does not extend to the complete lower filtered
matrix: two distinct minimum-degree-five columns can have the same singleton
leading row but different degree-six tails.  Choosing one singleton
correction silently discards their kernel difference.  On chart 26 the
minimum-degree-five leading matrix alone has at least 36,755 such internal
kernel directions; on legacy chart 27 the corresponding internal kernel has
dimension 96,310.  Any staged Schur computation that retains only one chosen
correction per leading row is therefore incomplete for a negative result.

The accelerator has executable regressions for repeated orbit
multiplicities and complete reduction past free coordinates.  Its output is
never a terminal by itself; every positive certificate is reconstructed over
`Q`, expanded to actual source-labelled rows, and mutation-tested in Python.

### 4.6 Whole-cutoff closure repairs the staged-kernel defect

The source-faithful replacement is to close the entire truncated Macaulay
component at once.  At cutoff seven, start from every target monomial of
off-anchor degree below seven, include every incident mixed-source column
whose minimum off-anchor degree is below seven, and retain every one of its
outputs below the cutoff.  This automatically includes internal leading
kernels, lower-syzygy tails, and components that first meet the target at the
new layer.

For zero-based chart 26 / legacy chart 29 the target has 1,017 stabilizer-row
orbits (12,169 labelled rows).  Exact Rust closure gives 218,187 row orbits
and 558,104 source-column orbits in six layers, then a cascading singleton
peel leaves a 13,697-by-25,561 core.  An independent Python engine agrees on
the seed, every coefficient in the first layer, and every literal core
column.  A fixed 13,202-column modular basis was solved over 32 compatible
primes and reconstructed over `Q`; the exact core certificate has 11,460
terms.  Reverse substitution through 204,490 audited singleton pivots gives
136,691 orbit-average source terms and zero residual on the full truncated
component.  Thus the genuine source identity

```text
H0 H1 H2 in I_mix + K_anchor^7
```

holds over `Q` on this chart.  The independent referee digest is
`6820f8c2c3b90a0ce65522d304fda11ccc5e30a999e19a71835b95226b4748b0`.
This supersedes the earlier staged `K^6 -> K^7` obstruction; it advances the
finite exponent-one ladder but does not yet close the chart.

The same whole-cutoff computation is now tractable on legacy chart 27:
577,305 row orbits and 1,447,685 columns close in eight layers and peel to a
44,741-by-77,265 core.  Its exact membership decision is pending.  These
sizes show that the direct all-degree method, not chosen-section Schur
transfer, is the current computational route toward the exact cutoff
`K_anchor^13`.

### 4.7 Orbit zero settles exponent-one membership and forces target powers

The maximally symmetric anchor triple takes the same perfect matching
`{01,23,45,67}` in all three colours.  Its stabilizer in `S8 x S3` has order
`(2^4 4!) 3! = 2,304`, so the labelled orbit has size 105.  Since the target
`T=H0 H1 H2` and `I_mix` are chart-independent, one literal identity at
cutoff thirteen would have proved global exponent-one membership; this made
orbit zero the optimal filtration test.

At cutoff seven the complete component has only 2,438 row orbits and 14,369
column orbits.  After 2,075 singleton pivots its core is 363-by-1,519.  A
sparse exact integer identity uses 11 core columns and 90 reverse pivots,
hence 101 orbit-average source columns total.  At cutoff eight the complete
component has 19,210 rows and 68,372 columns and peels to
5,515-by-15,240.  A sparse exact integer identity uses 32 core terms and 236
source columns total.  Independent raw-105, orbit-mass, and mutation replays
therefore prove

```text
T in I_mix + K_orbit0^7,
T in I_mix + K_orbit0^8.
```

The cutoff-nine result is negative and exact.  Complete closure gives
152,386 row orbits and 275,495 columns and peels to an
80,894-by-115,839 core.  A 37-row half-integral functional annihilates every
core column, extends by zero across all 71,492 singleton pivots, and pairs
`2304` with the target.  An independent raw incidence enumeration finds only
55 literal source-column orbits touching the dual and annihilates each.
Standard, `-O`, and `-I -S` replays agree (independent logical digest
`653edb66751251806f7e1b12a742c9ce4ec14ac521c3936f7aa3380be2c6dbf4`).
Consequently

```text
T not in I_mix + K_orbit0^9,
and therefore T not in I_mix.
```

This globally refutes every exponent-one `K^13` chart strategy; another
anchor chart cannot repair it.  The cutoff-eight identity has an exact
leading residual `R8` on 301 invariant degree-eight row orbits, with positive
integer coefficients divisible by 48.  In `R/I_mix`, the leading
off-anchor term of `T^2` is `R8^2` in degree 16.  The next finite test is thus
membership of `R8^2` in the degree-24, `K^16` associated-graded source
matrix.  A positive result starts a `T^2` lift toward cutoff 25; a negative
exact dual determines whether a higher target power or a different localized
unit is required.

There is a crucial completion guard.  Membership in `I_mix + K^d` controls
only the order-`d-1` formal neighbourhood of the twelve-anchor boundary.
Off-anchor variables are unrestricted on the actual chart, so no finite
sequence of such lifts proves chart emptiness unless it terminates in a
literal localized identity, supplies a well-founded global contraction, or
is combined with a theorem identifying the full chart with that formal
neighbourhood.  The exact chart problem is obtained by normalizing the
twelve anchor variables to one while retaining all 240 off-anchor variables;
equivalently, homogenized termination is a `t`-saturation problem.

For exponent-one membership there is a finite unsaturated ladder in
principle: `H0 H1 H2` and every mixed-generator column have total cell-degree
twelve, so a source-faithful lift through `K^13` would have zero residual and
prove literal membership in `I_mix`.  The orbit-zero cutoff-nine functional
has now supplied the first exact complete-component dual.  Because
`I_mix` is contained in `I_mix+K^9`, that dual proves global exponent-one
nonmembership, not merely failure of one chart's continuation.  The finite
ladder is therefore closed negatively and only target powers/localization
remain.

### 4.8 Sparse radical class and the corrected localization target

The cutoff-nine computation also gives a substantially sparser representative
of the first nonzero class.  A centered two-prime reconstruction followed by
all 71,492 reverse pivots gives an exact source combination with 9,607 terms
and residual `R8'` on only 120 quotient rows, all of anchor degree eight.  It
passes standard, `-O`, and `-I -S` literal replay (logical digest
`877ca35865130bd9ca55f19387b44d9473acd2b47d5eddd2d29c1718831cf968`).
Writing

```text
m_c = product_{uv in {01,23,45,67}} x_uv[c,c],
```

the residual has the exact factorization

```text
R8' = m_0 P_0 + m_1 P_1 + m_2 P_2.
```

Each `P_c` is an integral signed degree-eight polynomial on 49,392 labelled
monomials.  It uses no physical-pair edge; at every site it uses one port of
each colour other than `c`; and its site multigraph is 2-regular.  Every cross
term `m_c m_d P_c P_d`, `c != d`, is the unique anchor-degree-sixteen term of
one literal mixed-Hafnian column.  Hence

```text
[T^2]_{gr_K^16} = sum_c [m_c^2 P_c^2].
```

The tempting clean binary subideal does not contain this class.  After
factoring `m_0^2`, one explicit nonzero `P_0^2` coordinate has no incident
alternating-binary source column at all; in fact 610,503 of the 1,578,292
target row orbits have zero incidence in that restricted subideal.  This is
only a restricted-coordinate dual, not a dual to the complete associated-
graded source image: general mixed columns and lower-filtration syzygy tails
can enter the same port-multigraded block.  A source-faithful cutoff-17
computation must include those tails.  The naive full-square closure is very
large, so this negative result is a reason to seek a better localization,
not evidence against radical membership.

Anchor-only localization is also impossible.  For any triple of selected
pure matchings choose a physical edge `e` outside their at most twelve-edge
union.  Set every endpoint-colour cell on `uv` equal to a scalar `z_uv`, with
`z_e=-6` and every other `z_uv=1`.  Every coloured Hafnian is then

```text
90 + 15(-6) = 0,
```

while all twelve selected anchor cells are one.  Thus no chart anchor product
`a_A` lies in `sqrt(I_mix)`.  An exhaustive `105^3` chart audit passes in
three execution modes (digest
`e91660a805c977665eeeb5465c5c31d644dba2955e72dbb1d4352db431b48510`).

The corrected chart-local criterion retains the pure target:

```text
a_A^r T^m in I_mix
```

for some positive exponents on every one of the 31 chart orbits.  This is
enough because an exact source has both `a_A != 0` for at least one selected
pure-matching triple and `T != 0`.  On orbit zero, multiplying the sparse
class by `a=m_0m_1m_2` is especially promising.  Three pair-constant mixed
words kill the displayed representative `a R8'` through anchor degrees eight
and nine.  This is an associated-representative statement only: the
9,607-term identity for `T` was truncated at degree nine, so its omitted
degree-nine tails must be included before claiming `aT in I_mix+K^10`.
The source-faithful `aT` cutoff is now the smaller benchmark against the
diffuse global `T^2` cutoff.

This chart cover is also a symmetry-resolved sufficient decomposition of the
global square.  Expanding the three pure Hafnians gives

```text
T = sum_A a_A,             hence             T^2 = sum_A a_A T,
```

where `A` ranges over all `105^3` pure-matching triples, or 31
`S8 x S3` orbits.  Thus certificates for `a_A T` on all 31 orbit types sum to
a global certificate for `T^2`.  Failure on one orbit does not refute
`T^2` membership—it identifies where cross-chart source coupling would be
needed—but the decomposition avoids constructing the monolithic square
unless such coupling is genuinely necessary.

There is an exact computationally preferable formulation of each local
problem.  The full port torus acts by

```text
x_uv[a,b] -> lambda[u,a] lambda[v,b] x_uv[a,b],
H_w        -> (product_v lambda[v,w_v]) H_w.
```

The twelve selected anchors pair the 24 site-colour ports disjointly, so
their values can all be set to one using an integral Laurent section—no
roots and no target-preserving constraint are required.  Mixed vanishing and
pure nonvanishing are semi-invariant conditions and are therefore preserved.
Conversely, any anchors-one point with mixed amplitudes zero and `T != 0`
can be rescaled to make the three pure amplitudes one.  Thus chart `A` is
empty exactly when

```text
T in sqrt(J_A),
```

where `J_A` is the inhomogeneous mixed ideal after specializing its twelve
anchors to one in the remaining 240 variables.  This does not contradict the
earlier target-preserving gauge warning: that warning imposed three extra
product-one constraints which are unnecessary for the nonzero-target
formulation.  An all-31 literal covariance audit passes in three modes
(digest `9559afee...`).

For orbit zero, 78 specialized mixed generators have constant term one and
all 6,558 generators retain 105 distinct terms of degrees zero through four.
The specialized target has 1,157,625 distinct rows of degrees at most twelve.
A positive bounded Macaulay certificate for `T` is decisive; failure at a
chosen multiplier degree is not radical nonmembership.  This normalized
inhomogeneous solve now supersedes the homogenized `aT` benchmark.

The older first-layer chart-incidence calculation gives a useful, but also
limited, global compression.  An exact acyclic rational repair contracts 24
of the 31 support rows and leaves legacy one-based charts `25--31` critical.
The four all-disjoint charts above are legacy `28--31`; legacy `25--27`
remain among the nominal 27-carrier family.  The transferred higher block is
not supplied by the leading incidence calculation, so this is a seven-chart
triage result rather than a proof that the other 24 charts disappear.

Two `K` filtrations in the older chart literature must not be conflated.
The new 31-chart scan uses `K_anchor`, the ideal of all 240 cells outside the
twelve selected anchors.  The old exact legacy-chart-25 four-row dual uses
`K_carrier`, the ideal outside a 36-cell carrier (the twelve anchors plus 24
extra cells).  Hence `K_carrier` is strictly smaller and its nonmembership
modulo `K_carrier^5` does not contradict membership modulo `K_anchor^5`.
The four dual rows have degrees `(2,2,2,4)` in the carrier filtration but
`(5,6,6,6)` in the anchor filtration.  This predicts a later Schur interface,
not automatically a later dual: after alignment, 52 source columns of old
minimum carrier-degree zero hit the expanded cochain, in addition to the 56
columns it annihilates.  The cochain pairs zero with the new certificate only
after truncation below anchor degree five; its full pairing is `-3/4` and is
absorbed by the omitted tail.  Any anchor-layer obstruction must therefore
include the missing lower-degree Schur lift rather than importing the old
four rows verbatim.

The complementary 27-chart scan is now exact through anchor degree three:
all 54 congruences (cutoffs `K^3` and `K^4`) have integral certificates and
pass standard, `-O`, and `-I -S` replay.  Five exact `K^5` probes also lift:
leading-contractible legacy charts 1 and 24 and critical legacy charts
25,26,27.  This falsifies the tempting claim that first-layer
contractibility predicts the difficulty of the next source layer: critical
legacy 27 peels completely, while leading-contractible legacy 24 has the
largest core (1,152 rows, rank 1,101, determinant `-2^23`, denominator two).
These remain filtered identities, not chart closures.  See
`../unaudited-codex-n8-other27-kadic-2026-08-20/REPORT.md`.

## 5. Balanced contrast contractions

There is a global, chart-free compression which is useful even though its
radical consequence is not yet proved.  In the two-dimensional colour-
contrast plane put

```text
p=e0-e1,  q=e0-e2,  r=q-p,
A=Haf(pXp),  B=Haf(qXq),  C=Haf(rXr).
```

Exact tensor contraction gives

```text
8 T = (A+B-C)(A+C-B)(B+C-A)       modulo I_mix.
```

For every labelled assignment of `p,q,r` with count profile a permutation
of `(3,3,2)`, the corresponding polarized Hafnian is a signed sum of 256
literal mixed amplitudes and therefore lies in `I_mix`.  All three count
placements are essential.  The first fixed 560-member slice has an exact
uniform symmetric common zero with nonzero Heron target, so it is too small.
Two apparent uniform counterexamples to the full 1,680-member family were
rejected by a load-bearing orientation check: the antisymmetric edge
coordinate changes sign when a site permutation reverses an endpoint order.
However, a different orientation-faithful counterexample closes the entire
contrast-only route.  In the ordered `(p,q)` basis set every edge block to
`[[1,0],[0,0]]`, except edge `01`, where it is `[[1,1],[0,0]]`.  A balanced
assignment has at least two sites carrying the compulsory `q` direction,
while the whole graph supplies only one `q` input slot.  Consequently every
one of the 1,680 contractions vanishes termwise.  Nevertheless

```text
A=105,  B=0,  C=90,
(A+B-C)(A+C-B)(B+C-A) = -43875.
```

Thus the Heron target is not in the radical of the full balanced-contrast
ideal; no power or larger Macaulay calculation using only these contractions
can prove the source obstruction.  Literal all-assignment and raw-coordinate
replay, including a two-slot mutation, pass in standard, `-O`, and `-I -S`
modes with digest
`3bde44b9ae049d555b20a95dc1bdc5a568cf2fffaa40a55ada0f8ef0f7f927ba`.

The 1,680 raw contraction tensors have rank 229 inside the 256-dimensional
binary tensor space.  The 27-dimensional annihilator has the exact
`S8`-module decomposition

```text
6 S^(8)  +  3 S^(7,1).
```

Two-prime RREF and the character on every conjugacy class independently
verify this decomposition (digest
`ac774af23de60699798c2ab4ebe6cbfab0d1e7d24d10f1f9316e3f87f58530d8`).
Equivalently, after all balanced contractions vanish, the binary amplitude
tensor consists only of six symmetric Hamming-layer parameters and three
standard site-correction vectors.  The three pure contrast Hafnians remain
linearly free.  The counterexample above lies in this 27-plane and shows that
its intersection with the bilinear-edge Hafnian image is not contained in
the Heron hypersurface.  The module decomposition remains a useful exact
diagnosis of why the linear contractions lose too much information, but it
is no longer a candidate radical proof.

## 6. Diagonal normalized packet and the eight-support correction

On the orbit-zero anchors-one chart, restrict temporarily to the
cross-colour-zero locus and group the eight sites into four anchored pairs.
The compact mixed-word packet currently under study consists of 78
pair-constant permanent/triangle rows, the 48-word transversal orbit, and the
144-word cofactor orbit.  Writing `Q_c(s)` for the Hafnian on one selected
endpoint of each anchored pair, the transversal rows give

```text
Q_c(s) Q_d(complement(s)) = 0.
```

The first exact `F3` census gave 69,696 live one-colour
`(X,cofactor,Q)` signatures.  The cofactor partner condition leaves 168
signatures, all with ten live `Q` coordinates, and hence no two signatures
are compatible.  This is a correct special-fibre theorem, not a
characteristic-zero support bound.

The proposed lift “a live branch has at least nine nonzero `Q` coordinates”
is false.  A smooth `F7` point exposes an exact four-parameter
characteristic-zero family over `Q(sqrt(2),sqrt(65))` in which all six edge
blocks have the form

```text
[[a,b],[-1/b,0]],
```

all 22 one-colour branch equations vanish, `H=4`, and exactly eight `Q`
coordinates are live.  The pure number-field/Laurent replay passes in three
modes with digest
`9aeb739fe3f66c402e5446766d9e70971ec7adbe71e9d901f55d49fee1677c7b`.
Thus no proof may import the `F3` support count.
However, the live support

```text
{1,3,4,5,6,9,10,12}
```

has 96 images under the order-384 Boolean-cube symmetry group, and none of
the `96^2` ordered pairs obeys the complementary-disjointness condition.
The exact three-mode support audit has digest
`3d116eed54c464b605cf639c3c315632ca5cbcc8ddeb1766460b8d2d4a05b82e`;
the induced-cube degree sequences `(0,1,1,1,1,2,3,3)` and
`(1,1,1,1,1,1,2,4)` give a compact invariant separating the forced mate.

The apparent correction “at least eight” is also false.  On the same
weight-zero branch there is an exact `Q(sqrt(2))` boundary point with

```text
M_e = [[0,b_e],[-1/b_e,0]],
H=4,  supp(Q)={3,5,6,9,10,12}.
```

Its transformed `(entry,cofactor,Q)` orbit has 24 records.  Although 288
ordered pairs pass the `Q`-support test, every one violates both directions
of the entry/cofactor packet, so none is a two-colour point.
This orbit calculation has now been upgraded to an arbitrary-mate theorem.
Fixing the support-six point forces a mate's cells
`x9,x10,x13,x14` to zero, its twelve off-diagonal cofactors to zero, and its
six weight-two `Q` coordinates to zero.  Together with the six pair and four
triangle rows, these 28 literal generators have an exact-Q Nullstellensatz
certificate `sum c_i g_i=1`; no pure-Hafnian localization or partner branch
assumption is used.  The independently rebuilt three-mode audit has logical
digest `830839e1` (certificate logical digest `a17794ac`).

The entire localized weight-zero `d=0` chart now has an exact normal form.
After three Laurent gauge parameters are removed, its six block ratios have
Groebner basis

```text
r+s+2,  r+t+2,  r^2+2r-1.
```

The remaining quotient is affine four-space with coordinates
`(Q1,Q2,Q4,Q8)`; `Q0` is one explicit quadratic form and the six coordinates
`Q3,Q5,Q6,Q9,Q10,Q12` are always live.  Consequently this chart has no
support-seven stratum.  Support at most eight consists exactly of the
support-six origin, four one-coordinate axes (where `Q0` is also live), and
six two-coordinate sections of the quadric `Q0=0`.  The two-coordinate
support orbit has no support-level mate.  For the support-six and axis
families, a complete joint transformed census has 2,016 `Q`-compatible
ordered records but zero records satisfying even one entry/cofactor
direction.  The exact normal-form audit passes standard, `-O`, and `-I -S`
with digest
`9a244aec1a6735ebb275af76f0209da3c36f79b423abf8d59b1a48a91d98369c`.

The cofactor exclusion for every nonzero-`y` low-support stratum also has a
compact full-ring certificate.  The four one-coordinate axes have the same
six relevant nonzero cofactors.  On each of the six two-coordinate conics,
exact resultants prove that none of those cofactors can vanish.  The fixed
live coordinates `Q10,Q12` force a mate to have `Q5=Q3=0`, while the ordered
cofactor rows force its six cells `x3,x7,x13,x14,x19,x23` to zero.  On this
face the literal identity is

```text
2 = x15*x16*x21*e01 + x15*x17*x20*e02
    + e12 + e13 + e23 - t123
    - x6*x15*x20*Q3 - x2*x15*x16*Q5.
```

The twelve-term residual in the unrestricted ring is explicitly divided by
the six zero cells, and deleting any displayed source row or zero cell breaks
the identity.  Standard, `-O`, and `-I -S` replays have digest
`b51ebc0cf7735b90c9dcc3f673a641faff236ace12e1b9e664478e32cdcd30bf`.
This closes all axes, all conic sections, and every candidate mate branch at
once.  Together with the separate support-six Nullstellensatz, the entire
localized weight-zero `d=0`, support-at-most-eight chart is excluded against
an arbitrary partner—not merely against another transformed copy.

Three adjacent uniform-`d=0` strata are now classified as well.  On branch
mask zero, the saturated gauge quotient is reduced of length six; all six
points have every `a_e=0`, `H=4`, and the same support-six signature up to
the Boolean-cube action.  Hence the whole stratum is covered by the global
support-six arbitrary-partner certificate.  The three-mode classification
has logical digest
`4122623aa6f6b07b32d5ccbc5116e629ba388f095fa79967dacc1fedf49e4f4e`.

On branch mask one, the exact `H`-live gauge ideal has precisely two
one-dimensional minimal primes, over
`z^2-14z-1` and `z^2+2z-1`.  Writing `T=a5`, both have `H=4`; at `T=0`
their `Q` support is the already closed six-set
`{3,5,6,9,10,12}`, while at `T != 0` their support is exactly
`{0,1,2,3,4,5,6,8,9,10,12}` of size eleven.  Thus a nonzero-`T` point
cannot be the smaller member of a complementary-disjoint pair, and the
zero-`T` point has no arbitrary partner.  More strongly, both nonzero-`T`
components have now been closed against an arbitrary partner as well.  The
left entry/cofactor/Q supports force five partner cells and 39 literal
partner rows; on each quadratic component an exact 14-coefficient
Nullstellensatz replays to one, with no partner-Hafnian localization or
partner branch assumption.  The classification checker has logical digest
`47347c17bf32402a3a2d6caed5632b9d6e49e98e46faa3ca4c93533bebd65f0d`.
The arbitrary-partner certificate and independent audit have logical
digests `09c8cda2a965dd8567f1947c16064c06d0b59a0608aa7d958c8b088f9c2f8d7c`
and `a9c612a1b58b18866cf8bb0ff2d0ded432a18fb61ba2956a14d8d199ba0fb263`.
This is a statement about cofactor mask one with the uniform all-six
off-diagonal permanent chart; it is not a statement about every weight-two
permanent chart.

Finally, the parity-weight-four mask-eleven uniform `d=0` stratum is empty
without even localizing at `H`.  Five surviving rows collect to
`z*b0*b1*b2*b3*b4*b5`; after adjoining the Laurent inverse of the six `b`
variables this is a unit.  Its exact three-mode logical digest is
`874ede0c2e697042df7ff4eb2214e77c355bbd55686383b87539309ebfc2c321`.

A simultaneous Boolean-cube quotient of the cofactor orientation and the
chosen nonzero permanent term gives exactly 50 aligned one-zero-per-block
chart orbits.  Every specialized row was rebuilt from the 24-cell source.
Exact-Q, mod-1009, and mod-1013 calculations agree: 43 charts are units,
with full Singular lifts and deletion controls, and only seven survive:

```text
(0,12), (0,30), (0,63), (1,12), (1,38), (1,63), (11,21).
```

The first coordinate is the cofactor mask and the second the selected-term
mask.  The three-mode census has logical digest
`27a36e24f009503149e6162060588f883ee8df7d7f3dcbf7c00ce5556a9ec3f9`.
Among the survivors, `(0,63)` and `(1,63)` are the now closed uniform
branches above; `(0,12)` is the transformed branch-51 affine-four-space
chart, whose support-at-most-eight locus is closed but whose higher-support
locus is not.  Three of the four initially new survivors have since
collapsed.  Both `(1,12)` and `(1,38)` have exact three-dimensional normal
forms with `H=4`, six live `Q` coordinates, and complete `(X,C,Q)` orbits
identical to the already closed support-six orbit; their logical digests are
`d849b4815a3adc18f50bc6c7b76254b811afdc9da671052d844f5a13afa3ba93`
and `73d51b6e9c476fd0ff4acb6f5e5ba5b9e7fc840dc54d04e49294f9d39f7421eb`.
On `(0,30)`, a 26-term exact identity writes the pure Hafnian itself as a
combination of nine specialized packet rows, so its pure-live locus is
empty; the three-mode digest is
`70041a8c5d4b07e4b7686b1db6558cc7db652be081b5547a0cc5a9da08e07389`.
The last survivor `(11,21)` has two exact affine-line components over
`r^2-2r-1`.  At the line origin its signature is the closed support-six
orbit; away from the origin its support has size eleven.  For both generic
lines, the left signature forces an arbitrary mate into an exact unit ideal:
the frozen certificates use 22 and 14 nonzero coefficients respectively,
without localizing at the mate Hafnian.  The classification digest is
`bcb36aae97554efd441021f506bc5c2f122300e092e2f446084d511444dc36e6`;
the certificate and independent-audit digests are
`666b8ba0d38d27ddaba1695cb5933d49f8d4a780fc7938e6003f02f91efd8912`
and `156f4eed984458a715455d01fb7c86d6cc83d730c91a3e9254f7d7c55631e6e8`.

Therefore no two live colours can satisfy the complete diagonal packet if
each selected permanent block lies on an aligned one-zero-per-block chart:
choose the colour with at most eight live `Q` coordinates, then use the
classification above; the generic size-eleven components are separately
closed against arbitrary mates.  This is the first complete finite
pairwise theorem for all 50 aligned chart orbits.  It remains a boundary
theorem, not a classification of the surrounding full 24-variable open
charts.

The first controlled lift away from that boundary is also exact.  In the
branch-zero all-off-diagonal chart, release one lower-right entry `d` while
leaving the other five zero.  Two literal cofactor rows satisfy
`C1+C2=2*d*b3*b5`; the selected `b` entries are Laurent units, so `d=0`.
The source-derived lift and all six edge transports replay in three modes
with audit digest
`33f89235d71653579f2f7c9fb882367b5522514642f42fb317aeda5d1b7ad3c0`.
This closes every one-defect extension by symmetry, but not charts with
several defects simultaneously.

The same full-ring parametrization has now been stratified by the support of
genuinely live opposite permanent terms.  With edge order
`(01,02,03,12,13,23)`, exact-Q unit computations exclude the support-orbit
representatives

```text
{0}, {0,1}, {0,5}, {0,1,2}, {0,3,5}, {0,1,3}.
```

These are respectively the one-edge, adjacent/disjoint two-edge, and
star/path/triangle three-edge graphs.  The first four have frozen source
lifts with 4, 4, 14, and 6 nonzero multipliers; the path and triangle have
exact unit bases but their direct source lifts remain too large for the
bounded replay.  The
three-mode guarded checker has digest
`71896910025164afcb24015d655cb252bd9e911cdaa744555a16b6f438553bea`.
Independently, a torus-normalized 13-row calculation proves the triangle
stratum is empty without even localizing at the pure Hafnian; its three-mode
digest is
`a981105235c9bb70ed29a7f85b03780feedacd993a43b38248734bde6f777368`.
Thus every support orbit of size at most three is excluded.  All supports of
size at least four remain open; their bounded Gröbner runs timed out and no
conclusion is drawn from that.

There is a necessary boundary guard at size four.  In the off-diagonal
parametrization `b_e*c_e=-(1+a_e*d_e)`, localizing
`C=product_{e in S}(1+a_e*d_e)` isolates the genuine all-entry interior, but
`C=0` does **not** automatically land in the fully aligned 50-chart census:
only the affected blocks become aligned, while the other defects remain
full.  For the four-cycle `S={1,2,3,4}`, an exact Boolean-cube covariance
audit splits this boundary into 15 strata.  Their canonical
`(cofactor mask, selected-term mask, remaining-full-support mask)` types are
`(0,31,13)`, `(0,15,3)`, `(0,30,12)`, `(0,13,1)`, and the fully aligned
endpoint `(0,12,0)`.  Only the last is covered by the aligned theorem; every
proper boundary type needs a separate lower-defect classification.  The
three-mode audit digest is
`07871886949591b5a78924f54d39ea070ce976310108ed85884b97a320a56977`.
This prevents a localized-interior unit from being overstated as closure of
the entire four-cycle chart.

Three of the four proper canonical boundary types have now been settled
exactly.  Types `(0,13,1)` and `(0,15,3)` have homogeneous localized units
`t^6` and `t^8`; the first has a 14-term literal multiplier ledger, while
the second currently has exact homogeneous membership but no compact full
multiplier lift.  Their joint three-mode digest is
`1adc0b76fcce32afb9f0f400c2247a8753e278b60cd11360f96e18a188001141`.
Type `(0,30,12)` is not empty: its full literal ideal is exactly a rational
one-parameter family.  Every point of that family has all sixteen `Q`
coordinates nonzero, so a compatible partner has every `Q` coordinate zero;
the exact polarized-Hafnian identity then forces the partner's pure Hafnian
to vanish.  The classification and signature digests are respectively
`b21d9ee4cc4b1a68bd6acc99809186ea4cb4099e69dc253da7d6caca192299c5`
and
`d4263fffea8545c4921f04c2b3a8ff2bce8907d081f567c1c40061c23f00b4e3`.
Thus only `(0,31,13)` remains among the proper four-cycle boundary types.

The full recursive bookkeeping is now frozen as well.  A state records the
cofactor branch, the selected permanent-term mask, and the remaining
both-live mask; a boundary move toggles the selected term on one edge and
deletes that edge from the both-live mask.  The 729 labelled ternary edge
states collapse to 66 Boolean-cube orbits, with degree histogram
`11,14,18,14,6,2,1`.  The four hard starts reach 43 of these orbits, only
four of which are fully aligned.  The exact interface digest is
`a3a6fbc330aa06791417a3c06e1779de7c15b070ca734b657f4ed0c9b1311ac7`.

One lower stratum has also strengthened: the three-defect triangle is a unit
using ten literal source rows and only the product of the selected `b`
entries.  It needs neither the pure-Hafnian, selected-`a*d`, nor selected-`c`
localizers.  Its three-mode digest is
`507614bf88c7a84fb693403a4357246b012966e0429b4675e5f14b0ea8b1ce54`.

For the genuine four-cycle interior, the four upper cofactor rows form an
exact linear Cramer block.  After the lossless torus gauge its determinant is

```text
4*b0^2*b1*b3*d1*d3*d4*(b1*d3+b3*d1*d4)^2.
```

The source-faithful determinant audit has logical digest
`104b824e72f6e8617e48bf34976e095b21105b0447447f079c1231d2cedf608d`.
This reduces the generic branch to five compatibility
numerators in six Laurent parameters, but neither that reduced system nor
the complementary determinant-zero branch yet has an exact unit or a
characteristic-zero component.  Direct exact and modular-lift computations
remain fill-bound; no conclusion is drawn from them.

One proper subbranch of that generic Cramer locus is now closed exactly.
Assume in addition that `D0!=0`, `b1+d1=0`, and
`Kplus=b3*(d1-1)+d1+1=0`.  Literal source rows first force
`d1*d3-d1*d4-d3-d4=0` and solve `a0,a5`.  The remaining two triangle rows
have resultant

```text
16*d1^5*(d1-1)*(d1+1)^5*(d1^2+1)^2
 * (d1^2-2*d1-1)^2*(d1^2+2*d1-1)^2
 * (d1^4+2*d1^3+2*d1^2-2*d1+1)^2.
```

Already-localized factors are discarded; the `d1^2+2*d1-1` factor forces
`1+p1=0`, while exact norms `-128` and `119563878400` exclude the remaining
quadratic and quartic factors via a lower cofactor row.  The three-mode
source-faithful audit digest is
`7a035c72cc0aaa68501f33a9435ca3aee68b390278056c61570ca1abdda55ae6`.
This proves only the stated `Kplus=0` denominator branch; `Kplus!=0`,
`D0=0`, and the upper determinant branch `Delta=0` remain open.

The first exceptional subbranch of `Kplus!=0` is also closed.  After
`t123=0` solves its complementary factor, let `L` be the coefficient used
to solve `b3` from `Cof(0,0)`.  On `L=0`, that cofactor forces a second
polynomial `M=0`.  Their exact resultant splits into localized factors,
`d1^2+2*d1-1` (which forces all selected `p_i=-1`), and one residual
factor.  The latter is eliminated by the remaining triangle/cofactor rows:
one algebraic norm is
`38973380220162416179749905447126040576`, a leading-coefficient branch has
norm `-256`, and its final quartic forces `Delta=0`.  The guarded audit
digest is
`d37553fae0ea8caaff14216c571e1e0232e57f98b243d9d9b626d50ffe5c67b0`.
Within `B0=0`, the remaining honest generic piece is therefore
`Kplus!=0,L!=0`; the global `D0=0` and `Delta=0` branches still remain.

That `L!=0` piece has now been reduced exactly to four sparse polynomials
`F160,G84,C9,C35` in `b0,d1,d4`.  On the `C9=0` branch, the three
low-degree common univariate factors are closed with all live constraints:
`d1^2+2*d1-1` forces the selected factor `p3=0`, while the cubic
`d1^3+d1^2+3*d1-1` and quartic `d1^4+6*d1^2+1` each force `L=0`.
The corresponding bare factor ideals remain positive-dimensional, so these
are genuinely localized conclusions rather than accidental unit ideals.
The source-rederived, mutation-guarded three-mode digest is
`1581bf1cf6e5a8396bac677a5c86b92b5731d6499f7205306bfcd108bb1841dd`.
The higher `C9` and `C35` factors require algebraic-number extraction rather
than the fill-bound direct `facstd` computation; those exact closures are
recorded below.

The common-factor half of `C35` is now closed exactly.  On
`F160=G84=C35=S13=0` with `L!=0`, characteristic-zero `facstd` has one
one-dimensional component (basis size 26), and the literal specialized pure
Hafnian has zero normal form on it.  The `H+1` mutation has nonzero normal
form, so this is a genuine `H=0` component and cannot meet the pure-live
chart.  The source-rederived three-mode audit digest is
`6c4491ff3eb4340275df8b33dc5c2df92ae38a1f2f96687d361bc893efcfb99e`.
The distinct `C35` resultant intersection and the degree-34 `C9` factor are
treated next.

The distinct `C35` intersection eliminates further to nonlocalized factors
of degrees `2,2,4,24,153`.  Exact factorizing-basis checks close the first
three: `d1^2+2*d1-1` is `H=0` on the `L`-open branch, `d1^2+1` lies on
the already-separated `D0=0` branch, and
`d1^4+2*d1^3+6*d1^2-2*d1+1` lies on `L=0`.  The `H`-only control on the
second quadratic survives, showing that `D0` is load-bearing.  The stable
three-mode digest is
`6bb0457fafd2fb9bc811e9c64b539a75dc1793ffcdfa4c1524506c6085e3a759`.
The two high `C35` factors are now closed by exact algebraic-number gcds.
Over the degree-24 field, the two bivariate eliminants determine unique
`d4` and the original `F160,G84,C35` core determines unique `b0`; every
localized factor is nonzero, but all five omitted literal lower cofactors
are nonzero, so this point is rejected by the source system.  Over the
degree-153 field, the eliminants again determine unique `d4`, but the three
original core polynomials have gcd one in `b0`, so the eliminant point does
not lift at all.  The audit passes standard, `-O`, and `-I -S` with logical
digest
`f0f06077f4f38fc9fc65550506f969b6eb80844f032b349f6581e9393e36b21a`.

The degree-34 `C9` factor has the same exact outcome as the lifted degree-24
case: it determines unique `d4` and `b0`, solves all five elimination-core
polynomials, and remains on all nineteen declared live factors, but each of
the five unused literal lower cofactors is nonzero.  Exact nonzero norms are
stored for every lower row.  Its three-mode logical digest is
`8f86348955558f75d1617c128b320d1f05ccd74dcde06e42f8bcbd9427f3436e`.
Together with the low-factor, shared-`C35`, `Kplus=0`, and `L=0` audits,
this closes the entire `B0=0,Delta!=0,D0!=0` cycle subtree.

One Cramer-denominator exception outside that tree is also exact: on
`C0=b0^2+d4^2=0`, consistency of the `Cof(0,0),Cof(5,0)` system forces
`(d1^2+1)(d4-1)=0`; the two branches are then excluded by the remaining
triangle/cofactor rows, with the final conjugate norm `42467328` in both
signed cases.  The source-faithful audit is
`audit_branch0_cycle_d0_cramer_exception.py` with logical digest beginning
`a8b5f348`.  Its complement `C0!=0` is still open.

On the exceptional upper-determinant branch `Delta=0`, the entire
`Bplus=b1+d1=0` locus is also closed exactly.  The source-faithful rank-two
interface first excludes `x=1`; for `x!=1`, the generic solve branch and
both solve-coefficient divisors are empty by exact resultants and nonzero
norms.  The final three-mode audit is
`audit_branch0_cycle_delta_bplus_generic.py`, logical digest beginning
`37cbc170`.  The sole remaining `Delta=0` locus is therefore
`Bplus!=0`, represented by the exported six-by-four augmented rank
condition.

Inside that last `Bplus!=0` locus, the divisor `Au=0` is now empty as well.
The generic terminal resultant has only localized/unit factors; its two
triangle solve-coefficient exceptions are killed respectively by the live
factor `b1^2*(d1+1)` and by `1+p1`.  The literal-source checker passes in
all three interpreter modes with logical digest
`082927b0fa7e9d162872a30aab6f5587ed20f9d99c7b8bed87738d6c6c59c942`.
Thus the only surviving `Delta=0` interior branch is
`Bplus!=0,Au!=0`.

Thus a universal one-colour support lower bound is no longer the target.
The sharpened diagonal problem is pairwise: classify the low-support
components in the other cofactor charts and prove that none is a compatible
mate for the three normal-form classes above (or exhibit a genuine pair).
Only after that pairwise classification can the packet be lifted off the
diagonal locus; cross-colour tails remain uncontrolled.

## 7. Recommended proof order

1. Correct the twisted certificate's generator-sign metadata and promote the
   independently audited twisted-orbit and W40 fixed-support results at their
   exact stated scopes.
2. Do not continue the global exponent-one filtration: the exact orbit-zero
   cutoff-nine dual proves `T notin I_mix`.  Compare two valid radical routes:
   the global associated-graded class `(R8')^2`, and normalized chart-local
   radical membership `T in sqrt(J_A)`.  Start with the maximally symmetric
   anchors-one orbit-zero chart; its 78 constant mixed generators make it far
   smaller than the full square.  Keep complete source columns and exact-Q/
   raw-source replay as the acceptance gates; a modular result is discovery
   only, and bounded-degree nonmembership is not a radical obstruction.
3. On the other 27 charts, separate the 24 first-layer contractible types
   from the three legacy-critical types `25--27`, and use carrier geometry
   only to select source
   packets.  The statement that a split canonical star itself supplies a
   five-row packet is false: two forced pure response edges do not give the
   required singleton spikes or cofactor vanishings.  The next valid target
   is a source-global coefficient coupling, a localized ideal contraction,
   or a strictly decreasing source-valid chart rewrite.  Any cap conclusion
   must be checked against the literal forbidden-response and error maps.
4. On every surviving stratum, use the indispensable `(3,3,2)` equations to
   derive a source unit, a support deletion, or an active cap.  The 13+45
   response packet is a possible local derivation tool, not an assumed cover.
5. Once `N=8` is closed, isolate the small source identity responsible for
   the cap and test its stability under adding a two-site tail.  Only then
   attempt the uniform `h` induction.  A proof of `N=8` alone does not imply
   the all-order conjecture.

This reverses the risk profile of the current conditional architecture:
first prove a finite source-level theorem at the smallest open order, then
uniformize the mechanism that actually worked.
