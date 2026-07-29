# Exact F3 search in the joint-C3 n=8 slice

This note records an exact finite-field search inside the 84-parameter slice
first explored numerically by
`computations/search_c3_equivariant_n8.py`.  It is a discovery slice only:
neither SAT nor UNSAT over `F3` settles the characteristic-zero conjecture.
A SAT point would have to be lifted and verified over characteristic zero.

## 1. The coupled action and its 84 entry variables

Let

```text
g = (0 1 2)(3 4 5)(6)(7).
```

For a canonical endpoint-colour cell `(u,v;a,b)`, with `u<v`, apply the
generator by

```text
(u,v;a,b) -> (g(u),g(v);a+1,b+1),
```

then reorder the endpoints and their attached colours if necessary.  All
colours are taken modulo 3.  Requiring an aggregate entry to be constant on
these orbits is exactly the joint vertex/colour equivariance used in the
numerical script.

There are `28*9=252` canonical cells.  The action is free on them, including
on the fixed vertex edge `67` because the colours still cycle.  Hence there
are exactly `252/3=84` entry variables.  On edge `67`, the three variables are
the three classes indexed by `b-a mod 3`, agreeing with the circulant matrix
in the numerical parametrization.

The solver-free verifier assigns 84 distinct formal labels through the old
numerical `expand` map and proves that its equality partition is identical to
the independently generated exact cell partition.

## 2. The 2,187 coefficient equations are exhaustive

For a colouring `c`, define `Tc` by

```text
(Tc)_{g(v)} = c_v + 1.
```

This action has order three and is free: a fixed colouring would in
particular require `(Tc)_6=c_6+1=c_6`, which is impossible.  Thus the 6,561
colourings have 2,187 orbits.

If `M` is a perfect matching, then the cell-orbit monomial of `(c,M)` equals
the cell-orbit monomial of `(Tc,gM)` term by term.  Since `M -> gM` permutes
all 105 perfect matchings, the two coefficients are the same polynomial in
the 84 variables.  The target is also invariant: `T` cycles the three pure
colourings and maps every mixed colouring to a mixed colouring.  Consequently
one exact equation per colouring orbit is necessary and sufficient.

The verifier checks this matching-by-matching identity for all
`6561*105` pairs.  The search also collects identical matching monomials with
multiplicity reduced modulo 3; the verifier independently reconstructs and
compares every one of these 2,187 collected equations.

## 3. Seven exhaustive pure-supported-matching branches

The coefficient at the all-zero colouring is 1 in `F3`.  It is a sum of 105
matching monomials, so at least one monomial is nonzero.  Therefore every
solution has a perfect matching whose four pure-zero entries are all nonzero.

The centralizer of `g` in `S8` preserves the joint-equivariant ansatz.  An
independent enumeration of all `8!` permutations finds a centralizer of order
36.  Its action on the 105 perfect matchings has exactly seven orbits, with
sizes

```text
9, 36, 18, 3, 18, 3, 18.
```

Their lexicographically least representatives are

```text
01 23 45 67
01 23 46 57
01 26 34 57
03 14 25 67
03 14 26 57
03 15 24 67
03 15 26 47
```

There is also an equivariant diagonal sign gauge.  Choose signs
`r_v in F3*` with `product_v r_v=1`, and set

```text
s_{v,a} = r_{g^{-a}(v)}.
```

Then `s_{g(v),a+1}=s_{v,a}`, so multiplying an entry `(u,v;a,b)` by
`s_{u,a}s_{v,b}` is constant on coupled cell orbits.  Every pure coefficient
is multiplied by `product_v s_{v,a}=1`, while each mixed zero coefficient is
only rescaled.  The resulting `2^7=128` gauges therefore preserve both the
ansatz and the target.  On a supported perfect matching they can normalize
the first three pure-zero entries to 1; the fourth pair absorbs the sole sign
product constraint and remains nonzero.

Thus imposing value 1 on the first three entries and nonzero on the fourth of
each representative is an exhaustive symmetry split, not a support heuristic.
The verifier checks all 128 gauges, all 16 possible nonzero patterns on every
representative, that every commuting relabeling induces a well-defined
permutation of the 84 cell orbits, and that the seven matching orbits are
disjoint and cover all 105 matchings.

