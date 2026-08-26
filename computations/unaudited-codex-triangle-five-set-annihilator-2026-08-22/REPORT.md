# Universal five-set annihilator on a triangle carrier

Status: **UNAUDITED exact theorem and hostile source replay**.  No broad
solve was attempted.

## Outcome

The star simplification does not extend to triangles.  For a triangle
carrier, the universal five-set annihilator kills all 45 one-crossing
matchings, and `ker L_triangle` kills 54 of the 60 three-crossing matchings.
The remaining six terms are exactly one omitted triangle-edge response.

For each triangle vertex `t`, normalized `X5` forces the exact identity

```text
Theta_(t,beta)(R_(T\{t})(K))
    = sum_c delta(beta)_c K_cc e_c,                        (1)
```

for every `K in ker L_triangle` and every internal five-set annihilator
`beta`.  Consequently at least one diagonal blocker belongs to the row span
only **after adjoining the nine response rows on the opposite triangle
edge**.  No blocker is forced into `rowspan L_triangle` itself.

A literal source guard has `L_triangle=0`, `K=I_3`, all four blocker
functionals outside the row span, and a nonzero opposite-edge response which
satisfies the contracted target identity (1).  Thus the five-set theorem
alone does not make any of the 560 triangle clauses automatic.

## 1. Canonical carrier and the three five-sets

Fix

```text
cap pair p,q,
residual triangle T={t0,t1,t2},
outside residual triple O={o0,o1,o2}.
```

The literal triangle matrix `L_T(A)` has nine rows for each of the twelve
residual edges not internal to `T`, hence size `108x9`.  Its kernel consists
of cap matrices whose response is supported on the three edges of `T`.

For one `t in T`, put

```text
W_t=(T\{t}) union O,              |W_t|=5,
C_t={p,q,t},                      |C_t|=3,
{x,y}=T\{t}.
```

The certified universal five-set theorem supplies

```text
beta in ker B_(W_t),
b=delta_(W_t)(beta) !=0.                                (2)
```

Repeat independently for all three choices of `t`.

## 2. Complete matching-sector contraction

Contract `Phi_8(A)` by `K` on `p,q` and by `beta` on `W_t`, leaving the
colour slot at `t` exposed.  Relative to the `3|5` cut, all 105 perfect
matchings have one or three crossing edges:

```text
T1: 45 matchings,
T3: 60 matchings.                                        (3)
```

### One crossing: all 45 terms vanish

The unique exposed site `u in W_t` leaves the complete four-site internal
cofactor `h_u` on `W_t\{u}`.  Hence every one-crossing block factors through

```text
beta(V_u tensor h_u)=0.
```

This kills `T1` cofactor by cofactor, including the sector in which `p,q`
are matched directly.  In particular, the direct functional
`<K,A_pq>` does not survive this contraction.

### Three crossings: 54 killed, six survive

A three-crossing matching leaves one internal edge `ab` of `W_t`; the other
three sites receive `t,p,q`.  Grouping the two assignments of `p,q` gives
one literal response row.

If the two `p,q` endpoints are not both in `T`, that response edge is one of
the twelve edges represented in `L_T`, and `K in ker L_T` kills it.  Exactly
54 three-crossing matchings vanish this way.

The sole unrepresented response pair is `{x,y}=T\{t}`.  Its surviving terms
are

```text
3 choices of the O-site matched to t
  times
2 assignments of p,q to x,y
=6 source matchings.                                     (4)
```

Let

```text
G_(t,O)=H_({t} union O)(A) in V_t tensor V_O
```

be the literal four-site matching tensor, and define

```text
Theta_(t,beta)(Z)
  =(id_(V_t) tensor beta)(G_(t,O) tensor Z),
  Z in V_x tensor V_y,                                   (5)
```

with named slots restored.  The six terms (4) are exactly

```text
Theta_(t,beta)(R_xy(K)).                                  (6)
```

