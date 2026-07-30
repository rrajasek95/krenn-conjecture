# Independent audit: uniform selector-union maximal deficient shore

## 1. Verdict

**PASS after three scope clarifications.**  The matroid-union criterion,
maximal-witness argument, deletion equalities, Rado-witness rigidity,
aggregate row-span conversion, classification by \(b\), common-coloop
identification, and rootless support bounds in
[the source note](uniform-selector-union-maximal-defect-shore.md) are
correct.  None of these arguments selects six sites or cancels a common
matching power.

The source note now keeps the following qualifications explicit.

1. Theorem 1.1 is a purely matroidal statement.  Its common-coloop
   application additionally uses the surrounding literal full-nine
   equations.  Its rootless application additionally uses the audited
   rootless conclusion \(R_*^{[h]}\ne0\).
2. In the \(b=2\) branch, a rank-three local map after quotienting by the
   aggregate shore is an isomorphism of local linear spaces.  It is not a
   clean curved chart: target-zero representatives, fixed-label transport,
   a physical curvature minor, and clean-error/Omega control do not follow.
3. The final high-order concentration statement is exact for \(h\ge5\).
   At \(h=3,4\), the zero-rank endpoint rows listed in Section 7 below are
   not eliminated by the support bound and remain in the endpoint-dark
   coefficient ledger.

No change to the theorem or its proof is otherwise needed.

## 2. Matroid union on arbitrary \(2h\) sites: PASS

Let \(n=|W|=2h\), and let both Rado matroids have rank three.  The matroid
union formula is

\[
 r_{M_P\vee M_S}(W)
   =\min_{A\subseteq W}
      \bigl(n-|A|+\rho_P(A)+\rho_S(A)\bigr).             \tag{A1}
\]

An independent union set of size six can be partitioned into an
\(M_P\)-independent set and an \(M_S\)-independent set.  Since each part
has size at most three, equality of the total size forces two disjoint
three-element bases.  Conversely, two disjoint bases form such a union
set.  Thus the absence of disjoint bases is equivalent to the minimum in
(A1) being at most five.  This argument uses the rank bound three, not
\(n=6\).

Write \(A=W\setminus B\) and

\[
 F(B)=|B|+\rho_P(A)+\rho_S(A).
\]

Choose \(B\) inclusion-maximal subject to \(F(B)\le5\).  Because
\(F(B)\ge |B|\), one has \(b=|B|\le5\).  Also

\[
 F(\varnothing)=\rho_P(W)+\rho_S(W)=6,
\]

so \(B\ne\varnothing\).  In particular \(A\ne\varnothing\), since
\(n\ge6>b\).

For \(x\in A\), put

\[
 \epsilon_T(x)=\rho_T(A)-\rho_T(A\setminus\{x\})\in\{0,1\}.
\]

Maximality makes \(B\cup\{x\}\) a non-witness, and integrality therefore
gives

\[
\begin{aligned}
 6
 &\le F(B\cup\{x\})\\
 &=F(B)+1-\epsilon_P(x)-\epsilon_S(x)\\
 &\le6.
\end{aligned}                                               \tag{A2}
\]

The last inequality uses only \(F(B)\le5\) and
\(\epsilon_P,\epsilon_S\ge0\).  Equality throughout (A2) proves

\[
 F(B)=5,
 \qquad
 \epsilon_P(x)=\epsilon_S(x)=0
 \quad(x\in A).                                             \tag{A3}
\]

All inequalities in source display (9) are consequently sound.

## 3. Rado-witness rigidity and linear ranks: PASS

For one endpoint \(T\), let \(J\subseteq A\) minimize

\[
 \rho_T(A)=|A\setminus J|
      +\dim\sum_{y\in J}L_y^T.                              \tag{A4}
\]

If \(x\in A\setminus J\), the same \(J\) is admissible for
\(A\setminus\{x\}\), giving

\[
 \rho_T(A\setminus\{x\})
 \le \rho_T(A)-1,
\]

contrary to (A3).  Hence every minimizing witness contains every point of
\(A\), so its unique possible value is \(J=A\).  In particular,

\[
 \rho_T(A)=\dim U_T,
 \qquad
 U_T:=\sum_{x\in A}L_x^T.                                  \tag{A5}
\]

This is the needed bridge from Rado rank to ordinary aggregate linear
row-span rank.  It is stronger than merely choosing one convenient Rado
witness.

