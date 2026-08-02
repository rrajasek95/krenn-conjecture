# Independent audit: sitewise covariance supplies no face homotopy

This note independently audits commit `022ced5`.  The calculation is sound,
with the bounded scope stated in that commit: it excludes the bare sitewise
\(GL(3)\) connection cube and constant-coefficient cancellation between its
five deletion faces.  It does **not** exclude unrelated source syzygies,
higher-degree corrections, or a class created by non-flat specialization.

## Re-derivation

For a four-site face \(F\), I rebuilt

\[
 T_F=\sum_{c\in\{0,1,2\}^F}\operatorname{Haf}(q_c)e_c
\]

directly from its three perfect matchings.  At a site \(x\), put

\[
 D_{x;a\leftarrow b}=\sum_{y\ne x,j}
 q_{xy}^{bj}{\partial\over\partial q_{xy}^{aj}},
 \qquad
 L_{x;a\leftarrow b}e_c=
 \mathbf 1_{c_x=b}e_{c[x:=a]}.
\]

For a fixed output word, every matching has exactly one edge incident with
\(x\).  If that word has color \(a\) at \(x\), differentiation changes the
color on that unique endpoint from \(a\) to \(b\); otherwise it gives zero.
This is exactly the coefficient selected by \(L_{x;a\leftarrow b}\), hence

\[
                         D_{x;a\leftarrow b}T_F
                         =L_{x;a\leftarrow b}T_F.
\]

The audit checks all \(4\cdot 9=36\) matrix units on each face.  This also
checks the diagonal case: its source operator is the endpoint Euler
operator, and a perfect matching has one incident endpoint at the named
site.

Take \(\bar m=12112\), delete \(v\), and use

\[
 L_x=L_{x;0\leftarrow\bar m_x},\qquad
 D_x=D_{x;0\leftarrow\bar m_x}.
\]

For any choice of one of \(L_x,D_x\) at each of the four remaining sites,
the original output color is \(\bar m_x\) at an \(L\)-site and zero at a
\(D\)-site.  Every final output color is zero.  The coefficient color is
\(\bar m_x\) in both cases: it is selected directly at an \(L\)-site and is
changed from zero by the source derivative at a \(D\)-site.  Thus every one
of the sixteen corners equals

\[
             \operatorname{Haf}(q_{\bar m}|_{F_v})Y_0=h_vY_0.
\]

The independent program compares these coefficients with all fifteen
displayed monomials in the earlier denominator-reset note, rather than only
comparing the corners with one another.  Therefore

\[
 \prod_{x\in F_v}(L_x-D_x)T_{F_v}
   =(1-1)^4h_vY_0=0.
\]

Actions at distinct sites commute even when they touch the same edge: they
act on its two separately labelled endpoint colors.

## Target and ranks

The diagonal target is checked at every corner, not just at the all-\(L\)
and all-\(D\) corners.  Any corner containing a \(D\) vanishes because the
target is independent of \(q\).  The all-\(L\) corner vanishes because each
face tag

\[
                 2112,\ 1112,\ 1212,\ 1212,\ 1211
\]

contains both 1 and 2, whereas a diagonal word has one color at all sites.

An independent rational row reduction gives

\[
 \operatorname{rank}\{h_v\}=5,\qquad
 \operatorname{rank}\{g_v\}=5,\qquad
 \operatorname{rank}\{g_v,h_v\}=10.
\]

This can also be seen from supports: different deletion faces omit different
vertices, and the \(g_v\) use only color \(00\), while the \(h_v\) use only
colors 1 and 2.  The all-output and all-derivation lists are literally the
same five polynomials.  Consequently a constant combination that kills the
derivation companions also kills the desired output residues.

## Precise scope

The conclusion is not a general no-go for source syzygies.  A Weyl-algebra
identity \((L-D)T_F=0\) is only horizontality.  The source presentation has
polynomial coefficients, not formal derivative or jet generators, so the
calculation does not provide a chain with boundary \(h_vY_0\).  Conversely,
it does not prove that no larger source resolution can provide one.  In
particular it leaves open:

- a physical full-nine row or a proved Spencer contraction;
- a higher-\(q\)-degree syzygy whose initial terms cancel differently; and
- a specialization-created \(\operatorname{Tor}_1\) transgression.

Thus the exact safe conclusion is: the obvious covariance construction
produces a locked equality, not any of the five missing \(\tau_v\).

## Verification

The dependency-free checker
[verify_h3_sitewise_gl3_covariance_face_tau_no_go_independent_audit.py](../computations/verify_h3_sitewise_gl3_covariance_face_tau_no_go_independent_audit.py)
was run under normal Python and with `-O`, `-I`, and `-S`.  It verifies 180
local covariance identities, 80 universal connection corners, 80 diagonal
target corners, the five explicit \(h_v\), and the ranks \(5,5,10\).  Its
ledger digest is

    715d547ff6ec44e1be907193d64d64c7efe603476448fa3ac3d93c9db32f81b7
