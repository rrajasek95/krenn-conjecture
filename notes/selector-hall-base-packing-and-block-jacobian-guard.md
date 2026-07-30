# Selector/Hall data do not supply a separated own-edge chart

## 1. Outcome and scope

Work on six residual sites \(W\), with the complete physical pair notation

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                  \tag{1}
\]

The audited full-nine exceptional-shore theorem and response
nonnilpotence imply that each endpoint star has a three-site Hall--Rado
selector.  A mixed nonzero coefficient of the response top power also
gives an oriented balanced partition whose simultaneous-star matrix has
nonzero permanent.  Those facts do **not**, by themselves, imply a
balanced partition with disjoint endpoint selectors, shore separation, or
a source-valid own-edge lift.

There are two independent obstructions.

1. The exact condition for disjoint selector bases is a matroid-union
   inequality.  A nonzero Hall permanent controls only one nonzero scalar
   at each selected site and does not imply that inequality.  Section 3
   gives a fixed-block selected-word packet in which both endpoint
   matroids are \(U_{1,3}\oplus U_{2,3}\), every one-site deletion still
   has aggregate rank three, and a mixed response Hall permanent is
   \(-4\ne0\), but a three-site flat violates the union inequality.  Hence
   no disjoint selector partition exists.  The newer full-nine
   rank-two-shore theorem does classify the separate aggregate-rank-two
   common-exceptional-site stratum; it does not reach this coloop-free
   defect.
2. Even after granting disjoint fixed-label selectors and literal shore
   separation, the fixed quadratic blocks need not allow one scalar edge
   to vary independently.  Section 6 gives a fixed-source tensor packet
   satisfying all six off-diagonal tensor rows and all nine scalar rows at
   every mixed coordinate word.  Its mixed response Hall permanent is
   nonzero, but its block-evaluation Jacobian is the signless vertex-edge
   incidence map of \(K_6\).  A four-cycle covector obstructs every
   own-edge lift.  The packet fails exactly the three pure diagonal target
   tensors, so it is not a solution of (1); it is a sharp guard showing
   where a diagonal anchor must enter.

The audited two-dark-colour four-cut contradiction can be recovered
without literal zero blocks by using coefficient probes, but only under
additional common-kernel, internal-star-product, and target-incidence
hypotheses.  Section 7 records the exact coefficient-probe version.
Selectors and a Hall permanent imply none of those hypotheses.

Thus there is no proved incidence prerequisite for the proposed
diagonal-anchored overlap--jet lemma.  The minimal honest replacement is
to assume (or prove from a literal diagonal coefficient cut) both:

* the separated Rado base-packing condition of (16), including a mixed
  choice of representatives; and
* the Jacobian column-membership condition of (22) for an edge whose
  normalized direct entry is nonzero.

Transport of the fixed pure target flags remains an additional anchoring
condition.  No full proof of that transport is claimed here.

## 2. The exact matroid for a site selector

Let \(C=\mathbb C^3\) be the row-index space for the first endpoint.  For
each site \(x\in W\), put

\[
 L_x^P=\operatorname{im}(P_x^*:V_x^*\longrightarrow C^*),
 \qquad
 L_x^S=\operatorname{im}(S_x^*:V_x^*\longrightarrow D^*),       \tag{2}
\]

where \(D=\mathbb C^3\) is the row-index space for the second endpoint.
The Rado matroid \(M_P\) on ground set \(W\) declares \(I\subseteq W\)
independent when one can choose

\[
                 \lambda_x\in L_x^P\quad(x\in I)              \tag{3}
\]

independently.  Its rank on \(A\subseteq W\) is

\[
 \rho_P(A)=\min_{J\subseteq A}
 \left(|A\setminus J|+
       \dim\sum_{x\in J}L_x^P\right).                         \tag{4}
\]

Define \(M_S,\rho_S\) similarly.  A three-element set \(X\) is a
\(P\)-selector shore exactly when \(\rho_P(X)=3\).

**Proposition 2.1 (selector base packing).**  Suppose \(M_P\) and \(M_S\)
both have rank three on the six-element set \(W\).  There is a partition

\[
             W=X\sqcup Y,\qquad |X|=|Y|=3,                    \tag{5}
\]

