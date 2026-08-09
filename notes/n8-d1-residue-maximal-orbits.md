# N=8 D1: six maximal residue-support orbits

The arbitrary-boundary D1 problem now has a finite residue-only frontier.
Use one Boolean variable for each of the `54` residue K4 cells and impose:

1. the target residue fibre has a live matching;
2. none of the `80` mixed residue fibres has exactly one live matching;
3. the transported exact target-star quotient (`61594a9`);
4. the weakened same-diagonal obstruction (`ad7912b`);
5. the three-corner obstruction (`ee41aef`); and
6. the target-cross obstruction (`82bb313`).

This gives an exact `54`-variable, `1,204`-clause CNF with frozen hash
`5479362a3f988272af0333a275b8663a1e1bfb87d6989938314949342aca41ee`.
Every inclusion-maximal model was greedily extended, independently checked
maximal against the original CNF, quotiented by `S4 x S2`, and its entire
orbit downset blocked.  The residual CNF is UNSAT after exactly six orbits.
Their support sizes are

```text
34, 44, 45, 45, 46, 46.
```

Thus every residue support not already covered by one of the four exact
obstructions lies below one of six explicit representatives.  The checker
freezes every hole list, orbit size, target-line digraph, and non-target row
support profile.  This is an exhaustive Boolean theorem; it does not assert
that any of the six supports has a coefficient model.

## Fixed-vertex projection-rank roadmap

For a two-dimensional non-target kernel `K`, sort the three projection ranks
to the neighbouring colour spaces.  There are ten abstract profiles:

| profile | exact status / relevant atom |
|---|---|
| `(2,2,2)` | closed by the injective-tripod theorem `aa85cd4` |
| `(1,2,2)` | rank-one projection normal form; generic Koszul reduction, but the simultaneous-visible case remains to classify |
| `(1,1,2)` | projection-degenerate Koszul stratum; only flagged subcases are closed |
| `(1,1,1)` | common-line/compression stratum; requires a canonical residue family or a target/pure-lift factor |
| `(0,2,2)` | one blocked projection; sharp blocked-row flags are closed |
| `(0,1,2)` | blocked/rank-one filtration; flagged cases are closed, general incidence remains |
| `(0,1,1)` | double compression; target-star and pure-lift atoms cover some flags |
| `(0,0,2)` | two blocked projections; reduce to a line/two-factor slice |
| `(0,0,1)` | near-common-target star; target-star quotient applies when all three target vectors avoid the target line |
| `(0,0,0)` | fully blocked non-target star; the division-free target-star quotient closes the non-target target-vector branch |

This table deliberately separates proved coverage from the remaining
incidence classification.  Support patterns alone often permit both ranks
`1` and `2` when two rows have the same support, so the six orbit records do
not pretend to determine coefficient ranks.  They provide the exact finite
supports on which the rank cases must be split.

The strongest conceptual capstone now in view is:

> Every projection-rank/incidence profile is either residue-impossible, or
> has a canonical low-parameter residue family on which one of finitely many
> full/six-site pure-lift factors vanishes.

The exact checker
[`verify_n8_d1_residue_maximal_orbits.py`](../computations/verify_n8_d1_residue_maximal_orbits.py)
reconstructs the CNF and repeats the complete maximal-orbit proof.  Run it
with the repository virtual environment, which supplies PySAT/CaDiCaL.
