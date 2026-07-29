# The scalar-unit boundary can miss exactly one full four-cut row

## 1. Outcome

At the first six-site common complement, the scalar-unit obstruction can
be sharper than the isotropic-packet guard.  There are exact data with

\[
 U=E_{22}
\]

for which both triples \((t_0,t_1,t_2)\) and \((v_0,v_1,v_2)\) are
injective, both star pairs obey the two-dark-colour conclusion, and **80 of
the 81 full uncontracted four-cut rows hold for arbitrary direct block
\(A=(a_{ab})\)**.  The sole residual is

\[
 (a,b;c,d)=(2,2;2,2),\qquad -X_2^D.                    \tag{1}
\]

Thus injectivity of the two scalar-unit-side star triples, even together
with every target-zero row and the two colour-zero/one target rows, does
not reconstruct the exceptional coefficient.  This is a guard, not an
exact source: the opposite \(x\)- and \(y\)-triples remain sparse of rank
two, and the rank-three internal graph is empty.

## 2. Data

Take \(m=5\), \(D=\{0,1,2,3,4,5\}\), and write \(e_c^{(s)}\) for colour
\(c\) at site \(s\).  Put

\[
 z=e_0^{(2)}e_0^{(3)}+e_1^{(0)}e_1^{(4)},               \tag{2}
\]

\[
\begin{array}{c|ccc}
c&0&1&2\\ \hline
t_c&e_0^{(0)}&e_1^{(1)}&e_2^{(3)}\\
v_c&e_0^{(1)}&e_1^{(2)}&e_2^{(3)},
\end{array}                                               \tag{3}
\]

and

\[
\begin{array}{c|ccc}
c&0&1&2\\ \hline
x_c&e_0^{(4)}&e_1^{(5)}&0\\
y_c&e_0^{(5)}&e_1^{(3)}&0.
\end{array}                                               \tag{4}
\]

The rows in each triple in (3) are linearly independent.  Moreover
\(t_0v_0,t_1v_1,x_0y_0,x_1y_1\) are nonzero, while

\[
                         t_2v_2=x_2y_2=0,                \tag{5}
\]

so each pair has exactly one dark diagonal colour.

The two cells of \(z\) are disjoint, hence

\[
 z^{[2]}=e_1^{(0)}e_0^{(2)}e_0^{(3)}e_1^{(4)}\ne0,
 \qquad z^{[3]}=0.                                      \tag{6}
\]

## 3. All 81 differences

At \(m=5\), the exact four-cut row is

\[
\begin{aligned}
 &a_{ab}u_{cd}z^{[3]}+a_{ab}t_cv_dz^{[2]}
 +u_{cd}x_ay_bz^{[2]}+x_ay_bt_cv_dz\\
 &\hspace{42mm}=\delta_{a=b=c=d}X_a^D.                 \tag{7}
\end{aligned}
\]

The arbitrary-\(A\) terms vanish separately.  The first vanishes by
\(z^{[3]}=0\).  For every \((c,d)\), the second vanishes: for the two live
diagonal channels this follows from collision with sites \(0\) and \(2\)
of (6), every channel involving colour 2 collides at site \(3\), and the
remaining mixed channel already collides at site \(1\).

For \((c,d)=(2,2)\), (5) kills the fourth term.  Every nonzero basic
product \(x_ay_b\) collides with (6), so the third term also vanishes.
Consequently all nine \(E_{22}\) rows have zero left side; eight have zero
target, while the \((2,2;2,2)\) row has difference (1).

For \((c,d)\ne(2,2)\), the surviving fourth-layer products are exactly

\[
 x_0y_0t_0v_0z=X_0^D,
 \qquad x_1y_1t_1v_1z=X_1^D.                           \tag{8}
\]

Every other fourth-layer row collides at a displayed physical site.  This
proves all remaining rows of (7), and hence the claimed unique residual.

## 4. Scope

The construction removes one tempting repair of the full-isotropic guard:
connected-spanning rank-three provenance does imply that the full
\(t\)- and \(v\)-star maps are injective, but injectivity alone does not
recover the missing scalar-unit row.  A successful E1 continuation must
jointly use the dense opposite \(x/y\) rows or the actual invertible-block
graph/common-power provenance with the exceptional target equation.

The lightweight checker
[`verify_uncontracted_four_cut_scalar_unit_eighty_row_injective_guard.py`](../computations/verify_uncontracted_four_cut_scalar_unit_eighty_row_injective_guard.py)
enumerates the 81 rows against a basis of all direct blocks \(A\), checks
the divided powers and the unique signed residual, and audits the two
triple ranks and diagonal-product pattern exactly over \(\mathbb Q\).
