# A curvature minor is exterior data, not a matching-tensor projector

## 1. Outcome

The nonzero physical curvature minor

\[
 \kappa=AU-BF\ne0                                                \tag{1}
\]

does give two inverse channel functionals.  It does **not** by itself give
a source-level projection onto the two selected flags.  The obstruction is
elementary but structural: the inverse is an exterior-square construction,
whereas a matching through two exposed sites uses the symmetric square of
their star rows.

More precisely, let \(\xi,\eta\) be the two selected exposed-site star
forms, and suppose their values at two selected residual flags are

\[
 v=\binom A F,\qquad w=\binom B U,
 \qquad M=(v\ w),\qquad \det M=\kappa\ne0.                       \tag{2}
\]

The normalized inverse-channel forms \(X,Y\) are defined by

\[
                 \binom\xi\eta=M\binom XY.                       \tag{3}
\]

They take the values \((1,0)\) and \((0,1)\) at the two selected flags.
Nevertheless the physical two-star response is

\[
 \boxed{
 \xi\eta=AF\,X^2+(AU+BF)XY+BU\,Y^2.}                            \tag{4}
\]

The coefficient of \(XY\) is the permanent \(AU+BF\), not the curvature
\(AU-BF\), and the two same-channel contaminants are genuine matching
quadratics.  In the site-square-zero algebra,

\[
                         X^2=0
 \quad\Longleftrightarrow\quad
 \text{\(X\) is supported at at most one site}.                  \tag{5}
\]

Thus killing a same-channel term is already the sparse one-sided conclusion
which the inversion was supposed to prove.

This failure persists after retaining every residual word in the natural
mixed target slice, and it is compatible with goodness of both fan pairs
which produced the minor.  Section 4 gives a literal eight-site aggregate
guard with

* two good pairs \(pq,pr\);
* \(AU-BF=1\);
* the complete mixed \((p,0),(s,1)\) target slice equal to zero; and
* \(X^2\ne0\), \(Y^2\ne0\), with no nonzero member of
  \(\operatorname{span}\{X,Y\}\) supported at one site.

The guard is not a full ternary source.  Its conclusion is narrower and
exact: scalar inversion of the curvature square, even followed by the full
mixed-slice target equation and good-star injectivity, cannot be the missing
selector descent.  A positive proof must use target rows in other exposed
colours to force a new support/annihilator statement, or return to the clean
cap polynomial.  In the displayed guard the selected top slice is also
support-vacuous at two residual sites; the stronger power-free identity
between its direct and two-star cap quadratics nevertheless holds literally.

## 2. Symmetric square versus exterior square

Work in the site-square-zero algebra

\[
 {\cal R}(W)=\bigotimes_{i\in W}(\mathbb C\oplus V_i),
 \qquad V_iV_i=0.                                                \tag{6}
\]

Fix exposed sites \(p,s\), colours \(a,d\), and write their selected star
rows on \(W=B\setminus\{p,s\}\) as

\[
 \xi=\sum_{i\in W}\xi_i,\qquad
 \eta=\sum_{i\in W}\eta_i.                                    \tag{7}
\]

Choose two residual flags \((q,b),(r,c)\).  In endpoint order put

\[
 \begin{array}{ll}
 A=A_{pq}(a,b),&B=A_{pr}(a,c),\\
 F=A_{qs}(b,d),&U=A_{rs}(c,d).
 \end{array}                                                     \tag{8}
\]

These are exactly the two columns in (2).  Since \(M\) is invertible,

\[
 \binom X Y=M^{-1}\binom\xi\eta
 ={1\over\kappa}
   \begin{pmatrix}U&-B\\-F&A\end{pmatrix}
   \binom\xi\eta.                                              \tag{9}
\]

Consequently \(X_{q,b}=1,Y_{q,b}=0\) and
\(X_{r,c}=0,Y_{r,c}=1\).  This is the inverse two-flag selector, with no
genericity or division by any source entry other than the displayed
nonzero determinant.

Substituting

\[
                         \xi=AX+BY,\qquad \eta=FX+UY             \tag{10}
\]

proves (4).  In representation-theoretic language, \(\kappa\) is the
action of \(\bigwedge^2M\), while the physical pair response transforms
by \(\operatorname{Sym}^2M\).  There is no matching row containing two
copies of the \(p\)-star or two copies of the \(s\)-star: a perfect matching
uses each exposed site once.  Hence one cannot polarize (4) by importing
physical \(\xi^2\) and \(\eta^2\) rows; those rows do not exist in the
source.

