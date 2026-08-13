# At eight sites a failed circuit tail is only a star or triangle

## Result

Let `C` be a physically squarefree protected-relative frame circuit in the
eight-site packet.  Its two sides use the same even set `U` of physical
sites and `|U| >= 4`.  Hence the unused set has size `0`, `2`, or `4`.

* For zero unused sites, the circuit itself gives two full matching
  occurrences in one source word.
* For two unused sites, any supported decorated cell on their physical pair
  is a common tail.  Tail failure means that complete two-site cofactor
  support is empty.
* For four unused sites, tail failure means that the induced physical
  support graph has no matching of size two.  Its edge family is therefore
  pairwise intersecting and is empty, contained in a star, or contained in a
  triangle.

Thus the general Tutte branch of the frame-circuit lift theorem has no large
topology in the `N=8` endgame.  It lands exactly on the already identified
zero-cofactor, star, and triangle accessibility interfaces.  A `K2,2` tail
barrier cannot occur here: `K2,2` itself has a perfect matching.

Checker:
[`verify_n8_frame_circuit_tail_hall_reduction.py`](../computations/verify_n8_frame_circuit_tail_hall_reduction.py).

## Proof

A primitive squarefree circuit contains at least two edges on each side, so
it uses at least four physical sites.  Both sides are matchings, hence the
used and unused site counts are even.

On four vertices, a physical support graph has a perfect matching exactly
when its matching number is two.  If no such matching exists, every two
edges meet.  A pairwise-intersecting family of graph edges is contained in a
star or a triangle: choose two edges `ab,ac`; if every edge contains `a` the
family is a star, while an edge avoiding `a` must be `bc`, and every edge
meeting all three of `ab,ac,bc` lies in that triangle.

The checker exhausts all `2^6=64` simple support graphs on four sites and
freezes the exact split.  Endpoint colours need no extra compatibility: a
physical perfect matching uses each site once, so independently choosing one
supported decorated cell on each matching edge defines a consistent tail
word.

## Proof-frontier consequence

Combining this with the circuit cover and lift trichotomy leaves the
following eight-site entry map:

```text
frame circuit
  |
  +-- squarefree, tail exists --> literal common-tail matching component
  |
  +-- squarefree, no tail -----> empty cofactor / star / triangle
  |
  `-- repeated site -----------> physical Cartan-Spencer comparison
```

The missing two-site tail is a missing connector, not by itself a deletable
occupied cell; it must force circuit expansion or be absorbed by a complete
cofactor relation.  Co-located-star subcharts have existing deletion/unit
routes.  A general non-strict triangle still needs the promised
anchor-preserving Hall landing; this note identifies it but does not silently
close it.  After any of these routes produces a carrier, transverse
rank/support landing remains the downstream theorem.

## Scope

This is an exact `N=8` reduction of tail topology.  It does not apply
unchanged to a large unused complement at arbitrary `N`, prove coefficient
cancellation in the common-tail row, close every triangle source packet, or
construct a clean cap.

Run:

```text
python3 computations/verify_n8_frame_circuit_tail_hall_reduction.py
python3 -O computations/verify_n8_frame_circuit_tail_hall_reduction.py
python3 -I -S computations/verify_n8_frame_circuit_tail_hall_reduction.py
```

Frozen ledger SHA-256:

```text
89e59d2a2a173c911cb7ac88b24f76a9d5f92a46035687f0d83793c4b0d6ee2f
```
