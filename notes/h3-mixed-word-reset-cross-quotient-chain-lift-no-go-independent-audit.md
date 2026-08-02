# Independent audit of the mixed-word quotient reset

This note independently audits commit `befda3f`.  It confirms its finite
claims and its stated limitation.  It does not construct a source-chain lift,
a relative-Rees generator, or a nonzero filtered differential, and it does
not prove Krenn's conjecture.

## Result

The independent replay returns **PASS**.  Starting only from the two frozen
eight-site rational cell tables, it reconstructs the full (pq) EqSystem by
a bit-mask perfect-matching recursion.  It then constructs the fifteen
vectors

\[
 e_a^{(v)}q^{[2]},\qquad v\in\{1,2,3,4,5\},\quad
 a\in\{0,1,2\},
\]

as a new (243\times15) rational matrix.  It neither imports nor calls the
primary checker.

The exact EqSystem failure ledgers are:

\[
\begin{array}{c|c|c|c|c}
\text{packet}&\text{internal word}&(i,j)&H_{ij}&\delta_{ij}X_i\\ \hline
\text{direct-free}&000000&00&0&1\\
&012112&22&1&0\\
&012212&21&1&0\\
&012212&22&1&0\\
&111111&11&0&1\\
&222222&22&0&1\\ \hline
\text{tilted}&000000&00&0&1\\
&002012&22&1/2&0\\
&022012&02&-3/2&0\\
&022012&20&1/2&0\\
&022012&22&-1/4&0\\
&111111&11&0&1\\
&222222&22&0&1.
\end{array}
\]

There are no other failures among the (9\cdot3^6=6561) coefficients.
Consequently every mixed coefficient used by the reset is a nonzero
EqSystem defect with zero target, not a coefficient available on the source
locus.

## Odd quotient and exact descent witnesses

Let

\[
 D={\cal R}_1q^{[2]}\subset {\cal R}_5,
 \qquad C_q={\cal R}_5/D,
\]

and let (Y_0=e_{00000}).  Independent rational row reduction gives

\[
\begin{array}{c|c|c}
\text{packet}&\dim D&[Y_0]\text{ in }C_q\\ \hline
\text{direct-free}&7&\ne0\\
\text{tilted}&8&\ne0.
\end{array}
\]

For a five-letter word (m), write

\[
 P_m=\iota_{00000}\epsilon_m.
\]

Since ([Y_0]\ne0), this rank-one operator descends to (C_q) exactly when
the coordinate functional (epsilon_m) annihilates (D).  Checking all
fifteen denominator generators gives the complete ledger for the four
mixed tags under discussion:

\[
\begin{array}{c|c|c}
\text{packet}&m&\text{nonzero values on }e_a^{(v)}q^{[2]}\\ \hline
\text{direct-free}&12112&\varnothing\\
&12212&\varnothing\\
\text{tilted}&02012&\varnothing\\
&22012&(v,a,\text{value})=(2,2,1),(4,1,1).
\end{array}
\]

Thus (P_{12112},P_{12212}), and (P_{02012}) descend.  The tilted
(P_{22012}) does not: either displayed denominator generator is already a
boundary witness whose image is the nonzero class ([Y_0]).

## Reset normalization and indeterminacy

For every descended defect with value (r\ne0), scaling (P_m) by
(-\kappa/r) gives output (-\kappa Y_0).  The independently checked values
are

\[
\begin{array}{c|c|c|c|c}
\text{packet}&m&(i,j)&-\kappa/r&\text{output}\\ \hline
\text{direct-free}&12112&22&1/4&(1/4)Y_0\\
&12212&21&1/4&(1/4)Y_0\\
&12212&22&1/4&(1/4)Y_0\\
\text{tilted}&02012&22&5&(5/2)Y_0.
\end{array}
\]

Here (kappa=-1/4) and (-5/2), respectively.  These are valid numerical
normalizations only because the displayed inputs are nonzero guard defects.
On the true EqSystem all of those residuals vanish.

The direct-free packet independently confirms failure of zero
indeterminacy.  Both coordinate functionals annihilate (D), while

\[
 (P_{12112}-P_{12212})[e_{12112}]=[Y_0]\ne0.
\]

The input class is nonzero as well: adjoining (e_{12112}) raises the rank
of the denominator matrix from seven to eight.  Hence the two resets are
genuinely different quotient maps even though their selected guard
coefficients happen to agree.

## Scope check

The audit confirms the primary note's central warning.  (P_m) is an
endomorphism of the packet-specific odd quotient.  Applying it to a formal
EqSystem row merely transports that row's boundary.  After restriction to a
genuine source, the boundary is zero because
(H_{ij}-\delta_{ij}X_i=0).  Nothing in the quotient calculation supplies a
one-higher homotopy whose filtration-lowering boundary is
(kappa Y_0w).

Therefore quotient-level reset is not a source-chain lift.  The missing
object remains a typed syzygy in the relative EqSystem/cap resolution,
together with a theorem that the odd readout is independent of the chosen
lift.  The nonzero difference above shows that such independence cannot be
deduced from arbitrary descended word resets.

## Executable verification

The dependency-free audit is
[audit_h3_mixed_word_reset_cross_quotient_chain_lift_independent.py](../computations/audit_h3_mixed_word_reset_cross_quotient_chain_lift_independent.py).
It uses exact `Fraction` arithmetic and `require`/`RuntimeError` checks, so
optimized Python cannot remove its assertions.  Its frozen ledger digest is

```text
6a45beec7fa5394f8fd2e04847d0f853d4d272add15947b963b5b9ee21b7a2ba
```