with \(X\) a \(P\)-selector and \(Y\) an \(S\)-selector if and only if

\[
 \boxed{\qquad
       \rho_P(A)+\rho_S(A)\ge |A|
       \quad\text{for every }A\subseteq W.
       \qquad}                                               \tag{6}
\]

**Proof.**  Such a partition is a decomposition of \(W\) into an
independent set of \(M_P\) and an independent set of \(M_S\).  The matroid
union theorem says that this is possible exactly under (6).  Since the
two ranks and the two desired cardinalities are three, any covering by
the two independent sets is automatically the disjoint base partition
(5).  Equivalently, \(X\) is a common base of \(M_P\) and \(M_S^*\), and
the matroid-intersection min--max formula reduces to (6).  \(\square\)

Now let a mixed scalarization of the response have a nonzero Hall
permanent.  Expanding that permanent supplies a partition \(A\sqcup B\),
a bijection \(\pi:A\to B\), and scalar rows

\[
 \bar p_x\in L_x^P,\qquad \bar s_y\in L_y^S,
 \qquad
 \prod_{x\in A}\bar p_xK_*\bar s_{\pi(x)}^{\mathsf T}\ne0.   \tag{7}
\]

It follows only that \(\rho_P(\{x\})=1\) for \(x\in A\) and
\(\rho_S(\{y\})=1\) for \(y\in B\).  A permanent can be nonzero even when
its matrix has rank one or two.  Therefore (7) gives none of the
higher-cardinality inequalities in (6).

## 3. A coloop-free deficient-flat Hall guard

The preceding gap occurs with rational fixed data, outside both sparse
shores already closed by the full-nine theorem, and even without a common
coloop.

Let

\[
 W=A\sqcup B,
 \qquad A=\{0,1,2\},\qquad B=\{3,4,5\}.                \tag{G1}
\]

For both endpoint selector matroids, take one-dimensional local row
spaces represented by

\[
\begin{array}{c|cccccc}
x&0&1&2&3&4&5\\ \hline
L_x&\langle e_0\rangle&\langle e_0\rangle&\langle e_0\rangle
 &\langle e_1\rangle&\langle e_2\rangle
 &\langle e_1+e_2\rangle .
\end{array}                                                   \tag{G2}
\]

Thus each matroid is

\[
                         U_{1,3}|_A\oplus U_{2,3}|_B.          \tag{G3}
\]

It has rank three and no coloop.  Deleting any one site leaves aggregate
row rank three, so every rank-two-shore coordinate restriction is
vacuous.  Neither star is supported on at most two sites, and neither has
rank at most one away from an exceptional site.  Nevertheless

\[
                 \rho_P(A)+\rho_S(A)=1+1<3=|A|.       \tag{G4}
\]

so Proposition 2.1 forbids disjoint selector bases.

This matroid packet is realized by fixed three-dimensional local blocks
with a separating selected word.  Use the oriented partition

\[
 X=\{0,3,4\},\qquad Y=\{1,2,5\}.                      \tag{G5}
\]

For example, take the mixed word
\(\omega=(0,1,2,0,1,2)\).  At site \(z\), let
\(\ell_z=e_{\omega_z}^*\) and choose a second coordinate covector
\(m_z\) with \(m_z(e_{\omega_z})=0\).  Visible rows below are evaluated
through \(\ell_z\), while hidden rows are evaluated through \(m_z\).

At the selected word, let the visible \(P\)-rows on \(X\) be
\(e_0,e_1,e_2\), and let the visible \(S\)-rows on \(Y\) be the rows of

\[
 V=\begin{pmatrix}1&0&0\\1&0&0\\0&1&1\end{pmatrix}.          \tag{G6}
\]

Make the opposite-shore rows vanish at that word.  Explicitly, let

\[
 b_0=b_1=b_2=e_0,quad b_3=e_1,quad b_4=e_2,quad
 b_5=e_1+e_2,
\]

and define the local evaluation maps by

\[
 \begin{array}{c|cc}
 z& P_z(u)&S_z(u)\\ \hline
 z\in X&\ell_z(u)b_z&m_z(u)b_z\\
 z\in Y&m_z(u)b_z&\ell_z(u)b_z.
 \end{array}                                                \tag{G6a}
\]

