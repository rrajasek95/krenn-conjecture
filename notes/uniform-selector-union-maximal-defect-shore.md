# Uniform selector-union failure has a maximal exact shore

## 1. Outcome

Let \(W\) be the complete residual site set, with \(|W|=2h\ge6\), and let
\(M_P,M_S\) be the rank-three Rado matroids of the two endpoint stars:

\[
 L_x^P=\operatorname{im}(P_x^*:V_x^*\to C^*),\qquad
 L_x^S=\operatorname{im}(S_x^*:V_x^*\to D^*).
\tag{1}
\]

This note gives the uniform version of the six-site deficient-circuit
reduction.  It does not select six sites or replace the actual consecutive
powers by a smaller source.

The matroid argument, its conversion to aggregate linear ranks, and the
rootless support bounds were checked in
[the independent audit](uniform-selector-union-maximal-defect-shore-independent-audit.md).

**Theorem 1.1 (maximal deficient-shore reduction).**  If \(M_P,M_S\)
have no pair of disjoint bases, there is a set \(B\subset W\), with
\(1\le b=|B|\le5\), such that for \(A=W\setminus B\),

\[
 b+\rho_P(A)+\rho_S(A)=5,
\qquad
 \rho_T(A\setminus\{x\})=\rho_T(A)
 \quad(x\in A,\ T=P,S).
\tag{2}
\]

Every minimizing Rado witness for \(\rho_T(A)\) is all of \(A\).
Consequently

\[
 \rho_T(A)=\dim\sum_{x\in A}L_x^T
\tag{3}
\]

and every \(x\in A\) satisfies

\[
 \operatorname{rank}(P_x^*\oplus S_x^*)\le5-b.
\tag{4}
\]

The possible shores are therefore:

\[
\begin{array}{c|c|c}
b&(\rho_P(A),\rho_S(A))&\text{structure}\\ \hline
1&(2,2)&\text{common aggregate-rank-two coloop}\\
2&(1,2),(2,1)&\text{line-plus-plane shore}\\
3&(0,2),(1,1),(2,0)&\text{endpoint-dark on every site of }A\\
4&(0,1),(1,0)&\text{endpoint-dark on every site of }A\\
5&(0,0)&\text{endpoint-dark on every site of }A.
\end{array}
\tag{5}
\]

For \(b=1\), the unique site of \(B\) is the actual common coloop of the
complete \(2h\)-site packet.  In the surrounding literal full-nine
response system, the uniform
[common-coloop residual theorem](common-coloop-full-nine-residual-coupling.md)
applies directly.  For \(b=2\), the complement consists of the two sites
which must carry the transverse quotient of the rank-one endpoint;
Section 5 gives the exact shore/probe/local-isomorphism trichotomy.  For
\(b\ge3\), (4) supplies a common endpoint-dark physical covector at every
site of the full shore \(A\).

Thus the incidence problem is uniform before any coefficient is cut.  The
remaining work is source-level: couple the line-plus-plane quotient or the
endpoint-dark probes to the literal full-nine rows and their actual common
power.

## 2. Matroid union on the complete ground set

The matroid-union rank formula gives

\[
 \operatorname{rank}(M_P\vee M_S)(W)
 =\min_{A\subseteq W}
   \left(|W\setminus A|+\rho_P(A)+\rho_S(A)\right).
\tag{6}
\]

There are disjoint endpoint bases exactly when this rank is six.  Indeed,
an independent union set of size six decomposes into independent sets of
the two rank-three matroids; both parts must have size three and hence be
bases.

If disjoint bases do not exist, some \(B\subseteq W\), with
\(A=W\setminus B\), satisfies

\[
 F(B):=|B|+\rho_P(A)+\rho_S(A)\le5.
\tag{7}
\]

Choose \(B\) inclusion-maximal among all such witnesses.  Since
\(F(B)\ge|B|\), one has \(b\le5\).  Also \(b\ne0\), because

\[
 F(\varnothing)=\rho_P(W)+\rho_S(W)=6.
\tag{8}
\]

For \(x\in A\), maximality says \(B\cup\{x\}\) is not a witness.  Put

\[
 \epsilon_T(x)=\rho_T(A)-\rho_T(A\setminus\{x\})
 \in\{0,1\}.
\]

Then

\[
\begin{aligned}
 6
 &\le F(B\cup\{x\})\\
 &=F(B)+1-\epsilon_P(x)-\epsilon_S(x)\\
 &\le6.
\end{aligned}
\tag{9}
\]

Every inequality is an equality.  Hence \(F(B)=5\) and
\(\epsilon_P(x)=\epsilon_S(x)=0\) for every \(x\in A\), proving (2).

## 3. The Rado witness is the whole shore

For either endpoint, the Rado formula is

\[
 \rho_T(A)=\min_{J\subseteq A}
 \left(|A\setminus J|+
       \dim\sum_{y\in J}L_y^T\right).
\tag{10}
\]

Let \(J_T\) be any minimizing witness.  If
\(x\in A\setminus J_T\), the same \(J_T\) used in
\(A\setminus\{x\}\) gives

