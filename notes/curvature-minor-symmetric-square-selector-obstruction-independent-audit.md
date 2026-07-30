# Independent audit: curvature inversion does not project the symmetric response

## 1. Verdict

The theorem and literal guard in
[the curvature-selector obstruction](curvature-minor-symmetric-square-selector-obstruction.md)
are **PASS**, with one scope clarification and one advisable bookkeeping
clarification.

* The determinant \(AU-BF\) is exterior-square data, while the physical
  two-star product transforms by the symmetric square.  Formula (4) of
  the primary note, including all three coefficients, is exact.
* Lemma 2.1 is valid over \(\mathbb C\).
* The canonical mixed-row coefficient is \(R=m-1\); at eight sites it is
  exactly three.
* The divided-power exchange residual cancels identically with the stated
  factorials.
* Reconstructing every aggregate block of the eight-site guard gives no
  endpoint-order conflict.  Both \(pq\) and \(pr\) are genuinely good,
  the curvature minor is one, and every rank and target claim is correct.

The scope clarification is that the selected top mixed slice in the guard
is also support-vacuous at the two residual sites \(t,w\): the selected
internal quadratic and selected stars use only \(q,r,u,v\).  The stronger
source identity \(3\xi\eta+z=0\) is nevertheless literal and correct.
Thus the guard proves exactly the stated local nonimplication, but it
does not test a nonzero selected mixed cofactor on all six residual sites.

For bookkeeping, the phrase “all other unlisted blocks are zero” should
be read after expanding the six internal blocks prescribed by
\(z=-3\xi\eta\).  Listing those six blocks explicitly would prevent a
reader from mistaking them for conflicts with the displayed star blocks.
No mathematical repair is required.

## 2. Exterior inversion and symmetric multiplication

Put

\[
 v=\binom AF,\qquad w=\binom BU,\qquad
 M=(v\ w)=\begin{pmatrix}A&B\\F&U\end{pmatrix}.
\]

Then

\[
 \det M=AU-BF=\kappa
\]

and

\[
 \binom X Y
 =M^{-1}\binom\xi\eta
 ={1\over\kappa}
 \begin{pmatrix}U&-B\\-F&A\end{pmatrix}\binom\xi\eta.
\]

At the selected \((q,b)\)-coordinate the coefficient vector of
\((\xi,\eta)\) is \(v\), and at the selected \((r,c)\)-coordinate it is
\(w\).  Hence the corresponding coefficient vectors of \((X,Y)\) are
\((1,0)\) and \((0,1)\), respectively.  This statement concerns the
selected local coordinates and does not assert that other colour
components at those sites vanish.

Conversely,

\[
 \xi=AX+BY,\qquad \eta=FX+UY.
\]

The site-square-zero algebra is commutative between distinct sites, so
ordinary multiplication gives

\[
 \xi\eta
 =AF\,X^2+(AU+BF)XY+BU\,Y^2.                           \tag{A1}
\]

Thus the cross coefficient is the permanent \(AU+BF\), while the
determinant \(AU-BF\) controls only the inverse of \(M\).  There is no
missing factor of two in (A1): \(XY\) denotes the ordinary product of two
linear forms, just as the physical response \(\xi\eta\) does.  In a basis
using divided squares the matrix entries would be rewritten, but the same
symmetric-square obstruction remains.

The representation-theoretic wording is therefore accurate:
\(\bigwedge^2M\) is one-dimensional and acts by \(\det M\), whereas
\(\operatorname{Sym}^2M\) acts on the three terms
\(X^2,XY,Y^2\).  A matching uses one \(p\)-star and one \(s\)-star, so
there are no physical \(\xi^2\) or \(\eta^2\) rows from which to recover
an exterior projector.

## 3. Audit of Lemma 2.1

Write \(L=\sum_iL_i\), with \(L_i\in V_i\).  Since \(V_iV_i=0\),

\[
 L^2=\sum_{i\ne j}L_iL_j
    =2\sum_{i<j}L_i\otimes L_j.                         \tag{A2}
\]

