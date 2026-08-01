# A rank-55 three-invertible branch survives the generic-kernel equation and R2

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Exact scope and outcome

Fix a level-two block with rare colour \(c\) at endpoints \(p,q\), binary
residual colours \(a,b\), and residual vertices \(R=\{0,\ldots,5\}\). As in
the other level-two notes, put

\[
 P_r=(A_{pr}[c,a],A_{pr}[c,b])^{\mathsf T},\qquad
 Q_r=(A_{qr}[c,a],A_{qr}[c,b])^{\mathsf T},\qquad
 X_r=[P_r\ Q_r].
\]

There is an exact integral residual packet \(M\), endpoint-star data \(X\),
and gauge parameters \(\nu\) such that

1. the ranks of \(X_0,\ldots,X_5\) are \(2,2,2,1,0,0\);
2. the rank-\(55\) generic-kernel equation
   \[
   X_rJX_s^{\mathsf T}=(\nu_r+\nu_s)M_{rs},\qquad
   z=-\sum_r\nu_r
   \tag{1}
   \]
   holds on every residual edge;
3. all \(64\) selected level-two rows hold exactly;
4. \(\operatorname{rank}d\Psi_M=55\) over \(\mathbb Q\); and
5. two distinct literal R2 pure-column witnesses, one for \(a\) and one for
   \(b\), exist at every residual root.

Thus the generic-kernel equation plus R2 does **not** give a
classification-free contradiction for the whole
three-invertible/three-singular endpoint-star pattern. This is a local
selected-block/R2 guard, not a solution of the full eight-vertex equation
system.

## 2. Why zero stars are an escape hatch

Suppose \(X_i\) is invertible. Both endpoint edges \(ip,iq\) have nonzero
outside-\(\{a,b\}\) columns, so neither can be an R2 pure-\(a\) or pure-\(b\)
witness. Hence both witnesses at \(i\) must be internal and must meet
singular-star vertices.

If \(X_s=u_sv_s^{\mathsf T}\ne0\) has rank one, then the edge \(is\) cannot
have \(\nu_i+\nu_s=0\): equation (1) would give
\(X_iJX_s^{\mathsf T}=0\), contrary to invertibility of \(X_i\). Therefore

\[
 M_{is}=\frac{X_iJv_s}{\nu_i+\nu_s}u_s^{\mathsf T}.       \tag{2}
\]

This edge is a pure-column witness precisely when the left factor \(u_s\)
is a coordinate vector. Its witness colour is then fixed at every invertible
root.

For a zero star \(X_s=0\), by contrast, an edge with
\(\nu_i+\nu_s=0\) makes both sides of (1) zero and leaves all four entries of
\(M_{is}\) free. R2 can make one such edge a required pure-column witness
while leaving another zero-star edge generic. The witness below exploits
exactly this freedom.

## 3. The exact packet

Take \(J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\) and

\[
\begin{aligned}
X_0&=\begin{pmatrix}7&13\\7&1\end{pmatrix},&
X_1&=\begin{pmatrix}5&9\\8&7\end{pmatrix},&
X_2&=\begin{pmatrix}13&5\\8&6\end{pmatrix},\\
X_3&=\begin{pmatrix}1&1\\0&0\end{pmatrix},&
X_4&=0,&X_5&=0.
\end{aligned}                                                   \tag{3}
\]

Set

\[
 (\nu_0,\ldots,\nu_5)=\tfrac12(1,1,1,1,-1,-1),\qquad z=-1.       \tag{4}
\]

