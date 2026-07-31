# A unipotent response transgression kills the complete clean tail

## 1. Outcome

Let \({\cal A}\) be a commutative \(\mathbb C\)-algebra with a
derivation \(\partial\).  For \(x\in{\cal A}\), write
\(x^{[j]}=x^j/j!\).  Suppose

\[
 \partial q=r,\qquad \partial r=0,
 \qquad \alpha\in\mathbb C^\times,
 \tag{1}
\]

and that one physical cap row on \(2h\) residual sites is

\[
        \alpha q^{[h]}+r q^{[h-1]}=T,
        \qquad \partial T=0.                              \tag{2}
\]

Then the cap is clean:

\[
                 \boxed{(\alpha q+r)^{[h]}
                         =\alpha^{h-1}T.}                 \tag{3}
\]

This is a uniform positive criterion, not an assertion that the required
derivation already exists.  It replaces the response-order case split by
one triangular transgression.  In particular, for the target-zero
off-diagonal row, \(T=0\) is automatically fixed and (3) kills the whole
nonlinear tail.  For a target-bearing cap, fixing \(T\) is an additional
and essential hypothesis.  Here ``clean'' refers only to the vanishing of
the nonlinear response tail.  The resulting cap need not be active; in
particular a target-zero off-diagonal cap is normally inactive.  Thus (3)
is not by itself the active-clean bridge in the certified spine.

At \(h=3\), put

\[
 Q_j=r^{[j]}q^{[3-j]}\qquad(0\le j\le3).
\]

The four source consequences are

\[
\begin{aligned}
 \alpha Q_0+Q_1&=T,\\
 \alpha Q_1+2Q_2&=0,\\
 2\alpha Q_2+6Q_3&=0,\\
 6\alpha Q_3&=0.
\end{aligned}                                            \tag{4}
\]

The last three rows descend to \(Q_1=Q_2=Q_3=0\).  Thus the
quadratic/cubic obstruction

\[
                       \alpha Q_2+Q_3                    \tag{5}
\]

vanishes, with all factorials accounted for.  The second derivative alone
does **not** equal (5); the terminal derivative and downward triangular
elimination are indispensable.

One possible new proof target is therefore a **source-faithful unipotent
lift** of the response.  The tagged Hamming incidence class in
[the marked-site audit](h3-hamming-one-normal-incidence-compound-transgression.md)
is an obstruction to the restricted one-ended ansatz which factors every
marked response through the same site's incidence map.  It is not an
obstruction to an arbitrary global site derivation: an endomorphism at the
other endpoint can move an incidence vector outside its original image.
Even vanishing of all restricted local classes would still leave edgewise
compatibility, response invariance, and target fixation.  The independently
sharp eight-row boundaries show that the exceptional diagonal target must
participate in any theorem deriving such a lift from the presently tested
row data.

## 2. Triangular proof

Set

\[
                 Q_j=r^{[j]}q^{[h-j]},\qquad 0\le j\le h.
                                                               \tag{6}
\]

The divided-power product rule and (1) give

\[
                       \partial Q_j=(j+1)Q_{j+1}          \tag{7}
\]

for \(j<h\), while \(\partial Q_h=0\).  Hence, for
\(0\le k<h\),

\[
 \partial^k(\alpha Q_0+Q_1)
       =k!\bigl(\alpha Q_k+(k+1)Q_{k+1}\bigr),          \tag{8}
\]

and

\[
 \partial^h(\alpha Q_0+Q_1)=\alpha h!Q_h.              \tag{9}
\]

Because \(\partial T=0\), every derivative of (2) of positive order has
zero right side.  Equation (9) and \(\alpha\ne0\) give \(Q_h=0\).
Using (8) successively for \(k=h-1,h-2,\ldots,1\) gives

\[
                         Q_1=Q_2=\cdots=Q_h=0.           \tag{10}
\]

The original row then says \(T=\alpha Q_0\).  Finally,

\[
 (\alpha q+r)^{[h]}
     =\sum_{j=0}^h\alpha^{h-j}Q_j
     =\alpha^hQ_0
     =\alpha^{h-1}T,
\]

which proves (3) without cancelling a matching power.

## 3. Literal site-derivation criterion

For the residual site algebra

\[
 {\cal A}_W=\bigotimes_{x\in W}(\mathbb C\oplus V_x),
 \qquad V_xV_x=0,
\]