\[
\begin{aligned}
 \rho_T(A\setminus\{x\})
 &\le |(A\setminus\{x\})\setminus J_T|
      +\dim\sum_{y\in J_T}L_y^T\\
 &=\rho_T(A)-1,
\end{aligned}
\tag{11}
\]

contradicting (2).  Therefore \(J_T=A\), which proves (3).

Each local row image lies in its aggregate shore span.  Since the two
endpoint targets are direct summands,

\[
\begin{aligned}
 \operatorname{rank}(P_x^*\oplus S_x^*)
 &\le\dim\sum_{y\in A}L_y^P+
      \dim\sum_{y\in A}L_y^S\\
 &=\rho_P(A)+\rho_S(A)=5-b.
\end{aligned}
\tag{12}
\]

This proves (4).

## 4. Exact classification by complement size

Adding the \(b\) sites of \(B\) can increase either matroid rank by at
most \(b\).  Since both full ranks are three,

\[
 \rho_T(A)\ge3-b.
\tag{13}
\]

Combine (13), nonnegativity, and
\(\rho_P(A)+\rho_S(A)=5-b\).  For \(b=1\) this forces \((2,2)\); for
\(b=2\), it forces \((1,2)\) or \((2,1)\); and for \(b=3,4,5\) it gives
the remaining rows of (5).

When \(b\ge3\), equation (12) has rank at most two on the
three-dimensional domain \(V_x^*\), at every \(x\in A\).  Hence every
shore site has a nonzero covector killing both endpoint stars.

When \(b=1\), (3) says that both complete endpoint maps restricted away
from the sole site \(x_0\in B\) have linear rank two.  Their full Rado
rank three implies that the global endpoint maps are injective.  This is
exactly the uniform common-coloop input, with no selected-site inference.
This proves Theorem 1.1.  \(\square\)

## 5. The exact line-plus-plane quotient trichotomy

Assume \(b=2\) and, after exchanging endpoints,

\[
 \dim U_P=1,\qquad \dim U_S=2,\qquad
 U_T=\sum_{x\in A}L_x^T,\qquad B=\{u,v\}.
\tag{14}
\]

Put

\[
 H=U_P\oplus U_S\subset C^*\oplus D^*,\qquad
 {\cal Q}=(C^*\oplus D^*)/H.
\tag{15}
\]

Both \(H\) and \({\cal Q}\) have dimension three.  For \(y\in B\), let

\[
 \overline\Theta_y:V_y^*\longrightarrow{\cal Q}
\tag{16}
\]

be the quotient of \(P_y^*\oplus S_y^*\).  Exactly one of the following
ranges occurs.

1. For some distinct \(x,y\in\{u,v\}\), an endpoint aggregate map off
   \(y\) has rank at most two:

   \[
     \dim(U_P+L_x^P)\le2
     \quad\text{or}\quad
     \dim(U_S+L_x^S)\le2.
   \tag{17}
   \]

2. No shore in (17) is deficient, but
   \(\overline\Theta_u\) or \(\overline\Theta_v\) has rank two.  Its
   nonzero kernel is a core-valued probe \(\lambda_y\) satisfying

   \[
     P_y^*(\lambda_y)\in U_P,\qquad
     S_y^*(\lambda_y)\in U_S.
   \tag{18}
   \]

3. Both quotient maps have rank three and are linear isomorphisms
   \(V_y^*\simeq{\cal Q}\).

Indeed, if (17) fails, then each \(P\)-projection onto
\(C^*/U_P\) is onto its two-dimensional target, and each \(S\)-projection
onto \(D^*/U_S\) is nonzero.  Hence

\[
 2\le\operatorname{rank}\overline\Theta_y\le3.
\tag{19}
\]

Rank two gives (18), while rank three gives the final alternative.
These are local quotient isomorphisms only.  They do not supply clean
curved charts, a physical curvature minor, fixed-label transport, or
clean-error/Omega data.

## 6. Immediate rootless support consequence

Let \(R_*=P^{\mathsf T}K_*S\) be the scalar-zero response quadratic in
the rootless packet, for which the audited response theorem gives

\[
 R_*^{[h]}\ne0.
\tag{20}
\]

The \(b=5\) row of (5) has both endpoint stars supported entirely on the
five-site set \(B\).  Therefore \(R_*\) is supported on at most five
sites, so \(R_*^{[h]}=0\) for \(2h\ge6\), contradicting (20).  Thus the
last row is absent in the rootless branch.

More generally, if one endpoint rank in (5) is zero, every response edge
uses at least one site of \(B\).  A term of \(R_*^{[h]}\) would then need
\(h\) distinct sites of \(B\).  Hence such a row is impossible whenever
\(h>b\).  This is a support bound, not a termwise inference from a
cancelling sum: no supported perfect-matching monomial exists.

For \(h\ge5\), the rootless selector obstruction is consequently
concentrated in the uniform common-coloop, the two-site-complement
line-plus-plane shore, and the \(b=3\), \((1,1)\) endpoint-dark shore.
At \(h=4\), the \(b=4\) zero-rank row can remain; at \(h=3\), the
\(b=3,4\) zero-rank rows can remain.  These low-order rows stay inside
the endpoint-dark coefficient ledger rather than creating a new incidence
family.
