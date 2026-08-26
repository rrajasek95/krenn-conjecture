# Sharp mixed-norm hypothesis: exact local verdict

## Outcome

The unrestricted conjectural bound `P_mixed >= 2` on the balanced,
pure-normalized `n=8` slice is false.  It becomes viable again after removing
the active clean-cap branch: every zero or descending two-cell leakage ray at
the balanced Laurent point has a literal support-separated active `K=I` cap,
whereas the first two-cell supports that destroy all such caps have strictly
positive second variation `P2=5`.

## Exact counterfamily

Put `x=r^2>1`, `t^2=x-x^-3`.  Starting from the twelve Laurent anchor cells:

* replace colour-0 edge `25` and colour-2 edge `07` by `r^-3`;
* replace the other three anchors in each of colours 0 and 2 by `r`;
* keep colour 1 unit;
* add `A_02[2,0]=t` and `A_57[0,2]=-t`.

Every port has energy `x` in colours 0 and 2 and energy one in colour 1.
Every pure amplitude is one.  The only nonzero outputs are three pures and
four mixed words, with mixed amplitudes

```text
11111012 = -t
12012000 = r^-1
21000012 = -r*t^2+r^-5
21000111 = r*t
```

Therefore

```text
P(x)=x^3+x^2+x-3x^-1-x^-2-x^-3+4x^-5.
```

It is less than two just to the right of `x=1`.  Its unique global minimum
occurs at the unique positive root above one of

```text
D(x)=3x^8+2x^7+x^6+3x^4+2x^3+3x^2-20,
```

because `D'(x)>0`.  The root lies in `(1073/1000,537/500)` and the minimum is
approximately `1.798070075935623`.  `P` never vanishes for `x>1`, since the
first mixed amplitude is `-t != 0`.

The family is not no-cap.  Six exact `K=I` response supports are stars:
`23/4`, `24/3`, `34/2`, `56/7`, `57/6`, `67/5`.  The scalar is nonzero and
`kappa=(1,1,1)`, so these are active clean caps.

## Unit diagonal theorem

Fixing one perfect matching reduces the unit one-factor slice to `105^2 =
11,025` ordered triples.  The exact minimum is `P=2`, attained 864 times and
forming two `S8 x S3` orbits:

* pair cycle types `(4+4,8,8)`, 288 fixed-factor records;
* pair cycle types `(8,8,8)`, 576 records, containing the Laurent support.

The pairwise-Hamiltonian residue has 960 records: 576 at `P=2`, 384 at `P=3`.
The result is phase-independent because balance and pure normalization make
all one-factor cells unit, and every output word determines its matching.

## Local second variation and cap split

All 36 real diagonal alternating-cycle directions have `P2 >= 2`; all 1,260
signed two-cycle combinations have `P2 >= 4`.

For cross-colour leakage, contracting the twelve anchors gives 72 feasible
two-cell circulation rays.  Their phase-minimized distribution is

```text
-3/2:4, -1:2, -1/2:8, 0:2,
 3/2:4,  3:16, 7/2:24, 9/2:8, 5:4.
```

The sixteen nonpositive rays form five orbits under the order-four Laurent
stabilizer.  Every one has a termwise support-separated active identity cap;
there is no no-cap descending ray.  Of the 56 positive rays, 52 still have a
support-separated cap.  The remaining four form two stabilizer orbits and
already destroy all frozen identity caps; both have phase-independent
`P2=5` (`linear norm=4`, forced normalization contribution `=1`).

This proves a minimal-support local statement only.  It does not yet show a
global lower bound on the full no-cap Kempf--Ness slice or exclude arbitrary
non-identity caps on the two positive support orbits.

## Six-cell no-carrier descent and exact integration

The suggested multi-ray rescue fails already at the next support size.  Let

```text
A = +(25;1,2)/2 +(46;1,2)/2,
D = +(02;2,0)   -(57;0,2),
E = -(04;2,0)/10+(37;0,2)/10.
```