any collection \(D_x\in\operatorname {End}(V_x)\) defines a derivation
\(\partial_D\) by \(\partial_D(v)=D_xv\) for \(v\in V_x\).  If

\[
 q=\sum_{x<y}q_{xy},
\]

then the first condition in (1) is the explicit edgewise linear system

\[
 (D_x\otimes1+1\otimes D_y)q_{xy}=r_{xy}
                 \qquad(x<y).                            \tag{11}
\]

The other two conditions are likewise literal linear equations:

\[
                         \partial_D r=0,
             \qquad    \partial_D T=0.                  \tag{12}
\]

For a selected rank-one response \(r=p_as_b\), the stronger equations

\[
                         \partial_Dp_a=0,qquad
                         \partial_Ds_b=0                 \tag{13}
\]

imply the first equation in (12).  Thus (11)--(13) are a finite,
source-provenant feasibility problem in the local endomorphisms: (11) and
(13) are linear, while \(\partial_Dr=0\) is automatic under (13).

This global system must not be replaced by independent tagged cokernel
tests.  In map notation, contraction of (11) at a site \(x\) has the form

\[
 R_x= D_{\bar x}Q_x+Q_xD_x^*,                         \tag{13a}
\]

where \(D_{\bar x}=\bigoplus_{y\ne x}D_y\).  Modulo
\(\operatorname {im}Q_x\), the first term on the right can remain nonzero.
For example, on two sites take
\(q=e_0\otimes f_0\), let \(D_x=0\),
\(D_yf_0=f_1,D_yf_1=0\), and put
\(r=e_0\otimes f_1\).  Then
\(\partial_Dq=r\), \(\partial_Dr=0\), and the response factors may be
chosen fixed by \(D\), while the tag \(e_0^*\) gives
\(f_1\notin\operatorname {span}\{f_0\}=\operatorname {im}Q_x\).
Consequently the marked classes diagnose only the ansatz
\(D_{\bar x}Q_x\in\operatorname {im}Q_x\) (in particular a one-ended
lift).  The genuine positive target is the simultaneous edge system
(11)--(13), or a weaker source-faithful higher chain with the same
triangular conclusion.

## 4. Why response invariance cannot be dropped

It is not enough to have

\[
                       \partial q=r,qquad
                       \partial r=\lambda r.            \tag{14}
\]

At \(h=3\), \(\alpha=1\), and \(\lambda=-1/2\), the abstract divided-power
jet

\[
                     (Q_0,Q_1,Q_2,Q_3)=(4,-4,1,0)       \tag{15}
\]

satisfies the selected row and every iterated derivative of it under

\[
             \partial Q_j=j\lambda Q_j+(j+1)Q_{j+1},    \tag{16}
\]

but its clean tail is

\[
                          Q_2+Q_3=1.                    \tag{17}
\]

Indeed, substituting (15) into the right side of (16) gives
\(\partial(Q_0,Q_1,Q_2,Q_3)=-(Q_0,Q_1,Q_2,Q_3)\).  Thus (15) is an exact
\((-1)\)-eigenvector for the jet recurrence, while the selected-row
functional \(Q_0+Q_1\) annihilates it.  Every iterated row is therefore
zero, although (17) is nonzero.  Equivalently, this eigenvector defines a
one-dimensional differential quotient of the free response-jet module on
which the row dies and the clean tail survives.

This is an abstract response-grade guard, not a decorated GHZ source.  It
shows exactly why a scalable first-order lift is not the unipotent
transgression in (1).  A positive physical theorem must control the
response's own variation (or supply an equivalent higher Hasse--Schmidt
chain), not merely represent its first incidence row.

## 5. Scope and audit

The dependency-free checker
[verify_unipotent_response_transgression_clean_tail.py](../computations/verify_unipotent_response_transgression_clean_tail.py)
verifies (7)--(10) for \(1\le h\le12\), checks the clean identity over
exact rational test data, checks (4) with its factorials, and verifies the
resonant guard (15)--(17).  It runs unchanged under optimized Python.

This note does not modify the certified spine.  Its positive content is a
conditional algebraic mechanism.  To affect the conjecture, a later theorem
must construct (11)--(12), or a strictly weaker source-faithful chain with
the same triangular conclusion, from the complete exceptional anchor and
the adjacent full-nine overlap.
