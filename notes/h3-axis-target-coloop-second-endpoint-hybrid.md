# The symmetric endpoint hybrid leaves one two-edge return

## Result

The first endpoint-hybrid theorem leaves 618 possible cancellation terms.
Every one uses the physical endpoint ports `P0,S1` of the pure-2 target
anchor `M`. Its active cell on `P0` is `P0:11`, whereas the selected pure-2
cell is `P0:22`.

Use `P0:11` and the three pure-2 cells of `M` off `P0`. They form a nonzero
literal monomial in the mixed zero row

```text
u = 12222212
```

in site order `0,1,2,3,4,5,P,S`.

Checker:
`computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py`.

## Aggregate factor/reselection dichotomy

Split the complete direct-free row at `e=P0`:

```text
G_12222212 = x_e^11 H_e^2 + O_e = 0.               (1)
```

If `O_e=0`, the localized active cell forces `H_e^2=0`. Expanding the
normalized pure-2 target then forces a pure-2 matching `M'` omitting `P0`.
After reselecting `M'`, the already active `P0` arm of the first-hybrid mate
is external to `K,L,M'` and enters the endpoint-arm route.

If `O_e` is nonzero, some literal matching omitting `P0` is nonzero. The
word gives its new P-edge labels `12`. The selected P-edges are only
`P0` in `M`, `PS` in `K`, and `P2` in `L`; `PS:12` is forbidden by the
direct normalization.

## Exact complete-row census

For each of the 618 first-hybrid residual terms, the row has 15 matchings
retaining `P0` and 75 omitting it. The latter split exactly as

```text
external endpoint arm: 42,642;
crossed ports P2,S1:     1,854;
external offdiagonal q:  1,002;
two-edge return P2,S3:     852.
```

The endpoint counts are forced per residual: 69 external, three crossed,
and three candidates with ports `P2,S3`. In the last group, a residual edge
incident with site 0 carries labels `12`; if that edge is outside the pure
anchor union it enters the offdiagonal-q route. Only 852 candidates retain
the two-edge return after this label check.

The 618 source residuals split as `260` q-only, `72` strict-Hall, and `286`
same-skeleton candidates after retaining the actual `rho_3` labels. Hence
the final two-edge return count is respectively `320`, `144`, and `388`.

## The sole remaining word packet

Every return term has endpoint cells

```text
P2:12,
S3:22,
```

on the endpoint skeleton of the other-bright anchor `L`. Its two residual
edges carry the pure-2 word except for the single site-0 label `1`. The
canonical return is

```text
M = P0 | S1 | 23 | 45,
N = L = 01 | P2 | S3 | 45,
K = PS | 01 | 23 | 45,
second mate = 01 | P2 | S3 | 45.
```

Thus the symmetric hybrid removes the arbitrary decorated-anchor web. The
only remaining theorem is a source-typed two-edge companion/recurrence for
this `P2:12,S3:22` return. This note does not identify that return with an
existing strict-K2,2 unit without checking its complete companion rows.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py
python3 -O computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py
python3 -I -S computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py
```

Frozen ledger SHA-256:

```text
1e5415e20eaed90c971a6d5b4ec6bfcee50f695ac1bcc874f6f9e388fce50074
```