For each \(x\in A\), the image of the simultaneous local map

\[
 \Theta_x=P_x^*\oplus S_x^*:V_x^*\longrightarrow C^*\oplus D^*
\]

lies in \(U_P\oplus U_S\).  Since the two target spaces are direct
summands, (A3)--(A5) give

\[
 \operatorname{rank}\Theta_x
 \le \dim U_P+\dim U_S
 =\rho_P(A)+\rho_S(A)=5-b.                                 \tag{A6}
\]

Thus source equation (12) neither conflates matroid rank with aggregate
linear rank nor assumes that the two local maps have independent domains.

## 4. Classification and endpoint-dark sites: PASS

Adding the \(b\) elements of \(B\) raises either matroid rank by at most
\(b\), so

\[
 \rho_T(A)\ge3-b.                                           \tag{A7}
\]

Together with nonnegativity and
\(\rho_P(A)+\rho_S(A)=5-b\), this yields exactly

\[
\begin{array}{c|c}
b&(\rho_P(A),\rho_S(A))\\ \hline
1&(2,2)\\
2&(1,2),(2,1)\\
3&(0,2),(1,1),(2,0)\\
4&(0,1),(1,0)\\
5&(0,0).
\end{array}                                                 \tag{A8}
\]

For \(b\ge3\), (A6) has rank at most two on the three-dimensional space
\(V_x^*\).  Therefore every \(x\in A\) has a nonzero physical covector in
\(\ker P_x^*\cap\ker S_x^*\).  The endpoint-dark conclusion is sitewise
and uses the complete shore \(A\), not a selected six-site restriction.

For \(b=1\), write \(B=\{x_0\}\).  Equation (A5) gives

\[
 \dim\sum_{x\ne x_0}L_x^P
 =\dim\sum_{x\ne x_0}L_x^S=2.                              \tag{A9}
\]

Full Rado rank three implies that each full aggregate row span is
three-dimensional.  Equivalently, both global endpoint maps are
injective.  Deleting \(x_0\) drops each matroid rank from three to two, so
\(x_0\) is a coloop of each full matroid.  Thus, in a literal full-nine
packet, (A9) is precisely the input of the uniform common-coloop residual
theorem.  The pair equations are needed only for that downstream theorem,
not for (A1)--(A9).

## 5. Exact \(b=2\) local quotient trichotomy

Assume, after exchanging endpoints if necessary,

\[
 \dim U_P=\rho_P(A)=1,
 \qquad
 \dim U_S=\rho_S(A)=2,
 \qquad B=\{u,v\}.                                         \tag{A10}
\]

Put

\[
 H=U_P\oplus U_S\subset C^*\oplus D^*,
 \qquad
 \mathcal Q=(C^*\oplus D^*)/H.
\]

Both \(H\) and \(\mathcal Q\) have dimension three.  For \(y\in B\), let

\[
 \overline\Theta_y:
 V_y^*\xrightarrow{\ P_y^*\oplus S_y^*\ }
 C^*\oplus D^*\longrightarrow\mathcal Q                 \tag{A11}
\]

be the local quotient map.  The exact exhaustive alternative is:

1. for some ordered pair of distinct sites \(x,y\in\{u,v\}\), an endpoint
   map off \(y\) has deficient aggregate rank:

   \[
       \dim(U_P+L_x^P)\le2
       \quad\text{or}\quad
       \dim(U_S+L_x^S)\le2;                                 \tag{A12}
   \]

2. no aggregate shore in (A12) is deficient, but for some
   \(y\in\{u,v\}\) there is a nonzero
   \(\lambda_y\in V_y^*\) with

   \[
       P_y^*(\lambda_y)\in U_P,
       \qquad S_y^*(\lambda_y)\in U_S;                       \tag{A13}
   \]

   this is a core-valued physical probe; or
3. both \(\overline\Theta_u\) and \(\overline\Theta_v\) have rank three
   and hence are linear isomorphisms \(V_y^*\simeq\mathcal Q\).

Indeed, if item 1 is absent, then for each \(y\in\{u,v\}\) the projection
of \(L_y^P\) onto the two-dimensional quotient \(C^*/U_P\) is surjective,
and the projection of \(L_y^S\) onto the one-dimensional quotient
\(D^*/U_S\) is nonzero.  Consequently

\[
        2\le\operatorname{rank}\overline\Theta_y\le3.        \tag{A14}
\]

