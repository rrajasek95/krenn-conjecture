# Independent audit of the fifth-split collision theorem

## Outcome

The proof in
[live-three-zero-fifth-split-collision-beta.md](live-three-zero-fifth-split-collision-beta.md)
is sound on its stated collision, no-extra-singular stratum.  The audit
found no unlisted multiplicity profile, no genericity assumption on the
distinct value classes, and no defect in the Hermite-confluent rank
reduction.  Together with the separately audited distinct-value theorem,
it closes the full fifth split \(t=r+6\).

## Confluence and complementary minors

For a row class of multiplicity \(q\), the global numerator matrix contains
the divided jets of orders \(0,\ldots,q-1\).  Deleting one labelled copy
before collision leaves multiplicity \(q-1\), so its confluent numerator is
exactly the global matrix with the order-\(q-1\) top row deleted.  Deleting
labels in two distinct classes therefore gives precisely the complementary
top--top maximal minor used in Lemma 2.1.  This remains true when a value
class occurs on both shores: row and column Vandermonde factors are divided
out independently, mixed derivatives commute, and the cross value is
regular because \(2x\ne0\).

The independent checker compares the literal repeated-row/repeated-column
Cauchy permanent with the quotient of the two mixed-jet determinants in two
six-square cases, including shared shore values and a triple column class.
It then starts with an \(8\times6\) global numerator and verifies all six
top-pair deletions both against rebuilt lower-multiplicity jet matrices and
against their literal Cauchy permanents.  Every confluent Cauchy denominator
is nonzero.

If the global matrix had rank \(p\), its left kernel would have dimension
two.  Vanishing of every top--top complementary minor says exactly that all
two-coordinate minors of the kernel projection to top rows vanish.  That
projection has rank at most one, hence a nonzero kernel vector is supported
on non-top jets.  Its associated rational function has independent
principal parts, denominator degree \(q_{\rm rep}\), and numerator degree at
most \(q_{\rm rep}-2\).  A singleton row class gives
\(q_{\rm rep}\le p+1\), whereas the column jets impose \(p\) zeros away
from its poles.  Thus the rank-loss conclusion is valid for arbitrary row
multiplicities, not only doubles.

The resulting column relation has denominator degree \(p+m_R+1\), numerator
degree at most \(p+m_R-1\), and \(p+2\) Hermite roots.  Principal-part
independence makes the numerator nonzero.  Consequently the three cases in
(12) follow exactly, including lower-degree residual factors.

## Multiplicity exhaustion

The classification in Lemma 4.1 is uniform in \(p\).  With all
multiplicities at most four:

- a four-class plus a double permits \(4+1\) and leaves one copy of the
  double; a four-class plus a triple or four-class permits \(3+2\) and
  leaves one copy of the four-class; with only singleton companions an
  untouched singleton remains;
- two triple classes permit \(3+2\), leaving one copy of the second triple;
- one triple together with both a double and a singleton permits \(3+2\)
  while leaving the singleton;
- what remains is exactly all-distinct, a sole triple with homogeneous
  singleton or double companions, or a multiset made only of singles and
  doubles with at least one double.

This argument has no finite cutoff.  As a stress check, an independent
count-vector enumeration through 120 labels verifies the same dichotomy for
every \((c_1,c_2,c_3,c_4)\).

For a class of multiplicity at least five, subtraction of the two
pair-deleted \(e_5\)'s has the asserted sign and yields all one-deletion
\(e_4\)'s on \(W\).  Since \(|W|\ge6\), the factors \(|W|-d\) in the
successive summations for \(d=4,3,2,1\) never vanish.  The recurrence then
ends at \(h_i e_0=h_i=0\), contradicting structural nonvanishing.  The
checker verifies the full symbolic descent at the minimal boundary
\(|N|=8\).

## Moving classes and root counts

At an anchor selected once, removal of the double pole gives the exact
simple-residue condition \(Y_a=0\) in the constant-residual case.  Relative
to the fixed full exceptional multiset, selecting \(j\) moving labels adds
\(j/(a+x)\) to the row logarithmic derivative, while its column jet cluster
subtracts \((j+1)/(x-a)\).  Hence

\[
 \chi_j(a,x)={j\over a+x}-{j+1\over x-a}
             =-{x+(2j+1)a\over x^2-a^2}.
\]

After clearing the denominator, the coefficient of \(x\) is \(-1\), so
the polynomial is never identically zero and has at most two roots for
both \(j=1\) and \(j=2\).

For the linear residual, the two anchor equations are
\((1-aY_a,Y_a)(A,B)^T=0\) and its \(b\)-analogue.  Their determinant is
exactly
\(Y_b-Y_a+(b-a)Y_aY_b\).  Clearing the two quadratic denominators gives
degree at most four.  The five or more moving singleton values are distinct
and avoid every pole by the structural pair-sum condition.  Identity of the
quartic forces \(V=-U\) and then \(U=0\) or \(U=-2/(b-a)\); the two remaining
quadratics have nonzero leading coefficient.  This also covers a zero
anchor and every degree drop of the residual linear factor.

The route cardinalities are sharp at the smallest \(p=6\): triple-plus-
single and triple-plus-double profiles have respectively at least nine and
four moving choices after fixing an anchor; \(d\le3\) leaves at least five
singleton movers; \(d=4\) gives three double movers; and \(d\ge5\) gives at
least three.

## Cleanup and scope

At \(t=r+6\), one has \(|E|=p+7\), \(|R|=5\), \(|N|=p+2\),
\(|L|=p\), and \(|A|=k+1\) with \(5+k=p\).  For the chosen target star the
two binary shores after deleting the marked pair have size \(p,p\).  Any
other active star leaves sizes \(p+1,p-1\), so the same nonzero pivot
isolates the target coefficient for every active site.  Binary exchange
kills row one, and the inherited marked-pair triangular equation kills row
two.  Exceptional stars already vanish from
\((\nu_i-\mu)q_{iz_0}=0\).  Thus the final isolation conclusion uses only
the standing no-extra-singular hypotheses and is valid as stated.

The companion
[independent checker](../computations/verify_live_three_zero_fifth_split_collision_beta_independent_audit.py)
passes all exact tests.
