# Normalized orbit-0 algebra: exact packet audit

Status: unaudited discovery artifacts, all exact claims replayed under standard
Python, `python -O`, and `python -I -S` on 2026-08-20.

## Proved local facts

- The 78 pair-constant mixed rows do not suffice.  There is an exact rational
  normalized common zero with all three pure Hafnians nonzero, and its
  evaluation functional is an exact dual to the 868-row/5,400-column first
  Macaulay layer.
- Exactly six of the 27 mixed word orbits detect that rational point.  The
  smallest is `01010101` (orbit size 48).
- On the cloned six-block ansatz, `00001122`, `01010101`, and `01101001`
  specialize to
  `E=1+ad+bc`, `G1=9(ad)^2`, and `G2=(ad+2bc)^2`, with exact unit identity
  `1=(ad+3)G1/36-(ad-1)G2/4-(ad-1)E(ad+2-E)`.
- For six arbitrary oriented 2x2 blocks `M_ij`, with the four selected anchors
  normalized to one, define `e_ij=1+perm(M_ij)`, the four three-supervertex
  Hafnians `t_ijk`, and `Q_s` as the Hafnian on one selected endpoint of each
  superpair.  The exact 24-variable identity is

  ```text
  Z = sum_{ijk} t_ijk
      + sum_{s modulo complement} Q_s(M) Q_sbar(M)
      - (e_01 e_23 + e_02 e_13 + e_03 e_12).
  ```

  It recovers the cloned three-row polynomials and includes literal provenance
  for every mixed-edge residual tail.
- No lower bound of two or three active self-complement pairs is valid.  An
  exact F3 point has only `Q_6,Q_9` nonzero and pure `H=1`.  For all 128 ways
  to impose one zero factor in each other complement pair, the 17x24 Jacobian
  has rank 17.  Multivariate Hensel therefore gives a characteristic-zero
  branch with exactly one active self pair.
- The next orbit `00000101` excludes that branch on the same-colour diagonal
  locus.  Its row is exactly
  `x^d_uv * partial(H_c)/partial(x^c_uv)`.  Sixteen of the 24 nonanchor
  cofactors are units at the F3 point.  Their eight-cell complement leaves
  only one entry in blocks 02, 03, 12, and 13, so any second colour has
  permanent zero there, contradicting its pair-constant equation
  `perm(M_ij)=-1`.
- The proposed one-colour lower bound `|supp Q| >= 8` is false in
  characteristic zero.  Over `Q[z]/(z^2+2z-1)`, put

  ```text
  M_e = [[0,b_e],[-1/b_e,0]],
  b = (z,-z-2,1,-z-2,1,1).
  ```

  All 22 branch-51 base rows vanish, the literal raw pure Hafnian is `H=4`,
  and the exact support is `{3,5,6,9,10,12}`.  Thus two apparent
  seven-support deletion ideals actually contain the same support-six point.
  This was found by an exact-Q saturation after deriving the localized chart
  directly from the raw 24-variable polynomials, then replayed independently
  without Singular.
- Support-only compatibility is not enough even on that component.  Its B4
  support orbit has 8 masks and 32/64 ordered pairs pass
  `A intersect bar(B)=empty`.  The complete `(entry,cofactor,Q)` orbit has 24
  records and 288 Q-compatible ordered pairs; all 288 fail both entry/cofactor
  directions, so 0/576 pairs pass the complete diagonal `78+48+144` packet.
  Conceptually, its Q support is the weight-two layer of `F_2^4`.
  Q compatibility requires an odd relative endpoint flip, but an odd `1|3`
  cut crosses exactly one edge of every four-vertex perfect matching.  Hence a
  two-edge cofactor matching necessarily agrees with the other graph's
  all-edge entry orientation in one block.
- The entire branch-51 `d=0` chart has an exact compact normal form.  Gauge
  `b2=b4=b5=1`; then
  `b0=-r-2`, `b1=b3=r`, `r^2+2r-1=0`.  Only two independent linear
  equations remain among the six `a_e`, and the map obtained by adjoining
  `(Q1,Q2,Q4,Q8)` is invertible.  Hence the base quotient is affine
  four-space in `y=(Q1,Q2,Q4,Q8)`, while `Q0` is an explicitly replayed
  quadratic form in `y` (all ten coefficients are in the result JSON).
  Consequently the low-support strata are: the support-six origin; four
  one-`y` support-eight axes (their diagonal `Q0` coefficients are nonzero);
  and two-`y` support-eight points on `Q0=0`.
