# The endpoint-hybrid row reduces all label packets to one decorated-anchor web

## Result

The 98 label-sensitive records left by `6597199` consist of 48 external
residual-q packets and 50 packets with `L=N` as physical matchings. The same
argument also applies to the 12 intervening strict-Hall records.

In all 110 records the physical endpoint ports are exactly

```text
M : P0,S1,
N : P2,S3,
L : P2,S3.
```

Thus `N` and the other-bright pure anchor `L` share the edge `e=S3`.
The selected mixed word is `d=rho+(1,2)`: its cell on `e` has labels
`(rho_3,2)`, whereas the pure-one anchor cell has labels `(1,1)`.

Checker:
`computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py`.

## First use the actual mixed word

Across the 48 q-only physical records there are `48*3^6=34,992` literal
choices of `rho`. The external cells of `N` split exactly as follows:

```text
some external q cell is offdiagonal: 27,540;
every external q cell is diagonal:    7,452.
```

The first class enters the pinned nonanchor-offdiagonal route. The diagonal
class is not promoted by graph incidence; it is the domain of the hybrid
argument below. By cycle and number of external N-edges the diagonal counts
are `2,430` for `(C6,1)`, `2,916` for `(C8,1)`, and `2,106` for `(C8,2)`.

## The literal hybrid row

Fix the selected nonzero cell `x_e^(rho_3,2)` from `N`. Form the word

```text
u(rho_3) = (1,1,1,rho_3,1,1,1,2)
```

in site order `0,1,2,3,4,5,P,S`. On the matching `L`, its edge `e` uses
the selected mixed cell and every other edge uses the selected pure-one
cell of `L`. Hence the `L` monomial in the zero target row `G_u` is nonzero.

Split the complete direct-free hafnian row into matchings retaining and
omitting `e`:

```text
G_u = x_e^(rho_3,2) H_e^1 + O_e = 0.                 (1)
```

There are 15 retaining matchings and 75 omitting matchings. If an additional
nonzero retaining matching `B' != L` occurs, replacing its common mixed edge
cell by the already selected pure cell `x_e^(1,1)` gives a nonzero pure-one
monomial on `B'`. Thus `B'` is an alternate pure target matching.

Equivalently, if the omitting sum `O_e` vanishes, (1) and the localized
mixed cell force `H_e^1=0`. The pure target equation is

```text
x_e^(1,1) H_e^1 + P_e = 1,
```

so `P_e` is nonzero and supplies a pure-one matching omitting `e`. After
reselecting that matching as `L`, the active N-edge `e` is external to all
three pure anchors and enters the endpoint-arm route. This argument is
coefficientwise and does not assume a single retaining term survives.

## Complete classification of an omitting mate

If `O_e` is nonzero, at least one literal omitting matching is nonzero. For
each of the 110 records, each of the three values of `rho_3`, and all 75
omitting matchings, the exact priority census is

```text
external endpoint arm:                 22,770;
crossed response ports P2,S1:             990;
external offdiagonal residual-q cell:     372;
M-port decorated-anchor residual:         618.
```

The first three are existing source-valid routes. The counts have a simple
structural explanation. If `S` is paired away from both `S3` and `S1`, its
hybrid cell is an external endpoint arm. With `S1` fixed, pairing `P` away
from `P0,P2` is again external, while `P2,S1` is crossed. Only `P0,S1`
remains. Its three residual perfect matchings either expose an offdiagonal
q-cell (when `rho_3 != 1`) or stay in the final web.

For `rho_3=1`, all 330 possible `P0,S1` tails remain in the final class.
For each of `rho_3=0,2`, 186 of the 330 expose an external offdiagonal
q-cell and 144 remain. The final 618 candidates split by source record as

```text
q-only:       58,144,58 for rho_3=0,1,2;
strict Hall:  18, 36,18;
L=N:          68,150,68.
```

## Exact remaining obligation

The canonical survivor is

```text
M = P0 | S1 | 23 | 45,
N = L = 01 | P2 | S3 | 45,
K = PS | 01 | 23 | 45,
B' = M,
u(0) = 11101112.
```

Its active hybrid monomial changes both decorated endpoint components on
the physical target skeleton `M`; in particular the required offdiagonal
`S1` cell lies on a selected anchor edge, not outside the anchor union.
Every external residual q-cell in this last class is diagonal in `u`.

Therefore the endpoint-hybrid theorem eliminates the need for a general
same-skeleton word-change theorem. The sharp remaining input is narrower:
a source-valid closure of this `P0,S1` decorated-anchor bistar web. The
existing terminal-transfer bistar audit explains why a nonlinear companion
correction may be needed; this note does not declare the final web empty.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py
python3 -O computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py
python3 -I -S computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py
```

Frozen ledger SHA-256:

```text
d0f33488f518ed2501bd4a6e7a955bf487e7984b9041870dc36bb67a3aba907a
```
