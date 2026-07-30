# A mixed Hall selector forces flag drift or cofactor leakage

## 1. Outcome

Work at the first curved boundary, with six residual sites. The full-nine
all-probe identity is

\[
 P(u)^{\mathsf T}H(Q(u))S(u)
   ={\cal D}(u)-\operatorname {haf}(Q(u))a.             \tag{1}
\]

There is a genuine fixed-label cross-word consequence of (1), but it is
not the hoped-for type-3 rectangle. Suppose that at a mixed coordinate
probe the two endpoint stars admit a *separating coordinate selector*: on
an ordered partition

\[
 W=X\sqcup Y,\qquad
 X=(x_0,x_1,x_2),\quad Y=(y_0,y_1,y_2),                 \tag{2}
\]

the literal scalar rows are

\[
 P_{x_i}=e_i^{\mathsf T},\quad S_{x_i}=0,\qquad
 P_{y_i}=0,\quad S_{y_i}=e_i^{\mathsf T}.              \tag{3}
\]

No row-index basis change is made in (3). If
\(\alpha=a_{ab}\ne0\), \(a\ne b\), then the canonical response has

\[
 \operatorname {haf}(R)=\operatorname {per}
   (\operatorname {tr}(a)E_{ab}-\alpha I)=(-\alpha)^3\ne0. \tag{4}
\]

Thus (3) is already a nonzero Hall chart. Let \(\xi\) be a first-order
probe variation which changes only the scalar physical edge
\(Q_{x_a y_b}\), to first order, and remains tangent to the
pure-target-zero locus. On the open set where the two selector matrices
remain invertible, put

\[
 C=A^{-\mathsf T}aB^{-1},                              \tag{5}
\]

where \(A\) and \(B\) are the moving selector-row matrices. There is an
exact one-scalar alternative

\[
 \boxed{\quad
 \Lambda_{ab}
   =F\bigl(\alpha^2-\xi C_{ab}\bigr),
 \qquad F=\operatorname {haf}(Q).
 \quad}                                                \tag{6}
\]

Here \(\Lambda_{ab}\) is the first-order leakage from the other star rows
into the selector-normalized \((a,b)\) cofactor. Consequently, on the
saturation \(F\alpha\ne0\), a horizontal fixed-label flag
\(\xi C_{ab}=0\) and a genuine cofactor rectangle
\(\Lambda_{ab}=0\) cannot coexist. If the separating selector persists,
so that there is no leakage, (6) becomes the Riccati law

\[
                         \xi C_{ab}=C_{ab}^2.           \tag{7}
\]

This is a strictly smaller cross-word kernel than the fourteen-dimensional
fixed-word apolar kernel: the Hall point must escape through one explicit
flag-connection scalar or one explicit leakage scalar.

The law is sharp. Section 5 gives fixed literal blocks \(q,p_i,s_j\) and
a one-parameter mixed probe line on which all nine entries of (1) hold,
the Hall permanent is nonzero, the leakage is zero, and (7) holds by a
nontrivial rotation of the fixed-label selector flag. Hence even a
positive-dimensional family of complete mixed proportionalities does not
force the coordinate rectangle. The missing input is synchronization
with the three pure target flags, not another fixed-word apolar statement.

## 2. Why an invertible selector is not a fixed-label rectangle

Let \(A,B\in\operatorname {GL}_3(\mathbb C)\). Normalizing the two
selector matrices sends the three literal target cells to

\[
 T_c=A^{-\mathsf T}E_{cc}B^{-1}
    =(A^{-\mathsf T}e_c)(B^{-\mathsf T}e_c)^{\mathsf T}. \tag{8}
\]

The following elementary flag test records the exact distinction between
an oblique selector and the coordinate flag used in the type-3 rectangle.

**Lemma 2.1 (fixed-label flag test).** One has

\[
 A^{-\mathsf T}\operatorname {Diag}_3 B^{-1}
       =\operatorname {Diag}_3                         \tag{9}
\]

if and only if \(A\) and \(B\) are monomial matrices with the same
underlying permutation.

