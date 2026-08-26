# Rep1 next-25 exact-Q schedule — held, zero runs

The strict selected group IDs are `11,12,14,16,...,37`: the 25 lowest
canonical IDs after excluding independently closed groups `0–10,13,15`. Each source
was regenerated from the sealed rep1 quotient generator and byte-matched to the
canonical census.

The held executor is single-use and sequential. Each lane has native/wrapper/RSS
limits `240s/250s/8GiB`, direct-libproc process-group RSS with fail-closed
observation, an internally enforced wrapper, and an atomic result. The whole batch
stops on the first nonunit, resource failure, process failure, or transcript
mismatch. Skip, reorder, retry, relaunch, and parallel execution are forbidden.

No acceptance, clearance, attempt, result, or solver process exists. The source
files are design artifacts only and carry no new mathematical coverage.
