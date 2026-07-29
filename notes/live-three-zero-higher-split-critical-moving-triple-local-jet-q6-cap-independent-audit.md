# Independent audit: the critical moving-triple local-jet \(q=6\) cap

## 1. Verdict and scope

**PASS.**  I reconstructed the
[critical local-jet theorem](live-three-zero-higher-split-critical-moving-triple-local-jet-q6-cap.md)
from the exact moving-triple transport and complementary-row conventions.
The factor \(B_j(z-j)\) really does lie in \({\cal S}_i\), and the
order-three functional at \(j\) has a regular nonzero local unit.  Thus
two maximal selections are impossible.

At \(r=4\), this proves that the \(4^3 3^6\) restored baseline has at
most one \(q=6\) moving-triple selection and at least five \(q=5\)
selections.  This is a dimension-distribution result, not a closure of
the two \(p=28\) collision tuples.

## 2. Exact transport indexing

At the threshold

\[
 p=r(r+3),\qquad c=r+5,\qquad r\geq4,                       \tag{1}
\]

a maximal selection at the moving triple \(i\) has relation space and
transport

\[
 {\cal S}_i\subseteq\mathbb C[z]_{\leq r+1},\quad
 \dim{\cal S}_i=r,
 \qquad
 {\cal T}_i=B_i{\cal S}_i,\qquad
 B_i=(z-i)^2(z+i)^2.                                       \tag{2}
\]

Restoring the selected simple class at \(i\) gives the common baseline.
For another moving value \(j\), the selection indexed by \(i\) has not
selected \(j\): it remains a complementary class of exact multiplicity
three.  This is the convention needed for the local row below.

The exact common rows bound the common kernel by \(r+2\).  Hence two
maximal transported \(r\)-spaces meet in dimension at least \(r-2\).
Structural noncollision makes \(B_i,B_j\) coprime, and

\[
 B_i\mathbb C[z]_{\leq r+1}\cap
 B_j\mathbb C[z]_{\leq r+1}
       =B_iB_j\mathbb C[z]_{\leq r-3},                      \tag{3}
\]

also of dimension \(r-2\).  Thus

\[
 {\cal T}_i\cap{\cal T}_j
       =B_iB_j\mathbb C[z]_{\leq r-3}.                      \tag{4}
\]

There is no reversal of the moving factor in (4).  Since
\({\cal T}_i=B_i{\cal S}_i\), multiplication by the nonzero polynomial
\(B_i\) is injective, and division of (4) by precisely that factor gives

\[
                       B_j\mathbb C[z]_{\leq r-3}
                                  \subseteq{\cal S}_i.       \tag{5}
\]

Because \(r\geq4\), \(z-j\in\mathbb C[z]_{\leq r-3}\).  Therefore

\[
             S_*=B_j(z-j)=(z-j)^3(z+j)^2\in{\cal S}_i.      \tag{6}
\]

This confirms the exact containment under the transport conventions.

## 3. The local unit cannot vanish or have a pole

The relation-space identity at a complementary root \(j\) of
multiplicity three has local form

\[
                    {U_{i,j}(z)S(z)\over(z-j)^4},            \tag{7}
\]

where every factor removed into \(U_{i,j}\) is coprime to \(z-j\).
The structural hypotheses give

\[
 j\ne0,\qquad j\ne\pm i,\qquad j\ne\pm\nu
 \quad\hbox{for every other value }\nu.                     \tag{8}
\]

Consequently \(U_{i,j}\) is regular at \(j\) and
\(U_{i,j}(j)\ne0\).  The zero residue of a derivative is exactly

\[
                       (U_{i,j}S)^{(3)}(j)=0.                \tag{9}
\]

The witness (6) has exact order three at \(j\), so lower derivatives of
the unit do not contribute to the third derivative.  Directly,

\[
 (U_{i,j}S_*)^{(3)}(j)
    =3!\,U_{i,j}(j)(2j)^2
    =24j^2U_{i,j}(j)\ne0,                                  \tag{10}
\]

contradicting (9).  The proof uses neither a formal divisibility not
supplied by the common lift nor an implicit constant-unit assumption.

## 4. The \(p=28\) specialization

For \(r=4\), the common baseline has mass thirty, nine value classes,
and restored profile \(4^3 3^6\).  Selecting a moving triple \(i\)
leaves

\[
                         4^3 3^5 1_i,                        \tag{11}
\]

so every other moving value \(j\) is indeed an exact complementary
triple.  In the tuple with one double, that double is held fixed in role
two and disappears from the complement; it does not alter (11), the
transport, or the local unit at \(j\).

Thus the theorem applies to exactly

\[
                  (3,6,0,0),\qquad(3,6,1,-2)                \tag{12}
\]

for every split \((h,k)=(22,6),\ldots,(27,1)\).

## 5. Independent executable audit

[verify_live_three_zero_higher_split_critical_moving_triple_local_jet_q6_cap_independent_audit.py](../computations/verify_live_three_zero_higher_split_critical_moving_triple_local_jet_q6_cap_independent_audit.py)
imports neither the primary checker nor another census.  It reconstructs
the threshold dimensions, the correct factor division, the literal local
derivative with a general cubic Taylor unit, all structural noncollision
factors, and both \(p=28\) tuples at all six splits.
