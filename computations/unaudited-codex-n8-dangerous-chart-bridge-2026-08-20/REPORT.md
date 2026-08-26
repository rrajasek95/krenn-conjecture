# Dangerous charts 25--28 / legacy 28--31: exact bridge report

Status: unaudited computations, 2026-08-20.  No spine/certified file was
edited.  All anchors remain twelve named nonzero cells; none of the exact
identities assigns them the value one.

## Indexing and source mechanism

The requested zero-based quotient charts 25, 26, 27, 28 are legacy
one-based charts 28, 29, 30, 31.  They are not the legacy chart-25/26 cases
in the older notes.

Each dangerous chart has 6/4/6/4 singleton selected-skeleton X4 words.
Every such word has exactly 12 cancellation mates in K-degree two, 32 in
degree three, and 60 in degree four.  The localized five-row Cramer packet
from the M25 residual does not transplant: it requires five neighbouring
blocks to vanish, while these anchor charts invert twelve cells without
imposing those support zeroes.

## Exact ladder statements

`audit_dangerous_charts.py` proves over Z, hence over Q,

- all four charts: `H0 H1 H2 in I_mix + K^3`;
- all four charts: `H0 H1 H2 in I_mix + K^4`.

The signed degree-three certificate sizes are 282/211/205/207.  Chart 28
requires the recorded two-column degree-two kernel correction.  Standard,
optimized, and isolated Python runs have result SHA
`49226ce09479fb174221cb02d64b53d77e3574ea462dee5fa06f05f196dd02f5`.

`audit_degree4.py` proves all four charts satisfy

`H0 H1 H2 in I_mix + K^5`.

The degree-four row/column/hard-quotient/certificate counts are:

- chart 25: 17,610 / 75,900 / 126 / 1,958;
- chart 26: 16,332 / 64,628 / 0 / 1,721;
- chart 27: 17,578 / 75,720 / 190 / 3,793;
- chart 28: 16,300 / 64,190 / 2 / 1,971.

Three-mode result SHA:
`f67388de6f1af3321937ac01077e781bca6b72ccae1f7d1fae8160f726d0beeb`.

For chart 26 / legacy 29, `audit_degree5_chart26.py` gives an exact
16-action orbit-average certificate with 2,041 terms and literal rational
actual-row replay:

`H0 H1 H2 in I_mix + K^6`.

Result SHA:
`2c7e35f08ed2932cd99e4df4deb603625f55439281a69ac15759f7ad9b412f5c`.

The main new result is the source-faithful mixed cutoff-seven computation.
The complete target-incident truncated component has 218,187 row orbits and
558,104 source-column orbits.  Saturated singleton peeling leaves a
13,697-by-25,561 core.  Rust found a fixed-minor modular solution and
reconstructed it over Q; independent Python then:

1. matched the 1,017-orbit target and literal first closure layer
   `+13240/+3264`;
2. reconstructed all 25,561 core columns from their source words and
   multiplier cells exactly;
3. checked the 11,460-term rational core certificate;
4. audited all 204,490 singleton pivots and reverse-backsolved 125,231
   nonzero pivot coefficients;
5. obtained zero residual on the full cutoff component with 136,691
   orbit-average source terms; and
6. fired a hostile core-coefficient sign mutation.

Therefore chart 26 / legacy 29 now satisfies the genuine next ladder step

`H0 H1 H2 in I_mix + K^7 over Q`.

The exact referee passes standard, optimized, and isolated modes with result
SHA
`01d802903ad2f51f1a4fc705d4447883311f7ebcca19009b3ed2874ebb96d752`.
Pinned inputs are core certificate SHA `d1ed378a85e9f4011dcd347092bc41a5936c604f9a1ecdb3786cbfb8b83abefc`,
core interface SHA `487662cd76c11452bd8bf7feb343f290bffc3a623b18988c974d395ebdf55328`,
and pivot ledger SHA `1619e4d7335f13c07beaf8105b50e02af85b0cbf9f46871d9380c5aaff97a656`.
The largest numerator/denominator sizes are 107/90 bits.

This controls the full source-faithful truncated chart through K-degree six,
not merely a preselected source family.  It is not yet full localized-chart
control: cutoffs 8 through 13 remain, and total degree twelve makes cutoff
13 the exponent-one endpoint.

## Audited false obstruction and why the whole cutoff was necessary

The residual-led minimum-degree-six closure by itself has 140,578 rows and
361,406 columns, peeling to 7,149 by 8,889.  It is outside the image at
primes 1009 and 1013.  Adding 3,274 lower-kernel transfers obtained after a
chosen min5 correction still leaves a two-coordinate modular dual.

That dual is not a theorem about the full d5 source component.  The exact
counterexample `audit_degree6_chart26_missing_min5_kernel.py` finds two
different min5 singleton columns with the same sole d5 boundary row but d6
dual-tail values zero and one.  Their difference is an intrinsic min5 kernel
direction omitted by `singleton.setdefault`.  Frozen witness result SHA:
`f90d5e7698aaa9e11e012a45d67ee4adb1659e90b6771da78d52d71a5174eaef`.

Thus modular failures for a frozen correction choice are nonterminal.  The
mixed cutoff closure is the correct source-faithful construction because it
includes all intrinsic min5 kernels, all lower kernels, and every remote
lower component whose higher tail enters the target component.

## Strategic fixed-chart reduction and orbit 0

The target `T=H0 H1 H2` and the homogeneous ideal `I_mix` are independent of
the anchor chart.  Only the filtration ideal `K_anchor` changes with the
chosen twelve anchors.  Since every relevant monomial has total degree
twelve, `(K_anchor^13)_12=0`.  Consequently a cutoff-thirteen identity for
**any one** fixed chart proves the global identity `T in I_mix`; closing all
31 anchor orbits is unnecessary.

This makes zero-based orbit 0 the natural primary chart.  Its representative
has all three matchings equal to `01,23,45,67`.  Its twelve coloured anchor
cells have stabilizer

`(2^4 4!) * 3! = 384 * 6 = 2304`

in `S8 x S3`, and orbit size 105.  The independent finite audit
`audit_orbit0_global_strategy.py` verifies the representative, the 12
distinct coloured cells, the full stabilizer, orbit--stabilizer, and the
single-chart global implication.  Its standard/optimized/isolated digest is
`924b8a6bd5410d1d3c6423575e89fa7ce0e1c2dc805889911c5c51849d1ad824`.

At cutoff seven the 12,169 actual target rows collapse to only 36 target-row
orbits.  Full source-faithful closure has 2,438 row orbits and 14,369 source
column orbits; 2,075 singleton pivots leave a 363-by-1,519 core of rank 307.
The target is in the image over two primes, and the first common solution is
an exact 94-term integer core certificate with coefficients at most 96.

Independent Python checks match the raw target, all 2,304 actions, the first
closure layer `+207/+125`, and every literal core column.  Reverse replay of
that exact core certificate through the frozen pivot ledger uses only 265
nonzero pivots, hence 359 orbit-average terms total.

A target-overlap pivot order then exposes a much smaller exact core identity:
11 integer terms with coefficients

`24,24,48,4,96,96,-3,-96,-12,-12,-24`.

Its reverse solve uses only 90 pivots, so the final source-faithful identity
has 101 orbit-average terms.  Every coefficient is an integer, the raw
105-output quotient residual is zero, and a sign mutation fires.  Therefore
orbit 0 satisfies

`H0 H1 H2 in I_mix + K_anchor^7 over Q`.

The sparse exact referee passes standard, optimized, and isolated modes with result
SHA
`d203097fe973156930dd7b564de6b68aa87b95cb20ba195c1863f1d728b4eaa5`.
Pinned inputs are sparse exact core certificate SHA
`2d040af70823fe7a9931dc076467546293cfba6f0f072ae10e935f4c69b3c61f`,
core interface SHA
`bcd16826c7a30f7d1f0c1eb82229fde1ed5fdcf6f5b1f2a33244370b0d322f6d`,
and pivot ledger SHA
`40daf028bf76471de90fe84798d9446a5dde78667a3ec05335d11dcbfacdae69`.

Cutoff eight remains small enough for the same exact treatment.  Full closure
has 19,210 row orbits and 68,372 source-column orbits; 13,695 singleton pivots
leave a 5,515-by-15,240 core.  Initial exact reconstruction gives 96 core
terms and 370 nonzero full source terms.  Target-overlap pivot ordering reduces
this to an exact 32-term integer core and 236 nonzero full terms.  The
independent referee bypasses the producer's matrix arithmetic entirely at the
final stage: it rebuilds each of those 236
literal `H_w` columns from all 105 perfect matchings, truncates below degree
eight, canonicalizes under the 2,304 actions, and obtains the exact 58-orbit
target (37,513 labelled monomials).  All coefficients are integers, the largest
uses twelve bits, and a coefficient mutation fires.  Therefore