The promised support criterion is also exact.

**Lemma 2.1 (square-zero linear forms).**  If
\(L=\sum_{i\in W}L_i\in{\cal R}_1(W)\) over \(\mathbb C\), then

\[
                    L^2=0\quad\Longleftrightarrow\quad
       |\{i:L_i\ne0\}|\le1.                                    \tag{11}
\]

**Proof.**  The site-square-zero rule gives

\[
                         L^2=2\sum_{i<j}L_i\otimes L_j.          \tag{12}
\]

The summands belong to distinct site-support components of
\({\cal R}_2(W)\), so they cannot cancel.  Over a field, a tensor product
of two nonzero vectors is nonzero.  Thus (12) vanishes exactly when no two
site components of \(L\) are nonzero.  \(\square\)

In particular, an argument which removes the \(X^2\) term by asserting
\(X^2=0\) has assumed precisely a one-site support theorem.  The inverse
minor supplies no such theorem.

## 3. The complete mixed target row does not repair the mismatch

Let \(|B|=2m\), put \(R=m-1\), and let \(z\) be the internal quadratic
on \(W\).  If

\[
                         E=A_{ps}(a,d),                           \tag{13}
\]

then the canonical unnormalized coordinate cap is

\[
                         {\cal P}_{ps}^{ad}=R\xi\eta+Ez.          \tag{14}
\]

For \(a\ne d\), exact ternary monochromaticity requires the entire tensor
row

\[
                         {\cal P}_{ps}^{ad}z^{[m-2]}=0.           \tag{15}
\]

Equation (15) means every colouring word on all \(2m-2\) residual sites,
not a selected scalar coefficient.

Even this complete mixed row does not project (4).  For arbitrary
\(\xi,\eta\) and any \(E\ne0\), choose the literal internal quadratic

\[
                              z=-{R\over E}\xi\eta.              \tag{16}
\]

Then \({\cal P}_{ps}^{ad}=0\) before multiplication, so (15) holds
coefficientwise while all three terms in (4) may remain nonzero.  This is
not cancellation between selected matching monomials: it is the exact
source-level cancellation between the direct-edge/internal contribution
and the two-star contribution in the canonical cap.

The same blindness appears when the two overlapping pair presentations
are compared.  With the notation of the four-cut connection, their
difference contains

\[
 (\Delta v+\kappa z)z^{[k-1]}
 +\Delta zvz^{[k-2]}
 -k\bigl(\kappa z^{[k]}+\Delta vz^{[k-1]}\bigr).                 \tag{17}
\]

It is identically zero by

\[
 zz^{[k-1]}=kz^{[k]},\qquad
 zz^{[k-2]}=(k-1)z^{[k-1]}.                                    \tag{18}
\]

In particular, retaining all mixed target words does not leave a term
which can be divided by \(\kappa\).  The curvature is visible in the
power-free source connection, but its contribution to the top target-row
comparison is an exact divided-power boundary.

## 4. An eight-site literal-block guard with good fan pairs

Take

\[
 B=\{p,s,q,r,u,v,t,w\},\qquad V_i=\mathbb C^3,                  \tag{19}
\]

and use colours \(0,1,2\).  All vectors below at residual sites are
coordinate-zero vectors.  On
\(W=\{q,r,u,v,t,w\}\), define

\[
 X=e_{q,0}+e_{u,0},\qquad
 Y=e_{r,0}+e_{v,0},                                             \tag{20}
\]

and

\[
 \xi=X+Y,qquad \eta=X+2Y,qquad z=-3\xi\eta.                  \tag{21}
\]

Use \(z\) as the complete internal aggregate quadratic on \(W\).  Its
nonzero \((0,0)\)-entries are

\[
\begin{array}{c|rrrrrr}
\text{pair}&qu&rv&qr&qv&ur&uv\\ \hline
z(0,0)&-6&-12&-9&-9&-9&-9.
\end{array}                                                     \tag{21a}
\]

Put

\[
 A_{ps}(0,1)=1,                                                 \tag{22}
\]

make the colour-zero row of the \(p\)-star equal to \(\xi\), and make the
colour-one row of the \(s\)-star equal to \(\eta\).  Thus

\[
 \begin{array}{c|cccc}
 i&q&r&u&v\\ \hline
 A_{pi}(0,0)&1&1&1&1\\
 A_{is}(0,1)&1&2&1&2.
 \end{array}                                                     \tag{23}
\]

Entries in (23) are written in the displayed endpoint order.  Add

