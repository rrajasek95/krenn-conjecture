# D12 r1641 cap4.75m/support200k promotion — HELD

Status: **HELD_AWAIT_INDEPENDENT_COLUMN_CAP_DIAGNOSTIC_AND_DESIGN_REFEREES_PLUS_MANAGER_CLEARANCE**. No clone, endpoint read, or candidate arithmetic has occurred.

The exact cap4.25m support200k lane is a clean exhaustion control: it returned `COLUMN_CAP` at unchanged r1640 with no round record, no temporary output, and checkpoint/cache still `12f79c86...` / `1d7ce92a...`. It has zero continuation coverage but proves the deterministic next set contains at least 180,290 new columns. The exact count and next support are not exposed.

The frozen column-cap source theorem (`1cab0b83...`) proves that the cap is read only for result serialization and a single pre-arithmetic whole-next-set guard. Enumeration and scoring happen before that guard, while invariant-column arithmetic happens afterward. Thus a fresh higher-cap candidate computes the identical deterministic set/provider mathematics; relative to the exhaustion control, its sole normalized command difference is the cap literal.

## Cap choice

The earlier 126,678 projection was censored by cap4.25 exhaustion. This design declares a new fail-closed resource policy, explicitly not a theorem: double the strict lower bound to cover 100% under-observation, then apply the existing 25% reserve. That gives `ceil(180290*2*1.25)=450725` new columns and minimum total cap 4,520,436.

- 4.5m has 430,289 headroom and misses the declared bound by 20,436, so it is rejected as underprovisioned.
- 4.75m has 680,289 headroom and clears the bound by 229,564; it is selected as the smallest requested passing cap.
- 5.0m clears it by 479,564 but is not minimal under the declared policy.

Cap4.75 itself does not allocate or change computation. At the present mean cache record size, even filling all cap headroom projects a 9.56GiB cache and 17.74GiB retained-input-plus-output footprint. The preclone floor is raised to 96GiB; design-time free space was 155,515,164KiB. These are storage projections, not frontier guarantees.

If both independent referees and the manager approve, exactly one fresh r1640 clone may run with cap4.75m, support200k, native210/wrapper240/RSS36, and frozen source/provider/cold/rare/hierarchical/16/nonincremental settings. Acceptance requires atomic `ROUND_CAP` at exactly r1641, no r1642, all 4,069,711 inherited records byte-identical, strict checkpoint descendant, and full replay target 1/zero failures. Another `COLUMN_CAP`, any `SUPPORT_CAP`, or resource breach is zero coverage and held fail-closed.
