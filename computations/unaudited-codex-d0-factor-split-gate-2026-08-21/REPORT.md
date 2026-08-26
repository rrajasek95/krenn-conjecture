# Exact D0 residual-factor gates

## Result

On the reduced `D0=0, C0!=0, selected-pivot!=0` chart, the residual case

`A = U2 = Cof(1,3) = Cof(2,3) = Cof(3,3) = 0`

is empty.  The fully expanded characteristic-zero msolve input has six rows
and returned the literal unit basis `[1]:` in 0.181 seconds.  The input SHA is
`e89032d0edcd233f486c0882bb14ec4df0a18e0ad7ca2fd070214384f94f19ca`;
the output SHA is
`2306ef9a8d68d0afec4958b3b208f108d51adca09499a3583401abe25a112c28`.

## Exact involution

The coefficient-ledger audit proves that the Laurent involution

`(b0,d1,d4) -> (-b0^-1,-d1,d4^-1)`

acts by

- `A -> -b0^-3 d4^-2 B`,
- `U2 -> -b0^-13 d4^-9 U1`,
- `pivot -> -b0^-16 d4^-15 pivot`.

It exchanges the cleared literal cofactor restrictions `1 <-> 3` and
`2 <-> 4`, up to live Laurent monomials and signs.  Consequently the chosen
minimal packet `{1,2,3}` maps to the already-frozen minimal packet
`{1,3,4}`.  The single exact gate therefore also closes `B=U1=0` with the
involutive mate packet.

## Replay and scope

`audit_d0_factor_split_gate.py` rebuilds the pivot and the four reduced
factor rows from the exact source ledgers, verifies every Laurent relation,
checks the frozen literal-cofactor export and input/output hashes, and fires
coefficient, unit-output, and packet-label mutations.  `std`, `-O`, and
`-I -S` all return logical digest
`ca262c59b932fc711889e1867d934450e12f13780e36257a15afe3bb4b953d37`.

## Final `A*B`-open case

The sole remaining case in the exact pivot-open decomposition was tested with
the eight-row ideal

`<U0,U1,U2,U3,Cof(1,3),Cof(2,3),Cof(3,3),z*A*B*pivot-1>`.

The expanded live product has 1,088 terms; the strict 197,752-byte input SHA
is `503a30357eff7b3b5f4defeaf34797ace2656df73ede179a7848ff959a17655c`.
The 600-second-capped exact characteristic-zero run returned `[1]:` in 0.353
seconds.  Its source/localizer audit byte-rebuilds the four `U` rows, all
three literal cofactor restrictions, and the full Rabinowitsch product.
Standard, `-O`, and `-I -S` return logical digest
`38327726447992dc10cb13be72be798aa0c7b9d615aa2e017ed34a268a03148f`.

## Theorem ledger and remaining face

Together, the exact factorization of the four Cramer compatibilities and the
two gates close all three residual cases **on the selected-pivot-open chart**:

1. `A=0,U2=0`;
2. `B=0,U1=0` by the exact involution;
3. `A*B!=0,U0=U1=U2=U3=0`.

The earlier exact `C0=0` certificate remains valid.  This still does not close
the whole `D0=0` subtree: the frozen pre-pivot source explicitly excludes
`C0!=0,pivot=0`.  Exact factorization of the 320-term cleared pivot is

`b0*d1^5*d4^3*C0^2 * P1*P2*P3*P4`,

with four nonconstant multiplicity-one residual factors.  Thus the pivot-zero
face cannot be identified with `C0=0` after Laurent localization.  The stable
three-mode theorem-ledger digest is
`cd25ef17331e546dad33d8c85bb024acef66406cd03bebf4c8e73152772eb883`.

## Minimal pivot-zero interface

The next honest branch is now isolated without a Gröbner computation.  Before
dividing by the selected coefficient pivot, the two literal rows `t_013` and
`Cof(0,3)` form a `2 x 3` augmented linear matrix in `(a0,a5)`.  After
removing declared Laurent factors and `C0^2`, their coefficient determinant is

`R0*R1*R2*R3`,

where the four exact multiplicity-one factors have respectively 8, 8, 8, and
12 terms.  On determinant zero, common solvability forces the two exact
coefficient/RHS minors.  After stripping only declared live/C0 factors these
factor as

- 396-term minor: `R0*S256`;
- 555-term minor: `R1*R2*R3*S42`.

The two minors have no common nonlive factor: their exact gcd is
`d1^2*d4^2*C0`.  This gives a small, source-labelled residual face graph for
the pivot-zero branch.  It is a necessary consistency interface, not an
emptiness theorem.  Its `std`/`-O`/`-I -S` logical digest is
`d8ed94a0df577af9720dd3f8404dc2b124665edf83f5909b2cb18bc7cf85862f`.