- The four one-`y` axes form one 64-mask B4 support orbit, with a unique
  Q-compatible forced mate for each support.  Every nonzero entry and
  cofactor on an axis is a Laurent monomial in its nonzero axis parameter, so
  there are no hidden special-parameter support drops.  The complete orbit
  has 192 `(entry,cofactor,Q)` records and 576 ordered Q-compatible pairs;
  every pair fails both cofactor directions.  Thus the full diagonal packet
  excludes the entire one-`y` class, not just a sample.
  There is also a compact raw-polynomial unit behind this obstruction.  After
  the eight cofactor-forced mate cells
  `{3,7,9,10,13,14,19,23}` are set to zero,

  ```text
  2 = x15*x16*x21*e01 + x15*x17*x20*e02 + e12+e13+e23 - t123
      - x6*x15*x20*Q3 - x2*x15*x16*Q5.
  ```

  The unique forced mate has `Q3=Q5=0`, so its own base rows make the right
  side zero.  Restoring any of cells `3,7,13,14,19,23` makes the literal
  residual fire; cells `9,10` are forced but redundant for this identity.
- For the remaining two-`y`/`Q0=0` class, the six possible support masks all
  lie in a single 96-mask B4 orbit and that orbit has 0/9,216 ordered
  Q-compatible pairs.  Since `support size = 6 + number(nonzero y) +
  indicator(Q0 != 0)`, these three cases exhaust every `|supp Q| <= 8` point.
  Therefore no two colours from the branch-51 `d=0` low-support locus can
  satisfy the complete diagonal packet: support-six and one-`y` fail the
  entry/cofactor rows, while two-`y` fails already at the Q rows.
- A different exact four-parameter characteristic-zero family has
  `|supp Q|=8`, support `{1,3,4,5,6,9,10,12}`, and `H=4`.  Its B4 support
  orbit has size 96 (stabilizer 4) and 0/9,216 ordered Q-compatible pairs.
  The eight one-coordinate-deletion controls all admit compatible pairs, so
  the orbit obstruction is not a complement-convention artifact.
- Joint branch/support quotienting must use the stabilizer of the fixed
  cofactor branch, not full B4 independently.  The exact joint census is
  2,289 seven-support representatives and 2,606 eight-support representatives
  (branch stabilizers 48,48,8).  A p1009 broad Groebner screen was stopped
  after 120 cases because 98 hit the two-second timeout; its partial UNIT
  count has no classificatory meaning.
- The seven NONUNIT aligned-zero joint charts have now been structurally
  resolved at the low-support boundary.  Charts `(1,38)` and `(1,12)` have
  exact three-dimensional normal forms over
  `Q(r), r^2+2r-1=0`; their literal `(entry,cofactor,Q)` records are in the
  already frozen support-six orbit.  Chart `(0,30)` is pure-dead: its
  literal pure Hafnian reduces to zero in the exact saturated 15-row ideal.
  On chart `(11,21)`, four rows give a much smaller normal form.  With
  `x=a3*b0/a1`, `y=b0*b4/b2`, two cofactors first force `b5=0`, while
  `t012` and `cofactor_5_0` give

  ```text
  fx = 1-2*x-x^2 = 0,       g = x*y+x+y-1 = 0.
  (x+1)(x-y)+g = -fx,       (x+1)^2 = 2-fx.
  ```

  Hence `x=y`, and direct substitution in the raw pure polynomial gives
  `H=4`.  Its exact minimal-Q component has support
  `{1,4,7,8,11,14}` and again lies in the same frozen support-six joint
  orbit.  These are aligned boundary-chart statements, not full open-chart
  closures.
