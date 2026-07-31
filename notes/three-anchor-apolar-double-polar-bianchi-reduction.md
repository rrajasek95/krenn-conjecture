# The averaged Bianchi class is a defect-corrected reciprocal double polar

## 1. Outcome

Let \(W=\{0,\ldots,5\}\), let \(Q,R\) be symmetric zero-diagonal edge
arrays, and write

\[
 F(Q+tR)=\operatorname {haf}(Q+tR)
          =Q_0+tQ_1+t^2Q_2+t^3Q_3.                  \tag{1}
\]

For a selected off-diagonal deleted-pair row, put

\[
                         Q_1=-\alpha Q_0,
 \qquad \chi=\alpha Q_2+Q_3.                           \tag{2}
\]

Define the cohafnian polar

\[
 H(A)_{ij}=\operatorname {haf}(A[W\setminus\{i,j\}])
 \quad(i\ne j),\qquad H(A)_{ii}=0.                    \tag{3}
\]

Its second iterate has, for \(i\ne j\), the exact cross-star defect

\[
 \boxed{H(H(A))_{ij}=F(A)A_{ij}+2\mathcal B_{ij}(A)}
 \qquad(i\ne j),                                      \tag{4}
\]

where, for \(U=W\setminus\{i,j\}\),

\[
 \mathcal B_{ij}(A)=
 \sum_{\substack{S\subset U\\|S|=2}}
   \prod_{s\in S}A_{is}
   \prod_{u\in U\setminus S}A_{ju},
 \qquad \mathcal B_{ii}(A)=0.                         \tag{5}
\]

With \(\mathcal B_{ii}=0\), both sides of (4) vanish on the diagonal
(\(A_{ii}=0\) and \(H(A)_{ii}=0\)), so the following holds as a matrix
identity.  The correct double-polar covariant is

\[
 \mathcal P(A):=H(H(A))-2\mathcal B(A)=F(A)A.         \tag{6}
\]

Put \(C_k=[t^k]\mathcal P(Q+tR)\).  Then

\[
 C_1=Q_1Q+Q_0R,\qquad C_3=Q_3Q+Q_2R,                 \tag{7}
\]

and

\[
 \boxed{Q_0C_3-Q_2C_1=(Q_0Q_3-Q_1Q_2)Q
                         =Q_0\chi Q.}                 \tag{8}
\]

The committed twenty-cut marking identity in
[`h3-nonclean-twojet-middle-core.md`](h3-nonclean-twojet-middle-core.md)
is

\[
 {1\over8}\sum_{|S|=3}\Theta_S(2\alpha R,R,Q)=\chi. \tag{9}
\]

Combining (8) and (9) gives the exact comparison

\[
 \boxed{
 Q_0C_3-Q_2C_1
   ={Q_0\over8}\left(\sum_{|S|=3}
       \Theta_S(2\alpha R,R,Q)\right)Q.}              \tag{10}
\]

Therefore the reciprocal Hankel component \(Q_0C_3-Q_2C_1\) of the
defect-corrected double polar is exactly the \(Q_0Q\)-scaled radial image
of the averaged scalar Bianchi class
\({1\over8}\sum_{|S|=3}\Theta_S(2\alpha R,R,Q)\); the two objects agree
after multiplying the scalar class by \(Q_0Q\), not literally.  The six
terms in
(5) cannot be dropped: they are the cross-word class which an ordinary
cohafnian sandwich or top-apolar quotient forgets.

There is an equivalent cap reformulation.  Put

\[
                         A_{\mathrm{cap}}=\alpha Q+R.  \tag{11}
\]

The selected source row and homogeneity give

\[
\begin{aligned}
 \operatorname {haf}(A_{\mathrm{cap}})
 &=\alpha^3Q_0+\alpha^2Q_1+\alpha Q_2+Q_3\\
 &=\alpha^2(\alpha Q_0+Q_1)+\chi=\chi.               \tag{12}
\end{aligned}
\]

Consequently

\[
 \mathcal P(A_{\mathrm{cap}})=\chi A_{\mathrm{cap}},
 \qquad
 \boxed{\chi=0
 \quad\Longleftrightarrow\quad
 H(H(A_{\mathrm{cap}}))=2\mathcal B(A_{\mathrm{cap}})}             \tag{13}
\]

for a nonzero cap.  This is only a reformulation of cleanliness.  Its
useful feature is that \(H(A_{\mathrm{cap}})\) is exactly the vector of
four-hole hafnians, the lower-cofactor object potentially accessible to
the Hamming-two and adjacent-chart rows.  No result here says that those
physical rows already prove the boxed equality.

This does not prove the physical three-anchor landing.  It reduces that
landing to one explicit statement: the complete source must identify its
third-jet aggregate with the right side of (9), or kill the aggregate
landing error below.  No individual-cut vanishing is necessary.

## 2. Proof of the new double-polar identity

Fix \(i\ne j\) and expand \(H(H(A))_{ij}\) over the three perfect
matchings of \(U=W\setminus\{i,j\}\).  There are two disjoint monomial
types.

