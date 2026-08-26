# Three restartable scalar-only K18 profile exporters

## Verdict

`PASS` for the bounded construction and prefix replay. One shared exact Rust exporter now covers the remaining scalar-only K18 parent streams

- `D14:222 | R:4-2` (one K20 path ID),
- `D15:{223,232,322} | R:3-2` (three IDs), and
- `D16:{224,233,242,323,332,422} | R:2-2` (six IDs).

No full export, cross-part merge, response evaluation, or K20 tail expansion was run.

## Exact shared interface

The common key is `profile[29] | anchor_signature[12] | outgoing_K2_pivot` (42 bytes).  Each 104-byte signed record also stores `i128 weight`, contribution count, and a reversible witness: the literal 24-cell K18 parent, source-record index, first pivot/tail, outgoing pivot, both averaging counts, and packet ID.  Scale is the certified universal `U=400591699200`; every observed `m1*m2` divides `U`.

Parts are locally sorted, locally coalesced, nonzero, and atomically renamed.  A source-range shard is authoritative only after its atomic manifest exists.  Orphan parts from an interrupted range are ignored and the range is rerun with a fresh prefix.  A later signed external merge is still required across parts/shards.

The verifier reverses the stored first tail to its K14/K15/K16 head; checks the literal source packet (including the exact K16 checkpoint row); recomputes both pivot sets, signature, profile key, denominators, ordering, counts, and signed sums.

## Frozen 50,000-parent crosschecks

All six statistics agree exactly with Tail's frozen prefix (generated, pivotable, outgoing uses, nonzero keys, signed weight, and the full `(m1,m2)` histogram):

| stream | generated | pivotable | outgoing uses | nonzero keys | signed scaled sum | kernel time |
|---|---:|---:|---:|---:|---:|---:|
| K14/K4 | 62,720 | 50,000 | 83,200 | 15,950 | -1,394,114,051,506,176,000 | 0.034766 s |
| K15/K3 | 119,102 | 50,000 | 134,048 | 18,219 | -900,060,686,725,939,200 | 0.048138 s |
| K16/K2 direct | 50,000 | 50,000 | 178,572 | 10,660 | -62,058,292,582,809,600 | 0.125337 s |

## Full-job planning bounds (not executed)

| stream | exact pivotable parents | exact hard outgoing-use bound | hard unmerged bytes at 104 B | prefix-ratio sorted-byte estimate | kernel-only linear wall estimate |
|---|---:|---:|---:|---:|---:|
| K14/K4 | 357,580,800 | 27,891,302,400 | 2,900,695,449,600 | 11,863,100,704 | 248.63 s |
| K15/K3 | 923,253,760 | 72,013,793,280 | 7,489,434,501,120 | 34,987,181,424 | 888.87 s |
| K16/K2 direct | 807,499,618 | 62,984,970,204 | 6,550,436,901,216 | 17,904,527,576 | 2,024.19 s |

The hard byte bounds are exact consequences of the frozen operation bounds but deliberately pessimistic (one unmerged record per use).  The sorted-byte and wall figures are planning extrapolations from the prefix; they exclude cross-part merge, filesystem throughput, hash validation, and cache degradation.  In particular, they are not runtime certificates or authorization to launch the full jobs.

## Replay

```sh
rustc -O -C overflow-checks=yes computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/export_k18_parent_profiles.rs -o /tmp/export_k18_parent_profiles
/tmp/export_k18_parent_profiles verify k14 computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/prefix_k14.part000000.bin
/tmp/export_k18_parent_profiles verify k15 computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/prefix_k15.part000000.bin
/tmp/export_k18_parent_profiles verify k16 computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/prefix_k16.part000000.bin
python3 computations/unaudited-codex-orbit0-k18-three-stream-exporters-2026-08-23/audit_exported_prefixes.py
```

Authoritative result: `results_three_stream_exporter_prefixes.json`, SHA256 `242d2a8ee8dee48256776fd99fdb71a7a5f338660cbda914296d71155a198e90`.  Exporter source SHA256 `adb7edbec6fb251ad55cc688183e3344f45fa45e5486c925e5edbbb0d9f0ebe9`.