`H0 H1 H2 in I_mix + K_anchor^8 over Q`.

The cutoff-eight referee passes standard, optimized, and isolated modes with
SHA
`193e643067e49e5e68dc8a4c56288a70a23bcd72d76e8afc05671080b1d2520d`.
The 236 terms use only three word orbits: `00000011` (179 terms),
`00001111` (55 terms), and `00001122` (2 terms).

Cutoff nine changes the strategic conclusion.  Full closure has 152,386 row
orbits and 275,495 source columns; 71,492 singleton pivots leave an
80,894-by-115,839 core.  Two primes give the same rank 50,420 and the same
37-coordinate dual support.  The coefficients reconstruct uniquely to small
half-integers.  The exact cochain has degree histogram `{6:2,7:3,8:32}` and
pairs with the target by 2,304.

The independent referee checks exact annihilation of all 115,839 core columns,
extends the cochain by zero across the singleton rows, and checks all 187,331
retained source columns.  More importantly, it avoids relying only on the
ledger: starting from the 37 cochain rows, it independently enumerates all
literal incident source-column orbits.  There are only 55; rebuilding their
105 perfect-matching outputs gives pairing zero for every one.  A dual
coefficient mutation fires.  Hence

`H0 H1 H2 not in I_mix + K_anchor^9 over Q`.

The referee passes standard, optimized, and isolated modes with SHA
`653edb66751251806f7e1b12a742c9ce4ec14ac521c3936f7aa3380be2c6dbf4`.
This is not merely a chart-local warning: since `I_mix` is contained in
`I_mix+K_anchor^9`, it proves `H0 H1 H2 not in I_mix`.  Therefore no other
anchor chart can complete the exponent-one cutoff-thirteen program.  The
remaining proof must use a target power/radical certificate or a genuinely
localized unit identity.

For comparison, the chart-26 core has modular rank 13,202 and modular affine
nullity 12,359.  It is a single connected block.  There are 2,398 exact
duplicate-column pairs, but the existing certificate already uses at most one
column from each pair.  Cheap deterministic pivot reordering reduces modular
core support from 11,448 to 5,939, showing real but only representational
compression.  Even that is dominated by orbit 0's exact 11-core/101-total
identity, so further chart-26 sparsification is not the main route.

## Current frontier

- charts 25, 27, 28 / legacy 28, 30, 31: exact through `K^5`;
- chart 26 / legacy 29: exact through `K^7`;
- orbit 0: exact through `K^8`, followed by an exact obstruction at `K^9`;
- global exponent-one statement: exactly false, `H0 H1 H2 not in I_mix`;
- full chart proof claim: not yet established.

The optimal next experiment is no longer a cutoff ladder or a sweep of other
anchor charts.  It is to reuse the maximally symmetric orbit-0 quotient for a
low target power, or to seek a normalized/localized unit identity.  Any such
calculation must include product-rule source columns for the chosen target
power and must still end in an exact-Q certificate or dual; simply tensoring
the exponent-one matrix is not source complete.

The sparse cutoff-eight identity also gives a concrete first target-power
input.  Its exact leading residual `R8` has 301 invariant row orbits, all in
anchor degree eight; every coefficient is a positive integer divisible by 48,
and the cutoff-nine dual pairs with it by 2,304.  Thus, modulo `I_mix`, `T` is
represented by `R8` plus higher anchor-degree terms, so `T^2` begins in anchor
degree sixteen with leading class `R8^2`.  The smallest sound next computation
is therefore membership of `R8^2` in the total-degree-24, anchor-degree-16
associated-graded source.  A positive answer starts a lift of `T^2` toward the
degree-24 endpoint `K^25`; a negative exact dual would sharply delimit this
radical route before constructing the much larger full target-square closure.
The residual extractor's logical SHA is
`25d4acd094eb27e78e3941b738611522f112f57f4ef6f78f3657d50e18762d03`.

## 2026-08-20 radical-route correction and normalized frontier

The binary contrast contraction is an exact and useful change of variables:
with `p=(1,-1,0)`, `q=(1,0,-1)`, and `r=q-p`, write
`A=Haf(pXp)`, `B=Haf(qXq)`, and `C=Haf(rXr)`.  Literal tensor expansion gives

`8 H0 H1 H2 = (A+B-C)(A+C-B)(B+C-A) mod I_mix`.

However, the ideal generated by all balanced contrast contractions does not
control any power of this Heron target.  A rational counterexample has every
oriented contrast block equal to `[[1,0],[0,0]]`, except block `01`, which is
`[[1,1],[0,0]]`.  Every one of the 1,680 `(3,3,2)` contractions vanishes
termwise, while `(A,B,C)=(105,0,90)` and Heron is `-43875`.  The raw-colour
realization has `x_uv^{11}=1` on every edge and the single extra cell
`x_01^{12}=1`.  Direct, raw signed-256, optimized, and isolated replays are in
`audit_contrast_j332_single_exception_counterexample.py`; logical SHA
`467de03dabdc19b4bf543b381b2eda9b93234944d9d0a9ec00f592e1af53041a`.
Thus the contrast-only target-power route is terminally negative.

The associated linear tensor computation is nevertheless exact.  The full
1,680 balanced tensors span rank 229 in the 256-dimensional binary tensor
space.  Their 27-dimensional annihilator is

`6 [8] direct_sum 3 [7,1]`.

All higher two-row `S8` types are exhausted.  The three pure evaluations
`A,B,C` see only the six trivial coordinates and have rank three there, so
linear representation theory cannot force Heron.  Compact invariant and
standard bases are frozen in `audit_contrast_p332_tensor_annihilator.py`;
logical SHA
`db884c364c2fa60faf1d1b6a4902a0e094e475644750ccf2380c9f0ee26b8790`.

The exact diagonal superpair polarization clarifies the best normalized
structural lane.  Let `e_ij=per(M_ij)+1`, let `t_ijk=tau_ijk-2`, and let
`Q(s)` be the four-site Hafnian on one selected clone from each of the four
anchor pairs.  A literal matching census proves

`2H = sum_s Q(s)Q(sbar) - 2(e01 e23+e02 e13+e03 e12)
      + 4 sum e_ij + 2 sum t_ijk`.

Thus the 78 pair-constant rows reduce the pure Hafnian to the eight
complement-transversal self-products, while the smallest 48-word breaker
orbit supplies cross-colour products `Q_c(s)Q_d(sbar)=0`.  The exact packet
is in `audit_pairconstant_transversal_polarization_identity.py`; logical SHA
`25cc4d08011bcdf75a2e8baab31447a8a70ec89b5d951db821c983bd31da4051`.

A support-count finish from those rows alone is impossible in characteristic
zero.  The checker
`audit_pairconstant_breaker_active_pair_hensel_obstruction.py` gives a smooth
`F3` point with `per=-1`, `tau=2`, nonzero `H`, and only two active
complement pairs.  Six chosen `Q` factors vanish and the resulting 16-by-24
Jacobian has rank 16 with determinant-2 pivot minor.  Multivariate Hensel
lifting produces a characteristic-zero component with the same exact zeros
and live target.  Logical SHA
`01ee3c466bc0f70abd9dc6a6c167570d4d76c9377b9884df6ede569df918689e`.
An independent stronger search subsequently found smooth one-active branches.
Concretely, the six flattened blocks

`(2,1,1,2),(1,1,2,0),(1,0,2,2),(2,2,0,1),(0,2,1,1),(2,2,2,2)`

over `F3` have `per=-1`, `tau=2`, `H=1`, and `Q` support exactly
`{6,9}`, a single complementary active pair.  For every choice of one zero
factor from each of the other seven pairs, the corresponding 17-by-24
Jacobian has full row rank 17; the 14 `Q`-zero rows have rank 20.  Hence the
one-active obstruction is also smooth and lifts to characteristic zero.

Consequently the optimal next structural addition is the size-144 `6+2`
word orbit represented by `00000101`.  On the diagonal locus its equations
are the cofactor-gradient packet

`x^d_e * (partial H_c / partial x^c_e) = 0,  c != d`.

The four normalized anchor cells force the four anchor cofactors to vanish,
and Euler's identity forces every live pure colour to expose a nonanchor
cofactor edge.  Exact orbit enumeration shows this `6+2` family detects all
one-active attempts left by the 78+48 packet: the full 192-element `B4` graph
orbit of the displayed smooth point has no binary-compatible ordered pair,
and every one of its 36,864 ordered pairs is detected by a `6+2` word (with
minimum minority side two).  The exact finite diagonal search universe after
the six permanent and four triangle equations has 1,681,552 labelled
one-colour graphs; a signature census in `(X24,Cof24,Q16,H)` is the natural
next exhaustive referee, rather than repeating the graph enumeration.

