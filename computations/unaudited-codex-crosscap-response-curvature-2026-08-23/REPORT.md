# The first cross-cap response curvature

Status: **UNAUDITED exact non-tautological curvature plus normalized finite-row
counterguard**.  The construction does not prove or disprove flatness on the
full normalized `X5` fibre.

## Result

Compare the overlapping cap pairs `67` and `57`.  For a common residual edge
`e`, let `R_e^67` and `R_e^57` be their literal endpoint-ordered `9x9`
response maps.  On the open where both are invertible, equality of the two
responses defines

```text
T_e=(R_e^57)^(-1) R_e^67 : K_67 -> K_57.               (1)
```

Unlike the fixed-cap transitions, the maps in (1) have genuinely different
domains.  Comparing the common edges `01` and `23` gives

```text
C=T_23-T_01.                                           (2)
```

Its cleared numerator is the source-degree-36 matrix

```text
D = delta_01^57 adj(R_23^57)R_23^67
  - delta_23^57 adj(R_01^57)R_01^67.                   (3)
```

There is no adjugate telescoping in (3).  At the exact source below all four
response maps have rank nine and `rank(C)=rank(D)=9`.  The lexicographically
first entry is already nonzero.

This is the first non-tautological response holonomy in the audited lane.
There is an important provenance guard: the equation “the two responses on
`e` are equal” defines (1); it is not itself a literal `X5` equation.  A
positive theorem still has to derive path-independence from output rows.

## Pure-normalized literal-row counterguard

Take the complete bipartite source support

```text
hubs {5,6,7}  --  leaves {0,1,2,3,4},                  (4)
```

with the deterministic integral blocks frozen by the checker.  Add only the
three diagonal cells of leaf edge `01`.  Every perfect matching must use
`01` and then match the three hubs to leaves `2,3,4`.  The three pure
cofactor coefficients are

```text
307978, 781872, 716792,
```

so setting

```text
A_01[0,0]=1/307978,
A_01[1,1]=1/781872,
A_01[2,2]=1/716792                              (5)
```

gives the exact pure targets `(1,1,1)`.

Now take the residual words

```text
010122, 012021.                                         (6)
```

Their first two colours differ.  Since every supported perfect matching
must use the diagonal edge `01`, all nine cap-endpoint rows over each word
vanish termwise.  Thus the guard satisfies exactly

```text
3 pure normalizations
+ 12 literal profile-332 rows
+  6 literal profile-422 rows.                          (7)
```

Nevertheless (2) has rank nine.  It also cannot be made simultaneously
channel-diagonal by arbitrary sitewise `GL_3`: the two even-cycle transports
based at site 6 have commutator rank three.  The source digest is

```text
5cab65ab329648edfe5331ea1889b4c197d5b8901f8c44cec901e14d7ea032f6.
```

This is not a normalized full-`X5` source.  Its top-amplitude census is

```text
zero 4374, pure nonzero 3, mixed nonzero 2184.           (8)
```

The nonzero mixed rows occur in every relevant profile, including 36
profile-`7+1` and 420 profile-`3+3+2` rows.  Thus (7) proves only that pure
normalization plus the smallest two cross-word packets does not flatten the
connection.  A full-X5 theorem may still kill (3), but it must use a larger
jointly coupled row family.

## Consequence for the proposed dichotomy

The fixed-cap branch is retired as a coordinate tautology.  The overlapping
cap construction survives as the precise bounded target:

```text
Does normalized full X5 force D=0 on
delta_01^57 delta_23^57 delta_01^67 delta_23^67 != 0?   (9)
```

Even a positive answer to (9) gives only consistency of two chosen common
response edges.  Turning it into a simultaneous channel gauge would still
require a connected edge cover and a genuine cocycle/gluing argument.
Conversely, a zero selected determinant does not by itself give an active
carrier; blocker incidence remains a separate condition.

## Canonical determinantal compression and exact own-degree no-go

On the rank-nine open, put