The exact tangent quadratic form on the unscaled ray coordinates is
`diag(5,-3/2,-1/2)`; all three cross terms vanish.  Thus `A+D+E` has
`P2=-51/200`.  The four-cell `A+D` support retains exactly two identity
response triangles (`23|045` and `57|026`), while adding `E` destroys them.

This tangent integrates exactly.  Put `u=s^2`, and take the positive analytic
roots at `rho_c(0)=1` of

```text
rho0^2 (rho0-u) (rho0-u/100) = 1,
rho1^3 (rho1-u/4) = 1,
rho2^2 (rho2-101u/100) (rho2-u/4) = 1.
```

On a diagonal anchor with leakage energy `k*u`, use amplitude
`sqrt(rho_c-k*u)`, and use `s` times the six coefficients above on the leak
cells.  Then every port energy in colour `c` is `rho_c`, every off-diagonal
port Gram entry vanishes structurally, and all three pure amplitudes are one.
The contraction has exactly 17 nonzero outputs (three pure, fourteen mixed),
and

```text
P_mixed(s) = 2 - 51 s^2/200 + 504459 s^4/160000 + O(s^6).
```

This is not merely identity-cap-free.  For every one of the 168 possible
response stars and 560 possible response triangles, a forbidden response row
is a single nonzero source monomial times a diagonal coordinate `K_cc`.
Hence no arbitrary `3 x 3` response carrier can be active anywhere on the
positive branch `s>0`.

Each `rho_c` root exists uniquely for all `s>=0`, so the branch is global.
Outward-rounded interval replay isolates its only critical point at

```text
s^2 in [0.0397589013672, 0.0397589047242],
d^2 P/d(s^2)^2 in [6.52375466, 6.52377158],
P_min in [1.99490005061, 1.99490202117].
```

Moreover `P>4.7975` for `s^2>=5`, and
`P ~ (1894177/2000000) s^8`.  Thus this branch has a unique positive
infimum, but it decisively refutes the proposed local claim that the no-carrier
tangent cone has nonnegative second variation.

## Smallest exact enlargement

At the unique six-cell minimum, the smallest possible support enlargement is
one more balanced two-cell ray.  Thirty-nine such supports preserve the full
port-Gram diagonal structure and therefore integrate by the same exact
diagonal-rescaling construction.  Twelve sign/support classes descend.  A
canonical best representative is

```text
-(05;1,0) + (23;0,1).
```

Writing its squared amplitude as `v`, outward interval evaluation over the
certified six-cell critical interval gives

```text
dP/dv|v=0 in [-1.46012365332,-1.46012361327].
```

Its exact two-parameter normalization equations are

```text
rho0^2 (rho0-u-v) (rho0-u/100) = 1,
rho1^2 (rho1-v) (rho1-u/4) = 1,
rho2^2 (rho2-101u/100) (rho2-u/4) = 1.
```

The added support still has all 728 literal diagonal-`K` blocker rows.  Its
global numerical/interval branch screen pushes the infimum to the boundary
`u=0`, where it becomes (up to symmetry) the earlier two-cell clean-cap
family: `v=x-x^-3` and `P_min=1.798070075935...`.  The boundary normal is
strictly positive near that minimizer (`dP/du=0.1505018...`).  Thus the
no-carrier open approaches an active-cap boundary; it has no interior point
at which a further ordinary Hessian iteration is canonically based.

## Active-cap boundary normal cone

The exact two-cell boundary minimizer has six support-separated identity-star
carriers.  Of the 71 other balanced elementary rays, exactly eight destroy all
six stars at first nonzero order.  Four of those still leave a response
triangle.  The remaining four have, coefficient-independently, a literal
diagonal-`K` blocker row for every one of the 728 star/triangle carriers:

```text
(26;1,0)+(47;1,0),
(26;1,2)+(45;1,2),
(26;2,0)+(37;2,0),
(27;2,1)+(35;2,1).
```

