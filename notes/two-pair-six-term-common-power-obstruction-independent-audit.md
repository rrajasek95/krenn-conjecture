# Independent audit of the complete aligned two-pair obstruction

## 1. Verdict

This is a clean-room adversarial audit of
[the two-pair common-power theorem](two-pair-six-term-common-power-obstruction.md)
and its full aligned-three-field corollary.  Both are correct.  I found no
support, weight-normalization, arbitrary-\(q\), endpoint-order, or
complex-cancellation gap.

The logical strengthening in Section 6 of the primary note is universal:
once the aligned response modules have been split, every hypothetical aligned
solution has exactly two physical active pairs, whether its deviant sets have
size one or two and whether its hard-zero target vectors are coordinate axes
or genuine mixtures.  The only possible support-size profiles are
\((2,1,1),(2,2,1),(2,2,2)\).  The first has an elementary response
contradiction; the latter two have exact arbitrary-\(q\) power obstructions.

The accompanying
[independent checker](../computations/audit_two_pair_common_power_profiles_independent.py)
imports neither the primary builder nor its ledgers.  It uses different site,
edge, colour, variable, equation, and monomial orders.  It reconstructs the
complete \(qF=0\) coefficient matrices, builds all \(1,215\) matching
coefficients from sparse monomial dictionaries, and performs six fresh
unsaturated Singular calculations over \(\mathbb Q\).

This closes the **aligned three-field branch**, not the full Krenn conjecture.
An unconditional descent of an arbitrary multiplier to three aligned line
fields is still required.

## 2. Universal reduction to two physical pairs

In the aligned setup, let \(H_0,H_1,H_2\) be the three nonempty families of
active missing pairs.  The power projection proved in the aligned note says
they have no system of distinct representatives.  Hall's theorem for three
nonempty families gives exactly two possible witnesses:

\[
 \text{no SDR}\quad\Longrightarrow\quad
 \left[
 H_i=H_j=\{P\}\text{ for some }i\ne j
 \quad\text{or}\quad
 |H_0\cup H_1\cup H_2|\le2
 \right].                                                        \tag{A1}
\]

The aligned singleton-collision lemma excludes the first alternative.  Thus
the total union has size at most two.  It cannot have size one: nonemptiness
would make all three families equal to the same singleton, again contradicting
the collision lemma.  Therefore

\[
                         H_0\cup H_1\cup H_2=\{P,Q\},\qquad P\ne Q. \tag{A2}
\]

Each nonempty \(H_i\) is now one of
\(\{P\},\{Q\},\{P,Q\}\).  At most one colour can use \(\{P\}\), and at most
one can use \(\{Q\}\), because equal singleton families are forbidden.  There
can consequently be zero, one, or two singleton colours, giving precisely

\[
                             (2,2,2),\qquad(2,2,1),\qquad(2,1,1). \tag{A3}
\]

In the last profile the two singleton colours necessarily occupy distinct
pairs.  No statement about \(D_i\), target coordinates, or endpoint vectors
entered this deduction.

As a bookkeeping check, the independent script enumerates all \(15^3=3375\)
triples of nonempty families on a four-element ambient universe.  After
removing systems with an SDR and systems with equal singleton families, 78
remain.  Every one has a two-element union, with labelled counts

\[
 \begin{array}{c|ccc}
 \text{profile}&(2,1,1)&(2,2,1)&(2,2,2)\\ \hline
 \text{count}&36&36&6.
 \end{array}                                                     \tag{A4}
\]

These are \(\binom42\) labelled copies of the \(6,6,1\) possible assignments
on a fixed pair set.  The mathematical deduction above is
universe-independent; the census only audits its finite shapes.

## 3. The \((2,1,1)\) response contradiction

Relabel the unique two-pair colour and the two singleton colours so that

\[
               H_0=\{P,Q\},\qquad H_1=\{P\},\qquad H_2=\{Q\}.     \tag{A5}
\]

For \(R=\{a,b\}\), retain the complete ordered endpoint response

\[
 B_{ij}(R)=p_{i,a}\otimes s_{j,b}
            +s_{j,a}\otimes p_{i,b}.                              \tag{A6}
\]

In the split colour-one module, the response with row pair \((0,0)\) is zero.
That module has the single active term \(P\).  Its aggregate coefficient and
its four outside field factors are nonzero, so

