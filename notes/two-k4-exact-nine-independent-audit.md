# Independent audit of the exact-nine \(K_4\)-by-\(K_4\) frontier

## Outcome

The reduction in
[the exact-nine frontier note](two-k4-exact-nine-k33-frontier.md)
is sound after one necessary weighted-coefficient correction.  The two
right edges used in the final disjoint-orbit certificate need not have the
same internal weight.  Writing

\[
 \alpha=\lambda_{03}\rho_{02},\qquad
 \beta=\lambda_{03}\rho_{12},
\]

the certificate is \(\alpha\beta\), not \(\lambda^2\).  Both factors are
nonzero in the standard two-\(K_4\) chart, so the contradiction is
unchanged.  The frontier note and its primary checker now retain these
weights separately.

The independent executable audit is
[this checker](../computations/verify_two_k4_exact_nine_independent_audit.py).

## 1. Census and orbit completeness

The audit reimplements, rather than imports,

1. the pre-seven full-row/two-defect and two-singleton rules;
2. the separated singleton-plus-degree-two rule on both shores; and
3. the full \(S_4\times S_4\) action together with transposition.

Direct enumeration leaves \(2752\) of the \(\binom{16}{9}\) supports.
The nine displayed representatives generate pairwise disjoint orbits of
sizes

\[
 288,\ 16,\ 288,\ 192,\ 576,\ 576,\ 576,\ 144,\ 96,
\]

whose union is exactly the complete survivor set.  The perfect-matching
counts of their nonsingular complements are also independently
\(0,0,0,1,1,1,2,2,2\).  They are diagnostic only and are not used to
discard any orbit.

## 2. Legality of the seven overlap-one applications

For every claimed row pair, the audit checks that each actual singular
set is contained in the displayed selected two-set, that the two selected
sets meet in exactly the stated common site, and that every unselected
component is invertible.  The three padded cases are

\[
\begin{array}{c|c|c}
H_2&\{0,3\},\ \{3\}\subset\{1,3\}&h=3\\
H_4&\{0,2\},\ \{2\}\subset\{1,2\}&h=2\\
H_6&\{2,3\},\ \{2\}\subset\{0,2\}&h=2.
\end{array}
\]

This is legal because the overlap-one lemma requires only the two
*unselected* maps of each star to be invertible; selected maps are
arbitrary and may themselves be invertible.  The \(H_3\) application
passes the same check after transposition.  The primary checker now also
verifies all \(8\cdot729\) selected sector coefficients while retaining
one symbolic selected-left-edge weight and six independent symbolic
right-edge weights.  Thus no unit-weight specialization is used in the
pullback.

## 3. Disjoint-orbit quantifiers

For a disjoint pair, Lemma 3.1 has four cases.  If both exceptional pairs
contain a nonzero map, \(q_{\rm eff}=0\); if exactly one whole pair is
zero, \(q_{\rm eff}\) lies on one opposite edge.  Either conclusion gives
an endpoint with three vanished incident blocks and hence the usual
three-lines-versus-one-plane contradiction.  Therefore a selected
disjoint sector can survive only when **all four** exceptional blocks are
literal zero.

Applying this to rows \(1,2\), rows \(1,3\), and then to columns \(0,3\)
and \(1,3\), gives the four required zero unions

\[
\begin{split}
&\{10,11,22,23\},\quad \{10,11,32,33\},\\
&\{00,10,23,33\},\quad \{01,11,23,33\}.
\end{split}
\]

Their complement inside the nine singular positions is exactly
\(\{02\}\).  An independent enumeration of all \(2^9\) literal-zero
branches therefore leaves only the empty nonzero set and
\(\{B_{02}\}\), as claimed.

In either surviving branch, the vanished \(02\) and \(12\) effective
blocks have the form

\[
 \alpha E_{11}+u_0v^{\mathsf T}=0,\qquad
 \beta E_{22}+u_1v^{\mathsf T}=0.
\]

With

\[
 f_{11}=\alpha+u_{0,1}v_1,\quad
 f_{12}=u_{0,1}v_2,\quad
 g_{22}=\beta+u_{1,2}v_2,
\]

direct expansion gives

\[
 \beta f_{11}
 -v_1(u_{0,1}g_{22}-u_{1,2}f_{12})=\alpha\beta\ne0.
\]

This is division-free and also covers \(v=0\), hence \(B_{02}=0\).

## 4. Exact residual

After the seven overlap closures and the disjoint closure, the only
position orbit left is

\[
                 012\mid012\mid012\mid\varnothing.
\]

On either shore it has degree profile \((3,3,3,0)\).  Thus only the
regular star can have its singular components contained in a two-element
selected set, so no pair of stars satisfies either exact-eight local
hypothesis.

The independent audit rebuilds the erased-Hessian matrix for

\[
P_0=P_1=P_2=S_0=S_1=S_2=\operatorname{diag}(1,0,0),
\qquad P_3=S_3=I.
\]

It has exact rank \(19\), and all \(27\) columns on edges incident with
site \(3\) are identically zero.  Consequently the \(K_{3,3}\) mask is
exactly the remaining position orbit and is a genuine residual for the
current local lemmas; this computation does not assert that it solves the
full tensor equations.

## 5. Reproduction

Run

~~~text
python computations/verify_two_k4_exact_nine_frontier.py
python computations/verify_two_k4_exact_nine_independent_audit.py
~~~

Both finish with PASS.
