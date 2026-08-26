# Referee report: direct-parent responses into K21

## Verdict

The proposed direct-parent K21 computation is source-faithful **provided it
is labelled a 16-path subtotal, not a complete K21 page**.  The exact paths
are the seven direct K17 packets followed by K4, the six direct K18 packets
followed by K3, and the three direct K19 packets followed by K2.  They are 16
of the recurrence DAG's 52 required K21 lineages.

An independent anchor-signature enumeration (not a cycle-charge run) derives
all parent, pivot, and child-occurrence counts and verifies every scaled
division at `U=400591699200`.  It agrees with the expected frozen K17 and K18
censuses and newly pins the K19 pivot count.

## Signs and coefficient formula

Write the signed mass of R8-prime slice `r` as

```text
M_r = orbit_size_r * R8prime_coefficient_r.
```

For `P=-R8prime*E0*E1*E2`, every direct parent has coefficient
`c=-M_r`.  If its twelve-anchor signature admits `m` literal K0 pivots, the
declared all-dividing-pivots policy applies `a + tails = 0` and gives every
tail from every chosen pivot coefficient

```text
-c/m = +M_r/m,             scaled: U*M_r/m.
```

Thus all 16 response paths have a **positive response sign relative to the
signed R8-prime mass**.  This does not predict the sign of their cycle charge:
the charge functional itself can pair negatively with the emitted tails.

For a parent `x`, pivot `p`, response degree `j`, and charge functional
`lambda`, the exact scaled full-charge summand is

```text
(U*M_r/m(x)) * sum_{p divides x} sum_{t in T_j(p)}
    lambda(x - anchor_p + t).
```

The irreducible summand retains only children with no dividing K0 pivot.
The signature referee finds that every emitted K21 child is irreducible, in
agreement with the DAG bound that the last pivotable parent degree is K20.

## Packet IDs and parent formulas

The 485 R8-prime records and the frozen factor cardinalities
`(|K2|,|K3|,|K4|)=(12,32,60)` give:

| source | exact DAG IDs | raw-parent formula | raw parents |
|---|---|---:|---:|
| K17 to K21 by K4 | `D17:{234,243,324,333,342,423,432}|R:4` | `6*(485*12*32*60) + 485*32^3` | 82,938,880 |
| K18 to K21 by K3 | `D18:{244,424,442,334,343,433}|R:3` | `3*(485*12*60^2) + 3*(485*32^2*60)` | 152,251,200 |
| K19 to K21 by K2 | `D19:{344,434,443}|R:2` | `3*(485*32*60^2)` | 167,616,000 |

Per-packet raw parents are `11,174,400` for every K17 permutation of
`234`, `15,892,480` for `333`, `20,952,000` for every K18 permutation of
`244`, `29,798,400` for every K18 permutation of `334`, and `55,872,000`
for every K19 permutation of `344`.

## Exact signature-level work ledger

| parent group | raw parents | pivotable | pivot uses | K21 tail occurrences | K21 irreducible |
|---|---:|---:|---:|---:|---:|
| direct K17, then K4 | 82,938,880 | 81,076,480 | 267,564,800 | 16,053,888,000 | 16,053,888,000 |
| direct K18, then K3 | 152,251,200 | 137,817,600 | 260,736,000 | 8,343,552,000 | 8,343,552,000 |
| direct K19, then K2 | 167,616,000 | 111,744,000 | 111,744,000 | 1,340,928,000 | 1,340,928,000 |
| **total** | **402,806,080** | **330,638,080** | **640,044,800** | **25,738,368,000** | **25,738,368,000** |

The observed positive pivot counts are only `{1,2,3,5,7}`.  The audit checks
the stronger occurrence-wise condition

```text
(M_r * U) mod m = 0
```

before accepting any signature class.  Consequently integer division must
occur only after multiplication by the signed slice mass and `U`; a design
that asserts `U mod m = 0` globally would be an unnecessarily strong and
potentially misleading convention outside this direct subset.

## Implementation policy

For each literal factored parent occurrence:

1. compute its twelve-anchor signature and all 78 dividing K0 pivots;
2. skip it if the set is empty;
3. set `w=M_r*U/m`, with an exact-remainder assertion;
4. for every dividing pivot evaluate all 60, 32, or 12 tails according to
   source degree K17, K18, or K19;
5. add `w*lambda(child)` to the grouped K21 scalar.

Charge/profile caching may identify equal `(path profile, signature, pivot,
tail degree)` evaluations, but coefficients and raw occurrence counters must
remain source-linear.  The three packet families are disjoint DAG IDs, so
their grouped scalars may be added.  A grouped result does not supply 16
individual path scalars unless weights were kept separate by ID.

## Terminal result referee

The landed `results_k21_direct_charge.json` passes an independent
hash/arithmetic/count replay.  This replay reads the terminal JSON, the
previous signature-level plan result, the complete recurrence DAG, and the
audited Rust source; it does not execute the 402,806,080-parent job.

| direct-parent group | full = irreducible occurrences | scaled charge at `U` | reduced charge |
|---|---:|---:|---:|
| K17 then K4, 7 IDs | 16,053,888,000 | `-193472065663692963840` | `-16903800832/35` |
| K18 then K3, 6 IDs | 8,343,552,000 | `-370365062151064780800` | `-924545024` |
| K19 then K2, 3 IDs | 1,340,928,000 | `-68306666053002854400` | `-170514432` |
| **16-path subtotal** | **25,738,368,000** | **`-632143793867760599040`** | **`-55230881792/35`** |

The terminal IDs equal the planned lists exactly.  Its group ledgers also
reproduce `402,806,080` raw parents, `330,638,080` pivotable parents, and
`640,044,800` pivot uses.  For every group,

```text
full_occurrences = tail_count * pivot_uses = irreducible_occurrences
full_charge_scaled = irreducible_charge_scaled.
```

The negative displayed charges do not contradict the positive response sign:
the source implements `w=U*M_r/m`, while the signed cycle functional pairs
negatively with these emitted K21 tails.  Source inspection and its pinned
hash verify the exact occurrence-level remainder assertion
`(U*M_r) mod m == 0`.

Pinned terminal hashes:

- direct Rust source:
  `b8387f0cda67d39ed605fc1c4aab2801d4231b7d71d50c5dae5cca361f61968d`;
- included charge/profile provider:
  `24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045`;
- landed result:
  `3fb99bdf3e8f230bcc8fe61936de5cb9020623d628efc4f5bcefac9e73fe5899`;
- independent plan result:
  `6af4880ca1b398160d6a6e96dd0ecafe723e06c218c42052b62dfe93acd41300`.

Terminal-referee status:
`PASS_INDEPENDENT_TERMINAL_REFEREE_DIRECT16_K21_CHARGE`; logical SHA-256
`121a8b6421b8d6761c031f683192a89bdffcef9b66e868386b7453ff4e75c65a`.

## Scope and replay

This referee certifies the recurrence design, signs, IDs, exact parent/pivot
counts, division guards, and expected occurrence totals.  It does **not**
independently evaluate the 77-cycle functional or collect K21 rows.  It also
does not cover the other 36 required K21 lineages.

Run:

```text
python3 computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/audit_k21_direct_plan_referee.py
python3 computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/audit_k21_direct_terminal_referee.py
```

The machine-readable result has logical SHA-256
`1a05bf60b018d7d3eeed471de3cd9b6211029c4a8be9baa37f944e803e863292`.
