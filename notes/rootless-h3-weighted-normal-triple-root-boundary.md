# A transported weighted normal can still fill the \(h=3\) triple-root residual block

## 1. Outcome

This note isolates one sharp boundary at the anchored six-site rootless
interface.  It does not construct a full physical source and does not close
the clean-point problem.

There are two logically separate tasks after two differently labelled
diagonal anchors have aligned a completed \(2\times2\) label square.

1. The crossed four-index row must transport the weighted curvature-normal
   class through the fixed-chart selector-provenance quotient.
2. That transported class must meet the divisor of the exposed cubic on the
   physical binary cap line, so that it yields a nonzero functional on the
   residual Macaulay quotient.

The first task does not imply the second, even when the crossed row has a
nonzero selector-provenance class and therefore really does span the static
quotient.  At the first boundary, normalize the exposed cubic to

\[
                         f=v^3
\]

and suppose the completed label square leaves one weighted-normal cubic

\[
             g=a u^3+b u^2v+cuv^2+dv^3.                 \tag{1}
\]

Then, for

\[
                 Q_f=S_5/fS_2,\qquad S=\mathbb Q[u,v],
\]

multiplication by \(g\) has matrix

\[
 \boxed{
 M_{f,g}=
 \begin{pmatrix}
 a&0&0\\
 b&a&0\\
 c&b&a
 \end{pmatrix},qquad
             \det M_{f,g}=a^3.}                          \tag{2}
\]

Thus the single coefficient

\[
                 \boxed{\chi_{f,g}=g(1,0)=a}             \tag{3}
\]

is necessary and sufficient for rank three on this normalized
one-channel, triple-root boundary.  If \(a=0\), evaluation at the root
\([1:0]\) of \(f\) is a nonzero residual Macaulay annihilator.  If
\(a\ne0\), \(gS_2\to Q_f\) is an isomorphism and no such annihilator exists.

An exact rational packet below has all of the following simultaneously:

* two differently labelled diagonal anchors;
* a crossed row with nonzero class in the completed-square quotient;
* static transport of the edge/curvature sum by that crossed row;
* a nonzero weighted \(K_6\) four-cycle normal with the same scalar value;
  and
* \(f=v^3,\ g=u^3\), so \(\chi_{f,g}=1\) and the residual Macaulay map is
  an isomorphism.

This is a sharp associated-graded negative boundary.  It strengthens the
older static guards, in which the crossed row itself vanished in the
selector quotient: here the crossed row passes that test.  What remains
missing is a **line-dependent, grade-preserving coefficient** forcing
\(\chi_{f,g}=0\), or directly constructing the corresponding degree-five
functional.  Static matrix provenance, even when successful, does not
supply that coefficient.

The construction is deliberately a fibre product of exact quotient layers,
not a decorated site-square-zero realization of the full two-chart source.
Additional coupled full-nine coefficients may rule it out.  Accordingly it
is not a counterexample to the proposed anchored overlap theorem or to
Krenn's conjecture.

## 2. A crossed row which genuinely transports the static normal

Use two fixed physical labels \(r,s\) and put

\[
 d=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 H^\rightarrow=E_{rs},\qquad
 H^\leftarrow=2E_{sr}.                                  \tag{4}
\]

Both assignment tables are nonzero rank-one matrices.  Their sum and
crossed difference are

\[
 B=H^\rightarrow+H^\leftarrow
   =\begin{pmatrix}0&1\\2&0\end{pmatrix},\qquad
 J=H^\rightarrow-H^\leftarrow
   =\begin{pmatrix}0&1\\-2&0\end{pmatrix}.             \tag{5}
\]

Let \(\Delta\) be the diagonal matrices.  Since both off-diagonal entries of
\(d\) are nonzero, the quotient

\[
                   {\rm Mat}_2/(\Delta+\mathbb Qd)
\]

is one-dimensional, with coordinate

\[
                  \omega_d(F)=d_{sr}F_{rs}-d_{rs}F_{sr}
                              =F_{rs}-F_{sr}.             \tag{6}
\]

Here

\[
                       \omega_d(B)=-1,\qquad
                       \omega_d(J)=3.                     \tag{7}
\]

In particular the crossed row is not class-zero.  More explicitly,

\[
 \boxed{
 B=-\frac13J+\frac43d+
       \operatorname {diag}\!\left(-\frac43,-\frac83\right).}
                                                                  \tag{8}
\]

