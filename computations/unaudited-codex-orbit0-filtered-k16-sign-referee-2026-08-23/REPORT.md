# Exact sign referee for the frozen K16 response

## Result

The frozen `1,848,174`-orbit K16 artifact has the opposite sign from the
post-reduction residual of the stated telescope.  It remains exact and useful,
but must be interpreted as the K2 tail of the source correction (equivalently
source-minus-target), not as the residual after subtracting that correction.

The exact telescope is

```text
t0*t1*t2 + E0*E1*E2
  = H0*t1*t2 - E0*H1*t2 + E0*E1*H2.
```

With `R=T-S`, the current leading residual is therefore
`P=-R8'*E0_2*E1_2*E2_2`.  If a literal head has coefficient `-r`, subtracting
the source coefficient `-r` times `H=head+tails` cancels the head and leaves
`+r*tails`.  The frozen collector instead records `-r*tails`.

The lex-first replay makes the sign visible without abstraction:

```text
K14 row: 000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3
pivot word: 22220000
current head coefficient: -1
source coefficient: -1
head after P - source: 0
correct first K2-tail contribution: +1
collector contribution: -1
```

The mismatch is uniform term-by-term, so collection and removal of pivotable
K16 rows preserve it.  Hence the actual combined K16 bucket is

```text
direct K16 seed - stored frozen response,
```

not direct seed plus the stored response.

Replay:

```text
python3 computations/unaudited-codex-orbit0-filtered-k16-sign-referee-2026-08-23/audit_filtered_k16_sign.py --write-results
```

Logical digest:
`6a50fc3eb47a57c390b00e73ed0d32292a9ceb049844168381e30fd93acdc740`.
