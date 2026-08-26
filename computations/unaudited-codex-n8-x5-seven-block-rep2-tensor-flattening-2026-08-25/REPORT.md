# Rep2 tensor flattening and characteristic lift audit

## Outcome

The tensor/contraction route does not yet close representative 2 over
characteristic zero.  It does isolate a sharp characteristic-two
obstruction: 43 binary-color amplitudes form a deletion-minimal inconsistent
system over `F2`, without using the rank-one guard, either carrier incidence,
or the cap67 adjoint equations.  That obstruction is parity/Boolean-specific.
The same 43 equations have both a literal `F3` point and an explicit rational
point, so the `F2` certificate does **not** lift to `Q`.

Representative 2 therefore remains unresolved.  The result prevents a false
promotion of the small `F2` core and identifies exactly where a future
rational contraction must use more information.

## Source-labelled tensor census

The exact 13 supported matching terms were independently rebuilt for

```text
fixed    {03,16,27,45}
variable {04,12,35,67}
added    {06,14,17,23,26,56,57}.
```

All 127 complementary-quotiented bipartitions were enumerated.  The smallest
termwise rank-sum bound is the split `0123467 | 5`.  Its site-5 sources group
as

```text
A35: terms 5,7,9,11       A45: terms 0,3,4,12
A56: terms 2,8            A57: terms 1,6,10.
```

The five `A56/A57` terms lie in the common site-5 line `span(u)`.  Even after
using that exact rank-one contraction, the termwise sum bounds are 21 in the
binary restriction and 29 in the ternary tensor, versus GHZ flattening ranks
2 and 3.  Thus no naive subadditive flattening-rank identity can prove the
required carrier dichotomy.

## Exact `F2` core and certificate

Z3's minimized unsat core contains 43 amplitude equations: the target-one
word `00000000` and 42 target-zero words.  The core contains no guard,
incidence, adjoint, or nonzero-rank assertion.  Independent deletion replay
shows that removing any one of the 43 equations makes the Boolean system
satisfiable.

The package retains:

- the 43-equation SMT input;
- a 4.8 MB Z3 proof object;
- the exact word ledger and 43 deletion witnesses/statuses;
- an executable validator that reruns UNSAT and all 43 SAT deletions.

This is a theorem only over `F2`, where every coordinate obeys the Boolean
field identity `x^2=x` and signs collapse.

## Failure to lift

The minimized core is satisfiable over `F3`; the literal 103-coordinate model
is retained and independently replayed modulo 3.  More strongly, setting all
unlisted coordinates to zero gives this exact rational solution:

```text
a04_01=1,    a06_10=-1/2, a12_01=1,
a14_00=1,    a14_10=1,    a17_00=-2,
a17_10=-1,   a23_01=-1,   a26_01=-1,
a26_12=1,    a35_01=-1,   a35_10=1,
a67_01=-1,   a67_11=1,    u0=1, v0=1, v2=1.
```

Literal `Fraction` replay gives zero residual on all 43 equations.  An exact-Q
19-variable zero-pattern chart independently returns `NONUNIT` in 0.036 s.
The half and negative coordinates make explicit why the Boolean certificate
cannot be read as a rational identity.

The rational point violates 13 of the other binary-color equations.  It is a
countermodel to lifting the **43-core identity**, not a point of the complete
pair01 system and not a counterexample to rep2 closure.

## Scope and next obligation

Proved:

- exact deletion-minimal `F2` obstruction on 43 source-faithful amplitudes;
- exact `F3` and `Q` countermodels to any lift based only on those equations;
- exhaustive bipartition census ruling out the elementary termwise-rank route.

Not proved:

- satisfiability of all pair01 equations over `Q`;
- rank-one rep2 closure;
- forced cap45/star1 or cap03/star6 activity.

A future rational proof must use equations outside the 43 core (most likely
the guard/incidence/adjoint equations together with additional colors) or a
different source-labelled contraction.  Repeating the sealed Gröbner
geometry is not warranted.

Parent rep2 manifest:
`4539834523323399bf969703aef09dc18e578d5c2e0800d592144f048b14c4f5`.
