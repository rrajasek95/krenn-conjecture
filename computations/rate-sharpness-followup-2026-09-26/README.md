# Rate follow-ups: exact supporting replay

**Status: research, awaiting independent audit.** This package supports the
[sharper rate argument](../../notes/rate-sharpness-followup-2026-09-26.md)
and [paired-hafnian application](../../notes/paired-hafnian-application-2026-09-26.md).
It does not extend the certified or Lean-verified proof spine.

The [illustrated guide](../../explainers/RATE-FOLLOWUPS.md) explains the results
at undergraduate level.

## Reproduce

From the repository root, using Python 3.10 or later and its standard library:

```sh
python3 computations/rate-sharpness-followup-2026-09-26/verify.py > /tmp/rate-followups.json
diff -u computations/rate-sharpness-followup-2026-09-26/results.json /tmp/rate-followups.json
python3 -O computations/rate-sharpness-followup-2026-09-26/verify.py > /tmp/rate-followups-optimized.json
diff -u /tmp/rate-followups.json /tmp/rate-followups-optimized.json
```

Both differences should be empty. Every pass/fail check uses exact integers,
rationals, or Gaussian rationals, and remains active under `-O`.

The checker imports arithmetic and source conventions from the preceding
quantitative packages and replays the existing positive matching cover.
Those are dependencies, not independent implementations. Their pinned hashes
are checked before use; the new receipt also records its own source and note
hashes. The frozen all-orders proof must retain its original hash.

## What is checked

| Component | Evidence |
|---|---|
| Even-color projection | All 243 four-site and 10,935 six-site matching/color assignments; every linear off-color term is removed. |
| Literal projection | Four exact sources, including a dense complex six-site source; matching expansion, unchanged pure amplitudes, and the quadratic remainder estimate. |
| Exponents and constants | Rational budget inequalities for the generic 6-, 8-, and 10-site constants and the refined six-site constants. |
| Positive certificate | All 3,375 ordered matching triples; coefficient 41/1440 and all 180 required mixed words. |
| Phase condition | All 729 output words of a dense complex source with rational unit phases; a cancellation example whose margin is zero. |
| Optimality example | Exact prism expansion with linear target and cubic error amplitudes. |
| Rejected shortcut | Complete classification of the 1,530 triples without a rainbow matching; 1,440 contradict the proposed shortcut. |
| Paired hafnians | Eight complex/equality examples with block sizes 2–5; sector expansion, spectral floors, sharpness, and inability to control diagonal entries. |

The arbitrary-size projection rule, analytic norm inequalities, and universal
rate/stability theorems are proved in the accompanying notes. Finite examples
do not establish those universal claims by themselves. This replay is neither
an independent audit nor a Lean proof.

## Numerical calibration

[calibration.csv](calibration.csv) evaluates the phase-controlled bound for
several fidelities and edge-phase tolerances. Regenerate it separately:

```sh
python3 computations/rate-sharpness-followup-2026-09-26/verify.py --calibration /tmp/rate-calibration.csv > /tmp/rate-followups.json
diff -u computations/rate-sharpness-followup-2026-09-26/calibration.csv /tmp/rate-calibration.csv
```

These display values use floating-point arithmetic; no acceptance check does.
The final column also uses the independent probability cap
\((243/256)^3/15\). Physical probabilities refer only to the previously
specified zero-displacement Gaussian model with exact number selection and
no ancillary modes. They are upper bounds, not attainable-rate claims.

The unrestricted six-site square-root law remains open. The external
application's qualitative inequality follows from prior literature; this
package makes no claim to a new unrelated conjecture resolution.