If the rank is two, its kernel in the three-dimensional domain is
nonzero, and every nonzero kernel vector is precisely a probe satisfying
(A13).  If item 2 is also absent, both maps have rank three and hence are
isomorphisms.  No coefficient equation or matching-power cancellation
enters this argument.

There is also an exact matroid-level transverse statement.  Since
\(\rho_P(A)=1\) and \(\rho_P(W)=3\), while a single ground-set element
raises rank by at most one,

\[
 \rho_P(A\cup\{u\})=\rho_P(A\cup\{v\})=2.                  \tag{A15}
\]

Thus the two complement sites are both necessary in the contraction of
the rank-one endpoint and jointly carry its two transverse matroid
directions.  For the rank-two endpoint, the contraction on \(B\) has rank
one; at least one of \(u,v\), but not necessarily both, carries that
transverse direction.

The isomorphisms in item 3 are only quotient-linear identifications.  They
do not supply target-zero representatives, separated endpoint probes,
transport of the fixed pure-label diagonal, a nonzero physical four-cut,
or membership of clean-error Jacobian columns.  In particular, they must
not be called clean curved charts.

## 6. No hidden six-site or common-power step

The only numerical use of the endpoint rank is the constant six in the
union rank.  The ground set remains the complete \(2h\)-site set
throughout.  The bound \(b\le5\) follows from the union defect and does not
replace \(W\) by six sites.

Likewise, Sections 2--5 concern local row spaces and matroid ranks only.
They neither divide by \(q^{[h-1]}\) nor infer vanishing of individual
matching terms from a cancelling tensor equality.  When the \(b=1\)
branch is passed to the common-coloop theorem, that separate theorem uses
the actual consecutive powers on the same complete \(2h\)-site packet.

## 7. Rootless response support and exact thresholds: PASS

Suppose now that the surrounding rootless theorem supplies

\[
 R_*=P^{\mathsf T}K_*S,
 \qquad R_*^{[h]}\ne0.                                     \tag{A16}
\]

If \(\rho_P(A)=0\), (A5) forces \(L_x^P=0\) for every \(x\in A\), so the
entire \(P\)-star is supported on \(B\).  Every edge occurring in \(R_*\)
then has a \(P\)-leg at a site of \(B\).  A nonzero product of \(h\) such
edges needs \(h\) distinct \(P\)-leg sites because the site-square-zero
relations kill every collision.  Hence

\[
 h>b\quad\Longrightarrow\quad R_*^{[h]}=0.                 \tag{A17}
\]

The same proof applies if \(\rho_S(A)=0\).  This is a support-filtration
argument: no expansion term with the required site support exists, so
cancellation cannot create one.

For \(b=5\), both endpoint ranks on \(A\) are zero.  Both stars, and hence
\(R_*\), are supported in the five-site subalgebra on \(B\).  Its maximum
nonzero degree is five, whereas \(R_*^{[h]}\) has degree \(2h\ge6\).
Therefore this row is impossible for every \(h\ge3\), including the cases
where \(h\le b\).

The remaining zero-rank rows have the following exact status:

\[
\begin{array}{c|c|c}
b&\text{zero-rank pairs}&\text{excluded by (A17) when}\\ \hline
3&(0,2),(2,0)&h\ge4\\
4&(0,1),(1,0)&h\ge5\\
5&(0,0)&\text{all }h\ge3.
\end{array}                                                 \tag{A18}
\]

Consequently, for \(h\ge5\), the only surviving incidence families are
the \(b=1\) common-coloop shore, the \(b=2\) line-plus-plane shore, and the
\(b=3\) \((1,1)\) endpoint-dark shore.  For \(h=4\), the \(b=4\)
zero-rank pair can still survive; for \(h=3\), the \(b=3\) and \(b=4\)
zero-rank pairs can still survive.  These low-order cases are not new
matroid families, but they still require the endpoint-dark coefficient
ledger and are not closed by (A17).

## 8. Clarifications incorporated

The source theorem was mathematically correct.  It now additionally:

1. states that the common-coloop routing is conditional on the literal
   full-nine packet;
2. appends the quotient construction (A10)--(A14) to the \(b=2\) sentence
   and calls the final branch two local quotient isomorphisms, not clean
   charts; and
3. replaces the unquantified phrase "high-order" by \(h\ge5\), while
   retaining the \(h=3,4\) rows in (A18).

These are scope corrections only; none changes equations (2)--(13) or the
classification table.
