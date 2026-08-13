# The diagonal second polar does not reach the uniform Fitting cut

## Outcome

Twice differentiating or polarizing the contracted diagonal full-nine
relation does **not** force

\[
 \chi_i=[u^h]G_{h,i}=0
\]

and does not produce a Hilbert--Burch matrix of total column degree below
\(h\).  The reason is already visible before any rank calculation.  Along a
physical response-cap direction the contracted target row has only response
orders zero and one,

\[
                         L(t)=B_0+tB_1,                 \tag{1}
\]

so its second Hasse derivative is identically zero.  The nonlinear clean cap
starts two response orders later,

\[
 G_h(t)=\sum_{j=2}^h t^jB_j,
 \qquad B_j=q^{[h-j]}r^{[j]},                           \tag{2}
\]

and its order-two coefficient at the base point is only \(B_2\).  The
literal repeated-response grades \(B_2,\ldots,B_h\) are independent source
grades.  Thus the diagonal Hessian does not transport (1) into the whole
clean tail (2).

At the first two uniform orders this is exact:

\[
 \begin{array}{c|c|c}
 h&G_h(t)&D_t^{[2]}G_h(0)\\ \hline
 3&t^2B_2+t^3B_3&B_2\quad\text{(misses }B_3\text{)},\\
 4&t^2B_2+t^3B_3+t^4B_4&B_2\quad\text{(misses }B_3,B_4\text{)}.
 \end{array}                                            \tag{3}
\]

Evaluating the second polar at a nonzero endpoint does not fix the problem.
It yields one weighted moment

\[
                         \sum_{j=2}^h {j\choose2}B_j,   \tag{4}
\]

not the independent family of clean response grades and not a relation
forcing every leading coordinate \(\chi_i\) to vanish.

## 1. Source and grade audit

The mixed full-nine target row has response-count grades \(j=0,1\).  These
are precisely the terms removed before the clean error is formed.  The clean
tail lies in grades

\[
                    R^{[j]}q^{[h-j]},\qquad2\leq j\leq h. \tag{5}
\]

Word projection alone does not identify these layers.  A second polar of
(1) therefore gives \(0=0\); it cannot cross the response-count grading from
the target layers into (5).  A second polar of the already nonlinear cap
(2) is a valid algebraic operation, but it selects only its \(j=2\) layer.
Neither operation is the sought source identity

\[
                         \bigwedge^h\mathcal M_f=0.      \tag{6}
\]

The same distinction prevents a partial diagonal-anchor argument from
closing the gap.  The committed \(h=3\) seven-row packet has every selected
row zero and one literal diagonal anchor, while

\[
               \alpha R^{[2]}q+R^{[3]}=-2X_2\ne0.       \tag{7}
\]

It misses the two complementary diagonal anchors.  Pure-anchor inversion
also cannot repair (7): the diagonal \(r=1\) head and mixed Hessian \(r=2\)
head occupy incompatible tensor grades.  Hence a positive diagonal proof
must use a complete cross-anchor higher operation, not merely multiply or
differentiate one anchor equation.

There is an additional scope guard.  For target-stabilizer colour jets the
second fundamental form is identically zero: the second derivative is an
Euler multiple of the original target equation.  Such a jet supplies no new
source relation.  A useful higher jet must be a non-stabilizer
Hasse/Spencer deformation in the complete augmented source complex.

## 2. Exact Hessian counterguard

The clean pair

\[
                              u^h,\qquad v^h             \tag{8}
\]

has second Hasse polars

\[
              {h\choose2}u^{h-2},\qquad {h\choose2}v^{h-2}. \tag{9}
\]

They are nonzero and coprime, but the clean Macaulay map of (8) has full
rank \(2h\), so its simultaneous Bezout kernel is zero.  Explicitly,

\[
 \begin{array}{c|c|c}
 h&D^{[2]}u^h&D^{[2]}v^h\\ \hline
 3&3u&3v,\\
 4&6u^2&6v^2.
 \end{array}                                            \tag{10}
\]

Thus even a nonzero diagonal Hessian is not, by itself, a low-degree
Hilbert--Burch relation.  This is compatible with the literal physical-word
guard already recorded for \(h=3,4\): the all-\(u\) and all-\(v\) clean
coordinates occur in legitimate repeated grades \(R^{[h]}q^{[0]}\), while
the target rows occupy response counts zero and one.  The pure-axis packet
does not satisfy all diagonal GHZ anchors, so it is a counterguard to the
Hessian implication, not a counterexample to a theorem genuinely using the
complete diagonal sector.

## 3. The shortest positive replacement

The algebraic replacement is known.  The Hilbert--Cauchy carrier theorem
uses the moments

\[
 H_s=\int_0^1t^s(q+tr)^{[h-2]},dt,
 \qquad c_s=(r-2q)H_s,                                  \tag{11}
\]

with \(s=0,1\) for \(h=3\) and \(s=0,\ldots,h-3\) for \(h\geq4\).
After the degree-correcting multiplications by \(q\) and \(r\), this moment
tower plus the clean row spans every degree-\(h\) binary form.  A single
second polar supplies neither this tower nor its source provenance.

Consequently the exact missing positive theorem is one of the following
equivalent source-level statements.

1. A complete non-stabilizer Hasse/Spencer comparison carries response
   orders \(2,\ldots,h\), with their literal word, fine, and repeated grades,
   into one source-faithful Hilbert--Cauchy moment tower whose terminal
   readout is nonzero.
2. The same augmented source equations directly force
   \(\bigwedge^h\mathcal M_f=0\), or furnish a full-rank Hilbert--Burch
   syzygy matrix whose total column degree is strictly less than \(h\).

Every face used in such a totalization must preserve the residual word,
retain its response-count label \(j\), respect the diagonal anchors and
protected target rows, and extend the physical terminal/\(q\) cocycle.  No
committed second-polar or ordinary response-Plucker identity currently
supplies that augmented comparison.

## 4. Certified interface

The companion checker

```text
computations/verify_uniform_diagonal_second_polar_fitting_gap.py
```

pins the response-Pluecker/Fitting gate, the target-stabilizer second-jet
tautology, the Hilbert--Cauchy moment theorem, the \(h=3\) seven-row guard,
and the full-nine star-inverse grade guard.  It verifies (3)--(4), the
literal response-grade dimensions for \(3\leq h\leq10\), and the pure-axis
Macaulay/Hessian guard (8)--(10).