The smallest current proof gap
is therefore a finite localized/unit identity for the 78 pair-constant,
48 transversal-breaker, and 144 cofactor rows on the general diagonal
superpair locus, followed by polarization of the cross-colour tails.  The
421,216-column pruned normalized Macaulay layer remains a sound fallback and
referee, but is not the most efficient discovery route.

## Exact low-support diagonal branch classification

The characteristic-zero support lower bounds suggested by the finite-field
census are false even after the cofactor packet.  On the weight-zero branch
with

`M_e=[[a_e,b_e],[-1/b_e,0]]`

there is an exact support-six point over `Q(z)`, `z^2+2z-1=0`:

`a_e=0`, `b=(z,-z-2,1,-z-2,1,1)`.

Its literal pure Hafnian is 4, its nonzero `Q` coordinates are
`{3,5,6,9,10,12}`, its cell support consists of the twelve off-diagonal
block entries, and its cofactor support is `{9,10,13,14}`.  The independent
literal referee `audit_support6_component_pairwise_obstruction.py` checks all
permanent, triangle, selected-cofactor and Q values and the full `B4` orbit.
Its logical SHA is
`03b54935c9de9e0e126b336dfde745e1b9f19e62b9837f99d7c409d52109c5b2`.

More strongly, this point has **no arbitrary partner**, not merely no partner
in its own orbit.  Fixing it on the left forces partner cells
`x9=x10=x13=x14=0`, all twelve partner off-diagonal cofactors to vanish, and
partner `Q3,Q5,Q6,Q9,Q10,Q12` to vanish.  In that twenty-variable quotient,
the six permanent rows, four triangle rows, twelve cofactors and six Q rows
generate 1 over Q without even localizing at the partner pure Hafnian.  A
frozen 28-coefficient Nullstellensatz (13,350 coefficient characters) is in
`certificate_support6_fixed_left_partner_unit.json`; the independent source
rederivation and replay is
`audit_support6_fixed_left_partner_certificate.py`.  Certificate/audit logical
SHAs are respectively
`a17794ac82f6d4616af28fcf583567f1f92cc67de126b0cfe0b08b279d5cbd87`
and
`830839e18adb4be4aae7fd0cf70954eeb9103f40b409c0dfcb7d8e5d176d5c44`.

The entire localized weight-zero `d=0` chart is also explicitly normalized.
After the `b`-gauge, its base is affine four-space with coordinates
`y=(Q1,Q2,Q4,Q8)`, and `Q0` is one explicit quadratic form in `y`.  Every
point with Q-support at most eight is exactly one of:

- `y=0`, the support-six stratum closed globally above;
- one nonzero `y`, a support-eight axis; or
- two nonzero `y` with `Q0=0`, a support-eight two-axis stratum.

There is no genuine support-seven stratum.  The two-axis stratum has no Q
mate.  For a one-axis forced mate there is the compact literal identity,
modulo cells `{3,7,9,10,13,14,19,23}`,

`2 = x15*x16*x21*e01 + x15*x17*x20*e02 + e12+e13+e23 - t123`
`    - x6*x15*x20*Q3 - x2*x15*x16*Q5`.

The full-ring residual has only twelve terms and is retained explicitly as a
sum of multiples of those eight cell equations in
`audit_support6_forced_mate_compact_identity.py`; logical SHA
`51ea06939b5489678274aae78470d239c0b02f53bb440db9dffc79f42f66fec7`.
The full localized normal-form checker has logical SHA
`bd1d5367a978e964e15cab3dcdd53de0b1baf49d73018332af8c61477c2a0394`.

Thus the `d=0`, parity-weight-zero chart is closed for all Q-support at most
eight.  This is a theorem on one localized cofactor chart, not yet the whole
diagonal 270-row packet.  The remaining diagonal task is to extend the
normal-form/case split to the other localized block charts and parity classes,
or prove that every live point outside this chart has enough Q support to be
excluded pairwise.  Only after that diagonal theorem is complete does the
cross-colour-tail lift to the full normalized 240-variable chart become the
remaining step.

Three further simultaneous cofactor/cell-zero charts are now exact.

On branch mask 11 (parity weight four) with uniform `d_e=0`, five literal
cleared source rows (`t013,t023,Cof(0,2),Cof(1,2),Cof(3,2)`) combine to the
single Laurent monomial `z b0 b1 b2 b3 b4 b5`.  Hence the chart is empty
after imposing `z product(b_e)=1`, with no pure-H localization.  The compact
full sparse identity and mutation are in
`audit_weight4_dzero_unit_identity.py`, logical SHA
`874ede0c2e697042df7ff4eb2214e77c355bbd55686383b87539309ebfc2c321`.

On branch mask 0 with uniform `d_e=0`, gauge `b2=b4=b5=1` gives a
zero-dimensional quotient of vector-space dimension six, and all `a_e`
reduce to zero.  The six distinct points over `Q(z)`, `z^2+2z-1=0`, exhaust
the quotient.  Every point has `H=4`, Q-support
`{3,5,6,9,10,12}`, and lies in the globally excluded support-six joint orbit.
The completeness checker is
`audit_branch0_dzero_support6_classification.py`, logical SHA
`4122623aa6f6b07b32d5ccbc5116e629ba388f095fa79967dacc1fedf49e4f4e`.

On branch mask 1 with uniform `d_e=0`, the same gauge gives exactly two
irreducible one-parameter components, over
`z^2-14z-1` and `z^2+2z-1`.  With parameter `T=a5`, both have `H=4` and

- constant nonzero Q-coordinates `{3,5,6,9,10,12}`;
- nonzero linear multiples of T at `{1,2,4,8}`;
- a nonzero multiple of `T^2` at Q0; and
- identically zero coordinates `{7,11,13,14,15}`.

Thus `T=0` is the support-six orbit, while `T!=0` has support exactly eleven.
The exact two-minimal-prime classification is
`audit_branch1_dzero_classification.py`, logical SHA
`47347c17bf32402a3a2d6caed5632b9d6e49e98e46faa3ca4c93533bebd65f0d`.
Both generic components are also globally partner-free: fixing either on the
left forces five partner cells, eighteen partner cofactors, and eleven partner
Q-coordinates to vanish.  The resulting 39-row quotient ideals generate one;
each frozen lift uses only fourteen nonzero coefficients (213 and 215
characters).  Certificate and audit logical SHAs are
`09c8cda2a965dd8567f1947c16064c06d0b59a0608aa7d958c8b088f9c2f8d7c`
and
`a9c612a1b58b18866cf8bb0ff2d0ded432a18fb61ba2956a14d8d199ba0fb263`.

In the 50-orbit aligned chart convention `(cofactor mask, permanent-term
mask)`, these results identify three of the seven nonunit survivors:

- `(0,63)`: branch-0 uniform-`d=0`, now closed;
- `(1,63)`: branch-1 uniform-`d=0`, now closed; and
- `(0,12)`: the B4 image of branch-51 uniform-`d=0`, with a complete affine
  four-space normal form but only the support-at-most-eight strata closed.

The four genuinely new aligned charts are `(0,30)`, `(1,12)`, `(1,38)`, and
`(11,21)`.  Higher-support strata of the already-normalized `(0,12)` chart
also remain, so “not genuinely new” does not mean fully closed.

## A first off-boundary rigidity identity

The branch-0 uniform-`d=0` chart is rigid against releasing a single one of
its six lower-right cells.  On edge 01 write

`M_01=[[a0,b0],[-(1+a0*d)/b0,d]]`

and retain `M_e=[[a_e,b_e],[-1/b_e,0]]` on the other five edges.  Literal
substitution into the 22 branch-0 rows leaves fifteen distinct nonzero rows.
The localized Groebner basis has size 58 and dimension three, but its lift of
`d` uses only three nonzero coefficients.  In fact the proof is the human
two-cofactor identity

`Cof(1,0)=d*(-b4+b3*b5),  Cof(2,0)=d*(b4+b3*b5)`.

Their sum is `2*d*b3*b5`; since all six selected `b` cells are live, this
forces `d=0`.  The pure-H localization has coefficient zero.  Edge symmetry
gives the same conclusion for every one-defect release, although this says
nothing about two or more defects released simultaneously.

The frozen lift is `certificate_branch0_one_defect.json`, logical SHA
`fcba1015b2c66436f493425d5610c210a2dbba9291ff579f24c488266b3dbb09`.
The independent raw-row replay, sign mutation, and three-mode check is
`audit_branch0_one_defect_certificate.py`, logical SHA
`33f89235d71653579f2f7c9fb882367b5522514642f42fb317aeda5d1b7ad3c0`.