Both local row images are then exactly \(\langle b_z\rangle\); at the
selected probe the visible rows are those of (G6) and the opposite rows
vanish.  Thus both endpoint stars are globally injective and have exactly
the coloop-free matroid (G3), even though the visible \(S\)-shore has rank
two.

Put the fixed block \(\ell_x\otimes\ell_y\) on each edge of the matching
which pairs the ordered sites of \(X\) with those of \(Y\), and zero on
every other edge.
Then \(F=1\), the cross-shore cofactor matrix is the identity, and

\[
                    P^{\mathsf T}H(Q)S=V=-Fa
 \quad\text{for}\quad a=-V.                           \tag{G7}
\]

Choose the off-diagonal entry \((a,b)=(1,0)\).  Then

\[
 \alpha=a_{10}=-1,\qquad \tau=\operatorname{tr}a=-2,
 \qquad
 K_*=\tau E_{10}-\alpha I=I-2E_{10}.                  \tag{G8}
\]

The oriented simultaneous-star matrix is

\[
 K_*V^{\mathsf T}
   =\begin{pmatrix}1&1&0\\-2&-2&1\\0&0&1\end{pmatrix},
 \qquad
 \operatorname{per}(K_*V^{\mathsf T})=-4\ne0.        \tag{G9}
\]

Thus a nonzero permanent coexists with the strict union defect (G4).
The scalar \(q\)-edges and star values all come from fixed rank-one
physical blocks.  This remains a selected-word packet, not a solution of
(1) on all words.  Its force is exact: it has the same numerical aggregate
rank bounds as the known shore restrictions, has no common coloop, and shows
that a Hall permanent does not eliminate a smaller deficient flat.  The
full-nine shore theorems do not logically apply to this selected-word guard.

There is now a useful positive qualification for the rank-two common
exceptional-site stratum.  The
[full-nine rank-two-shore theorem](full-nine-rank-two-shore-coordinate-support.md)
proves that if
\(\operatorname{rank}P_{\bar x}=\operatorname{rank}S_{\bar x}=2\), and
\(c,d\) span the two off-\(x\) kernel lines, then

\[
 \beta q^{[h]}=\sum_i c_i d_iX_i,
 \qquad \beta=c^{\mathsf T}ad.                         \tag{G10}
\]

with each of \(c,d\) supported on at most two fixed labels.  Hence such a
full-nine common exceptional site routes either to a unary/binary
top tensor or, when \(\beta=0\), to coordinate-disjoint kernel supports.
This classifies the aggregate-rank-two common-coloop subcase.  It does not
imply (6), does not cover a Rado coloop whose off-site aggregate span still
has rank three, and does not apply to the coloop-free three-element defect
(G4).

## 4. Shore separation is another Rado problem

It is useful not to hide shore separation in a choice of row bases.  In
the all-probe formulation, let \(U_x\simeq\mathbb C^3\) be the local
probe space and regard

\[
       P_x:U_x\to C^*,\qquad S_x:U_x\to D^*                 \tag{14}
\]

as the two fixed local evaluation maps.  Define the separated local row
spaces

\[
 \widehat L_x^P=P_x(\ker S_x),\qquad
 \widehat L_x^S=S_x(\ker P_x).                              \tag{15}
\]

Let \(\widehat\rho_P,\widehat\rho_S\) be their Rado rank functions.
A partition \(W=X\sqcup Y\) admits probes for which the \(P\)-rows on
\(X\) are independent and the \(S\)-rows vanish there, while the
\(S\)-rows on \(Y\) are independent and the \(P\)-rows vanish there, if
and only if

\[
 \boxed{\qquad
 \widehat\rho_P(A)+\widehat\rho_S(A)\ge |A|
 \quad(A\subseteq W).
 \qquad}                                                  \tag{16}
\]

This is Proposition 2.1 applied to the restricted spaces (15).  It is
strictly stronger than (6).  Ordinary endpoint selectors use
\(P_x(U_x)\) and \(S_x(U_x)\), not the restricted images (15).

