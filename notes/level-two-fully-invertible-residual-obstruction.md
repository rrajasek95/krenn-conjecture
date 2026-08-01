# A rank-\(55\) level-two residual cannot be fully block-invertible

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Fix a level-two block with rare colour \(c\) at \(p,q\), complementary
colours \(a,b\), residual set \(R\), and binary residual blocks

\[
                         M_{rx}=A_{rx}[\{a,b\},\{a,b\}].
\]

> **Fully invertible residual theorem.** In a solution of the full
> eight-vertex equations, it is impossible to have simultaneously
> \[
>       \operatorname{rank}d\Psi_M=55
>       \quad\hbox{and}\quad
>       \det M_{rx}\ne0\ \hbox{for all }r<x\hbox{ in }R.              \tag{1}
> \]

Equivalently, every rank-\(55\) level-two block in a hypothetical solution
must contain a singular internal \(2\times2\) block. This closes the
Zariski-generic fully invertible part of the genuinely two-sided residual
locus, not merely a selected endpoint-star rank pattern.

The proof combines the universal pair-pencil rule R2 with the
[zero-star four-\(c\) theorem](level-two-zero-star-four-c-obstruction.md).

## 2. R2 forces both endpoint stars to vanish

As before, put

\[
 P_r=(A_{pr}[c,a],A_{pr}[c,b]),\qquad
 Q_r=(A_{qr}[c,a],A_{qr}[c,b]),\qquad
 X_r=[P_r\ Q_r].                                      \tag{2}
\]

Apply R2 at a residual root \(r\) to the pair \(a,b\). Its two alternatives
are:

1. every incident two-row block is supported in the output columns \(a,b\);
   or
2. two distinct incident edges are pure-column witnesses, one for \(a\) and
   one for \(b\).

Suppose \(X_r\ne0\). At least one of the endpoint edges \(rp,rq\) has a
nonzero entry in its outside output column \(c\), so preservation fails.
Every internal edge \(rx\), \(x\in R\setminus\{r\}\), has invertible
\(M_{rx}\), and hence cannot be supported in only one output column. Thus no
internal edge is a pure-column witness.

Among the two endpoint edges, every edge whose selected star \(P_r\) or
\(Q_r\) is nonzero is also disqualified by its nonzero \(c\)-column. Since
\(X_r\ne0\), at most one endpoint edge remains even eligible. It cannot
supply the two distinct witnesses required by R2. This contradiction proves

\[
                              X_r=0.                  \tag{3}
\]

The argument holds at every residual root, so \(P=Q=0\).

## 3. Rank \(55\) finishes the contradiction

All fifteen residual blocks are invertible, so every deletion live graph is
\(K_5\), in particular connected and nonbipartite. The kernel-budget lemma in
the zero-star note applies. At rank \(55\):

* the six-site slope \(\Psi(M)\) is nonzero; and
* every four-site binary cofactor is nonzero.

With \(P=Q=0\), the selected level-two equation reduces to

\[
                              z\Psi(M)=0,             \tag{4}
\]

where \(z=A_{pq}[c,c]\). Hence \(z=0\). The zero-star four-\(c\) theorem now
applies and contradicts the pure-\(c\) target coefficient. This proves (1).

The proof uses invertibility only to remove every internal pure-column
witness at every root. A future refinement may replace it by the exact
rootwise count of available pure witnesses, but (1) already removes the
dense open residual stratum without a rank-pattern census for the \(X_r\).

## 4. The forbidden locus is nonempty and generic

The checker supplies a deterministic integral packet whose fifteen blocks
are

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&\begin{pmatrix}7&13\\7&1\end{pmatrix}&
02&\begin{pmatrix}5&9\\8&7\end{pmatrix}&
03&\begin{pmatrix}13&5\\8&6\end{pmatrix}\\
04&\begin{pmatrix}10&4\\9&3\end{pmatrix}&
05&\begin{pmatrix}5&3\\13&2\end{pmatrix}&
12&\begin{pmatrix}10&13\\5&9\end{pmatrix}\\
13&\begin{pmatrix}12&13\\10&3\end{pmatrix}&
14&\begin{pmatrix}5&2\\12&2\end{pmatrix}&
15&\begin{pmatrix}11&6\\8&9\end{pmatrix}\\
23&\begin{pmatrix}2&6\\7&6\end{pmatrix}&
24&\begin{pmatrix}10&11\\4&9\end{pmatrix}&
25&\begin{pmatrix}8&8\\9&5\end{pmatrix}\\
34&\begin{pmatrix}1&13\\9&1\end{pmatrix}&
35&\begin{pmatrix}2&12\\7&12\end{pmatrix}&
45&\begin{pmatrix}13&11\\11&1\end{pmatrix}.
\end{array}
\]

Every determinant is nonzero, with minimum absolute value \(6\). The exact
\(64\times60\) differential has rank \(55\): five independent integral
gauge kernels give the upper bound, and a \(55\)-minor is nonzero modulo
\(101\). All 64 slope coordinates and all \(15\cdot16=240\) four-site
cofactor coordinates are nonzero. Thus the conditions in (1) define a
nonempty dense open subset of residual packet space; the theorem is not
excluding an empty formal case.

## 5. Audit

[verify_level_two_fully_invertible_residual_obstruction.py](../computations/verify_level_two_fully_invertible_residual_obstruction.py)
checks all fifteen determinants, absence of internal pure-column witnesses,
the three possible nonzero endpoint-star support types in the R2 count,
the exact differential rank, all six five-site cofactor ranks, the full slope
support, and all four-site cofactor coordinates. It composes the neighbouring
exact differential audit by an explicit file path and remains live under
normal, optimized, and isolated Python with no non-standard dependency.

## 6. Revised frontier

For every selected level-two block of a hypothetical solution, at least one
of the following must now hold:

1. \(\operatorname{rank}d\Psi_M\le54\); or
2. some internal binary block \(M_{rx}\) is singular.

The earlier pair-pencil theorem already closes two large singular patterns,
and the one-sided theorem closes the generic one-sided locus. The next
rank-\(55\) target should therefore use R2 to organize the unavoidable
singular blocks rootwise, retaining rank-one endpoint stars rather than
enumerating all \(X_r\) normal forms.
