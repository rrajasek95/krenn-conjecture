# Every source-changing two-block support has an active clean cap

Status: **all 34 first source-changing support pairs are closed.**  Under the
exact frozen source/guard symmetry they form 18 orbits.  Every orbit has a
coefficient-independent active clean cap, so a common zero of its six
residual polynomials implies an active cap without any elimination or
additional equation.

## Exact symmetry and residual ledger

The site permutations preserving the four fixed identity edges, the four
variable cycle edges, cap `67`, and triangle `012` form the order-two group

```text
1,  (1 2)(6 7).
```

It partitions the 34 support pairs into two singleton and sixteen doubleton
orbits.  Put

```text
P_a=1+X[a,a]Y[a,a],   Q_b=1+U[b,b]V[b,b].
```

For each representative, `Z,W` name its two added blocks.  Literal perfect-
matching expansion gives the following complete six-residual ledger; each
formula holds for every ordered `a!=b`.

| Orbit | Representative | Residual polynomial | Active cap / triangle | Possible internal responses |
|---:|:---:|---|:---:|:---:|
| 0 | `01,23` | `P_a Q_b + Z[a,b]W[b,a]V[b,b]` | `16 / 027` | `07,27` |
| 1 | `01,24` | `P_a Q_b + Z[a,b]W[b,a]Y[a,a]V[b,b]` | `03 / 145` | `15,45` |
| 2 | `01,36` | `P_a Q_b + Z[a,b]W[a,b]` | `27 / 016` | `16` |
| 3 | `01,46` | `P_a Q_b + Z[a,b]Y[a,a]W[a,b]` | `03 / 145` | `15,45` |
| 4 | `05,34` | `P_a Q_b + Z[a,a]U[b,b]W[a,a]V[b,b] + Z[a,a]W[a,a]` | `03 / 145` | `45` |
| 5 | `06,13` | `P_a Q_b + Z[a,b]W[b,a]` | `27 / 016` | `16` |
| 6 | `06,14` | `P_a Q_b + Z[a,b]W[b,a]Y[a,a]` | `03 / 456` | `45,56` |
| 7 | `06,37` | `P_a Q_b + Z[a,b]U[b,b]W[a,b]` | `16 / 027` | `02,27` |
| 8 | `06,47` | `P_a Q_b + Z[a,b]U[b,b]Y[a,a]W[a,b]` | `03 / 456` | `45,56` |
| 9 | `13,25` | `P_a Q_b + X[a,a]Z[b,a]W[b,a]V[b,b]` | `03 / 145` | `14,45` |
| 10 | `13,56` | `P_a Q_b + X[a,a]Z[b,a]W[a,b]` | `03 / 145` | `14,45` |
| 11 | `14,25` | `P_a Q_b + Z[b,a]W[b,a]V[b,b]` | `03 / 145` | `45` |
| 12 | `14,56` | `P_a Q_b + Z[b,a]W[a,b]` | `03 / 145` | `45` |
| 13 | `15,36` | `P_a Q_b + X[a,a]Z[b,a]W[a,b]` | `03 / 456` | `45,46` |
| 14 | `15,46` | `P_a Q_b + Z[b,a]W[a,b]` | `03 / 145` | `45` |
| 15 | `17,26` | `P_a Q_b + Z[b,b]W[b,b] + X[a,a]Z[b,b]W[b,b]Y[a,a]` | `03 / 145` | `45` |
| 16 | `36,57` | `P_a Q_b + X[a,a]U[b,b]Z[a,b]W[a,b]` | `03 / 456` | `45,46` |
| 17 | `46,57` | `P_a Q_b + U[b,b]Z[a,b]W[a,b]` | `03 / 145` | `45` |

The other 16 supports are obtained by `(1 2)(6 7)`, including the induced
block renaming/transposition.  The machine-readable ledger records every
member and every new matching.  All 108 representative residual cases were
replayed on dense exact rational source matrices.

## Cap-minor theorem

For each of the 34 supports, the audit selects one of the unchanged identity
blocks `A03,A16,A27,A45` as cap.  The displayed triangle contains every site
pair on which that cap can possibly have a response.  Therefore all 108
forbidden response entries are the **zero polynomial** for arbitrary block
coefficients.  Equivalently, the forbidden response matrix has rank zero,
all of its positive-size minors vanish identically, and its kernel is the
entire nine-dimensional cap space.

Take `K=I3`.  Since the cap block is also `I3`, its four activity factors are

```text
kappa=(K00,K11,K22)=(1,1,1),   s=<K,I3>=3.
```

Over characteristic zero this is an active clean cap.  This certificate is
strictly stronger than the requested implication: it uses neither normalized
pure rows, same-source reciprocity, nor a common-zero assumption.  Those
hypotheses remain compatible but are unnecessary in the two-block layer.

## The arbitrary `A01,A23` locus

This load-bearing direct family has

```text
R_ab=P_aQ_b+A01[a,b]A23[b,a]V[b,b].                 (1)
```

Regardless of whether the six equations (1) vanish, cap `16` with triangle
`027` is active clean for `K=I3`: the only possible responses are `07` and
`27`, both internal to that triangle.  Thus every coefficient point of the
arbitrary `A01,A23` locus—and in particular every six-residual common zero—
routes to the active-cap branch.

## Scope

There is no surviving inactive common-zero family among the 34 two-block
supports.  Combined with the parent theorem, the zero-, one-, and first
source-changing two-block layers are closed.  A genuinely new support escape
must use at least three off-family site blocks.  Those larger supports are not
classified here, so this is not yet the full support dichotomy or a full-
conjecture proof.  No broad CEGAR or D12 data was used.

Parent manifest:
`73a0b8e1e9e3934ce74f77506b85748c8f147219fecb53992ca122b44fb7a3bb`.