For a mixed chart, the representatives supplied by (16) must in addition
be chosen in the target-zero locus

\[
             G_0(u)=G_1(u)=G_2(u)=0.                         \tag{17}
\]

That is a genuine incidence requirement on the representatives, not a
matroid-rank consequence.  Finally, independent selector rows produce
invertible matrices \(A,B\), but they need not preserve the fixed target
diagonal.  The fixed-label flag test says that

\[
 A^{-\mathsf T}\operatorname{Diag}_3B^{-1}
       =\operatorname{Diag}_3
\]

only when \(A,B\) are monomial with the same underlying permutation.
Thus neither (6) nor (16) supplies cross-word alignment with the three
pure target flags.

## 5. The actual block-evaluation Jacobian

For fixed physical blocks, define

\[
 \Phi(u)=\bigl((Q_{xy}(u))_{x<y},G_0(u),G_1(u),G_2(u)\bigr),
 \qquad Q_{xy}(u)=q_{xy}(u_x,u_y).                    \tag{18}
\]

At six sites, both the source and target tangent spaces in (18) have
dimension eighteen.  Nevertheless no dominance or submersion property is
part of the source hypotheses.  Its literal differential is

\[
\begin{aligned}
 dQ_{xy}|_u(\xi)
   &=q_{xy}(\xi_x,u_y)+q_{xy}(u_x,\xi_y),\\
 dG_c|_u(\xi)
   &=\sum_z(\xi_z)_c\prod_{w\ne z}u_{w,c}.
\end{aligned}                                                   \tag{19}
\]

For an edge \(e\in\binom W2\), a source-valid pure-horizontal own-edge
lift is exactly a solution of

\[
                  d\Phi_u(\xi)=(\mathbf e_e,0,0,0).    \tag{21}
\]

Consequently the minimal Jacobian hypothesis is the column-membership
condition

\[
 \boxed{\quad
 (\mathbf e_e,0,0,0)\in\operatorname{im}d\Phi_u.
 \quad}                                                 \tag{22}
\]

Equivalently, every left-kernel pair
\((\lambda_{xy},\mu_c)\in\ker(d\Phi_u)^{\mathsf T}\) must have
\(\lambda_e=0\).  In fixed blocks, the left-kernel condition is the local
system

\[
 \sum_{y\ne z}\lambda_{zy}
        q_{zy}(\,\cdot\,,u_y)
 +\sum_c\mu_c
       \left(\prod_{w\ne z}u_{w,c}\right)e_c^*=0
 \quad\text{in }U_z^*,\qquad z\in W,                  \tag{23}
\]

with the appropriate transposed block when \(z\) is the second endpoint.
This is the actual incidence test.  Endpoint selector ranks do not occur
in (23).

## 6. A fixed-source mixed-torus guard with no own-edge lift

The failure of (22) persists after granting all the desired selector and
separation data.

Take

\[
 X=\{0,2,4\},\qquad Y=\{1,3,5\},\qquad
 \omega=(0,0,1,1,2,2),                                \tag{24}
\]

and put \(\ell_z=e_{\omega_z}^*\in V_z^*\).  Define fixed physical
blocks

\[
 q_{xy}=\ell_x\otimes\ell_y\quad(x<y),                 \tag{25}
\]

and fixed endpoint stars

\[
 p_i=\ell_{2i},\qquad s_i=\ell_{2i+1},
 \qquad i=0,1,2,                                      \tag{26}
\]

where each form in (26) is supported at its displayed site.  Thus, at
the word \(\omega\), the \(P\)-rows on \(X\) and the \(S\)-rows on \(Y\)
are both the literal standard basis; the opposite-shore rows vanish.
Both endpoint maps are injective, each is supported on exactly three
sites, and deletion of any site leaves rank at least two.

Put

\[
                         a=-\frac15\mathbf 1_{3\times3}.       \tag{27}
\]

There is an exact tensor identity behind this choice.  If

\[
                     L=\prod_{z=0}^5\ell_z,
\]

then the complete graph has fifteen perfect matchings and a four-vertex
complete graph has three, so

\[
                         q^{[3]}=15L,
 \qquad                 p_i s_jq^{[2]}=3L              \tag{28}
\]

