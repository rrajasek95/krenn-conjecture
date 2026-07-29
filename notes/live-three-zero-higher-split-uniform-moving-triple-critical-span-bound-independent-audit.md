# Independent audit: the uniform critical moving-triple span bound

## 1. Verdict and exact scope

**PASS, conditional on the stated exact common-lift hypothesis.**  The
Wronskian estimate, the coprime pair-intersection calculation, the
five-product determinant, and the resulting four-selection contradiction
are all correct over \(\mathbb C\).

The phrase *exact moving-triple common-lift family* carries an essential
hypothesis that is only implicit in the primary note: if the restored
baseline has multiplicities \(m_1,\ldots,m_c\), then the common space
\(\mathcal K\) is annihilated at the corresponding distinct nodes by the
exact order-\(m_\nu\) rows (with locally invertible coefficients).  Thus

\[
  1\le m_\nu\le r,
  \qquad \sum_{\nu=1}^c m_\nu=(r+1)(r+2),
\]

and these rows impose the Wronskian weights used below.  If the displayed
conditions (1)--(4) of the primary note were read without this meaning, the
claim would be false: one could simply take
\(\mathcal K=\mathbb C[z]_{\le c}\).  This is a scope/self-containment
caveat, not a defect in the argument in its intended common-lift setting.

Under that interpretation the conclusions are exactly:

* for \(c\le r+4\), at most one maximal moving-triple selection;
* for \(c=r+5\), at most three maximal moving-triple selections;
* for the \(p=28\), \(4^3 3^6\) family, at least three of its six selected
  kernels have dimension at most five.

The last conclusion is a dimension drop, not a closure of either collision
profile to which that family belongs.

## 2. Independent Wronskian reconstruction

Suppose that \(\mathcal K\) contains a subspace \(V\) of dimension

\[
                              d=r+3.
\]

First take \(V\) primitive at every baseline node.  Since
\(m_\nu\le r<d\), an exact order-\(m_\nu\) row forces local Wronskian
weight at least \(d-m_\nu\).  The total forced finite weight is therefore

\[
 \sum_{\nu=1}^c(d-m_\nu)
       =dc-(r+1)(r+2).                                      \tag{1}
\]

The Wronskian of a \(d\)-space in \(\mathbb C[z]_{\le c}\) has degree at
most

\[
                              d(c+1-d).                     \tag{2}
\]

The excess of (1) over (2) is independent of \(c\):

\[
\begin{aligned}
 dc-(r+1)(r+2)-d(c+1-d)
  &=d(d-1)-(r+1)(r+2)\\
  &=(r+3)(r+2)-(r+1)(r+2)\\
  &=2(r+2)>0.                                               \tag{3}
\end{aligned}
\]

Common factors cannot remove this excess.  For example, if the gcd has
order \(t\) at a node of multiplicity \(m\), then for \(t\le m\) division
lowers the degree cap by \(dt\) and leaves an exact order-\((m-t)\) row.
Relative to the primitive contribution \(d-m\), its correction is

\[
 dt+\bigl(d-(m-t)\bigr)-(d-m)=(d+1)t\ge0.                  \tag{4}
\]

If \(t>m\), the row becomes automatic, but the cap loss contributes

\[
                       dt-(d-m)\ge0.                        \tag{5}
\]

Gcd roots away from the baseline nodes only lower the cap.  Hence (3)
excludes every \((r+3)\)-subspace and proves

\[
                            \dim\mathcal K\le r+2.           \tag{6}
\]

## 3. Pair intersections

The containment
\(\mathcal S_i\subseteq\mathbb C[z]_{\le c-4}\), together with
\(\dim\mathcal S_i=r\), already implies the feasibility condition
\(c\ge r+3\).  Let \(i\ne j\) be two maximal selections.  Their transported
spaces have dimension \(r\), so (6) gives

\[
 \dim(\mathcal T_i\cap\mathcal T_j)
   \ge 2r-(r+2)=r-2.                                      \tag{7}
\]

The hypotheses \(i\ne0\), \(j\ne0\), and \(i\ne\pm j\) imply that

\[
 B_i=(z^2-i^2)^2,
 \qquad B_j=(z^2-j^2)^2
\]

are coprime.  Consequently

\[
 B_i\mathbb C[z]_{\le c-4}\cap
 B_j\mathbb C[z]_{\le c-4}
   =B_iB_j\mathbb C[z]_{\le c-8}.                          \tag{8}
\]

Its dimension is \(\max(c-7,0)\).  If \(c\le r+4\), this is at most
\(r-3\), contradicting (7); hence two maximal selections are impossible
in the subcritical range.  At \(c=r+5\), the dimension in (8) is exactly
\(r-2\).  Thus every surviving pair satisfies

\[
 \mathcal T_i\cap\mathcal T_j
   =B_iB_j\mathbb C[z]_{\le r-3}.                           \tag{9}
\]

If \(\dim\mathcal K<r+2\), (7) would be strictly larger and would already
contradict (8).  Thus no equality branch was lost in deriving (9).

## 4. Four maximal selections give a contradiction

Choose four maximal values and write \(a_i=i^2\).  Pairwise
nonopposition makes \(a_0,a_1,a_2,a_3\) distinct.  In the coefficient
basis \((1,t,t^2,t^3,t^4)\), the five rows corresponding to the pairs

\[
                         01,\ 02,\ 03,\ 12,\ 13
\]

and the polynomials \((t-a_i)^2(t-a_j)^2\) have determinant

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\quad\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2.                \tag{10}
\end{aligned}
\]

Every factor is nonzero, so these products form a basis of the
five-dimensional space \(\mathbb C[t]_{\le4}\).  Equation (9), applied to
these five pairs, then puts the multiplication span

\[
       \mathbb C[z^2]_{\text{degree in }z^2\le4}
       \cdot\mathbb C[z]_{\le r-3}
       \quad\text{inside }\mathcal K.                      \tag{11}
\]

The exponents occurring in (11) are covered by

\[
 [0,r-3],\ [2,r-1],\ [4,r+1],\ [6,r+3],\ [8,r+5].         \tag{12}
\]

For \(r=4\) these intervals meet end-to-end, and for \(r>4\) consecutive
intervals overlap.  They therefore cover every exponent from zero through
\(r+5\).  Hence (11) is the full \(\mathbb C[z]_{\le r+5}\), of dimension
\(r+6\), contradicting (6).  Four maximal selections cannot coexist.

## 5. The \(p=28\) specialization and limitations

For \(r=4\), the threshold is \(p=4(4+3)=28\), and the restored baseline
\(4^3 3^6\) has mass thirty and nine classes:

\[
             30=(r+1)(r+2),\qquad 9=r+5.
\]

There are six legal moving-triple values.  The separate six-kernel
frontier bounds every selected kernel by six dimensions.  Since at most
three can attain six, at least three have dimension at most five.

This audit does not derive the common-lift transport from an arbitrary
collision profile, does not say anything for \(c\ge r+6\), and does not
convert a lower-dimensional selected kernel into a contradiction.  The
characteristic-zero field and the distinct-square condition are also
used essentially in (10).

The independent checker
[verify_live_three_zero_higher_split_uniform_moving_triple_critical_span_bound_independent_audit.py](../computations/verify_live_three_zero_higher_split_uniform_moving_triple_critical_span_bound_independent_audit.py)
does not import the primary checker.  It verifies the Wronskian and gcd
arithmetic, the whole feasible subcritical range, the symbolic determinant,
the interval cover, direct exact ranks of the product multiplication span,
and the \(p=28\) count.
