# Sparse exact GHZ8 families stay below residual rank 55

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

The universal L0 tangent-incidence condition says that an eight-site binary
GHZ source whose deletion packet has differential rank $55$ must have
full/mixed-row ranks $55/53$. A useful baseline is the residual rank of the
sparse cycle, switch, subdivision, and cancellation constructions already in
the repository.

For these sparse constructions, an exact census over all 28 endpoint-pair
deletions gives:

| exact binary GHZ8 source | coefficient field | maximum residual rank |
|---|---:|---:|
| alternating cycle | $\mathbb Q$ | 22 |
| two-matching switch | $\mathbb Q(\sqrt2)$ | 26 |
| polystable two-matching switch | $\mathbb Q(\sqrt3)$ | 26 |
| rational cancellation / pair-cap source | $\mathbb Q$ | 31 |
| subdivided active-rank-two gadget | $\mathbb Q$ | 26 |

For every one of the 140 deletions, removing the two pure output rows lowers
the differential rank by exactly two. Thus every audited sparse source has
the required tangent-incidence shape, but none approaches the dangerous
rank-55 stratum.

This is not a classification and does **not** prove that a rank-55 binary
GHZ8 source is absent. Its role is to provide a replayable low-complexity
baseline. In particular, it does not cover denser cancellation components of
the binary GHZ8 fibre.

That qualification is material: the later
[exact rank-53 chart](binary-ghz8-exact-rank53-source.md) gives a denser
rational source with residual ranks $53/51$. The present census records the
sparse baseline rather than the best exact rank now known.

## Sources audited

The first four sources are reconstructed independently from existing exact
artifacts:

1. the alternating binary cycle;
2. the switched $C_4$ family with its two standard exact normalizations;
3. the rational eight-site cancellation source used in the pair-cap route;
4. a new direct two-vertex subdivision of the support-minimal six-site
   active-rank-two gadget.

For the last item, the cell $(2,3,0,0)$ in the six-site gadget separates the
two pure tensors exactly: terms using it sum to $e_{0^6}$, while terms not
using it sum to $e_{1^6}$. Replacing that cell by the two-edge path
$2\!-\!6,3\!-\!7$ in colour zero and adding the internal edge $6\!-\!7$
in colour one therefore gives an exact eight-site binary GHZ source. This
adds a cancellation source with an active rank-two internal block to the
census rather than only another monomial cycle.

## Exact audit

[verify_binary_ghz8_residual_rank_census.py](../computations/verify_binary_ghz8_residual_rank_census.py)
uses only the standard library. It:

* implements exact arithmetic in $\mathbb Q(\sqrt d)$;
* verifies all 256 matching-tensor coefficients of each of the five displayed
  sources;
* builds $d\Psi_M$ after every endpoint-pair deletion;
* computes both its full 64-row rank and its 62 mixed-row rank exactly; and
* checks the complete rank-pair histograms, not just their maxima.

The checker passes normal, optimized, and isolated Python. Its maximum $31$
is a statement only about the displayed sparse families, not about the full
binary GHZ8 fibre.