## Complete closure of aligned survivor `(11,21)`

The final assigned genuinely new aligned chart has an exact two-line normal
form.  After the three-cell spanning-tree gauge `b0=b4=a3=1`, its fifteen
literal distinct rows have a dimension-one ideal with exactly two minimal
primes over Q.  They are matched in both directions to the following lines
over `Q(r)`, `r^2-2r-1=0`, with parameter `T=b3`:

- `b1=(r-2)T`, `b2=a1=r`, `b5=0` on both lines;
- on the first, `a5=r-2` and
  `(a0,a2,a4)=((3r-15),(30-13r),(4r-13))*T/7`;
- on the second, `a5=-r` and
  `(a0,a2,a4)=((3r+9),(6-5r),(-4r-5))*T/7`.

Every literal source row vanishes and the raw pure Hafnian is exactly 4.  At
`T=0`, both lines lie in the already excluded support-six joint orbit.  At
`T!=0`, both have Q-support
`{0,1,2,3,4,6,7,8,10,11,14}` and the same 17-cell support; their cofactor
supports are respectively `{3,9,10,12,15,21}` and
`{3,4,7,17,18,21}`.

For each generic line, fixing the left colour forces six partner cells,
seventeen partner cofactors and eleven partner Q-coordinates.  The resulting
38-row quotient ideal generates one without a partner-H localization.  The
two exact lifts use 22 and 14 nonzero coefficients (415 and 211 characters).
The independent audit rebuilds all rows from the literal source, restores the
full-ring residual as a multiple of the six cell equations, and fires a sign
mutation.  Classification, certificate and audit logical SHAs are
`bcb36aae97554efd441021f506bc5c2f122300e092e2f446084d511444dc36e6`,
`666b8ba0d38d27ddaba1695cb5933d49f8d4a780fc7938e6003f02f91efd8912`,
and
`156f4eed984458a715455d01fb7c86d6cc83d730c91a3e9254f7d7c55631e6e8`.

Thus `(11,21)` and every simultaneous B4 transform is closed on the entire
aligned zero-cell boundary.  Companion lanes have separately reduced
`(1,12)` and `(1,38)` to the support-six orbit; `(0,30)` is being handled in
the Huygens lane.  Those companion conclusions are not reproved here.

## The branch-0 four-cycle and its boundary guard

For the defect cycle `S={1,2,3,4}`, use the lossless gauge
`b2=b4=b5=d2=1`.  The apparent p=7 survivor is an exact characteristic-zero
two-parameter family over `Q(r,t,u)`, `r^2+2r-1=0`:

```
d1=r, d2=1, d3=t, d4=-r*t,
a1=-r-2, a2=-1, a3=-1/t, a4=(r+2)/t,
b0=t, b1=(r+2)(u-1)-t, b3=u/t,
a0=2(r+2)(1-u)/t, a5=0.
```

Here `c1=c2=c3=c4=0`, `c0=-1/t`, `c5=-1`.  All 22 literal source rows
vanish and the raw pure Hafnian is exactly 4.  The specialization
`r=2,t=1,u=5 (mod 7)` reproduces the earlier finite-field point; its raw
Hafnian is 4, correcting the denominator-cleared probe value 6.  This is not
a point of the true both-term-live interior.  It is the fully aligned chart
`(branch,term)=(0,33)`, canonically `(0,12)`, and is therefore a boundary
control rather than a counterexample to an interior unit.

The exact replay and mutation are in
`audit_branch0_cycle_czero_component.py`, logical SHA
`5dcb5dc3ad09933773076efd5b25c3a069e6f239c523a2c2a97218d16f8c7b48`.

The whole boundary requires a stronger guard.  Writing
`Cprod=product_{e in S}(1+a_e*d_e)`, `Cprod=0` is a union of fifteen strata,
not just the fully aligned one.  If the zero set is `Z`, switch the dead
offdiagonal selected terms on `Z`; the induced term mask is `63 xor Z` and
the remaining genuinely full support is `S\Z`.  The zero-count histogram is
`4,6,4,1`; the six two-zero strata split as four adjacent and two opposite.
Only `Z=S` has no remaining full block and belongs directly to the closed
50-chart aligned family.  Every proper `Z` is a lower-defect recursive chart,
so an interior saturation plus the aligned endpoint alone would not close
the original k4 chart.

All fifteen canonical `(branch,term,remaining)` triples are frozen in
`audit_branch0_cycle_boundary_covariance.py`, logical SHA
`07871886949591b5a78924f54d39ea070ce976310108ed85884b97a320a56977`.
The corrected interior localization additionally inverts every factor of
`Cprod`.  Exhaustive source-faithful screens find no full point over F5 or F7,
but direct modular/exact Groebner runs remain fill-bound; this is evidence,
not a characteristic-zero theorem.

The smallest current interior elimination interface uses
`p_e=a_e*d_e`.  Four upper cofactor rows solve `p1,...,p4`; the three rows
`t012,t013,Cof(5,0)` solve/check `a0`, and `t023,t123` solve/check `a5`.
After these nine rows the exhaustive F7 screen leaves 78 interior candidates.
Adding `Cof(0,0)` and `Cof(0,3)` kills all 78 (over F5, `Cof(0,0)` alone
kills all ten survivors).  Thus an eleven-row Cramer/Schur elimination is
the most focused next exact computation.  Its upper determinant is

`4*b0^2*b1*b3*d1*d3*d4*(b1*d3+b3*d1*d4)^2`.

The resulting split factor is
`Delta=b1*d3+b3*d1*d4`.  Nevertheless, p1009 `slimgb` still times out at
120 seconds for the eleven-row model with a product localizer, separate
localizers, block order, and both `Delta` branches.  No conclusion is drawn
from these timeouts.  The determinant itself is independently rebuilt from
the four literal source rows, including its two `2x2` block zero pattern and
a hostile sign mutation, in `audit_branch0_cycle_upper_cramer.py`, logical
SHA `104b824e72f6e8617e48bf34976e095b21105b0447447f079c1231d2cedf608d`.

One solve-denominator subbranch is now closed exactly.  Retain
`Delta!=0`, `D0=d1*d4+d3!=0`, but set `B0=b1+d1=0`.  The literal `t023`
compatibility numerator factors as

`2*b0^2*d1^3*(b3*d4-d3)*(d1*d3-d1*d4-d3-d4)`.

Thus the first three live factors force
`d1*d3-d1*d4-d3-d4=0`.  On the subsequent `t123` factor
`Kplus=b3*d1-b3+d1+1=0`, the source rows `Cof(5,0)` and `Cof(0,0)` solve
`a0,a5`, while `Cof(0,3)` forces
`b0^2*(d1^2-1)-2*d1*d4=0`.  The remaining `t012,t013` numerators are two
quadratics in `b0`; their exact resultant is

`16*d1^5*(d1-1)*(d1+1)^5*(d1^2+1)^2`
`*(d1^2-2*d1-1)^2*(d1^2+2*d1-1)^2`
`*(d1^4+2*d1^3+2*d1^2-2*d1+1)^2`.

All prefactors in the first line are already live.  On
`d1^2+2*d1-1=0`, the two quadratics force `b0=d1`, and `1+p1=0`.  On
`d1^2-2*d1-1=0`, `Cof(3,3)` gives a linear separator whose two nested
norms end in `-128`.  On the quartic factor, the same lower cofactor has
norm `119563878400`.  Hence the entire `B0=0,Kplus=0` subbranch is empty
over characteristic zero.  This does not close `Kplus!=0`, `D0=0`, or
`Delta=0`.

The source-derived replay, exact resultants, lower-cofactor separators and
hostile mutation are frozen in
`audit_branch0_cycle_b0_denominator_kplus.py`, logical SHA
`7a035c72cc0aaa68501f33a9435ca3aee68b390278056c61570ca1abdda55ae6`;
the checker passes standard, `-O`, and `-I -S` modes.

The first exceptional solve inside the complementary `Kplus!=0` branch is
also closed.  There `t123` solves `a5`; after removing the live `b3` factor,
`Cof(0,0)` has form `(d1-1)*L*b3-d1*M`.  On `L=0`, it forces `M=0`, and

`Res_b0(L,M)=2*d1*(d1-1)^2*(d1^2+2*d1-1)`
`*(d1^2*d4+2*d1*d4-2*d1+d4)`.