The two diagonal terms in (8) are exactly the two differently labelled
anchors.  Thus, if \(J\) has been proved to be an admitted source-valid row
on the same filtered selector family, (8) transports \(B\) at the static
matrix layer.  This packet is strictly beyond the boundary
\(\omega_d(J)=0,\ \omega_d(B)\ne0\).

The two oriented curvature tables

\[
       K^\rightarrow=d-H^\rightarrow,\qquad
       K^\leftarrow=d-H^\leftarrow                         \tag{9}
\]

obey both exact channels

\[
 K^\rightarrow-K^\leftarrow+J=0,\qquad
 K^\rightarrow+K^\leftarrow=2d-B.                         \tag{10}
\]

Thus no sign or sum/difference ambiguity is being hidden in (8).

For completeness, this square embeds in a formal full-label top map.  With
labels \(r,s,t\), take

\[
 D=\begin{pmatrix}1&1&0\\1&2&0\\0&0&1\end{pmatrix}.
\]

For each of two chart copies introduce nine independent cap symbols
\(v_{ij}^{(\nu)}\), a top symbol \(Q_\nu\), and the common labelled targets
\(X_r,X_s,X_t\).  Define

\[
 M_\nu(v_{ij}^{(\nu)})=\delta_{ij}X_i-D_{ij}Q_\nu.       \tag{11}
\]

Then all eighteen formal normalized rows

\[
                  D_{ij}Q_\nu+M_\nu(v_{ij}^{(\nu)})
                          =\delta_{ij}X_i                 \tag{12}
\]

hold, with the same physical labels on the two copies.  Formula (12) only
records the full-nine associated-graded top map.  The independent symbols
are not asserted to be products of literal stars in one exact source; this
is precisely why the packet is a boundary rather than a source
counterexample.

## 3. The same scalar is a nonzero weighted \(K_6\) normal

On the six residual vertices \(0,\ldots,5\), take the uniform nonzero
vertex-factor base

\[
                            q_e=1\qquad(e\in\tbinom{[6]}2).
\]

Use the four-cycle on the rectangle with rows (0,2) and columns (1,3):

\[
 c_{01}=c_{23}=1,\qquad c_{03}=c_{12}=-1.                \tag{13}
\]

At this uniform base the weighted edge covector is \(\lambda=c\), and its
transport through the matching-Lefschetz map is the complementary-cut
covector

\[
                         \mu_V=c_{V^c}.                    \tag{14}
\]

The checker verifies the full identity

\[
                         \mu^{\mathsf T}T_q=\lambda^{\mathsf T}
                                                                  \tag{15}
\]

on all fifteen edge basis vectors.  Now take the rank-one correction

\[
                         \beta_{01}=-1,qquad
                         \beta_e=0\quad(e\ne01).          \tag{16}
\]

Then

\[
 \boxed{
 \mu^{\mathsf T}T_q\beta=\lambda(\beta)=-1=\omega_d(B).} \tag{17}
\]

The finite displayed rectangle is

\[
                  Q+R=\begin{pmatrix}0&1\\1&1\end{pmatrix},
                  \qquad\det(Q+R)=-1,                     \tag{18}
\]

so (17) is also its finite curvature determinant.  By contrast the radial
direction has \(\lambda(q)=0\).  Therefore the scalar in (17) is a genuine
transverse weighted normal, not radial padding.

Equations (8) and (17) deliberately grant both pieces of aggregate/static
transport which were absent in the earlier guards.  They still say nothing
about where the resulting cubic vanishes on the binary cap line.

## 4. The exact triple-root residual calculation

Use the ordered monomial bases

\[
 S_2=(u^2,uv,v^2),\qquad
 Q_{v^3}=(\overline{u^5},\overline{u^4v},
                         \overline{u^3v^2}).              \tag{19}
\]

Indeed \(v^3S_2\) is the span of the last three degree-five monomials.
Multiplying (1) by the three quadratic basis elements and reducing modulo
\(v^3S_2\) gives

\[
\begin{aligned}
 g u^2&\longmapsto (a,b,c)^{\mathsf T},\\
 g uv &\longmapsto (0,a,b)^{\mathsf T},\\
 g v^2&\longmapsto (0,0,a)^{\mathsf T}.
\end{aligned}                                             \tag{20}
\]

This proves (2).  It also proves both directions of the sharp boundary.

* If \(a\ne0\), the three columns in (20) are a basis of \(Q_f\).  Hence
  every functional annihilating the residual image is zero.
* If \(a=0\), coefficient evaluation

  \[
                       \varepsilon(\overline h)=[u^5]h
                                                               \tag{21}
  \]

  is well defined on \(Q_f\), is nonzero, and kills all three columns in
  (20).  In projective language it is evaluation at \([1:0]\), the support
  of the divisor \(V(v^3)\).

