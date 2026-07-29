# Representative Laurent certificates versus exhaustive support coverage

This note separates two logically different parts of the six-site
low-rank computation.

* The exhaustive result is the lexicographic CEGAR proof in
  `proofs/low-rank-graph-laurent-obstruction.md`.  Its Boolean formula
  overapproximates every complex support chart, lex leaders retain at least
  one member of every finite relabeling orbit, every learned clause is an
  exact Laurent or cancellation implication, and terminal UNSAT excludes
  every chart in the stated rank-graph case.
* The certificates below are small, solver-independent examples of the
  algebra behind individual learned clauses.  They do not by themselves
  enumerate all charts.  Their role is to make the local characteristic-zero
  obstruction inspectable without trusting SAT model order or an UNSAT
  backend.

For a coloring `c` and perfect matching `M`, let `a(c,M)` be the integer
exponent vector of the corresponding supported Laurent monomial.  An exact
two-term mixed fiber `{M,N}` gives

\[
 x^{d_c}=-1,\qquad d_c=a(c,M)-a(c,N).                    \tag{1}
\]

Thus an integer identity `a(t,Q)-a(t,P)=sum_j z_j d_(c_j)` with odd
`sum_j z_j` forces the `P` and `Q` terms of the target fiber to be negatives
of one another.  If the target has exactly one further supported term, its
zero coefficient equation is impossible.  If instead an odd combination of
binomial differences is zero, multiplying (1) gives `1=-1` directly.

## Four compact residual certificates

The following identities are exact coordinate identities in the formal
entry/factor variables of the displayed support charts.

### `F=2P2+2P1`

Take exceptional edges `{01,23}`.  The three source colorings

\[
 c_1=000001,\qquad c_2=000002,\qquad c_3=000012
\]

all have exact support `{1,14}`.  Put
`d_j=a(c_j,1)-a(c_j,14)`.  The target coloring `t=000011` has exact support
`{0,1,14}`, and

\[
 a(t,14)-a(t,1)=-d_1+d_2-d_3.                            \tag{2}
\]

The right side has odd coefficient sum, so target matchings 1 and 14 cancel,
leaving the supported matching-0 monomial equal to zero.

### `F=P3+3P1`

Take exceptional edges `{01,12}`.  The source colorings

\[
 c_1=000011,qquad c_2=001000,qquad c_3=001010
\]

all have exact support `{2,9}`.  With
`d_j=a(c_j,2)-a(c_j,9)`, coloring `t=000001` has exact support `{1,2,9}` and

\[
 a(t,9)-a(t,2)=-d_1-d_2+d_3.                             \tag{3}
\]

Hence target matchings 2 and 9 cancel, leaving its supported matching-1
monomial equal to zero.

### `F=P2+4P1`

Take exceptional edge `{01}`.  The colorings

\[
 c_1=000001,qquad c_2=000002,qquad c_3=000012
\]

all have exact support `{0,4}`.  Put
`d_j=a(c_j,0)-a(c_j,4)`.  Coloring `t=000011` has exact support `{0,4,11}`,
and

\[
 a(t,4)-a(t,0)=-d_1+d_2-d_3.                             \tag{4}
\]

The first two target terms cancel and the matching-11 monomial remains.

### `F=6P1`

There are no exceptional edges.  Three exact binomial fibers are

\[
\begin{array}{c|c}
c_1=020001&\{9,10\}\\
c_2=020011&\{3,6\}\\
c_3=020021&\{4,7\}.
\end{array}
\]

Orient each difference in the displayed matching order.  Direct integer
comparison gives

\[
 -d_1-d_2+d_3=0.                                        \tag{5}
\]

The coefficient sum is odd, so (1) and (5) give `1=-1`.

The complete factor supports for these four charts are hardcoded in
`computations/verify_small_laurent_f2_certificates.py` and
`computations/verify_small_laurent_f1_f0_certificates.py`.  The scripts
reconstruct all `3^6=729` coefficient fibers, verify every forced anchor,
check that constant fibers are nonempty and mixed fibers are never
singletons, confirm every displayed exact support, and then check
(2)--(5) coordinate by coordinate.  No SAT formula or solver is used.

## A generalized `3P2` example

Some learned charts require more than one binomial cancellation.  The exact
`3P2` chart in `computations/verify_generalized_laurent_3p2.py` has a
rank-25 binomial lattice with a coordinate minor of determinant `+/-1`.
After quotienting by its sign character, three four-term fibers give

\[
 x^{e_1}=1,qquad x^{e_2}=-1,qquad x^{e_3}=1,
 \qquad -e_1-e_2+e_3=0.                                  \tag{6}
\]

Multiplication forces `1=-1`.  The verifier reconstructs the complete chart
and audits the unimodular quotient and (6) with exact arithmetic.  The
general power-relation lemma and full fiber list are recorded in
`notes/generalized-laurent-elimination.md`.

## What the exhaustive computation adds

Equations (2)--(6) eliminate five particular labeled support charts.  The
exhaustive verifier repeatedly obtains an arbitrary remaining lex-minimal
chart, derives a sound exact-fiber clause from the same Laurent lemma, and
continues until the necessary support formula is UNSAT.  Consequently:

1. exact arithmetic proves each learned clause locally;
2. lex constraints only remove redundant relabelings and retain an orbit
   representative;
3. SAT supplies finite coverage of all remaining Boolean support charts;
4. terminal UNSAT, not any one representative identity, proves the universal
   rank-graph obstruction.

This division is important.  The representative scripts are independent
audits of the algebraic cut mechanism, while the recorded lex/SAT run is the
certificate of exhaustive coverage.  Neither is silently substituted for
the other.

