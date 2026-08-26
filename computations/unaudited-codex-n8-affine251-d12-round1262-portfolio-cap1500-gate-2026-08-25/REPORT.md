# Round 1262 portfolio and 1.5M cap gate: prepared and held

The observed final production metadata says round 1261 has 1,238,541 columns and support 1,065, leaving only 11,459 columns below the accepted 1.25M cap. Those values are not yet accepted as audit inputs: the independent Poincaré/round-1261 replay and chain seal remains the launch authority.

No checkpoint/cache hashing, cloning, or solve was performed. `freeze_poincare_pins.py` contains a deliberate `WAIT_FOR_POINCARE_FINAL_REPLAY_CLEAR` manifest-hash interlock and cannot create launch pins until that exact hash is patched after the seal.

Once cleared, the runner performs one six-way auto/best tree round to 1262, one fixed replay of the selected strategy/pivot, and only if cold/rare wins, one additional fixed replay with `--column-cap 1500000`. Its 1.25M control and 1.5M candidate must differ at exactly that normalized command argument and produce byte-identical checkpoint/cache state. Each run has its own 120-second/36-GiB watchdog. Production source and state remain untouched.

The first cleared six-way attempt reached the 120-second watchdog and was terminated at 123.374 seconds, peak 18,476,512 KiB. It produced no `result.json`; the cloned checkpoint/cache rehash to the accepted input hashes. No fixed or cap run launched. This failure is preserved in `portfolio_failed120/` and `FAILURE_AUDIT.json`.

The retry changes only the portfolio output directory and time geometry: native 110→145 seconds, watchdog 120→155 seconds, with the same six choices, round/cap, engine, and 36-GiB bound. Fixed and cap-only replays remain at native 110/watchdog 120. `RETRY_ACCEPTANCE.json` freezes these differences before relaunch.

Status: `FIRST_PORTFOLIO_FAIL_CLOSED_RETRY155_FROZEN`.
