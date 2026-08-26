# K14/K4 atomic-part cleanup

After Cycle's independent validation (`logical 3347cf43`), all 490 K14/K4
atomic sorted source parts were rehashed against
`results_k14_k4_full_replay.json`.  Every hash matched.  Exactly
**12,564,507,832 bytes** were then removed, scoped only to
`k14_*.part*.bin` in this directory.

The merged profile checkpoint, merger/evaluator/checker sources, manifests,
results, replay ledger, and main report remain.  Post-delete replay confirms
the merged checkpoint SHA is still
`5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f`
and all four pinned report/result hashes remain unchanged.

The removed parts are not locally recoverable, but they are deterministically
regenerable: run the pinned exporter source (SHA prefix `adb7edbe`) over the
16 recorded source ranges into fresh prefixes, then rerun
`merge_k14_profiles.rs`.  The retained 490-entry replay manifest supplies the
expected per-part hashes.
