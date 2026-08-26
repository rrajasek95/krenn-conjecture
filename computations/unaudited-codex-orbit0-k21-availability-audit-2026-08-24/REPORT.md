# Exact K21 recurrence and artifact-availability audit

## Verdict

`PASS_EXACT_K21_52_ID_RECURRENCE_AND_AVAILABILITY_AUDIT`.  The frozen
K14--K24 recurrence DAG requires exactly **52** reachable K21 lineage IDs,
and the machine ledger partitions them by literal ID with no missing, extra,
or duplicate path.

The recurrence classification is exact:

| class | pivot depth | IDs |
|---|---:|---:|
| direct packet followed by one pivot response | 1 | 16 |
| derived | 2 | 30 |
| derived | 3 | 6 |

The direct 16-ID contribution is computed and independently terminal-refereed
at grouped full/irreducible charge `-55230881792/35`.  The five retained-
profile groups covering another 14 derived IDs are also computed and
independently audited at `-24730854875640832/2258025`.  Their strict disjoint
30-ID partial is therefore

```text
-28294075214451712/2258025
```

for both full and irreducible K21 charge.  This is eight group scalars, not 30
individual-ID scalars and not the complete K21 page.

## Exact current availability

| availability | IDs | consequence |
|---|---:|---|
| independently refereed direct grouped K21 charge computed | 16 | reuse the three direct-group scalars |
| independently audited profile grouped K21 charge computed | 14 | reuse the five profile-group scalars |
| literal pivotable K18 `[2,2]` checkpoint retained | 1 | terminal K3 charge evaluation only |
| K19 parent must be reconstructed from a literal source/checkpoint | 10 | reconstruct, signed-collect, then emit terminal K2 |
| K19 parent must be reconstructed from a source formula | 11 | replay source, signed-collect, then emit terminal K2 |

Thus 14 derived IDs have landed exact grouped charges, one more derived ID is
charge-ready from a literal terminal-parent interface, and 21 derived IDs
have no retained prolongable K19 parent.  At this pinned audit point exactly
22 IDs remain outside the strict 30-ID partial.

## Disjoint recurrence groups

| source/response group | depth | IDs | terminal parent | availability |
|---|---:|---:|---:|---|
| direct D17 `[4]` | 1 | 7 | K17 | computed/refereed |
| direct D18 `[3]` | 1 | 6 | K18 | computed/refereed |
| direct D19 `[2]` | 1 | 3 | K19 | computed/refereed |
| D14 `[3,4]` | 2 | 1 | K17 | profile charge computed/audited |
| D14 `[4,3]` | 2 | 1 | K18 | profile charge computed/audited |
| D15 `[2,4]` | 2 | 3 | K17 | grouped profile charge computed/audited |
| D15 `[3,3]` | 2 | 3 | K18 | grouped profile charge computed/audited |
| D15 `[4,2]` | 2 | 3 | K19 | reconstruct from direct-K15 checkpoint |
| D16 `[2,3]` | 2 | 6 | K18 | grouped profile charge computed/audited |
| D16 `[3,2]` | 2 | 6 | K19 | reconstruct from direct-K16 checkpoint |
| D17 `[2,2]` | 2 | 7 | K19 | replay direct-K17 source |
| D14 `[2,2,3]` | 3 | 1 | K18 | retained literal K18 checkpoint |
| D14 `[2,3,2]` | 3 | 1 | K19 | reconstruct from hidden-K16 parent provider |
| D14 `[3,2,2]` | 3 | 1 | K19 | replay K14/R3 K17 source |
| D15 `[2,2,2]` | 3 | 3 | K19 | replay K15/R2 K17 source |

The JSON records all 52 literal lineage IDs individually, including direct
packet, complete response word, sign, terminal parent degree, availability,
artifact keys, and exact remaining action.

## Strict 30/52 assembly audit

The independent audit pins and rederives
`k21_manifest_direct16_profile14_partial.json` and
`results_k21_direct16_profile14_22_gap.json`.  The manifest has exactly eight
disjoint scalar groups, covers the exact union of the independently accepted
16-ID and 14-ID results, and reproduces the rational value above by summing
each group scalar once.  The strict complete-page gate correctly returns
`REJECT_INCOMPLETE_K21_52_ID_GATE`, with 30 covered, 22 missing, no duplicate,
and no extra ID.

An independent hostile self-test constructs a synthetic complete 52-ID
manifest with one four-ID scalar group.  It verifies that the group scalar is
counted once, then rejects both a one-ID deletion and a duplicate-ID group.
These guards are recorded machine-readably in the result JSON.

## Retained terminal interfaces

The K17 terminal interfaces are the three frozen
`weights_k17_{direct,k14_k2,k15_k2}.bin` streams.  They retain the path/cycle
profile, anchor signature, selected pivot, and signed coefficient needed for
a terminal K4 evaluation; the applicable 14-ID slice has now been evaluated
and audited.  The K18 profile interfaces are the direct, K14/K4, K15/K3, and
K16/K2 merged profile checkpoints; they analogously suffice for a terminal K3
evaluation and the applicable direct/profile groups have landed.  The hidden
`[2,2]` path is stronger: the surviving
`checkpoint_k18_22_pivotable.bin` is a literal canonical-row checkpoint with
exact orbit mass, so `D14:222|R:2-2-3` needs no parent reconstruction.

Every large artifact is size-pinned and tied to its publisher/referee digest.
The K16/K2 merged profile and the smaller literal source checkpoints were also
rehash-checked directly by this audit.  The 12.68-GB hidden checkpoint uses its
independently frozen `CHECKPOINTS.sha256` manifest rather than a redundant
full reread.

## Exact reconstruction boundary

All 21 reconstruction-required paths end with a K19 parent followed by K2.
No canonical K19 coefficient/profile checkpoint survives.  The sources are
nevertheless pinned and reconstructable:

- direct K15 and K16 have literal canonical source checkpoints;
- direct K17 and the K14/R3 and K15/R2 K17 streams have frozen source-linear
  replay formulas and the exact R8prime structure;
- the hidden K14/R2 K16 stream retains all 31 literal parent runs plus a
  restartable K3 child provider.

The existing K19 scalars and source-compressed profile files do **not** close
this gap: they were designed for a single terminal response, omit exact-zero
signed profiles, and are not row checkpoints.  Likewise, the raw
`checkpoint_k17_*.bin` files contain irreducible normals rather than the
pivotable parent feeds.

## Scope and replay

This is an availability/provenance theorem for the immediate K21 cycle
charge.  It does not collect K21 coefficients, emit K22 tails, assemble the
full residual, run the terminal span test, or imply a conjecture verdict.

Replay with:

```sh
python3 computations/unaudited-codex-orbit0-k21-availability-audit-2026-08-24/audit_k21_availability.py
```

The recurrence DAG byte SHA-256 is
`469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa`,
its logical digest is
`ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`,
and this availability ledger's logical digest is
`4db5d5a2baf16a02c1da86da1a020b96e2152aab226e70bacc981f47ea129b23`.