The exact Laurent involution fixes `R0`, `R3`, `S42`, and `S256`, and swaps
`R1 <-> R2`, always up to the frozen monomial/sign relations.  The seven
inclusion-minimal factor-pair ideals therefore form five symmetry orbits:

- `{R0*R1,R0*R2}`;
- `{R0*R3}`;
- `{R0*S42}`;
- `{R1*S256,R2*S256}`;
- `{R3*S256}`.

For later generic-chart work the artifact separately records the common
source-live product `b0*d1*d4*C0` and the product of complementary `R` factors;
the latter is explicitly optional and is not used in the closed-cover claim.
The five optional products have 80, 24, 64, 113, and 80 terms.  The symmetry
audit is stable in all three modes at logical digest
`eb6fe00736e47088412934230abf26b877a84a1a4829c7336780a3576c483f49`.

### Upstream live-factor correction

Before launching the apparent smallest `{R0,R3}` gate, literal source replay
fired an essential guard: the upper four-cofactor Cramer solve has determinant
proportional to `Delta^2`, and after `D0=0` and the endpoint solve one has the
exact identity

`Delta = d4*R3/(2*b0*C0)`.

Thus `R3` is already live in the ambient `Delta!=0` cycle chart.  The attempted
gate was stopped before msolve; setting `R3=0` returns to the separately
retained `Delta=0` boundary where the solved interface is invalid.  The honest
pivot-zero cover therefore has five pairs in three orbits:

- `{R0*R1,R0*R2}`;
- `{R0*S42}`;
- `{R1*S256,R2*S256}`.

The exact correction is stable in all three modes at digest
`c694d0d8676452be54dc6f529f93a8edd6ac84d9229f4aafde2802ccd5dac9c9`.
For reverse unit work the first orbit is smallest: two 8-term constraints and
an 80-term optional generic live product (96 total terms), versus 114 and 377
for the other two representatives.

## Exact closure of corrected orbit O1

The representative `R0=R1=0` was tested against all ten literal residual rows
after the upper and endpoint solves, but before any selected-pivot division:
the four triangle rows and `Cof(e,3)` for all `e=0,...,5`.  The only
Rabinowitsch product is the guaranteed

`b0*d1*d4*C0*R3`,

where `R3` is equivalent to the already-live `Delta`.  `R2` is explicitly not
localized.  Every cleared source-row denominator factors only over those five
guaranteed live factors.

The 13-row, 173,479-byte strict characteristic-zero input returned the literal
unit basis `[1]:` in 0.038 seconds.  The exact Laurent involution therefore also
closes `R0=R2=0`.  Source rebuilding, denominator sentinels, the no-`R2`
localizer check, and unit mutation pass under standard, `-O`, and `-I -S` with
logical digest
`843442aa0e1f82d6bdc367f03e8de300c01e97bb2fc07cd3a7ef8942dc630479`.
Orbits O2 (`R0*S42`) and O3 (`R1*S256`, with involutive mate) remain open.

## Exact closure of corrected orbit O2

For `R0=S42=0`, the audited O1 input was regenerated and only its second
factor row was replaced by the unique exact 42-term consistency factor.
The ten literal source rows and `b0*d1*d4*C0*R3` localizer are byte-identical;
`R1` and `R2` remain unrestricted.  Exact characteristic-zero msolve returned
`[1]:` in 0.030 seconds.  The single-factor replacement, source denominator
ledger, unchanged-localizer sentinel, and unit mutation replay under all three
modes with digest
`e505d4627acb06602ec3e9fe29a731807e5d01a1d6b3c1bfe1ae3570690953bf`.
Only corrected orbit O3, `{R1*S256,R2*S256}`, remains open.

## Exact closure of corrected orbit O3 and complete D0 theorem

For `R1=S256=0`, the same ten literal rows and guaranteed
`b0*d1*d4*C0*R3` localizer were retained; `R0` and `R2` are unrestricted.
The exact gate returned `[1]:` in 0.219 seconds.  The frozen Laurent involution
fixes `S256` and sends `R1 <-> R2`, so the mate is closed as well.  Source,
factor, localizer, symmetry, and mutation replay pass in all three modes with
logical digest
`ddfaef7abe057df82b59ec69cab3c41563f403ace017d95ef492308db61669a8`.

All three source-admissible pivot-zero orbits are therefore empty.  Combining
them with the pivot-open theorem and the earlier `C0=0` certificate proves:

> Under the declared `Delta!=0` branch-0 four-cycle interior assumptions, the
> complete `D0=0` source scheme is empty over characteristic zero.

The complete three-mode theorem ledger has digest
`2d6ef3e488f2b29f8f25a3d4ab0ab74f501313c5298c0c5e205101969296347e`.
This closes the whole `D0=0` branch, not the whole four-cycle: `D0!=0`
generic residuals and recursive term-boundary faces remain separate.
