# Factored L0 gives a cut-determinantal obstruction at rank \(55\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome and scope

Let \(M=(M_{ru})\) be a binary packet on six residual sites \(R\), and let

\[
 D=d\Psi_M:\mathbb C^{60}\longrightarrow\mathbb C^{64}.
\]

Suppose:

1. \(\operatorname{rank}D=55\);
2. the five trace-zero vertex gauges are independent and equal \(\ker D\);
3. \(e_{0^6},e_{1^6}\in\operatorname{im}D\).

Choose arbitrary preimages

\[
 DK^{00}=e_{0^6},\qquad DK^{11}=e_{1^6},\qquad
 K^{01}=K^{10}=0.                                  \tag{1}
\]

For the four binary L0 slices to come from two **physical, shared endpoint
stars**, every residual-site cut must carry a rank-two-on-the-Segre matrix
pencil. This gives exact coupled minor tests:

* every \(5\times5\) minor vanishes;
* every \(4\times4\) minor is a scalar multiple of \(\det(A)^2\);
* every \(3\times3\) minor is divisible by \(\det(A)\).

For either mixed target-zero slice, every live \(K_{2,2}\) of invertible
residual blocks must have scalar projective holonomy. On the Zariski-open
locus where no residual four-cycle has scalar holonomy, each mixed gauge
support has one of only **17 labelled patterns**: the empty graph, one of
six \(K_{1,5}\) stars, or one of ten \(K_3\sqcup K_3\) graphs.

These are necessary conditions, not a proof of \((8,3)\). Rank \(55\) does
not imply the no-flat-cycle hypothesis, and passing the cut-minor tests is
not asserted to reconstruct globally shared endpoint factors.

## 2. Normalize the four slices modulo the gauge kernel

Add endpoint sites \(p,q\). For endpoint colours \(s,t\in\{0,1\}\), write

\[
 U_r^s(i)=A_{pr}[s,i],\qquad
 V_r^t(i)=A_{qr}[t,i],\qquad
 W_{st}=A_{pq}[s,t].                                  \tag{2}
\]

Expansion by the two endpoints gives

\[
 T_{st}=W_{st}\Psi(M)+D(N^{st}),                      \tag{3}
\]

where, for \(r\ne u\),

\[
 N^{st}_{ru}=U_r^s(V_u^t)^{\mathsf T}
             +V_r^t(U_u^s)^{\mathsf T}.              \tag{4}
\]

Euler's identity is \(D(M)=3\Psi(M)\), so the four target equations are

\[
 D\left(N^{st}+\frac{W_{st}}3M\right)
 =\begin{cases}
 e_{0^6},&(s,t)=(0,0),\\
 e_{1^6},&(s,t)=(1,1),\\
 0,&s\ne t.
 \end{cases}                                         \tag{5}
\]

By the kernel hypothesis, there are trace-zero
\(\mu^{st}\in\mathbb C^6\) such that

\[
 N^{st}_{ru}+\frac{W_{st}}3M_{ru}
 =K^{st}_{ru}+(\mu_r^{st}+\mu_u^{st})M_{ru}.          \tag{6}
\]

Set

\[
 \lambda_r^{st}=\mu_r^{st}-\frac{W_{st}}6.            \tag{7}
\]

Then

\[
 \boxed{
 N^{st}_{ru}=K^{st}_{ru}
 +(\lambda_r^{st}+\lambda_u^{st})M_{ru},\qquad
 W_{st}=-\sum_{r\in R}\lambda_r^{st}.}               \tag{8}
\]

This is independent of the preimages chosen in (1). Replacing \(K^{st}\)
by \(K^{st}+G(\eta)\), with \(\sum_r\eta_r=0\), is absorbed by
\(\lambda^{st}\mapsto\lambda^{st}-\eta\) and leaves \(W_{st}\) unchanged.

Equation (8) is the exact point at which rank \(55\) and “kernel equals
gauges” enter. If the gauges are dependent or the rank drops, additional
kernel terms must be retained.

## 3. Port flattening across a residual cut

Regard \((r,i)\), \(r\in R\), \(i\in\{0,1\}\), as a port. Fix a cut
\(R=L\sqcup S\), orient crossing blocks from \(L\) to \(S\), and form the
\(2|L|\times2|S|\) matrix

