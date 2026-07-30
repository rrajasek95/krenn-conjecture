# The scalar-zero tangent packet has a pure-descent or apolar-Hall alternative

## 1. Outcome

Let \(W\) have \(2h\) sites, \(h\geq3\), and suppose the complete physical
pair rows are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                              \tag{1}
\]

Fix an off-diagonal curvature entry

\[
 \alpha=a_{ab}\ne0,\qquad \tau=\operatorname {tr}a,
 \qquad K_*=\tau E_{ab}-\alpha I.                    \tag{2}
\]

Thus \(K_*\) is invertible, its contraction with \(a\) is zero, and, for

\[
                   r=\sum_{i,j}(K_*)_{ij}p_i s_j,     \tag{3}
\]

the rootless scalar-zero packet is

\[
             rq^{[h-1]}=-\alpha\Delta_{2h,3},
             \qquad r^{[h]}\ne0.                     \tag{4}
\]

There is a uniform, support-free alternative.

* If \(r^{[h]}\) has only constant-colour coordinates, it is, after a
  one-site diagonal normalization and deletion of unused colour axes, an
  exact unary, binary, or ternary matching source on \(W\).  The ternary
  case is an immediate two-site descent: it is impossible at \(h=3\) by
  the proved six-site theorem, and only
  the ternary case contradicts minimality in higher order.  The unary and
  binary cases remain structural alternatives.
* Otherwise there is a mixed word \(\omega\) for which a scalar matrix
  \(R_\omega\), obtained from the invertibly paired endpoint stars, obeys

  \[
    \operatorname {haf}(R_\omega)\ne0,
    \qquad
    D\operatorname {haf}_{Q_\omega}(R_\omega)=0.       \tag{5}
  \]

  Moreover the first inequality supplies a balanced partition
  \(W=A\sqcup B\), \(|A|=|B|=h\), on which the simultaneous-star matrix
  has a nonzero permanent.  In particular, its nonzero-entry graph has a
  perfect matching and therefore satisfies all Hall inequalities.

The complete nine rows give more than (5): on every word they give one
explicit \(3\times3\) cohafnian identity, equation (12) below.  This is the
natural place where common-power information meets the star factorization.
Neither side alone can close the packet.  Section 5 gives a uniform
injective-star response guard, and Section 6 points out that the existing
exact rational pair-cap example already satisfies (4), including
\(r^{[3]}\ne0\), when the star factorization and the other eight rows are
forgotten.

## 2. Word scalarization and the full-nine cohafnian identity

Write \(p_{i,x}\in V_x\) and \(s_{j,x}\in V_x\) for the site components of
the two stars.  For a word

\[
                         \omega:W\longrightarrow\{0,1,2\},       \tag{6}
\]

let \(P_\omega,S_\omega\) be the \(2h\times3\) scalar matrices whose
\(x\)-th rows are

\[
 P_x=(p_{0,x}(\omega_x),p_{1,x}(\omega_x),p_{2,x}(\omega_x)),
 \quad
 S_x=(s_{0,x}(\omega_x),s_{1,x}(\omega_x),s_{2,x}(\omega_x)).    \tag{7}
\]

Let \(Q_\omega\) be the symmetric zero-diagonal \(2h\times2h\) matrix
obtained by taking the \((\omega_x,\omega_y)\)-coordinate of the block
\(q_{xy}\).  Define its cohafnian matrix by

\[
 H(Q_\omega)_{xy}=
 \begin{cases}
  \operatorname {haf}((Q_\omega)_{W\setminus\{x,y\}}),&x\ne y,\\
  0,&x=y.
 \end{cases}                                                   \tag{8}
\]

The divided-power conventions give

\[
 [q^{[h]}]_\omega=\operatorname {haf}(Q_\omega),
 \qquad
 [p_i s_jq^{[h-1]}]_\omega
       =(P_\omega^{T}H(Q_\omega)S_\omega)_{ij}.       \tag{9}
\]

Let

\[
 D_\omega=
 \begin{cases}
 E_{cc},&\omega=c^{2h}\text{ is constant},\\
 0,&\omega\text{ is mixed}.
 \end{cases}                                                   \tag{10}
\]

