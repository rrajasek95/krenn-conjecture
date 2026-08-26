# Rep2 group16 D(t1) timeout reduction

The consumed exact-Q `D(t1)` chart has 64 variables and 6,569 distinct generators.  Its expanded homogeneous grading has exact rank 58 and nullity 6.  Three coordinates have literal global-unit witnesses: `sat` in generator 6567 and the inverse pair `t1,it1` in generator 6568.

The weight rows of `it1` and `sat` form a primitive rank-two minor (determinant `-1`) in the grading lattice.  Therefore the corresponding two-dimensional torus action sets `it1=sat=1` without root extraction.  The inverse equation `t1*it1-1=0` then forces `t1=1`.  Exact source specialization removes all three coordinates and the vanished inverse equation, yielding one source-faithful 61-variable / 6,568-generator chart.

This is an exact isomorphism of the timed chart, not an open-only shortcut.  The old 480-second attempt remains consumed and was not rerun.  No Singular command was executed for this design, and no mathematical closure is claimed until the reduced exact-Q chart is independently audited and solved.