- The first non-aligned branch-zero obstruction is also exact.  For the
  both-diagonal-term support triangle `{01,02,12}`, the anchor-preserving
  torus `diag(t_i,t_i^-1)` sets `b03=b13=b23=1`; its remaining common
  parameter sets `d01=1` over the algebraic closure.  Three literal
  cofactor rows then give

  ```text
  R12-R20+b0*R16 = -2*b0*(d0+d1+d3),
  R16 = (b1-1)*d0 + (b0-1)*d1,
  ```

  so `d3=-1-d1` and `b1=1+d1-b0*d1`.  After these lossless substitutions,
  the 13 distinct raw source rows plus the `b` and `a*d` liveness
  localizers form the unit ideal over Q (and p1009,p1013).  No pure-Hafnian
  localizer is used: this triangle defect stratum is empty outright.  An
  exact Groebner unit is frozen, but a source-multiplier lift is not.
- For the next defect orbit, the triangle-plus-pendant support
  `{03,12,13,23}` (edge indices `{2,3,4,5}`), an exact localized reduction
  is frozen and its two Cramer branches are now exact-closed over
  characteristic zero.  The
  same torus losslessly gives `b2=b4=b5=d2=1`.  Literal rows `R20` and
  `R14` solve `a0` and `a3`; after these substitutions,

  ```text
  R6red+R18red = -2*b3*d5*(d3+b1*d4+b0*d5).
  ```

  Thus `E=d3+b1*d4+b0*d5=0`.  Then `R16+a2*E` solves `a2`, reduced `R6`
  solves `a1`, and reduced `R18=-2*b3*d5*E` is redundant.  Every division
  is by a factor already localized on this both-term stratum.  The resulting
  system has eight geometric variables and twelve distinct residual rows.
  With no `H` localizer and no `c`-entry localizer it is UNIT modulo both
  1009 and 1013; standard, `-O`, and `-I -S` replays agree.  This is only
  modular discovery: direct Q runs timed out at 240--300 seconds, so no
  rational emptiness claim is made.  In particular nothing here is
  transported to the separate k4-cycle orbit.
- The triangle-plus-pendant residual now has a sharper exact Cramer split.
  After the proved relation `E=0`, rescale `x=d4*a4`, `y=d4*d5*a5` and use
  source rows 7 and 12.  Their determinant and both Cramer numerators share
  the live factor `d4*(b0*d5+b1*d4)=-d4*d3`; after cancelling it, the genuine
  open-chart divisor `P26` has 26 terms, while the `x,y` numerators have 18
  and 46 terms.  Nine transported source rows remain.  Modulo both 1009 and
  1013 their ideal has basis size 142 and dimension 3, and the 46-term `y`
  numerator `N5` has least nilpotence exponent three: the first two reduced
  powers have `(terms,degree)=(46,8),(891,16)`, while `N5^3` reduces to zero.
  A tracked p1009 lift has 776,737 multiplier terms and maximum product degree
  36.  This historically isolated the exact-Q target
  `N5^3 in <nine transported rows>` on `P26 != 0`; direct Q Singular and
  homogeneous probes timed out.  The bounded coefficient-first exact-Q gate
  recorded below now supersedes that failed route.  Standard, `-O`, and
  `-I -S` replays give digest
  `89841cbc366dd55d798fc3c7904eb28bae899538c2cafebbc4efb401d5c0331c`.
  The deterministic exact bounded-Macaulay exporter gives, at the first
  possible cutoff 24, 118,755 monomial rows and 83,264 labelled multiplier
  columns.  Its row-exponent digest is
  `32e04be0fda62392330ac7ac06706166184cc457f5df9bad6105dc0b5aef405c`;
  the locally emitted integer-column JSONL has SHA
  `a41af44182768c7c6273c106aaac2c1309efdac1732d54706cd1611a3119b02e`.
  This is an interface checksum, not a membership result.
- The complementary `P26=0` branch was reduced through the following exact
  boundary system before its characteristic-zero closure.  The system is
  the eleven `E=0` source rows plus `P26`; native F4SAT initially showed that
  their full 109-term live product is a unit at two large primes.  Factor
  profiling sharpens the required localization to

  ```text
  F0 = b0*b1*b3*d4*d5*(b1*d4+b0*d5).
  ```

  The transported `a2,a3,a4,a5` factors are not needed.  A mandatory negative
  control localizing only `D=b1*d4+b0*d5` is NONUNIT (25 leading monomials at
  `p=1073741827`); this invalidates a tempting `D` identity that appeared only
  because msolve 0.10.1 had silently misparsed a parenthesized Rabinowitsch
  row.  Every frozen input now expands `z*F-1` termwise and passes the common
  strict parser.
