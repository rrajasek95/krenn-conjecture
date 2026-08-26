# Rep4 all-equal-y modular pilot — held, zero launch

Status: **PASS_HELD_ZERO_LAUNCH**. This package materializes exactly one
rep4-localized `F_32003` input with 91 variables and 6,577 generators and a
refusal-by-default runner. No Singular process, ideal run, clearance, result,
second chart, exact-Q lane, or relaunch belongs to this seal.

The modular source is mechanically and uniquely derived from the independently
refereed rep4 Q source by changing `ring r=0,` to `ring r=32003,` and replacing
the terminal `quit` with one `slimgb`/`reduce(1)` status epilogue. It byte-matches
the referee plan's expected SHA-256 `9471d6bb...`. The support, stored-edge
orientations, carrier `A06^T*K*[A23^T|A35]`, and 91/6,577 counts are rep4-specific;
no cross-representative equivalence is used.

The direct-libproc runner measures the whole isolated process group, writes only
an atomic fresh result, and refuses before `Popen` unless the pinned referee plan
and a strict new manager clearance are both present. The requested 180/195-second
limits tighten the referee plan's 240/255 limits; the 8 GiB cap is unchanged.
Every possible outcome remains diagnostic only.
