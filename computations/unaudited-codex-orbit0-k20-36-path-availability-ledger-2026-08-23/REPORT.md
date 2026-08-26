# Authoritative K20 36-path artifact-availability ledger

## Verdict

The certified K20 DAG has exactly 36 reachable lineage IDs.  The current
artifact state partitions them exactly as follows:

| availability | paths | consequence |
|---|---:|---|
| exact K20 full/irreducible charge already computed | 2 | reuse directly |
| exact terminal-parent profile/weight interface available | 17 | four terminal profile evaluations suffice |
| immediate K18 parent represented only by a scalar charge | 16 | reconstruct and collect the pivotable K18 parent stream |
| direct K20 source packet available, charge not evaluated | 1 | one factorized direct evaluation |

The machine-readable ledger lists every path individually and proves literal
set equality with the frozen 36-ID interface.  Logical digest:
`718c38963c38c9bacfd013d2f43c7028ebe26d69f3d0e15047dd4238a1de3903`.

This is an availability theorem, not a new K20 charge run.  Only two K20
lineages currently have numerical charges; the other 34 remain an exact
charge gap.

## Exact computed paths

| lineage | exact artifact |
|---|---|
| `D14:222|R:2-2-2` | `results_k20_222_charge.json`, SHA-256 `a022874ad36361caf44de2473b4a5c7534ecfb9c082df046e3f26046fcc90a57`; independent referee PASS |
| `D14:222|R:2-4` | `results_full_hidden_k3_k4_charge.json`, SHA-256 `aa25a2deee2aff213b9f49b9f61826d161293651ccafa1cd7332ef978ae89934` |

Their exact two-path partial is frozen separately; it is not a K20 subtotal
for the other 34 paths.

## Parent-profile interfaces: 17 paths

These are source-compressed `(profile, signature, pivot, weight)` interfaces.
The frozen K19 implementation proves that the cycle charge and next-pivot
predicate depend only on those fields and the requested terminal tail degree.
They therefore suffice for the **K20 charge total**, but they are not literal
row checkpoints and cannot support a later row-collection claim.

| group | lineage IDs | frozen interface | terminal change |
|---|---:|---|---|
| K14 `[3,3]` | 1 | `weights_k17_k14_k2.bin`, SHA `34fdbffd...` | K2 to K3 |
| K15 `[2,3]` | 3 | `weights_k17_k15_k2.bin`, SHA `864b3cac...` | K2 to K3 |
| direct K16 `[4]` | 6 | `weights_k16_direct_k3.bin`, SHA `d7dee1ea...` | K3 to K4 |
| direct K17 `[3]` | 7 | `weights_k17_direct_k2.bin`, SHA `4fa59665...` | K2 to K3 |

Each multi-lineage file is already aggregated across its named direct-packet
group.  It yields the exact group charge, not separate per-lineage scalars;
the ledger records that granularity rather than overstating provenance.

## Scalar-only K18 boundary: 16 paths

The exact K18 charge result retained full/irreducible scalar pairings but not
the pivotable K18 parent profiles.  A scalar cannot be prolonged through the
terminal K2 response.  Four source components must therefore be replayed:

| K18 component | K20 paths |
|---|---:|
| K14 `[4]` then `[2]` | 1 |
| K15 `[3]` then `[2]` | 3 |
| K16 `[2]` then `[2]` | 6 |
| direct K18 then `[2]` | 6 |

The controlling scalar file is `results_k18_charge.json`, SHA-256
`eff58152c9b465b4fa770642898ada990f682bc677dac9363374f54aa65d5d47`.
The later 17-path K18 assembly confirms coverage but does not create these
missing parent streams.  The special hidden `[2,2]` parent checkpoint does
not repair any of these 16 lineages; it has already been consumed by the
computed `[2,2,2]` path.

## Minimal complete-K20 schedule

1. Reuse the two exact K20 path charges.
2. Evaluate the four frozen profile/weight groups at their new terminal tail
   degrees.  This covers 17 paths without row materialization.
3. Replay the four scalar-only K18 source components, signed-canonical-collect
   only pivotable K18 parents, and feed the resulting streams through one K2
   terminal evaluator.  This covers 16 paths.
4. Evaluate the direct `D20:444|R:direct` packet factorwise.
5. Add all group results over Q and require literal coverage equality with all
   36 DAG IDs for both full and irreducible charges.

This is smaller than reconstructing every path from K14: it reuses the exact
terminal profile interfaces where they are sufficient and reconstructs only
the four K18 components for which the archive retained scalars alone.

## Scope guards

- The raw `checkpoint_k17_*.bin` files are irreducible normals; they are not
  parent feeds for K20.
- The retracted incomplete K20 interface is neither a subtotal nor a coverage
  certificate.
- The direct `444` source is structurally available, but no exact K20 charge
  artifact exists for it yet.
- No K20 row generation, charge evaluation, or residual collection was run in
  this audit.

Replay with `python3 audit_k20_36_path_ledger.py`.
