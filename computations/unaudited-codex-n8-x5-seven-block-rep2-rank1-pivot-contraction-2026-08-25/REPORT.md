# Representative 2 rank-one pivot contraction

Status: `PASS_EXACT_LOCALIZED_EQUIVALENT_CONTRACTION`.

## Lemma

Work over any field in the exact representative-2 rank-one branch.  Write
`A57=u v^T` and put `w=A26 v`, so the pinned stored-edge guard becomes

```
A06 v = 0,       A17 w = v,       A56 = -u w^T.
```

For rank one, `u` and `v` are nonzero; `A17 w=v` also forces `w` nonzero.
Choose nonzero coordinates `u_r`, `v_s`, and `w_t`, use the rank-one gauge to
set `u_r=1`, and localize with `q v_s=1` and `zeta w_t=1`.  Then the six guard
equations solve uniquely for six source entries:

```
a06_i,s = -q sum_{j != s} a06_i,j v_j,
a17_i,t =  zeta (v_i - sum_{j != t} a17_i,j w_j).
```

Indeed, after substitution the two guard rows are respectively
`-S_i(q v_s-1)` and `-T_i(zeta w_t-1)`.  Thus quotienting by the six guards is
isomorphic to substituting the displayed entries in the localized ring.  This
is an **equivalent contraction**, not a sufficient-subset shortcut.

After fixing failed colour 0, its stabilizer swaps colours 1 and 2.  The 27
raw triples `(r,s,t)` form exactly 14 stabilizer orbits, replayed exhaustively
by the verifier.  Hence the charts cover the entire rank-one locus.  The
rank-zero locus was already closed by the pinned cap67 structural argument.

## Size reduction and scope

For cap45/star1 each exact chart has 98 variables and 6,578 equations; for
cap03/star6 it has 100 variables and 6,578 equations.  Each retains every one
of the 6,561 full-X5 amplitudes, all nine adjoint equations, all six incidence
equations, and two inverse equations.  Relative to the prior localized gate,
six source variables and six guards disappear while two localizers are kept.

This does not prove the reduced ideals are unit.  The first remaining
obligation is exactly to prove every reduced chart empty (for either named
incidence failure) or produce a chart point.  Guard algebra alone yields no
further contradiction: the incidence equations contain independent blocks
`A04,A35,A23` and require the full-X5 amplitudes for closure.
