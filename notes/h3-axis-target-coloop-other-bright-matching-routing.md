# The other-bright target leaves two exact label-sensitive topology packets

## Result

Take each of the 50 no-cross triples (M,N,K) after the unary E3 landing:
M is the selected bright target matching, N the active mixed outside
matching, and K the direct unary matching. The other diagonal response has
target value one, so choose one literal other-bright pure matching L.

There are 90 possible physical L skeletons: a bright pure matching cannot
contain P-S because the normalized direct block has only its 00 cell.
The checker exhausts all 50 times 90 = 4,500 choices and classifies them in
proof priority:

    crossed response skeleton in the pure-anchor union: 612;
    otherwise an active endpoint arm of N is external: 3778;
    otherwise only residual-q edges of N are external:   48;
    otherwise a distinct N in an anchor Hall web:        12;
    remaining same-skeleton label packets L=N:           50.

Checker:
computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py.

The C6 split is 130/746/10/4/10 and the six C8 records contribute
482/3032/38/8/40, in the displayed category order.

## Why the first three classes advance

The three pure anchors are M,K,L. If their physical union contains a
crossed response skeleton, the packet has the exact matching topology
missing from the 50 original triples.

If no crossed skeleton is present but an endpoint arm of N lies outside the
three pure anchors, that arm is part of the already selected nonzero mixed
monomial. It is therefore a literal active external endpoint component, not
a support possibility.

In the remaining 12 nondegenerate cases, N is contained in the pure-anchor
union and is distinct from M,K,L. Thus the union contains an exact fourth
anchor-contained matching and has entered the strict Hall matching web.
The checker does not reprove the downstream source-labelled Hall/lock
theorems.

This routes 4,402 cases by physical topology. It does **not** route the 48
cases in which the only external edges of N are residual-q edges: although
those q cells are active, their decorations can be diagonal, so neither an
external endpoint-arm theorem nor an offdiagonal/nonanchor-label theorem is
available from incidence alone.

The count agrees with the independent 82-case guard: before crossed-skeleton
priority, 82 cases have nonempty external N-edges consisting only of
residual-q edges. Of those, 34 already contain a crossed skeleton; the other
48 are the genuine priority residual.

## The two exact label obstructions

The smallest residual-q-only representative is

    M = P0 | S1 | 23 | 45,
    N = 01 | P2 | S3 | 45,
    K = PS | 02 | 13 | 45,
    L = 04 | 15 | P2 | S3.

Here the only edge of N outside M union K union L is 01. Its active
decoration is not determined by physical incidence. A diagonal decoration
is the precise missing label audit.

All 50 original triples have one and only one residual topology type:

    L=N as physical perfect matchings.

The same physical skeleton carries two different decorated coefficients:
one is the selected mixed zero-response monomial and the other is a
pure other-bright target monomial. Topology sees neither a new edge nor a
new matching.

The smallest representative is

    M = P0 | S1 | 23 | 45,
    N = L = 01 | P2 | S3 | 45,
    K = PS | 01 | 23 | 45.

This representative is already full-support impossible by the common-edge
unit in 7f3096a, but the other 49 do not all share a common physical edge.
Their remaining gate is coefficient-theoretic: couple the mixed and pure
decorations on one matching through the common q/full response rows. No
further physical matching-union census can distinguish them.

## Scope

This is an exact physical matching theorem with the P/S direct-cell
restriction included. A crossed skeleton is not asserted coefficient
nonzero solely from containment. Only an external endpoint arm is routed as
such; an external residual-q cell is kept as an obstruction despite being
active. The 48 q-only and 50 L=N cases are not claimed feasible; they are the
sharp label-sensitive packets left by this topology census.

Run:

    python3 computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py
    python3 -O computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py
    python3 -I -S computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py

Frozen ledger SHA-256:

    1b20cd6d8ca11706716617efafcf8729db2642e9391e7917ad40d089c8dd29e1
