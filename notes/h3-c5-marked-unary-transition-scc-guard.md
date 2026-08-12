# Marked C5 unary propagation has five closed reset-word components

## Result

The complete marked unary rows do not propagate a normalized off-cycle tail
to its desired bright spoke or to an endpoint-visible response coefficient.
Keeping literal output words and decorated matchings, their transition graph
is

```text
75 vertices = 5 reset words * 15 six-site perfect matchings,
5 strongly connected components, each of size 15,
no edge between distinct reset words.
```

Relative to the ten off-cycle base occurrences, the exact 140 transitions
are the pinned

```text
20 same-reset changed tails,
40 translated C4 terms,
80 translated C6 terms.
```

Re-pivoting on a mate supplies no additional row: all fifteen terms are in
the same complete unary coefficient.  Thus repeated unary propagation stays
in one closed reset-word component.

Checker:
`computations/verify_h3_c5_marked_unary_transition_scc_guard.py`.

## Source labels and the invariant

Let `m=12112` on the odd sites `D={1,...,5}` and let `x=0`.  For reset site
`v`, the marked complete unary output word is

\[
 w_v(x)=w_v(v)=0,\qquad w_v(i)=m_i\quad(i\ne v).       \tag{1}
\]

Every transition is a pair of literal decorated matching monomials in the
single coefficient `U[w_v]`.  The checker records for each transition:

* the source row and full output word;
* reset site;
* source and destination physical matchings and all edge decorations;
* same-reset/C4/C6 type;
* zero GHZ-target readout; and
* the fact that no endpoint-response or augmented ordinary-residue label is
  present on this q-only unary source row.

Because a decorated perfect matching records the colour at every site, a
term in `U[w_v]` cannot also lie in `U[w_r]` for `r!=v`.  This proves the
five-component decomposition without a numerical graph heuristic.

The desired accessibility occurrence instead has

\[
                 q_{xv}^{0m_v}N                       \tag{2}

and lies in the full word `0|12112`.  It is not a vertex of (1).  A
translated mate does contain two `0m` q-spokes, but its old reset site `v`
is still colour zero.  Deleting one spoke therefore leaves a tail in the
wrong word grade, exactly as in commit `467d545`.

Nor is an endpoint bracket created.  The conditional theorem `8771755`
needs

\[
 (p_i@x\,s_j@v+p_i@v\,s_j@x)N,                       \tag{3}

whereas every graph vertex is q-only.  Inferring (3), endpoint activity,
goodness, or Hall incidence from a q-tail edge would discard source labels.

## Exact silent SCC guard

There is a simultaneous cyclotomic specialization over
`Z[w]/(w^2+w+1)`:

```text
selected C5 internal cells        = 1,
all five off-cycle chord cells    = w,
marked reset spokes q_xv^00       = 1,
all translated q_xr^(0,m_r)       = 0,
all desired full-m spokes         = 0.
```

In every reset face, its three surviving matching terms have values

```text
1, w, w^2,
```

and the complete row vanishes by `1+w+w^2=0`.  Their directed co-occurrence
component is a three-vertex silent SCC.  The three successive value ratios
are `w,w,w`, with closed holonomy `w^3=1`.  All five faces satisfy this
simultaneously; all ten off-cycle tail values remain nonzero, while every
translated C4/C6 term vanishes because it uses a translated spoke.

This proves that the marked unary transition graph by itself cannot force
(2), (3), or an offanchor/Hall exit.  It is a coefficient-typed partial
guard, not a full physical source: it does not impose all other unary words,
the four response targets, endpoint activity, or rootless goodness.

## Exact next input

The smallest row not present in the graph is a complete endpoint
word-change/spoke-to-hole relation which changes the reset value at `v` from
`0` to `m_v` while retaining the same decorated internal tail.  Equivalently,
an independently proved active bracket (3) invokes `8771755`.  More unary
re-pivoting within (1) cannot provide either datum.

Run:

```text
python3 computations/verify_h3_c5_marked_unary_transition_scc_guard.py
python3 -O computations/verify_h3_c5_marked_unary_transition_scc_guard.py
python3 -I -S computations/verify_h3_c5_marked_unary_transition_scc_guard.py
```

Frozen ledger SHA-256:

```text
c0035aea1dda69c7416711cffe672e877a3905156f913d930b9e5b05f3991459
```
