# Round 1464 external sequential v2 failure

The fresh `repair/first` lane failed closed at the 330-second wrapper wall
limit: elapsed 331.124102 seconds, peak RSS 27,875,808 KiB, return code -15.
It emitted no result, frontier score, or lane evidence.  Consequently none of
the other five tasks, the fixed replay, or the cap-2.5m candidate ran, and the
attempt supplies zero accepted portfolio coverage.

The v2 design manifest is `2455a76d...`; the watchdog pins the expected source
`2cf62905...` and binary `ade47c27...`.  The cloned checkpoint/cache retain the
sealed input sizes and mtimes, but this audit deliberately makes no byte-hash
claim about those large failure remnants.  No state at round 1464 was accepted.

Verdict: the explicitly authorized 300-native/330-wrapper geometry is not
sufficient for this lane.  Further widening or a different portfolio design
requires new authority.
