# Round1262 internal sequential portfolio design audit

Status: `PASS_EXACT_INTERNAL_SEQUENTIAL_PORTFOLIO_DESIGN`.

The frozen command uses the accepted round1261 input and invokes the original `auto/best/tree` portfolio at period 1 with parallel evaluation disabled. Source inspection confirms that parallel and sequential modes construct the same ordered six tasks: repair then cold, each with first/last/rare pivots. The parallel branch joins handles in that same order; the sequential branch evaluates it directly. Both pass the resulting choices to the same stable key `(unseen frontier count, support count)`, so task order remains the exact tertiary tie-break.

The 520/540-second allowance is one bounded six-lane family gate, not six independent 120-second lane gates. The watchdog sibling changes only its maximum-time guard and matching message from 155 to 540; RSS, process-group termination, telemetry, and atomic-output logic are unchanged.

The two prior parallel attempts both ended at `WALL_CAP` with return code -15 and no result JSON. They therefore contribute zero accepted coverage. No large cache was read and no solve was launched by this audit.

This is a design PASS, not a production-result PASS. Acceptance still requires terminal resource telemetry, the exact round1262 result, selected fixed-lane replay, and cap-only byte equivalence.