**Proof.** If (9) holds, every rank-one tensor \(T_c\) in (8) lies in the
diagonal subspace. A rank-one diagonal matrix has at most one nonzero
diagonal cell. Since the three \(T_c\) are independent, their cells are
distinct. Thus each column \(A^{-\mathsf T}e_c\) and the corresponding
column \(B^{-\mathsf T}e_c\) lie on the same coordinate axis, and the
three axes occur once each. This says exactly that the two matrices are
monomial with the same permutation. The converse is immediate.
\(\square\)

At one mixed word, the target matrix is zero, so (1) sees only the oblique
left-right orbit of \(a\); it cannot impose (9). At the three constant
words, (8) is evaluated using three generally different pairs

\[
 (A_{0^6},B_{0^6}),\quad(A_{1^6},B_{1^6}),\quad
 (A_{2^6},B_{2^6}).                                    \tag{10}
\]

The fact that the three unnormalized targets are \(E_{00},E_{11},E_{22}\)
does not identify these six moving flags. Applying an independent row
normalization at each word would replace the fixed direct block \(a\) by
three different matrices and is therefore not a physical argument.

## 3. The selector-normalized first jet

Let

\[
 F(u)=\operatorname {haf}(Q(u)),\qquad
 M(u)=P(u)^{\mathsf T}H(Q(u))S(u).                     \tag{11}
\]

Fix a mixed coordinate probe \(u\) satisfying (3). Near \(u\), let
\(A\) be the matrix whose \(i\)-th row is \(P_{x_i}\), and let \(B\) be
the matrix whose \(j\)-th row is \(S_{y_j}\). Their determinants are one
at \(u\), so the selector-normalized matrix

\[
 \widehat H=A^{-\mathsf T}MB^{-1}                      \tag{12}
\]

is regular on a neighbourhood of \(u\). Notice that \(\widehat H\) is
not being declared to be the physical cross-cofactor matrix away from
\(u\). At the base point, however, the shore separation in (3) gives

\[
                  \widehat H_{ij}(u)=H(Q(u))_{x_i y_j}. \tag{13}
\]

Normalize (1) in the same way:

\[
 \widehat H=\widehat D-FC,\qquad
 \widehat D=A^{-\mathsf T}{\cal D}B^{-1},\qquad
 C=A^{-\mathsf T}aB^{-1}.                              \tag{14}
\]

Let \(e=x_a y_b\), where \(\alpha=a_{ab}\ne0\). A **pure-horizontal
own-edge lift** at \(u\) is a tangent vector \(\xi\) in the probe space
such that

\[
 dQ_f(\xi)=\delta_{ef}\quad(f\in\tbinom W2),
 \qquad dG_c(\xi)=0\quad(c=0,1,2).                     \tag{15}
\]

The terminology refers only to the target monomials: (15) does not freeze
the endpoint stars. It is an exact Jacobian incidence condition on the
fixed physical block map

\[
 u\longmapsto (Q(u),G_0(u),G_1(u),G_2(u)).             \tag{16}
\]

Define the leakage scalar

\[
 \Lambda_{ab}:=
   \xi\widehat H_{ab}-
   \xi H(Q)_{x_a y_b}.                                 \tag{17}
\]

Since a cohafnian never uses the deleted edge itself, (15) gives

\[
                       \xi H(Q)_{x_a y_b}=0.           \tag{18}
\]

Thus \(\Lambda_{ab}\) measures exactly the first-order failure of the
selector-normalized entry to remain the literal physical cofactor. It
contains the newly appearing opposite-shore rows and the corresponding
normalization terms; it is not a generic rank defect.

**Proposition 3.1 (cross-word Riccati--leakage identity).** Under
(3), (15), and \(\alpha=a_{ab}\ne0\), equation (6) holds.

**Proof.** At the mixed base point, \({\cal D}=0\), \(A=B=I\), and hence
\(C=a\). The \((a,b)\)-entry of (14), together with (13), is

\[
                  H(Q)_{x_a y_b}=-F\alpha.             \tag{19}
\]

The target derivative in (14) vanishes by (15). Also

\[
 \xi F=\sum_f H(Q)_f\,dQ_f(\xi)=H(Q)_{x_a y_b}.        \tag{20}
\]

Differentiating the \((a,b)\)-entry of (14), then using (18)--(20), gives

\[
\begin{aligned}
 \Lambda_{ab}
 &=-(\xi F)\alpha-F\,\xi C_{ab}\\
 &=F\alpha^2-F\,\xi C_{ab},
\end{aligned}
\]

