# Rep5 k2/t1 smallest torus-chart modular held referee

Verdict: **PASS approved held / zero run**.  All 16 exact-Q torus sources
independently recount as 73 variables, 6,561 generators, 4,416,511 bytes, and
5,322,351 distributed syntax terms.  The frozen `(bytes, terms, SHA-256)` rule
therefore selects lexicographically smallest Q source `13c204f7...` with
assignment `yn1=yn2=t0=1,t2=0`.

The modular source `c36bd3b7...` is byte-for-byte the selected Q source after
one `0 -> 32003` ring replacement and replacement of its census-only `quit`
by the strong `slimgb/size/reduce(1,G)` epilogue.  It remains exactly
73/6,561.  No other body byte changed.

Runner `76ed5449...` has native/wrapper/RSS gates 240/255 seconds/8 GiB,
direct libproc process census and process-group RSS, exclusive pre-Popen attempt
consumption, atomic result publication, and strict one-lane/no-Q/no-other-chart/
no-relaunch fields.  Four independent mutations of wall, RSS, observer, and
atomic publication are rejected by the referee.  Acceptance and clearance
instances, attempts, results, locks, logs, and temporaries are all absent.

This approval remains **held only**.  It binds producer design manifest
`2b220f91...`, design referee `20f24c8d...`, and consumed open84 timeout referee
`0cb2ba30...`; the timeout is not reused.  It gives no mathematical coverage,
does not close the selected chart or any of the 16-cover, and does not itself
authorize a launch.
