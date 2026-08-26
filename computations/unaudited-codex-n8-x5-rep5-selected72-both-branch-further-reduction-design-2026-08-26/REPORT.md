# Rep5 selected-72 both-branch further reduction design

Verdict: **exact further covers exist for both parent branches; design-only, not closure.**

For the parent `q=A37[20]=1` branch, exactly three coordinates divide any complete generators: `A04[20..22]`, each dividing 486. Exhaustive scoring selects `x=A04[20]`. The identity `D(x) union V(x)` gives an open localization that adjoins `inv_x*x=1` and soundly divides all 486 `x`-multiple generators, plus a literal `x=0` branch. This is reversible and root-free; it is a factor/localization reduction, not a torus quotient.

For the parent `q=0` branch, the inherited grading has exact rank 71/nullity 1 with primitive weights `+1` on `A04[20..22]` and `-1` on `A35[21..22]`. Exhaustive coordinate scoring selects the recorded primitive coordinate and yields two 71-variable `D/V` torus charts, with no root extraction.

The four generated exact-Q design sources jointly cover both existing 72-variable branches. An independent flat-polynomial replay reconstructs every divided or specialized generator and both grading identities. Sixteen hostile mutations reject. No Singular process, ideal solve, mathematical coverage, implication between the two parent branches, or rep5 closure is claimed.
