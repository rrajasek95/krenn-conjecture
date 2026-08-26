# Independent D12 round-1563 direct cap-equivalence audit

Status: `PASS_EXACT_DIRECT_CAP2750_TO_CAP3000_EQUIVALENCE`.

The control cap 2,750,000 and candidate cap 3,000,000 runs used the same
audited round-1562 input and differ only in the column-cap command value. Their
round-1563 semantic result and selected cold/rare round record are identical.
Both produced 2,691,509 columns with support 4,175, and their checkpoint and
vector-cache outputs are byte-identical: checkpoint SHA-256
`a21b5b592b5443504acc2a8625f482f6ae052cb990105bd36a7a877ae188a1fd`
and cache SHA-256
`06d202cf07a189090ae1d91298f10bcac8bcc384ea4052415c7fd4a5724445e1`.

Both watchdogs passed atomically. The maximum wall time was 76.540295 seconds
and maximum RSS was 24,797,616 KiB, within the predeclared 150-second and
36-GiB bounds. No dual output exists. The accepted resumable branch is
`candidate_cap3000`; no continuation beyond round 1563 is claimed here.