\[
                              B_{00}(P)=0.                         \tag{A7}
\]

The same row pair in the singleton colour-two module gives

\[
                              B_{00}(Q)=0.                         \tag{A8}
\]

But the diagonal colour-zero response is supported only at \(P,Q\); equations
(A7)--(A8) make it zero, contradicting its nonzero pure target.  This argument
allows cancellation inside each tensor \(B_{00}(R)\), retains both endpoint
orders, and uses aggregate coefficients only.  It needs neither a deviant-set
hypothesis nor either common-power equation.

The primary and independent checkers also prove the corresponding unrestricted
power ideals are unit.  Those calculations are useful controls but are not a
logical dependency of the aligned corollary.

## 4. Reductions for the power-only profiles

Consider any of the profiles in (A3), with all displayed active coefficients
nonzero.

### 4.1 Arbitrary local dimensions

At each site, choose a linear retraction onto the span of the three field axes
which fixes those axes.  Extending the retraction by \(1\mapsto1\) gives a
unital homomorphism of the square-zero local algebra.  Tensoring over the six
sites fixes every target lift and commutes with matching powers.  A solution
with larger local spaces would therefore project to one with exactly three
local coordinates.  Transverse coordinates of \(q\) have not been assumed
zero; they are removed by a functorial image of the equations.

### 4.2 Arbitrary nonzero weights

For a colour active on both distinct pairs \(P,Q\), the two target coefficients
can be normalized independently by sitewise axis scaling.  This requires
surjectivity of the two outside-support characters

\[
 (t_u)_{u\in U}\longmapsto
 \left(\prod_{u\notin P}t_u,\prod_{u\notin Q}t_u\right).           \tag{A9}
\]

There is a root-free solution.  Choose \(x\in P\setminus Q\) and
\(y\notin P\cup Q\).  In the two character rows, the columns at \(x,y\) are
\((0,1)\) and \((1,1)\), whose determinant is \(-1\).  Set all other site
scalars to one and solve multiplicatively using these two coordinates.  A
singleton colour uses only one outside-support character and can be normalized
at any site outside its missing pair.  The three colours have independent
local axis scalars, so all active coefficients in every profile can be set to
one simultaneously without roots.

The independent checker verifies the unimodular-minor property for all
\(\binom{15}{2}=105\) distinct pair choices.  It also obtains the complete
orbit census: 60 adjacent and 45 disjoint choices.  These are the only two
pair orbits under site relabelling.

### 4.3 The necessary linear equation

In the matching algebra,

\[
                              q\,q^{[2]}=3q^{[3]}.                 \tag{A10}
\]

Thus \(q^{[2]}=F,\ q^{[3]}=0\) implies

\[
                                  qF=0.                           \tag{A11}
\]

Only the \(q\)-block on a lift's missing pair can multiply that four-site
lift without a local square-zero collision.  Consequently (A11) involves
exactly the 18 endpoint-ordered cells of the \(P\)- and \(Q\)-blocks.  For
each six-site coordinate word, the independent builder collects every
contributing active lift before forming a row; it does not separate colliding
words.

Exact rational rank and RREF calculations give:

\[
\begin{array}{c|cc|cc}
 &\multicolumn{2}{c|}{P,Q\text{ adjacent}}
 &\multicolumn{2}{c}{P,Q\text{ disjoint}}\\
 \text{profile}&\text{rows}&\text{rank}&\text{rows}&\text{rank}\\ \hline
 (2,1,1)&33&18&35&18\\
 (2,2,1)&39&18&43&18\\
 (2,2,2)&45&18&51&18
\end{array}                                                       \tag{A12}
\]

All 18 columns are pivots in every case.  Hence the exact kernel condition is
particularly simple:

\[
                              q_P=q_Q=0.                           \tag{A13}
\]

The remaining 13 physical edge blocks are unrestricted, leaving
\(13\cdot3^2=117\) affine coordinates.  This independently reconstructs the
117-dimensional kernels in the primary checker and verifies that its
parameterization loses no branch.

## 5. Clean-room construction of the six affine ideals

For a four-set \(S=\{a,b,c,d\}\) and coordinate word
\((i_a,i_b,i_c,i_d)\), the independent builder forms the coefficient

