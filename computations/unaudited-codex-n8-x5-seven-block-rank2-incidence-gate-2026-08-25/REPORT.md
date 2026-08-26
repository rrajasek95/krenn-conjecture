# Exact rank-two closure of the canonical seven-block branch

## Outcome

For the canonical full-family support

```text
{06,13,17,24,26,56,57} + {04,12,35,67},
```

all five exact full-rank chart orbits for `rank(A57)=2` are unit ideals over
`Q`.  Together with the independently sealed `rank(A57)<=1` result and the
guard exclusion of rank three, this closes every rank for this canonical
support: the formal guard plus the complete 6,561 full-X5 equations force an
active cap67/triangle012 or cap45/star(center=2).

This is one of the six full-family support representatives (plus its named
order-two guard mate).  An exhaustive transport test found no permissible
source/site permutation from it to representatives 1--5, so this report does
not claim those five supports or all 64 loci.

## Exact rank-two reduction

Write

```text
A57 = U V^T,                    U,V in Mat(3,2), full column rank.
```

The stored-edge guard orientation gives

```text
A56^T = -A26 V U^T,
A56   = -U (A26 V)^T,
A06 V = 0,
(I-A17 A26)V = 0.
```

With `W=A26 V`, the cap67 response matrices factor through `U^T`:

```text
R05(K) = (A06 K V) U^T,
R15(K) = (K V-A17 K^T W) U^T,
R25(K) = (A26 K V-K^T W) U^T.
```

Thus three arbitrary 3-by-3 response duals reduce exactly to three 3-by-2
matrices, 18 variables rather than 27.  The audit independently replays the
response factorization and its Frobenius adjoint on 257 exact integer samples.

## Five full-rank charts

If cap45/star2 is inactive, either a diagonal functional fails or the fixed
identity pairing fails.  For its response space

```text
P tensor Q,
P = Row(A04),
Q = ColSpan(A35^T,U),
```

the diagonal failure is `e_i in P and e_i in Q`.  Fixed-identity pairing
failure forces `P=Q=Q^3`, which is contained in every such incidence branch.
Color symmetry normalizes `i=0`.

Choose a nonzero 2-by-2 row minor in each of `U,V`.  Label by the failed color
`i` and the omitted minor rows `r,s`.  Diagonal `S3` has exactly five equality
orbits on the 27 ordered triples `(i,r,s)`:

```text
i=r=s, i=r!=s, i=s!=r, r=s!=i, all distinct.
```

The five generated charts represent these orbits.  Each imposes

```text
eta * minor_U * minor_V - 1 = 0
```

and therefore excludes rank-deficient factors fail-closed.  Each chart has
120 variables and 6,589 equations: 6,561 full-X5, 12 reduced guard, 9 cap67
adjoint, 6 cap45 incidence, and 1 minor-inverse equation.

## Exact elimination results

Every modular control and every rational proof-producing run terminated with

```text
INPUT_GENERATORS=6589
GROEBNER_SIZE=1
UNIT_REMAINDER=0
STATUS=UNIT_IDEAL
```

| chart | `F_32003` wall | `Q` wall |
|---|---:|---:|
| all equal | 40.089 s | 39.771 s |
| incidence equals U | 40.767 s | 37.798 s |
| incidence equals V | 36.907 s | 36.499 s |
| equal minors off incidence | 37.064 s | 38.269 s |
| all distinct | 47.181 s | 36.571 s |

Only the five `Q` runs carry mathematical coverage.  The modular runs are
independent controls of the identically generated systems.

## All-rank canonical conclusion and transport boundary

The pinned rank-one package closes `rank(A57)<=1`.  The five rational units
above close rank two.  Rank three cannot occur because the canonical support
requires nonzero `A06`, while the guard contains `A06 A57^T=0`; Sylvester's
rank inequality gives `rank(A57)<=2`.

To test rather than assume transport, the audit enumerated all 40,320 site
permutations, requiring preservation of the fixed identity edge set, the
variable block family, and the added support.  The canonical-to-representative
counts are exactly

```text
[1,0,0,0,0,0].
```

The sole self-map is the identity.  The named guard symmetry supplies the
canonical support's mate outside the chosen list of six representatives, but
there is no legal direct transport to the other five.  Representative 2 has
the same outside-site/rank-factor shape and is the smallest natural next
separate ideal, not a consequence of this certificate.

Parent manifests:

```text
guard/full-family: 21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf
rank(A57)<=1:      45ab914ff35c446f67fcc2ec86a6d4201c8ddf3e0afed0b9420e269ad610daa9
```
