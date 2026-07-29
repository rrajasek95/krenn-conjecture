# Higher splits: the \(p=28\) \(4^3 3^6\) even--odd span drop

## 1. Result and scope

Continue from the
[first selected six-kernel boundary](live-three-zero-higher-split-p28-six-kernel-boundary.md).
At \(p=h+k=28\), consider a moving-triple family whose restored common
baseline is

\[
                              4^3 3^6.                         \tag{1}
\]

For each of the six triple values \(i\), selecting that class in role two
leaves relation complement

\[
                              4^3 3^5 1_i.                     \tag{2}
\]

This is the natural baseline for the two residual tuples
\((e,a,b,u)=(3,6,0,0)\) and \((3,6,1,-2)\); in the latter, the unique
double is held fixed in role two for every moving-triple selection.

**Theorem 1.1 (even--odd span drop).** The six moving-triple selections
cannot all have six-dimensional selected row kernel. Consequently at least
one has selected kernel dimension at most five.

This is only a dimension-drop theorem. It does not close either collision
profile or assert that every selected kernel of dimension at most five is
already contradictory.

The six repeated values are nonzero, distinct, and pairwise nonopposite.
In particular their squares are distinct.

## 2. Pair intersections fill their complete ambient spaces

Suppose all six selected kernels have dimension six. For a moving value
\(i\), the relation-space theorem applied to (2) gives

\[
 \mathcal S_i\subseteq\mathbb C[z]_{\le5},
 \qquad \dim\mathcal S_i=4.                                  \tag{3}
\]

Put

\[
                         B_i=(z-i)^2(z+i)^2.                  \tag{4}
\]

The exact moving-triple transport embeds the six four-spaces into one
common kernel:

\[
 B_i\mathcal S_i=\mathcal T_i\subseteq\mathcal K
                       \subseteq\mathbb C[z]_{\le9}.          \tag{5}
\]

The restored baseline (1) has mass \(30\). A seven-space in
\(\mathbb C[z]_{\le9}\) would have forced Wronskian weight

\[
                    3(7-4)+6(7-3)=33
\]

against the cap

\[
                    7(10-7)=21.
\]

Thus

\[
                            \dim\mathcal K\le6.               \tag{6}
\]

For distinct moving values \(i,j\), nonopposition makes \(B_i\) and
\(B_j\) coprime. Hence

\[
\begin{aligned}
 B_i\mathbb C[z]_{\le5}\cap B_j\mathbb C[z]_{\le5}
   &=B_iB_j\mathbb C[z]_{\le1}\\
   &=\langle B_iB_j,\ zB_iB_j\rangle .                       \tag{7}
\end{aligned}
\]

On the other hand, (5)--(6) imply

\[
             \dim(\mathcal T_i\cap\mathcal T_j)
                 \ge4+4-6=2.                                \tag{8}
\]

The ambient intersection in (7) has dimension two, so equality is forced:

\[
          \boxed{\mathcal T_i\cap\mathcal T_j
                =\langle B_iB_j,\ zB_iB_j\rangle}
                \qquad(i\ne j).                              \tag{9}
\]

In particular, every polynomial on the right of (9) belongs to
\(\mathcal K\).

## 3. Four values already span ten dimensions

Write \(t=z^2\) and \(a_i=i^2\). Then

\[
                    B_i=(t-a_i)^2.                           \tag{10}
\]

Choose any four of the six distinct squares \(a_0,a_1,a_2,a_3\). Five
off-diagonal products already span the full five-space
\(\mathbb C[t]_{\le4}\). Indeed, take the pairs

\[
                 01,\ 02,\ 03,\ 12,\ 13.                    \tag{11}
\]

In the coefficient basis \(1,t,t^2,t^3,t^4\), the determinant of the five
polynomials

\[
                   (t-a_i)^2(t-a_j)^2                       \tag{12}
\]

indexed by (11) is

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\qquad\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2,                \tag{13}
\end{aligned}
\]

which is nonzero because the squares are distinct. Therefore (9) forces

\[
        \mathbb C[z^2]_{\le4}\subseteq\mathcal K,
        \qquad z\,\mathbb C[z^2]_{\le4}\subseteq\mathcal K.  \tag{14}
\]

The two subspaces in (14) are respectively even and odd, so their sum is
direct and has dimension \(5+5=10\). This contradicts
\(\dim\mathcal K\le6\), proving Theorem 1.1.

## 4. Exact audit

[verify_live_three_zero_higher_split_p28_three_quartic_six_triple_even_odd_span_drop.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_even_odd_span_drop.py)
checks both residual selections at all six \(p=28\) splits, the mass and
Wronskian gap, the exact coprime pair-intersection dimension, the symbolic
five-by-five determinant (13), and the ten-dimensional even--odd
contradiction.

The
[independent audit](live-three-zero-higher-split-p28-three-quartic-six-triple-even-odd-span-drop-independent-audit.md)
reconstructs the two selections, the common-kernel and intersection bounds,
the determinant factorization, and the dimension-drop-only scope without
importing the primary checker.
