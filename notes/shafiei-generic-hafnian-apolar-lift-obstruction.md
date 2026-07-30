# Shafiei's generic-hafnian apolar ideal does not lift the mixed packet

## 1. Outcome

Shafiei's theorem on the apolar ideal of the generic hafnian is relevant,
but it does **not** close the mixed scalar-zero branch.

For the generic \(6\times6\) zero-diagonal symmetric hafnian \(F\), the
mixed identity

\[
                 D F_Q(R)=0                                      \tag{1}
\]

is initially only the pointwise statement

\[
                         (L_R\mathbin\circ F)(Q)=0.
\]

It can legitimately be homogenized into membership of one cubic
constant-coefficient operator in the apolar ideal.  However, Shafiei's
quadratic generators then reduce that membership to exactly the one scalar
equation (1).  They do not imply that \(L_R\) is a universal annihilator,
or that the numerical edge entries of \(Q\) or \(R\) obey edge-square,
incident-edge, or balanced-four-site relations.

More precisely, if \(L_Q,L_R\) are the linear differential forms attached
to the two edge matrices and \(I=\operatorname{Ann}(F)\), then

\[
 \boxed{
 \overline{\frac12L_Q^2L_R}
       =D F_Q(R)\,
        \overline{Y_{01}Y_{23}Y_{45}}
       \quad\hbox{in }\mathbb C[Y_{xy}]/I.}             \tag{2}
\]

Thus (1) is equivalent to

\[
                       \frac12L_Q^2L_R\in I_3,           \tag{3}
\]

and (3) contains no additional support information.  In fact, (2) remains
true after extending scalars from \(\mathbb C\) to an arbitrary commutative
\(\mathbb C\)-algebra.  Thus the inverse image of \(I_3\) in the family of
operators \(\frac12L_Q^2L_R\) is scheme-theoretically the single equation
\(D F_Q(R)=0\), even when \(Q\) and \(R\) vary polynomially.  The Hilbert
function

\[
                         (1,15,15,1)                     \tag{4}
\]

makes the obstruction transparent: \(I_3\) is merely the kernel of the
one-dimensional top apolar pairing.

There are two separate failures of the hoped-for lift.

1. Shafiei classifies constant-coefficient differential operators that
   annihilate the generic hafnian **identically**.  The physical equation
   says that the quadratic polynomial \(L_{R_\omega}\circ F\) vanishes at
   one specialized \(Q_\omega\), in a direction \(R_\omega\) depending on
   the same word and the same local covectors.  Homogenizing with two
   copies of \(L_{Q_\omega}\) reaches the one-dimensional socle and loses
   the lower-degree information one wanted to lift.
2. The all-word identities assemble into a pulled-back Jacobian identity
   with a nonzero pure-word right side.  They do not give a homomorphism
   from the generic hafnian's apolar algebra to the physical tensor
   algebra.

Section 6 gives an exact six-site scalar packet satisfying the entire
selected-mixed-word interface

\[
 P^TH(Q)S=-\operatorname{haf}(Q)a,
 \qquad \operatorname{haf}(R)\ne0,
 \qquad D F_Q(R)=0,                                    \tag{5}
\]

with both scalarized stars of rank three, invertible \(K_*\), and a
nonzero Hall-certified permanent.  Its response edges violate a balanced
four-site generator under the coefficient-preserving site-marker lift.
It also has \(\overline{L_QL_R}\ne0\) although
\(\overline{L_Q^2L_R}=0\).  Hence even the full nine rows at one word do
not repair the apolar argument.  Only genuinely cross-word information
can still do so.

This is a no-gain result for this literature route, not a counterexample to
the global physical system and not a closure of the conjecture.

## 2. The exact literature theorem and conventions

