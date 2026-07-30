# A physical dark cut need not be Hessian-compatible

## 1. Outcome

The literal cap identity, factor rank one, and the two-site quotient purity
do **not** force the aggregate Hessian compatibility

\[
                   d\kappa_q(\ker H_q)=0.                 \tag{1}
\]

The corank-one scalar guard from
[the general \(K_6\) pullback audit](general-k6-curvature-rowspace.md)
has an exact one-colour decorated lift.  On six residual sites it has

\[
        \beta=LS,\qquad \beta\mathfrak q^{[2]}=X_a,       \tag{2}
\]

exactly two target-blocked sites, the pure two-site quotient from the
blocked-site descent, and a nonzero literal transition curvature.  Yet its
physical scalarization has a corank-one Hessian and

\[
        d\kappa_q(z)=-1\ne0\qquad(z\in\ker H_q).           \tag{3}
\]

This negative statement is deliberately limited to the displayed physical
data.  The lift is not a full-nine source.  In fact it can be completed so
that both endpoint triples are injective, the direct block is invertible,
the selected diagonal row holds, and all six off-diagonal rows hold.  The
only failed rows are the other two diagonal target anchors.  This is exactly
the same row-level gap as in the one-row guard of
[the blocked-site descent](target-blocked-site-polar-descent.md), now with
the corank-one Hessian obstruction retained.

Thus the next possible compatibility theorem must genuinely use one of
those unused diagonal anchors, or an overlapping second chart which couples
it to the selected scalarization.  The seven-row packet below cannot refute
a theorem using the complete full-nine source.

## 2. Minimal decorated lift

Let \(W=\{0,\ldots,5\}\), let every local space have basis
\(e_a,e_b,e_\delta\), and write \(x_{i,c}\) for \(e_c\) at site \(i\).
In the site-square-zero algebra put

\[
\begin{aligned}
 Q=\{&01,02,03,04,05,12,13,14,23,45\},\\
 \mathfrak q&=\sum_{ij\in Q}x_{i,a}x_{j,a},\\
 L&=x_{0,a},\qquad S=x_{1,a},\qquad
 \beta=LS=x_{0,a}x_{1,a}.                                \tag{4}
\end{aligned}
\]

Only the matching \(23\mid45\) of the four sites complementary to
\(01\) occurs in \(\mathfrak q^{[2]}\).  Hence, with literal divided
powers,

\[
                    \beta\mathfrak q^{[2]}=X_a.           \tag{5}
\]

There are no auxiliary decorated terms in (4): this is the one-colour
embedding of the scalar guard itself.

The local cap planes are

\[
 H_0=H_1=\mathbb C e_a,\qquad H_2=H_3=H_4=H_5=0.          \tag{6}
\]

Thus \(B_a=\{0,1\}\).  Retain sites \(0,1\), contract them by
\(e_a^*\), and quotient the other four sites by their \(H_i\)'s.  The
two-site identity is literally

\[
 \beta_{01}(e_a^*,e_a^*)
       (\mathfrak q|_{\{2,3,4,5\}})^{[2]}
   =x_{2,a}x_{3,a}x_{4,a}x_{5,a}.                         \tag{7}
\]

In particular the physical dark matching is \(23\mid45\).  This verifies
the strong quotient conclusion, not just a nonzero top scalar.

## 3. The surviving Hessian-kernel obstruction

Probe every site by \(e_a^*\).  The resulting scalar edge array is

\[
 q_{ij}=\begin{cases}1,&ij\in Q,\\0,&ij\notin Q,
       \end{cases}
 \qquad \beta_q=\mathbf e_{01}.                            \tag{8}
\]

For

\[
                   \kappa(q)=q_{01}q_{23}-q_{02}q_{13},    \tag{9}
\]

the base is four-cycle-flat and

\[
 \lambda=d\kappa_q
   =\mathbf e_{01}+\mathbf e_{23}
      -\mathbf e_{02}-\mathbf e_{13},
 \qquad \lambda(\beta_q)=1.                              \tag{10}
\]

The weighted \(K_6\) Hessian has

