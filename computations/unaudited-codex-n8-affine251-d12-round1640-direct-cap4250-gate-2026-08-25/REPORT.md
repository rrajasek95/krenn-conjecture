# Held round-1640 direct cap-4.0m to cap-4.25m gate

Status: `HOLD_AWAIT_INDEPENDENT_R1639_AUDIT_AND_POST_AUDIT_COMPACTION`.
No clone, large endpoint read, or arithmetic was performed.

The proposed gate uses sequential fresh clones of the independently audited
round-1639 endpoint. The cap-4.0m control must finish exactly round 1640 with
`ROUND_CAP` before the cap-4.25m candidate is permitted to launch. Promotion
requires byte-identical checkpoints and caches, equal semantic fields, and only
the normalized cap literal differing in results and commands.

There is a material projected blocker. The endpoint has only 31,631 columns of
4.0m headroom, while round 1639 added 66,458. The frozen source checks whether
the complete next incident set exceeds the cap before doing column arithmetic;
therefore control/candidate byte equality is possible only if the exact next set
has at most 31,631 columns. This is not known without the held control. If the
control reports `COLUMN_CAP`, the candidate must not launch and no equivalence
claim is allowed.

After independent audit and authorized compaction, the measured prelaunch free
space must be at least `88,080,384 KiB`. If the exact gate unexpectedly passes,
cap-4.25m leaves at least 250,000 columns of headroom; a conservative 100,000
per-round bound permits only rounds 1641 and 1642 before another hold. This is a
geometry estimate, not continuation authorization.
