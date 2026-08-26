# D611-open Hafnian contraction audit

Status: **exact obstruction PASS**.  The audited twelve 611 equations do not
define a closed quadratic self-map on the twelve selected tail variables.

For `uv in {a6,a7:0<=a<6}`, the literal equation is

```text
h2_uv*T01_uv
 + sum A_ub[0,2] A_vc[1,2] Haf4(G2 without u,v,b,c) = 0.
```

After inverting only the twelve audited `h2_uv`, it gives
`T01_uv=-Q_uv/h2_uv`.  Every quadratic factor belongs to the external `02`
and `12` channels; none is one of the twelve selected `01` cells.  Thus this
is twelve coordinate functions in the 156-variable boundary.  If `T` means
all 168 cross-colour cells, twelve equations still do not define a fixed
point map.

## Exact contractions

The source-symbolic Hafnian identities replay termwise:

```text
sum_e g_e h_e = 4H
sum_g g d_g P1 = 3P1,       sum_X X d_X P1 = P1
sum_g g d_g P2 = 2P2,       sum_X X d_X P2 = sum_Y Y d_Y P2 = P2
sum_(f disjoint e) g_f h_ef = 3h_e.
```

Here `P1` and the ordered `P2` have respectively 420 and 1,260 literal
terms.  Restricting Euler to the twelve selected physical edges produces a
boundary term, not a scalar multiple of `H`: the selected incidence is zero
on the 15 matchings containing `67`, and two on the other 90.

The literal 71 contraction is likewise boundary-valued.  After substituting
the two selected tail coordinates at residual site `a`,

```text
sum_(t=6,7) (h^j_at/h^k_at) Q^k_at
  = sum_(b<6,b!=a) h^j_ab A_ab[i,j].
```

The right side contains residual cross-colour cells, so this is a six-vector
identity rather than a zero scalar invariant.

For the canonical 332 row `F_00011212`, eliminating its three selected
linear tail terms leaves six independent degree-one boundary variables:

```text
a_03_01, a_04_01, a_13_01, a_14_01, a_23_01, a_24_01.
```

Hence the 360 rows do not source-symbolically collapse to an invariant in
the twelve selected coordinates.

## Exact counterexample to the partial contraction

Over `Q(lambda)/(105 lambda^4-1)`, set every diagonal cell to `lambda` and

```text
a_01_02 = a_67_12 = 1,
a_06_01 = -1/(5 lambda),
a_01_01 = a_67_10 = 1/(5 lambda),
```

with all other cross cells zero.  Then all three pure Hafnians equal one,
all twelve `D611` factors equal `15 lambda^3`, the twelve 611 rows vanish,
and the eight selected 71 rows vanish.  The point is nonzero.  The 332 packet
detects it: 138 of 360 rows are nonzero, with
`F_00011212=-lambda^2/5`.

This is not an X5 counterexample.  It proves precisely that pure+611+71 and
Euler contraction do not kill the remote branch; closure must retain the
full boundary-valued 332 equations.

## Replay

```sh
.venv/bin/python computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/audit_tail_remote_hafnian_contraction.py --write-results
.venv/bin/python -O computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/audit_tail_remote_hafnian_contraction.py --write-results
.venv/bin/python -I -S computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/audit_tail_remote_hafnian_contraction.py --write-results
```