The checker verifies the endpoint-ordered two-summand response formula on
every source label.  Swapping the residual colours in its crossed summand is
a hostile failure.

## 3. Target comparison and augmented-row identity

On normalized `X5`, `Phi_8(A)=Delta_8`.  The target contraction is

```text
sum_(c=0)^2 b_c K_cc e_c^(t).                             (7)
```

Equating (6) and (7) proves (1).

For a fixed output coordinate `c`, (1) says that the following functional of
`K` vanishes on `ker L_T`:

```text
b_c ell_c - (the c-th row of Theta_(t,beta) composed R_xy).
```

Therefore

```text
b_c ell_c - Theta_(t,beta,c) R_xy in rowspan L_T.          (8)
```

Choose a `c` with `b_c!=0`.  Then

```text
ell_c in rowspan [L_T ; R_xy].                            (9)
```

This is the strongest unconditional blocker statement supplied by the
five-set theorem.  Cyclically, for every one of the three triangle edges,
some diagonal blocker lies in the row span after adjoining that edge's nine
rows.

If a triangle carrier is unblocked, (9) implies that the restriction of
every triangle-edge response to `ker L_T` is nonzero.  Thus any active
triangle witness on normalized `X5` must use all three triangle edges; a
proper star-supported response has already been excluded by the star
five-set theorem.

## 4. Literal hostile source

Take the canonical labels

```text
p=6, q=7, T={0,1,2}, O={3,4,5}, t=0,
```

and set, in requested endpoint order,

```text
A_61=I3,  A_72=I3,  A_03=E00,  A_45=E00,  A_67=I3,
all other blocks zero,
K=I3.                                                     (10)
```

Then:

1. all 108 rows of `L_T` are zero, because the only nonzero response edge
   is the omitted triangle edge `12`;
2. `R_12(K)=I3`;
3. every internal four-site cofactor on
   `W_0={1,2,3,4,5}` is zero, so evaluation at the word `00000` is a valid
   `beta in ker B_W` with `delta(beta)=e_0`;
4. the contracted source tensor is exactly `e_0`, equal to the contracted
   target projection in (7);
5. `K_00,K_11,K_22` and `<K,A_67>=3` are all nonzero functionals while
   `rowspan L_T=0`.

Thus (1) and the universal annihilator are compatible with a genuinely
active triangle carrier.  This source is deliberately not a normalized
`X5` source; it is a source-faithful counterguard showing that the contracted
identity itself cannot be strengthened by formally discarding the surviving
opposite-edge term.

## 5. No new direct cap-error equation

The identity is linear in one response edge.  The direct pair term occurs in
the one-crossing sector and is annihilated with the rest of `T1`, so neither
`<K,A_pq>` nor a new direct-block condition appears in (1).

Moreover a response supported on a residual triangle already has matching
number at most one.  Its squarefree `r^2` and `r^3` cap-error terms vanish for
the usual support reason.  Equation (1) does not add a separate cap-error
constraint; it explains how the pure target is routed through the one
triangle edge omitted by the five-set cut.

Therefore the reduced singular incidence target remains

```text
full normalized X5
+ reduced real normal-cone condition
+ 64 least-block Gram normal equations
+ balance
+ all 560 triangle blocker Gram clauses.                  (11)
```

The new augmented identities (8)--(9) are exact additional relations inside
that target, but they do not remove a triangle selector.  The smallest next
triangle-specific target is to combine the three cyclic augmented identities
with the simultaneous full-`X5` rows; treating one five-set in isolation is
terminal.

## Replay

```sh
python3 computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/audit_triangle_five_set_annihilator.py --write-results
python3 -O computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/audit_triangle_five_set_annihilator.py
python3 -I -S computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/audit_triangle_five_set_annihilator.py
```

The hostile `--mutate-crossed-orientation` run must fail.  The standard run
returns logical SHA-256
`c5156bea2cc1ba3a78209cfa10e464e92de17a9e79032f393babebdb8bc7169c`.
