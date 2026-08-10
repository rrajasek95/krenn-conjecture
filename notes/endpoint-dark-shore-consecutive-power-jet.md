# Endpoint-dark shores expose one consecutive-power cofactor jet

> **Additive fixed-plane sharpening.**  The complete one-site jet below is
> now known to be sharp at its literal source scope.  The exact rational
> guard in
> [`n8-rank11-scalar-fixed-dark-plane-one-site-guard.md`](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md)
> has a fixed dark coordinate plane, rank-three endpoint and diagonal maps,
> one actual six-site \(q\), two distinct sets of nine one-site rows, and
> the corresponding consecutive powers, while a nonzero target-free scalar
> response survives.  The joint five-site coefficient fails.  Therefore
> the fixed dark-plane branch cannot be closed from separate releases;
> its joint error is a scalar normal \(\lambda\mu^{\mathsf T}W\) invisible
> to every clean-plane cap.  An individually labelled two-site coefficient
> (or the equivalent source-labelled two-chart overlap) is load-bearing.
> The subsequent
> [`joint labelled carrier theorem`](n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md)
> evaluates it: the natural 24-cell completion fibre has a two-row unit,
> while the unrestricted residue is exactly twelve pure matching carriers
> plus three mixed carriers.

## 1. Outcome

Work on the complete rootless full-nine packet on \(2h\) residual sites,

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2,
\tag{1}
\]

and let

\[
 a\ne b,\qquad \alpha=a_{ab}\ne0,\qquad
 K_*=\operatorname {tr}(a)E_{ab}-\alpha I,\qquad
 r=\sum_{i,j}(K_*)_{ij}p_i s_j.
\tag{2}
\]

The off-diagonal contraction and the rootless hypothesis give, respectively,

\[
 rq^{[h-1]}=-\alpha(X_0+X_1+X_2),
 \qquad r^{[h]}\ne0.
\tag{3}
\]

Let \(A\subset W\) be a shore on which every site has a common
endpoint-dark covector, and put \(B=W\setminus A\), \(b=|B|\ge2\).  The
complete coefficient content of all dark contractions is one pair of
literal consecutive-power cofactor maps

\[
 \mathcal J_A=(F_A,E_A),\qquad
 F_A=\iota_A q^{[h]},\quad E_A=\iota_A q^{[h-1]}.
\tag{4}
\]

The fixed diagonal target is the coordinatewise product map

\[
 \beta_A=(\beta_{A,0},\beta_{A,1},\beta_{A,2}).
\tag{5}
\]

The exact identities proved below are

\[
 \boxed{
 a_{ij}F_A(\theta)+p_i^B s_j^B E_A(\theta)
   =\delta_{ij}\beta_{A,i}(\theta)X_i^B }
\tag{6}
\]

for all nine rows, and

\[
 \boxed{
 r_B E_A(\theta)
   =-\alpha\sum_i\beta_{A,i}(\theta)X_i^B. }
\tag{7}
\]

They retain arbitrary complex cancellation, endpoint order, and the actual
consecutive divided powers.  In particular,

\[
 \boxed{\ker E_A\subseteq\ker\beta_A,
        \qquad \operatorname {rank}E_A\ge
                        \operatorname {rank}\beta_A.}
\tag{8}
\]

This gives three concrete conclusions.

1. A one-site deficient circuit is impossible in the six-site rootless
   packet: both endpoint stars vanish there, so \(r\) is supported on five
   sites and \(r^{[3]}=0\).
