# K23 strict 42/59 partial integration

Status: **PASS_INDEPENDENT_K23_42_OF_59_PARTIAL_INTEGRATION_REFEREE**. This is an exact partial integration, not a complete K23 claim.

## Coverage and arithmetic

- Sealed direct23 fragment: 23 IDs in 4 scalar groups.
- Sealed grouped direct-K16 fragment: 18 IDs in 3 scalar groups.
- Sealed hidden-collected singleton: 1 ID in 1 scalar group.
- Combined: exactly 42 of 59 frozen K23 IDs, with no duplicate or extra ID.
- Each of the 8 grouped scalars is added exactly once. The hostile per-ID multiplication is unequal and rejected.
- Exact subtotal: scaled by `U = 400591699200`, `-4222958701661124231168`; rational `-1832881380929307392/173867925`.
- Every included group has `full = irreducible` because its K23 output is terminal in the sealed producer evidence.

The direct-K16 fragment manifest is sealed but omits `group_id`. This integration restores each label uniquely from the corresponding group in the sealed composite result by exact ordered ID equality; all scalar, rational, evidence-path, and evidence-hash fields remain byte-for-byte equal to the source fragment entry. The referee checks this normalization explicitly.

## Exact remaining gap

The 17 missing IDs are exactly:

- `D14:222|R:2-3-4`
- `D14:222|R:2-4-3`
- `D14:222|R:3-2-4`
- `D14:222|R:3-3-3`
- `D14:222|R:4-2-3`
- `D15:{223,232,322}|R:2-2-4`
- `D15:{223,232,322}|R:2-3-3`
- `D15:{223,232,322}|R:3-2-3`
- `D15:{223,232,322}|R:4-4`

Equivalently, the gap is 9 scalar groups: five D14 singletons and four grouped three-ID D15 families.

## Referee and pins

The frozen DAG, expected 17-group contract, official strict assembler, all three source fragment manifests, upstream independent/package audits, and all five distinct evidence-result files are SHA-256 pinned and replayed. The official assembler reproduces the partial result exactly. Independent hostile tests reject duplicate groups, regrouped IDs, unknown groups, rational/scaled disagreement, evidence-hash corruption, and per-ID multiplication.

- Integration manifest SHA-256: `47b30fbb855f18e7ab10db4ff48b5b905211dc1eb4f37935c33220f4a447f8ca`
- Strict partial result SHA-256: `9e7021c430731a39a0587a6d24ba625ba7b3a401d17a3e1f2f8b68ede8a48051`
- Independent audit SHA-256: `0ce385763b44d458de11fc30b6a46a5c79507f98d0eb44877ba45e60287bd9dd`
- Independent audit logical SHA-256: `1881d45148513af77de2a93a1ac2f9accd2ee4114a8b8f2dbf80d0aa5a843005`

No recurrence fold, charge production, K24 work, row construction, or new lineage inference was performed.