All are port-Gram orthogonal and hence integrate exactly by adding their
squared amplitude to the appropriate diagonal energy entries before solving
the four-factor `rho` equation.  Exact bisection of the old minimum gives

```text
v in [0.2643999720865587,0.2643999720865588].
```

After minimizing the real/Gaussian phase sign, outward interval normal costs
for the four rays are respectively

```text
4.56977505192, 5.64188010340, 3.55263535299, 5.35810840820.
```

Thus every smallest support addition that actually leaves the full carrier
branch has strictly positive first normal cost, at least
`3.55263535298826`.  This is a finite exact normal-cone statement; it does not
yet rule out destructive interference among two or more added rays.

The mandatory interference guard closes this qualification through the
inclusion-minimal three-ray level.  Six-star masks reduce the search to 68
minimal two-ray and 288 minimal three-ray unions; the exact literal
arbitrary-`K` audit leaves 34 pair supports and 73 triple supports.  Across
these supports there are 114 distinct ray pairs.  In every pair, the two
linear output-word sets are disjoint and no word made from one cell of each
ray meets the base output-word set.  Therefore both the Hermitian and
holomorphic cross terms vanish identically: the normal form is diagonal.

An exhaustive 8,704 pair-state plus 299,008 triple-state Gaussian phase replay
then reduces to exact one-ray intervals.  The sharp lower coefficient is

```text
0.4289925585212376
```

on the ray `(13;1,0)+(46;0,1)` with opposite real phases (equivalently equal
imaginary phases).  Thus every inclusion-minimal two- or three-ray support
that destroys all arbitrary-`K` star/triangle carriers has strictly positive
normal cost.  No nonpositive multi-ray survivor remains at these support
levels.

## Global normal cone: non-minimal counterdirection

The inclusion-minimal restriction is essential.  Every one of the six
descending rays may be combined with any one of the four full single-ray
hitters; all 24 unions retain literal blockers for all 728 arbitrary-`K`
carriers.  A canonical exact direction is

```text
-(02;2,0) +(57;0,2) -(26;1,0)/10 -(47;1,0)/10.
```

It is port-Gram orthogonal and, at the exact active-cap minimum, has outward
normal coefficient

```text
[-1.1673273435176432,-1.1673273435175493].
```

Thus global normal-cone positivity is false even for two added rays: the
small full hitter may have arbitrarily small nonzero coefficient while the
descending ray dominates.  This does not contradict the inclusion-minimal
pair/triple theorem above.

This direction integrates exactly.  With `v` fixed at the old two-cell
minimum and `w` its squared amplitude, the normalization equations are

```text
rho0^2 (rho0-v-w) (rho0-w/100) = 1,
rho1^2 (rho1-v)   (rho1-w/100) = 1,
rho2^3 (rho2-w) = 1.
```

The source has exactly 17 nonzero outputs (three pure and fourteen mixed),
listed literally by `integrate_global_normal_counterfamily.py`; all 728
blocker rows persist for every `w>0`.  The first critical point is certified
by

```text
dP/dw(0.17247) < 0 < dP/dw(0.17249),
P(86239/500000) in
[1.695752682056310,1.6957526820563373].
```

An outward 10,026-box derivative screen finds no uncertainty outside the
single critical window near `w=0.172478` on `10^-8 <= w <= 5`.  This statement
is only for the fixed-`v` slice and is not the constrained minimum of the
two-parameter support.

## Corrected 18-cell constrained minimum

Allowing both old squared amplitude `v` and new squared amplitude `w` to
vary gives the constrained critical point

```text
v = 0.2052415678447232...,
w = 0.1929534886934304...,
P = 1.6852918479402192....
```

On the rational enclosure `v in [0.20523,0.20526]`,
`w in [0.19294,0.19297]`, the exact outward interval Hessian is

```text
Hvv in [6.75641246,6.76353119],
Hvw in [2.30906614,2.31159809],
Hww in [6.85375214,6.86166373],
det(H) in [40.9632907,41.0772902].
```