The summand indexed by \(\{i,j\}\) lies in the direct multidegree
component \(V_i\otimes V_j\).  Terms for different unordered pairs
therefore cannot cancel.  Over \(\mathbb C\), the tensor product of two
nonzero vectors is nonzero, and two is invertible.  Hence \(L^2=0\) if
and only if no two site components of \(L\) are simultaneously nonzero,
which is exactly support on at most one site.

The field assumptions matter: the displayed proof would fail in
characteristic two.  The primary note works over \(\mathbb C\), so its
statement is exact.

## 4. Canonical normalization and divided-power cancellation

For a pair \(p,s\) in an order-\(2m\) source, let \(z\) be the internal
quadratic and let \(E=A_{ps}(a,d)\).  The raw pair row is

\[
                  Ez^{[m-1]}+\xi\eta z^{[m-2]}
       =\delta_{ad}X_a.                                      \tag{A3}
\]

Using

\[
                  zz^{[m-2]}=(m-1)z^{[m-1]},
\]

and putting \(R=m-1\), equation (A3) is equivalent to

\[
 \bigl(R\xi\eta+Ez\bigr)z^{[m-2]}
                  =R\delta_{ad}X_a.                          \tag{A4}
\]

Thus the normalization in the primary note is correct.  At \(N=8\),
\(m=4\), so \(R=3\).  For the mixed row \(a\ne d\), the right side of
(A4) is zero.

The overlap expression audited in equations (17)--(18) of the primary
note is

\[
\begin{aligned}
 &(\Delta v+\kappa z)z^{[k-1]}
 +\Delta zvz^{[k-2]}\\
 &\hspace{25mm}
 -k\bigl(\kappa z^{[k]}+\Delta vz^{[k-1]}\bigr).
\end{aligned}
\]

Its \(\kappa\)-part is zero because

\[
                  \kappa zz^{[k-1]}=k\kappa z^{[k]}.
\]

Its \(\Delta\)-part has coefficient

\[
                  1+(k-1)-k=0
\]

on \(\Delta vz^{[k-1]}\), using
\(zz^{[k-2]}=(k-1)z^{[k-1]}\).  Endpoint order plays no role in this
last commutative common-complement product.  The claimed exact Bianchi
cancellation is valid, including the first \(k=2\) four-cut boundary.

## 5. Literal expansion of the guard

Use the primary note's

\[
 X=e_{q,0}+e_{u,0},\qquad
 Y=e_{r,0}+e_{v,0},\qquad
 \xi=X+Y,\qquad \eta=X+2Y.
\]

For an unordered pair of distinct sites, the coefficient of
\(\xi\eta\) is the sum of the two endpoint orders.  Therefore the only
nonzero internal blocks prescribed by \(z=-3\xi\eta\) are

\[
\begin{array}{c|cccccc}
\text{pair}&qu&rv&qr&qv&ur&uv\\ \hline
\xi\eta\text{ coefficient}&2&4&3&3&3&3\\
z(0,0)&-6&-12&-9&-9&-9&-9.
\end{array}                                                   \tag{A5}
\]

There are no loops or same-site cells, because they vanish in the
site-square-zero algebra.  Every entry in (A5) is internal to
\(W=\{q,r,u,v,t,w\}\).  Hence none conflicts with:

* the \(p\)-star blocks \(pq,pr,pu,pv,pt,pw\);
* the \(s\)-star blocks \(qs,rs,us,vs\); or
* the direct block \(ps\).

The apparent reuse of the letters \(u,v\) in an internal pair is merely
site notation, not endpoint-order ambiguity.  Every block in (A5) is a
\((0,0)\)-cell and is symmetric under reversing the physical storage
order.

The blocks into \(s\) are stored with rows at \(q,r\) and columns at
\(s\).  Thus

\[
 A_{qs}(0,1)=1,\qquad A_{rs}(0,1)=2,
\]

exactly matching the coefficients of \(\eta\) in (23).  The matrices

