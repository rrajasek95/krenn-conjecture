# Higher splits: the critical moving-triple local-jet \(q=6\) cap

## 1. Result and scope

Continue from the
[uniform critical moving-triple span bound](live-three-zero-higher-split-uniform-moving-triple-critical-span-bound.md).
Let \(r\geq4\), put

\[
                             p=r(r+3),
\]

and consider an exact moving-triple common-lift family whose restored
baseline has mass \((r+1)(r+2)\) on \(c=r+5\) value classes.  For a
moving triple \(i\) with maximal selected-row-kernel dimension \(r+2\),
write

\[
\begin{aligned}
 {\cal S}_i&\subseteq\mathbb C[z]_{\leq r+1},
       &\dim{\cal S}_i&=r,\\
 B_i&=(z-i)^2(z+i)^2,
       &{\cal T}_i=B_i{\cal S}_i&\subseteq{\cal K}
                                   \subseteq\mathbb C[z]_{\leq r+5}.
\end{aligned}                                                \tag{1}
\]

The moving values are nonzero, distinct, and pairwise nonopposite.  The
complement belonging to the selection of \(i\) still contains every
other moving value \(j\) with exact multiplicity three.  Consequently
there is a local unit \(U_{i,j}\), with \(U_{i,j}(j)\ne0\), such that

\[
                   (U_{i,j}S)^{(3)}(j)=0
                         \qquad(S\in{\cal S}_i).              \tag{2}
\]

**Theorem 1.1 (critical local-jet cap).**  At most one moving-triple
selection can have maximal selected-row-kernel dimension \(r+2\).

For \(r=4\), the restored profile is \(4^3 3^6\).  Thus at least five of
its six moving-triple selections have kernel dimension at most five.
The low-role selected-lift incidence theorem excludes dimension four,
so on the surviving formal-selection branch these five dimensions are
exactly five.

This is a dimension-distribution theorem, not a closure of either
\((e,a,b,u)=(3,6,0,0)\) or \((3,6,1,-2)\).  The five \(q=5\) relation
three-spaces still require a joint compatibility contradiction.

## 2. The critical pair intersection is full

Suppose distinct moving values \(i,j\) both have maximal kernel
dimension.  The exact-row Wronskian argument in the uniform theorem gives

\[
                              \dim{\cal K}\leq r+2.            \tag{3}
\]

The two transported \(r\)-spaces therefore satisfy

\[
 \dim({\cal T}_i\cap{\cal T}_j)
       \geq 2r-(r+2)=r-2.                                    \tag{4}
\]

Since \(B_i\) and \(B_j\) are coprime and \(c=r+5\),

\[
\begin{aligned}
 B_i\mathbb C[z]_{\leq r+1}\cap
 B_j\mathbb C[z]_{\leq r+1}
   &=B_iB_j\mathbb C[z]_{\leq r-3},\\
 \dim B_iB_j\mathbb C[z]_{\leq r-3}
   &=r-2.                                                    \tag{5}
\end{aligned}
\]

The lower bound in (4) fills the whole ambient intersection:

\[
             {\cal T}_i\cap{\cal T}_j
                  =B_iB_j\mathbb C[z]_{\leq r-3}.             \tag{6}
\]

Dividing the containment in \({\cal T}_i=B_i{\cal S}_i\) by the
nonzero polynomial \(B_i\) yields

\[
                   B_j\mathbb C[z]_{\leq r-3}
                              \subseteq{\cal S}_i.             \tag{7}
\]

Because \(r\geq4\), the multiplier \(z-j\) belongs to
\(\mathbb C[z]_{\leq r-3}\).

## 3. The complementary triple jet gives the contradiction

Take

\[
                         S_*(z)=B_j(z)(z-j)
                                =(z-j)^3(z+j)^2.              \tag{8}
\]

Equation (7) puts \(S_*\) in \({\cal S}_i\).  It has exact order three
at the nonzero point \(j\).  Multiplication by the local unit in (2)
does not change that order, and its third derivative is

\[
       (U_{i,j}S_*)^{(3)}(j)
            =3!\,U_{i,j}(j)(2j)^2
            =24j^2U_{i,j}(j)\ne0.                            \tag{9}
\]

This contradicts the exact complementary triple row (2).  Hence two
maximal selections cannot coexist, proving Theorem 1.1.

The argument uses the relation-space jet, not merely the dimensions of
the transported spaces.  This is why it improves the earlier
four-active-value span contradiction precisely at the critical class
count.

## 4. Exact audit

[verify_live_three_zero_higher_split_critical_moving_triple_local_jet_q6_cap.py](../computations/verify_live_three_zero_higher_split_critical_moving_triple_local_jet_q6_cap.py)
checks the threshold degrees and dimensions for a range of \(r\), the
critical full-intersection identity, the literal order-three derivative
in (9), both \(p=28\) residual tuples at all six splits, and the
dimension-drop-only scope.
