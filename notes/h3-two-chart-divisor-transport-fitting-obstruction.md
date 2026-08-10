# The smallest (h=3) two-chart transport module has Fitting obstruction (chi^3)

## Outcome

Retain the smallest completed two-chart packet requested by the rootless
bridge:

* two differently labelled diagonal anchors;
* the common direct label table;
* one crossed row whose target grade is zero;
* one selector-compatible literal four-cut coefficient; and
* the three quadratic prolongations required to define a functional on
  (Q_f).

On the triple-root chart (f=v^3), this packet has a nonzero
(Q_f)-dual **if and only if** one explicit source-grade coefficient
(chi) vanishes.  After exact row reduction its top Fitting generator is

\[
                         \boxed{-3\chi^3}.                 \tag{1}
\]

Thus the retained rows do not automatically supply the desired dual.  For
generic (chi\ne0) they do the opposite: they fill (Q_f).  On
(chi=0), coefficient extraction ([u^5]) is the required nonzero dual.
The missing theorem is precisely a literal two-chart identity forcing
(chi=0); no further static selector rank calculation can replace it.

This is an exact rank/cokernel obstruction, not a full-source counterexample.
It couples the literal four-cut source grading to the completed-square
transport, but does not assert that arbitrary cut-local coefficients extend
to one global matching source.

## 1. The completed label square closes exactly

Use labels (r,s) and write

\[
 d=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 H^\rightarrow=E_{rs},\qquad H^\leftarrow=2E_{sr}.
\]

The transported normal and crossed zero-target row are

\[
 B=H^\rightarrow+H^\leftarrow
   =\begin{pmatrix}0&1\\2&0\end{pmatrix},\qquad
 J=H^\rightarrow-H^\leftarrow
   =\begin{pmatrix}0&1\\-2&0\end{pmatrix}.              \tag{2}
\]

Let (E_{rr},E_{ss}) denote the two diagonal-anchor grades.  Then

\[
 B=-\frac13J+\frac43d-\frac43E_{rr}-\frac83E_{ss}.       \tag{3}
\]

In the ordered entry basis (rr,rs,sr,ss), the four source-grade columns
((E_{rr},E_{ss},d,J)) form

\[
 S=\begin{pmatrix}
 1&0&1&0\\
 0&0&1&1\\
 0&0&1&-2\\
 0&1&2&0
 \end{pmatrix},
 \qquad \det S=-3.                                      \tag{4}
\]

So two anchors plus the crossed row really do transport the static normal;
there is no residual static provenance class left to exploit.  This is the
genuinely two-chart threshold, beyond a one-chart selector no-go.

## 2. The four-cut leaves one nonlinear source grade

At a selected mixed output coefficient, put the binary cap line in the
form

\[
                         F=\alpha q+R.
\]

In divided-power matching notation,

\[
 F^{[3]}=\alpha^3q^{[3]}+\alpha^2Rq^{[2]}
          +\alpha R^{[2]}q+R^{[3]}.                      \tag{5}
\]

The physical crossed output row is zero, hence its literal source
coefficient is

\[
                         \alpha q^{[3]}+Rq^{[2]}=0.       \tag{6}
\]

Subtracting (alpha^2) times (6) from (5) is source-grade exact and leaves

\[
              \boxed{\alpha R^{[2]}q+R^{[3]}.}           \tag{7}
\]

This is the smallest selector-compatible four-cut term which static label
transport does not control.  Let its transported scalar cubic be

\[
                g=\chi u^3+b u^2v+cuv^2+dv^3.            \tag{8}
\]

The coefficient (chi=[u^3]g) is therefore not a new formal quotient
symbol: it is a specified coefficient of the literal repeated-insertion
grades (R^{[2]}q) and (R^{[3]}).  Equations (3) and (6), however, impose
no equation on it.

This is also the exact place where a two-chart Bianchi or divisor-transport
identity would have to enter.  Such an identity must show that (7) has zero
(u^3)-coefficient on the divisor (v=0), not merely that (J) is nonzero
in the static selector quotient.

## 3. Exact residual Macaulay presentation

Normalize the exposed cubic to (f=v^3).  In the bases

\[
 S_2=(u^2,uv,v^2),\qquad
 Q_f=(\overline{u^5},\overline{u^4v},\overline{u^3v^2}),
\]

multiplication by (8) is

\[
 M_g=\begin{pmatrix}
 \chi&0&0\\
 b&\chi&0\\
 c&b&\chi
 \end{pmatrix},
 \qquad \det M_g=\chi^3.                                \tag{9}
\]

After (3), the complete seven-dimensional presentation is block diagonal:

\[
                         S\oplus M_g.                     \tag{10}
\]

Equations (4) and (9) prove (1).  They give the sharp dichotomy.

* If (chi\ne0), (M_g) is an isomorphism onto (Q_f).  There is no
  nonzero (Q_f^*)-functional annihilating the literal transported span.
* If (chi=0), the functional

  \[
                         \varepsilon(\bar h)=[u^5]h       \tag{11}
  \]

  is nonzero and annihilates every column of (M_g).  For generic
  (b\ne0), the combined rank is six and this cokernel is exactly
  one-dimensional.

Hence the answer to the bounded question is not “two charts supply a
dual”, but the exact conditional statement

\[
 \boxed{
 \text{the two-chart/four-cut module supplies a nonzero }Q_f\text{ dual}
 \iff [u^3](\alpha R^{[2]}q+R^{[3]})=0.}                 \tag{12}
\]

## 4. Scope and stopping rule

The calculation is source-faithful at the level claimed: (3) is an exact
label-grade identity and (5)--(7) retain the repeated physical insertion
grades instead of replacing them by an output-only invariant.  It makes no
coefficient-grid assumption and works over any characteristic in which
(3) is invertible (the unscaled column statement can be used in
characteristic (3)).

It does **not** prove that the cut-local data in (2), (6), and (7) extend to
one global exact source, nor that a synchronized full-nine overlap has only
one residual cubic.  It is therefore neither a Krenn counterexample nor a
retirement of the full two-chart route.

It does give a sharp stopping rule for this module: do not add more static
anchors, crossed tables, or selector ranks.  The next proof-completing row
must be a source-provenant identity that kills the coefficient in (12), or
an exact global source packet with that coefficient nonzero.

The dependency-free checker
[`verify_h3_two_chart_divisor_transport_fitting_obstruction.py`](../computations/verify_h3_two_chart_divisor_transport_fitting_obstruction.py)
audits (3)--(12), the literal four-grade subtraction for several exact
rational (alpha), the generic rank-seven case, the rank-six boundary, and
the explicit dual (11).  It uses explicit runtime failures and is unchanged
under `python -O`.