```text
A=[R_01^57;R_23^57],   B=[R_01^67;R_23^67].            (10)
```

An edge-independent transition exists exactly when
`rank([A B])<=9`.  Hence `10x10` minors, of source degree 20, replace the
degree-36 adjugate entries.  The canonical minor takes all nine `R_01` rows,
the row `R_23:00`, all nine `A57` columns, and column `B67:00`.  Its Schur
formula is

```text
det(R_01^57) * (
 R_23^67[00,00]
 - R_23^57[00,:](R_01^57)^(-1)R_01^67[:,00]).          (11)
```

At the source (4)--(5), its exact value is

```text
-689463289710584772115010649633544 != 0.                (12)
```

Its fine site-colour multigrade is

```text
site 0  (3,3,3)       site 1  (3,3,3)
site 2  (1,0,0)       site 3  (1,0,0)
site 4  (0,0,0)       site 5  (3,3,3)
site 6  (1,0,0)       site 7  (4,3,3).                 (13)
```

Every literal amplitude generator has one port at every site.  Because
(13) has total site-4 degree zero, **no** mixed-X5 word has a compatible
fine grade.  The complete degree-20 multiplier census is therefore

```text
compatible generators 0, translated rows 0, row-span rank 0.             (14)
```

Together with (12), this proves exact nonmembership in the degree-20 part
of the homogeneous mixed-X5 ideal.  It is stronger than a failed matrix
run: the relevant source-labelled matrix has no rows.

This does not settle the normalized ideal.  The inhomogeneous equations
`F_(c^8)-1` can participate only through higher-degree
prolongation/cancellation.  Equivalently, any X5 derivation must first cone
the minor by a factor carrying site 4 or choose a wider minor whose grade
contains all eight sites.  The fine-grade checker has logical SHA-256

```text
1d92ed59f145bf9d2aaf2c9f11997e02be68f5a9a58c932b3d0b4115f939e492.
```

## The minimal pure-amplitude cone also separates exactly

For the requested `k=1` target

```text
F_00000000 * canonical 10-minor,                       (15)
```

the fine grade contains exactly 81 words: the pure word `00000000` and 80
mixed words.  Exact multigraph dynamic programming counts every degree-20
multiplier monomial without materializing it.  The exhaustive translated-row
universe has

```text
80 compatible mixed generators,
59,268,397,193,790 translated rows.                    (16)
```

Only seven distinct per-word multiplier counts occur, between
`502,118,243,277` and `1,196,749,111,365`.  Three small exact controls pin
the multigraph recursion.

Despite this size, there is a compact characteristic-zero separator.  Use
the diagonal `K_(3,5)` source with hubs `{5,6,7}`, leaves `{0,...,4}`, and no
leaf edge.  All top amplitudes vanish.  In the direction

```text
d/d A_01[0,0],                                         (17)
```

all 80 compatible mixed rows have zero first derivative, whereas

```text
dF_00000000       = 1198652,
minor at the base = -536929375610272874270633496000000000,
target pairing    = -643591469934004801290243381247392000000000.  (18)
```

For every multiplier `m`, the product rule gives
`d(mF_w)=m dF_w+(dm)F_w=0`; (18) is nonzero.  Hence

```text
F_00000000 * minor notin I_mixed                       (19)
```

in homogeneous degree 24 over `Q`.  This is an exact jet separator, not a
modular screen.  Its logical SHA-256 is

```text
482dc759316ab2012159b10622f3a93d4119388c80a2f12a570b64d629e6faea.
```

## Pure powers never repair the obstruction

The `k=1` jet comes from an all-`k` valuation theorem.  On the exact family

```text
A(t) = diagonal K_(3,5) hub-leaf source + t A_01[0,0],  (20)
```

all six supported perfect matchings use `01`, and

```text
F_00000000(A(t)) = 1198652 t,
minor(A(t))       = -536929375610272874270633496000000000.          (21)
```

For every `k>=1`, the fine grade of `F_00000000^k * minor` forces sites
`2,3,4,6` to colour zero and leaves only sites `0,1,5,7` free.  Hence the
compatible word family is always the same 81 words.