- Greedy two-prime deletion leaves the exact eight-row core
  `(7,8,9,10,12,15,19,101)`.  It is F4SAT-UNIT at `p=1073741827` and
  `p=1073741789`; the guarded toolkit manifests have SHAs
  `72a2bb2ec81e3e3f9c958350eec69c2117e30a05af15592ccc2a482095a6501b`
  and
  `aecae8d60c562910759d1a5cf3498fb84faa282277fa44f357ae90d8bf87657d`.
  The `P26=0` branch is now closed over characteristic zero by a corrected,
  coefficient-first re-export of precisely these eight rows plus the expanded
  Rabinowitsch equation `z*F0-1`.  Guarded msolve returns the literal empty
  sentinel `[-1]:` in 4.55 seconds; independent standard, `-O`, and `-I-S`
  replays check every source monomial/coefficient, the exact `F0` product,
  and sentinel/mutation controls.  The canonical input SHA is
  `62540e25e6dd53a668e48bef2af2f0fe4dcbcd0008138b1f210ae1af9d2523f6`
  and the manifest logical SHA is
  `62019cf3279c50d713b276bd28bcf0abbcb4b6658f342dfae1f8a8316602a2aa`;
  see `../unaudited-codex-tp-p26-boundary-char0-2026-08-21/REPORT.md`.
  This exact closure is restricted to `P26=0` on `F0 != 0`; the complementary
  `P26!=0` lane is closed separately below.  Earlier direct exact-Q Singular runs on
  both the twelve-row and eight-row systems timed out at 300 seconds, and a
  homogeneous modular-reconstruction attempt spawned stale workers and was
  terminated without output or claim.
- The complementary `P26!=0` fully-live Cramer interior is now exact-closed
  without the stalled degree-24 lift.  The coefficient-first input consists
  of the nine transported rows `(8,9,10,11,13,15,17,19,21)` and

  ```text
  z*F0*A3hat*P26*N4*N5*A2hat-1.
  ```

  The expanded coefficient has 8,506 terms and degree 40.  Exact-Q msolve
  returns literal `[-1]:` in 14.286 seconds.  Independent standard, `-O`,
  and `-I-S` source replays verify every transported coefficient, all six
  live factors, input/output bytes, and the sentinel.  Canonical input SHA:
  `6c8d379f399465c73e475c09314bee3a315f8f89ca40e941fcff845f561fbd73`;
  manifest logical SHA:
  `2ca019ebd396746cd525d4eca2ac5a4cc4afbd59e27d55ad43d698ca3fa35466`;
  see `../unaudited-codex-tp-p26-interior-char0-2026-08-21/REPORT.md`.
  Together with the stronger `P26=0,F0!=0` gate, this closes the declared
  triangle-plus-pendant stratum.  The `P26!=0` divisors `A3hat=0`, `N4=0`,
  `N5=0`, or `A2hat=0` violate frozen live/support antecedents and are not
  unresolved subcharts of that stratum.
- A bounded, exact-input homogeneous Macaulay ladder was therefore run only
  through the declared cap 14.  The target is `t^d` after separately
  homogenizing the eight core rows and the expanded `z*F0-1`.  At both 1009
  and 1013 the dimensions `(ambient rows, columns, rank)` are

  ```text
  d= 9: ( 24310,   409,   409)
  d=10: ( 43758,  1419,  1419)
  d=11: ( 75582,  4137,  4137)
  d=12: (125970, 10593, 10593)
  d=13: (203490, 24519, 24514)
  d=14: (319770, 52338, 52275).
  ```

  The target is outside at every degree and prime; the first source
  dependencies appear at degree 13 (five), growing to 63 at degree 14.  An
  independent streaming checker replays each displayed left dual against
  every exact integer column and pairs it nontrivially with `t^d`.  The
  target-zero mutation fires, and standard, `-O`, and `-I -S` modes agree.
  Audit SHA is
  `4f177a9fcdea72bf2491973ece2aae7a5525c12af65ace475028ffc6af2112c7`;
  three-mode manifest SHA is
  `3f58bf12423266373df6d921e6b471ea922d5273d1eba8678a79adf5eabe7869`.
  Thus no certificate exists in this direct homogeneous span through degree
  14; this is a bounded modular obstruction, not a Q nonmembership theorem.

