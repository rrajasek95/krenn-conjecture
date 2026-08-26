# Structure after completing the full `7+1` packet

## The 196-term separator

The exact integer dual for closure22 plus all 48 profile-`7+1` words is a
single connected relative edge-colour cocycle.  Its 196 columns use 61
physical multigraphs and 15 ordered-colour histograms; the coefficient
incidence matrix is connected and has rank seven.  Every physical graph has
degree sequence `(4,4,4,4,4,2,2,2)`.

Its physical, colour, and joint affine ranks are respectively 14, 5, and 19,
so there is no nonconstant marginal intersection.  Its coefficient sum is
`-2`, 28 first-moment coordinates are nonzero, and none of the 15 colour
histograms has a distinct global-colour translate elsewhere in the support.
Thus it is not a toric circuit, marginal, signed cut/cycle, or single minor.
Completing profile `7+1` has fused the older disconnected residue into a
larger chart-specific cocycle; it has not exposed a familiar cellular class.

## The word `00202112`

This word has colour multiplicities `(3,3,2)`: colour 0 occurs at sites
`0,1,3`, colour 1 at `5,6`, and colour 2 at `2,4,7`.  Its full `S8 x S3`
orbit has size 1,680 and stabilizer order 144,

```
H = ((S3 x S3) semidirect C2) x S2,
M_332 = Ind_H^(S8 x S3)(1).
```

On restriction to site permutations,

```
M_332|S8 = 3 * (
  S[8] + 2 S[7,1] + 3 S[6,2] + S[6,1,1]
  + 3 S[5,3] + 2 S[5,2,1] + S[4,4]
  + 2 S[4,3,1] + S[4,2,2] + S[3,3,2]).
```

On restriction to colour permutations it is 280 copies of the regular
`S3` representation.

Exactly one degree-nine translation of `X_00202112` pairs with the dual, by
`+1`.  Its physical multiplier is the nine-edge graph

```
07, 17, 25, 34, 36, 37, 45, 46, 56,
```

and its ordered-colour histogram is `5(00)+1(10)+2(11)+1(12)`.  A literal
decorated multiplier is frozen in the checker output.

## Why this is not the next module theorem

`00202112` is only the lexicographically first word with one crossing.  There
are 35 one-translation killers spread over five different shape orbits.
More broadly, 4,932 words and 151,027 translations cross the separator, and
all eight remaining mixed word-shape orbits occur.  Within shape `(3,3,2)`,
1,592 of 1,680 words cross, including 14 one-translation killers.  The
selection is not constant on its source orbit because the joint quotient is
not `S8`-equivariant.

Therefore adding the full `(3,3,2)` orbit will kill this separator but no
module-completion theorem forces exactness; the previous two completions
already show that a replacement relative class can appear.  It is also a
poor cost choice: `(3,3,2)` requires 1,680 new equations, whereas the crossed
profile `(6,2)` has orbit size 168, nine words already admitted, and needs
only 159 additions.  It is the immediate one-site refinement of `(7,1)`.

Actionable prediction: if orbit completion remains the heuristic, test the
full `(6,2)` module before `(3,3,2)`.  Treat any resulting zero reduction or
new dual as a semigroup calculation requiring the same literal/characteristic
zero scope checks; do not interpret orbit completion itself as exactness.

Replay:

```
python3 computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_full_profile71_terminal_structure.py --check-results
python3 -O computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_full_profile71_terminal_structure.py --check-results
python3 -I -S computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_full_profile71_terminal_structure.py --check-results
```
