# Independent direct r1464 cap-2.5m equivalence audit

Verdict: `PASS_EXACT_DIRECT_CAP2250_TO_CAP2500_EQUIVALENCE`.

The direct `cold/rare`, hierarchical, nonincremental control (`--column-cap 2250000`) and candidate (`--column-cap 2500000`) resumed the same sealed r1463 state. After output-directory normalization, the column-cap literal is the only command difference. Both produce byte-identical checkpoint and cache outputs at r1464: 2,054,273 columns, support 2,427, target coefficient 1, with 4,744 new columns.

The common checkpoint SHA-256 is `0191363f5da4b5b74945dd48a51954195200957996c5d3ff43c5242c37a7c64f`; the common cache SHA-256 is `9bb1b64f80def9014f0b031f4683da5bf00354b331cf2bc0541672ce02d67b29`. Both 120-second native / 150-second wrapper runs passed atomically; maximum elapsed time was 58.458481 seconds and maximum RSS was 23,890,368 KiB.

The producer's independent checker/result/report/manifest are pinned at `e2ca88e93e58b2a97440e26fc10391f35e4741ded01f98414c0a85f4dea28d4a`, `0bd1e6c30481e0bf69531bd819b78496ec230039b19db6aae1ef59995db465af`, `72f8ca2e39eadbad3f7910b66b901a19664cba42f35ede58d11cc9fe3387eb8f`, and `4439f24a65283ffdb3efded051bc0a07dc065634fea555c06367da1b3858e46b` respectively.

The separate external sequential portfolio attempt is not promoted. Its `repair/first` lane reached the 330-second wrapper wall cap, returned -15, emitted no result or frontier evidence, and contributed zero accepted coverage. This affects optimization selection only: it neither changes nor weakens the independently verified direct cold/rare cap equivalence. Portfolio selection remains deferred.

This package certifies the one-round r1463→r1464 cap equivalence only. It does not assert closure or any r1465 continuation.