After this normalization, the seven branches have residual centralizer
subgroups of orders `4,1,1,12,1,12,1`.  The SAT search gates an exact ternary
lex-leader for every nonidentity element by its branch selector.  This is
sound because each finite residual orbit has a lexicographically least member;
the gated constraints are inactive in every other branch.

## 4. Exact incremental SAT encoding

Each of the 84 entries is one-hot encoded with values `0,1,2`.  For every
matching monomial, a Boolean `nonzero` variable is the conjunction of its four
entries being nonzero, and a three-XOR chain records the parity of entries
equal to 2.  A one-hot accumulator then adds `0`, `1`, or `2` modulo 3.  When
identical monomials occur twice, the transition is multiplied by 2; a
multiplicity of 3 vanishes exactly in `F3`.

The search starts with the pure equation.  Every candidate assignment is
evaluated exactly on all 2,187 representative equations.  Violated full
equations are appended in batches; matching product circuits are shared
between equations.  Hence this is lazy only in scheduling: each learned
constraint is an exact 105-matching coefficient identity, and a branch may be
declared SAT only after a direct raw enumeration of all 105 matchings on all
6,561 colourings.

Commands:

```bash
.venv/bin/python computations/verify_f3_c3_equivariant_orbits.py
.venv/bin/python -u computations/search_f3_c3_equivariant_n8.py \
  --solver cadical195 --batch 64 --phase sparse
```

The solver-free audit currently reports

```text
PASS cells=252 cell_orbits=84 orbit_size=3 colourings=6561
colouring_orbits=2187 matchings=105 centralizer=36 matching_orbits=7
matching_orbit_sizes=[9, 36, 18, 3, 18, 3, 18]
residual_groups=[4, 1, 1, 12, 1, 12, 1]
equivariant_gauges=128
numerical_partition=matched covariance=all_6561x105
```

The finite-field branch outcomes are recorded in the search log
`computations/search_f3_c3_equivariant_n8.log`; they must not be interpreted
as a characteristic-zero obstruction or counterexample.

## 5. Exact near-points and focused repair searches

Two exact finite-field phenomena help guide the search but are not solutions.

First, a full-support sign assignment was found for which all 6,561 output
coefficients are zero.  This is a nontrivial point of the base locus, not a
realization of `Delta`.  Its `2187 x 84` Jacobian over `F3` has rank 39, and
the `Delta` direction is not in its tangent image.  The optimized dense
solver

```text
computations/search_f3_c3_dense_sign_n8.py
```

encodes the full-support problem directly with 84 sign bits.  Since a
coefficient has 105 terms, if `k` matching products are negative then

```text
sum_M sign(M) = 105 - 2k = k (mod 3).
```

All 2,187 equations therefore become modulo-three counts of shared XOR
products.  The complete lex-reduced CNF has 1,051,983 variables and 3,733,285
clauses.

Second, a gauge-normalized ten-cell assignment in branch 1 realizes every
pure coefficient and 2,186 of the 2,187 representative equations.  Its sole
bad representative is

```text
(0,0,0,0,2,1,1,2),
```

and that mixed fibre contains exactly one supported matching of value 1.  Its
coupled orbit consists of three raw colourings.  The independent direct audit
is

```bash
.venv/bin/python computations/verify_f3_c3_ten_cell_near_point.py
```

and reports

```text
PASS ten-cell F3 C3 near-point: pure orbit exact,
2186/2187 representative coefficients exact, one mixed C3 orbit
(3 raw colourings) has a singleton value-1 term
```

Exact completion searches retaining those ten values are UNSAT through 14
nonzero cell orbits (up to four added orbits): caps 12, 13, and 14 closed in
8, 8, and 7 CEGAR rounds respectively.  These are focused subsearches only;
they do not close branch 1 because a realization may alter or delete a core
entry, or use more cells.  Their reproducible logs are

```text
computations/search_f3_c3_equivariant_branch1_core10_cap12.log
computations/search_f3_c3_equivariant_branch1_core10_cap13.log
computations/search_f3_c3_equivariant_branch1_core10_cap14.log
```