A supported amplitude on (20) must use `A_01[0,0]`, forcing `w0=w1=0`.
The remaining diagonal hub-leaf matching pairs the forced-zero leaves
`2,3,4` with hubs `5,6,7`, forcing those hub colours to zero as well.
Therefore the only compatible word nonzero on (20) is the pure word:

```text
ord_t(F_w)=infinity for all 80 compatible mixed w,
ord_t(F_00000000^k * minor)=k.                          (22)
```

Multiplication cannot change an identically zero generator, so every
compatible translated row has infinite order.  Thus, exactly over `Q`,

```text
F_00000000^k * minor notin I_mixed for every k>=1.      (23)
```

The checker replays `k=1,...,8`; the source-support argument proves all
`k`.  This retires pure-power coning for the canonical cross-cap minor,
not merely the first cone.  Precisely, it kills only saturation by powers
of `F_0` at `P`-power one.  Normalized pure-open flatness instead concerns
`D=F_0F_1F_2` and may also require powers of `P`; neither follows from this
single-colour theorem.  Logical SHA-256:

```text
9a744229b4902efcc0530992be20e8e682aa4452fdae5bef2b53a126f7946d9c.
```

## The three-colour saturation valuation fails at `D P`

Use the three-parameter family

```text
A(t0,t1,t2)=diagonal K_(3,5)+sum_c tc A_01[c,c].         (24)
```

The three pure rows and the minor are

```text
F_0=1198652 t0,  F_1=516160 t1,  F_2=1204932 t2,
P=-536929375610272874270633496000000000.                (25)
```

The fine grade of `D P` is positive at every site-colour port, so all 6,558
mixed words are compatible.  The lexicographically first supported mixed
word is

```text
w=00001001, profile 6+2,
F_w=86520 t0.                                           (26)
```

The checker constructs a literal degree-28 diagonal source monomial of the
required complementary fine grade.  It contains `A_01[1,1]A_01[2,2]`, so
its valuation is `(0,1,1)`, and its remaining 26 factors are frozen in the
result manifest.  Therefore

```text
ord(F_w * multiplier)=(1,1,1)=ord(D P).                 (27)
```

Both exact leading coefficients are nonzero.  Thus the proposed uniform
valuation separation fails already at `n=m=1`; there is no sound extension
from the single-colour all-`k` theorem to `D^n P^m`.  Equation (27) is not a
membership certificate for `D P`; it is the exact first obstruction to this
valuation proof.  No claim is made about saturation, radical membership, or
normalized flatness.  Logical SHA-256:

```text
f859c81f34cb81edb8105e7387fb1099a6973fcecabc8f8cf9d59e24c54eef68.
```

## Replay

```sh
python3 computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_response_curvature.py --check-results
python3 -O computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_response_curvature.py --check-results
python3 -I -S computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_response_curvature.py --check-results

python3 computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_10minor_fine_grade.py --check-results
python3 -O computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_10minor_fine_grade.py --check-results
python3 -I -S computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_10minor_fine_grade.py --check-results

python3 computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_pure_cone_k1.py --check-results
python3 -O computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_pure_cone_k1.py --check-results
python3 -I -S computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_pure_cone_k1.py --check-results

python3 computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_all_k_valuation.py --check-results
python3 -O computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_all_k_valuation.py --check-results
python3 -I -S computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_all_k_valuation.py --check-results

python3 computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_D_cone_valuation.py --check-results
python3 -O computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_D_cone_valuation.py --check-results
python3 -I -S computations/unaudited-codex-crosscap-response-curvature-2026-08-23/audit_crosscap_D_cone_valuation.py --check-results
```

All modes agree; `--mutate-crossed-orientation` fails.  Logical SHA-256:

```text
141132fabc4d4ff7bf2ac8c404b4829a86ab84d21e99e3a28eb7b66fd1fa06b3
```