* A monomial containing \(A_{ij}\) is \(A_{ij}\) times one six-site
  perfect-matching monomial, and each term of \(A_{ij}F(A)\) occurs once.
* Otherwise \(i\) is incident with two vertices of \(U\), and \(j\) with
  the other two.  The choice of the two neighbours of \(i\) gives one
  term of (5), and it occurs for the two possible outer pairings.

This proves (4).  For a normalization check, if every edge of \(A\) is
one, then \(F(A)=15\), \(H(A)_{ij}=3\), and \(H(H(A))_{ij}=27\); the
defect is \(12=2\cdot6\).

Equation (6) now gives

\[
 \mathcal P(Q+tR)
 =(Q_0+tQ_1+t^2Q_2+t^3Q_3)(Q+tR).                    \tag{14}
\]

Taking the coefficients of \(t,t^3\) proves (7), and direct elimination
proves the first equality in (8).  Substitution of (2) proves the second.
No division or nonvanishing assumption is used.

## 3. Local landing is sufficient, but not necessary

For a three-set \(S\), with complement \(T\), write

\[
\begin{aligned}
 \Theta_S(A,B,Q)={}&
 \sum_{\{i,k\}\subset S} A_{ik}
       \sum_{j\in T}B_{pj}Q_{T\setminus\{j\}}\\
 &+\operatorname {per}(B_{S,T}),                     \tag{15}
\end{aligned}
\]

where \(p\) is the unique member of \(S\setminus\{i,k\}\).  A sufficient
physical landing on this cut is

\[
 \widehat A_{ik}=2\alpha R_{ik}\quad(\{i,k\}\subset S),
 \qquad
 \widehat B_{pj}=R_{pj}\quad(p\in S,j\in T).          \tag{16}
\]

It requires only three internal second-jet entries and nine crossing
first-jet entries, not a global tangent derivation.  If the corresponding
physical mixed coefficient is zero, (16) makes the desired
\(\Theta_S(2\alpha R,R,Q)\) zero.

The exact error when (16) is not literal is also small.  Put

\[
 \varepsilon=\widehat A-2\alpha R,\qquad
 \delta=\widehat B-R                                  \tag{17}
\]

on those entries and define

\[
 \ell_p(B,Q)=\sum_{j\in T}B_{pj}Q_{T\setminus\{j\}}. \tag{18}
\]

Multilinearity gives

\[
\begin{aligned}
 \Theta_S(\widehat A,\widehat B,Q)
 -\Theta_S(2\alpha R,R,Q)
 ={}&\sum_{\{i,k\}\subset S}
   \varepsilon_{ik}\ell_p(R+\delta,Q)\\
 &+2\alpha\sum_{\{i,k\}\subset S}
   R_{ik}\ell_p(\delta,Q)\\
 &+\operatorname {per}((R+\delta)_{S,T})
       -\operatorname {per}(R_{S,T}).                 \tag{19}
\end{aligned}
\]

Consequently the genuinely necessary target is aggregate error
annihilation after summing (19), not twenty separate instances of (16).
This is where simultaneous diagonal-anchor provenance may enter.

## 4. Exact cancellation guard against a cutwise target

Cutwise vanishing cannot follow from the endpoint polar identity, even
when the tail is already clean.  Take

\[
 Q_{01}=Q_{23}=Q_{45}=1
\]

and every other entry of \(Q\) zero.  Let

\[
\begin{aligned}
 u&=(1,-1,2,0,1,1),\\
 v&=(1,2,-2,1,-2,1),\\
 R_{ij}&=u_iv_j+v_iu_j,\qquad \alpha=-2.               \tag{20}
\end{aligned}
\]

Exact expansion gives

\[
                    (Q_0,Q_1,Q_2,Q_3)=(1,2,6,12).     \tag{21}
\]

Thus both \(\alpha Q_0+Q_1=0\) and \(\chi=0\).  Nevertheless, in
lexicographic order on the twenty three-sets, the cut values are

\[
\begin{gathered}
 -12,-12,-12,-36,-20,20,-28,20,-4,-36,\\
 -44,-4,20,-28,20,-12,20,44,52,52.                    \tag{22}
\end{gathered}
\]

They are individually nonzero and sum to zero.  This is a scalar
rank-two response packet, not a full-nine source.  It proves exactly that
(10), and even cleanliness, control only the aggregate.  A positive proof
may use (16) cutwise, but it must not promote that sufficient construction
to a necessary conclusion.

## 5. Scope and audit

The new rigorous content is (4), (8), their exact comparison (10) with
the committed average, the cap reformulation (11)--(13), the local error
formula (19), and the cancellation guard (20)--(22).  No claim is made
that the complete anchors already annihilate (19); that is the remaining
physical chain-map statement.

The lightweight, dependency-free checker
[`verify_three_anchor_apolar_double_polar_bianchi_reduction.py`](../computations/verify_three_anchor_apolar_double_polar_bianchi_reduction.py)
verifies (4) formally on all fifteen edge variables, checks (8), (10), and
(19) over exact arithmetic, and reproduces (21)--(22).  It performs no
word-space or source-support enumeration.