\[
 \operatorname{rank}H_q=14,
 \qquad
 z=\mathbf e_{02}-\mathbf e_{03}
       -\mathbf e_{24}+\mathbf e_{34}\in\ker H_q.         \tag{11}
\]

But \(\lambda(z)=-1\).  Therefore

\[
             \lambda\notin\operatorname{row}H_q,          \tag{12}
\]

so no aggregate four-set pullback exists.  Equations (5) and (7) explain
why the extra decorated information does not change this calculation: after
the physical probes it says exactly that the one-edge cap has a nonzero
complementary hafnian.  It supplies no equation on the other fourteen edge
directions, including the kernel direction (11).

## 4. Exact seven-row completion

The preceding lift can retain the strongest harmless parts of a full-nine
chart.  Set

\[
 (p_a,p_b,p_\delta)=(x_{0,a},x_{1,a},x_{2,a}),\qquad
 (s_a,s_b,s_\delta)=(x_{1,a},x_{0,a},x_{2,a}).             \tag{13}
\]

Both triples are linearly independent.  There are four perfect matchings
in \(Q\), so

\[
                        \mathfrak q^{[3]}=4X_a.            \tag{14}
\]

The coefficients of \(p_i s_j\mathfrak q^{[2]}\) form the matrix

\[
 T=\begin{pmatrix}
 1&0&1\\
 0&1&1\\
 1&1&0
 \end{pmatrix},
 \qquad
 p_i s_j\mathfrak q^{[2]}=T_{ij}X_a.                      \tag{15}
\]

Choose the direct block

\[
 d={E_{aa}-T\over4}
   ={1\over4}\begin{pmatrix}
       0&0&-1\\
       0&-1&-1\\
       -1&-1&0
     \end{pmatrix},
 \qquad \det d={1\over64}\ne0.                           \tag{16}
\]

Then every one of the nine left sides is audited at once:

\[
 d_{ij}\mathfrak q^{[3]}+p_i s_j\mathfrak q^{[2]}
                         =(E_{aa})_{ij}X_a.                \tag{17}
\]

Consequently the \((a,a)\) row is exactly \(X_a\), and all six
off-diagonal rows are exactly zero.  The row ledger fails only at

\[
 (b,b):\quad0\ne X_b,
 \qquad
 (\delta,\delta):\quad0\ne X_\delta.                     \tag{18}
\]

This is the same pair of unused diagonal anchors missing in the earlier
blocked-site guard.  The present packet is stronger in a different
direction: it preserves the smooth corank-one Hessian obstruction and even
has an invertible direct block.

For the selected functional \(\ell=E_{aa}\), one has \(\ell(d)=0\), so
the selected cap remains the direct-zero rank-one cap (4).  At its literal
edge \(01\), the two oriented endpoint products from (13) are
\(E_{aa}\) and \(E_{bb}\).  Thus

\[
 \ell(d-E_{aa})=-1,
 \qquad
 \ell(d-E_{bb})=0.                                       \tag{19}
\]

The same cap therefore detects a nonzero physical transition curvature at
the same edge.  Curvature visibility does not repair (12).

## 5. Exact scope

The construction proves that none of the following, alone or together,
implies Hessian row-space compatibility:

* a literal decorated identity \(\beta\mathfrak q^{[2]}=X_a\);
* factor rank one for \(\beta\);
* the pure two-site blocked-target quotient;
* a nonzero physical dark matching and four-cycle differential;
* a nonzero literal transition curvature;
* the selected diagonal plus all six off-diagonal full-nine rows, even with
  injective endpoint triples and invertible \(d\).

It does **not** test the two missing diagonal anchors or any overlapping
second chart.  It also does not reach the filtered source-provenance module:
the aggregate pullback already fails at (12), one stage earlier.

The lightweight exact checker
[`verify_physical_dark_cut_hessian_kernel_counterlift.py`](../computations/verify_physical_dark_cut_hessian_kernel_counterlift.py)
audits the decorated matching products, the quotient, the rank and kernel,
the seven-row ledger, direct-block determinant, and transition evaluation.
