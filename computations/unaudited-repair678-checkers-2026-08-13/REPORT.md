# UNAUDITED REPAIR CANDIDATES — audit repair items 6, 7, 8

**Status: UNAUDITED. These are replacement *candidates*, not committed
checkers. Nothing outside this directory was modified.**

| | |
| --- | --- |
| Pinned HEAD at authoring | `7d57c552a3ef57d3a95c3bc933af547ad55e087d` |
| Re-verified at | `6680bc133402682e4abc9e09104af498a9468bc3` (three later commits landed mid-pass; none touches any file pinned below, and all six scripts reproduce their digests at both HEADs) |
| Source of the defect list | `computations/unaudited-external-spine-audit-2026-08-13/REPORT.md` |
| Scope | audit repair items **6** (rebuild foundations ledgers, add controls, fix the involution check), **7** (repair the orbit-lifting checkers), **8** (verify the six-concept pivot applicability) |
| Style | stdlib only; clean under `python3`, `python3 -O`, `python3 -I -S`; `require`-based (no `assert`, so `-O` is a no-op on the checks) |

Every script ships a **content-hashing frozen ledger** (digests of monomial
lists, evaluation vectors, rank vectors, cell profiles and orbit data — never
of counts, strings or booleans alone) and at least one **fabricated-geometry
positive control** executed in the same process under a `should_fail` guard.

The mathematics being re-verified was already established as **true** by the
external auditors' independent reconstructions. What was missing was a
checker that verifies it. That is what these are.

---

## 1. `verify_lambda_kills_operator_block.py`

**Repairs**: `computations/verify_h3_first_flat_physical_anchor_six_term_separator.py`
(the checker contains `operator_feature_sum = 0; operator_ainc = 0;
require(operator_feature_sum - operator_ainc == 0)` and publishes
`"complete_8580_first_flat_operator_columns": 0`; the 8,580-column operator
is never loaded).

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: ~29 s.

What it actually does:

- reconstructs the exact first-Spencer-flat operator block through the pinned
  construction modules (8,580 columns, exact rank 1,328, 343-term solution —
  all re-derived, not asserted), attaches each column's literal bridge
  (kind-3) feature rows through the canonical covariance/arm-contraction
  presentation, and appends the 288 repeated full-nine columns;
- evaluates `Lambda = sum(six selected private matching features) - ainc`
  **column by column** on all 8,868 columns;
- separately establishes the *structural* reason the audit identified: **490**
  of the 8,580 operator columns carry a nonzero bridge feature, **0** touch
  any of the six selected private features, **0** carry anchor incidence — so
  the vanishing is structural, not a cancellation;
- recomputes the repeated half from the boundaries: profile
  `{features=1, pure_marker=1}: 6`, `{features=0, pure_marker=0}: 282`.

Result: `Lambda == 0` on all 8,580 operator columns and all 288 repeated
columns.

| ledger field | value |
| --- | --- |
| `operator_evaluation_stream_sha256` | `a860af97c1980c112f3e2683140d0ae7e7a6bd603509ea2094b4a8320a99aeb5` |
| `operator_bridge_subcolumn_sha256` | `9b66cb028ba8eecfe85f1f7fd8b46199811f6e4c515dc9a010ed9acefbaeea16` |
| **`ledger_sha256`** | **`3ea9d9cfbbc2571df1c1a5b8de8c7a82bb052e6670246edc82684cfe411ad21e`** |

**Positive controls (both fire):**
1. *fabricated feature selection* — take the six most frequent bridge features
   that **do** occur in the operator block instead of the six selected private
   matching rows. Lambda then takes values
   `{0: 8090, 1/2: 254, 1: 95, 3/2: 66, 2: 39, 3: 22, 4: 11, 6: 2, 8: 1}`;
2. *fabricated anchor-incidence law* — `ainc = 0` on the pure repeated
   columns; Lambda reads `-1` there.

**Mutation test:** replacing the covector by "sum of **all** bridge features
minus ainc" makes the run fail with
`('Lambda is nonzero on an operator column', ...)` and the above histogram.
The 8,580-column check is therefore doing work — exactly what the committed
`0 - 0 == 0` cannot demonstrate.

---

## 2. `verify_activity_overlap_ranks.py`

**Repairs**: `computations/verify_h3_physical_cartan_active_overlap_landing.py`
(`rank_before = (2, 3)` and `rank_after = (3, 3)` are literals compared to
themselves; no matrix is built anywhere in the file; negating the claim leaves
the digest byte-identical).

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: ~3 s.