Taking the coordinate \(\omega\) in all nine equations (1) proves the
single matrix identity

\[
 \boxed{
 P_\omega^{T}H(Q_\omega)S_\omega
       =D_\omega-\operatorname {haf}(Q_\omega)a.}     \tag{11}
\]

This retains the endpoint order: its \((i,j)\)-entry is literally the
\(p_i s_j\) row.  It also retains all complex cancellation, since
cohafnians are the aggregate coefficients of \(q^{[h-1]}\), not selected
matching terms.

For later reference, (11) is the promised full-nine identity:

\[
 \boxed{
 \begin{array}{ll}
 P_\omega^{T}H(Q_\omega)S_\omega
       =-\operatorname {haf}(Q_\omega)a,
       &\omega\text{ mixed},\\[2mm]
 P_c^{T}H(Q_c)S_c
       =E_{cc}-\operatorname {haf}(Q_c)a,
       &\omega=c^{2h}.
 \end{array}}                                                  \tag{12}
\]

Thus the mixed response matrices are not arbitrary zero contractions:
they are all scalar multiples of the same direct block \(a\).

## 3. The tangent and apolar identities

For the same word define

\[
 (R_\omega)_{xy}
   =P_xK_*S_y^T+P_yK_*S_x^T\quad(x\ne y),
 \qquad (R_\omega)_{xx}=0.                            \tag{13}
\]

This is precisely the scalar edge matrix of \(r\).  Consequently

\[
                [r^{[h]}]_\omega=\operatorname {haf}(R_\omega). \tag{14}
\]

The derivative of the degree-\(h\) hafnian is

\[
 D\operatorname {haf}_{Q}(R)
   =\sum_{x<y}R_{xy}
          \operatorname {haf}(Q_{W\setminus\{x,y\}}).           \tag{15}
\]

Equations (8), (11), and (13) therefore give

