# The unrestricted six-site weighted closure needs at least twenty-two new cells

This note records the exact support and phase boundary after allowing new
monochromatic coordinate cells in the six-site Hamiltonian-cover module.  The
two certified layers are:

1. every support extension with no mixed singleton fibre uses at least twenty
   new cells, and this is sharp;
2. after adjoining universally valid odd-phase-core clauses, the exact lazy
   optimization bound rises to twenty-two additions; in particular every
   35-cell no-singleton extension has an inconsistent exact-binomial subsystem,
   and the intervening 36-cell layer is excluded as well.

Indeed, nonzero cell weights cannot cancel a singleton monomial, and the
binomial equations in any weighted extension must be mutually consistent.
Thus any extension that can actually be weighted needs at least 37 cells.  The
conclusion uses the certified no-singleton support bound and only universally
valid phase clauses; it does not assume that all mixed fibres remain binomial.
The static exact-35 CNF calculation below independently confirms the minimum
equality layer, while the lazy optimum jump also excludes 36 cells.  A portable
DRUP trace for the static calculation remains pending.

## 1. Exact minimum support closure

The seed has fifteen cells: nine diagonal cells from the three pure factors
and six decorated cells from the two extra factors.  The unrestricted universe
has

\[
                 9\binom 62=135
\]

cells (uv;ab), including every new diagonal cell (uv;ii).

The script

```text
computations/optimize_hamiltonian_cycle_cover_closure.py
```

uses a support variable (x_e) for each of the 135 cells.  Seed variables are
hard true, and every nonseed cell has the unit soft clause

\[
                              \neg x_e.
\]

Thus the RC2 cost is exactly the number of added cells.  After each optimum is
returned, all (3^6) words and all fifteen perfect matchings are enumerated.
If a mixed word (c) has the unique supported term (M), the optimizer adds
the universally valid clause

\[
 \bigvee_{e\in M}\neg x_e
 \quad\vee\quad
 \bigvee_{R\ne M} y_{\,R\setminus M}.                    \tag{1}
\]

Here (y_A\leftrightarrow\bigwedge_{e\in A}x_e) is encoded in both directions;
strict-superset requirements are deleted because they are redundant.  Clause
(1) says exactly that (M) disappears or a distinct matching in the same word
appears.  Every no-singleton support satisfies every learned clause, including
clauses learned from other supports.

The successive exact lower bounds on the number of additions were

```text
0, 9, 10, 12, 15, 15, 16, 18, 19, 19, 19, 20, 20.
```

After 482 singleton-trigger clauses, RC2 returned a valid closure at cost
twenty.  Since the learned formula is a relaxation of the full no-singleton
problem, its optimum (20) is a lower bound; the re-enumerated returned model
is the matching upper bound.  Therefore:

> **Minimum-closure lemma.**  An unrestricted extension of this fifteen-cell
> seed in which every nonempty mixed fibre has at least two terms contains at
> least (35) cells.  Equality is attained.

The proof can be rerun with

```bash
.venv/bin/python computations/optimize_hamiltonian_cycle_cover_closure.py \
  --order 6 --solver cadical195
```

The displayed minimum support has twenty added cells:

```text
01;20
02;01 02;02 02;21
03;02 03;21 03;22
04;00 04;20 04;21
15;00
25;12 25;20 25;22
35;10 35;12 35;20
45;02 45;10 45;12
```

Its pure-fibre sizes are ((2,1,2)), and its complete mixed histogram is

\[
                              \{2:71\}.                  \tag{2}
\]

Thus all 71 nonempty mixed fibres are exact binomials.

## 2. A three-row phase contradiction

Orient each binomial row as its first enumerated term minus its second.  Three
fibres of the support above are

\[
\begin{array}{c|l|l}
c&\text{first term}&\text{second term}\\ \hline
000002&01;00\ 23;00\ 45;02&04;00\ 15;02\ 23;00\\
000122&01;00\ 24;02\ 35;12&03;01\ 15;02\ 24;02\\
011102&03;01\ 12;11\ 45;02&04;00\ 12;11\ 35;12.
\end{array}                                               \tag{3}
\]

Their Laurent exponent rows obey the literal cell-by-cell identity

\[
              D_{000002}-D_{000122}-D_{011102}=0.         \tag{4}
\]

Every canceling binomial requires (x^{D_c}=-1).  Raising these equations to
the coefficients in (4) makes the left side (1), whereas the right side is

\[
                       (-1)^{1-1-1}=-1.
\]

Hence no assignment of nonzero complex cell weights cancels all mixed fibres
of this minimum support.  The checker

```bash
python3 computations/verify_n6_minimum_closure_phase_obstruction.py
```

independently enumerates the 74 nonempty fibres, verifies (2), pins all six
terms in (3), and checks (4) as a signed multiset identity.  It uses no SAT,
MaxSAT, FLINT, or floating-point package.

The phase-consistent optimizer mode feeds all unit three-row circuits back as
exact support-breaking clauses:

```bash
.venv/bin/python computations/optimize_hamiltonian_cycle_cover_closure.py \
  --order 6 --solver cadical195 --require-phase-consistency
```

For the first optimum there are 73 such unit circuits.  The standalone checker
reconstructs all 71 dense exponent rows, finds exactly these 73 three-row
circuits, and verifies a signed unit dependence for every one.

