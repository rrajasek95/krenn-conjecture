# Filtered Laurent holonomy on a two-adic minimum face

## Outcome

There is a gauge-invariant obstruction which is strictly stronger than the
valuation replacement graph.  Suppose several mixed coefficient fibres each
have exactly two lowest-valuation matching terms, separated from every other
term by a gap `delta_i`.  An odd integer dependency among the corresponding
Laurent exponent differences forces

\[
                         \min_i\delta_i\leq \nu(2).        \tag{1}
\]

Thus an odd circuit whose unused terms all lie more than one two-adic level
above its selected pair is impossible.  Exact binomial fibres have infinite
gap and recover the usual odd-sign contradiction.  Unlike an odd cycle in
the rainbow replacement graph, this obstruction can use different
complements in different fibres.  It is unchanged by every endpoint-colour
gauge, so repeated color-balanced rescaling cannot remove it.

The 31-cell plateau in
`valuation-rainbow-descent-cycle.md` is killed by this invariant: its complete
336-state replacement graph is bipartite, but three exact binomial fibres
have `d_3=d_1+d_2`.

The missing uniform implication is false at the order-zero tropical level.
For the two-edge star valuation, every one of the 729 generator initial forms
vanishes at the all-ones residue point and the saved degree-nine residual has
an odd-coefficient, globally minimum rainbow monomial of valuation `-3`.
Nevertheless every coefficient fibre has six, rather than two, lowest terms,
so no near-binomial circuit is present.  The known four-row first-jet
certificate obstructs this particular point one level later.  Consequently
the mandatory negative residual monomial plus the generator initial forms
does not force (1); any universal arithmetic continuation must retain
higher-jet data or handle multi-term leading fibres directly.

The finite assertions are audited by
`computations/verify_valuation_filtered_laurent_circuit.py`.

## 1. The filtered odd-circuit lemma

Let `K` be a discretely valued characteristic-zero field with residue
characteristic two.  Put `e=nu(2)>0`.  Give every nonzero aggregate cell a
value `x_s in K^*`.  For a decorated perfect matching `M`, write

\[
                         X_M=x^{a_M}.                       \tag{2}
\]

For mixed fibres indexed by `i`, choose two terms `M_i,N_i` of the common
minimum valuation `mu_i`, and assume all remaining terms have strictly
larger valuation.  Define

\[
 \delta_i=\min_{L\ne M_i,N_i}\bigl(\nu(X_L)-\mu_i\bigr),  \tag{3}
\]

with `delta_i=+infinity` if the fibre is exactly binomial, and orient

\[
 d_i=a_{M_i}-a_{N_i},\qquad q_i=X_{M_i}/X_{N_i}.           \tag{4}
\]

**Lemma 1.1 (filtered odd Laurent circuit).**  Suppose every chosen mixed
coefficient vanishes.  If integers `z_i`, not all zero, satisfy

\[
              \sum_i z_i d_i=0,\qquad \sum_i z_i\equiv1\pmod2,             \tag{5}
\]

then

\[
              \min_{z_i\ne0}\delta_i\leq e.              \tag{6}
\]

**Proof.**  Divide the `i`th coefficient equation by `X_(N_i)`.  Equation
(3) gives

\[
 q_i+1=-\sum_{L\ne M_i,N_i}X_L/X_{N_i},\qquad
                         \nu(q_i+1)\geq\delta_i.           \tag{7}
\]

Let `delta` be the minimum in (6).  The congruence
`q_i=-1 mod m_delta` remains valid after taking any positive or negative
integer power, since `q_i` is a unit.  The exponent dependency in (5) gives

\[
 1=x^{\sum_i z_i d_i}=\prod_i q_i^{z_i}
      \equiv(-1)^{\sum_i z_i}=-1\pmod{\mathfrak m_\delta}. \tag{8}
\]

Hence `nu(2)>=delta`, proving (6).  `QED`

