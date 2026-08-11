# A same-base pure/mixed decoration forces a new physical matching

## Result

Suppose one physical perfect matching `B` carries both

```text
a nonzero pure other-bright target monomial,
and a distinct nonzero mixed zero-row monomial.
```

This is exactly the `L=N` residual left by the mandatory other-bright
matching.  It is not terminal.

Choose an edge `e` of `B` on which the two decorations differ.  Use the
mixed decorated cell on `e` and the pure decorated cells on every other
edge of `B`.  Since the matching edges are disjoint, these cells form a
legal monomial in one global output word.  Every factor was already nonzero,
so the hybrid monomial is nonzero.  Its word is mixed because the decoration
on `e` differs from the pure one; hence its target coefficient is zero.

Checker:
[`verify_h3_axis_target_coloop_same_base_hybrid_mate.py`](../computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py).

## Why the mate changes physical matching

For a fixed physical matching and a fixed output word, the decorated
matching monomial is unique.  Therefore the hybrid term cannot cancel with
a second term on the same skeleton `B`.  Exactness of the complete tensor
coefficient forces a nonzero monomial on a different perfect matching `B'`.

Two distinct perfect matchings cannot share all but one edge: after three
edges of a `K8` matching are fixed, the last two sites force the fourth edge.
Equivalently,

\[
                     B\mathbin\triangle B'
\]

is a disjoint union of alternating even cycles, each of length at least
four.  Thus the hybrid zero row opens a literal `C4`-or-longer
matching-exchange route.  This argument is coefficient-exact and does not
assume support completeness.

## Canonical packet

For the smallest same-base representative, take

```text
M = P0 | S1 | 23 | 45,
N = L = 01 | P2 | S3 | 45,
K = PS | 01 | 23 | 45.
```

Let `L` carry pure word `11111111` and let `N` carry mixed word
`22122212`.  The two decorations differ on physical edges `01`, `S3`, and
`45`.  Replacing exactly one of those three pure cells by its mixed cell
gives three explicit nonzero mixed coefficients.  Each requires a mate on
a physical matching other than `N=L`.

The checker also audits all `105` perfect matchings of `K8`: distinct pairs
share at most two edges, and every symmetric-difference component has even
length at least four.  Across every nonempty abstract changed-edge set it
checks the `3,360` possible one-edge hybrid choices.

## Routing consequence

The same-base decoration obstruction is removed.  The forced mate has the
existing physical split:

1. a new endpoint edge enters the complete-column/active-arm route;
2. an anchor-contained mate enters the Hall/lock matching web; or
3. only new residual `q` edges occur, leaving the already isolated
   diagonal/offdiagonal residual-`q` coefficient gate.

The theorem forces an active matching monomial, not merely a possible edge.
It does not claim that a residual-`q`-only mate is automatically an endpoint
arm or four-good.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py
python3 -O computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py
python3 -I -S computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py
```

Frozen ledger SHA-256:

```text
a18578cec952f4e7077e3716bec120ca36031df8a24944a2e5627234749218a2
```