Thus the critical point is a strict constrained local minimum.  There are 38
balanced elementary two-cell rays outside its 18-cell source support which
are port-Gram orthogonal to it; 33 retain literal blockers for all 728
arbitrary-`K` carriers.  Every one-ray normal is positive, the smallest being

```text
[0.2381545690820857,0.2389344402264733]
```

on `-(12;1,0)+(56;0,1)`.  This singleton screen is not a terminal active-set
certificate because cross-ray interference is nonzero.

## Mandatory non-minimal guard at the 18-cell minimum

The first exact pair screen already supplies a counterdirection.  Put

```text
L = (04;1,2) + (13;2,1),
R = (15;2,0) - (24;0,2).
```

Their exact interval normal block on the critical enclosure is

```text
[[3.4295778877..3.4301382299,  -1.4119462789..-1.4106451613],
 [same,                           .2579345030...2587087861]],
det in [-1.1089858263,-1.1025128737].
```

The union remains port-Gram orthogonal and has literal blockers for all 168
stars and 560 triangles.  The rational combination `L+5R` has exact normal
coefficient

```text
[-4.2355306735,-4.2145853895].
```

Consequently the finite active-set descent does not terminate at 18 cells:
the next source-faithful branch has 22 support cells.  This is a strict
non-minimal effect; testing the elementary rays one at a time misses it.

## 22-cell hostile optimization guard

Allowing the old squared amplitudes `v,w` and the two new ray amplitudes
`x,y` to optimize independently gives the exact algebraic normalization
profiles

```text
colour 0 energies: 0, v+w+y, 0, w/100,
colour 1 energies: v+x, 0, w/100, 0,
colour 2 energies: w, x+y, 0, 0,
product_k (rho_c-energy_{c,k}) = 1  (c=0,1,2).
```

The resulting support has 22 cells and exactly 26 output words (three pure,
23 mixed).  Its joint critical point is

```text
(v,w,x,y) =
(0.2223557019950540, 0.1069204609594815,
 0.0291884845587185, 0.1712456987787089),
P = 1.6585248355223345.
```

A Krawczyk image lies strictly inside the radius-`2e-7` box about this point.
The outward interval leading Hessian minors are

```text
[5.6529256,5.6531007], [36.9308227,36.9346792],
[2170.2068,2170.8790], [3450.3377,3459.6819].
```

Thus the box contains a unique strict interior critical point.  All 168 star
and 560 triangle blockers remain literal on the positive-amplitude open.
This family is **not** an exact GHZ source and is retained only as a hostile
optimization/support guard; exact GHZ points are automatically no-cap by the
six-site theorem.

## Exact block-normal tensor-activity clause

At a norm-minimal exact-fibre point, the single-edge specialization of
`A_E perp ker(L_E)` gives the exact implication

```text
X_e[a,b] != 0  =>  OR_{z in {0,1,2}^6} C_e[z] != 0,
```

where `C_e[z]` is the residual six-site Hafnian column.  Globally these are
252 source-cell implications, deduplicating to 28 edge/cofactor OR clauses
over `28*729=20,412` labelled residual columns.  The full-star adjoint
equation adds no stronger unconditional support clause because its output
multiplier is unrestricted.

The 22-cell family is a bounded counterguard to a support-only use of this
theorem.  Its 22 live-cell implications deduplicate to 19 live edges.  Every
one of the 19 residual cofactors has 4--10 supported columns and an actually
nonzero value on the certified family; each has 2--7 singleton columns.
Nevertheless every one of the 728 carrier blockers remains literal, and the
support has neither the 12-entry support6 nor 18-entry support8 count.
Therefore tensor activity plus the Boolean projection of no-cap does not
force a cap or a known low-support signature.  Any stronger use of the block
normal theorem must couple the actual cofactor coefficients to the
simultaneous mixed GHZ cancellation equations.
