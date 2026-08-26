# Rep1 next10 exact-Q held-schedule referee

Status: **PASS — strict held schedule approved, zero runs**.

The selected group IDs are exactly 1 through 10 in ascending order; already closed groups 0, 13, and 15 are excluded. All ten canonical charts, source sizes, and source hashes match the sealed 162-group census, and every source independently parses as 91 variables and 6,577 generators.

Runner `810ba01d...` is sequential and single-use, invokes pinned `gtimeout` internally, sums fail-closed direct-libproc process-group RSS, enforces 240/250 seconds and 8 GiB per lane, writes each result atomically, and stops the whole batch on the first nonunit/resource/process/transcript failure. Prefix assertions prohibit skip/reorder; the durable batch marker prohibits relaunch and only one Popen site exists.

No acceptance, clearance, batch marker, result directory, temporary, solver run, skip, parallel lane, or relaunch exists. The included acceptance enables only later explicit manager clearance; this audit launches nothing.
