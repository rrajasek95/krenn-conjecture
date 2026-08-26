# Rep5 guard-pivot k0 modular pilot — held zero-run package

This package materializes exactly the independently approved `rep5`, `p00`, guard-pivot `k=0` chart over `F_32003`: 88 variables and 6,574 generators. The source is the byte-exact Q input SHA `d4204428...` with the sole ring literal changed from `r=0` to `r=32003`; its resulting SHA is `dc04c722...` as predicted by the referee's held plan.

The single-use runner enforces a native 240-second wall, an internally pinned 250-second `gtimeout`, and an 8 GiB process-group RSS cap using direct `libproc` census and fail-closed per-member rusage. It creates the exclusive attempt marker before `popen`, refuses stale artifacts, and atomically records every caught terminal outcome.

This is a zero-run package. Independent acceptance and a fresh nonce/expiry/no-overlap clearance are absent and required. Exact Q, `k=1`, `k=2`, relaunch, parallel execution, and mathematical coverage are all forbidden here.