## Missing global lemma

Literal `4+4` breaker rows polarize across colours:
`Q_s(M^c) Q_sbar(M^d)`, whereas the pure identity needs the self term
`Q_s(M^c) Q_sbar(M^c)`.  More importantly, outside the same-colour diagonal
locus every `e`, `t`, `4+4`, and `6+2` row has cross-colour residual tails.
A global proof must control those tails or prove a source-faithful reduction
to the diagonal packet.  None of the identities here proves closure of the
full normalized chart.

## Primary artifacts

- `audit_polarized_superpair_core_identity.py`, result SHA
  `145ab8d797d4a149860b37d45ec43a439aa11da69d2ea245b0e6e97fdb030f16`.
- `audit_one_active_hensel_cofactor_breaker.py`, result SHA
  `3f86523a08fddadd1b234948dfdbff9dc7216e149d041f2b30fca9beaf6abc9d`.
- `search_one_colour_self_support.py`, bounded finite-field discovery SHA
  `1eee72caf700e94bce8b27cc30655e4c7a86ce606b0f3a75a80cfe0bf3f8ff72`.
- `audit_weight0_lowq_char0_parametrization.py`, result SHA
  `9aeb739fe3f66c402e5446766d9e70971ec7adbe71e9d901f55d49fee1677c7b`.
- `audit_lowq_support_b4_orbit.py`, result SHA
  `09ac675af05da7067abeae2f5682db0800afdfe51ef66ec16af4256d4011c0cc`.
- `audit_weight0_support6_char0_component.py`, result SHA
  `90dd5f8465937925931b3e80829102e419e57d27b5e0d8c30bd116c628a01fa0`.
- `screen_lowq_joint_branch_orbits.py`, three-mode census SHA
  `75e937f1d5c653e80a91e75682e7862be229cc44db9aae18216f2d0b4f2ad68b`.
- `audit_weight0_dzero_normal_form.py`, result SHA
  `bd1d5367a978e964e15cab3dcdd53de0b1baf49d73018332af8c61477c2a0394`.
- `audit_one_y_forced_mate_unit.py`, result SHA
  `6eb1c73208eca0672e67df89b6c0f2535698924b44db80b0c31e1c550ed49250`.
- `audit_pairconstant_plus_breaker_block_ansatz.py`, result SHA
  `6e56b931...` (full digest in its JSON).
- `audit_aligned_survivor_0_30_pure_dead.py`, result SHA
  `6d25ac5758ddc346205d6930580d67faee562c22dfb6edc6960cdd78793b45c2`.
- `audit_aligned_survivor_1_12_normal_form.py`, result SHA
  `d849b4815a3adc18f50bc6c7b76254b811afdc9da671052d844f5a13afa3ba93`.
- `audit_aligned_survivor_1_38_normal_form.py`, result SHA
  `73d51b6e9c476fd0ff4acb6f5e5ba5b9e7fc840dc54d04e49294f9d39f7421eb`.
- `audit_aligned_survivor_11_21_four_row_normal_form.py`, result SHA
  `b80a52af3fdb54144574c3d04ee3d2fb68b72bd4406fcd80d7441ca4f396f7cf`.
- `audit_branch0_triangle_defect_torus_unit.py`, result SHA
  `a981105235c9bb70ed29a7f85b03780feedacd993a43b38248734bde6f777368`.
- `audit_branch0_triangle_pendant_localized_chain.py`, exact-chain plus
  modular-unit result SHA
  `5f06e307ead3d9047875475e81e364b402c02508b6b104796571093e31e06002`.
- `export_branch0_triangle_pendant_p26_boundary_msolve.py` and
  `probe_branch0_triangle_pendant_p26_base_row_core.py`, exact boundary/core
  exporters; row-core discovery SHA
  `c1c697bcee3e08d4ffabd1ecd11c0f26d75fa1ce0b4b742e5757a58baab66549`.
- `export_branch0_triangle_pendant_p26_base_homogeneous_macaulay.py` and
  `audit_branch0_triangle_pendant_p26_base_homogeneous_ladder.py`, bounded
  degree-9--14 exact-interface modular ladder and independent dual replay.
