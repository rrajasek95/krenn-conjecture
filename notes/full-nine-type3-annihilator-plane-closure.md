# The full nine pair equations close the type-3 exceptional shore uniformly

## 1. Outcome and exact scope

The proof is first written at the six-site boundary and then promoted in
Section 9 to every even residual size.  Let \(W\) initially have six
sites.  At each site \(y\), let \(V_y\) be the
three-dimensional physical colour space with fixed basis

\[
                    e_0^{(y)},e_1^{(y)},e_2^{(y)}\in V_y,
\]

and work in the site-square-zero algebra

\[
 {\cal R}_W=\bigotimes_{y\in W}(\mathbb C\oplus V_y),
 \qquad V_yV_y=0.
\]

Suppose \(q\in({\cal R}_W)_2\), \(p_i,s_j\in({\cal R}_W)_1\), and
\(a=(a_{ij})\in\operatorname {Mat}_{3\times3}(\mathbb C)\) satisfy all
nine physical pair equations

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad
 X_i=\bigotimes_{y\in W}e_i^{(y)},
 \qquad 0\le i,j\le2.                                  \tag{1}
\]

Let \(C=\mathbb C^3\) and \(D=\mathbb C^3\) be the two row-index spaces,
with fixed labelled bases \(f_0,f_1,f_2\) and \(g_0,g_1,g_2\), and define

\[
 \begin{aligned}
 P:C&\longrightarrow\bigoplus_{y\in W}V_y,
 &P(f_i)&=p_i,\\
 S:D&\longrightarrow\bigoplus_{y\in W}V_y,
 &S(g_j)&=s_j.
 \end{aligned}                                        \tag{2}
\]

For \(x\in W\), write \(P_{\bar x}\) and \(P_x\) for the projections of
\(P\) to the sites away from \(x\) and to \(V_x\), respectively.

**Theorem 1.1 (type-3 exceptional-shore closure).**  If \(P\) is
injective, then

\[
                         \operatorname {rank}P_{\bar x}\ge2
                         \qquad(x\in W).               \tag{3}
\]

The same assertion holds for the second endpoint star \(S\) when \(S\) is
injective.

The theorem excludes both ranks zero and one and uses no contracted cap
matrix.  A nonnilpotent contracted response

\[
                    r(K)=\sum_{i,j}K_{ij}p_i s_j
                    \quad\text{with}\quad r(K)^{[3]}\ne0.       \tag{4}
\]

will be used only to exclude the separate two-site-support alternative
and hence force a three-site selector.  Thus Theorem 1.1 genuinely closes
the whole rank-at-most-one type-3 alternative under the **complete
six-site pair system**.  It does not close type 3 from one contracted
response row alone.

No row-basis change or physical colour-basis change occurs below.  The
fixed row covectors on \(C\), the annihilator derived in \(V_x^*\), and
the fixed physical axes in \(V_x\) remain distinct throughout.

## 2. The kernel and annihilator-plane identity

Fix \(x\in W\) and suppose, for contradiction, that

\[
                         \operatorname {rank}P_{\bar x}=1.      \tag{5}
\]

Put

\[
                         U=\ker P_{\bar x}.                     \tag{6}
\]

Then \(\dim U=2\).  If \(c\in U\) and \(P_x(c)=0\), then both projections
of \(P(c)\) vanish.  Injectivity of \(P\) therefore makes

\[
                         P_x|_U:U\longrightarrow V_x            \tag{7}
\]

injective.  Its image

\[
                         M=P_x(U)                                \tag{8}
\]

is a plane.  Choose a nonzero covector

\[
          \lambda\in V_x^*,\qquad \ker\lambda=M.                \tag{9}
\]

Let \(\epsilon_0,\epsilon_1,\epsilon_2\) be the coordinate covectors dual
to the **fixed** row basis \(f_0,f_1,f_2\), and set

\[
 \lambda_i=\lambda(e_i^{(x)}),\qquad
 X_i'=\bigotimes_{y\ne x}e_i^{(y)},\qquad
 Q=q^{[3]},\qquad
 T=\lambda\mathbin{\lrcorner}Q.                        \tag{10}
\]

Because degree six is the top degree on the six sites, \(Q\) is canonically
an element of