The degenerate factor `d1^2+2*d1-1=0` makes all four `p_i=-1`, violating
the selected-term localizers.  Off that factor, `L=M=0` parametrizes
`b0=(d1^3+3*d1^2-d1+1)/((d1-1)(d1+1)^2)` and
`d4=2*d1/(d1+1)^2`.  The remaining two triangles have 34 and 24 terms;
`Cof(0,3)` splits into two linear-in-`b3` factors.  The first factor has
triangle norm
`38973380220162416179749905447126040576`.  For the second, the apparent
cubic component is a leading-coefficient degeneration whose surviving
constant has norm `-256`, while the only quartic component forces
`Delta=0`.  Hence `B0=0,Kplus!=0,L=0` is empty on the `Delta!=0` chart.

The exact sparse source replay and mutation are in
`audit_branch0_cycle_b0_kplus_complement_lzero.py`, logical SHA
`d37553fae0ea8caaff14216c571e1e0232e57f98b243d9d9b626d50ffe5c67b0`;
standard, `-O`, and `-I -S` all pass.  The new remaining part of `B0=0` is
the honest `Kplus!=0,L!=0` branch; `D0=0` and `Delta=0` also remain.

The `L!=0` part has now been compressed to a source-faithful finite
resultant interface.  Solving

`b3=d1*M/((d1-1)*L)`

leaves four literal numerators `F160,G84,C9,C35` over
`Q[b0,d1,d4]`.  The first two are the retained triangle equations.  The
`C9` compatibility has shared factor
`Q=d4*(d1+1)^2-2*d1`; on `Q=0`, however,
`C9=(d1^2+1)*L`, so the branch is excluded by `L!=0`.  Its remaining
resultant factors are `d1^2+2*d1-1`,
`d1^3+d1^2+3*d1-1`, the live numerator of `b0`,
`d1^4+6*d1^2+1`, and one degree-34 factor.  The `C35` tree shares `Q`,
the quadratic, the live numerator, and has one additional 13-term
degree-eight factor.  This is an exact reduction interface, not itself an
emptiness theorem.  It is frozen in
`audit_branch0_cycle_b0_lnonzero_residual.py`, logical SHA
`4fe39f575c7dc4172b11fbf8547ac39c746cc041c44fffa5c93f3f53d705df6e`;
standard, `-O`, and `-I -S` all pass.

One exceptional determinant inside `D0=d1*d4+d3=0` is also closed.  The
rows `Cof(0,0),Cof(5,0)` are linear in `b1,b3`, with determinant

`-2*b0*d1*(b0^2+d4^2)`.

On `C0=b0^2+d4^2=0`, augmented consistency forces
`(d1^2+1)*(d4-1)=0`.  If `d4=1`, two triangle rows force `b3=-d1`, and
the final two `a5` rows have resultant `-8*d1^5`.  If `d1^2+1=0`, the two
signs `b0=+-d1*d4` reduce to a common norm polynomial
`d4^4+6*d4^2+1`; direct literal replay on that quartic gives nonzero norm
`42467328` in both signs.  Thus the full `D0=0,C0=0` subbranch is empty
over characteristic zero.  The exact source replay and mutation are in
`audit_branch0_cycle_d0_cramer_exception.py`, logical SHA
`a8b5f3480b137580b6cd6751171afdc2cec5cc6505239e6cd62ba47fa776e6d0`;
standard, `-O`, and `-I -S` all pass.  The complementary `D0=0,C0!=0`
branch and `Delta=0` remain.

The `Delta=0` branch now has its own exact rank-two interface.  Writing
`x=b3/b1` gives `d3=-x*d1*d4`; the four upper cofactors solve two p
variables and reduce to the displayed equations `U=V=0`.  On `b1+d1!=0`,
the remaining six literal rows form a `6x4` augmented linear matrix in
`p1,p2,a5`.  On `b1+d1=0`, a complementary matrix and the forced factor
`W=d1^2*x-d1*x+d1+1` are retained without dividing any non-live row gcd.
The source/mutation interface is
`audit_branch0_cycle_delta_zero_linear_interface.py`, logical SHA
`6306fccb20f4af48e0739f6a1231c2b2e5ee0f38da439e35cba978f92344b998`.

The entire `Delta=0,b1+d1=0` branch is empty.  The companion `x=1`
packet is a direct unit.  For `x!=1`, `W=0` solves x; the `U,V` resultant
splits into the selected-term contradiction `p2=-1` and a bivariate factor
P.  On P, a linear subresultant solves b0.  The generic terminal equations
have incompatible degree-18/22 univariates.  Both zero triangle-coefficient
exceptions have common factor only `d1^2+1`, which is incompatible with P.
The exact replay is `audit_branch0_cycle_delta_bplus_generic.py`, logical
SHA `37cbc170f9b656d39980ba441d6394510d55da0b1c9752662f8fb8de733763a4`;
all three Python modes pass.

For `Delta=0,b1+d1!=0`, the whole divisor where the d4 coefficient

`Au=-b0*d1*x-b0*x-d1*x-1`

vanishes is also empty.  Here `U,V` force
`b0=-d1`, `x=d1^-2`, and
`d4=-d1^3(d1+1)/(d1-1)`.  The remaining six-row packet has term counts
`[9,0,0,8]`, `[0,5,0,11]`, `[2,2,2,3]`, `[8,8,8,12]`,
`[8,8,3,12]`, `[12,12,5,13]`.  Its generic terminal resultant has five
small factors, all excluded by exact unit/Bplus checks.  The t012
zero-coefficient ideal contains the live factor `b1^2(d1+1)`; the sole
nonunit t013 exception contains the live selected factor `p1+1`.
`audit_branch0_cycle_delta_au_zero.py` freezes the literal replay and
mutation, logical SHA
`082927b0fa7e9d162872a30aab6f5587ed20f9d99c7b8bed87738d6c6c59c942`;
standard, `-O`, and `-I -S` pass.

The complementary `Au!=0` locus has no generic component.  Solving U for
d4 makes V the 12-term quadratic

`Q=b0^2*x^2*((d1-1)^2*x-(d1+1)^2)+C(d1,x)`.

The quadratic is irreducible over `Q(d1,x)`: the displayed linear factor A
is coprime to C and occurs to odd valuation.  Two source-derived 4x4
consistency minors, rows `(2,3,4,5)` and `(0,2,3,4)`, reduce modulo Q to
938/1526-term polynomials of b1-degrees 5/4 after removing only the live
factor `b1^2`.  Their resultant class is nonzero over the quadratic function
field; an exact specialization `(d1,x)=(2,3)` gives
`Q=-2*(27*b0^2+13)` and a nonzero linear remainder.  Therefore no component
dominates the `(d1,x)` plane.  This does **not** close the proper resultant
or denominator divisors.  The exact generic theorem is
`audit_branch0_cycle_delta_au_open_generic.py`, logical SHA
`5a3740767646cf9d898b883f04f3d0b927eb6049bd2191d0a6e6d9bbdfa985c2`;
all three modes pass.

For modular decomposition of those remaining divisors, Q plus the two
minor cores is exported in variables `b0,b1,d1,x`.  The raw p1009 file has
SHA `65843ad1...`; the large-prime live-saturated F4SAT input at p1073741827
has SHA `c66b0998...`.  The deterministic exporter
`export_branch0_cycle_delta_au_open_msolve.py` has logical SHA
`9065772ef2214954774db80220d0ab9cc62fc48e129916a13147390aa2a3f573`.
Projection has forgotten the selected `p_i+1` localizers, so a negative
modular result would remain nonterminal; a positive unit can be replayed in
the full packet.

The quadratic-leading exceptional divisor `A=0` inside this `Au!=0` locus
is now closed exactly.  Since `Q=0` as well, its exact resultant is

`16*d1^2*(d1^2+1)*(d1^2+2*d1-1)`.

The live `d1` factor leaves two branches.  They force respectively
`(d1^2+1,x+1)=0` and
`(d1^2+2*d1-1,x-2*d1-5)=0`.  After the exact `U`-solve for `d4`, the six
literal augmented rows together with all four selected-term localizers,
the declared solve factors, and `Au` have exact characteristic-zero unit
Groebner bases on both branches; the pure Hafnian is not used.  The guarded
checker is `audit_branch0_cycle_delta_au_open_a_zero.py`, with logical
result digest
`acf8fb11c47016a5e9d2aa11a587c7ce4aeb477c434e0891ea06927636c8e4f4`;
standard, `-O`, and `-I -S` all pass.  Direct `liftstd` and targeted `lift`
did not terminate within the bounded runs, so this artifact certifies the
exact unit bases but does not claim a sparse literal multiplier ledger.
The remaining `Delta=0` work is confined to the proper `A!=0`
resultant/denominator divisors.

Those `A!=0` divisors now have a much smaller exact projection interface.
Let `L,R,T` be the literal consistency minors on row sets `(2345)`,
`(0234)`, and `(1234)`.  For each pair form

`rho=NF_Q(Res_b1(minor_i,minor_j))=rho1*b0+rho0`