The rank model is stated explicitly in the file header rather than left
implicit: the overlap cap `(P, u)` carries three selected endpoint heads
`e0, e1, e2` (unary pure-zero, and the two selected bright colours); passing
to the cap at `u` deletes head `e_c` iff `u` is the S-neighbour of the
colour-`c` selected bright matching; target-fullness of `u` is rank three on
the inner star. The checker **imports the pinned `rank` routine** from
`verify_h3_post_ks_full_nine_overlap_visibility_reduction.py` (exact Gaussian
elimination over `Q`) — the machinery the landing checker already had
available and did not call — and evaluates it on every packet.

Computed rank profiles over all **461,700** packets:

| branch | packets | computed profile |
| --- | --- | --- |
| `selected_target_full_arm_repairs_quotient` | **310,500** | `(2,3) -> (3,3)` for all |
| `shared_bright_neighbour_activity_not_forced` | 76,950 | `(3,3) -> (3,3)` for all |
| `full_set_avoids_bright_neighbours_activity_not_forced` | 74,250 | `(3,3) -> (3,3)` for all |

**Orbit argument (verified, not assumed):** under `G = S6 x S2` (internal
relabelling x bright-colour swap) the branch and rank data are constant on
orbits. The checker computes the full orbit decomposition by union-find over
the generators `(0 1)`, `(0 1 2 3 4 5)` and the colour swap, gets **452
orbits** with size histogram `{90: 8, 180: 15, 360: 57, 720: 136, 1440: 236}`
summing to 461,700, and **verifies** constancy on every orbit. So a
452-element representative set is provably sufficient — and the checker
evaluates all 461,700 anyway and hashes the stream.

| ledger field | value |
| --- | --- |
| `full_evaluation_stream_sha256` | `cdb976d7845e68c28b421b1dd5d1ffbb74d063261a8889a6507319bc964863b9` |
| **`ledger_sha256`** | **`962f9d51f57acde38f22b959b0e32fface655f4f94a36167b4e57d5bdf2177e9`** |

**Positive controls (both fire):**
1. *fabricated bright inventory* — drop the direct-free condition so the
   "bright" matchings include the ones using the direct PS pair;
2. *fabricated synchronization* — in the selected-arm branch take the
   candidate site **outside** `{n1, n2}` instead of inside it. This is the
   precise geometric content of the target-full/bright synchronization
   theorem, and without it the overlap is already `(3,3)` before transport.

**Mutation test:** swapping the head-deletion law (candidate `= n1` deletes
`e2` instead of `e1`) fails with
`('the selected-arm branch is no longer uniformly (2,3)->(3,3)',
{'[2, 3]->[2, 3]': 310500})`.

---

## 3. `verify_double_coloop_interference_coefficients.py`

**Repairs**: `computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py`
(the verified `1 / 14 / 15 / 75` partition is a pure matching count that holds
for any edge in any packet — 15 of 105 matchings contain a given edge, 15
contain the direct PS pair disjointly, 105-30 = 75 remain — and never inspects
a colour or a coefficient; plus the "one orbit" wording error).

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: <1 s.

Three genuinely new layers:

1. **Census and orbits, stated correctly.** 270 residual ordered packets =
   **two** `S6` orbits, sizes **90** (`matching1 = matching2`) and **180**
   (tails one `C4` apart), computed by union-find and with the tail shape
   verified constant on each orbit; the bright-colour swap preserves both.
   The impossibility of a single 270-orbit is encoded as the Lagrange check
   `720 % 270 != 0`.
2. **Literal cell-level coefficient claims.** For every one of the 270 packets
   and every one of the 105 matchings, the decorated cell multiset assigned by
   the hybrid word (colour 2 at `S` and the common S-neighbour `n`, colour 1
   elsewhere) is computed and checked: the seed uses the pure-2 diagonal cell
   on `e = (n,S)` plus the three pure-1 diagonal cells of `matching1`, all
   four being anchor cells; the 14 retain-`e` mates are `A_e^{22}` times a
   pure-1 cofactor monomial; the 15 direct mates carry the cell
   `((P,S), 1, 2)` with its colours checked; each of the 75 avoiding mates
   exposes exactly one off-diagonal S-arm cell `((m,S), 1, 2)` on an edge
   outside all three pure anchors.
3. **The algebraic identity, exactly, on an honest complete-row model.** Exact
   rational cells, rows summed over all 105 matchings, escape hypotheses
   imposed as cell values, normalizations **solved** for, and then derived:
   `R_hybrid = A_e^{22} * C_1`, `A_e^{22} != 0`, `R_hybrid = 0 => C_1 = 0`,
   and `R_pure1 = 1` forces the omit-`e` aggregate to equal 1 — so a nonzero
   pure-1 matching term omitting the common S-arm is **forced** and is
   exhibited. Run for both orbit representatives and then, independently
   seeded, for all 270 packets.