\[
                         V_x\otimes Z,
 \qquad Z=\bigotimes_{y\ne x}V_y.                       \tag{11}
\]

For \(c\in U\), the linear form \(P(c)\) is supported only at \(x\).
Put

\[
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[2]}\in Z.           \tag{12}
\]

Every term of \(s_jq^{[2]}\) containing an \(x\)-factor is killed when it
is multiplied by \(P_x(c)\).  Restriction to the other five sites is an
algebra homomorphism, so the surviving terms give the exact factorization

\[
                         P(c)s_jq^{[2]}=P_x(c)\otimes h_j.        \tag{13}
\]

Take the \(\epsilon_i(c)\)-linear combination of the three equations in
column \(j\) of (1), and contract the \(x\)-slot by \(\lambda\).  The term
in (13) vanishes because \(P_x(c)\in M=\ker\lambda\).  Hence

\[
 \boxed{
   (c^{\mathsf T}a)_jT
       =\epsilon_j(c)\lambda_jX_j'
       \qquad(c\in U,\ 0\le j\le2).}                  \tag{14}
\]

This is the only place where similarly labelled quantities meet:
\(\epsilon_j(c)\) is a coordinate in the row-index space \(C\), whereas
\(\lambda_j\) is the value of a covector in the physical space \(V_x^*\).
Equation (14) follows from the diagonal target in the fixed labels; it
does not identify the two spaces or normalize either basis.

## 3. A nonzero annihilator slice is impossible

Assume first that

\[
                              T\ne0.                    \tag{15}
\]

Define

\[
 J=\{j:\lambda_j\epsilon_j|_U\ne0\}.                  \tag{16}
\]

If \(j\in J\), choose \(c\in U\) for which
\(\epsilon_j(c)\lambda_j\ne0\).  Equation (14) makes \(T\) a nonzero
multiple of \(X_j'\).  The three tensors \(X_0',X_1',X_2'\) are linearly
independent, so

\[
                              |J|\le1.                  \tag{17}
\]

For \(j\notin J\), equation (14) and \(T\ne0\) give

\[
                 (c^{\mathsf T}a)_j=0
                 \qquad\text{for every }c\in U.       \tag{18}
\]

### 3.1 No active index

Suppose \(J=\varnothing\).  Combining (1) with \(c\in U\), then using
(13) and (18), gives in every column

\[
                 P_x(c)\otimes h_j=\epsilon_j(c)X_j.   \tag{19}
\]

A two-plane in \(C\) contains a vector with at least two nonzero fixed
coordinates.  Choose \(c\in U\) with
\(\epsilon_j(c)\epsilon_k(c)\ne0\) for distinct \(j,k\).  The \(j\)- and
\(k\)-instances of (19) are nonzero pure-tensor equalities.  The first
makes \(P_x(c)\) proportional to \(e_j^{(x)}\), while the second makes the
same nonzero vector proportional to \(e_k^{(x)}\), a contradiction.

### 3.2 One active index

It remains to suppose \(J=\{k\}\).  Since \(\epsilon_k|_U\ne0\), the
space

\[
                         U\cap\ker\epsilon_k            \tag{20}
\]

is a line.  For every inactive column, the same calculation as in (19)
still gives

\[
                 P_x(c)\otimes h_j=\epsilon_j(c)X_j.
\]

Take a nonzero \(c\) on the line (20).  If both coordinates outside
\(k\) were nonzero, their two inactive columns would give the same
contradiction as in Section 3.1.  Thus, for one \(d\ne k\), rescale \(c\)
so that

\[
                              c=f_d.                    \tag{21}
\]

Column \(d\) is inactive.  Equations (1), (13), and (18) therefore give

\[
             P_x(f_d)\otimes h_d=X_d.                  \tag{22}
\]

In particular \(h_d\ne0\) and

\[
                         P_x(f_d)\parallel e_d^{(x)}.   \tag{23}
\]