\[
 (B_{st})_{(r,i),(u,j)}
 =K^{st}_{ru}(i,j)
 +(\lambda_r^{st}+\lambda_u^{st})M_{ru}(i,j).         \tag{9}
\]

Let \(u_L^s\) collect the \(U_r^s(i)\) on \(L\), and define
\(u_S^s,v_L^t,v_S^t\) similarly. Equations (4) and (8) give

\[
 B_{st}=u_L^s(v_S^t)^{\mathsf T}
          +v_L^t(u_S^s)^{\mathsf T}.                  \tag{10}
\]

Collect columns as

\[
 U_L=[u_L^0\ u_L^1],\quad V_L=[v_L^0\ v_L^1],\qquad
 U_S=[u_S^0\ u_S^1],\quad V_S=[v_S^0\ v_S^1].         \tag{11}
\]

For an arbitrary \(A=(a_{st})\in\operatorname{Mat}_{2\times2}\), put
\(B(A)=\sum_{s,t}a_{st}B_{st}\). Then

\[
 \boxed{
 B(A)=[U_L\ V_L]
 \begin{pmatrix}0&A\\ A^{\mathsf T}&0\end{pmatrix}
 [U_S\ V_S]^{\mathsf T}.}                            \tag{12}
\]

In particular,

\[
 \operatorname{rank}B_{st}\le2,\qquad
 \operatorname{rank}[B_{s0}\ B_{s1}]\le3,\qquad
 \operatorname{rank}[B_{0t}\ B_{1t}]\le3,             \tag{13}
\]

and the concatenation of all four \(B_{st}\) has rank at most four.

## 4. The determinant hierarchy

The middle matrix in (12) has rank at most four and

\[
 \det\begin{pmatrix}0&A\\A^{\mathsf T}&0\end{pmatrix}
 =\det(A)^2.                                          \tag{14}
\]

Hence every \(5\times5\) minor of \(B(A)\) vanishes. For four-element row
and column sets \(I,J\), Cauchy--Binet has only one term:

\[
 \det B(A)_{I,J}
 =\det[U_L\ V_L]_I\,
  \det[U_S\ V_S]_J\,
  \det(A)^2.                                         \tag{15}
\]

Thus every \(4\times4\) minor is a scalar multiple of the same quartic.

If \(\det A=0\), write \(A=xy^{\mathsf T}\). Then

\[
 B(A)=u_L(x)v_S(y)^{\mathsf T}
      +v_L(y)u_S(x)^{\mathsf T},                      \tag{16}
\]

which has rank at most two. Every cubic \(3\times3\) minor vanishes on the
irreducible hypersurface \(\det A=0\), and therefore

\[
 \det B(A)_{I,J}=\det(A)\,\ell_{I,J}(A)               \tag{17}
\]

for a linear form \(\ell_{I,J}\). Equations (15)--(17), unlike the four
individual rank bounds, retain the shared-factor coupling.

## 5. Mixed slices force projectively flat four-cycles

For \(s\ne t\), \(K^{st}=0\). Write

\[
 a_{ru}=\lambda_r^{st}+\lambda_u^{st},\qquad
 N_{ru}=a_{ru}M_{ru}.                                \tag{18}
\]

Choose distinct sites \(r,r',u,u'\), viewed as the cut
\(\{r,r'\}\mid\{u,u'\}\), and orient all four blocks from the first pair
to the second. Suppose all four \(a\)'s are nonzero and all four residual
blocks are invertible. The \(4\times4\) block matrix

\[
 \begin{pmatrix}N_{ru}&N_{ru'}\\N_{r'u}&N_{r'u'}\end{pmatrix}
\]

has rank at most two, while \(N_{ru}\) is invertible. Its Schur complement
vanishes:

\[
 N_{r'u'}=N_{r'u}N_{ru}^{-1}N_{ru'}.                 \tag{19}
\]

Substitution gives

\[
 \boxed{
 a_{ru}a_{r'u'}M_{r'u'}
 =a_{r'u}a_{ru'}M_{r'u}M_{ru}^{-1}M_{ru'}.}          \tag{20}
\]

Equivalently,

\[
 M_{r'u'}^{-1}M_{r'u}M_{ru}^{-1}M_{ru'}
 =\frac{a_{ru}a_{r'u'}}{a_{r'u}a_{ru'}}I_2.          \tag{21}
\]

Thus every live mixed-slice \(K_{2,2}\) has scalar projective holonomy.
The unknown potentials affect only the scalar in (21).