| ledger field | value |
| --- | --- |
| `full_cell_type_stream_sha256` | `14f85210b4c5a8c5c6688a1c21197e466f59d3e80ec088a850c204748fbf084d` |
| `all_270_certificate_stream_sha256` | `70ab22848f5922940df2b370e5591b3adbf5d16238d80a51af772d364bb6f740` |
| **`ledger_sha256`** | **`505624ba62ee7a720beb89f3cc319078aaee83595519d42aedd76a31ffccb9d7`** |

**Positive controls (both fire):**
1. *fabricated hybrid colouring* — heat `S` and the common **P**-neighbour
   instead of the common S-neighbour;
2. *fabricated residual condition* — define the residual by the shared
   S-neighbour alone (dropping the shared P-neighbour), which is not the
   double-coloop condition.

**Mutation test:** classifying against the P-arm instead of the S-arm (both
are common to the two anchors, so the naive precondition still passes) fails
with `('the seed lost the pure-2 diagonal cell on the common S arm',
((0, 1, 1, 1), (2, 3, 1, 1), (4, 6, 1, 1), (5, 7, 2, 2)))`.

---

## 4. `verify_six_concept_pivot_applicability.py`

**Repairs**: `computations/verify_h3_active_fan_coloop_complete_row_pivot.py`
(`audit_complete_row_pivot` is free-symbol ring arithmetic,
`audit_six_closed_concepts` emits the string
`"the same alpha*U_i-d_i*V_i=alpha pivot"`, and the two functions never touch
each other's data, so zero of six concepts is verified).

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: <1 s.

- **The six concepts are identified honestly.** All `2^15` subsets are closed
  under the blocker operator; **448** Galois-closed sets result; `S6`
  decomposes them into **11** orbits; removing the two degenerate ones leaves
  **446** in **9** orbits; the blocker duality `F <-> T(F)` pairs those 9 into
  exactly **6** concept types (three self-dual — triangle 3|3, path 3|3, star
  5|5 — and three dual pairs 1|9, 2|4, 2|6). The six committed
  representatives are then verified to realize the six types, one each. This
  is the `5,141 / 446 / six types` census the audit reproduced, now connected
  to the pivot.
- **An honest complete-row model per (channel, hole)**, 60 in total (2 target
  channels x 30 oriented holes). In each: exact rational decorated cells on
  eight sites; the direct PS cell zeroed; `e = (0,1)` made a *computed* coloop
  of the pure-`c` support (the checker verifies every nonzero pure-`c`
  monomial contains `e`); `alpha` **solved** so that `alpha*C_c = 1`; the
  endpoint hole pinned by zeroing the `i`-channel P-arm and S-arm cells off
  it, which leaves the pure-`c` row untouched; the pure-`i` target row
  **solved** to 1 and the two-site mixed row **solved** to 0.
- **The pivot then derived, not posited**: `d_i C_i + U_i = 1`,
  `alpha C_i + V_i = 0` with the *same* cofactor `C_i` (checked separately on
  the retain-`e` parts), `alpha U_i - d_i V_i = alpha`, `alpha != 0`, and
  therefore a literal omit-`e` term is forced. Its endpoint hole is checked to
  be the pinned one, and the **claimed typing is checked term by term**:
  exactly two changed cells, both incident with `e`; identical decorations
  elsewhere; unchanged P/S partners, orientation and endpoint output heads.
- The substantive regime is non-degenerate: of the 60 models, **24** (the
  holes disjoint from the coloop) have `C_i != 0` with both `U_i` and `V_i`
  nonzero; the other 36 (holes meeting the coloop) have `C_i = 0`, `U_i = 1`,
  `V_i = 0` — the identity still holds and is still verified.

| ledger field | value |
| --- | --- |
| `pivot_model_stream_sha256` | `79e9f76a40a4add7145e39324ab16547d0459991fe7f24dba2fca006e2034d0e` |
| **`ledger_sha256`** | **`a07fd3ffac971fb9b330d59b81a3a5822382d47b88a61deba9a4cf88d9c013f7`** |

**Positive controls (both fire):**
1. *fabricated coloop* — keep the pure-`c` cells on edges meeting `{0,1}`, so
   `e` is not a coloop; the computed coloop property fails;
2. *fabricated closed concept* — `{01, 02, 03}` presented as saturated.

**Mutation test:** changing the mixed word to alter only **one** coloop
endpoint fails with `('a paired omit-e term lost its two changed incident
cells', ((0, 6), (1, 7), (2, 3), (4, 5)), ((0, 6),))`.

---

## 5. `verify_involution_pinned.py`

**Repairs**: the endpoint-involution half of
`computations/verify_h3_physical_cartan_source_orbit_descent.py` (the ledger
records the *string* `"0 <-> 1"` plus two counts, so it misreports after
mutation; the audit found 16 of 28 transpositions pass).

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: ~18 s.

**Which branch of the task's alternative applies: the second.** The theorem
does **not** need specifically `0 <-> 1`; it needs membership in an invariance
group, and this checker verifies THAT correctly and exhaustively. The
construction `K = (1-s)H_w` uses only: (A) `s` an involution of the eight
sites; (B) `s` an automorphism of the direct-free presentation, transporting
every literal decorated 90-term row; (C) `s` commuting with the signed tail
Weyl action at `TAIL_SITES = (2,5)`.

Established:

- `Aut(direct-free presentation) = Stab_{S8}({3,6})`, order **1440**,
  isomorphic to `S6 x S2` — verified over **all 8! = 40,320** site
  permutations, and the set-level criterion is checked to agree with the
  criterion on the literal decorated rows for every one of the 28
  transpositions (3^8 words each);
- exactly **16** transpositions transport every literal row (the 15 inside the
  six non-forbidden sites plus the forbidden-pair swap `3 <-> 6`) — this
  reproduces the audit's 16-of-28;
- exactly **8** also satisfy (C): `0<->1, 0<->4, 0<->7, 1<->4, 1<->7, 2<->5,
  3<->6, 4<->7`. `0 <-> 1` is admissible; it is **not forced**, and the ledger
  records the whole admissible set plus a per-transposition row-transport
  digest, so substituting an inadmissible swap moves the digest;
- a sharper reading of the committed "endpoint oddization kills the target
  defect" test than the audit's: over all 40,320 permutations it holds **iff
  the permutation stabilizes the tail pair `{2,5}` setwise** (group order
  1440). It is therefore exactly condition (C) — not vacuous, but it never
  sees the forbidden pair, so it cannot pin `0 <-> 1` either.

| ledger field | value |
| --- | --- |
| **`ledger_sha256`** | **`3a97871981a9851ef9bae9a571b19b94b159d2c12e79e127d119e6cf01f62ad4`** |

**Positive controls (both fire):**
1. *fabricated direct-free pair* `{3,7}` — its automorphism group is a
   different subgroup of `S8`;
2. *row transport under `0 <-> 3`* (moves the forbidden pair) — must not
   transport the real presentation's rows.

**Mutation tests (two):**
- fabricated decoration law (edge reversal no longer swaps the two colours)
  fails with `('literal row transport disagreed with the presentation
  automorphism group', (0, 1), False, True)`;
- `TAIL_SITES = (2,5) -> (2,4)` fails with `('tail sites changed', (2, 5))`.

---

## 6. `LEDGER-DISCIPLINE.md` + `ledger_discipline_demo.py`

**Built**: yes. **Passes**: yes, all three modes. **Runtime**: <1 s.

The note proposes the two rules the audit demands — *frozen ledgers must hash
mathematical content*, and *every checker ships a fabricated-geometry positive
control* — with the idioms and a one-second self-test for rule 1. The demo
runs entirely in memory and writes nothing.

Before/after on the sl2 prism checker
(`computations/verify_h3_sl2_weyl_cartan_prism.py`), all five variants
executed in one process:

| variant | `ledger_sha256` |
| --- | --- |
| V0 as committed | `bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2` |
| V1 = V0 with every mathematical `require` deleted | `bde6a55f...` (**identical**) |
| V2 = V1 **and** the signed Weyl action mutated `(-1)**a -> (-1)**b` | `bde6a55f...` (**identical**) |
| V3 = V0 with a content-hashing ledger | `b5efd5075b0543169ce71107e2f4be379651a4cbcec325dca8f840aa02bab5a6` |
| V4 = V3 with checks deleted **and** the same mutation | `bd5fdde4aebc8f3c58e38cd7b828494d26dad105c0977c9bcc04bc07f6366bea` (**changed**) |

V2 is the point: a copy of the checker that computes a **false** Weyl action
and performs **no verification at all** publishes the committed pinned digest
byte for byte. One rolling hash over the computed vectors fixes it.

Demo `ledger_sha256`:
`5fc65b4416593efbb07e3b125e9efc7b068141252f4b796a4e9bcca08d4d65e0`.

---

## 7. `WORDING-FIXES.md`

Six items for the notes maintainers, each with the committed sentence, its
file:line at the pinned HEAD, the correction, and how it is substantiated:
the 270 two-orbit correction; the `2,126,208` (chart, triple)-pairs qualifier
and the 260,118 distinct triples; the 264 four-cell survivors on chart
`(1,3)`; the "no unclosed linear branch" model-scope; the determinant-bright
entry-versus-landing split; and the "every new typed hole strictly enlarges
the closure" inflationarity note. Two supporting corrections (the
446/9-orbits/six-types accounting, and the "s **is** `0<->1`" -> "take `s` to
be" phrasing) are appended.

**Two figures in that list were NOT recomputed here** and are flagged as such
in the file: the `260,118` distinct triples and the `264` four-cell survivors
on chart `(1,3)`. Both come from the auditors' own computation and would need
the full `E14` chart machinery to re-derive. The *qualifiers* they support
(the pairs-versus-triples distinction; three-cell emptiness not being "the
last local monomial degree") stand independently of the exact numbers.

---

## Three-mode reproduction

All six scripts, run as `python3 X.py`, `python3 -O X.py`,
`python3 -I -S X.py`, produce identical `ledger_sha256` in all three modes at
both HEADs above.

| script | `ledger_sha256` | approx. runtime (one mode) |
| --- | --- | --- |
| `verify_lambda_kills_operator_block.py` | `3ea9d9cfbbc2571df1c1a5b8de8c7a82bb052e6670246edc82684cfe411ad21e` | 29 s |
| `verify_activity_overlap_ranks.py` | `962f9d51f57acde38f22b959b0e32fface655f4f94a36167b4e57d5bdf2177e9` | 3 s |
| `verify_double_coloop_interference_coefficients.py` | `505624ba62ee7a720beb89f3cc319078aaee83595519d42aedd76a31ffccb9d7` | <1 s |
| `verify_six_concept_pivot_applicability.py` | `a07fd3ffac971fb9b330d59b81a3a5822382d47b88a61deba9a4cf88d9c013f7` | <1 s |
| `verify_involution_pinned.py` | `3a97871981a9851ef9bae9a571b19b94b159d2c12e79e127d119e6cf01f62ad4` | 18 s |
| `ledger_discipline_demo.py` | `5fc65b4416593efbb07e3b125e9efc7b068141252f4b796a4e9bcca08d4d65e0` | <1 s |

Mutation harness used for the six mutation tests above:
`scratchpad/repair678/mutate.py` (session scratchpad; copies each script,
repoints `ROOT` at the repository, applies one edit, and runs it). All six
mutations fail; the messages are quoted per script.

---

## Honest limits of this pass

1. **These are candidates, not audited checkers.** They have not been
   externally re-audited, and their `EXPECTED_LEDGER_SHA256` values are
   self-pins living in the same files as the ledgers — the audit's
   cyclic-pin-graph criticism applies to them too. Content hashing makes a pin
   *mean something mathematically*; it does not make a self-pin trustworthy.
   A digest registry outside the checkers is the complementary repair and is
   not attempted here.
2. **The overlap rank model (script 2) is stated, not derived.** The three
   selected endpoint heads, the deletion law, and target-fullness implying
   inner rank 3 are the model the pinned post-KS visibility reduction already
   uses; this pass makes it explicit and evaluates it on every packet, which
   is strictly more than the committed literals. Deriving that model from the
   physical cap differential is theorem work and remains open.
3. **The honest complete-row models (scripts 3 and 4) are models.** They show
   the identities are true and non-vacuous on a faithful complete-row
   presentation with the coloop and the normalizations constructed. They do
   not show the *physical* rows realize them. Script 3 additionally imposes
   the escape hypotheses (forbidden direct mixed cell = 0, no new off-diagonal
   S-arm cell) as cell values — verifying the conditional, not the hypotheses.
4. **Script 4 uses pseudo-random rational cells** from a deterministic LCG,
   with a bounded seed retry when an assignment is too degenerate to carry a
   normalization (a `ModelNotGeneric` path that can never mask a failure of a
   mathematical claim, since those use `require`). The seed actually used is
   recorded in each certificate and hashed.
5. **Nothing here addresses the CRITICAL items.** The operator-to-physical
   chain map for `K`, the derivation of `eta`/`sigma`, `D2 = -delta` as
   attainability versus equality, and source-typing `x_v` are theorem work
   (audit repair items 1-5), untouched by this pass.
6. **Two figures in `WORDING-FIXES.md` were not recomputed** — see section 7.
