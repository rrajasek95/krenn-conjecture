# A load lemma closes every three-block support

Status: **all 1,140 three-added-block supports have a coefficient-independent
active clean cap.**  There are no three-block evaders.  The first supports on
which this structural fixed-cap method can fail require four added blocks.

## Response-support graph criterion

For a fixed identity cap `pq`, form a graph `H_pq` on the six residual sites:

```text
ab is an edge of H_pq
iff pa and qb are source-supported, or pb and qa are source-supported.
```

Every literal response of cap `pq` is supported on an edge of `H_pq`.  Hence,
if the vertices used by `H_pq` fit in a three-set `T`, all 108 response entries
outside triangle `T` are zero polynomials for arbitrary source coefficients.
Taking `K=I3` gives

```text
forbidden response rank = 0,   kernel dimension = 9,
kappa=(1,1,1),                 <K,A_pq>=<I3,I3>=3.
```

Thus in characteristic zero, `pq/T/K` is an active clean cap.  This is a
pure support criterion: it requires no residual equations, pure equations,
or coefficient cancellation.

## Pigeonhole proof through three additions

The four identity edges

```text
03, 16, 27, 45
```

form a perfect matching.  In the base four-cycle graph, each endpoint of a
fixed cap has one external neighbour, so a cap starts with at most two
external response vertices.

Every off-family edge joins vertices belonging to two distinct fixed caps;
call this one endpoint-load on each.  With `m` added edges the total load over
the four fixed caps is `2m`.  For `m<=3`, some cap has load at most one:

```text
sum loads <= 6 across four caps  =>  min load <= 1.
```

That cap has at most `2+1=3` external neighbours, so its response graph fits
inside a triangle.  The criterion above supplies an active clean cap.  This
proves the zero-through-three-block theorem without enumeration.

## Exact three-block classification

The audit nevertheless exhausts all

```text
C(20,3)=1,140
```

three-edge additions.  Under the exact frozen guard symmetry
`< (1 2)(6 7) >`, they form 579 orbits: 18 singleton and 561 doubleton.
Every support has a stored fixed-cap/triangle certificate; the deterministic
certificate census is `03:796`, `16:228`, `27:116`.  There are zero evaders.
The support calculation is exact, and 257 distributed dense rational sources
independently replay the forbidden responses and all four activity factors.

Consequently no inactive common-zero family survives at three blocks.  The
result is stronger than the requested implication because it does not assume
that the six residuals have a common zero.

## Sharp first boundary at four blocks

The load argument is sharp: with four additions all four cap loads can equal
two.  A bounded support-only diagnostic of all `C(20,4)=4,845` cases finds:

```text
264 supports evade every fixed-identity triangle certificate;
 24 supports evade every fixed-identity triangle and star certificate;
 12 exact order-two orbits among those 24.
```

The twelve representatives are:

```text
01,23,46,57    01,23,47,56
01,24,36,57    01,24,37,56
01,25,36,47    01,25,37,46
06,13,24,57    06,13,25,47
06,14,23,57    06,14,25,37
06,15,23,47    06,15,24,37
```

These are **not** proved cap-free.  Only the coefficient-independent fixed-
identity certificate has disappeared.  For a chosen carrier `C`, the next
exact conditions are coefficient-dependent:

```text
rank L_C <= 8
and each of K00, K11, K22, <K,A_pq> is nonzero on ker L_C.
```

Equivalently, the response minors must produce a nonzero kernel and none of
the four activity rows may lie in the row space of `L_C`.  The present audit
records each fixed-cap response-support graph but does not solve these minor
systems or inspect non-identity caps.

## Scope

Combined with the parent packages, every support with zero, one, two, or three
off-family site blocks is closed.  The 24 four-block structural evaders are
the first coefficient-dependent boundary; their cap equations remain open.
This is not the full support dichotomy or a full-conjecture proof.  No broad
CEGAR or D12 data was used.

Parent manifest:
`139a5270a384a36d6a1b3312dd6e1a0efba0cafe76912a179c973039e1464297`.