for every \(i,j\).  Hence

\[
 \boxed{\qquad
       a_{ij}q^{[3]}+p_i s_jq^{[2]}=0
       \quad(0\le i,j\le2).
       \qquad}                                        \tag{29}
\]

In particular, all six off-diagonal tensor rows of (1) hold.  Every one
of the nine scalar equations holds at every mixed coordinate word,
because its target coefficient is zero.  The defect of (29) from (1) is
exactly the three pure tensors \(X_0,X_1,X_2\).  Thus this is a fixed
physical-block, all-mixed-word guard, not a full-nine source.

At the displayed word,

\[
 Q_{xy}=1,\qquad F=15,\qquad H_{xy}=3,
 \qquad P^{\mathsf T}HS=3\mathbf 1=-Fa.                \tag{30}
\]

For the off-diagonal entry \((a,b)=(0,1)\),

\[
 \alpha=-\frac15,\qquad \tau=-\frac35,\qquad
 K_*=\frac15I-\frac35E_{01}.                          \tag{31}
\]

The oriented \(X\)-to-\(Y\) response matrix is \(K_*\).  Its only
permutation term is the diagonal one, and therefore

\[
                      \operatorname{per}(K_*)=\frac1{125}\ne0. \tag{32}
\]

This is a literal separating, fixed-label Hall chart on the saturated
\(F\alpha\ne0\) locus.

Now vary the probes at the base word and put

\[
                         \dot t_z=\ell_z(\xi_z).
\]

Equations (19), (25) give

\[
                         dQ_{xy}(\xi)=\dot t_x+\dot t_y.       \tag{33}
\]

Every colour occurs twice in \(\omega\), so each pure product has four
zero factors and

\[
                         dG_0=dG_1=dG_2=0.                     \tag{34}
\]

Choose an edge \(e=xy\) and two further distinct vertices \(z,w\).  The
edge covector

\[
 \lambda_{xy}=1,\qquad \lambda_{zw}=1,
 \qquad \lambda_{xz}=-1,\qquad \lambda_{yw}=-1         \tag{35}
\]

with all other coefficients zero annihilates (33), because each of the
four vertex variables occurs once with each sign.  It has
\(\lambda_e=1\).  By the dual criterion following (22), no solution of
(21) exists.  Since \(e\) was arbitrary, **no scalar edge has an own-edge
lift** at this chart.

The same calculation holds on the nonzero torus
\(u_z=t_ze_{\omega_z}\).  There

\[
 Q_{xy}=t_xt_y,\qquad
 F=15\prod_zt_z,\qquad
 H_{xy}=3\prod_{v\ne x,y}t_v,                          \tag{36}
\]

and all nine mixed proportionality entries continue to hold with the
same fixed \(a\).  The obstruction is therefore not an isolated scalar
assignment.

This guard is also hostile to replacing literal zero-star sites by
coefficient probes.  At every site,

\[
 \ker(P_z\oplus S_z)=\ker\ell_z,
 \qquad
 q_{zy}(v,\,\cdot\,)=0
 \quad\text{whenever }v\in\ker\ell_z.                 \tag{37}
\]

Thus every probe which kills both endpoint stars also kills every
incident quadratic block, including the direct scalar needed by a
two-anchor cross row.

## 7. What coefficient probes would need for the two-anchor argument

The preceding negative result does not mean that literal zero blocks are
logically necessary for the audited two-dark-colour contradiction.  They
can be weakened to exact coefficient-probe conditions, as follows.

Choose two residual sites \(i,j\), put \(D=W\setminus\{i,j\}\), and let
\(z=q|_D\).  For local probes \(v\in U_i,w\in U_j\), write

\[
\begin{aligned}
 u(v,w)&=q_{ij}(v,w),\\
 t(v)&=\sum_{x\in D}q_{ix}(v,\,\cdot\,),\\
 v'(w)&=\sum_{x\in D}q_{jx}(w,\,\cdot\,),
\end{aligned}                                                   \tag{38}
\]

and let \(x_a=p_a|_D,y_b=s_b|_D\).  Call the probe pair
\((v,w)\) endpoint-dark when