over the quadratic `Q=x^2*A*b0^2+C`, and then the exact quadratic norm

`N_ij=num(x^2*A*rho0^2+C*rho1^2)`.

This computation takes about twenty seconds per prime, replacing the
fill-bound four-variable elimination.  At both `p=1009` and `p=1013`, after
removing only the declared live factors, the three norms have one
irreducible non-live factor each, of respective total degrees
`348,340,351` and multiplicity one.  The numerator/denominator profiles are

```text
LR: unit*(x-1)*C^6*F348 / A^4
LT: unit*(x-1)*C^6*F340 / A^4
RT: unit*(x-1)*C^7*F351 / A^6.
```

Thus the third source minor removes the degree-348 curve as a component:
any surviving modular parameter point lies in the finite triple
intersection `F348=F340=F351=0`.  This is deliberately only a two-prime
discovery statement, not a characteristic-zero emptiness theorem.  The
factor files and irreducibility replays are frozen in
`audit_branch0_cycle_delta_au_open_pair_norm_residual.py`, logical digest
`d4a762dec07a378405a31595dd5cf91b3f1a841cdfde2b0945d950d915b86366`;
the shared three-mode runner manifest has logical digest
`119c2bb3939f27be08201a74086b502e01de59a34c48595137ec67ada19358ce`.

The strict three-minor msolve export has input SHA
`ea721f77db438c31b1f40c7f0c452858fff77acb5e1c971ae423b6a6be9b3049`.
Guarded F4SAT completed in 190 seconds with a 193-element basis, but its
staged elimination timed out at 600 seconds with zero output.  The direct
two-variable norm-triple msolve basis timed out at 300 seconds, and a
bounded Singular lex run timed out at 180 seconds.  None of those timeouts
is used as evidence.  The earlier independent two-minor staged elimination
was interrupted after 33 minutes and roughly 13 GB once the quotient norm
subsumed its discovery role; it produced no output and no claim.  The honest
remaining branch is therefore the exact-Q lift/classification of the finite
triple-norm intersection, together with restoration of all selected-term
localizers in the full six-row packet.

A complete necessary rank obstruction is now frozen as well.  All fifteen
maximal minors of the literal `6x4` augmented packet matrix were recomputed
after the exact U/Q quotient and removal of only declared live monomials.
The strict large-prime input has SHA
`9a35d90174bb0ac4323b3db78aa0df9c2c4d9b09d7620fff571384e993c6d79a`;
the exporter verifies that a literal `t_013` sign mutation changes exactly
the ten minors containing its row.  At `p=1073741827`, chart-live F4SAT
terminates in 458.6 seconds with a nonunit, zero-dimensional 117-leading-term
basis.  Its standard-monomial degree is 268 (Hilbert values
`1,4,10,20,35,56,84,58`).  The output SHA is
`50107ba9ea3b644bb8c0e5e027aa9a09e305f343cd2c0eddc0b8dbbac2450dda`
and the toolkit manifest logical SHA is
`fa68e694683723b3f89acff72a2608074e51999b00293c1597301a89aae5acd4`.
This removes the extension-field curve caveat from the three-minor model:
every actual packet solution lies in a finite exceptional scheme.  It does
**not** prove emptiness, since maximal-minor points can be rank-deficient
false positives and selected `p_i+1` factors remain projected out.  Over
`F_1009`, the rational points of the three-norm residual give 3,033 lifted
minor fibres: 3,029 hit excluded live divisors and the other four have
coefficient/augmented ranks `3/4`; all four are detected by the smallest
unused core, minor `(1,2,3,5)`.  This rational census is only a diagnostic.

The full basis and rational-parametrization computation has now been
repeated at the independent 30-bit prime `1073741789`.  The exact integer
rows are unchanged under rebasing (strict input SHA
`6989314791c6cbf500a614570c86c38f034465017a1f4085f710dc95f6b6b872`),
and F4SAT again gives a zero-dimensional degree-268 scheme.  Its guarded
parametrization has logical SHA
`552ffd0ecfaa509aebdddc28894f122c2e8e745b2fcc0af929b5db1e994556f7`.
Literal finite-field replay of the U/Q solve, all six augmented packet rows,
all four selected factors, and the pure Hafnian shows that every one of the
16 irreducible components at both primes has coefficient/augmented rank
`3/3`, permits all four selected factors to remain nonzero, and has nonzero
pure Hafnian **inside this necessary subsystem**.  This replay uses the
eleven literal rows `Cof(1..5,0)`, the four triangles, `Cof(0,0)`, and
`Cof(0,3)`; it omits the five remaining literal rows `Cof(1..5,3)`.
Therefore these are not genuine full one-colour packet points.  An
independent replay of the first quadratic component finds all five omitted
cofactors nonzero.  A subsequent independent full raw-row referee proves the
stronger statement at both large primes: on every one of all 32 irreducible
factors, exactly `Cof(1..5,3)` are nonzero and every other nontrivial literal
row vanishes.  Hence all 32 are full-source false positives.  Its result SHA
is `36dfe4bcee4855b546de0d837405ed0e2b239345eb0859eeacadfc9a06018188`.
The factor splittings differ
(`2^6 6^2 24^4 28^2 46^2` versus `2^6 4^6 10^2 106^2`), so individual
modular quadratic factors cannot be paired or promoted to characteristic
zero.  The parameterized referee is
`probe_branch0_cycle_delta_au_open_all_minor_components.py`; its surviving
status is explicitly named `necessary_subsystem_fails_omitted_cofactor`.  The
canonical exact-Q RUR remains useful only as a finite quotient in which to
test those five omitted cofactors; it cannot itself certify a packet point.

For a direct characteristic-zero classification, the same sixteen integer
equations have been exported with a new Rabinowitsch variable: the F4SAT
saturating factor is replaced exactly by the fully distributed equation
`z*live-1`.  The first sixteen rows are byte-identical to the prime-field
seed, and an independent text inverse recovers the live factor from the
expanded final row.  The exporter
`export_branch0_cycle_delta_au_open_all_minors_char0.py` passes standard,
`-O`, and `-I -S` through the common checker, logical SHA
`eb9c47dc49b1f45ba4a6b2602f0beed405b1660e0331c6aec48aeb420d2ec1a0`;
the canonical input SHA is
`d53b3b284e83a9798f5236921c6eccdfce6ccb6c7ac7eed6bc4de3e55b0ccf14`.
An earlier manual distributor placed some numeric coefficients after `z`
(for example `z*2*monomial`).  Msolve 0.10.1 silently parses that differently
from the canonical `2*monomial*z` despite reporting zero invalid equations.
The resulting 18-minute positive-dimensional sentinel is therefore
withdrawn as corrupted input, not a geometric statement.  The canonical
export uses SymPy's coefficient-first printer and proves symbolically that
the z-derivative of the final row is the frozen live factor and its z=0
specialization is `-1`.  No exact-Q conclusion is currently claimed.

The five omitted lower cofactors now close that finite residual exactly.  A
fraction-free Cramer construction is essential because a lower cofactor is
quadratic, not affine, in the remaining unknowns `p1,p2,a5`.  Using retained
rows `t_023,t_123,Cof(0,0)`, homogenize the literal numerator of
`Cof(3,3)` by the square of their 10-term coefficient determinant and
replace `D*p_i` by the three adjugate numerators.  This identity remains
necessary when `D=0`; no pivot factor is divided out.  After the exact
Au-open d4 solve, reduction modulo Q, and removal only of the chart-live
monomial `b1^5*d1^3`, the resulting parameter core has 4,031 terms and
degrees `[1,7,24,19]` in `(b0,b1,d1,x)`.  It is substantially smaller than
the analogous `Cof(1,3)` core (7,264 terms), whose p1 F4SAT timed out at 600
seconds without output.

The compact exporter
`export_branch0_cycle_delta_au_open_cofactor33_compact.py` includes the
literal clearing denominator `(b1+d1)*(x-1)`, the Cramer homogenization
identity, a source mutation, two strict modular inputs, and a
coefficient-first characteristic-zero Rabinowitsch input.  Standard, `-O`,
and `-I -S` pass with logical SHA
`4465d3080dae3c77ae506be5859c736846c0ef26fad5ebe462c85583953af747`.
F4SAT gives a unit basis at both independent 30-bit primes: 406.01 seconds
at `1073741827` (manifest logical SHA
`dcd25ad899bbee340db8444954203e92df2fcb5eb96d5b7c42c2e846f8f5e3b7`)
and 357.10 seconds at `1073741789` (logical SHA
`1afb6b4693d030103bde44f539335355fe20c2039768a2c4bd64c91ff3ee5a57`).

