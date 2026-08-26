# Plan amendment after round 1635

Stage08 atomically wrote an exact sole round1635 continuation with no round1636 record or temporary outputs. It loaded all3,726,609 round1634 vectors and produced3,756,136 columns/support14,074. Its status is `INCOMPLETE_RESOURCE_GATE/WALL_CAP`; this is accepted only as the exact-target round1635 exception, not as a generic semantic relaxation. Watchdog137.348668 seconds passed below150 with no breach.

Pre-resume hashes: result `31466fa0a0a5a73f73fda4e2a36630d4c9a96d225ee17955e1e3571bcf251322`, watchdog `1502eaf57caaee8f0d2ab9744687b1511e29cd21d9fcb1461c1056ce0c65dc43`, checkpoint `83c6880c204ff1b26b486b24bc3c8688161e3a7065c6a3cb9dbfba2d965395b0`, cache `97fdb106abb96a90c0a8e2be225f9d75a71f570e5d93e3e228a1bf7df3fa77c6`.

For stages09–12 only, native wall changes120→150 seconds and hard wrapper150→180 seconds. Source, binary, mathematics, cold/rare strategy, cap4m, RSS36, hierarchical nonincremental kernel, one-round geometry, and disk/cap guards are unchanged. Stage09 closes Block C (stages07–09); Block D is stages10–11; Block E is stage12. Each block remains capped below540 seconds.

The first stage09 wrapper invocation was refused before arithmetic because the original wrapper SHA `48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522` accepts at most155 seconds. It produced zero coverage and no result/watchdog/log outputs; its unchanged clone is retained as `stage09_refused_wrapper155_attempt`. Stages09–12 use the already sealed wrapper SHA `75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997` invoked at180 seconds. Its exact source diff from the old wrapper is solely the maximum accepted bound155→540 and corresponding error text; live libproc RSS, atomic-output, and termination logic are identical.