For the boundary packet take

\[
                             f=v^3,\qquad g=u^3.          \tag{22}
\]

Then \(f\) and \(g\) are coprime, the full six-column Macaulay map

\[
                         fS_2\oplus gS_2=S_5             \tag{23}
\]

is an isomorphism, and \(\chi_{f,g}=1\).  Multiplying the static normal
\(B\), crossed row \(J\), and \(K_6\) correction \(\beta\) by the same
scalar cubic \(g\) preserves (8), (10), and (17) coefficientwise.  It does not
turn any of them into a nonzero functional annihilating (23).

A leading-coefficient mutation is sharp.  Replacing \(g=u^3\) by, for example,

\[
                         g=u^2v+2uv^2+3v^3                 \tag{24}
\]

changes the decisive coefficient \(a\) from \(1\) to \(0\); the lower
coefficients do not affect the determinant criterion.  The residual rank
becomes two and (21) is the required annihilator.

## 5. The minimal missing coefficient on this boundary

Let a line-dependent weighted normal be written on the completed square as

\[
                         \mathcal N(u,v)=g(u,v)B.          \tag{25}
\]

Since \(\omega_d(B)=-1\), the divisor-incidence coefficient is equivalently

\[
 \boxed{
 \chi_{f,\mathcal N}
    =-\,[u^3]\omega_d(\mathcal N)
    =g(1,0).}                                             \tag{26}
\]

On the normalized one-channel triple-root stratum, (26) is one scalar and
is necessary and sufficient:

\[
 \chi_{f,\mathcal N}=0
 \quad\Longleftrightarrow\quad
 \varepsilon\bigl(gS_2\bigr)=0
 \quad\Longleftrightarrow\quad
 \operatorname {rank}(gS_2\to Q_f)\le2.                 \tag{27}
\]

Neither the two anchors nor (8) constrains (26); they live in the static
label-matrix quotient.  Equation (17) normalizes the class but in the
boundary packet makes (26) nonzero.  The crossed row controls the same
static class, yet without a source-faithful binary-line comparison it does
not force the class to meet \(V(f)\).

Therefore a positive two-chart argument on this stratum needs one of the
following genuinely new outputs:

1. a literal coefficient-cut identity, before the common power is
   cancelled, which forces \(\chi_{f,\mathcal N}=0\); or
2. the degree-five functional (21), transported from the physical rows and
   proved to kill every residual channel.

If more than one independent residual cubic survives, the corresponding
condition is that **each** value at \([1:0]\) vanish.  The one-scalar claim
in (26) is only for the completed-square one-channel boundary.  For a
squarefree or differently nonreduced exposed cubic, the analogous object is
the appropriate evaluation/principal-part component on \(V(f)\); no
uniform reduction to (26) is claimed here.

## 6. Exact scope

The packet proves the following narrow negative statement:

\[
 \boxed{
 \begin{gathered}
 \text{two labelled anchors}
 +\text{a crossed row nonzero in the static quotient}\\
 +\text{static transport of the weighted normal}
 +\text{a nonzero weighted }K_6\text{ curvature value}\\
 \not\Longrightarrow
 \text{a residual }h=3\text{ Macaulay annihilator}
 \end{gathered}}
                                                               \tag{28}
\]

when these data are retained only as the exact associated-graded layers
displayed above.  This does not show that the complete literal two-chart
overlap permits their decoupling.  Proving that it does not is precisely the
remaining source-provenance problem.

The contribution is the sharp stopping coefficient (26).  It distinguishes
three statements which should not be conflated:

* \(\omega_d(J)\ne0\): the crossed row spans the static selector quotient;
* \(\mu^{\mathsf T}T_q\beta\ne0\): the finite curvature-normal class survives
  the weighted aggregate comparison; and
* \(\chi_{f,\mathcal N}=0\): that class meets the exposed divisor and creates
  a residual Macaulay functional.

The first two hold in the boundary packet while the third fails.

The dependency-free checker
[`verify_rootless_h3_weighted_normal_triple_root_boundary.py`](../computations/verify_rootless_h3_weighted_normal_triple_root_boundary.py)
audits the two-anchor relation (8), both curvature channels (10), all
eighteen formal full-label top rows, the weighted \(K_6\) identity (15) on
all edge basis vectors, the finite normal (17), the general triangular
matrix (2) on exact rational probes, the rootless isomorphism (23), and the
sharp rank-two mutation (24).  It uses explicit runtime failures and runs
unchanged under `python -O`.