The fifteen residual blocks are

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&\begin{pmatrix}128&153\\68&57\end{pmatrix}&
02&\begin{pmatrix}204&146\\48&50\end{pmatrix}&
03&\begin{pmatrix}20&0\\8&0\end{pmatrix}\\[4pt]
04&\begin{pmatrix}0&10\\0&4\end{pmatrix}&
05&\begin{pmatrix}9&3\\5&3\end{pmatrix}&
12&\begin{pmatrix}142&102\\131&104\end{pmatrix}\\[4pt]
13&\begin{pmatrix}14&0\\15&0\end{pmatrix}&
14&\begin{pmatrix}0&13\\0&2\end{pmatrix}&
15&\begin{pmatrix}10&13\\5&9\end{pmatrix}\\[4pt]
23&\begin{pmatrix}18&0\\14&0\end{pmatrix}&
24&\begin{pmatrix}0&12\\0&13\end{pmatrix}&
25&\begin{pmatrix}10&3\\5&2\end{pmatrix}\\[4pt]
34&\begin{pmatrix}12&0\\2&0\end{pmatrix}&
35&\begin{pmatrix}0&11\\0&6\end{pmatrix}&
45&\begin{pmatrix}0&0\\0&0\end{pmatrix}.
\end{array}                                                     \tag{5}
\]

For \(0\le r<s\le3\), the displayed block is exactly
\(X_rJX_s^{\mathsf T}\), while \(\nu_r+\nu_s=1\). Every edge from
\(\{0,1,2,3\}\) to \(\{4,5\}\) has zero multiplier and zero numerator in
(1), so its displayed block is unconstrained by (1). Finally
\(\nu_4+\nu_5=-1\) and \(M_{45}=0\). This proves (1) edge by edge. Euler's
identity then gives the selected equation

\[
 z\Psi(M)+d\Psi_M\bigl((X_rJX_s^{\mathsf T})_{rs}\bigr)=0.       \tag{6}
\]

The exact differential rank is \(55\). The six-site slope has \(56\) nonzero
coordinates out of \(64\); full slope support is not being assumed.

## 4. Literal R2 witnesses

The two witness edges at each residual root can be chosen as follows:

| root | pure-\(a\) edge | pure-\(b\) edge |
|---:|:---:|:---:|
| \(0\) | \(03\) | \(04\) |
| \(1\) | \(13\) | \(14\) |
| \(2\) | \(23\) | \(24\) |
| \(3\) | \(34\) | \(35\) |
| \(4\) | \(4p\) | \(4q\) |
| \(5\) | \(5p\) | \(5q\) |

The first eight claims are literal in (5), with the block transposed when
viewed from its second endpoint. At roots \(4,5\), both selected outside-
\(c\) endpoint columns vanish because \(X_4=X_5=0\). The otherwise unused
binary entries on \(rp,rq\) may therefore be completed by a nonzero two-row
block supported only in column \(a\) on \(rp\), and one supported only in
column \(b\) on \(rq\). These are compatible with the selected endpoint-star
data and are two distinct R2 witnesses.

This endpoint completion asserts only the stated local R2 rows. No global
ternary array satisfying all overlapping level-two blocks or all \(3^8\)
value equations is claimed.

## 5. Consequence for the proof route

Any theorem excluding all three-invertible rank-\(55\) blocks must use more
than (1) and the residual R2 exits. In the guard, the zero-multiplier cut

\[
 \{0,1,2,3\}\mid\{4,5\}                                      \tag{7}
\]

contains eight blocks invisible to the generic-kernel equation. R2 fixes
only enough of them to supply the required columns; the remaining entries
restore differential rank \(55\).

The precise next inputs available to attack this survivor are overlapping
level-two blocks, L0/L1 value rows, or R2 applied to additional colour pairs
in a genuine global completion. Subfamilies with fewer zero-star freedoms
may still admit rank-drop theorems; this guard makes no claim about them.

## 6. Machine audit

[verify_level_two_three_invertible_r2_guard.py](../computations/verify_level_two_three_invertible_r2_guard.py)
checks independently and exactly:

* endpoint-star ranks \(2,2,2,1,0,0\);
* all \(60\) scalar instances of (1) and \(z=-\sum\nu\);
* all \(64\) selected level-two rows;
* differential rank \(55\) over \(\mathbb Q\), modulo \(101\), and modulo
  \(1{,}000{,}003\);
* five independent universal gauge-kernel directions; and
* the literal pure-column witness table above, including the outside-\(c\)
  endpoint-column compatibility at roots \(4,5\).

It is standard-library-only and passes normal, optimized, and isolated
Python.