Choose \(c'\in U\) independent of \(f_d\).  Applying the same inactive
column \(d\) to \(c'\) gives

\[
             P_x(c')\otimes h_d=\epsilon_d(c')X_d.     \tag{24}
\]

The left side is nonzero because \(P_x|_U\) is injective and \(h_d\ne0\).
Thus \(\epsilon_d(c')\ne0\), and uniqueness of the factors of a nonzero
pure tensor makes \(P_x(c')\) proportional to \(e_d^{(x)}\).  This and
(23) make the images of the independent vectors \(c'\) and \(f_d\)
dependent, contradicting injectivity of \(P_x|_U\).

Both possibilities in (17) are impossible.  Consequently

\[
                              T=0.                     \tag{25}
\]

## 4. The two-row rectangle obstruction

The remaining case uses the following elementary tensor lemma.

**Lemma 4.1 (two-row rectangle obstruction).**  Let \(L\) be a
two-dimensional vector space.  Let \(p_u,p_v\) be one basis of \(L\), and
let \(e_u,e_v\) be another.  Let \(Y_u,Y_v\) be independent nonzero
vectors in a vector space \(Z\).  There are no tensors and scalars

\[
 Q\in L\otimes Z,\qquad h_u,h_v\in Z,\qquad
 \beta_{ij}\in\mathbb C\quad(i,j\in\{u,v\})           \tag{26}
\]

such that

\[
 \beta_{ij}Q+p_i\otimes h_j
      =\delta_{ij}e_i\otimes Y_i
      \qquad(i,j\in\{u,v\}).                           \tag{27}
\]

**Proof.**  If \(Q=0\), the two off-diagonal equations force
\(h_u=h_v=0\), contradicting either diagonal equation.  Hence \(Q\ne0\).

If both off-diagonal scalars \(\beta_{uv},\beta_{vu}\) are nonzero, the
off-diagonal equations put \(Q\) in both \(p_u\otimes Z\) and
\(p_v\otimes Z\).  These subspaces have zero intersection, a
contradiction.

Suppose exactly one is nonzero, say \(\beta_{uv}\ne0\).  Then the two
off-diagonal equations give

\[
 Q=p_u\otimes R,\qquad h_v=-\beta_{uv}R,\qquad h_u=0    \tag{28}
\]

for a nonzero \(R\in Z\).  The \((u,u)\) equation makes \(R\)
proportional to \(Y_u\).  The \((v,v)\) equation is

\[
 (\beta_{vv}p_u-\beta_{uv}p_v)\otimes R
                         =e_v\otimes Y_v,              \tag{29}
\]

so \(R\) is also proportional to \(Y_v\), contrary to their independence.
The case \(\beta_{vu}\ne0\) is symmetric.

Finally, if both off-diagonal scalars vanish, the off-diagonal equations
give \(h_u=h_v=0\).  The two diagonal equations then make the same nonzero
tensor \(Q\) proportional to both \(e_u\otimes Y_u\) and
\(e_v\otimes Y_v\), which is impossible.  \(\square\)

## 5. The zero annihilator slice is impossible

With \(T=0\), equation (14) becomes

\[
                 \epsilon_j(c)\lambda_j=0
                 \qquad(c\in U,\ 0\le j\le2).         \tag{30}
\]

Choose \(d\) with \(\lambda_d\ne0\).  Then
\(U\subseteq\ker\epsilon_d\), and equality holds because both spaces are
planes.  No other \(\lambda_j\) can be nonzero: otherwise the two-plane
\(U\) would lie in the one-dimensional intersection of two distinct
coordinate hyperplanes.  If

\[
                         \{u,v,d\}=\{0,1,2\},          \tag{31}
\]

then the fixed labels therefore give

\[
 \begin{aligned}
 U&=\operatorname {span}\{f_u,f_v\},
 &\lambda&\parallel(e_d^{(x)})^*,\\
 M&=P_x(U)=\ker\lambda,
 &M&=\operatorname {span}\{e_u^{(x)},e_v^{(x)}\}.
 \end{aligned}                                        \tag{32}
\]

This coordinate flag is forced by (30); it is not obtained by a row or
physical basis normalization.

Put

\[
                  \widehat p_u=P_x(f_u),\qquad
                  \widehat p_v=P_x(f_v).               \tag{33}
\]

They form a basis of \(M\), by injectivity of \(P_x|_U\).  Moreover,
\(T=(\lambda\otimes1)Q=0\).  In the top-degree identification (11), this
means

\[
                              Q\in M\otimes Z.          \tag{34}
\]

For \(i\in\{u,v\}\), the row \(p_i=P(f_i)\) is supported only at \(x\).
Restricting (1) to the literal physical rows and columns indexed by
\(u,v\), and using (13), gives

\[
 a_{ij}Q+\widehat p_i\otimes h_j
      =\delta_{ij}e_i^{(x)}\otimes X_i'
      \qquad(i,j\in\{u,v\}).                           \tag{35}
\]

Lemma 4.1 applies with

\[
 L=M,\qquad
 (p_u,p_v)=(\widehat p_u,\widehat p_v),\qquad
 (e_u,e_v)=(e_u^{(x)},e_v^{(x)}),\qquad
 (Y_u,Y_v)=(X_u',X_v').                                \tag{36}
\]

All its hypotheses are now literal: the two ordered pairs in \(M\) are
bases, and \(X_u',X_v'\) are independent.  This contradicts the assumed
rank-one case.

## 6. The zero-rank shore is impossible

Suppose instead that \(P_{\bar x}=0\).  Injectivity of \(P\) makes
\(p_0,p_1,p_2\), now all supported at \(x\), a basis of \(V_x\).  Put

\[
 Z=\bigotimes_{y\ne x}V_y,\qquad Q=q^{[3]},\qquad
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[2]}.
\]

The same site-square-zero factorization as in (13) gives, for every
\(i,j\),

\[
        a_{ij}Q+p_i\otimes h_j
             =\delta_{ij}e_i^{(x)}\otimes X_i'.
                                                               \tag{37}
\]

Fix a column \(j\), and let \(i,k\) be the other two indices.  If both
\(a_{ij}\) and \(a_{kj}\) are nonzero, the two off-diagonal equations put
\(Q\) in

\[
                         (p_i\otimes Z)\cap(p_k\otimes Z)=0.
\]

They then force \(h_j=0\), contradicting the diagonal equation.  If
exactly one of \(a_{ij},a_{kj}\) is nonzero, the off-diagonal equation
with zero scalar first gives \(h_j=0\); the other gives \(Q=0\), and the
diagonal again fails.  Consequently

\[
                         a_{ij}=a_{kj}=0.
\]

The off-diagonal equations now give \(h_j=0\), and the diagonal equation
becomes

\[
                         a_{jj}Q=e_j^{(x)}\otimes X_j'.          \tag{38}
\]

This conclusion holds in each of the three columns.  It makes the same
nonzero tensor \(Q\) proportional to all three linearly independent
tensors \(X_0,X_1,X_2\), a contradiction.  The rank-zero and rank-one
cases are both impossible, proving Theorem 1.1.  \(\square\)

## 7. Endpoint symmetry and closure of type 3

To apply Theorem 1.1 to the second endpoint, transpose the pair-index
rectangle:

\[
 \widetilde a_{ji}=a_{ij},\qquad
 \widetilde p_j=s_j,\qquad
 \widetilde s_i=p_i.                                  \tag{39}
\]

The right side of (1) becomes
\(\delta_{ji}X_i=\delta_{ji}X_j\), so (39) is a system of exactly the
same form.  This swaps the two row-index roles; it does not change any
physical colour axis.

Now suppose a pair covector \(K\) gives (4), and both endpoint stars are
injective.  Theorem 1.1 and its transposed form eliminate the
rank-at-most-one-away-from-one-site alternative at the two endpoints.
The other sparse alternative, support on at most two sites, is
incompatible with (4): every term in a three-edge matching would need
three distinct endpoint sites.  The Hall--Rado selector dichotomy
therefore yields

\[
 \boxed{\text{each injective endpoint star has a three-site physical
 selector.}}                                             \tag{40}
\]

The box is scoped to the complete pair system (1) together with the
nonnilpotence assumption (4).

## 8. Application to the rootless scalar-zero packet

For an off-diagonal curvature entry

\[
                 \alpha=a_{ab}\ne0,\qquad a\ne b,
 \qquad \tau=\operatorname {tr}a,                      \tag{41}
\]

the canonical scalar-zero covector is

\[
                         K_*=\tau E_{ab}-\alpha I.      \tag{42}
\]

It is invertible, has diagonal \(-\alpha I\), and contracts (1) to

\[
 r_*q^{[2]}=-\alpha(X_0+X_1+X_2),
 \qquad
 r_*=\sum_{i,j}(K_*)_{ij}p_i s_j.                      \tag{43}
\]

In the rootless branch, the clean-error gcd-one condition supplies

\[
                              r_*^{[3]}\ne0.            \tag{44}
\]

Equation (1) and endpoint injectivity already put this packet in the
type-3 scope of Theorem 1.1.  Equation (44) also removes the two-site
support alternative, so Section 7 routes both stars to selectors.  In
particular type 3 is genuinely empty here, not merely
reduced to the rank-one normal form
\(r_*=LM+E_x\).

The roles of the hypotheses in this argument are:

* the complete nine pair equations drive both the annihilator-plane
  argument and the zero-rank column argument;
* injectivity of the endpoint under study makes \(P_x|_U\) injective in
  rank one and makes \(p_0,p_1,p_2\) a local basis in rank zero; the
  opposite endpoint's injectivity is not used in either proof;
* \(\alpha=a_{ab}\ne0\) and invertibility of \(K_*\) are upstream facts
  producing the canonical scalar-zero packet and its three-channel target;
* rootlessness \(r_*^{[3]}\ne0\) excludes the two-site support
  alternative;
* one contracted equation such as (43), without the other eight physical
  pair equations, is outside the theorem and is compatible with the
  registered unary type-3 guard.

Accordingly this note closes the type-3 sparse branch of the six-site
rootless packet and routes both endpoints to the selector branch.  The
same conclusion is uniform by the next section.  It does not by itself
close the remaining selector/Macaulay or mixed apolar--Hall branch of the
global argument.

## 9. Uniform even-residual strengthening

The six-site exponent is not used in the annihilator-plane proof.

**Theorem 9.1 (uniform full-nine exceptional-shore closure).**  Let
\(h\ge1\), let \(|W|=2h\), and replace (1) by

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                  \tag{45}
\]

If \(P\) is injective, then

\[
                         \operatorname {rank}P_{\bar x}\ge2
                         \qquad(x\in W).               \tag{46}
\]

The transposed assertion holds for every injective second endpoint star
\(S\).

**Proof.**  Put

\[
 Q=q^{[h]},\qquad
 q_0=q|_{W\setminus\{x\}},\qquad
 h_j=(s_j|_{W\setminus\{x\}})q_0^{[h-1]}.             \tag{47}
\]

Top degree gives

\[
 Q\in V_x\otimes\bigotimes_{y\ne x}V_y,
 \qquad
 h_j\in\bigotimes_{y\ne x}V_y.                       \tag{48}
\]

If \(c\in\ker P_{\bar x}\), every term of
\(s_jq^{[h-1]}\) containing site \(x\) collides with \(P_x(c)\), while
restriction to the other \(2h-1\) sites gives

\[
 P(c)s_jq^{[h-1]}=P_x(c)\otimes h_j.                   \tag{49}
\]

This is exactly the factorization (13).  The contraction identity (14),
the \(T\ne0\) argument, the \(T=0\) coordinate rectangle, and the
rank-zero column argument use only (49), the two-dimensional row kernel,
and independence of \(X_0',X_1',X_2'\).  They are unchanged for every
\(h\ge1\).  Transposing the row-index rectangle proves the assertion for
\(S\).  \(\square\)

For a rootless scalar-zero packet on \(2h\) residual sites,

\[
 r_*q^{[h-1]}=-\alpha(X_0+X_1+X_2),
 \qquad r_*^{[h]}\ne0.                                 \tag{50}
\]

When \(h\ge3\), a star supported on at most two sites makes
\(r_*^{[h]}=0\), since the \(h\) response edges require \(h\) distinct
endpoints from that star.  The Hall--Rado dichotomy and Theorem 9.1
therefore give the uniform conclusion

\[
 \boxed{\text{for every }h\ge3,\text{ both injective endpoint stars in
 a rootless full-nine packet have three-site selectors.}}       \tag{51}
\]

The threshold in (51) is sharp for this last inference: at \(h=2\), two
response edges can use exactly two star-support sites.  This does not
affect the uniform rank statement (46).
