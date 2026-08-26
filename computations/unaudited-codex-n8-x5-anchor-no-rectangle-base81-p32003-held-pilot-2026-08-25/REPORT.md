# Held anchor/no-rectangle base81 p32003 pilot

Status: **PASS — READY HELD, ZERO RUNS**.

This package materializes only the smallest modular diagnostic from held plan SHA-256 `8c4c30693c21f01ded35272bfb154a1e312e085481a09c8a16c395d32a380d84`: the canonical 81-variable/6,561-generator anchor/no-rectangle ideal over `p=32003`. The source is exactly 420,125 bytes with SHA-256 `80495d946b3e3078a7538b4762e9151b612533cc2b1445269a1e24f30d3e5dc7`.

The source is reconstructed byte-for-byte from canonical Q source SHA-256 `25b25aac93a336c36c0299c5d6ee9b2a984b5ca0e644170ef235af92f01124f3` by changing only the unique ring coefficient field from `0` to `32003` and replacing the terminal `quit;` with frozen epilogue SHA-256 `4e89c111ad7d0f708bce7296a0d209507dede12b4a2ccfce78be184ccc790500`. The canonical source already prints input counts; the appended epilogue runs `slimgb(I)`, reduces `1`, and reports unit/nonunit status.

Runner SHA-256 `90b276285e87741b18f990eb94c4694379601fc1e6a65a4c6f186a2a6726ad8a` is one-shot and fail-closed. It pins Singular and `gtimeout`, uses direct Darwin `libproc` for the fresh process census and live process-group RSS, enforces native/wrapper/RSS gates of 180 s / 190 s / 8 GiB, writes logs and JSON atomically, refuses overwrite, and records no automatic relaunch, Q lane, or second lane.

No clearance, attempt directory, refusal record, result log, watchdog log, temporary file, or solver process has been created. A future launch requires a fresh clearance valid for at most 900 seconds that binds this package manifest plus an independent plan-audit result and manifest. Any failed preflight is a terminal zero-arithmetic refusal under `REFUSAL_SCHEMA.json`.

Scope is modular diagnosis only. Even a unit ideal over `p=32003` would require independent terminal audit and does not by itself prove exact-Q closure, records 12–15, or the full conjecture.
