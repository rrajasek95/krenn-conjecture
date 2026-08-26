# Rep2 group16 strict-leaf exact reduction

Starting from the pinned strict leaf `V(a57_01,a04_11)` (59 variables, 6,064 distinct generators, 157,829 terms), exact parsing finds the unit-coefficient graph relation

`-1-a26_00-a26_02*a57_02 = 0`.

The reversible substitution `a26_00=-1-a26_02*a57_02` removes one variable and that graph equation.  Exact substitution, coefficient combination, zero removal, and generator deduplication produce a pinned 58-variable/6,063-generator/113,139-term source.  Its homogeneous grading has rank 54 and nullity four; its affine-linear rank is three and full linear-part rank is 43.  The complete-factor census has 28 positive coordinates, led by `a04_12,a04_21,a04_22` at 504 generators each.

Exhaustive primitive-weight scoring selects `a14_01` (weight `-1`).  The exact root-free `D(a14_01) union V(a14_01)` cover has a structural unit ideal on the open chart and a single nonempty closed chart with 57 variables, 6,015 generators and 111,546 terms.  Consequently `a14_01=0` is forced on this strict leaf; the global nonempty-leaf count remains three.

No source was sent to Singular.  This package proves only the graph isomorphism, forced-zero reduction, and exact chart-ledger update; it makes no closure or performance claim.
