# Cofactor graphs reduce the remaining onset problem to two configurations

**Written proof and exact exhaustive graph certificate; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/cofactor-graph-ghz-frontier-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

A ground cofactor graph must admit nonzero edge weights with zero sum
at every vertex. This package classifies that necessary condition
on all 32,768 six-vertex graphs using two independent exact tests:
incidence-rank preservation and coverage by explicit integer
kernel circuits. No numerical coefficient search is involved.

Two additional analytic rules propagate small-edge bounds and
settle any graph with four anchored arms at one vertex or a six-cycle
of anchors. Combined with the balanced-response theorem, only
three cofactor graph types remain. They reduce to two anchor
configurations for the remaining onset proof.

At most sixteen projective single-cell directions remain for any
full-support single-color ground zero; with no zero cofactor rows,
at most eight remain, and with exactly one zero row none remain.
Both residual anchor configurations have exact ground examples,
including a new real example made from two triangles joined by
one bridge in the cofactor graph.

From the repository root, with Python 3.11 or later:

~~~sh
python3 -B computations/cofactor-graph-frontier-2026-09-27/verify.py > /tmp/cofactor-graph-frontier.json
diff -u computations/cofactor-graph-frontier-2026-09-27/results.json /tmp/cofactor-graph-frontier.json
python3 -B -O computations/cofactor-graph-frontier-2026-09-27/verify.py > /tmp/cofactor-graph-frontier-optimized.json
diff -u /tmp/cofactor-graph-frontier.json /tmp/cofactor-graph-frontier-optimized.json
~~~

The standard-library replay checks the complete support census,
all 285 labelled minimal circuit witnesses, every residual pair in
the surviving graph classes, 384 vertex matching expansions,
1,440 propagation quartet identities, and all cofactors in the
two ground examples. The bridge example uses exact arithmetic
modulo a quartic polynomial, with a separate positive-root argument.

The graph enumeration is exhaustive. Its application to arbitrary
nearby complex sources also uses the written analytic estimates;
the finite ground examples alone do not prove those estimates.
Checks remain active under optimized Python.