\[
\begin{aligned}
 &q_{ab}(i_a,i_b)q_{cd}(i_c,i_d)
 +q_{ac}(i_a,i_c)q_{bd}(i_b,i_d)\\
 &\hspace{35mm}
 +q_{ad}(i_a,i_d)q_{bc}(i_b,i_c),                                \tag{A14}
\end{aligned}
\]

then subtracts the corresponding target coefficient.  It represents each
polynomial as an exact dictionary from degree-zero or degree-two monomials to
integer coefficients.  Only after all three matchings and the target constant
have been collected is the polynomial encoded for Singular.  This construction
audits the endpoint orientation explicitly: when an edge is encountered in
the reverse site order, its two colour coordinates are swapped.

There are exactly

\[
                              \binom64\,3^4=1215                   \tag{A15}
\]

coordinate equations in each case, and every one is retained.  The ideals
contain the complete coefficient system (A14) after the exact linear
substitution (A13).  They are affine and unsaturated: no \(q\)-coordinate,
minor, weight, or auxiliary variable is inverted.

The checker sends each independently ordered ideal to Singular over
\(\mathbb Q\), using a variable stream and monomial ordering distinct from
the primary computation.  All six exact Gröbner bases are \([1]\):

\[
\begin{array}{c|c|c|c|l}
\text{profile}&\text{orbit}&\text{variables}&\text{generators}
 &\text{independent ledger SHA-256}\\ \hline
(2,1,1)&\text{adjacent}&117&1215&
\texttt{f3a1bb1a22656b22612c095806b35c5bdd66f8449f87738f813c750f7eb01fc6}\\
(2,1,1)&\text{disjoint}&117&1215&
\texttt{accdf2cd03ae931efe018ee7f3e9857f17404e285cbb9fc5bd97c2e867a7ce5b}\\
(2,2,1)&\text{adjacent}&117&1215&
\texttt{71054f25fc031313a7a8b12214f484116aeef5a9a93b8bb7026c5d65bb7a75a0}\\
(2,2,1)&\text{disjoint}&117&1215&
\texttt{8ef0868c49e00e5d82a7af1903dc67e356b4ae2f7e4e95ed7f107c0be2497482}\\
(2,2,2)&\text{adjacent}&117&1215&
\texttt{7b06d8aad8b9c4eebe180691fc6539643815346265e4dea7857139c2e3b73127}\\
(2,2,2)&\text{disjoint}&117&1215&
\texttt{e5637a34fc001c205eac4d7e79b547cd1fb3c6a6886c78edc665f639ef685b37}
\end{array}                                                       \tag{A16}
\]

A unit ideal over \(\mathbb Q\) remains a unit ideal after scalar extension
to \(\mathbb C\).  In particular, the \((2,2,1)\) controls independently
reconstruct the specific five-term dependency used by the primary corollary,
and the two \((2,2,2)\) calculations independently verify Theorem 1.1.

## 6. Scope and cancellation audit

The active coefficients are defined after all parallel descriptions and
complex cancellation have been aggregated.  Only nonzero aggregate
coefficients are normalized.  The \(qF\) rows collect equal coordinate words,
the matching polynomials collect all three perfect matchings, and the ideals
are unsaturated.  Thus zero edge blocks, rank drops, cancellations among
matching terms, and arbitrary full \(3\times3\) endpoint blocks all remain in
the calculation.

Combining Sections 2--5 gives the primary full aligned-three-field corollary:

* Hall plus singleton collision forces exactly two physical active pairs;
* the \((2,1,1)\) profile dies in the response table;
* the \((2,2,1)\) profile dies by the five-term power ideal; and
* the \((2,2,2)\) profile dies by the six-term power ideal.

This conclusion permits arbitrary one- or two-site deviant sets and genuine
linear mixtures at hard zero-diagonal sites.  It does not prove that an
arbitrary non-pure multiplier decomposes into, or descends to, three aligned
line fields.  That genuinely non-pure descent is the remaining global
frontier.

## 7. Reproduction

Run the full independent audit with:

    uv run python computations/audit_two_pair_common_power_profiles_independent.py

For a fast deterministic rebuild of all matrices, polynomials, and frozen
ledgers without invoking Singular, use:

    uv run python computations/audit_two_pair_common_power_profiles_independent.py --build-only
