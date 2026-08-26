# Decorated hidden-K16 H-action referee

## Verdict

**PASS on the bounded one-H-slice prefix.**  The decorated action, Generic's
orbit ledger, and Cycle's emitted K2 checkpoint agree exactly.  The 29-byte
coarse path profile is not a source-faithful replacement for this decorated
object.

## Exact action and mass formula

Let `A_p` be the four-cell anchor for pivot `p` and `T_p` its 12 K2 tails.
For `g in H`, define `rho_g(p)` uniquely by

```text
g A_p = A_{rho_g(p)}.
```

The decorated object is `d=(r,p)` with `A_p` dividing the literal parent row
`r`, and

```text
g.d = (g.r, rho_g(p)).
```

Thus `S_d={g:g.d=d}`, `|H.d|=384/|S_d|`.  The checker exhaustively verifies
for all `384*78*12 = 359,424` cases that `g T_p=T_{rho_g(p)}`.  Consequently

```text
E_p(r) = sum_{t in T_p} (r-A_p+t)
E_{rho_g(p)}(g.r) = g E_p(r).
```

For a decorated H-orbit `D` with total orbit mass `M_D`, let `S=S_d` act on
the 12 tails of a representative.  Each `S`-tail orbit `O` contributes
`M_D*|O|` to the H-orbit mass of its child.  Equivalently, emit all 12 tails
of the representative with mass `M_D` and H-canonicalize/aggregate the
children.  If a later checkpoint stores per-labelled coefficients, divide
the final child orbit mass by its child orbit size only after all signed
contributions have been merged; exact divisibility is required.

## Exact prefix comparison

- `1,054,592` labelled `(parent,p2)` uses aggregate to `261,696` decorated
  H-orbits with scaled signed mass `-2407088221087334400`.
- The independently reconstructed decorated map equals Generic's ledger in
  every key, weight, and use count.  Generic's exhaustive orbit census gives
  orbit size `384`, stabilizer size `1` for all `261,696`; the referee also
  recomputes orbit-stabilizer and the tail-orbit mass formula on 257
  deterministic representatives.
- Emitting `3,140,352 = 12*261,696` representative tails reproduces Cycle's
  `694,172` canonical K2 rows, weights, and pivotability flags exactly.
- Generic's coarse-profile guard is decisive: `59,970/62,678` coarse keys
  contain multiple decorated H-orbits, with maximum 48.  The coarse PKey may
  evaluate immediate cycle charge but cannot generate K2 rows source-faithfully.

Run `referee_decorated_h_action.rs` with features `hidden_child_prefix`,
`full_hidden_charge`, and `decorated_h_referee`.  No global K2 collection is
claimed.
