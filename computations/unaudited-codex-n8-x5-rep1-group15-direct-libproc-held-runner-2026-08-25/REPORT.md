# Held rep1 group15 direct-libproc runner

Status: **MATERIALIZED AND SEALED; NOT LAUNCHED.**

The canonical group15 Q source is materialized atomically at 1,841,468 bytes and SHA `1611c16c73323e7a85ee730ba055f9f2092873841698e8fcc4f5799571ccab04`. The one-shot runner is pinned to plan `e778f68f...` and independent approval manifest `b1714d0a...`.

The runner contains no external process-listing command. It performs its fresh census with Darwin libproc `proc_listpids`/`proc_pidpath`, observes process-group RSS with `PROC_PIDTASKINFO`, and enforces native 240 seconds, wrapper 250 seconds, and 8 GiB. Attempt source, logs, watchdog, and result are atomic and refuse overwrite. Every terminal outcome consumes the one-shot attempt; no relaunch, second lane, group17, or group25 path exists.

`FRESH_CLEARANCE.json` is deliberately absent. A future launch requires a fresh record conforming to `FRESH_CLEARANCE.schema.json`, bound to the held-runner manifest, current plan/referee pins, a unique nonce, and a validity window no longer than 15 minutes.
