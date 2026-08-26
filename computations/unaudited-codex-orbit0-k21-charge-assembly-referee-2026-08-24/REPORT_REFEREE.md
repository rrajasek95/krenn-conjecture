# Independent referee: generic filtered-degree exact assembler

Status: **PASS** for
`assemble_filtered_degree_exact.py` at pinned SHA-256
`cf4a5214a15081b91d89c90fc4b79c39e0d54e9b183f442131eec258bf1bce69`.
No charge evaluator was run.

## Frozen DAG

The referee did not merely read the declared degree lists.  It independently
selected all `reachable: true` nodes by degree from the frozen node ledger and
compared the sorted IDs to `required_reachable_lineage_ids_by_degree`.

| degree | unique required IDs |
|---|---:|
| K20 | 36 |
| K21 | 52 |
| K22 | 76 |
| K23 | 59 |
| K24 | 35 |

All five sets agree exactly.  Node IDs are globally unique, the embedded count
ledger agrees, and every reachable K21--K24 ID occurs as a reachable edge
child.  Removing the stored logical hash and canonically hashing the remaining
DAG JSON reproduces
`ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66`.

## Exact grouped-scalar semantics

Coverage is flattened over every `id`/`ids` member, but `full` and
`irreducible` are summed once per manifest entry.  The referee independently
used `Fraction` arithmetic over the authoritative manifests:

- K20 covers 36 IDs using 11 scalar entries;
- K21 covers 47 IDs using 12 scalar entries;
- no grouped scalar is multiplied by the size of its ID group.

This independently reproduces the authoritative complete K20 values:

```text
full        = 12488470121433187072/521603775
irreducible = 12162234158979734656/521603775
```

Fresh generic K20 JSON was byte-identical across standard, `-O`, and `-I -S`
runs (SHA-256
`01bebf013e13a89c625ede721c664066b2e1f9ba0cd2125d911e561ba6a511f4`).
Its coverage, missing-ID list, DAG pin, and exact rational fields match the
authoritative historical K20 result.  The generic schema intentionally uses
new names such as `complete_claim`, so byte equality is claimed among generic
replays, while exact-field equality is claimed against the historical schema.

## Current K21 gate

Fresh partial-audit output is byte-identical to the frozen generic artifact,
SHA-256
`fb80865e12ac44d46a9425f7b8e2d16d9331e34a98eb35270860a0a906a5b31a`.
It covers 47 of 52 IDs and reports exactly:

```text
D14:222|R:2-3-2
D14:222|R:3-2-2
D15:223|R:2-2-2
D15:232|R:2-2-2
D15:322|R:2-2-2
```

as missing, with partial full = irreducible charge
`-448972336918014464/22678425`.  Without `--audit-incomplete`, the same
manifest exits 2 and creates no output.  This audits the specifically pinned
47/52 artifact; it does not claim that later charge packages have already been
incorporated into that manifest.

## Fail-closed interpreter matrix

The internal self-test produced identical bytes under:

```text
python3
python3 -O
python3 -I -S
```

The referee also independently invoked the CLI with missing, duplicate, extra,
bad-digest, ambiguous-schema, and unsupported-degree mutations.  All 18
mode/mutation combinations exited 2 with `REJECT` and left no output file.
Optimized mode therefore does not remove a security/completeness check.

The assembler validates evidence digests syntactically as lowercase 64-hex
strings.  It does not dereference an evidence artifact or recompute that
artifact's digest; provenance authenticity remains the responsibility of the
pinned producer/referee packages supplying each manifest entry.  This is a
scope note, not a failure of the declared exact assembly gate.

## Replay

```bash
python3 computations/unaudited-codex-orbit0-k21-charge-assembly-referee-2026-08-24/audit_filtered_degree_exact.py
```

Result logical SHA-256:
`620bdc2c0d6f52ac195583072838b31c63946dde614b727f1e53a6351b7e91f4`.