which is (6). \(\square\)

At the base coordinate flag,

\[
 \xi C=-(\xi A)^{\mathsf T}a-a(\xi B).                 \tag{21}
\]

Consequently (6) is also the explicit connection identity

\[
 \Lambda_{ab}=F\left(
  \alpha^2+\bigl((\xi A)^{\mathsf T}a+a(\xi B)\bigr)_{ab}
                     \right).                         \tag{22}
\]

If the shore separation persists to first order, then (12) remains the
physical cross-cofactor matrix, so \(\Lambda_{ab}=0\). Equations
(6), (19) then give (7). In contrast, if the fixed coordinate flag is
horizontal, \(\xi A=\xi B=0\), then \(\xi C_{ab}=0\) and (6) forces the
nonzero leakage \(\Lambda_{ab}=F\alpha^2\) on the open set
\(F\alpha\ne0\).

## 4. The Hall permanent is literal on this chart

Let

\[
 K_*=\operatorname {tr}(a)E_{ab}-\alpha I.             \tag{23}
\]

At the base point (3), the response has no within-shore edges, and its
oriented \(X\)-to-\(Y\) matrix is exactly \(K_*\). The only nonzero
permutation product of \(K_*\) is its diagonal product. Indeed, a
permutation using the sole off-diagonal cell \((a,b)\) cannot fill column
\(a\), because every other off-diagonal cell is zero. Therefore

\[
 \operatorname {haf}(R_u)=\operatorname {per}(K_*)
                    =(-\alpha)^3\ne0.                 \tag{24}
\]

This is stronger than a support-only Hall certificate. Proposition 3.1
therefore says that a literal nonzero Hall selector on the saturated
\(F\ne0\) chart cannot have the type-3 behaviour “fixed coordinate flag
and no rectangle leakage.” One of those two assertions must fail in the
precise amount (6).

## 5. A literal-block mixed-line guard

The flag-drift alternative in (6) is real even when all nine mixed scalar
identities hold on a positive-dimensional probe family.

Specialize the distinguished label pair to \((a,b)=(0,1)\), let
\(\gamma\in\mathbb C^*\), and use the six sites in (2). Give every local
space its fixed physical basis
\(e_0,e_1,e_2\), with dual basis \(e_0^*,e_1^*,e_2^*\). Use the probe
line

\[
\begin{array}{c|cccccc}
z&x_0&x_1&x_2&y_0&y_1&y_2\\ \hline
u_z(t)&e_0+t e_1&e_0&e_1&e_2&e_0&e_1
\end{array}                                             \tag{25}
\]

Every pure target monomial vanishes identically on this line:

\[
                         G_0=G_1=G_2=0.                \tag{26}
\]

Take the only nonzero endpoint-star components to be

\[
\begin{aligned}
 p_{0,x_0}&=e_0^*+\gamma^{-1}e_1^*,&
 p_{1,x_1}&=e_0^*,&p_{2,x_2}&=e_1^*,\\
 s_{0,y_0}&=e_2^*,&s_{1,y_1}&=e_0^*,&s_{2,y_2}&=e_1^*.
\end{aligned}                                          \tag{27}
\]

All other \(p\)- and \(s\)-components are zero. Thus, on (25),

\[
 A(t)=\operatorname {diag}(d,1,1),\qquad B(t)=I,\qquad
 d=\frac{\gamma+t}{\gamma}.                            \tag{28}
\]

Take the only nonzero internal blocks, in the displayed endpoint order,
to be

\[
\begin{aligned}
 q_{x_0y_1}&=(\gamma e_0^*+e_1^*)\otimes e_0^*,\\
 q_{x_1y_0}&=e_0^*\otimes e_2^*,\\
 q_{x_2y_2}&=e_1^*\otimes e_1^*.
\end{aligned}                                          \tag{29}
\]

Reverse endpoint order uses the transposed block. These are fixed
bilinear blocks; no scalar edge is being varied independently of its
source. On (25), their scalar matrix consists of the single perfect
matching

\[
 x_0y_1\mid x_1y_0\mid x_2y_2
       \quad\text{with weights}\quad \gamma+t,1,1.     \tag{30}
\]

Consequently

