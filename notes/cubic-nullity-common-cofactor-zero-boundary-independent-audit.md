# Independent audit: the cubic common-cofactor-zero boundary

## 1. Verdict and scope

The theorem and countermodel in
[cubic-nullity-common-cofactor-zero-boundary.md](cubic-nullity-common-cofactor-zero-boundary.md)
are sound over the intended field \(\mathbb C\).  In particular, if

\[
 P_c=H_L(A),\qquad L=B\setminus\{p,a_c,q,q'\},
\]

then the portion of either leave-one-anchor kernel supported at the extra
nonneighbour is exactly the full local three-port when \(P_c=0\), and is
zero when \(P_c\ne0\).  The dense family in the primary note realizes the
zero case sharply for every even \(N\ge8\): both deletion kernels have
dimension exactly three, but they live at the opposite local ports and
have no common \(L\)-star component.

This is a local obstruction to a proposed kernel-compatibility inference.
It is not a Krenn counterexample and is not promoted as one.  Its complete
cofactor is a nonzero mixed tensor and fails the pure cofactor equation for
each of the three colours.

## 2. Local-port classification and the gluing identity

Fix one anchor colour and abbreviate

\[
 S=L\mathbin{\dot\cup}\{q,q'\},\qquad
 K_q=L\mathbin{\dot\cup}\{q'\},\qquad
 K_{q'}=L\mathbin{\dot\cup}\{q\}.
\]

All tensor factors below are restored to physical site order.  For
\(z=(z_{q'},z_L)\), the complete cofactor map on \(K_q\) is

\[
 \Phi_{q,c}(z)=\sum_{v\in K_q}z_v^{(v)}\otimes
                     H_{K_q\setminus\{v\}}.
\]

Contract its \(q'\)-slot by \(e_j^*\).  The term centered at \(q'\) is

\[
                         (e_j^*z_{q'})H_L.
\]

In a term centered at \(v\in L\), the unmatched site \(q'\) must pair
with one and only one \(w\in L\setminus\{v\}\).  Orienting the physical
block from \(q'\) to \(w\), its contracted row is
\(b^{q'}_{j,w}=(e_j^*\otimes\mathrm{id})A_{q'\mid w}\).  Partitioning the
complete matching sum by \((v,w)\) therefore gives, without division or
termwise noncancellation,

\[
 (e_j^*)_{q'}\mathbin{\lrcorner}\Phi_{q,c}(z)
 =(e_j^*z_{q'})P_c+
 \sum_{v\ne w}z_v^{(v)}\otimes b^{q'}_{j,w}{}^{(w)}
       \otimes H_{L\setminus\{v,w\}}.                 \tag{A}
\]

Setting \(z_L=0\) in (A) gives exactly

\[
                     \Phi_{q,c}(z_{q'})=z_{q'}\otimes P_c. \tag{B}
\]

Over a field, a simple tensor is zero precisely when one factor is zero.
Thus

\[
 \ker\Phi_{q,c}\cap V_{q'}=
 \begin{cases}V_{q'},&P_c=0,\\0,&P_c\ne0.\end{cases}
\]

Swapping \(q,q'\) proves the other equality.  When \(P_c\ne0\), the
kernel of restriction from \(\ker\Phi_{q,c}\) to the common \(L\)-port is
the intersection just computed, hence restriction is injective.  When
\(P_c=0\), the guaranteed local three-port restricts to zero.  This proves
the classification in the primary note for arbitrary cancellations and
zero blocks; it is not a generic-rank argument.

The independent checker expands matchings in a different order from the
primary verifier and checks (A) coefficient by coefficient with dense
integral, endpoint-asymmetric blocks whose physical labels are interleaved.

## 3. The surviving nine Hessian equations

Contract the complete tensor \(H_S\) at \(q,q'\) by colours \(d,j\).
There are exactly two cases for a matching:

1. \(q\) is paired directly with \(q'\), contributing
   \(A_{q\mid q'}(d,j)P_c\); or
2. \(q\) is paired to \(v\in L\), \(q'\) is paired to a distinct
   \(w\in L\), and the remainder contributes
   \(H_{L\setminus\{v,w\}}\).

Writing \(s^q_{d,v}\) and \(s^{q'}_{j,w}\) for the corresponding physical
star rows yields the universal identity

\[
 (e_d^*)_q(e_j^*)_{q'}H_S
 =A_{q\mid q'}(d,j)P_c+
   \sum_{v\ne w}s^q_{d,v}{}^{(v)}\otimes
       s^{q'}_{j,w}{}^{(w)}\otimes H_{L\setminus\{v,w\}}. \tag{C}
\]

For a genuine cubic target cofactor
\(H_S=\lambda_c^{-1}e_c^{\otimes S}\), equation (C) is exactly the nine
equations

\[
 A_{q\mid q'}(d,j)P_c+
 \Theta_c(s^q_{d,L},s^{q'}_{j,L})
 =\delta_{cd}\delta_{cj}\lambda_c^{-1}e_c^{\otimes L}.
\]

No symmetry of the physical block was introduced: from the reversed
endpoint its coefficient is
\(A_{q'\mid q}(j,d)=A_{q\mid q'}(d,j)\).  The independent checker verifies
(C) for all nine colour pairs in both endpoint orientations.  Hence, on
the \(P_c=0\) boundary, the eight zero Hessian responses and the one pure
nonzero response really are the next surviving constraints.

The same matching partition also proves the entry-minimality statement.
Changing only \(A_{q\mid q'}\) by \(\Delta A\) changes the anchor cofactor
by exactly \(\Delta A\otimes P_c\).  If all three anchor-specific
\(P_0,P_1,P_2\) vanish, deleting a nonzero \(qq'\)-block preserves all
three cofactors used in the expansion at the cubic vertex \(p\), and
therefore preserves the full target while reducing aggregate entry
support.  Thus entry-minimality implies only

\[
 A_{qq'}\ne0\Longrightarrow P_c\ne0\text{ for at least one }c.
\]

It does not choose that colour and does not imply that two \(P_c\)'s are
nonzero.

## 4. Uniform dense cancellation family

Put \(r=N-4\), which is even and at least four, and label
\(L=\{1,\ldots,r\}\).  Every internal block is a nonzero multiple of
\(E=e_0e_0^T\), with scalar weights

\[
 w_{12}=-(r-2),\qquad w_{uv}=1\quad(\{u,v\}\ne\{1,2\}).
\]

The only possible word in \(H_L\) is the all-zero word.  Matchings using
edge \(12\) contribute
\(-(r-2)(r-3)!!\); matchings avoiding it contribute
\((r-1)!!-(r-3)!!=(r-2)(r-3)!!\).  Hence \(P_c=H_L=0\) by exact
cancellation.

For a double deletion, let its scalar cofactor be \(h_{vw}\).  If one of
\(v,w\) is special, all surviving weights are one and

\[
 h_{vw}=(r-3)!!.
\]

If neither is special, the same partition on the remaining \(r-2\)
vertices gives

\[
 h_{vw}=-(r-2)(r-5)!!+
       \bigl((r-3)!!-(r-5)!!\bigr)=-2(r-5)!!.
\]

Every double cofactor is therefore nonzero over \(\mathbb C\).

Attach either terminal \(t\in\{q,q'\}\) to every \(v\in L\) by the
endpoint-asymmetric block
\(A_{t\mid v}=e_0^{(t)}\otimes e_1^{(v)}\).  The three cofactor-map
columns centered at \(t\) vanish because \(H_L=0\).  For a column centered
at \(v\in L\), its output is

\[
 \sum_{w\ne v}h_{vw}
 e_0^{(t)}\otimes e_1^{(w)}\otimes
 e_\gamma^{(v)}\otimes
 e_0^{\otimes(L\setminus\{v,w\})}.                    \tag{D}
\]

The three values of \(\gamma\) occupy disjoint word sectors.

* For \(\gamma=0\), the coefficient matrix is the zero-diagonal matrix
  \(M=(h_{vw})\).  Write \(t_0=r-2\) and \(d=(r-5)!!\).  Its eigenvalue
  on the special-vertex difference line is \(-(t_0-1)d\); on the
  sum-zero subspace of the other \(t_0\) vertices it is \(2d\), with
  multiplicity \(t_0-1\).  On the remaining two constant directions the
  determinant is
  \(-2(t_0-1)^2(t_0+1)d^2\).  Consequently

  \[
  \det M=2^{r-2}(r-3)^3(r-1)((r-5)!!)^{r}\ne0.
  \]

* For \(\gamma=1\), a column relation has
  \(h_{vw}(x_v+x_w)=0\) on every edge.  Since every \(h_{vw}\ne0\), a
  triangle gives \(2x_v=0\), and characteristic zero gives all
  \(x_v=0\).
* For \(\gamma=2\), the ordered colour pattern \((v:2,w:1)\) identifies
  the center, so the columns are independent.

Thus the \(3r\) nonterminal columns in (D) are independent.  The domain
has dimension \(3(r+1)\), and the only kernel is the local \(V_t\).  For
\(K_q=L\dot\cup\{q'\}\) this is \(V_{q'}\); for
\(K_{q'}=L\dot\cup\{q\}\) it is \(V_q\).  After lifting both kernels to
the common union, any simultaneous vector has zero \(L\)-component and
is supported on \(q,q'\) only.

The field qualification matters only as expected.  The construction and
rank statement are asserted over \(\mathbb C\).  The independent checker
records rank \(r\) for the signless-incidence sector over \(\mathbb Q\)
and rank \(r-1\) modulo two, so no characteristic-two conclusion has been
silently imported.

## 5. The sharp \(N=8\) endpoint and failure of the target equations

At \(N=8\), \(r=4\).  The scalar weights are
\(w_{12}=-2\) and all other weights are one, so

\[
 \operatorname{haf}(w)=-2+1+1=0.
\]

The five double cofactors meeting \(\{1,2\}\) equal one and the remaining
cofactor equals \(-2\).  The matrix \(M\) has determinant \(12\).  Each
five-site deletion map has 15 columns, rank 12, and kernel exactly its
opposite local three-port.  Thus the smallest permitted even order is
included without a hidden large-order assumption.

Give the direct \(qq'\)-block any nonzero asymmetric matrix.  It is silent
because its contribution is \(A_{qq'}\otimes P_c=0\), while making the
aggregate support on \(S\) complete.  The full tensor is nevertheless

\[
 H_S=\sum_{\{v,w\}\subset L}2h_{vw}
 e_0^{(q)}\otimes e_0^{(q')}\otimes e_1^{(v)}\otimes
 e_1^{(w)}\otimes e_0^{\otimes(L\setminus\{v,w\})}.    \tag{E}
\]

Every displayed coefficient is nonzero.  Every supported word has two
local colour-one entries and terminal colour zero, so (E) contains no
constant word of colour 0, 1, or 2.  Since it is nonzero, it cannot equal
\(\lambda_c^{-1}e_c^{\otimes S}\) for any \(c\).  This directly checks
that the family fails all three cubic pure-cofactor equations.  It is
therefore a sharp countermodel to the nullity-to-common-kernel inference,
not a GHZ/Krenn source and not a conjecture counterexample.

## 6. Independent exact checker

Frozen audited primary artifacts:

```text
5a51a1ad69ca41076124c92eb5331b23dc11e3683e9d380ac07c0fb930d0fd8a  notes/cubic-nullity-common-cofactor-zero-boundary.md
bfeb8b9968c29218b28834535c9798f15b132f7ac485bc3244ea0457b82be5f2  computations/verify_cubic_nullity_common_cofactor_zero_boundary.py
```

The clean-room checker
[audit_cubic_nullity_common_cofactor_zero_boundary_independent.py](../computations/audit_cubic_nullity_common_cofactor_zero_boundary_independent.py)
does not import the primary verifier.  It independently:

* expands exact perfect-matching tensors from endpoint-ordered blocks;
* checks (A) and (C), including all nine Hessian rows and both endpoint
  orientations, on dense asymmetric integral data;
* verifies the direct-block variation formula;
* proves the determinant identity symbolically and checks scalar hafnians,
  every double cofactor, signless-incidence ranks, full cofactor-map ranks,
  and opposite local kernels;
* tests the physical cancellation family at \(N=8,10,12\), including its
  complete support, silent asymmetric direct block, and mixed tensor; and
* verifies directly that none of the three pure-cofactor equations holds.

Its frozen SHA-256 is

```text
f5b5314753933f63fa1c3544d821d728389cdbfcfdcba777b11f6a96d20a727f  computations/audit_cubic_nullity_common_cofactor_zero_boundary_independent.py
```

Both exact checkers pass.