Most importantly, the canonical characteristic-zero solve terminates in
223.85 seconds with the literal output `[-1]:`.  The common runner parses
this as the empty degree-zero scheme, logical SHA
`440aee99e70783bd6101994939b610739d4556b95bc54e68880b0d8592bd181f`.
The source/output referee
`audit_branch0_cycle_delta_au_open_cofactor33_exact_unit.py` independently
rederives the 4,031-term core, checks that it is the penultimate exact input
row, and verifies the exact empty output and manifest.  Its result SHA is
`bab619bc8240d8ac2ae9cc6296069a3a1b6a23d6c7c6a2576b30fa44d6f3ac4e`;
its three-mode runner logical SHA is
`201ec6c276c12f08614d174c3b7828c9757fd850c7cd565d3aa258c8a0a68353`.
Therefore no full literal packet solution exists on the
`Delta=0,Bplus!=0,Au!=0,A!=0` branch.  Together with the previously frozen
`Bplus=0`, `Au=0`, `A=0`, and solve-denominator closures, this completes the
Delta-zero subtree of the branch-0 four-cycle.  This is an exact emptiness
theorem, though the engine output is not a sparse multiplier ledger.

The remaining fully generic interior chart
`Delta*D0*Bplus*b0*b1*b3*d1*d3*d4 != 0` has now been reduced against the
same literal upper-Cramer, `a0`, and `a5` solves without importing any result
from the closed `B0=0` factor tree.  The five retained compatibility
numerators have `(terms,total-degree)` profiles
`(63,13),(63,9),(44,11),(72,12),(73,10)`.  Reducing every omitted lower
cofactor source-faithfully shows that `Cof(3,3)` and `Cof(4,3)` are smallest
at 472 terms; `Cof(3,3)` has the lower degree 15 after removing exactly the
declared live factors `Delta*b1`.  The other omitted profiles are
`487/15`, `487/17`, `472/16`, and `504/16` after their live linear factors.

The exporter `export_branch0_cycle_generic_cofactor33_core.py` freezes this
six-row necessary core, verifies the exact solve denominators, and includes
a literal-source mutation.  It deliberately saturates only at the nine
actual solve/chart factors above: it does not use `p_i` or `1+p_i`, so a unit
would be stronger than emptiness of the both-term-live interior.  Its
standard, `-O`, and `-I -S` replay passes with logical SHA
`05f4cc2499775bf378bf010ddd0891fed2171dbee1688cb11af4ff5763eabe54`.
The requested single-prime gate at `1073741827` did not terminate: native
F4SAT was stopped by the common runner after 600.70 seconds with zero output,
manifest input logical SHA
`73c65ae35daaf7518a9b0f77ad41e1c0bffbacba7f2d54e7f1c135f995c8b74f`.
Consequently no second prime or exact-Q run was launched, and this generic
interior remains open rather than negatively certified.

An exact structural pivot avoids repeating that broad computation.  After
removing only the already frozen live monomial factors from the five retained
compatibilities, normalized `t_013` is affine in `b3`:
`t_013=2*b0*(A*b3+B)`, where `A` has 19 terms/degree 6 and `B` has 44
terms/degree 7.  Thus the generic residual splits first into `A=0` (where
`B=0` is also necessary) and `A!=0`, on which `b3` is eliminated by the
fraction-free identity `Res(A*b3+B,f)=A^deg(f) f(-B/A)`.

The five exact resultants have primitive factor profiles
`D0*b0^2*P851`, `b0*P1342`, `b0*P324`, `b0*P1846`, and
`D0*b0^2*C8*Q4098`, with subscripts denoting term counts after the frozen
live factors.  The smallest new split is therefore the omitted-Cof(3,3)
quartic
`C8=b0^2*d1*d3-b0^2*d3-b0*d1*d3*d4-b0*d1*d3-b0*d1*d4-b0*d3*d4-d1*d3*d4+d1*d4^2`
versus the 4,098-term degree-26 factor.  This is an exact residual split, not
an emptiness theorem.  The audit
`audit_branch0_cycle_generic_b3_resultant_tree.py` replays all factorizations;
standard, `-O`, and `-I -S` pass with logical SHA
`a7a76b9d51f6f8c26a823b7613950244db2e9b2507131c54b50e76b47469e917`.

The small `A!=0,C8=0` side has also been tested directly, without replacing
the source rows by their resultants.  The exact input contains the original
five generic compatibility numerators, the cleared literal `Cof(3,3)` row,
`C8`, and one Rabinowitsch equation localizing precisely
`b0*b1*b3*d1*d3*d4*Delta*D0*Bplus*A`.  The exporter
`export_branch0_cycle_generic_aopen_c8_exact.py` passes standard, `-O`, and
`-I -S` with logical SHA
`8dc69457d88212334c45fa811a206009525f738cde18106184242eb0d401502c`.
One characteristic-zero Singular `slimgb` run was stopped at the requested
ten-minute cap (10m13s wall time including the final poll); it was still at
the `slimgb` command, used about 2.06 GiB RSS, and emitted no basis or
component.  Hence `A!=0,C8=0` remains open; no second engine/run and no claim
of nonemptiness or emptiness is made.  The `Q4098` and `A=0,B=0` sides were
not touched.

The engine-specific timeout is now superseded by an exact reverse gate on
the identical ideal.  The exporter also emits a canonical coefficient-first
msolve characteristic-zero input: the same six source-derived rows, `C8`,
and the fully expanded Rabinowitsch row, with no forbidden parentheses or
post-variable coefficients.  Its updated three-mode export logical SHA is
`7dfb75e59d5f2856d0b0ffbdd1bbed40ab70dd5e1c0f1a30c884165f393db9e1`.
The common exact parametrization runner terminates in 30.90 seconds with the
literal output `[-1]:`, identifying the degree-zero empty scheme; runner
logical SHA
`13ee888f9d7983f4d355cf2018f7f7e59df626f5e5d3dc35ed6e53d1cf1cff55`.

The independent referee
`audit_branch0_cycle_generic_aopen_c8_exact_unit.py` rederives all eight
canonical rows from the frozen source, checks the variable order and strict
syntax, differentiates the expanded sentinel back to the exact ten-factor
live product, checks its `z=0` specialization is `-1`, fires a source-row
mutation, and requires the byte-literal output plus runner hashes/scope.  Its
result SHA is
`009ead4b3ad57e5b8f028b42534e40b6405a42abea0c6b74ba45b2311ad40d12`;
standard, `-O`, and `-I -S` pass with logical SHA
`3858646199f090c13236b73be3cf4bb3eb7f1fc5b1c59ef8303d633c6ec912f7`.
Therefore the generic `A!=0,C8=0` branch is exactly empty over characteristic
zero.  Only the `A!=0,Q4098=0` and `A=0,B=0` residuals remain from this
resultant tree.

The complementary `A=B=0` branch is not killed by the same necessary core.
Its canonical exact input imposes the original six direct rows, `A`, `B`,
and localizes only at `b0*b1*b3*d1*d3*d4*Delta*D0*Bplus` (not at `A`).
The export passes three modes with logical SHA
`c4d8e73fef732217db35f9b79976b0c86db91e8b8849533bbfe18f284b0c7736`.
The exact gate terminates in 125.69 seconds with the literal msolve sentinel
`[1, 7, -1, []]:`, i.e. a positive-dimensional necessary-core scheme in
seven ambient variables including the inverse variable.  The independent
source/sentinel audit passes three modes with logical SHA
`8dbf218bf60d21ddc5633881ddded2314c5064e4aa38be1ee18a6a6948eda2f6`.
This is explicitly not a full packet point.

Adding the next-smallest literal omitted lower row `Cof(4,3)` does not yet
kill it.  That row is rederived from the literal source through the same
Cramer/`a0`/`a5` substitutions, with only live `Delta*b1` removed; it has
472 terms and degree 16.  The canonical export passes three modes with
logical SHA
`48eb63519390f96c08cf91c225411141426e42d9527123ff79050cabfc4a0be6`.
The exact gate again returns `[1, 7, -1, []]:` after 134.54 seconds, runner
logical SHA
`94baa35515c692d8fa7d1d4b375a041b9ba8aacbb8d3586e54daa7fb5f91f020`.
Its independent ten-row source, sentinel, and mutation referee has result SHA
`ed6d8a0dfcbd08ddf03f72f361f26bf5481da3daced8687d12260bc3171dbb04`;
three-mode logical SHA
`b0572098341aa7b239732b5b80d3ff7dfafa41f4f957f84f0d873360518bb576`.
Per scope, this lane stops here: other omitted lower cofactors may still kill
the component, no full-source solution/counterexample is claimed, and the
`A!=0,Q4098=0` branch remains untouched.

