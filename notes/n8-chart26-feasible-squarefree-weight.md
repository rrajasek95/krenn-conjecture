# A feasible squarefree weight inside the certified chart-26 cone

## Outcome

The non-squarefree degree-six lead is not intrinsic to the full Groebner
cone determined by the certified degree-four and degree-five layers.  There
is an explicit integral weight which

* preserves all 6,558 original degree-four leading monomials;
* preserves all 84,005 leading monomials in the complete degree-five
  Buchberger layer; and
* makes the squarefree monomial `0951b4c7ebf5` the unique leading monomial
  of the first 546-term degree-six compatibility cell, with margin one.

The admissible term order compares homogeneous total degree first, then
off-support (y)-degree (so (t) is last), then the displayed integral
weight, and finally the old lexicographic order.  The weight has 103 nonzero
coordinates, ranges from (-10) to (27), and is frozen in
`verify_n8_chart26_feasible_squarefree_weight.py`.

This weight was found by a cutting-plane calculation.  Each oracle pass
streamed every old degree-four polynomial and every completed degree-five
transport cell, adding only violated lead inequalities.  The first seven
squarefree degree-six candidates were infeasible in the resulting cone.
The eighth candidate closed after 17 oracle scans.  The committed checker
does not trust that numerical search: it replays the final integer weight
against every relevant polynomial using exact integer arithmetic.

## Interpretation

This revives the squarefree-degeneration route.  The repeated edge in the
old lexicographic lead was a term-order artifact, not an unavoidable vertex
of the degree-four/degree-five Groebner cone.  The next calculation should
continue Buchberger completion in this new order and ask whether every new
minimal degree-six leading monomial can also remain squarefree.

The result is deliberately bounded.  It does not prove that the full
homogenized ideal has a squarefree initial ideal, and therefore does not yet
prove radicality or pure-target membership.

## Verification

Run

```text
python3 computations/verify_n8_chart26_feasible_squarefree_weight.py
```

The replay exhausts the 6,558 original polynomials, all 84,005 degree-five
cells, and all 372 top-degree terms of the first degree-six cell.
