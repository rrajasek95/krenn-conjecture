# Stage 15 failure seal

Verdict: **REJECT_NO_SPACE_DURING_ATOMIC_CACHE_WRITE**. The accepted continuation frontier remains stage 14, round 1442.

The frozen v4.1 solver ran from the accepted round-1442 checkpoint/cache under cold/rare, 16-worker hierarchical nonincremental mode, a 2,000,000-column cap, native wall 90 seconds, wrapper wall 115 seconds, and a 36 GiB RSS limit. Arithmetic messages reached round 1447 (1,970,322 columns, support 2,136), but the terminal write failed with `No space left on device (os error 28)`. No `result.json` was published. The newer checkpoint has no matching complete cache/result and is not an accepted state.

Pinned small evidence:

- `stderr.log`: 3,261 bytes, SHA-256 `6a968e4c2e4fe7176097652885e8dd9164e6e408c5eb8f80898be376ca3501c7`
- `stdout.log`: 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `watchdog.json`: 51,767 bytes, SHA-256 `6aa1ccb1851b831e83759435ad9ee5e35af3911f6e84c4208c533d9e67ca1f1f`
- watchdog: status FAIL, rc 2, 114.659502 seconds, peak RSS 24,576,880 KiB, 449 live samples, no RSS breach

The exact unaccepted large files safe to remove after this seal are `stage15/checkpoint.bin` (29,599,730 bytes, unmatched round-1447 state) and `stage15/vectors.bin` (4,221,170,622 bytes, redundant clone of the retained accepted round-1442 input). The failed `vectors.bin.tmp` partial was already removed during external storage recovery and was absent when this seal was written. Preserve the small logs, watchdog, and both failure-seal files.

A distinct relaunch must clone the accepted stage-14 checkpoint/cache with hashes `094c339af0be4684323f4d576b0b608d521da76bb44083b71c4c65a9425e4bdb` / `1fd9cd661feef3957c0dda310b3213ff11784a48c520b76d73323e950a9db7c1`. Require at least 12 GiB free before launch (16 GiB preferred): the replacement cache alone is approximately 4.3 GB, and atomic publication needs output plus input/metadata/log safety headroom.