\[
 F=\gamma+t,\qquad
 H_{x_0y_1}=1,\quad H_{x_1y_0}=F,\quad H_{x_2y_2}=F,   \tag{31}
\]

and every other cohafnian is zero. Finally, take the fixed direct block

\[
 a=
 \begin{pmatrix}
 0&-\gamma^{-1}&0\\
 -1&0&0\\
 0&0&-1
 \end{pmatrix}.                                       \tag{32}
\]

Direct multiplication gives

\[
 P^{\mathsf T}HS=
 \begin{pmatrix}
 0&F/\gamma&0\\
 F&0&0\\
 0&0&F
 \end{pmatrix}
 =-Fa.                                                 \tag{33}
\]

Together with (26), this is every one of the nine scalar entries of (1),
for every \(t\).

Here \(\alpha=-\gamma^{-1}\), \(\operatorname {tr}(a)=-1\), and

\[
 K_*=-E_{01}+\gamma^{-1}I.                             \tag{34}
\]

The oriented response matrix is

\[
 A(t)K_*=
 \begin{pmatrix}
 d/\gamma&-d&0\\
 0&1/\gamma&0\\
 0&0&1/\gamma
 \end{pmatrix},                                       \tag{35}
\]

so

\[
 \operatorname {haf}(R(t))
   =\operatorname {per}(A(t)K_*)
   =\frac{\gamma+t}{\gamma^4}\ne0
 \qquad(\gamma+t\ne0).                                \tag{36}
\]

The mixed tangent contraction also vanishes literally: the two common
nonzero cells of \(H\) and \(A(t)K_*\) contribute
\(-d+F/\gamma=0\).

The selector remains separating, hence \(\Lambda_{01}=0\). On the
other hand,

\[
 C_{01}(t)=(A(t)^{-\mathsf T}a)_{01}
          =-\frac1{\gamma+t},
 \qquad
 \frac{dC_{01}}{dQ_{x_0y_1}}=C_{01}^2.                \tag{37}
\]

Thus the guard realizes the Riccati escape in (7) exactly. It retains
fixed literal blocks, endpoint order, both rank-three endpoint stars, all
nine mixed proportionality entries, complex signs, and a nonzero Hall
permanent. It is deliberately only a mixed probe-line packet. It does
not satisfy (1) on all probes or at the three constant words and is not a
ternary source.

## 6. The exact remaining incidence

The uniform full-nine type-3 closure supplies a three-site selector for
each endpoint star in the nonnilpotent scalar-zero packet. It does not
supply any of the following stronger statements used above:

1. the two selectors are disjoint and cover the six residual sites;
2. they annihilate the opposite endpoint star as in (3);
3. their oblique row flags agree with the fixed physical labels;
4. the block-evaluation Jacobian has the own-edge lift (15); or
5. the selector flag and physical cofactor remain synchronized to first
   order.

These are incidence assertions, not generic rank assertions. On a
first-jet chart where (3) and (15) do hold, Proposition 3.1 reduces the
last item to one exact scalar. If \(I_{9}^{(1)}\) denotes the first-jet
ideal of (1), including the linear equations in (3), (15), and the inverse
selector chart, then (6) gives the finite saturation consequence

\[
 1\in
 \bigl(I_{9}^{(1)}+\langle\Lambda_{ab},\xi C_{ab}\rangle\bigr)
       :(F\alpha)^\infty.                              \tag{38}
\]

Indeed, modulo the two added scalars, (6) is \(F\alpha^2=0\).

Thus a type-3-style fixed-coordinate rectangle would close this saturated
Hall stratum immediately, but endpoint selectors alone do not produce it.
The smallest live cross-word alternatives are now explicit:

\[
 \boxed{
 \text{overlapping/oblique selectors, no own-edge lift, or the exact
 flag-drift--leakage relation (6).}}
                                                               \tag{39}
\]

The mixed-line guard proves that the last alternative cannot be deleted by
using all nine mixed proportionalities, shared multilinear block
provenance, or the Hall permanent alone. A further argument must transport
the three constant-word flags into the same selector chart, or derive an
equivalent source-variable condition killing both \(\xi C_{ab}\) and
\(\Lambda_{ab}\). This is strictly narrower than asking again for the
full mixed-hafnian vanishing theorem.
