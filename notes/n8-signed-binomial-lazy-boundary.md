# Lazy signed-binomial boundary at `n=8`, target orbit 39

## 1. Exact outcome

Consider aggregate decorated cells

\[
       (u,v;a,b),\qquad 0\leq u<v<8,\quad a,b\in\{0,1,2\},
\]

with each selected cell assigned weight \(\pm1\).  Fix target orbit 39:

\[
\begin{aligned}
M_0&=01|23|45|67,\\
M_1&=02|13|46|57,\\
M_2&=03|14|27|56.
\end{aligned}                                             \tag{1}
\]

Require that the constant-colour fibre `r^8` has the unique supported
matching \(M_r\), of product weight `+1`.  Require every mixed fibre to be
empty or to contain exactly two supported perfect matchings whose product
weights are opposite.

The cap-22 lazy SAT search

```text
.venv/bin/python computations/search_n8_signed_binomial_lazy_cegar.py \
  --orbit 39 --max-cells 22 --learning hybrid \
  --structural-batch 128 --sign-batch 512 --max-rounds 1000
```

returns

```text
UNSAT orbit=39 max_cells=22 rounds=27 variables=50875
learned_clauses=173398 fibre_gadgets=29 mate_gadgets=386
overfull_cuts=0 pair_constraints=101
```

The runs with caps `16`, `17`, `18`, `20`, and `21` also return `UNSAT`.
The proof-producing Glucose cap-22 run has 58,600 variables and 205,040
final CNF clauses; its preserved deletion-free DRUP trace has 1,065,236
additions ending in the empty clause.

Two independently organized searches also exclude cap 23, although these
two longer runs currently have no independently checked proof trace:

```text
signed lazy (glucose42): UNSAT, rounds=20, variables=132338,
  learned_clauses=480994, fibre_gadgets=420, parity_core_cuts=6,
  pair_constraints=100
support-first (cadical300): UNSAT, rounds=18, variables=114654,
  learned_clauses=403481
```

Thus the solver cross-checks give the sharper lower bound of 24 among the
252 decorated cells.  The certificate-backed boundary retained on disk is
cap 22, and cap 16 has additionally been checked from start to finish by the
small independent DRUP checker.  These are bounded exact-search statements,
not an exclusion of orbit 39 without a cell cap.

## 2. Why the encoding is exact

The base formula has one support bit and one sign bit for each of the 252
cells.  It forces the twelve cells in (1), fixes their signs positive by
stub-sign gauge, and forbids each of the other 104 constant matchings in
each colour.  Thus every constant target coefficient is exactly `+1`.

No mixed-fibre variables are present initially.  Given a SAT model, the
checker directly enumerates all \(3^8\) colourings and all 105 perfect
matchings.

The refinement clauses are consequences of the required property:

1. If a mixed fibre contains one term `T`, a one-way mate gadget says that
   keeping every cell of `T` requires selecting another perfect matching.
   A mate selector implies every cell of the matching outside `T`; cells
   shared with `T` are already true.  Reverse implications are unnecessary.
2. If three or more terms occur, the union of any three selected terms is
   forbidden.  In hybrid mode a recurrent or overfull fibre is instead
   given an exact Tseitin description of all 105 terms, an at-most-two
   sequential counter, and implications excluding cardinality one.
3. If two terms have equal product sign, their common sign variables cancel.
   A parity gate on the symmetric difference of their cell sets, guarded by
   the union of their support bits, forces odd parity and hence opposite
   products.
4. Gaussian elimination over \(\mathbb F_2\) is also applied to all current
   two-term fibres at once.  An inconsistent parity dependency gives a
   sign-independent nogood guarded by the union of the participating terms.
   Any support satisfying that guard either has an illegal third term or
   inherits the same inconsistent sign equations.

Therefore refinement cannot remove a requested signed-binomial support.
If the incremental formula becomes unsatisfiable, the bounded search space
is exhausted.  Conversely, a reported SAT model is accepted only after a
fresh direct enumeration verifies the unique constant terms and every
mixed fibre.

For a proof-producing run, select `glucose42` and give a prefix:

```text
--solver glucose42 --proof-prefix computations/cert_n8_orbit39_cap16
```

The search then writes the final DIMACS formula and a deletion-free DRUP
trace.  The fully checked cap-16 certificate is
`computations/cert_n8_orbit39_cap16.cnf` together with
`computations/cert_n8_orbit39_cap16.drup`.  Verify it independently by

```text
.venv/bin/python computations/verify_drup_certificate.py \
  computations/cert_n8_orbit39_cap16.cnf \
  computations/cert_n8_orbit39_cap16.drup
```

The checker confirms 6,848 variables, 21,986 CNF clauses, and 1,544 RUP
proof additions ending in the empty clause.

The larger cap-22 certificate is preserved as
`computations/cert_n8_orbit39_cap22.cnf` and
`computations/cert_n8_orbit39_cap22.drup`.  The trace ends in the empty
clause; a complete streaming pass by the independent checker is still
expensive because the deletion-free proof is about 1.2 GB.

Orbit 39 has exactly eight coloured-target automorphisms: four fix all
three colours, and four exchange colours `0,1` while fixing colour `2`.
The optional flag `--symmetry-lex` adds seven sound lex leaders on the 252
support bits followed by the 252 sign bits.  The flag is off by default, so
it does not enter the certificates above.  The optional command

```text
--best-prefix computations/n8_orbit39_cap23_best.json
```

records selected cells, their signs, and the complete matching-term lists
of every bad fibre whenever the near-model score improves.

## 3. Scope

This calculation concerns the restrictive parallel-cell chart with
aggregate weights in \(\{0,+1,-1\}\), unique constant matchings, and
binomial mixed fibres.  It does not cover arbitrary complex weights,
constant fibres with cancellation, or mixed fibres with more than two
terms.  In particular, it is not an upper-bound proof for Krenn's
conjecture at `n=8`.