\[
 A_{qs}=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix},
 \qquad
 A_{rs}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}
\]

have determinants \(-1\) and \(-2\), respectively.  Hence their row maps
at \(q\) and \(r\) are invertible.

For the pair \(pq\), after deleting \(p,q\), the \(p\)-rows have:

\[
\begin{array}{c|c}
\text{\(p\)-row}&\text{private or surviving component}\\ \hline
0&(r,0),(u,0),(v,0),(s,1)\\
1&(t,0)\\
2&(w,0).
\end{array}
\]

They are linearly independent.  The three \(q\)-rows are independent
because their restriction to the surviving site \(s\) is \(A_{qs}\).
Thus \(pq\) is good.

For \(pr\), the \(p\)-row table is the same with \(q\) replacing \(r\)
in the first line, and the three \(r\)-rows restrict invertibly to
\(A_{rs}\) at \(s\).  Thus \(pr\) is also good.  Internal blocks from
(A5) can only add output coordinates and cannot lower either rank.

## 6. Curvature, channel support, and the target slice

At flags \((q,0)\) and \((r,0)\), with exposed colours
\((p,0),(s,1)\),

\[
 A=1,\qquad B=1,\qquad F=1,\qquad U=2.
\]

Consequently

\[
 M=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 \det M=AU-BF=1,
\]

and indeed

\[
 \binom\xi\eta=M\binom XY.
\]

Ordinary squaring gives

\[
 X^2=2e_{q,0}e_{u,0},\qquad
 Y^2=2e_{r,0}e_{v,0}.
\]

Both are nonzero.  Since the supports of \(X\) and \(Y\) are disjoint,
a nonzero \(\lambda X+\mu Y\) has support two if exactly one coefficient
is nonzero and support four if both are nonzero.  No nonzero channel form
is supported at one site.

Finally \(E=A_{ps}(0,1)=1\) and \(R=3\), so

\[
                 {\cal P}_{ps}^{01}=3\xi\eta+z=0              \tag{A6}
\]

as a literal quadratic identity.  Therefore

\[
                 {\cal P}_{ps}^{01}z^{[2]}=0
\]

coefficientwise, exactly the complete mixed target row.

There is an additional sharp scope fact.  The selected \(\xi,\eta,z\)
are all supported on \(q,r,u,v\), so neither side can cover residual sites
\(t,w\).  Thus the top mixed slice would vanish even without using (A6).
This does not invalidate the guard: goodness uses the \(p\)-rows at
\(t,w\) in endpoint colours \(1,2\), which are invisible to the selected
\((p,0),(s,1)\) slice.  It does mean that (A6) should not be described as
a nontrivial cancellation between nonzero top-degree mixed coefficients.
It is a stronger power-free cap cancellation sitting above a
support-vacuous selected top row.

## 7. Conclusion and exact repairs

The primary note's mathematical conclusion is valid:

\[
 \{\text{two good fan pairs},\ \kappa\ne0,\
   \text{complete selected mixed row}\}
 \not\Longrightarrow
 \{\text{one-sided inverse channel}\}.
\]

No displayed equation, block, determinant, rank, or target statement
requires correction.  Two prose improvements are advisable:

1. after defining \(z\), list the six blocks in (A5), or state explicitly
   that “unlisted” excludes the blocks prescribed by \(z\);
2. note that the selected mixed top row is support-vacuous at \(t,w\),
   although the literal quadratic cancellation
   \(3\xi\eta+z=0\) remains valid.

The guard is correctly labelled local and is not a ternary exact source.
It establishes the exterior-versus-symmetric obstruction, but it does not
exclude a stronger selector theorem using another exposed-colour row or
a nonzero selected cofactor on all six residual sites.

Both prose clarifications were then applied: the six internal \(z\)-blocks
are listed, and the support-vacuous top-slice scope is explicit.  The
repaired primary has SHA-256

    3bde66be07dc74e565cbaf170b6e0596470725e35819e405d6fc39d78b717e07  notes/curvature-minor-symmetric-square-selector-obstruction.md