\[
             P_i(v)=S_i(v)=P_j(w)=S_j(w)=0.           \tag{39}
\]

Contracting (1) at \(i,j\) by an endpoint-dark pair gives
the exact four-layer row

\[
\begin{aligned}
 &a_{ab}u(v,w)z^{[2]}
 +a_{ab}t(v)v'(w)z
 +u(v,w)x_ay_bz+x_ay_bt(v)v'(w)\\
 &\hspace{38mm}
 =\delta_{ab}\,v_a w_a X_a^D.                         \tag{40}
\end{aligned}

No whole physical block has been set to zero in (40); only its selected
coefficient has vanished.

**Lemma 7.1 (coefficient-dark two-anchor pattern).**  Let \(r\ne s\).
Suppose there are endpoint-dark probe pairs
\((v_r,w_r)\) and \((v_s,w_s)\) such that

\[
\begin{gathered}
 t(v_r)v'(w_r)=t(v_s)v'(w_s)=0,\\
 (v_r)_r(w_r)_r\ne0,qquad
 (v_s)_s(w_s)_s\ne0,qquad
 (v_s)_r(w_s)_r=0.                                    \tag{41}
\end{gathered}

Then (1) is inconsistent.

**Proof.**  Put

\[
        R_c=a_{cc}z^{[2]}+x_cy_cz\qquad(c\in\{r,s\}).  \tag{42}
\]

Use (40) first with endpoint colours \((r,r)\) and probes
\((v_r,w_r)\), then with endpoint colours \((s,s)\) and probes
\((v_s,w_s)\), and finally with endpoint colours \((r,r)\) and the
\(s\)-probe pair.  The three rows are

\[
\begin{aligned}
 u(v_r,w_r)R_r&=(v_r)_r(w_r)_rX_r^D,\\
 u(v_s,w_s)R_s&=(v_s)_s(w_s)_sX_s^D,\\
 u(v_s,w_s)R_r&=0.
\end{aligned}                                                   \tag{43}
\]

The second row forces the scalar \(u(v_s,w_s)\ne0\).  The third then
forces \(R_r=0\), contrary to the first.  \(\square\)

Lemma 7.1 is the precise way coefficient covectors can recover the
three-row precedent without literal zero-star sites.  Its hypotheses are
not selector consequences:

* a common endpoint-dark probe requires
  \(\ker(P_z\oplus S_z)\ne0\), whereas the combined local map can be
  injective at every site while both global endpoint maps have selectors;
* the vanishing in the first line of (41) concerns the complete product
  of two internal \(q\)-stars after cancellation;
* the last two lines of (41) are fixed-target incidence conditions; and
* the nonzero direct scalar is forced only after the pure diagonal target
  row is retained.

The torus guard (37) shows an exact failure mode: common-kernel probes can
exist, but all of them lie in the radical of the direct quadratic block.

## 8. Minimal additional hypotheses and the live lemma

There are three logically distinct gates.

1. **Separated base packing.**  Prove (16) and choose its representatives
   in the mixed target-zero locus (17).  The ordinary selector theorem and
   the mixed Hall permanent do not imply this.
2. **Own-edge transversality.**  On that chart, find an edge
   \(e=x_ay_b\) with \(F\ne0\) and nonzero normalized direct entry, and
   prove (22).  Full rank of the entire \(18\times18\) Jacobian is a
   convenient stronger assumption, but (22) for one distinguished edge
   is the exact minimum.
3. **Diagonal flag anchoring.**  Transport at least one literal pure
   target coefficient into the same selector chart so that independent
   oblique normalizations cannot absorb it.  The fixed-source guard of
   Section 6 satisfies every mixed coefficient row and fails precisely at
   this gate.

For the alternative two-anchor route, items 1--2 may be replaced by the
coefficient-dark hypotheses (41).  Those hypotheses are stronger local
incidence data, not a consequence of matroid base packing.

Accordingly, the incidence prerequisite should not be built into the
statement of an anchored overlap--jet lemma as if already proved.  A
rigorous version must either assume the separated-base and Jacobian
conditions explicitly, or prove them as part of the diagonal-anchored
overlap argument.  The present note proves only the negative incidence
result and the exact guarded alternatives.
