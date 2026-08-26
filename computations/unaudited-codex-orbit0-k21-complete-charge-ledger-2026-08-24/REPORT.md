# Complete exact K21 charge ledger

Status: **PASS_COMPLETE_K21_52_ID_EXACT_Q**.

The strict generic assembler covers exactly all 52 reachable K21 lineage IDs
in the frozen recurrence DAG, with no missing, duplicate, or extra ID.  The
complete manifest contains 15 exact scalar groups.  A grouped scalar is summed
once while every member ID participates independently in the coverage gate.

## Exact charge

Full and irreducible charges agree:

```text
K21 full        = -15276224591027275648/521603775
K21 irreducible = -15276224591027275648/521603775
common U        = 400591699200
```

This is a charge ledger only.  No membership or nonmembership conclusion is
drawn from the value or its sign.

## Closure of the former 47/52 gate

The prior 47-ID manifest is preserved byte-for-byte as the first 12 scalar
groups.  The five missing IDs were closed by three independently refereed
source-faithful scalars:

| covered ID(s) | scalar added once | producer evidence |
|---|---:|---|
| `D14:222|R:2-3-2` | `-381879288887675648/173867925` | `a58fa701...` |
| `D14:222|R:3-2-2` | `-32834300375025536/15806175` | `46065e0c...` |
| `D15:{223,232,322}|R:2-2-2` | `-4849716689615104/929775` | `c6879b66...` |

The last row covers three IDs but contributes its scalar exactly once.  An
independent deliberately-wrong recomputation that multiplies every scalar by
its group size gives a different result and is rejected.

## Coverage and provenance guards

The final audit independently selected reachable degree-21 nodes from the DAG,
obtaining the same unique 52-ID set as the declared list.  Flattening the
manifest gives exactly that set, and the generic assembler reports:

```text
required_paths = 52
covered_paths  = 52
scalar_groups  = 15
missing        = []
duplicates     = []
extra          = []
```

The generic assembler was separately refereed under standard Python, `-O`, and
`-I -S`, including fail-closed hostile mutations.  All three newly appended
producer results and their independent referee results are byte-pinned.  The
manifest logical SHA-256 is
`5e257c21950dfe539e8771e52be9e3e82aaf6593ac3c45e97df2311b7b0eae8b`.

Authoritative files:

- `computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/k21_manifest_complete_52.json`
- `computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/results_k21_complete_52_exact.json`

Replay the final independent ledger audit with:

```bash
python3 computations/unaudited-codex-orbit0-k21-complete-charge-ledger-2026-08-24/audit_k21_complete_52.py
```

Final audit logical SHA-256:
`c5dd10ffd307121e9e1385d72ab77105708b85149ca682efd5ce2cd1e345035a`.