The `A=B=0` reduction has now been completed source-wise.  Adding the three
remaining lower rows `Cof(1,3)`, `Cof(2,3)`, and `Cof(5,3)` gives exact
coverage of all sixteen distinct literal rows: six Cramer/solve equations,
five compatibility numerators, and all five lower cofactors.  No localization
was added beyond the frozen nine chart/solve factors.  The full-source export
passes three modes with logical SHA
`1d1f6a462f997da9af9f89db595207ca5aa7270b4f64b57aacc846012313cdf7`.
The exact gate still returns the positive-dimensional sentinel
`[1, 7, -1, []]:` after 96.93 seconds, runner logical SHA
`f3905ce5cfaf032ceaedb66a42a6487ae938a1af6c728d46a8b38ce1d3a7367d`.
This establishes only a positive-dimensional full one-colour zero-row
scheme; it is not yet an H-live packet component.

The literal Hafnian test is now frozen exactly.  After the same Cramer,
`a0`, and `a5` substitutions,
`H=b1*b3*Hcore/(b0*Delta^2*D0)`, where `Hcore` has 258 terms and degree 15.
Every displayed denominator and the `b1*b3` numerator monomial is already
live, so the decisive input replaces the final sentinel by the prior
nine-factor product times `Hcore`, leaving all source rows unchanged.  Its
source/H/sentinel exporter passes standard, `-O`, and `-I -S` with logical
SHA `9be9d9914e7ca30f094034f7125f3160ddf5b6f9297dd0bc5511b8f595129788`.
The exact characteristic-zero gate timed out at 600 seconds with zero output,
runner logical SHA
`98bc82267b39fd8f33add56706f62d0a77d5d5aa46bb976381ef8b9c018ab0f1`.
Thus the full-source `A=B=0` component is neither proved H-dead nor proved
H-live; no genuine packet component/counterexample claim is made.  The other
generic residual `A!=0,Q4098=0` remains untouched.

Two bounded modular diagnostics also fail to resolve the H status.  The
canonical large-prime interfaces are emitted from the same exact source/H
derivation and now pass three modes together with logical SHA
`cb7fa0c45552c09d194bd663133e5e649159aba1b438439069d1f7e47b86c752`.
First, native F4SAT at `1073741827` on the H-open system timed out after
300.43 seconds with zero output (input logical SHA
`11b58d82228b9d8c25ce1c7a25d3430831399e69e8164d2854f70b75066146a5`).
Second, a full-basis F4SAT run on the already-positive full-source `A=B`
component using only the original nine-factor localization, specifically to
reduce `Hcore` in its quotient, also timed out at the 300-second cap with
zero output.  Thus there is neither a modular UNIT nor a quotient normal form
for H, and no second prime was run.  This is the terminal H-status blocker for
this lane.

The complementary `A!=0,Q4098=0` side has been reduced source-faithfully by
successively restoring every omitted lower cofactor.  Fraction-free
elimination through the exact affine `t_013` pivot gives
`Cof(4,3) -> b0^2*D0*C8*R4885`,
`Cof(1,3) -> b0^2*D0*C8*S4331`,
`Cof(2,3) -> b0^2*D0*C8*T4750`, and
`Cof(5,3) -> b0^3*D0*C8*U3217`, after removing only the displayed frozen
live factors and the separately closed `C8` branch.  `Q4098` and `R4885`
have exact gcd one; `T4750` has exact gcd one with each of `Q4098,R4885,
S4331`.  These gcd statements exclude common hypersurface factors only and
do not empty their intersections.  The `Q/R` three-mode export logical SHA
is `f20819e5d80154f8328e48b7d9b2b0a036fa50b6fd5571963cc8a7312e945b36`;
the `T` source/gcd interface logical SHA is
`fa010c9db0377c5ecd272d80d10ec3cbd16c98068d993387b6eabf4a478417f2`.

The reduced exact `Q=R=S=0` gate, together with all four retained
compatibility factors and the precise ten-factor A-open localization, timed
out after 600.85 seconds with zero output (runner logical SHA
`372added51d83ed29e212fb46ffb710c05dad6cfc104abc1c9f3191f608138a3`).
Adding both `T4750` and `U3217` gives the current smallest source-complete
codimension-five necessary core.  Its 707,764-byte canonical characteristic-
zero input likewise timed out after 600.44 seconds with zero output (runner
logical SHA
`7fcf74892e851158f2c8b26317127719fbec1fd4e0eaf78fa3a4fe1ee0235850`).
It is neither an empty-scheme certificate nor a component/counterexample.

Finally, the recurring factors have been compared concretely with the
standard four-qubit invariants of the literal sixteen-entry tensor
`Q_s`: Luque--Thibon `H`, all three 4-by-4 flattening determinants, and
Cayley's degree-24 hyperdeterminant (constructed as the discriminant of the
three-qubit-hyperdeterminant quartic).  On two exact `QQ[b0]` slices after
the identical Cramer and A-open pullback, `B,Q,R,S,T,U` have numerator and
denominator gcd one with every invariant.  `A` and `C8` also have numerator
gcd one, but occur wholly in the pullback denominators: they are elimination
poles, not numerator invariant factors.  Thus none of the recurring factors
is, or divides, these standard covariants.  The exact result SHA is
`19fc3de664cd6d0940de51f206732c5f26446f4299e7cf833966fb785b76dbd1`;
the checker also replays all sixteen literal source `Q_s` and includes a
sign-mutation guard.  Deterministic three-mode replay is pending at this
writing.  It subsequently passed with logical SHA
`e3218827ef9dc02467130d26f6950cfefac1c279584f54acda2998c4f6091213`.

A first modular geometry probe of the codimension-five core is also frozen as
a blocker.  At `p=1073741827`, native F4SAT on one deterministic generic
hyperplane slice timed out after 300.19 seconds with zero output (manifest
SHA `fe7d590adacc3079bde31f98d1f18400b8ef33a1dcd6cb572926a07b4dc9a1ba`).
Losslessly solving that affine equation for `b0` and mapping all nine rows
plus the exact final live product into four variables did not help: the same
slice again timed out after 300.37 seconds with zero output (manifest SHA
`0644b49aff0af4e355dae978f9b7354923e4d344d73c8f6697677ea2f1bfb4c4`).
Neither run supplies UNIT, NONUNIT, dimension, or degree evidence; no second
prime result is claimed.  A two-hyperplane, three-variable quotient has been
exported but not run, with result SHA
`4e6faee90b4513347163bf7e8300645c55b8d3902f9b93dea7434996d4f1a6ab`.

### Corrected Delta interface and D10 structural split

The preceding codimension-five export used an incorrect cleared Delta after
the affine `t_013` elimination.  With
`pivot=2*b0*A*b3+2*B`, the root is `b3=-B/(b0*A)`, so the literal cleared
factor is
`TrueDeltaN=b0*A*b1*d3-B*d1*d4`, not
`A*b1*d3-B*d1*d4`.  The corrected exact exporter includes the literal
source identity and a dropped-`b0` hostile mutation; its result SHA is
`9c0d6d617d4b56327eb2a3a8313dd8ad1fd65c230a889af853499b7ae0ad6e29`.
The earlier exact A-open/C8 unit is unaffected because it retains `b3` and
localizes the literal six-variable Delta directly.

The old three-hyperplane residual has degree 11 at two large primes.  Its
first-prime RUR factors with degrees `1+3+3+4`, and exact arithmetic in every
factor makes the true Delta zero while all formerly declared factors remain
live.  This diagnoses that residual as an artifact of the incorrect
localizer, but is modular evidence rather than a characteristic-zero radical
certificate.  The finite referee result SHA is
`65e57c41c733643f76b5174cbe42d1c7b8fa4cde8b2817dd284142f038cd9a35`.
The corrected unsliced five-variable F4SAT gate timed out at 300.27 seconds
with zero output (manifest file SHA
`05e9837b8e563e14055015d04e477ffea98267c2382af614cfd1add7e456b91f`).

Exactly, `TrueDeltaN=C8*D10`, with `D10` ten terms of degree five and affine
in `b1`: `D10=L6*b1+C4`.  The smallest retained row is `P324`, quadratic in
`b1`, and
`Res_b1(D10,P324)=unit*d1*K4*A*W64`, with factor profiles
`(1,1),(4,4),(19,6),(64,12)`.  Moreover
`K4=b0*(b0+d4)*d3+d1*d4*(b0^2+d4)` is affine in `d3`.
Thus the `L6`-open D10 boundary reduces to four variables and its K4-open
subbranch to three; the companions are `L6=0`, `b0+d4=0`, and the
64-term degree-12 `W64` branch.  The exact structural artifact SHA is
`1a771c1b3c96ddeb517e5661dac9472c37a96d5882840f18d3ae8facc1ec9318`.
This split describes the detected D10 boundary but does not yet prove the
full corrected core is contained in it.
