# Common-origin factorization has no scalar rank obstruction

## 1. Outcome

Let

\[
 \mathcal R=\bigotimes_{u=0}^5(\mathbb F\oplus \mathbb Fz_u),
 \qquad z_u^2=0,
\]

over a field of characteristic different from two.  There is a quadratic
\(q\), with

\[
                         q^{[3]}=0,                       \tag{1}
\]

and six linear forms \(p_0,p_1,p_2,s_0,s_1,s_2\) such that

\[
       p_i s_j q^{[2]}=\delta_{ij}z_0z_1z_2z_3z_4z_5.   \tag{2}
\]

Consequently, on putting \(A_i=p_iq\) and \(B_j=s_jq\), all six cubic
factors have one common quadratic origin and nevertheless

\[
        A_iB_j=2\delta_{ij}z_0z_1z_2z_3z_4z_5.          \tag{3}
\]

In particular, vanishing of the six-site matching power does **not** force
the middle catalecticant of \(q^{[2]}\) to have rank at most two.  It can
have full rank six.  Thus a proof of the non-pure ternary boundary cannot
come from a pointwise rank bound on the factorization
\((p_iq)(s_jq)\), even after retaining both the common \(q\)-origin and
\(q^{[3]}=0\).

This is deliberately a scalar local model.  Its three right-hand sides in
(2) lie on the same top-degree line; it does not have three independent
local colour axes and is not a Krenn counterexample.  Its force is to
isolate what a successful factorization argument must still use: the
sitewise separation of the three tensors \(X_i=e_i^{\otimes6}\).  Treating
the \(X_i\)'s merely as three nonzero values, or scalarizing before using
their local factors, loses the obstruction completely.

## 2. A six-cycle cancellation with invertible cofactor form

Use the cycle order

\[
                         0,1,5,2,4,3,0
\]

and assign its consecutive edge weights

\[
                         (a,b,c,d,e,f).
\]

Thus

\[
 q=az_0z_1+bz_1z_5+cz_5z_2+dz_2z_4+ez_4z_3+fz_3z_0.  \tag{4}
\]

The only perfect matchings of this cycle are its two alternating
one-factors, so

\[
             q^{[3]}=(ace+bdf)z_0z_1z_2z_3z_4z_5.       \tag{5}
\]

Let \(C=(C_{uv})\) be the symmetric zero-diagonal cofactor matrix

\[
 C_{uv}=[z_{[6]\setminus\{u,v\}}]q^{[2]}
       =\operatorname{haf}(q|_{[6]\setminus\{u,v\}}).   \tag{6}
\]

With row order \((0,5,4)\) and column order \((1,2,3)\), the only nonzero
block of \(C\) is

\[
 D=\begin{pmatrix}
 ce&be&bd\\
 df&ae&ad\\
 cf&bf&ac
 \end{pmatrix},
 \qquad
 C\sim\begin{pmatrix}0&D\\D^{\mathsf T}&0\end{pmatrix}. \tag{7}
\]

For example, deleting \(0,1\) leaves the unique two-matching
\(25\mid34\), of weight \(ce\), while deleting \(0,3\) leaves
\(15\mid24\), of weight \(bd\).  The other seven displayed entries follow
in the same way.  Deleting two vertices on the same side of the cycle
bipartition leaves no perfect matching, which gives the two zero diagonal
blocks in (7).

A direct determinant expansion gives

\[
             \det D=(ace-bdf)^2,
 \qquad      \det C=-(ace-bdf)^4.                       \tag{8}
\]

On the hypersurface (5), if all six edge weights are nonzero, then
\(bdf=-ace\), and hence

\[
                         \det C=-16(ace)^4\ne0.          \tag{9}
\]

This gives a five-parameter family of smooth scalar points of the
hafnian-zero hypersurface with a nonsingular cofactor form.  The familiar
rank-one adjugate phenomenon for determinants has no hafnian analogue
here.

## 3. Exact rational diagonal response

Take

\[
                         (a,b,c,d,e,f)=(2,1,-1,1,1,2).  \tag{10}
\]

The two perfect matching weights are \(-2\) and \(2\), proving (1).  In
fact, they are respectively

\[
              01\mid25\mid34\quad\hbox{and}\quad
              03\mid15\mid24.                           \tag{11}
\]

In the ordinary site order \((0,1,2,3,4,5)\), (6) is

\[
 C=\begin{pmatrix}
 0&-1& 1& 1& 0& 0\\
-1& 0& 0& 0&-2& 2\\
 1& 0& 0& 0& 2& 2\\
 1& 0& 0& 0&-2& 2\\
 0&-2& 2&-2& 0& 0\\
 0& 2& 2& 2& 0& 0
 \end{pmatrix},
 \qquad \det C=-256.                                    \tag{12}
\]

Set

\[
\begin{array}{lll}
p_0=z_0,&p_1=z_1,&p_2=z_2,\\[2mm]
s_0=(-z_1+z_3)/2,&
s_1=-z_0/2+z_5/4,&
s_2=(z_4+z_5)/4.
\end{array}                                             \tag{13}
\]

The coefficient of the top monomial in \(p_i s_jq^{[2]}\) is the
bilinear pairing of the coefficient rows of \(p_i,s_j\) through \(C\).
If \(P=(I_3\ 0)\), the three rows in the second line of (13) are exactly
the first three rows of \(C^{-1}\).  Therefore

\[
                         PCS^{\mathsf T}=I_3,            \tag{14}
\]

which is (2).  Associativity and \(q^2=2q^{[2]}\) then give (3) without
any independent choice of the cubic factors.

## 4. Why the cross-products themselves are also insufficient

The independence of the target tensors alone does not repair a proof that
has already forgotten the common origin.  Let each local space contain
independent \(e_0,e_1,e_2\), choose any three distinct triples
\(T_0,T_1,T_2\subset[6]\), and put

\[
 A_i=\bigotimes_{u\in T_i}e_i^{(u)},
 \qquad
 B_i=2\bigotimes_{u\notin T_i}e_i^{(u)}.                \tag{15}
\]

Then \(A_iB_i=2X_i\).  For \(i\ne j\), the equal-sized distinct triples
satisfy \(T_i\setminus T_j\ne\varnothing\); at such a site both \(A_i\)
and \(B_j\) are occupied, so their product is zero in the site-square-zero
algebra.  Hence

\[
                         A_iB_j=2\delta_{ij}X_i.         \tag{16}
\]

This second example has the genuine three independent pure targets but
does not assert \(A_i=p_iq,B_j=s_jq\) for one \(q\).  Together, (3) and
(16) show the exact boundary of the abstract route:

* common origin plus \(q^{[3]}=0\) does not yield a scalar rank defect;
* independent pure targets plus all cross-products zero do not contradict
  middle-degree factorization; and
* any positive lemma must use **both** structures simultaneously, before
  scalar contraction destroys the six sitewise colour lines.

The standalone checker
[`verify_common_origin_factorization_rank_countermodel.py`](../computations/verify_common_origin_factorization_rank_countermodel.py)
verifies the symbolic determinant formulas, every coefficient of (1)--(3)
over \(\mathbb Q\), and the complementary-support construction (15)--(16).
