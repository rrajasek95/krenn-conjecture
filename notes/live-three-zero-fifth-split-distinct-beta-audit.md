# Independent audit of the fifth-split distinct-beta argument

## Outcome

The proof in
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md)
is sound on its stated all-distinct, no-extra-singular stratum.  This audit
found no genericity assumption beyond the explicitly required distinctness,
exceptionality from the common value, and nonvanishing structural pair sums.
Promotion of the result is justified.

## Reduction audit

At (t=r+6), the definitions (p=r-1) and (k=r-6=p-5) give

\[
 |E|=p+7,\qquad |A|=k+1,\qquad |R|=5,\qquad
 |N|=p+2,\qquad |L|=5+k=p.
\]

Thus deleting the marked pair from (N) produces every maximal minor of
one fixed ((p+2)\times p) numerator matrix.  Confluence of the (k)
common columns gives the functions

\[
 {1\over(z+\nu_c)^2}\quad(c\in R),\qquad
 {(-1)^j(j+1)\over(z+\mu)^{j+2}}\quad(0\le j<k).
\]

Their principal parts are linearly independent.  The confluent Cauchy
denominator is nonzero because the row values are distinct, the five
exceptional column values and \(\mu\) are distinct, and all row--column
sums are nonzero.  Hence simultaneous pivot vanishing really does produce
a nonzero rational function with denominator degree (p+6), numerator
degree at most (p+4), and the (p+2) distinct roots in (N).  The
factorization (Q_R=P_Nq_R), with (0\ne q_R) and
\(\deg q_R\le2\), follows without a rank-one or uniqueness assumption on
the column dependence.

Removing ((z+a)^2) from the denominator and differentiating at (z=-a)
gives exactly

\[
 q_R'(-a)+\left(-\sum_{i\in N}{1\over a+\nu_i}
 -{k+1\over\mu-a}-2\sum_{c\in R\setminus\{a\}}{1\over c-a}\right)
 q_R(-a)=0.
\]

Rewriting the coefficient using the full exceptional set gives the stated
(A_a+\sum\psi(a,c)).  This derivation never divides by (q_R(-a)), so it
also covers a constant or linear (q_R), a repeated root, and a root at an
anchor.

## Moving determinant and poles

Four fixed nonzero exceptional values exist even if one exceptional value
is zero.  With three of them as anchors, the determinant of the three
quadratic residue rows is a rational function whose product with

\[
 (x^2-a^2)(x^2-b^2)(x^2-c^2)
\]

has degree at most six.  There are (p+3\ge9) allowed moving exceptional
values.  None is a pole: equality is excluded by distinctness and equality
to the negative of an anchor is excluded by the structural pair-sum
condition.  The cleared determinant is therefore identically zero.

At (x=\pm a), only the (a)-argument has a pole, and the determinant is
affine in that argument.  Its two nonzero residues force the two evaluations
of \(\Phi_A\) to vanish.  The opposite-pole subtraction has the nonzero
prefactor

\[
 {2a(b-c)\over(a+b)(a+c)},
\]

and cyclically likewise at (b,c).  Nonzero anchors, distinct anchors, and
the structural pair sums account for every division.  The resulting three
linear equations have the exact certificate

\[
 -(b^2-c^2)L_a-(a^2-c^2)L_b+(a^2-b^2)L_c
 =3(a-b)(a-c)(b-c)\ne0.
\]

## Boundary and cleanup checks

The smallest case (r=7) has (p=6,k=1), so ordinary Borchardt applies
and the moving set has exactly nine values, still more than the degree-six
bound.  An exact rational stress instance with thirteen exceptional values,
one equal to zero, had numerator rank six and all 28 maximal minors nonzero.
For the near-collision substitution (a=1,b=1+\varepsilon,
c=1+2\varepsilon), the final certificate is
(-6\varepsilon^3\), nonzero for every genuine distinct-value point.

Finally, one nonzero pivot kills row zero at every active star site; binary
colour exchange kills row one, and the established marked-pair triangular
cleanup kills row two.  Exceptional stars already vanish from
\((\nu_i-\mu)q_{i z_0}=0\).  Repeating over the three coordinates at
(z_0), and using the standing zero--zero and removed type-`22` facts,
isolates (z_0) in the rank-three graph.  This last conclusion is therefore
valid precisely in the inherited no-extra-singular setup.

The exact companion checker was rerun successfully; its symbolic
determinant, six pole residues, denominator inventory, and Vandermonde
certificate agree with the independent derivation above.