\[
\begin{aligned}
 D\operatorname {haf}_{Q_\omega}(R_\omega)
  &=\sum_{i,j}(K_*)_{ij}
       (P_\omega^TH(Q_\omega)S_\omega)_{ij}\\
  &=\sum_{i,j}(K_*)_{ij}(D_\omega)_{ij}
     -\operatorname {haf}(Q_\omega)
       \sum_{i,j}(K_*)_{ij}a_{ij}.                    \tag{16}
\end{aligned}

By (2), the last sum is

\[
       \tau a_{ab}-\alpha\operatorname {tr}a=0.       \tag{17}
\]

The diagonal of \(K_*\) is \(-\alpha I\), because \(a\ne b\).  Hence

\[
 \boxed{
 D\operatorname {haf}_{Q_\omega}(R_\omega)=
 \begin{cases}
  -\alpha,&\omega=c^{2h},\\
  0,&\omega\text{ mixed}.
 \end{cases}}                                                  \tag{18}
\]

This is exactly (4) word by word.  It says that all three pure
scalarizations are non-apolar, while every mixed scalarization is apolar.

## 4. Pure descent or a simultaneous-star Hall certificate

**Theorem 4.1 (pure-descent/apolar-Hall alternative).**  Under (1)--(4),
exactly one of the following structural branches occurs.

1. There is a nonempty \(C\subseteq\{0,1,2\}\) and nonzero scalars
   \(\lambda_c\) such that

   \[
                   r^{[h]}=\sum_{c\in C}\lambda_cX_c.           \tag{19}
   \]

   After a local algebra projection onto the axes in \(C\) and an
   invertible diagonal change at one site, \(r\) becomes an exact
   \(|C|\)-colour matching source on \(W\).  If \(|C|=3\), this is a
   two-site ternary descent.
2. There is a mixed word \(\omega\) such that (5) holds.  In addition,
   some balanced partition \(W=A\sqcup B\) satisfies

   \[
       \operatorname {per}
       \bigl((P_xK_*S_y^T)_{x\in A,y\in B}\bigr)\ne0.           \tag{20}
   \]

   Therefore the bipartite graph

   \[
    x\sim y\quad\Longleftrightarrow\quad
            P_xK_*S_y^T\ne0,qquad x\in A, y\in B,             \tag{21}
   \]

   has a perfect matching.  In particular

   \[
                  |N(U)|\geq|U|\quad\text{for every }U\subseteq A. \tag{22}
   \]

**Proof.**  If every mixed coefficient of \(r^{[h]}\) is zero, (14) and
\(r^{[h]}\ne0\) give (19) with \(C\ne\varnothing\).  Project every unused
colour axis to zero at every site.  This is a local algebra endomorphism
and does not change (19).  At one fixed site, multiply the \(c\)-axis by
\(\lambda_c^{-1}\).  Functoriality of matching powers changes (19) into

\[
                            \sum_{c\in C}X_c,          \tag{23}
\]

which proves the first branch.

Otherwise choose a mixed \(\omega\) with
\(\operatorname {haf}(R_\omega)\ne0\).  Equation (18) proves (5).  Expand
each edge entry in the hafnian using (13), thereby orienting every matching
edge from its \(P\)-endpoint to its \(S\)-endpoint.  Grouping terms by the
set \(A\) of \(P\)-endpoints gives the exact identity

\[
 \operatorname {haf}(R_\omega)
   =\sum_{\substack{A\subseteq W\\|A|=h}}
      \operatorname {per}
       \bigl((P_xK_*S_y^T)_{x\in A,y\in W\setminus A}\bigr).    \tag{24}
\]

Since the left side is nonzero, at least one permanent in (24) is nonzero.
A nonzero permanent has a nonzero permutation term, which is a perfect
matching in (21).  Hall's inequalities follow.  \(\square\)

Two elementary consequences make the certificate easy to falsify in a
candidate packet.  Every site is \(P\)-active or \(S\)-active on the
selected word.  Moreover there are at most \(h\) \(P\)-only sites and at
most \(h\) \(S\)-only sites: every \(P\)-only site must lie in \(A\), and
every \(S\)-only site must lie in \(B\).

Endpoint-star injectivity is global and does not strengthen these
wordwise statements automatically.  A word scalarization can lower either
star rank, and even a rank-one matrix in (20) can have nonzero permanent.

## 5. A uniform injective-star response guard

The common-power relation in (1) cannot be replaced by arbitrary response
tensors.  The following construction satisfies both injective-star
conditions, an invertible \(K_*\), the formal nine response rows, and
\(r^{[h]}\ne0\), uniformly in \(h\).

Choose disjoint pairs

\[
 P_1=\{a_1,b_1\},\qquad P_2=\{a_2,b_2\},              \tag{25}
\]

put \(R_0=W\setminus(P_1\cup P_2)\), and split

\[
 R_0=A_0\sqcup B_0,qquad |A_0|=|B_0|=h-2.            \tag{26}
\]

Fix \(a_0\in A_0,b_0\in B_0\) and put \(P_0=\{a_0,b_0\}\).  Define

\[
\begin{array}{lll}
 p_0=\displaystyle\sum_{x\in A_0}e_0^{(x)},
 &\quad&s_0=\displaystyle\sum_{y\in B_0}e_0^{(y)},\\[2mm]
 p_1=e_1^{(a_1)},&&s_1=e_1^{(b_1)},\\
 p_2=e_2^{(a_2)},&&s_2=e_2^{(b_2)},                  \tag{27}
\end{array}
\]

and the degree-\(2h-2\) tensor

\[
 F=F_0+F_1+F_2,
 \qquad
 F_c=\bigotimes_{x\notin P_c}e_c^{(x)}.              \tag{28}
\]

Only the two holes of \(F_c\) can accept the two linear factors in a
nonzero product.  Equations (27)--(28) therefore give all nine identities

\[
                         p_i s_jF=\delta_{ij}X_i.      \tag{29}
\]

Both star triples are injective, since their displayed supports are
disjoint.  Take a direct block with \(a_{ab}=-1\), \(a\ne b\), and every
other entry zero.  Then

\[
 \alpha=-1,\quad\tau=0,\quad K_*=I,
 \quad r=p_0s_0+p_1s_1+p_2s_2,
 \quad rF=\Delta_{2h,3}.                              \tag{30}
\]

Let \(\omega\) be colour \(0\) on \(R_0\), colour \(1\) on \(P_1\), and
colour \(2\) on \(P_2\).  A perfect matching contributing to
\([r^{[h]}]_\omega\) must use the two edges \(a_1b_1,a_2b_2\), followed by
a bijection from \(A_0\) to \(B_0\).  Hence

\[
                         [r^{[h]}]_\omega=(h-2)!\ne0.             \tag{31}
\]

If formal symbols \(Q=0\) and \(F\) are used in place of
\(q^{[h]}\) and \(q^{[h-1]}\), then (29) is literally the full nine-row
system \(a_{ij}Q+p_i s_jF=\delta_{ij}X_i\).  What is deliberately missing
is a quadratic \(q\) satisfying

\[
                         q^{[h-1]}=F,qquad q^{[h]}=0.             \tag{32}
\]

At \(h=3\), the
[uniform pure-lift theorem](uniform-pure-lift-private-edge-degeneration.md)
proves that no such \(q\) exists.  Thus (25)--(31) is not an eight-site
counterexample.  It is a sharp guard: exterior rank, injective endpoint
stars, all nine response products, invertibility of \(K_*\), and
nonnilpotence of \(r\) are mutually compatible.  A successful argument
must use the common-power cohafnians in (11), not only the response
rectangle.

## 6. A common-power tangent guard at \(h=3\)

The complementary warning is already present in the exact rational data of
[the polarized pair-cap example](polarized-six-site-paircap-counterexample.md).
Its quadratics \(q,z\) satisfy

\[
                         zq^{[2]}=\Delta_{6,3}.        \tag{33}
\]

They also satisfy \(z^{[3]}\ne0\), a fact not needed in the original note.
Indeed, on the mixed word

\[
                         \omega=(0,1,1,0,0,1),         \tag{34}
\]

the only supported \(z\)-edges are

\[
                         z_{03}=1,qquad z_{15}=1/3,
                         \qquad z_{24}=2.              \tag{35}
\]

They form the unique supported perfect matching, so

\[
                         [z^{[3]}]_\omega=2/3\ne0.     \tag{36}
\]

Equation (33) makes its hafnian derivative zero on every mixed word and
one on every pure word.  Thus even the complete common-power tangent
equation together with mixed nonnilpotence is consistent.  This example
does not supply \(z=\sum(K_*)_{ij}p_i s_j\) for two injective star triples,
and it does not satisfy a shared set of nine physical rows.  It guards
exactly the apolar/common-power half of the argument, complementary to
Section 5.

## 7. The remaining proof target

The scalar-zero branch has therefore been reduced without support
enumeration to one interface.  In the mixed branch, the same word has

\[
\begin{gathered}
 P_\omega^TH(Q_\omega)S_\omega
       =-\operatorname {haf}(Q_\omega)a,\\
 \operatorname {haf}
   (P_\omega K_*S_\omega^T+S_\omega K_*^TP_\omega^T)\ne0,\\
 \sum_{x<y}(R_\omega)_{xy}H(Q_\omega)_{xy}=0,          \tag{37}
\end{gathered}
\]

while the three constant words replace the last zero by \(-\alpha\) and
the first right side by \(E_{cc}-\operatorname {haf}(Q_c)a\).

A genuine closure lemma must couple these identities across words.  One
useful precise form would be:

> Under the global rank-three conditions on both endpoint stars and the
> full cohafnian system (12), mixed apolarity forces every mixed coefficient
> of \(r^{[h]}\) to vanish, and the three nonzero pure derivatives force all
> three pure coefficients of \(r^{[h]}\) to be nonzero.

That statement would put Theorem 4.1 in its ternary descent branch and
finish the scalar-zero packet by minimality.  Sections 5 and 6 show why
both hypotheses are essential.  Alternatively, one can attack (37)
directly by proving that its Hall-certified permanent is incompatible with
the single direct-block proportionality in (12).  This is a simultaneous
star/cohafnian problem, rather than a search through support cases.
