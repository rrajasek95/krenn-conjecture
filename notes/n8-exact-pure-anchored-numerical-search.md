# Exact-pure anchored numerical search at N=8

Date: 2026-08-08.

Research evidence only.  A failed numerical search proves nothing, and a
floating-point candidate would still require exact reconstruction and a
separate audit of all 6,561 output coefficients.

## Outcome

The unrestricted optimizer can lose one or two pure target coefficients and
settle at raw loss `0.5` or `1.0`.  The anchored search removes that artifact:
one diagonal entry in each colour is solved rationally from its pure hafnian
equation, so all three pure coefficients remain one throughout optimization.
The analytic gradient includes the implicit derivatives of those three
entries and is independently checked in real and complex modes.

The first complex campaigns found no finite candidate.  When the 249 free
complex entries were bounded coordinatewise by four but the three eliminated
entries were allowed to move, all eight starts escaped by sending an
eliminated entry to magnitude 41--55.  Their mixed residual maxima were only
`0.00382`--`0.00548`, with source norms 51--69.  Imposing a strong soft
modulus cap four on the eliminated entries stopped that escape; the first
compact runs instead stalled with mixed residual maxima `0.0247` and
`0.0341`, source norms about eight, and all three pure residuals below
`7e-16`.  This is the expected border signature, not a proof of emptiness.

## Rational anchor chart

For each colour `i`, choose one diagonal pivot entry `p_i`.  Its pure
coefficient is affine in that entry:

\[
                         H_i=p_i C_i+R_i.
\]

On the chart `C_i != 0`, install

\[
                         p_i=(1-R_i)/C_i.
\]

For any other complex source coordinate `x`, implicit differentiation gives

\[
                 \frac{\partial p_i}{\partial x}
                 =-\frac{\partial H_i/\partial x}{C_i}.
\]

The search applies this chain rule to the exact 105-matching adjoint, then
optimizes only the 6,558 mixed residuals.  A small cofactor guard excludes the
rational chart boundary.  Free real and imaginary coordinates can be hard
bounded; the eliminated pivots use a separately reported soft modulus cap
and penalty.

## Reproduction

The analytic/implicit-gradient audit is:

```text
.venv/bin/python computations/verify_n8_full_complex_anchored_search.py
.venv/bin/python -O computations/verify_n8_full_complex_anchored_search.py
```

Representative campaigns are:

```text
.venv/bin/python computations/search_n8_full_complex_anchored.py \
  --seed 13000 --starts 4 --maxiter 1400 --entry-bound 4 \
  --l2-penalty 1e-8 --candidate-threshold 1e-9

.venv/bin/python computations/search_n8_full_complex_anchored.py \
  --seed 13100 --starts 4 --maxiter 1400 --entry-bound 4 \
  --border-start --border-t 0.3 --noise 0.03 \
  --l2-penalty 1e-8 --candidate-threshold 1e-9

.venv/bin/python computations/search_n8_full_complex_anchored.py \
  --seed 13200 --starts 2 --maxiter 1200 --entry-bound 4 \
  --pivot-bound 4 --pivot-bound-penalty 10000 \
  --l2-penalty 1e-8 --candidate-threshold 1e-9
```

The program archives a candidate only when its unpenalized maximum mixed
residual passes the requested threshold.  No archive was produced in the
campaign above.