Call an invertible residual packet **four-cycle generic** if (21) is
non-scalar for every four distinct sites and every \(2+2\) partition. This
is an additional Zariski-open hypothesis; rank \(55\), pure-image
incidence, and R2 do not imply it.

## 6. The 17 mixed gauge supports on the generic chart

For one mixed slice define

\[
 G_\lambda=\{ru:\lambda_r+\lambda_u\ne0\}.            \tag{22}
\]

If \(M\) is four-cycle generic, (21) makes \(G_\lambda\) \(C_4\)-free.

> **C4-free sum-graph lemma.** Over characteristic zero, a \(C_4\)-free
> nonzero-sum graph on six labelled vertices has exactly one of these forms:
>
> 1. \(\lambda=0\), giving the empty graph;
> 2. five \(\lambda_r\)'s are zero and the sixth is nonzero, giving
>    \(K_{1,5}\);
> 3. three values are \(c\) and three are \(-c\), for \(c\ne0\), giving
>    \(K_3\sqcup K_3\).

Proof: let \(Z=\{r:\lambda_r=0\}\). If \(|Z|\ge2\) and
\(|R\setminus Z|\ge2\), two vertices from each set give a \(K_{2,2}\).
Thus \(|Z|=6\), \(|Z|=5\), or \(|Z|\le1\). If \(|Z|=1\), its universal
adjacency to the five nonzero vertices forces every nonzero vertex to have
at least three opposite-valued mates; three equal nonzero mates are
mutually adjacent and give a four-cycle with the zero vertex. Hence
\(|Z|=1\) is impossible.

Now \(Z=\varnothing\). Values \(c,-c\) form an opposite-value orbit, and
every edge between distinct such orbits is live. Two orbits of size at
least two give a \(K_{2,2}\). If one orbit has size at least two and there
are two outside vertices, those two vertices and any two in the orbit also
give a \(K_{2,2}\). Hence there is at most one outside vertex. With one
outside vertex, either sign class in the large orbit has size at least
three; that live triangle together with the universally adjacent outside
vertex contains a four-cycle. If every orbit is a singleton, the live graph
is \(K_6\). Thus all vertices lie in one orbit \(\{c,-c\}\). Its two sign
classes are live cliques, so each has size at most three; both consequently
have size three.

The labelled count is

\[
 1+6+\frac12\binom63=17.                              \tag{23}
\]

Each mixed slice independently chooses one of these patterns on the
four-cycle-generic invertible chart.

## 7. Exact algorithm and relation to R2

1. Row-reduce \(D\), verify rank \(55\), verify that its kernel is the five
   gauges, and solve for \(K^{00},K^{11}\).
2. Introduce the \(24\) potentials \(\lambda_r^{st}\); then
   \(W_{st}=-\sum_r\lambda_r^{st}\).
3. For each residual cut, build (9) and enforce (15)--(17)
   coefficientwise in \(A\).
4. If all \(M_{ru}\) are invertible, precompute the flat four-cycles. If
   none exists, replace each mixed six-parameter potential by the finite
   17-pattern split before solving the pure-slice equations.

R2 uses the same endpoint variables. The residual-root-to-\(p\) binary
block is \(U_r^{\mathsf T}\). It is a pure output-column-\(s\) witness
exactly when

\[
 U_r^{1-s}=0,\qquad U_r^s\ne0,                        \tag{24}
\]

and similarly for \(V_r\) at \(q\). An R2 witness allocation therefore
becomes local zero/nonzero conditions on the factors in (12). R2
preservation and the outside-\(c\) selected-star columns remain separate
hypotheses.

## 8. Audit

The standalone checker
[verify_level_two_factored_l0_cut_determinants.py](../computations/verify_level_two_factored_l0_cut_determinants.py)
verifies:

* \(120\) direct/gauge normalization and preimage-independence identities;
* all \(36\) five-minors, \(225\) four-minors, and \(400\) three-minors of
  a formal \(6\times6\) cut pencil;
* the exact \(K_{2,2}\) anchor identity, its scalar projective holonomy, and
  a mutation destroying scalar holonomy;
* all \(203\) set partitions and \(4{,}088\) partial-negation
  configurations, yielding exactly the expected 17 labelled graphs with
  rational representatives.

The checker uses only the standard library and remains live under normal,
optimized, and isolated Python.