The statement also holds for a non-discrete real-valued extension: use the
valuation ideals `{y:nu(y)>=delta}`.  No choice of uniformizer is involved.

## 2. Gauge invariance

Under an arbitrary endpoint-colour diagonal change

\[
 x_{uv}^{ab}\longmapsto
             \lambda_{u,a}\lambda_{v,b}x_{uv}^{ab},       \tag{9}
\]

every matching monomial in the fibre of a fixed colouring `c` is multiplied
by the same scalar

\[
                         \prod_v\lambda_{v,c_v}.           \tag{10}
\]

Therefore `q_i`, every valuation gap `delta_i`, and the exponent dependency
in (5) are invariant.  A global source scaling likewise multiplies every
six-site matching term by the same cube.  In particular (6) survives every
target-preserving color-balanced gauge and every repetition of such gauges.

This is the precise advantage over a state-graph orientation.  The latter
records only which rainbow networks are connected by one replacement and is
necessarily reversible.  The circuit (5) records multiplicative holonomy
among matching ratios, even when the three replacements never form a state
cycle.

## 3. Exact application to the 31-cell plateau

For the three mixed colourings

\[
 (1,0,0,2,1,1),\quad(1,1,0,2,1,0),\quad(1,1,1,0,1,1),    \tag{11}
\]

the 31-cell support has exactly two matching terms.  With the orientation in
the verifier, their exponent differences obey

\[
                              d_3=d_1+d_2.                 \tag{12}
\]

Taking `(z_1,z_2,z_3)=(1,1,-1)` gives an odd coefficient sum.  All three
gaps are infinite, contradicting Lemma 1.1.  This excludes every nonzero
weighting on that support which cancels all mixed fibres, even though the
complete 736-edge rainbow replacement graph is bipartite.  The obstruction
therefore survives both the two-cycle and plateau-completion countermodels.

The original 13-cell model fails at the preceding, tropical layer: four
mixed fibres are singletons.  A true zero coefficient cannot have a unique
lowest term.  Repairing those four singletons produces the 31-cell support,
where (12), rather than a replacement cycle, is the obstruction.

## 4. Why the negative residual monomial does not force the circuit

Set the valuation of every colored cell on the underlying edges `01` and
`02` equal to `-1`, and set the other 117 cell valuations equal to zero.
For every vertex colouring, exactly the six perfect matchings which pair
vertex zero with vertex one or two have minimum valuation `-1`.  Giving all
their initial residues the value one makes every generator initial form
zero in characteristic two.

This valuation also contains a globally minimum monomial from the actual
integral residual `R`.  One representative, written as endpoint-coloured
occurrences, is

\[
\begin{split}
 \Gamma={}&02_{02}\,02_{11}\,01_{22}\,12_{00}\,15_{11}\\
           &\,35_{02}\,34_{12}\,34_{21}\,45_{00}.       \tag{13}
\end{split}
\]

It matches every one of the eighteen stubs once.  Its three occurrences on
`01` or `02` give `nu(x^Gamma)=-3`; no rainbow network can be lower because
all negative edges meet vertex zero and that vertex has only three stubs.
In the saved first integral residual its orbit row is 1589 and its
coefficient is `-1`.

Thus (13) is simultaneously

1. a genuine odd-coefficient monomial of the degree-nine residual;
2. a globally minimum negative color-balanced rainbow monomial; and
3. compatible with all 729 generator initial forms.

Yet every fibre has six lowest terms.  There is no fibre with exactly two
leading terms, hence no circuit to which Lemma 1.1 applies.  This is a
countermodel to the proposed *incidence implication*, not to Krenn's
conjecture: the all-ones initial point fails at the next two-adic digit.  The
four colourings

\[
 000000,\quad000001,\quad000010,\quad000011               \tag{14}
\]

give the existing rank-`45/46` linearized obstruction.  The arithmetic
frontier is therefore a filtered multi-term initial-ideal invariant which
incorporates (14), not another rescaling of the minimum monomial.
