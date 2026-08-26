# Balanced degree-24 cycle-Morse pivot lemma

## Theorem (literal source form)

Let `R` be a degree-24 monomial in the 252 ordered cell variables such that
its port graph on `(site,colour) in {0,...,7} x {0,1,2}` is 2-regular.  Let
`w` be a nonconstant physical word and let `M` be one of the 105 physical
perfect-matching terms of the literal generator `H_w`.  Assume `M` divides
`R` occurrence-by-occurrence and its four edges lie in four distinct connected
cycles of the port graph.  Put `U=R/M`.

Then the literal column `U H_w` has 105 terms with coefficient one:

1. `U M=R`, and no other term equals `R`;
2. every other term `U N`, `N!=M`, is again port-balanced and has strictly
   fewer port cycles than `R`.

Thus `R` is a unit pivot for cycle-count order.  No group quotient, generic
coefficient, or residual-support hypothesis is used.

## Proof

Deleting the four selected edges from four distinct cycles leaves four
edge-disjoint paths, one for each selected edge, plus all untouched cycles.
Their eight degree-one endpoints are exactly the eight ports `(i,w_i)`.  Every
physical perfect matching `N` on the sites reconnects those endpoints, hence
restores port degree two.

Contract the four paths.  The number of newly closed cycles is the number of
components of the 2-regular multigraph `M union N` (parallel edges are allowed).
It is four exactly when all four components are doubled edges, equivalently
`N=M`.  For every `N!=M` it is at most three; untouched cycles contribute the
same summand on both sides.  Distinct physical perfect matchings use distinct
physical edge sets, so the target monomial occurs once.

Exhaustively, over all 105² ordered pairs `(M,N)`, the connection partitions
and counts are

| contracted path-cycle partition | pairs |
|---|---:|
| `1+1+1+1` | 105 |
| `1+1+2` | 1,260 |
| `1+3` | 3,360 |
| `2+2` | 1,260 |
| `4` | 5,040 |

Consequently the output cycle-count histogram is
`{4:105, 3:1260, 2:4620, 1:5040}`; each selected `M` has a unique four-cycle
completion.  A hostile path-pairing different from `M` has multiple peers at
the selected cycle count, verifying that “four distinct old cycles” is
load-bearing.

## Exact K-filtration statement

Let `K(X)` count nonanchor cells, with the twelve orbit-zero anchors
`A_(01),(23),(45),(67)[cc]`.  Additivity of monomial degree gives, termwise,

```text
K(U N) = K(R) - K(M) + K(N).
```

Outputs can therefore move in either K direction.  There are two distinct
valid uses:

- In `R/K^17`, if `K(R)<=16`, project the literal column to its terms of
  K-degree at most 16.  The pivot `R` remains and every retained nonpivot term
  still has fewer cycles; omitted terms are exactly higher-filtration terms.
- To retain the entire 105-term column literally inside K-degree at most 16,
  the necessary and sufficient condition is
  `max_N K(N)-K(M) <= 16-K(R)`.

The exhaustive source-decoration census covers all 6,558 mixed words and all
688,590 selected `(w,M)` terms.  For every mixed word `max_N K(N)=4`, so the
full-column condition becomes `K(M)>=K(R)-12`.  At a K16 parent it is exactly
“all four selected cells are nonanchors.”  The selected-term K histogram is
`{0:78,1:648,2:10656,3:107472,4:569736}`.

This filtration guard explains why a source-faithful K16 reducer may project
away K17--K20 completions, but may not claim that every cycle-Morse column is
wholly supported at K<=16.

## Replay and scope

Run `verify_cycle_morse_pivot_lemma.py` in this directory.  It enumerates the
11,025 matching connection pairs and the complete mixed-word decoration
census; it does not expand any residual.

The checker pins the literal degree-24 provider source and uses only its
structural conventions, not its retracted positive-only `R8` reconstruction.
The theorem is a triangular-pivot lemma, not a confluence or global closure
claim: inverse parents and critical pairs can still feed the lower-cycle
sector.

Logical result SHA-256:
`20c08278aa96cc51c6e3fb81a1db8959ac280f1c8babc08789c647d849be2a18`.