The support-breaking clause for one inconsistent core (mathcal C) deserves
to be explicit.  Let (G) be the union of the cells in its displayed pairs.
For each other matching (R) in an affected word, put

\[
 A_{c,R}=M_R(c)\setminus
       \bigl(M_i(c)\cup M_j(c)\bigr),
 \qquad y_A\longleftrightarrow\bigwedge_{e\in A}x_e.
\]

The optimizer adds

\[
       \bigvee_{e\in G}\neg x_e
       \quad\vee\quad
       \bigvee_{(c,R):R\notin\{i,j\}}y_{A_{c,R}}.         \tag{5}
\]

If a displayed term disappears, the first disjunction permits it.  If all
displayed terms stay, consistency requires at least one affected fibre to stop
being that exact binomial, and the second disjunction says precisely that a
third matching appears.  A fibre gaining four or more terms also satisfies
(5), since at least one of its third-term selectors is true.  Removing a
strict-superset requirement is safe: whenever that superset is present, its
smaller requirement already enables another third term.  Hence every support
whose exact-binomial subsystem is consistent satisfies every phase-core
clause, without any assumption that all its fibres have size two.

After adding all 73 checked clauses (5), one further cost-twenty support had 75
singletons and supplied 75 more universally valid clauses (1).  The resulting
relaxation had exact RC2 optimum 22; no cost 21 was skipped.  This proves the
stronger checkpoint:

> **Phase-consistent closure lower bound.**  If an unrestricted extension of
> the six-site seed has no mixed singleton and its exact-binomial Laurent
> subsystem is consistent, it contains at least (15+22=37) cells.

In particular, every actually weighted extension satisfies the hypothesis,
even if some other mixed fibres have more than two terms.  Subsequent
cost-twenty-two optima still had 114, 99, and 8 singleton fibres respectively;
the running exact search may raise the bound further.

## 3. Full at-most-35 phase formula

The stronger certification driver

```text
computations/search_n6_full_closure_phase.py
```

replaces lazy singleton discovery by the complete Boolean formula.  Its
semantics are as follows.

* There are 135 support variables (x_e), the fifteen seed variables are
  true, and a CNF totalizer imposes (sum_e x_e\leq35).
* For every word (c\in\{0,1,2\}^6) and every one of the fifteen perfect
  matchings (M), a variable (t_{c,M}) is defined in both directions by

  \[
                  t_{c,M}\longleftrightarrow
                  \bigwedge_{e\in M(c)}x_e.              \tag{6}
  \]

* For every mixed (c) and every (M), the clause

  \[
                 \neg t_{c,M}\ \vee\!
                 \bigvee_{R\ne M}t_{c,R}                 \tag{7}
  \]

  forbids (M) from being the unique supported term.  No upper bound on a
  fibre size is imposed.
* If exact binomial patterns
  (E(c;i,j)=t_{c,i}t_{c,j}\prod_{k\notin\{i,j\}}\neg t_{c,k})
  have Laurent rows with an odd integer dependence, they cannot coexist in a
  weighted source.  The learned clause is the literal negation

  \[
                         \bigvee_{E\in\mathcal C}\neg E.  \tag{8}
  \]

  Before (8) is added, exact signed-Hermite reduction checks that the named
  rows are inconsistent.  Unit three-row circuits are batched; a checked
  FLINT odd relation is the fallback.

Thus every clause has an independently stated semantic meaning.  If the final
formula is UNSAT, every no-singleton support of size at most 35 has an
inconsistent exact-binomial subsystem, a necessary obstruction even when
other fibres have three or more terms.

With proof logging enabled, the driver records the named semantic cores, the
final DIMACS formula, its SHA-256 digest, and a deletion-free DRUP trace:

```bash
.venv/bin/python computations/search_n6_full_closure_phase.py \
  --cap 35 --minimum 35 \
  --solver cadical195 --proof-solver glucose4 \
  --proof-prefix computations/certificates/n6-full-closure-phase-exact35
```

The lower cardinality constraint uses the already proved minimum-closure lemma,
so this formula isolates the equality layer rather than reproving that lemma.
The search backend returned `UNSAT` after the first batch of all 73 cores; the
final formula has 12,212 variables and 59,031 clauses.  Portable proof
generation and replay use

```bash
.venv/bin/python computations/verify_n6_full_closure_phase_certificate.py \
  computations/certificates/n6-full-closure-phase-exact35
```

The verifier does not trust the stored phase clauses: it reconstructs every
named row from its word and matching numbers, checks exact signed-Hermite
inconsistency, rebuilds the final CNF byte for byte, verifies its SHA-256, and
then checks every deletion-free DRUP addition by reverse unit propagation.

Current certificate status: CaDiCaL returned the exact-35 `UNSAT` verdict in
about 18.5 minutes.  The subsequent Glucose4 proof run was stopped at total
elapsed time 60:07 after about 41.5 minutes of proof search, with stable memory
but no completed trace.  The older generator deliberately wrote no partial
files, so no `.cnf`, `.json`, or `.drup` bundle is claimed and replay has not
yet been performed.  The generator now writes the semantic CNF/JSON bundle
before beginning any future proof replay and marks an unfinished proof by a
null line count.
