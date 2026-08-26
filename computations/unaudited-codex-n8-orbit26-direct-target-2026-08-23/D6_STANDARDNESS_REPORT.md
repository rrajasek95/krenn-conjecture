# Exact target standardness through homogeneous degree six

The lex-first transferred row

`0111202020494f4f50f8`

has encoded y-degree 10 and total degree 12, hence equals a y10 monomial
times `t^2`.  Its homogeneous degree-six divisors comprise 72 y6 rows, 82
y5*t rows, and 72 y4*t^2 rows.  The earlier t-free-only divisor check is
superseded.

The corrected literal census finds no incident y6 divisor, but it does find
156 source columns incident to 76 shorter divisors: 124 normalized-original
times degree-two columns and 32 redundant complete-d5 times degree-one
columns.  The latter add no rowspace, since every complete d5 cell is already
an explicit original-times-linear combination.

For the 108 incident original columns with a t-free y2 multiplier, exact
inverse incidence on their y6 leading rows closes to 790 columns and 50,179
rows in 79 components.  A deterministic private-row peel removes all 790
columns.  Thus the target-rooted y6 map is injective: no combination using a
column which touches a target y5*t or y4*t^2 divisor can cancel its y6 head.

The remaining y1*t slice is `t` times the completed degree-five module.  Its
direct target-rooted closure has 22 columns, 1,547 rows, exact rational rank
22, kernel zero, and no target pivot.  The y0*t^2 slice is `t^2` times the
original degree-four module.  Independently, none of the 6,558 original d4
leads and none of the 84,005 completed d5 leads divides the target.

Therefore no homogeneous degree-six initial monomial divides the target in
the frozen chart26 t-last order: the target is standard through total degree
six.  This is target-specific and says nothing yet about degree seven,
another term order, or another lower-degree right inverse.

Replay:

```text
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_y10_dead_row_complete_d6.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/solve_y10_d6_staged_blocks.py
```

Frozen logical digests:

- corrected homogeneous divisor census: `447409df3f67c76ef437937b3e041065adc83d96d6e90a35b091f8638b80d1b5`;
- staged standardness theorem: `62646275d6847e4f2044a337b6fcf23a37eda7368a57876a259b53d40f75c4db`.