\[
                         A_{pt}(1,0)=1,qquad A_{pw}(2,0)=1       \tag{24}
\]

and complete the two blocks into \(s\) by

\[
 A_{qs}=
 \begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix},
 \qquad
 A_{rs}=
 \begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix},            \tag{25}
\]

with rows indexed at \(q,r\) and columns at \(s\).  Equations (23) and
(25) agree on their common specified entries.  All other unlisted blocks
and entries, apart from the internal blocks prescribed in (21a), are zero.

The pair \(pq\) is good.  After deleting \(p,q\), the three \(p\)-rows
are independent because the colour-zero row is nonzero on
\(r,u,v,s\), while the other two have the private components at \(t,w\).
The three \(q\)-rows are independent because the block \(A_{qs}\) is
invertible.  The same argument, using \(A_{rs}\), proves that \(pr\) is
good.

For the selected flags \((q,0),(r,0)\),

\[
 A=A_{pq}(0,0)=1,\quad B=A_{pr}(0,0)=1,
 \quad F=A_{qs}(0,1)=1,\quad U=A_{rs}(0,1)=2,                   \tag{26}
\]

and hence

\[
                              AU-BF=2-1=1.                       \tag{27}
\]

The corresponding channel matrix and its normalization are exactly

\[
 M=\begin{pmatrix}1&1\\1&2\end{pmatrix},qquad
 \binom\xi\eta=M\binom XY.                                    \tag{28}
\]

Both same-channel terms survive:

\[
 X^2=2e_{q,0}e_{u,0}\ne0,qquad
 Y^2=2e_{r,0}e_{v,0}\ne0,                                     \tag{29}
\]

and

\[
                              \xi\eta=X^2+3XY+2Y^2.             \tag{30}
\]

Indeed every nonzero \(\lambda X+\mu Y\) has support two when one of
\(\lambda,\mu\) is zero and support four otherwise.  Thus the entire
inverse-channel plane contains no one-site-supported form.

Finally, here \(m=4\) and \(R=3\).  The complete mixed coordinate row at
\((p,0),(s,1)\) is

\[
 \bigl(3\xi\eta+A_{ps}(0,1)z\bigr)z^{[2]}=0,                   \tag{31}
\]

because the parenthesis vanishes literally by (21)--(22).  Equivalently,
the coefficient of **every** residual colour word in the matching tensor
with exposed colours \(0\) at \(p\) and \(1\) at \(s\) is zero, exactly
as required by the ternary target.  Thus (27), goodness, and the full mixed
slice coexist with (29)--(30).

The selected \(\xi,\eta,z\) use only \(q,r,u,v\), so this top slice is
also support-vacuous at \(t,w\).  The guard therefore does not test a
nonzero six-site selected cofactor.  Its stronger content is the literal
power-free source identity \(3\xi\eta+z=0\), together with goodness supplied
by endpoint colours invisible to that slice.

The other exposed-colour rows were not chosen to equal the ternary target,
so this is not a counterexample to the conjecture.  It is a source-level
countermodel to the proposed local implication

\[
 \{\text{good fan},\ \kappa\ne0,\ \text{complete selected mixed row}\}
 \Longrightarrow
 \{\text{inverse channel is one-sided}\}.                       \tag{32}
\]

## 5. Exact remaining lemma for a selector bypass

The determinant inversion has therefore reached its natural endpoint.  A
direct selector proof must add a statement not contained in the curvature
minor or its mixed target projection.  One adequate form would be:

> **Physical channel-sparsification lemma.**  In a full exact ternary
> source, the transverse exposed-colour rows coupled to some nonzero
> curvature square force the associated normalized channel forms to have
> a square-zero response (or force their same-channel terms into a
> common-power annihilator which makes the full clean error vanish).

By Lemma 2.1, literal square-zero is exactly a support theorem, not a
formal consequence of invertibility.  If only annihilation after a common
power is proved, the conclusion must be stated at the level of the full
homogeneous clean error; cancelling the common power is not valid in the
site-square-zero algebra.

This sharply separates the two remaining mechanisms:

1. prove channel sparsification from the **other** diagonal and mixed
   exposed-colour rows, thereby obtaining a genuine selector/clean cap; or
2. use those transverse rows directly to force a common active zero of the
   canonical clean-error line.

No large graph case split is involved.  What is ruled out is the shorter
step “invert \(AU-BF\), then project”: the inversion and the matching
projection live in different Schur functors, and the exact guard above
realizes the discrepancy with literal aggregate blocks.
