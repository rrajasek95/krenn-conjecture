# Independent audit: the rank-sharp L0 packet fails endpoint factorization

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

The rank-\(55\), mixed-rank-\(53\) packet \(M^\sharp\) in
[the three-invertible L0 note](level-two-three-invertible-l0-obstruction.md)
passes the universal linear tangent-incidence screen, but it does **not**
admit binary endpoint blocks. More precisely, there are no arbitrary

\[
 U^0,U^1,V^0,V^1\in(\mathbb C^2)^6,\qquad
 W_{00},W_{01},W_{10},W_{11}\in\mathbb C
\]

whose four eight-site binary slices are

\[
 T_{00}=e_{0^6},\qquad T_{11}=e_{1^6},\qquad
 T_{01}=T_{10}=0.
\]

The \(00\), \(11\), and \(01\) slices already contradict one another; the
\(10\) slice is unused. This is an exact obstruction to this particular
sharpness packet, not a theorem excluding every packet on the
\(55/53\) incidence locus.

## 2. Exact quotient by the differential kernel

Put \(D=d\Psi_{M^\sharp}\). Independent exact elimination gives

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mix}=53
\]

over \(\mathbb Q\), modulo \(101\), and modulo \(1{,}000{,}003\).
The five trace-zero vertex gauges are independent and lie in \(\ker D\);
therefore they are the entire kernel. The cells \((01,00)\) and \((45,11)\)
are literal tangent preimages of \(e_{0^6}\) and \(e_{1^6}\), respectively.

For endpoint colours \(s,t\), let

\[
 N^{st}_{ru}(i,j)
 =U^s_r(i)V^t_u(j)+V^t_r(i)U^s_u(j).
\]

The L0 slice equation is

\[
 D(N^{st})+W_{st}\Psi(M^\sharp)=
 \begin{cases}
 e_{0^6},&(s,t)=(0,0),\\
 e_{1^6},&(s,t)=(1,1),\\
 0,&s\ne t.
 \end{cases}
\]

Euler's identity \(D(M^\sharp)=3\Psi(M^\sharp)\), followed by the exact
kernel description, absorbs \(W_{st}\) into six unrestricted scalars
\(\lambda^{st}_r\). Thus every endpoint completion would satisfy, block by
block,

\[
 N^{st}_{ru}(i,j)
 =E^{st}_{ru}(i,j)
  +(\lambda^{st}_r+\lambda^{st}_u)M^\sharp_{ru}(i,j),       \tag{1}
\]

where \(E^{00}\) is the single cell \((01,00)\), \(E^{11}\) is the single
cell \((45,11)\), and \(E^{01}=0\). Conversely, the absorption loses no
information: one recovers \(W_{st}=-\sum_r\lambda^{st}_r\).

## 3. A local rational Nullstellensatz certificate

Only the residual \(K_4\) on vertices \(\{0,1,4,5\}\) is needed. Its blocks
are

\[
\begin{array}{c|c@{\quad}c|c}
01&\begin{pmatrix}2&3\\4&6\end{pmatrix}&
45&\begin{pmatrix}1&0\\0&0\end{pmatrix}\\[4pt]
04&\begin{pmatrix}5&6\\11&8\end{pmatrix}&
05&\begin{pmatrix}6&7\\13&9\end{pmatrix}\\[4pt]
14&\begin{pmatrix}6&8\\12&11\end{pmatrix}&
15&\begin{pmatrix}7&9\\14&12\end{pmatrix}.
\end{array}
\]

Write the \(72\) scalar instances of (1) in lexicographic order

\[
 (s,t)\in(00,11,01),\quad
 ru\in(01,04,05,14,15,45),\quad
 (i,j)\in(00,01,10,11),
\]

and call them \(f_1,\ldots,f_{72}\). The independent checker contains
explicit rational sparse polynomials \(c_k\), supported on only \(38\)
indices, for which

\[
                         \sum_{k=1}^{72}c_kf_k=1.           \tag{2}
\]

The four multipliers on the \(00\)-slice edge \(01\) begin

\[
 (c_1,c_2,c_3,c_4)=
 \left(-1,\frac8{11},\frac12,-\frac4{11}\right).
\]

The complete certificate has \(124\) multiplier monomials, coefficient
degree at most two, and at most eight terms in any one multiplier. A
standard-library sparse-polynomial implementation reconstructs all selected
equation labels and orientations and expands (2) over \(\mathbb Q\) to the
single constant \(1\). Hence the common zero set of the three slice systems
is empty over \(\mathbb C\).

## 4. Machine audit and frontier

[audit_level_two_l0_sharp_factor_obstruction_independent.py](../computations/audit_level_two_l0_sharp_factor_obstruction_independent.py)
independently checks:

* the exact \(55/53\) differential ranks over three fields;
* the two literal pure tangent columns and the five-dimensional gauge
  kernel;
* the reduction from arbitrary direct cells \(W_{st}\) to (1);
* the precise \(38\) selected equations among the \(72\) local equations;
* the \(38/124/2/8\) certificate statistics; and
* the expanded identity (2) in exact rational arithmetic.

It imports no project module and passes normal, optimized, and isolated
Python. The linear incidence condition remains sharp, but \(M^\sharp\) is
not a factored L0 completion. The next sharpness question is whether some
other point of the rank-\(55\), mixed-rank-\(53\) locus satisfies the
factored two-star equations, or whether factorization imposes a stronger
universal rank drop.
