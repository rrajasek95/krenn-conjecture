# Toric binomial rank certificates below four exceptional edges

This note records an exact algebraic refinement of the arbitrary-support
formula.  It is useful for the remaining `|F|<=3` six-vertex rank graphs,
but the current finite search has not yet turned it into an exhaustive
obstruction.

## 1. The binomial lattice lemma

Fix one support chart.  Give every supported exceptional entry and every
supported coordinate of a rank-one endpoint factor its own formal nonzero
variable.  A supported perfect matching at a coloring `c` is a Laurent
monomial `x^{a_(c,M)}` in these variables.

Suppose a mixed coefficient has exactly two supported matchings `M,N`.
The exact coefficient equation is

\[
 x^{a_{c,M}}+x^{a_{c,N}}=0,
 \qquad
 x^{d_c}=-1,
 \quad d_c=a_{c,M}-a_{c,N}.                    \tag{1}
\]

**Lemma 1.1 (even binomial lattice certificate).**  Let `c_1,...,c_s` be
mixed two-term fibers and let `z_1,...,z_s` be integers.  If

\[
 \sum_r z_r d_{c_r}
 =e_{A(i,j)}+e_{A(k,l)}-e_{A(i,l)}-e_{A(k,j)},
 \qquad \sum_rz_r\equiv0\pmod2,                \tag{2}
\]

then the indicated `2 by 2` minor of `A` vanishes.

**Proof.**  Every variable occurring in (1) is nonzero.  Raise the
relations (1) to the possibly negative integral powers `z_r` and multiply.
The right side is `(-1)^(sum z_r)=1`.  Equation (2) makes the left side

\[
 \frac{A(i,j)A(k,l)}{A(i,l)A(k,j)}.
\]

All four entries are nonzero because their exponent coordinates occur in
the supported source monomials.  Cross multiplication gives the claimed
minor identity. `QED`

This strictly extends the fixed-color coefficient rectangle used for
`|F|=4,5`: the other four vertex colors and even the two matchings may vary
between the source fibers.

## 2. Sound nonzero-minor witnesses

For an active exceptional matrix, introduce nine auxiliary variables
`w_(A,I,J)`, one for each `2 by 2` minor.  Require an active matrix to select
at least one witness.  A witness only implies the necessary support
condition

\[
 (A(i,j)\ne0\wedge A(k,l)\ne0)
 \ \vee\
 (A(i,l)\ne0\wedge A(k,j)\ne0).               \tag{3}
\]

Every actual rank-at-least-two matrix extends to this Boolean system by
selecting one genuinely nonzero minor.  If Lemma 1.1 proves the selected
minor zero, the clause forbidding that witness together with the exact
source-fiber supports is therefore sound.  The checker represents exact
fiber supports by Tseitin variables, so a four-fiber certificate produces a
five-literal rank cut after the definitions are installed.

`computations/verify_f3_toric_obstruction.py` implements this construction.
SciPy MILP is used only to propose a short integral combination.  Before a
cut is accepted, ordinary exact integer matrix multiplication verifies (2)
and its parity condition.  Thus floating-point output is never trusted as a
certificate.

## 3. The recurrent `3P2` chart

Let

\[
 M=\{01,23,45\}=F.
\]

In every chart encountered late in the canonical-witness search, all three
exceptional matrices have full support.  Three rank-one edges with both
endpoint supports full form another perfect matching `N`; the remaining
nine rank-one edges have coordinate support.  Hundreds of distinct label
charts occur, but every fully supported selected minor encountered so far
has a four-fiber certificate with coefficients `(+1,-1,-1,+1)`.

For example, take `N={02,14,35}` and the four mixed colorings

\[
\begin{array}{c|c}
 +1&(0,0,1,2,1,2)\\
 -1&(0,1,1,2,1,1)\\
 -1&(1,0,2,2,1,2)\\
 +1&(1,1,2,2,1,1).
\end{array}                                                \tag{4}
\]

If each coloring in (4) has exact support `{M,N}`, the alternating sum of
the four exponent differences is

\[
 e_{A_{01}(0,0)}+e_{A_{01}(1,1)}
 -e_{A_{01}(0,1)}-e_{A_{01}(1,0)},             \tag{5}
\]

and the coefficient sum is zero.  Lemma 1.1 kills that minor.  Notice that
the colors at vertices `2` and `5` vary between corners; this is why the old
fixed-other-colors rectangle audit misses (4).

Up to the global color action, a minor of a fixed exceptional edge has two
orbits: its row and column pairs omit the same color, or they omit different
colors.  Canonical searches for these two cases generated respectively more
than 425 and 200 distinct exact four-fiber cuts before being capped.  No
model-independent implication forcing a member of this certificate family
has yet been proved.  The evidence points to the following precise missing
finite lemma:

> Conditional on a selected nonzero exceptional minor in `F=3P2`, the
> support and translated-fiber clauses force four exact binomial fibers whose
> even exponent combination is that minor.

## 4. Current smaller-graph audit

The earlier closure/rectangle engine gives the following exact relaxation
status:

\[
\begin{array}{c|c}
F&\text{outcome}\ \hline
2P_2\sqcup2P_1&\text{survives after 4 transfers; not all exceptional zero}\
P_3\sqcup3P_1&\text{survives with 0 transfers; all exceptional zero allowed}\
P_2\sqcup4P_1&\text{survives with 0 transfers; exceptional zero allowed}\
6P_1&\text{survives after 15 transfers}.
\end{array}                                                \tag{6}
\]

The first row immediately generates the same kind of four-binomial toric
minor cuts, but a short exploratory run again proliferated past one hundred
charts.  Thus (6) is a status report for a necessary relaxation, not an
existence claim for complex weights.
