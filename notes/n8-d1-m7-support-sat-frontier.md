# N = 8 D1: exact seven-cell support-SAT frontier

Date: 2026-08-08.

Generator/verifier:
[`computations/search_n8_d1_m7_support_sat.py`](../computations/search_n8_d1_m7_support_sat.py).

This is the next layer after the exact \(m\leq6\) closure.  It freezes a
complete Boolean necessary-condition problem for exactly seven active,
(E1)-admissible cells outside \(\Sigma\).  It does **not** claim SAT or
UNSAT, and a Boolean survivor would not by itself be an exact source.

The subsequent exact
[`anchor-normal-form cover`](n8-d1-m7-anchor-normal-form-cover.md) reduces
the search to 26 anchor-unit branches over 22 off-support orbits.  A solver
should use that quotient rather than attack the undifferentiated CNF first.

## 1. Exact encoded statement

There is one Boolean variable for each of the 217 (E1)-admissible aggregate
cells: 89 in \(\Sigma\) and 128 outside it.  The encoding imposes:

1. exactly seven of the 128 off-\(\Sigma\) variables are true;
2. the six committed D1 live/harm/(E2) cells are true;
3. a matching term is true exactly when all of its cell variables are true;
4. each target-pure fibre has at least one true matching term; and
5. every target-zero fibre has zero or at least two true matching terms,
   never exactly one.

Item 4 covers \(b^8,c^8,a^8\), the pure-a words on both six-site deletions,
and pure-a residue.  Item 5 covers every mixed word of the full 6561-word
output system, both 729-word six-site systems, and the 81-word residue
system.  Thus all

\[
                         6561+729+729+81=8100
\]

fibres are represented.  The zero-or-at-least-two rule is a necessary
support shadow of exact cancellation: a nonzero coefficient cannot be a
single nonzero monomial.

This formulation includes all \(3+4\) anchor types at \(m=7\), including
four-small-residue and repaired two-residue-edge traces.  It is not obtained
by merely adjoining one cell to the \(m=6\) orbit.

## 2. Deterministic CNF

The DIMACS encoding has:

| quantity | count |
|---|---:|
| base support variables | 217 |
| shared matching-term ANDs | 368,388 |
| total Tseitin variables | 1,089,745 |
| clauses | 4,357,876 |
| bytes | 79,697,108 |

Matching conjunctions are shared by their exact cell set.  A linear
prefix/suffix OR construction encodes “not exactly one.”  The exact-seven
condition uses variables \(p_{i,j}\) for “the first \(i\) inputs contain at
least \(j\) true cells,” through \(j=8\), followed by
\(p_{128,7}\wedge\neg p_{128,8}\).

The verifier exhausts 1024 rows of the exact-counter recurrence and 510 rows
of the cancellation recurrence.  In particular it retains the complete
\(j=1\) equivalence

\[
             p_{i,1}\longleftrightarrow p_{i-1,1}\lor x_i.
\]

An exploratory encoding mistakenly replaced one instance of this recurrence
by a unit clause.  That file was rejected before freezing and is not part of
the repository.  The committed file is the corrected encoding.

Frozen DIMACS digest:

~~~text
4f547d43acf27781c02a89d7c108bdcce8021d69181539a543ea5d887f6770d6
~~~

## 3. Solver status

**OPEN.**  The direct 17.8 MB SMT formulation and a full Tseitin SAT attempt
did not return a verdict within 120--180 seconds with the available Z3
binary.  A smaller exact CEGAR run produced successive models with 56, 158,
and 110 newly violated fibres; after adding 330 exact fibre constraints the
next solve timed out.  These are performance observations, not mathematical
evidence for SAT or UNSAT.

The script therefore prints `NOT_RUN` by default.  `--solve` is explicitly
non-certifying: `SAT` must be followed by direct evaluation of all 8100
fibres and symmetry quotienting, while `UNSAT` must be accompanied by a
checked proof certificate before this note can change status.

## 4. Reproduction

~~~text
python3 computations/search_n8_d1_m7_support_sat.py
python3 computations/search_n8_d1_m7_support_sat.py \
  --emit-cnf /tmp/n8-d1-m7.cnf
python3 computations/search_n8_d1_m7_support_sat.py \
  --emit-cnf /tmp/n8-d1-m7.cnf --solve --timeout 180
~~~

Frozen ledger digest:

~~~text
5e0a2de2749b4d63f5aca4c18349200f0231e516ca0c7209bd4608958521036f
~~~

## 5. What remains

The immediate bounded job is to solve this projection with a proof-producing
SAT backend or a complete CEGAR/orbit enumeration.  Each projected survivor
then needs its exact polynomial ideal; Boolean support feasibility cannot
establish an exact counterexample.  Independently, D1 supports with eight or
more off-\(\Sigma\) cells and all higher orders remain open.