2. On a two-site dark cut at \(h=3\),

   \[
      E_A(v,w)=u(v,w)z+t(v)v'(w).
   \tag{9}
   \]

   Two dark probe pairs whose fixed-target patterns are not related by the
   same projective scalar contradict (1) as soon as their nonzero values in
   (9) are projectively equal.
   This strictly weakens the internal-star condition in Lemma 7.1 of
   [the selector/Hall guard](selector-hall-base-packing-and-block-jacobian-guard.md):
   that lemma sets both products \(t(v)v'(w)\) to zero and hence forces the
   required projective collision on the common line \(\mathbb Cz\).
3. For the uniform maximal \(b=3\) dark shore, \(E_A\) is only a linear
   form on the three-site complement.  The whole large-shore problem is
   therefore the bounded rank test (8), together with the three-site
   full-nine system (6).  In the high-order \((1,1)\) branch the response
   on \(A\) is one nonzero decomposable field \(\kappa UV\).  In fact the
   complete response is one global rank-one quadratic plus a quadratic
   supported on the three complement sites.

The maximal-defect matroid theorem does **not** itself force the needed
rank defect in (8).  Section 7 gives an exact six-site scalar-rootless
guard with an actual quadratic, injective endpoint stars, a minimal
\((0,1)\) dark shore, \(rq^{[2]}=\Delta_{6,3}\), and \(r^{[3]}\ne0\), for
which \(E_A\) has rank four while \(\beta_A\) has rank one.  The guard does
not satisfy the full-nine information beyond the scalar contraction.  It
therefore proves exactly that the scalar response, consecutive powers,
nonnilpotence, and dark matroid data cannot by themselves supply the missing
collision.

Section 8 gives the complementary uniform guard: it has an actual common
quadratic, all nine **fully dark contracted** rows, the deletion-stable
\((1,1)\) shore, injective endpoints, and a nonnilpotent response, while
the bounded inequality (31d) is an equality of rank one.  Its first
uncontracted shore-site row fails.  Hence the natural next input is
precisely the four-site one-bright jet (61)--(63), not another refinement
of the fully dark contraction.

The smallest additional source-overlap condition is now explicit:

> find a shore \(A\) and a coefficient
> \(\theta\in\bigotimes_{x\in A}K_x\) such that
> \(E_A(\theta)=0\) but \(\beta_A(\theta)\ne0\).

Equivalently, it is enough to force an affine \(E_A\)-collision between two
coefficients whose target values differ.  A sufficient projective version
is a proportional nonzero \(E_A\)-pair whose target values are not related
by the same scalar.  Equation (7) then gives the contradiction immediately.
No support census is involved.

## 2. The dark coefficient spaces

For each site \(x\), let

\[
 K_x=\ker(P_x^*\oplus S_x^*)\subseteq V_x^*.
\tag{10}
\]

Thus every \(\lambda\in K_x\) obeys

\[
 \lambda(p_{i,x})=\lambda(s_{j,x})=0
 \qquad(0\le i,j\le2).
\tag{11}
\]

Assume \(K_x\ne0\) for every \(x\in A\), and put

\[
 \mathcal K_A=\bigotimes_{x\in A}K_x.
\tag{12}
\]

Let \(\epsilon_i^{(x)}\in V_x^*\) be the fixed physical coordinate
covector dual to \(e_i^{(x)}\).  Define the three target functionals

\[
 \beta_{A,i}=\bigotimes_{x\in A}
       \epsilon_i^{(x)}\big|_{K_x}\in\mathcal K_A^*.
\tag{13}
\]

For a decomposable coefficient
\(\theta=\bigotimes_{x\in A}\lambda_x\), this is literally

\[
 \beta_{A,i}(\theta)=\prod_{x\in A}\lambda_x(e_i^{(x)}).
\tag{14}
\]

Extend by linearity to arbitrary \(\theta\in\mathcal K_A\).

The rank of \(\beta_A\) has a purely local readout.  The functional
\(\beta_{A,i}\) is nonzero exactly when
\(\epsilon_i^{(x)}|_{K_x}\ne0\) at every \(x\in A\).  If
\(\beta_{A,i}\) and \(\beta_{A,j}\) are both nonzero, they are
proportional exactly when

\[
 \epsilon_i^{(x)}|_{K_x}\ \parallel\
 \epsilon_j^{(x)}|_{K_x}
 \qquad\text{for every }x\in A.
\tag{14a}
\]

Indeed, this is uniqueness of the factors of two nonzero decomposable
tensors.  Thus, if \(\beta_{A,i}\) and \(\beta_{A,j}\) are both nonzero,
one site at which their restricted labels are transverse forces
\(\operatorname {rank}\beta_A\ge2\).

Coefficient contraction of the two consecutive powers defines

\[
\begin{aligned}
 F_A:\mathcal K_A&\longrightarrow({\cal R}_B)_b,
 &F_A(\theta)&=\iota_\theta q^{[h]},\\
 E_A:\mathcal K_A&\longrightarrow({\cal R}_B)_{b-2},
 &E_A(\theta)&=\iota_\theta q^{[h-1]}.
\end{aligned}
\tag{15}
\]

The degrees are exact because \(|A|=2h-b\).  These are coefficient maps
of the actual powers of one \(q\), not independently assigned tensors.

## 3. Exact full-nine and scalar contractions

Contract (1) at every site of \(A\) by a decomposable dark coefficient.
If either marked endpoint form \(p_i\) or \(s_j\) occupies a site of \(A\),
its local coefficient vanishes by (11).  Therefore both endpoint forms
must be supported in \(B\).  The \(q\)-terms are exactly (15), giving

\[
 a_{ij}F_A(\theta)+p_i^B s_j^B E_A(\theta)
   =\delta_{ij}\beta_{A,i}(\theta)X_i^B.
\tag{16}
\]

Linearity proves the same formula for every
\(\theta\in\mathcal K_A\).  This proves (6).

Now multiply (16) by \((K_*)_{ij}\) and sum.  By construction,

\[
 \sum_{i,j}(K_*)_{ij}a_{ij}=0,
 \qquad (K_*)_{ii}=-\alpha.
\tag{17}
\]

The endpoint product on \(B\) is \(r_B\), so the result is exactly (7).
The three \(X_i^B\) are linearly independent and \(\alpha\ne0\).  Hence
\(E_A(\theta)=0\) implies every \(\beta_{A,i}(\theta)=0\), proving (8).

Two useful equivalent forms of the conclusion are:

* \(\beta_A\) factors linearly through the image of \(E_A\); and
* if \(E_A(\theta')=cE_A(\theta)\) for \(c\ne0\), then
  \(\beta_A(\theta')=c\beta_A(\theta)\).

Thus a projective cofactor collision can occur only between identical
projective fixed-target patterns.

## 4. The two-site jet and the coefficient-dark lemma

Return to \(h=3\) and take \(A=\{x,y\}\).  Put
\(D=W\setminus\{x,y\}\), and let \(z=q|_D\).  For dark probes
\(v\in K_x,w\in K_y\), write

\[
\begin{aligned}
 u(v,w)&=(v\otimes w)(q_{xy}),\\
 t(v)&=\sum_{d\in D}(v\otimes\operatorname{id})q_{xd},\\
 v'(w)&=\sum_{d\in D}(w\otimes\operatorname{id})q_{yd},\\
 T(v,w)&=t(v)v'(w).
\end{aligned}
\tag{18}
\]

Literal matching separation gives

\[
 \boxed{
 E_A(v,w)=u(v,w)z+T(v,w),
 \qquad
 F_A(v,w)=u(v,w)z^{[2]}+T(v,w)z.}
\tag{19}
\]

Indeed, after exposing \(x,y\), a matching either uses the direct edge
\(xy\), or uses one star from each exposed site.  There are no missing
factorials in divided-power notation.

With \(x_i=p_i|_D,y_j=s_j|_D\), all nine rows become

\[
 a_{ij}\bigl(uz^{[2]}+Tz\bigr)
   +x_i y_j(uz+T)
 =\delta_{ij}v_iw_iX_i^D.
\tag{20}
\]

This is the complete four-layer coefficient row.  It contains no
termwise vanishing assumption.

Suppose two dark probe pairs \((v,w)\), \((\tilde v,\tilde w)\) have

\[
 E_A(\tilde v,\tilde w)=cE_A(v,w)\ne0
\tag{21}
\]

but their Hadamard target vectors

\[
 (v_0w_0,v_1w_1,v_2w_2),\qquad
 (\tilde v_0\tilde w_0,
  \tilde v_1\tilde w_1,
  \tilde v_2\tilde w_2)
\tag{22}
\]

are not related by the same scalar \(c\).  Equation (7) gives an immediate
contradiction.

Lemma 7.1 of the selector/Hall guard is a special case.  Its two probe
pairs satisfy \(T=0\).  Their nonzero diagonal target rows force both
direct coefficients \(u\) to be nonzero, so their two values of \(E_A\)
lie on the same projective line \(\mathbb Cz\).  The crossed target
incidence in that lemma says precisely that (22) is not projectively the
same.  Thus the real condition is a consecutive-cofactor collision, not
literal internal-star vanishing.

For reference, the fixed-target incidence gate itself is also linear.
The span of the three restricted bilinear forms

\[
 (v,w)\longmapsto v_iw_i
 \quad\text{on }K_x\times K_y
\tag{23}
\]

has dimension \(\operatorname {rank}\beta_{\{x,y\}}\).  If that rank is
at least two, two decomposable probes with nonproportional target patterns
exist.  Lemma 7.1 uses a stronger crossed-zero pattern.  In either form,
what remains unforced is an \(E_A\)-collision.

## 5. What the minimal circuits do and do not force

For a one-site minimal circuit \(A=\{x\}\), both local endpoint row
images vanish.  Hence \(p_{i,x}=s_{j,x}=0\) for every \(i,j\).  The
quadratic \(r\) is supported on the other five sites, so no three-edge
matching occurs:

\[
 r^{[3]}=0.
\tag{24}
\]

This contradicts rootlessness and closes the singleton circuit.

For a two-site minimal circuit, suppose without loss of generality that
the aggregate rank pair is \((0,1)\).  Then

\[
 P_x=P_y=0,qquad
 L_x^S=L_y^S=\mathbb C\ell\ne0.
\tag{25}
\]

Thus \(S_x(c)=\ell(c)s_x\), \(S_y(c)=\ell(c)s_y\), and

\[
 K_x=s_x^\perp,qquad K_y=s_y^\perp
\tag{26}
\]

are planes.  The circuit data do not force
\(\operatorname {rank}\beta_{\{x,y\}}\ge2\).  For example,

\[
 s_x=e_0^{(x)},\qquad s_y=e_1^{(y)}
\tag{27}
\]

gives \(K_x=\{v_0=0\}\), \(K_y=\{w_1=0\}\).  Only the colour-two
bilinear form in (23) is nonzero on both planes, so \(\beta\) has rank
one.

For a three-site minimal circuit, the common dark kernels may all be
lines.  Then every pair domain \(K_x\otimes K_y\) is one-dimensional and
the two-probe route is unavailable.  The correct object is the simultaneous
three-site contraction

\[
 E_A(\lambda_x\otimes\lambda_y\otimes\lambda_z)
 =u_{xy}t_z+u_{xz}t_y+u_{yz}t_x,
\tag{28}
\]

a linear form on the three-site complement.  The target vector is
\((\lambda_{x,i}\lambda_{y,i}\lambda_{z,i})_i\), which can even vanish
identically when the three kernel lines occupy three different fixed
coordinate axes.  Again the matroid circuit supplies darkness but neither
fixed-target incidence nor a cofactor-kernel witness.

## 6. The uniform maximal \(b=3\) shore

Now use the maximal deficient shore from
[the uniform selector-union theorem](uniform-selector-union-maximal-defect-shore.md).
When \(b=3\), its dark shore has

\[
 |A|=2h-3,qquad |B|=3.
\tag{29}
\]

Therefore

\[
 E_A:\mathcal K_A\longrightarrow
       V_{b_0}\oplus V_{b_1}\oplus V_{b_2}
\tag{30}
\]

is a literal one-hole cofactor flattening into a nine-dimensional space,
while \(F_A\) is a top tensor on the same three sites.  Equations (6)--(8)
reduce the whole large-shore coefficient question to

\[
\begin{gathered}
 a_{ij}F_A(\theta)+p_i^B s_j^B E_A(\theta)
   =\delta_{ij}\beta_{A,i}(\theta)X_i^B,\\
 \ker E_A\subseteq\ker\beta_A.
\end{gathered}
\tag{31}
\]

There is a completely explicit bounded version of (31).  Keep the
off-diagonal anchor \((a,b)\) with \(\alpha=a_{ab}\ne0\), and on the
three-site algebra of \(B\) put

\[
\begin{aligned}
 G_{ij}&=\alpha p_i^B s_j^B-a_{ij}p_a^B s_b^B
 &&(i\ne j),\\
 D_i&=\alpha p_i^B s_i^B-a_{ii}p_a^B s_b^B
 &&(0\le i\le2).
\end{aligned}
\tag{31a}
\]

Define

\[
\begin{aligned}
 N_B=\{e\in({\cal R}_B)_1:\;&G_{ij}e=0\quad(i\ne j),\\
                            &D_ie\in\mathbb C X_i^B
                                      \quad(0\le i\le2)\}.
\end{aligned}
\tag{31b}
\]

For \(e\in N_B\), let \(\Gamma_B(e)_i\) be the unique scalar such that
\(D_ie=\Gamma_B(e)_iX_i^B\).  Multiply the \((i,j)\) row of (31) by
\(\alpha\) and subtract \(a_{ij}\) times the anchor row.  This eliminates
\(F_A\) literally and gives

\[
 \boxed{
 \operatorname {im}E_A\subseteq N_B,\qquad
 \Gamma_BE_A=\alpha\beta_A.}
\tag{31c}
\]

Consequently

\[
 \boxed{
 \operatorname {rank}\beta_A
 \le\operatorname {rank}\Gamma_B
 \le\dim N_B\le9.}
\tag{31d}
\]

Thus \(\dim N_B<\operatorname {rank}\beta_A\) closes the shore
immediately.  More invariantly, (31c) says that the only remaining
possibility is exact factorization of all three fixed-target functionals
through this explicit nine-dimensional full-row multiplier space.

No six-site extraction and no replacement common power occurs.

In the high-order nonzero-rank branch, the aggregate shore ranks are
\((1,1)\).  Hence there are row covectors \(\lambda,\mu\) and physical
linear forms \(U,V\), supported on \(A\), such that

\[
 P|_A=\lambda\otimes U,qquad
 S|_A=\mu\otimes V.
\tag{32}
\]

Consequently

\[
 r_A=\kappa UV,qquad
 \kappa=\lambda^{\mathsf T}K_*\mu.
\tag{33}
\]

If \(h>3\), then in fact

\[
 r_A=\kappa UV\ne0.
\]

Otherwise every response edge meeting \(A\) is an \(A\)-\(B\) edge.  A
perfect matching would need to mate all \(2h-3>3\) sites of \(A\) with
only three sites of \(B\), which is impossible.  This would give
\(r^{[h]}=0\).  In particular, both \(\kappa\ne0\) and \(UV\ne0\).

There is also an exact completion of the whole response.  Put

\[
 \ell=\lambda^{\mathsf T}K_*S_B,\qquad
 m=P_B^{\mathsf T}K_*\mu,\qquad
 \widehat r_B=r_B-\kappa^{-1}m\ell .
\]

Here \(\ell,m\) are linear forms supported on \(B\), and \(\widehat r_B\)
is a quadratic supported on \(B\).  More precisely,

\[
 \widehat r_B=P_B^{\mathsf T}\widehat K S_B,\qquad
 \widehat K=K_*-\kappa^{-1}K_*\mu\lambda^{\mathsf T}K_*.
\]

The matrix \(K_*\) is invertible, and
\(I-\kappa^{-1}\mu\lambda^{\mathsf T}K_*\) is a rank-two projection.
Hence \(\widehat K\) has rank two, left radical
\(\mathbb C\lambda\), and right radical \(\mathbb C\mu\).  Thus it is the
nondegenerate two-channel pairing on the two row-index quotients.  Direct
expansion gives

\[
 \boxed{
 r=\kappa\widehat U\widehat V+\widehat r_B,\qquad
 \widehat U=U+\kappa^{-1}m,\quad
 \widehat V=V+\kappa^{-1}\ell .}
\tag{33a}
\]

Since \(B\) has three sites, \(\widehat r_B^{[2]}=0\).  Therefore

\[
 \boxed{
 r^{[h]}=\kappa^h(\widehat U\widehat V)^{[h]}
  +\kappa^{h-1}(\widehat U\widehat V)^{[h-1]}\widehat r_B.}
\tag{33b}
\]

The same identity has a four-column catalecticant form across the shore.
Let \(m_A=|A|=2h-3\) and put

\[
 C_t=U^{[t]}V^{[m_A-t]}\in({\cal R}_A)_{m_A}.
\]

Writing \(\widehat U_B,\widehat V_B\) for the \(B\)-parts in (33a), define

\[
\begin{aligned}
D_{h-3}&=\kappa^h h!\,\widehat U_B^{[3]},\\
D_{h-2}&=\kappa^h h!\,\widehat U_B^{[2]}\widehat V_B
 +\kappa^{h-1}(h-1)!\,\widehat U_B\widehat r_B,\\
D_{h-1}&=\kappa^h h!\,\widehat U_B\widehat V_B^{[2]}
 +\kappa^{h-1}(h-1)!\,\widehat V_B\widehat r_B,\\
D_h&=\kappa^h h!\,\widehat V_B^{[3]}.
\end{aligned}
\]

Expanding the divided powers across \(A\mid B\) gives the exact
four-column flattening

\[
 \boxed{
 r^{[h]}=\sum_{t=h-3}^{h}C_t\otimes D_t.}
\tag{33c}
\]

Thus the entire high-order response is controlled by four adjacent
coefficients of the binary product \(\prod_{x\in A}(V_x+zU_x)\), paired
with four explicit cubics on three sites.  This is a bounded
catalecticant problem, not a growing support classification.

At every \(x\in A\), the local support of both summands in (33b) lies in
\(\langle U_x,V_x\rangle\).  Thus every local flattening of \(r^{[h]}\)
on the shore has rank at most two.  In particular, if \(r^{[h]}\) has
only constant-colour coordinates, at most two of those coordinates can
be nonzero: three nonzero tensors \(X_i\) have local flattening rank three.

Writing \(r_{AB}\) for the original cross part, exact matching separation
across the odd \(A\mid B\) cut further gives

\[
 \boxed{
 r^{[h]}=r_A^{[h-2]}r_{AB}r_B
          +r_A^{[h-3]}r_{AB}^{[3]}.}
\tag{34}
\]

The first term has one cross edge and one \(B\)-internal edge; the second
has three cross edges.  These are the only solutions of
\(j+2k=3\), where \(j\) and \(k\) count cross and \(B\)-internal edges.

Thus the remaining high-order dark branch is not an arbitrary deficient
shore.  It is one nonzero decomposable response field on \(A\), the
bounded three-site jet (31), and the two parity layers (34).

## 7. Exact scalar-rootless guard at the sharp \(h=3,b=4\) boundary

The following packet shows why (8) is not a consequence of the scalar
row and matroid data in the direction needed for a contradiction.  Let

\[
 W=\{x,y,a,b,c,d\}
\tag{35}
\]

and use the three fixed coordinate axes at every site.  Put

\[
\begin{aligned}
q={}&e_1^{(x)}e_1^{(c)}+e_2^{(x)}e_2^{(a)}
     +e_0^{(y)}e_0^{(d)}+e_2^{(y)}e_2^{(b)}\\
   &+e_0^{(b)}e_0^{(c)}+e_1^{(a)}e_1^{(d)}.
\end{aligned}
\tag{36}
\]

Choose endpoint rows

\[
\begin{array}{lll}
p_0=e_0^{(a)}+e_1^{(b)},&p_1=e_2^{(a)},&p_2=e_2^{(c)},\\
s_0=e_0^{(x)}+e_1^{(y)},&s_1=e_2^{(a)},&s_2=e_2^{(d)},
\end{array}
\tag{37}
\]

and take \(K_*=I\).  The same-site product \(p_1s_1\) vanishes, so

\[
\begin{aligned}
r={}&e_0^{(a)}e_0^{(x)}+e_0^{(a)}e_1^{(y)}
    +e_1^{(b)}e_0^{(x)}+e_1^{(b)}e_1^{(y)}\\
   &+e_2^{(c)}e_2^{(d)}.
\end{aligned}
\tag{38}
\]

There are exactly three compatible choices of one \(r\)-edge and two
\(q\)-edges:

\[
\begin{array}{c|c}
\text{matching}&\text{word}\\ \hline
 ax\mid yd\mid bc&0^6\\
 by\mid xc\mid ad&1^6\\
 cd\mid xa\mid yb&2^6.
\end{array}
\tag{39}
\]

Therefore

\[
 rq^{[2]}=X_0+X_1+X_2.
\tag{40}
\]

The two \(r\)-matchings

\[
 ax\mid by\mid cd,qquad ay\mid bx\mid cd
\tag{41}
\]

give the same mixed word, so \(r^{[3]}\ne0\) (its coefficient there is
two).  Both endpoint triples in (37) are injective.

Take \(A=\{x,y\}\), \(B=\{a,b,c,d\}\).  On \(A\), the first endpoint
has aggregate rank zero, while both local row images of the second
endpoint are the same nonzero row-index line generated by \(s_0\).  Hence
\(A\) is exactly the minimal \((0,1)\) circuit, or equivalently the
maximal \(h=3,b=4\) dark shore.

Its dark planes are

\[
 K_x=\langle\epsilon_1^{(x)},\epsilon_2^{(x)}\rangle,
 \qquad
 K_y=\langle\epsilon_0^{(y)},\epsilon_2^{(y)}\rangle.
\tag{42}
\]

For

\[
 v=v_1\epsilon_1^{(x)}+v_2\epsilon_2^{(x)},\qquad
 w=w_0\epsilon_0^{(y)}+w_2\epsilon_2^{(y)},
\]

one has \(q_{xy}=0\) and

\[
\begin{aligned}
E_A(v,w)={}&v_1w_0e_1^{(c)}e_0^{(d)}
 +v_1w_2e_1^{(c)}e_2^{(b)}\\
&+v_2w_0e_2^{(a)}e_0^{(d)}
 +v_2w_2e_2^{(a)}e_2^{(b)}.
\end{aligned}
\tag{43}
\]

The four displayed tensors occupy four different physical pairs, so the
linearized map \(E_A:K_x\otimes K_y\to({\cal R}_B)_2\) has rank four.
Meanwhile \(\beta_A\) has rank one: only its colour-two component is
nonzero.  Since

\[
 r_B=e_2^{(c)}e_2^{(d)},
\]

multiplication of (43) gives exactly

\[
 r_BE_A(v,w)=v_2w_2X_2^B,
\tag{44}
\]

which is the dark contraction of (40).

To match the canonical notation, take for example \(a=-E_{01}\).  Then
\(\alpha=-1\), \(\operatorname {tr}a=0\), and (2) gives \(K_*=I\).
The packet therefore retains the literal scalar-zero response, its
factorization through two injective endpoint triples, the actual
consecutive power \(q^{[2]}\), nonnilpotence of \(r\), and the exact dark
shore.

It is **not** a full-nine packet.  For instance

\[
 p_0s_0q^{[2]}=X_0+X_1,
\]

so the \((0,0)\) row is not its required single target.  This is the
precise missing information: the full-nine equations beyond the scalar
contraction must force a rank loss or an overlap collision in \(E_A\).
None follows from the scalar row, rootlessness, or the dark matroid geometry
alone.

## 8. A uniform equality guard for the bounded full-nine jet

Even the actual consecutive cofactors, all nine contracted rows, deletion
stability, and the nonnilpotent four-column response can attain equality
in (31d).  The missing information is genuinely in the uncontracted or
non-dark rows.

Fix \(h\ge4\), let \(|A|=2h-3\), and put
\(B=\{b_1,b_2,b_3\}\).  At every site use the three fixed coordinate
axes.  Set

\[
\begin{gathered}
 U=\sum_{x\in A}e_1^{(x)},\qquad
 V=\sum_{x\in A}e_2^{(x)},\\
 x=e_0^{(b_1)},\qquad y=e_0^{(b_2)},\qquad
 z_i=e_i^{(b_3)}.
\end{gathered}
\tag{46}
\]

Take

\[
\begin{array}{lll}
p_0=U+x,&p_1=x+z_1,&p_2=x,\\
s_0=y,&s_1=V+y,&s_2=y+z_2,
\end{array}
\tag{47}
\]

and let \(J\) be the all-ones \(3\) by \(3\) matrix.  For

\[
 a=E_{00}-J,\qquad (a,b)=(0,1),
\tag{48}
\]

one has

\[
 \alpha=-1,\qquad \operatorname {tr}a=-2,\qquad
 K_*=I-2E_{01}.
\tag{49}
\]

On \(A\), the aggregate endpoint data are

\[
 P|_A=(1,0,0)^{\mathsf T}\otimes U,\qquad
 S|_A=(0,1,0)^{\mathsf T}\otimes V.
\tag{50}
\]

Both ranks remain one after any shore-site deletion, both complete
endpoint triples in (47) are injective, and

\[
 K_x=\mathbb C\epsilon_0^{(x)}
 \quad(x\in A),\qquad
 \beta_A=(1,0,0).
\tag{51}
\]

Choose any perfect matching \(M\) on the even set
\(A\cup\{b_3\}\), and define the actual quadratic

\[
 q=e_0^{(b_1)}e_0^{(b_2)}
   +\sum_{\{u,v\}\in M}e_0^{(u)}e_0^{(v)}.
\tag{52}
\]

For \(\theta=\bigotimes_{x\in A}\epsilon_0^{(x)}\), the literal
consecutive cofactors are

\[
 E_A(\theta)=z_0,\qquad F_A(\theta)=X_0^B.
\tag{53}
\]

Every product \(p_i^Bs_j^Bz_0\) equals \(X_0^B\): the extra \(z_1\)
or \(z_2\) component collides at \(b_3\).  Since \(a_{00}=0\) and every
other entry of \(a\) is \(-1\), all nine equations (31) hold exactly.
For completeness, the off-diagonal equations defining \(N_B\) include
\(xz_2e=0\) and \(z_1ye=0\); these kill the \(b_2\)- and
\(b_1\)-components of \(e\), while \(D_0e\in\mathbb CX_0^B\) leaves
only the \(z_0\)-axis at \(b_3\).  Hence

\[
 N_B=\mathbb Cz_0,\qquad
 \operatorname {rank}\Gamma_B
 =\operatorname {rank}\beta_A=1.
\tag{54}
\]

The associated response is

\[
\begin{aligned}
r={}&-2UV-Uy-xV+Vz_1\\
   &+xy+xz_2+z_1y.
\end{aligned}
\tag{55}
\]

Thus \(r_A=-2UV\), and (33a)--(34) apply.  To see nonnilpotence without
any support census, partition \(A=A_1\sqcup A_2\) with
\(|A_1|=h-1\), \(|A_2|=h-2\).  The coefficient of the word which is
colour one on \(A_1\), colour two on \(A_2\), colour zero at
\(b_1,b_2\), and colour two at \(b_3\), is

\[
 -(h-1)(-2)^{h-2}(h-2)!\ne0.
\tag{56}
\]

Indeed \(xz_2\) and one \(-Uy\) edge are forced, followed by a bijection
of the remaining \(h-2\) colour-one and \(h-2\) colour-two shore sites
through \(-2UV\).  The three-cross layer cannot carry this word.

This packet is not claimed to satisfy the uncontracted global nine rows.
That qualification is exact: it has the genuine quadratic (52), its
literal consecutive cofactors, the complete contracted nine-row jet, the
maximal deletion-stable \((1,1)\) shore, injective endpoint triples, the
rank-two Schur response, and \(r^{[h]}\ne0\).  Hence none of those bounded
facts can by itself make (31d) strict.  The residual equality case must be
killed by a non-dark coefficient or an uncontracted full-row overlap.

## 9. Remaining coefficient target

The endpoint-dark branch is reduced to one source-faithful statement.

> **Dark-shore cofactor-overlap target.**  In a complete full-nine
> rootless packet, for the maximal \(b=3\), \((1,1)\) shore—or for one of
> its low-order zero-rank boundaries—the literal one-hole cofactor map
> \(E_A=\iota_Aq^{[h-1]}\) has a kernel coefficient on which at least one
> fixed diagonal functional \(\beta_{A,i}\) is nonzero.

By (7), this target is already the contradiction.  A projective version
is enough: two coefficient probes whose fixed-target values are not related
by the same scalar must have proportional nonzero \(E_A\)-values.  Lemma
7.1 obtains this by forcing both internal-star products to vanish; an
overlap theorem may instead force proportionality of the complete cofactors
(9), which is the strictly weaker and invariant requirement.

Equations (14a) and (31d) give a particularly concrete two-part route:
classify the nine-dimensional space \(N_B\), and find one shore site at
which two surviving fixed labels are transverse.  For example,
\(\dim N_B\le1\) together with
\(\operatorname {rank}\beta_A\ge2\) is already impossible.  The guard in
Section 8 attains equality with a common monochromatic dark line at every
shore site, so neither part follows from the response catalecticant alone.

The next nonredundant source jet is also bounded.  Leave one
\(x\in A\) uncontracted, put \(C_x=B\cup\{x\}\), and define

\[
\begin{aligned}
 F_x:\mathcal K_{A\setminus\{x\}}&\longrightarrow({\cal R}_{C_x})_4,
 &F_x(\theta)&=\iota_\theta q^{[h]},\\
 E_x:\mathcal K_{A\setminus\{x\}}&\longrightarrow({\cal R}_{C_x})_2,
 &E_x(\theta)&=\iota_\theta q^{[h-1]}.
\end{aligned}
\tag{57}
\]

Replace \(B\) by \(C_x\) in (31a)--(31b) to obtain the four-site
admissible space \(N_{x\mid B}\subset({\cal R}_{C_x})_2\) and its target
map \(\Gamma_{x\mid B}\).  The same literal elimination proves

\[
 \operatorname {im}E_x\subseteq N_{x\mid B},\qquad
 \Gamma_{x\mid B}E_x
  =\alpha\beta_{A\setminus\{x\}}.
\tag{58}
\]

These one-site jets are not independent.  For every \(\nu\in K_x\),

\[
\begin{aligned}
 \iota_\nu E_x(\theta)&=E_A(\theta\otimes\nu),\\
 \beta_{A,i}(\theta\otimes\nu)
 &=\nu(e_i^{(x)})
       \beta_{A\setminus\{x\},i}(\theta).
\end{aligned}
\tag{59}
\]

The new content of this jet can be written without any hidden component.
For \(\theta\in\mathcal K_{A\setminus\{x\}}\), decompose

\[
 E_x(\theta)=H_x(\theta)+T_x(\theta),\qquad
 H_x(\theta)\in({\cal R}_B)_2,\quad
 T_x(\theta)\in V_x\otimes({\cal R}_B)_1.
\tag{60}
\]

Thus \(H_x\) is the part missing the freed site and \(T_x\) is the part
containing it.  Since

\[
 p_i^{C_x}=p_i^B+\lambda_iU_x,\qquad
 s_j^{C_x}=s_j^B+\mu_jV_x,
\]

the full one-site row is exactly

\[
\boxed{
\begin{aligned}
a_{ij}F_x(\theta)+p_i^Bs_j^BT_x(\theta)
&+\bigl(\lambda_iU_xs_j^B
       +\mu_jp_i^BV_x\bigr)H_x(\theta)\\
&=\delta_{ij}\beta_{A\setminus\{x\},i}(\theta)
       e_i^{(x)}X_i^B.
\end{aligned}}
\tag{61}
\]

There are no omitted terms.  The product \(p_i^Bs_j^BH_x\) has degree
four on only three sites and vanishes; every term using both a local
endpoint and \(T_x\) collides at \(x\); and the product \(U_xV_x\)
also vanishes at one site.  Contracting (61) by any \(\nu\in K_x\)
recovers (31).

Eliminating \(F_x\) from (61) with the same anchor gives a finite linear
system

\[
\begin{aligned}
G_{ij}T_x+C_{ij,x}H_x&=0 &&(i\ne j),\\
D_iT_x+C_{ii,x}H_x
 &=\alpha\beta_{A\setminus\{x\},i}
                    e_i^{(x)}X_i^B,
\end{aligned}
\tag{62}
\]

where

\[
\begin{aligned}
C_{ij,x}={}&
\alpha\bigl(\lambda_iU_xs_j^B+\mu_jp_i^BV_x\bigr)\\
&-a_{ij}\bigl(\lambda_aU_xs_b^B+\mu_bp_a^BV_x\bigr).
\end{aligned}
\tag{63}
\]

Thus the first new question is sharply localized: can one
two-form \(H_x\) repair all six off-diagonal dark equations while also
carrying the three fixed diagonal targets in (62)?

This one-site jet genuinely detects information absent from (31).  In the
guard of Section 8, let \(u\) be the shore site paired with \(b_3\) in
\(M\).  Then \(E_u\) contains both
\(e_0^{(u)}z_0\) and \(xy\).  In the \((0,2)\) row, the latter produces
the uncancelled mixed tensor
\(e_1^{(u)}xyz_2\).  Thus the guard fails precisely at this first
uncontracted overlap, even though its fully dark jet is exact.

A closure can therefore try to force a second visible target or such a
mixed defect in one \(N_{x\mid B}\).  The fixed-dark-plane guard cited at
the start realizes the rank-one-aligned alternative with two complete
one-site contractions and genuine consecutive powers, so this alternative
is not eliminable from separate releases.  The next step there is the joint
five-site compatibility of
(58)--(59) for two freed shore sites.  This is still a non-growing
five-site problem.

The first such compatibility is now exact.  On the natural exposed-site
fibre it is an ordinary two-row unit; in the unrestricted source its only
escape is the fifteen-term carrier ledger in
[`n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md`](n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md).
What remains is to route those carriers with entry minimality and the
source-faithful second chart, not to derive another separate one-site jet.

The exact objects available to prove it are only

\[
 \boxed{
 \text{three-site full-nine jet (31)}
 +\text{ decomposable shore response (33)}
 +\text{ four-column response (33a)--(33c)}
 +\text{ parity split (34)}
 +\text{ one-/two-site compatibility (57)--(63)}.}
\]

This is the natural endpoint-dark analogue of the common-coloop curvature
corner and the inactive-root second-polar problem: in all three ledgers the
missing step is faithfulness of a literal consecutive-power cofactor on a
small fixed-label quotient.
