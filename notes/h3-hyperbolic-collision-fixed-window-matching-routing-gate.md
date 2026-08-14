# Hyperbolic collisions resolve to the two required switches, but are not source matchings

## Verdict

The four first faces of the hyperbolic root-return mechanism have a unique,
fully port-labelled matching resolution.  For every residual perfect-
matching tail, their two squarefree repairs are exactly

```text
A/B for the 0<->1 root square,
A/C for the 0<->2 root square,
```

where

\[
 A=Dq_{01}=PS|01,\qquad
 B=p_0s_1=P0|S1,\qquad
 C=p_1s_0=P1|S0.                                    \tag{1}
\]

All repairs stay on the same operation four-set `{P,S,0,1}` and leave the
residual tail literally unchanged.  Thus the matching geometry is positive:
there is no port wandering and no outside residual fan.

The unconditional physical construction nevertheless fails one grade
earlier.  A collision is a two-edge star with one missing and one doubled
augmented vertex, not a perfect matching.  It is absent from the squarefree
hafnian source module.  Matching completion determines the two endpoints of
a collision Tate cell; it does not construct that cell.

This is compatible with the local Pfaffian realization in `bcdf138`: the
root flow is a genuine determinant-one symmetry of the signed operation
`K4`.  The unresolved step is reinserting that local signed symmetry into
the complete unsigned, word-graded hafnian source with every incident
matching and principal-parts face restored.

Exact checker:
[`verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py`](../computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py).

## 1. Uniform fixed-tail resolution theorem

Let `a,b,u,v` be four distinct operation ports and let `T` be a perfect
matching on a disjoint residual set.  Consider the collision star

\[
                              (bu)(bv)T,               \tag{2}
\]

in which `a` is missing and `b` is doubled.  A squarefree repair which
changes one star arm must be one of

\[
                    (au)(bv)T,\qquad (av)(bu)T.        \tag{3}
\]

Both are perfect matchings.  Conversely, squarefreeness forces the new edge
to join the missing vertex `a` to the endpoint freed by the deleted star
arm, so (3) is exhaustive.  Their symmetric difference is the primitive
four-cycle on `{a,b,u,v}`.

This elementary observation gives the complete table:

| collision | missing/doubled | two repairs |
|---|---|---|
| `D*s1 = PS,S1` | `0 / S` | `A, B` |
| `p0*q01 = P0,01` | `S / 0` | `A, B` |
| `D*s0 = PS,S0` | `1 / S` | `A, C` |
| `p1*q01 = P1,01` | `S / 1` | `A, C` |

The repair theorem is natural in the tail.  Removing a common tail edge
before repair gives exactly the result of repairing first and removing it;
reinsertion is the reverse equality.  A matching flip inside the residual
tail changes `T` on both repaired endpoints and does not touch the operation
four-cycle.  The checker verifies this for tail sizes `0,2,4,6`; the proof
above is uniform.

For the canonical window `2345`, the tails are

```text
23|45, 24|35, 25|34.
```

Hence the four natural collision families have twelve literal collision
occurrences.  Every one has exactly the two repairs in the table, and zero
repair edges meet a residual-tail vertex.

## 2. The signs are exactly the required physical switches

The two root orders in `a29eb69` give the same oriented returns

\[
                         A-B,\qquad A-C.              \tag{4}
\]

Their sum is the Gate-II direction charge

\[
                         (A-B)+(A-C)=2A-B-C=L.        \tag{5}
\]

The shore-sign gauge `diag(1,-1,-1)` sends (4) to

\[
                         A+B,\qquad A+C,              \tag{6}
\]

which are precisely the two profile-changing families proved necessary in
`0d3f6d4`.  One family together with the complete response `A+B+C` does not
project `L`; both do, through

\[
             L=-4(A+B+C)+3(A+B)+3(A+C).              \tag{7}
\]

After the same gauge, `L=(2,-1,-1)` becomes `(2,1,1)`, of augmentation
four.  Thus a physical collision return would supply the desired
noncentered landing, rather than another centered holonomy loop.

There is an essential occurrence-level qualification.  Each collision has
the two parents displayed in Section 1, and the root acts on the complete
response with opposite coefficients:

| collision | contribution from first parent | contribution from second |
|---|---:|---:|
| `D*s1` | `A: -1` | `B: +1` |
| `p0*q01` | `A: +1` | `B: -1` |
| `D*s0` | `A: -1` | `C: +1` |
| `p1*q01` | `A: +1` | `C: -1` |

Thus every collision coefficient is zero after the complete response
collects its two parents.  The hyperbolic return uses the **parent
anti-diagonal**, not the collected collision scalar.  The required physical
object must therefore be occurrence-labelled: it has to retain which of the
two matching completions produced the same collision monomial.  This is the
exact naturality gap between the local Pfaffian symmetry and a source chain
map.

## 3. Smallest exact source-labelled guard

Take one fixed tail, say `23|45`, and the first collision

\[
                         D s_1 q_{23}q_{45}.           \tag{8}
\]

Its augmented-vertex degree has `0` missing and `S` doubled.  Its two
repairs are the physical perfect matchings

\[
             D q_{01}q_{23}q_{45},\qquad
             p_0s_1q_{23}q_{45}.                     \tag{9}
\]

There are 105 perfect matchings on the eight vertices
`P,S,0,1,2,3,4,5`; (8) is not one of them.  The coefficient functional of
the missing-`0`/doubled-`S` monomial kills all 105 squarefree matching
coordinates and reads one on (8).  Adding the two repairs (9) changes
nothing, because they were already in the squarefree module.

This three-monomial packet is the smallest exact guard to the implication

```text
two physical matching completions exist
    => the collision top exists as a physical source row.
```

The implication is false.  At `h=3`, the full relevant collision quotient
has dimension twelve: four distinct missing/doubled sectors times three
tail matchings.  The four sector types cannot cancel one another because
their augmented-vertex degree vectors are distinct.

## 4. Mandatory first principal-parts boundary

Each selected collision occurrence has four edges.  Removing an edge
through the doubled vertex leaves a `3K2` face; removing one of its two tail
edges leaves a `P3+K2` face.  Across the twelve fixed-window collisions the
exact flagged boundary is

```text
24 occurrence-labelled 3K2 flags,
24 distinct P3+K2 faces.
```

After forgetting the removed-edge/parent flag, the `3K2` half has eighteen
distinct monomials.  Six are shared by two collision families with
multiplicity two.  With the selected root-path signs none cancels: the
collected coefficient histogram is

```text
-2: 3,  -1: 6,  +1: 6,  +2: 3.
```

Thus a collision top cannot retain only the attractive matching return or
only the repeated-site half.  The response collision lives in word
`11:110000`.  Its `P3+K2` tail cofactors do not equal the canonical AugP2
packet in word `01211222`; their decorations, operation grade and
homological face differ.  The existing root cube contains no word-changing
arrow between them.

The first missing full-source object is therefore one **occurrence-split**
tail-natural family
for each of

```text
D*s1, p0*q01, D*s0, p1*q01,
```

packaged into a collision principal-parts mapping cylinder whose:

1. squarefree return faces are the two switches (6);
2. complete first boundary retains both the `P3+K2` and `3K2` halves;
3. word-changing AugP2 comparison carries the reduced-Eq correction; and
4. the same cell has physical `q`, anchor, `W`, ordinary-residue and shifted-
   ridge faces.

The two forward families alone reproduce the coefficient top, but both root
orders—and therefore all four collision families—are required for the
flat, order-natural hyperbolic square requested in `a29eb69`.

## 5. Proof consequence

The new boundary is sharper than either a purely positive or purely
negative answer:

```text
matching placement and tail naturality    proved, uniquely;
landing in A+B and A+C                    proved after shore gauge;
outside residual fan / port wandering     not forced;
collision source top                      absent from squarefree source;
full PP/AugP2 mapping cylinder             still missing.
```

If the four occurrence-labelled collision Tate families are constructed,
equations (5)--(7)
close the fixed-window centered-square gate with no further coefficient
projector.  If an exhaustive same-grade source map contains no such
families, any one of the twelve primitive parent-anti-diagonal collision
covectors is a terminal detector before the downstream cap/ridge ladder.

## Verification

Run

```text
python3 computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py
python3 -O computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py
python3 -I -S computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py
```

The checker uses exact rational and labelled monomial arithmetic, pins the
root-return, physical-routing and collision/AugP2 audits, verifies the
uniform repair theorem and naturality, and freezes the complete canonical
first-PP census.
