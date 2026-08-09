# Essential-star counting forces seven rank-one good pairs at N=8

## Outcome

Let arbitrary endpoint-ordered aggregate blocks satisfy

\[
                         H_8(A)=\Delta_{8,3}.                 \tag{1}
\]

Choose the three active rank-one colour witnesses at every site supplied by
the forced incident-edge theorem.  Then one of the following holds.

1. Some physical pair is selected in both directions.  Its block is a
   nonzero literal coordinate cell
   \(A_{vu}=\lambda e_b^{(v)}\otimes e_a^{(u)}\).
2. No physical pair is selected in both directions.  There are then **at
   least seven active rank-one physical pairs whose two deleted endpoint
   stars are both injective**.

Thus the earlier reciprocal/four-exception dichotomy sharpens to

\[
 \boxed{\text{a reciprocal coordinate block, or at least seven rank-one
 good pairs}.}                                               \tag{2}
\]

The alternatives are conditioned on the chosen witness system; (2) does
not assert that the two resulting properties are logically disjoint.

## Essential-incidence proof

For an endpoint `u` and neighbor `v`, let

\[
 L_{u\leftarrow v}=\operatorname{im}(V_v^*\longrightarrow V_u)
                                                               \tag{3}
\]

be the complete mode-`u` support of `A_uv`.  The target flattening says that
the seven neighbor supports span `V_u`.  Call `(u,v)` essential when deleting
`L_{u<-v}` makes their sum proper.  The essential-subspace lemma in
[the target-flattening theorem](target-flattening-essential-star-pair-bound.md)
gives

\[
                    e(u):=\#\{v:(u,v)\text{ essential}\}\le3. \tag{4}
\]

It also identifies the equality case: if `e(u)=3`, the three essential
supports are independent lines and **every other incident support is zero**.
This statement includes zero blocks: the zero support is never essential,
because deleting it changes no span.

Let `R` be the graph of active rank-one physical pairs.  In the
no-reciprocal branch the 24 directed colour witnesses occupy 24 distinct
physical pairs, so

\[
                         |E(R)|\ge24.                         \tag{5}
\]

If `e(u)=3`, the equality case leaves exactly three nonzero blocks at `u`.
The forced incident-edge theorem already supplies three distinct active
rank-one neighbors there, so these are precisely the surviving blocks and

\[
                              d_R(u)=3.                        \tag{6}
\]

Since `R` omits at most four of the 28 pairs, (6) requires all four omitted
edges to be incident with `u`.  At most one vertex can have this property:
two four-edge stars have union at least seven.  Every other vertex has at
most two essential neighbors.  Hence the global directed essential budget
is not 24 but

\[
                         \sum_u e(u)\le3+7\cdot2=17.           \tag{7}
\]

An `R`-edge is a bad pair exactly when at least one of its two endpoint
incidences is essential.  Assign every bad `R`-edge to one such incidence;
distinct physical pairs give distinct directed incidences.  Equations
(5)--(7) therefore give

\[
 \#\{\text{good active rank-one pairs}\}
       \ge |E(R)|-17\ge7,                                    \tag{8}
\]

as claimed.  Notice that no pointwise degree-six assertion is needed: the
rank-one graph has average degree at least six, while the only pointwise
fact used is the equality implication (6).

If `R` omits respectively zero, one, two, or three edges, no vertex can
have `e(u)=3`; the same ledger improves (8) to 12, 11, 10, or 9 good
rank-one pairs.  Seven is the worst case only when four `R`-edges are
missing.

## Sharp incidence counterguard

The bound seven is sharp for the information used above.  Take

\[
 R=K_8\setminus\{04,05,06,07\}.                              \tag{9}
\]

Orient `01,02,03` away from 0.  On vertices `1,...,7`, use the regular
cyclic tournament with forward steps 1, 2, and 3; label those steps by
colours 0, 1, and 2.  Label the three arcs from 0 by the three colours.
Every vertex has one outgoing witness of each colour, no pair is reciprocal,
and all 24 used blocks are rank one with the required coordinate line at
the head.

At 0, give the three tail factors the three coordinate lines.  At each
outer vertex, give its three free tail factors one repeated coordinate
line.  Choose this repeated line to agree with the extra incoming arc from
0 at vertices 1, 2, and 3.  The three incoming tournament arcs have the
three distinct head axes.  Consequently 0 has three essential neighbors,
each outer vertex has two, and no edge is essential in both orientations.
Exactly 17 rank-one pairs are bad and exactly seven are good.

This realizes the full rank/support/head-axis incidence data, including
zero blocks on (9)'s complement.  It does not construct the matching
cofactors or satisfy (1), so it is not a Krenn counterexample.  It shows
that improving seven requires mixed-fibre or cofactor provenance, not a
stronger count from the same local subspaces.

## What this buys in E1/E2

The registered escape-chart theorem puts every good pair at every even
order at exactly the extra-kernel (E1) or defect-at-least-two (E2) fork.
Therefore the no-reciprocal N=8 branch now supplies at least seven such
charts whose **deleted direct block itself is active and rank one**.

No current E1/E2 theorem closes them merely from that added rank condition.
The distinguished-span-two E1 theorem already permits an arbitrary complex
direct block and still needs its dense graph/span hypotheses.  Conversely,
the E2 rank graph is built from rank-three blocks of the internal complement;
rank one of the deleted direct block does not select an E2 defect or a
centered low-degree mask.  In particular, the existing centered rank-one
overlap theorem concerns a specific internal/spoke mask, not rank one of
`A_uv`.  If a reciprocal coordinate block is diagonal, it can instead land
on the explicitly unresolved scalar-matrix-unit boundary of the E1 cap
packet.  Thus (2) is a substantial unconditional supply theorem for the
overlap machinery, but not yet an E1/E2 elimination.

## Reproduction

```sh
python3 computations/verify_n8_rankone_good_pair_essential_count.py
python3 -O computations/verify_n8_rankone_good_pair_essential_count.py
```

The checker independently audits the complement/essential budget for all
five possible edge counts and constructs the sharp 24-witness endpoint-line
model, including the zero-block and endpoint-order checks.