The primary source is
[Shafiei, *Apolarity for determinants and permanents of generic matrices*,
arXiv:1212.0515v2, Theorem 4.14](https://arxiv.org/abs/1212.0515v2).
The paper works over a field of characteristic zero or characteristic
\(p>2\), using Macaulay contraction.  It notes that contraction may be
replaced by ordinary constant-coefficient differentiation in
characteristic zero, or when the characteristic exceeds the degree of the
form.  Everything below is over \(\mathbb C\), so there is no characteristic
or divided-factor ambiguity.

Let

\[
 E=\{\{x,y\}:0\le x<y\le5\},
 \quad
 \mathcal R=\mathbb C[X_e:e\in E],
 \quad
 \mathcal T=\mathbb C[Y_e:e\in E],                    \tag{6}
\]

and let \(\mathcal T\) act on \(\mathcal R\) by contraction.  The generic
zero-diagonal symmetric hafnian is

\[
 F(X)=\operatorname{haf}(X)
     =\sum_{M\in\operatorname{PM}(6)}\prod_{e\in M}X_e. \tag{7}
\]

Shafiei states the theorem for a generic symmetric matrix.  Its diagonal
variables do not occur in the hafnian, so their dual variables are linear
annihilators; the proof then restricts to the generic zero-diagonal
symmetric matrix.  In the edge-only ring (6), the degree-two generators
inherited from the Pfaffian proof are the following.

* \(Y_{xy}^2\) for every edge \(xy\);
* \(Y_{xy}Y_{xz}\) for every pair of incident edges;
* for each four distinct vertices \(i,j,k,l\), two independent differences
  among

  \[
       Y_{ij}Y_{kl},\qquad Y_{ik}Y_{jl},\qquad
       Y_{il}Y_{jk}.                                   \tag{8}
  \]

For example, one may take

\[
 Y_{ij}Y_{kl}-Y_{ik}Y_{jl},
 \qquad
 Y_{ij}Y_{kl}-Y_{il}Y_{jk}.                            \tag{9}
\]

The signs in (9) can be checked directly, without importing a Pfaffian
sign convention: differentiating by any of the three two-edge matchings on
the same four vertices leaves the same hafnian on the complementary
vertices.  Shafiei's Theorem 4.14 says that the Pfaffian argument, with
Pfaffians replaced by hafnians, proves generation in degree two.

The theorem says that these quadrics generate

\[
                         I=\operatorname{Ann}(F).       \tag{10}
\]

For six vertices, the apolar Hilbert function is

\[
 \dim(\mathcal T/I)_d=\binom{6}{2d},
 \qquad 0\le d\le3,                                   \tag{11}
\]

which is (4).  This dimension statement can also be verified directly.
The degree-\(d\) value is the dimension of the space of all degree-\(d\)
contractions of \(F\).  First derivatives are the fifteen four-vertex
subhafnians; their monomial supports are disjoint because a two-edge
matching determines its four-vertex support.  Second derivatives span the
fifteen distinct edge variables, and third derivatives span the constants.
Thus the dimensions are \(1,15,15,1\).  Concretely, in degree two every
operator product on four distinct vertices is identified with the other
two perfect matchings on those vertices, while all products with a
repeated vertex vanish.

## 3. Exact translation of the physical tangent equation

Let \(B\) be a commutative \(\mathbb C\)-algebra.  For a symmetric
zero-diagonal edge matrix \(V=(V_e)\) with entries in \(B\), define

\[
                         L_V=\sum_{e\in E}V_eY_e.       \tag{12}
\]

For a \(B\)-valued matrix \(Q\), let

\[
 H(Q)_{xy}=\operatorname{haf}
               (Q_{\{0,\ldots,5\}\setminus\{x,y\}}).  \tag{13}
\]

Then the polarization of the directional derivative used in the
scalar-zero packet is

\[
 D F_Q(R)=\sum_{x<y}R_{xy}H(Q)_{xy}.                   \tag{14}
\]

For numerical \(Q,R\), this is exactly
\((L_R\mathbin\circ F)(Q)\).

Because every monomial of \(F\) is squarefree, Macaulay contraction and
ordinary differentiation agree on the operators that occur here.  In the
expansion of \(L_Q^2L_R\), the two \(Q\)-edges can occur in two orders.
Therefore the exact normalization is

\[
             \left(\frac12L_Q^2L_R\right)\mathbin\circ F
                       =D F_Q(R).                      \tag{15}
\]

This proves the equivalence between (1) and (3).  It is important that
this uses a **degree-three** operator.  The first-order operator \(L_R\)
does not annihilate \(F\) identically: (4) gives \(I_1=0\), so no nonzero
constant direction does.

### Proposition 3.1 (universal top-apolar no-gain lemma)

Put \(A=\mathcal T/I\) and

\[
                 \mu=\overline{Y_{01}Y_{23}Y_{45}}\in A_3.
\]

For every commutative \(\mathbb C\)-algebra \(B\) and every two
\(B\)-valued edge matrices \(Q,R\), one has

\[
 \overline{\frac12L_Q^2L_R}
       =D F_Q(R)\,\mu\qquad\text{in }A_3\otimes_{\mathbb C}B.  \tag{15a}
\]

Write \(I_B=I\cdot B[Y_e:e\in E]\).  Then

\[
 \frac12L_Q^2L_R\in (I_B)_3
       \quad\Longleftrightarrow\quad D F_Q(R)=0\text{ in }B. \tag{15b}
\]

Consequently Shafiei's quadratic generation gives no equation beyond
\(D F_Q(R)=0\), even scheme-theoretically and even for polynomially varying
families \(Q,R\).

**Proof.**  Expand \(\frac12L_Q^2L_R\) modulo \(I\).  An operator monomial
with a repeated edge is divisible by an edge square.  An operator monomial
whose edges share a vertex is divisible by an incident-edge generator.
Hence only triples of pairwise disjoint edges survive, and these are the
perfect matchings of the six vertices.

For a perfect matching \(M\), choose its \(R\)-edge \(e\).  The factor
\(\frac12\) cancels the two orders of the other two \(Q\)-edges, so the
coefficient is exactly

\[
                         R_e\prod_{f\in M\setminus\{e\}}Q_f.    \tag{16}
\]

The balanced four-site differences connect all perfect matchings by
four-vertex flips: if a target matching edge \(ij\) is absent, the two
current matching edges incident to \(i,j\) can be flipped to insert \(ij\),
after which one continues on the remaining vertices.  Thus every
surviving operator monomial has the same class

\[
                         \mu=\overline{Y_{01}Y_{23}Y_{45}}.     \tag{17}
\]

Summing (16) over \(e\in M\) and over all \(M\) gives (2), by (14).
Finally \(\mu\ne0\), since \(\mu\circ F=1\), and (4) says that \(A_3\) is
the one-dimensional space \(\mathbb C\mu\).  Hence after scalar extension
\(A_3\otimes B=B\mu\), so a coefficient times \(\mu\) is zero if and only
if that coefficient is zero in \(B\).  This proves (15a), (15b), and (2).
\(\square\)

Return now to numerical matrices.  There is also an exact degree-lowering
obstruction.  For a four-set \(S\), let \(\nu_S\in A_2\) be the common
class of its three two-edge matchings.  Multiplication by
\(\overline{L_Q}\) is

\[
 m_Q:A_2\longrightarrow A_3,
 \qquad m_Q(\nu_S)=Q_{S^c}\mu.                         \tag{17a}
\]

Indeed, the only edge disjoint from the four vertices of \(S\) is the
complementary edge \(S^c\); every other product is an incident-edge
annihilator.  The fifteen classes \(\nu_S\) form a basis by (11).
If \(Q\ne0\), this map has rank one and a fourteen-dimensional kernel.
The tangent equation says only

\[
 \overline{L_QL_R}\in\ker m_Q,                         \tag{17b}
\]

because \(m_Q(\overline{L_QL_R})=\overline{L_Q^2L_R}\).
It does **not** say \(L_QL_R\in I_2\).  Thus the tempting step from the
cubic membership back to a quadratic annihilator would require a new
kernel-exclusion lemma; it is not a consequence of quadratic generation.

The proof also exposes the cancellation mechanism.  Shafiei's relations
identify different matching operator monomials; they do not make their
individual coefficients zero.  The scalar sum of those coefficients can
vanish while a selected response matching, and hence a Hall permanent,
remains nonzero.

## 4. Why the generators do not become response-edge equations

Because \(I\) is generated by quadrics, a cubic in \(I_3\) can be written
as a sum of those quadrics times linear forms.  That ideal-membership
certificate is an identity in the operator variables \(Y_e\); it does not
say that the coefficients \(Q_e,R_e\) are zeros of the same quadrics.  To
turn the generators into response-edge equations one needs extra data,
such as an assignment of operator variables to response elements.

There is a precise criterion for this stronger interpretation.  Let
\(\mathcal A\) be a commutative \(\mathbb C\)-algebra and assign an element
\(\rho_{xy}\in\mathcal A\) to every edge.  The assignment extends to an
algebra map

\[
                    \mathcal T/I\longrightarrow\mathcal A      \tag{18}
\]

if and only if

\[
\begin{aligned}
 \rho_{xy}^2&=0,\\
 \rho_{xy}\rho_{xz}&=0,\\
 \rho_{ij}\rho_{kl}
   &=\rho_{ik}\rho_{jl}
    =\rho_{il}\rho_{jk}
       \quad(i,j,k,l\text{ distinct}).                 \tag{19}
\end{aligned}
\]

This follows immediately from the generating theorem.  But the physical
tangent identity does not assert the existence of (18).

* Sending \(Y_{xy}\) to the scalar \(R_{xy}\in\mathbb C\) would make the
  first line of (19) force every \(R_{xy}=0\), contradicting
  \(\operatorname{haf}(R)\ne0\).
* The coefficient-preserving site-marker attempt uses the site-square-zero
  algebra

  \[
     \mathcal A_W=\mathbb C[z_0,\ldots,z_5]/(z_0^2,\ldots,z_5^2),
     \qquad
     \rho_{xy}=R_{xy}z_xz_y.                            \tag{20}
  \]

  The first two lines of (19) are then automatic, but the third becomes

  \[
     R_{ij}R_{kl}=R_{ik}R_{jl}=R_{il}R_{jk}              \tag{21}
  \]

  on every four-set.  Neither tangent apolarity nor the full-nine
  cohafnian identity states (21).

Even (21), if supplied separately, is not intrinsically incompatible with
a Hall certificate: the complete assignment \(R_{xy}=1\) satisfies all
balanced products and has hafnian \(15\).  It can be oriented as
\(R_{xy}=B_{xy}+B_{yx}\) with \(B_{xy}=1/2\); every balanced \(3\times3\)
submatrix then has permanent \(3!/2^3=3/4\ne0\).  Thus an apolar-algebra
map would be a genuine additional lifting lemma, but would not by itself
be the desired contradiction.  Any closure would still have to use the
physical common-block and cross-word structure.

## 5. The all-word system is a pulled-back Jacobian identity

The distinction remains after polarizing all words at once.  We use the
notation and the full-nine identity from the
[primary tangent note](curved-scalar-zero-tangent-apolar-hall-alternative.md),
whose constants and endpoint order were checked in its
[independent audit](curved-scalar-zero-tangent-apolar-hall-alternative-independent-audit.md).
Introduce a local probe

\[
                     u_x=(u_{x,0},u_{x,1},u_{x,2})       \tag{22}
\]

at every site.  Evaluate the fixed physical blocks and stars on these
probes:

\[
\begin{aligned}
 Q(u)_{xy}&=q_{xy}(u_x,u_y),\\
 P(u)_{x,i}&=p_{i,x}(u_x),\\
 S(u)_{x,j}&=s_{j,x}(u_x),\\
 R(u)_{xy}&=P(u)_xK_*S(u)_y^T+P(u)_yK_*S(u)_x^T.        \tag{23}
\end{aligned}
\]

Set

\[
 G_c(u)=\prod_{x=0}^5u_{x,c},
 \qquad
 \mathcal D(u)=\operatorname{diag}(G_0(u),G_1(u),G_2(u)). \tag{24}
\]

The complete nine tensor rows assemble exactly into

\[
 P(u)^TH(Q(u))S(u)
       =\mathcal D(u)-F(Q(u))a.                         \tag{25}
\]

Indeed, each entry on both sides is linear in each individual probe
\(u_x\).  Its values on the \(3^6\) coordinate probes are exactly the
wordwise full-nine identities, and those values determine a multilinear
form.  Thus (25) is an identity in
\(\mathbb C[u_{x,c}:0\leq x\leq5,\ 0\leq c\leq2]\), not an interpolation
assumption.

Fix \(a\ne b\), put \(\alpha=a_{ab}\ne0\) and
\(\tau=\operatorname{tr}a\), and contract (25) with

\[
 K_*=\tau E_{ab}-\alpha I,
 \qquad
 \sum_{i,j}(K_*)_{ij}a_{ij}=0,                         \tag{26}
\]

gives

\[
 \boxed{
 D F_{Q(u)}(R(u))
       =-\alpha\bigl(G_0(u)+G_1(u)+G_2(u)\bigr).}       \tag{27}
\]

A word \(\omega\) is the coordinate probe \(u_x=e_{\omega_x}\).  The
right side of (27) is zero at a mixed word and is \(-\alpha\) at a constant
word.  Applying Proposition 3.1 over the probe polynomial ring gives the
more explicit family identity

\[
 \overline{\frac12L_{Q(u)}^2L_{R(u)}}
 =-\alpha\bigl(G_0(u)+G_1(u)+G_2(u)\bigr)\mu.           \tag{27a}
\]

The right side is not the zero polynomial.  Thus the mixed coordinate
probes do not imply that \(L_{R(u)}\circ F\) annihilates \(F\) identically,
and they do not even put the homogenized family in the extended apolar
ideal over the full probe ring.  After quotienting the probe ring by
\(G_0+G_1+G_2\), (15b) says that its resulting apolar membership is
precisely (27), with no extra equations.

Write

\[
 \Phi_q:u\longmapsto Q(u)\in\mathbb A^{15}.             \tag{28}
\]

No dominance statement for \(\Phi_q\) is part of the physical hypotheses.
More importantly, dominance would not by itself repair the argument:
\(R(u)\) varies with \(u\), need not descend to a function of \(Q(u)\), and
(27) has a nonzero right side.  Precisely, \(R(u)\) is a section of the
pullback by \(\Phi_q\) of the ambient tangent bundle of
\(\mathbb A^{15}\).  On the hypersurface

\[
                         G_0+G_1+G_2=0                  \tag{29}
\]

this section is killed by the pulled-back differential \(dF\).  It is not
necessarily a vector field on the image of \(\Phi_q\), because it need not
be constant on fibres of \(\Phi_q\).  The resulting problem is therefore a
syzygy in the pulled-back hafnian Jacobian module, with the pure polynomial
\(G_0+G_1+G_2\) retained.  It is not the constant-coefficient apolar-ideal
problem solved by Theorem 4.14.

## 6. Exact selected-word counterpacket

The following exact packet shows that no contradiction can be extracted
from (5) at one mixed word, even with full scalar star rank and the
physical definition of \(K_*\).

Take

\[
                         Q_{xy}=1\quad(x\ne y).          \tag{30}
\]

There are fifteen perfect matchings of six vertices, and every four-site
all-one hafnian has three matchings.  Hence

\[
                         F(Q)=15,
 \qquad
                         H(Q)_{xy}=3\quad(x\ne y).       \tag{31}
\]

Let \(e_0,e_1,e_2\) be the standard rows of \(\mathbb C^3\), and define the
six rows of the scalarized endpoint stars by

\[
\begin{array}{c|cccccc}
 x&0&1&2&3&4&5\\ \hline
 P_x&e_0&0&e_1&0&e_2&0\\
 S_x&0&e_0&0&e_1&0&-2e_2.
\end{array}                                             \tag{32}
\]

Both \(P\) and \(S\) have rank three.  Direct multiplication gives

\[
 M:=P^TH(Q)S
   =\begin{pmatrix}
       3&3&-6\\
       3&3&-6\\
       3&3&-6
     \end{pmatrix}.                                     \tag{33}
\]

Put

\[
 a=-\frac1{15}M
   =\begin{pmatrix}
      -1/5&-1/5&2/5\\
      -1/5&-1/5&2/5\\
      -1/5&-1/5&2/5
     \end{pmatrix}.                                     \tag{34}
\]

Then

\[
                         M=-F(Q)a,                       \tag{35}
\]

which is the complete nine-entry mixed cohafnian identity.  Moreover

\[
 \tau=\operatorname{tr}a=0,
 \qquad
 \alpha=a_{01}=-\frac15,
 \qquad
 K_*=\tau E_{01}-\alpha I=\frac15I.                    \tag{36}
\]

Thus \(K_*\) is invertible and the response defined in (23), specialized
at this word, has exactly three nonzero edges:

\[
                  R_{01}=\frac15,
 \qquad R_{23}=\frac15,
 \qquad R_{45}=-\frac25.                               \tag{37}
\]

Equations (31) and (37) give

\[
 D F_Q(R)=3\left(\frac15+\frac15-\frac25\right)=0,
 \qquad
 \operatorname{haf}(R)
       =\frac15\frac15\left(-\frac25\right)
       =-\frac2{125}\ne0.                              \tag{38}
\]

The lost lower-degree class is visibly nonzero.  In the
\(\nu_{\{0,1,2,3\}}\) coordinate of \(A_2\), one has

\[
\begin{aligned}
 [\,\overline{L_QL_R}\,]_{\nu_{\{0,1,2,3\}}}
 &=Q_{01}R_{23}+R_{01}Q_{23}
   +Q_{02}R_{13}+R_{02}Q_{13}\\
 &\qquad+Q_{03}R_{12}+R_{03}Q_{12}
   =\frac25\ne0.                                      \tag{38a}
\end{aligned}
\]

Thus this physical-format packet lies nontrivially in the
fourteen-dimensional kernel (17b); it explicitly refutes any wordwise
descent from the cubic annihilator to \(L_QL_R\in I_2\).

For the balanced partition

\[
                      A=\{0,2,4\},
 \qquad B=\{1,3,5\},                                  \tag{39}
\]

the oriented simultaneous-star matrix is

\[
       (P_xK_*S_y^T)_{x\in A,y\in B}
            =\operatorname{diag}\left(\frac15,\frac15,-\frac25\right), \tag{40}
\]

whose permanent is \(-2/125\).  The Hall certificate is therefore
nonzero, not merely support-feasible.

Finally apply the coefficient-preserving marker lift (20).  The four-site
Shafiei generator

\[
                         Y_{01}Y_{23}-Y_{02}Y_{13}       \tag{41}
\]

maps to

\[
               \frac1{25}z_0z_1z_2z_3\ne0.             \tag{42}
\]

So this packet does not define that response-weighted apolar-algebra map.
On the other hand, Proposition 3.1 reduces its cubic tangent operator to
zero because the three equal cohafnian coefficients multiply response
weights summing to zero in (38).  This is the exact
specialization/cancellation obstruction.

The packet is deliberately only one mixed scalarization.  It need not
extend to the constant words or to one shared global physical tensor, so
it is not a counterexample to the conjecture.  It proves the narrower and
needed statement that Theorem 4.14 supplies no fixed-word closure; any
successful argument must couple different words.

## 7. Exact obstruction and the smallest missing lemma

The literature theorem can be used safely in this project in the following
form.

> **Generic-hafnian apolar diagnostic.**  At six residual sites, mixed
> scalar-zero tangency is equivalent to the top-degree apolar membership
> \(\frac12L_{Q_\omega}^2L_{R_\omega}\in I_3\).  Reduction by Shafiei's
> quadrics returns exactly the scalar tangent equation and no support,
> lower-degree annihilator, or four-site relation on
> \(Q_\omega,R_\omega\).  This remains true after arbitrary scalar
> extension, so putting all words in one polynomial family does not create
> hidden apolar equations.

Accordingly, **no lifting or closure lemma follows from Theorem 4.14
alone**.  The exact obstruction has three equivalent descriptions:

1. \(L_{R_\omega}\circ F\) vanishes at \(Q_\omega\), not identically as a
   polynomial in the generic edge variables.
2. Homogenization puts \(\frac12L_{Q_\omega}^2L_{R_\omega}\) in the
   one-dimensional top apolar pairing, where membership is the single
   scalar equation \(D F_{Q_\omega}(R_\omega)=0\).
3. One degree lower, the equation says exactly that
   \(\overline{L_{Q_\omega}L_{R_\omega}}\) lies in the kernel of
   \(m_{Q_\omega}:A_2\to A_3\).  For \(Q_\omega\ne0\) that kernel is
   fourteen-dimensional, and the class need not vanish.

An apolar-algebra-map route would have to add the relations (19), and the
coefficient-preserving marker version would have to add (21).  Those are
genuine extra physical assertions, not consequences of apolar ideal
membership.  Section 6 refutes them as wordwise consequences of the full
nine mixed rows.  Moreover, the all-one response shows that even the
balanced relations alone do not contradict a nonzero Hall certificate, so
such a map is stronger than necessary and still not a closure by itself.

The weakest missing statement that eliminates the live mixed branch is
the following cross-word assertion.

> **Missing cross-word kernel-exclusion lemma.**  Let fixed global blocks
> \(q_{xy}\), fixed endpoint stars \(p_i,s_j\), and a fixed direct block
> \(a\), with \(\alpha=a_{ab}\ne0\), satisfy all nine tensor rows,
> equivalently the polynomial identity (25).  Assume also the global
> rank-three conditions on both endpoint-star triples, and define \(K_*\)
> and \(R(u)\) by (23), (26).  Then for every mixed coordinate probe
> \(\omega\),
> \[
>    \overline{L_{Q_\omega}L_{R_\omega}}\in\ker m_{Q_\omega}
>       \quad\Longrightarrow\quad
>    \operatorname{haf}(R_\omega)=0.                    \tag{43}
> \]

By (27), the premise in (43) holds at every mixed word.  Thus (43) is
equivalently the direct conclusion that all mixed coefficients of the
response top power vanish.  It is the smallest needed output: it does not
ask for the stronger balanced products (21) or for an algebra map.
The selected-word packet proves that the global/shared-block hypotheses in
(43) cannot be deleted; any proof must compare at least two word
scalarizations or use an equivalent polynomial coefficient coupling.

To close the entire six-residual-site scalar-zero packet through the known
ternary descent, one must additionally prove

\[
       \operatorname{haf}(R_{c^6})\ne0
       \qquad(c=0,1,2).                                 \tag{44}
\]

Indeed, (43) and (44) would give
\(\operatorname{haf}(R(u))=\sum_c\lambda_cG_c(u)\) with every
\(\lambda_c\ne0\).  A one-site diagonal normalization then gives the exact
ternary response source used in the primary tangent theorem.  The already
known pure derivative values \(-\alpha\) in (27) do **not** imply (44), so
that nonvanishing is a separate part of the closure.

The natural algebraic target is therefore not another presentation of
\(I\).  It is the syzygy module of the hafnian Jacobian after the
block-evaluation pullback (28), together with the star factorization of
\(R(u)\), the pure polynomial in (27), and the response hafnian
\(\operatorname{haf}(R(u))\).  Those data retain the varying direction and
cross-word information that top apolarity discards.
