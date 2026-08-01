# Pair-pencil rank drop in the level-two differential

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. The level-two differential

Fix a level-two block: vertices \(p,q\) carry the rare colour \(c\), and the
six remaining vertices \(R\) carry the complementary colours \(a,b\). Put

\[
 P_x=\binom{A_{px}[c,a]}{A_{px}[c,b]},\qquad
 Q_x=\binom{A_{qx}[c,a]}{A_{qx}[c,b]},\qquad
 X_x=[P_x\ Q_x].
\]

Let \(M\) be the binary \(\{a,b\}\)-block on \(R\), let
\(\Psi(M)\in\mathbb C^{2^6}\) be its matching tensor, and let \(C_{xy}(w)\)
be the four-vertex cofactor. Expansion by the two rare vertices gives

\[
 z\Psi(M)(w)+
 \sum_{x<y}(P_xQ_y^{\mathsf T}+Q_xP_y^{\mathsf T})_{w_xw_y}C_{xy}(w)=0,
 \tag{1}
\]

where \(z=A_{pq}[c,c]\). With
\(N_{xy}=P_xQ_y^{\mathsf T}+Q_xP_y^{\mathsf T}\), this is exactly

\[
 d\Psi_M\!\left(N+\frac z3M\right)=0.                 \tag{2}
\]

The factor \(1/3\) is Euler's identity: every six-vertex perfect matching
has three edges, so \(d\Psi_M(M)=3\Psi(M)\). Identity (2), exact rank-\(55\)
witnesses, and the resulting generic-kernel statement were independently
reconstructed from the interrupted Claude trace
agent-a1dfcff36e4b0f443. On that dense open locus,

\[
 \ker d\Psi_M
 =\{((\mu_x+\mu_y)M_{xy})_{xy}:\sum_x\mu_x=0\},       \tag{3}
\]

so (2) forces

\[
 N_{xy}=(\nu_x+\nu_y)M_{xy},\qquad z=-\sum_x\nu_x.   \tag{4}
\]

This note closes one exceptional family inside (4). It does **not** claim
that all rank patterns in (4) have been classified.

## 2. The pair-pencil rule at eight vertices

Here is a direct proof of the only universal support rule used below. Fix a
root \(r\), colours \(a\ne b\), and write

\[
 R_u(j)=M_{ru}[a,j],\qquad S_u(j)=M_{ru}[b,j].
\]

Call \(u\) an \(a\)-pure witness when the two-row submatrix is nonzero and
supported only in column \(a\); this does not require both individual rows to
be nonzero. Suppose there is no such witness and the two rows are not
everywhere supported in columns \(a,b\). Choose \(u_*\) and
\(c\notin\{a,b\}\) with
\((R_{u_*}(c),S_{u_*}(c))\ne(0,0)\). Set \(\pi_{u_*}=c\). For any other
neighbour \(u\), set \(\pi_u=\bot\) if
\(R_u(a)=S_u(a)=0\); otherwise choose \(\pi_u\ne a\) for which
\((R_u(\pi_u),S_u(\pi_u))\ne(0,0)\). Such a choice exists because \(u\) is
not \(a\)-pure.

Put \(f_u(T)=1\) when \(\pi_u=\bot\), and otherwise put

\[
 f_u(T)=R_u(\pi_u)+T S_u(\pi_u).
\]

Every factor is a nonzero affine polynomial. Hence
\(P(T)=\prod_{u\ne r}f_u(T)\) is nonzero and has degree at most \(n-1\).
Over \(\mathbb C\), choose \(t\) with \(P(t)\ne0\). Set
\(v_r=e_a+te_b\), \(\rho_u(j)=R_u(j)+tS_u(j)\), and

\[
 v_u=\begin{cases}
 e_a,&\pi_u=\bot,\\
 \rho_u(\pi_u)e_a-\rho_u(a)e_{\pi_u},&\pi_u\ne\bot.
 \end{cases}
\]

Then \(\rho_u\cdot v_u=0\), while every \(v_u(a)\ne0\). In the product-vector
contraction identity, every perfect-matching term dies at its unique edge
incident to \(r\). On the target side, the \(a\)-product is nonzero; every
outside-colour product dies at \(r\), and the \(b\)-product dies at \(u_*\)
because \(v_{u_*}\) is supported on \(\{a,c\}\). This contradiction proves:
missing an \(a\)-pure witness forces preservation of the pair. Swapping
\(a,b\) proves the dichotomy R2: either both distinct pure-column witnesses
exist, or every incident pair of rows is supported in columns \(a,b\).

This argument works for every even \(n\ge2\) over \(\mathbb C\). Over a finite
field, \(|F|\ge n\) suffices. The external Lean artifact proves the rule at
\(n=6\); the proof above is the audited hand extension to \(n=8\).

## 3. What R2 forces in (4)

Suppose four of the \(X_x\) in (4) are invertible and two are zero. At an
invertible \(x\), preservation is impossible because the edges to \(p,q\)
have two independent entries in their \(c\)-columns. Neither endpoint edge
can be a pure-\(a\) or pure-\(b\) witness. An edge to another invertible \(y\)
cannot be one either: (4) makes \(M_{xy}\) invertible. Hence the two zero-\(X\)
vertices must be the two distinct pure-column witnesses.

Call the four invertible vertices \(0,1,2,3\) and the two zero vertices
\(4,5\). Identifying \(a,b\) with \(0,1\), for some
\(\sigma\in\{0,1\}^4\) their blocks have the form

\[
 M_{x4}=u_xe_{\sigma_x}^{\mathsf T},\qquad
 M_{x5}=v_xe_{1-\sigma_x}^{\mathsf T},                \tag{5}
\]

with \(u_x,v_x\ne0\). Since all eight blocks in (5) are nonzero, (4) gives
\(\nu_x+\nu_4=\nu_x+\nu_5=0\) for every live \(x\). The live-live numerator
\(X_xJX_y^{\mathsf T}\) is invertible, so the common live value of \(\nu\) is
nonzero. Consequently \(\nu_4+\nu_5\ne0\), and (4) gives

\[
                              M_{45}=0.                \tag{6}
\]

## 4. Rank-drop theorem

> **Theorem.** Let \(M\) be any binary six-vertex block satisfying (5)--(6),
> with arbitrary live-live blocks. Then
> \(\operatorname{rank}d\Psi_M\le54\). If two values of \(\sigma\) are zero
> and two are one, then \(\operatorname{rank}d\Psi_M\le53\).

There are always five kernel directions

\[
 K^{\mu}_{xy}=(\mu_x+\mu_y)M_{xy},\qquad \sum_x\mu_x=0. \tag{7}
\]

Indeed every matching monomial is multiplied by
\(\sum_{xy\in\mathcal M}(\mu_x+\mu_y)=\sum_x\mu_x=0\). On a dense set these
five directions are independent.

It remains to exhibit directions supported only on live-live edges. Write

\[
 \Omega_{xy}=u_xv_y^{\mathsf T}-v_xu_y^{\mathsf T}.   \tag{8}
\]

If one fibre of \(\sigma\) has at least three members \(i<j<k\), set

\[
 K_{ij}=\Omega_{ij},\qquad K_{ik}=-\Omega_{ik},\qquad
 K_{jk}=\Omega_{jk},                                  \tag{9}
\]

and set all other blocks of \(K\) to zero. When the fibre has size three,
the two possible nonzero dead-colour cofactors reduce, after removing the
singleton factor, to

\[
 \Omega_{ij}u_k-\Omega_{ik}u_j+\Omega_{jk}u_i=0,
 \qquad
 \Omega_{ij}v_k-\Omega_{ik}v_j+\Omega_{jk}v_i=0.      \tag{10}
\]

When the fibre has size four, with remaining vertex \(\ell\), the only
nonzero cofactor gives the four-site Bianchi identity

\[
 \Omega_{ij}(u_kv_\ell+v_ku_\ell)
 -\Omega_{ik}(u_jv_\ell+v_ju_\ell)
 +\Omega_{jk}(u_iv_\ell+v_iu_\ell)=0.                \tag{11}
\]

Both identities follow by expansion; their six or twelve tensor monomials
cancel in pairs. Thus \(d\Psi_M(K)=0\).

For the balanced case, write the two fibres as
\(A=\{a_0,a_1\}\) and \(B=\{b_0,b_1\}\), and give each the signs \(+1,-1\).
There are two directions, supported on the four cross edges:

\[
 K^u_{ab}=\epsilon_a\delta_b\,u_au_b^{\mathsf T},
 \qquad
 K^v_{ab}=\epsilon_a\delta_b\,v_av_b^{\mathsf T}.     \tag{12}
\]

If the dead colours select the same fibre, every cofactor in (12) is zero.
If they select opposite fibres, exchanging complementary indices makes the
two terms equal with opposite signs. Summing first over \(A\) or first over
\(B\) therefore gives zero. Hence both directions lie in the kernel.

For generic \(u_x,v_x\), (9) is nonzero, while the two vectors in (12) are
independent: specialize \(u_x=e_0,v_x=e_1\). No nonzero direction in (7) can
be supported only on live-live edges. Indeed
\(\mu_x+\mu_4=\mu_x+\mu_5=0\) for every live \(x\), together with
\(\sum\mu=0\), forces \(\mu=0\). Generic nullity is therefore at least six,
or seven in the balanced case. All \(55\times55\) minors, and in the balanced
case all \(54\times54\) minors, vanish on a dense open set. As polynomials
they vanish identically, proving the theorem at every specialization.

The checker
[verify_level_two_pair_pencil_rank_drop.py](../computations/verify_level_two_pair_pencil_rank_drop.py)
verifies (9)--(12) over all \(16\) assignments and all \(64\) binary words as
\(1{,}408\) formal polynomial identities. It separately verifies (7), the
transversality calculation, and exact calibration ranks \(35,49,53\) for the
three assignment types. It is stdlib-only and runs in seconds under normal,
optimized, and isolated Python.

## 5. Consequence and remaining obstruction

The four-invertible/two-dead family cannot occur on the rank-\(55\) branch of
(3): the theorem gives rank at most \(54\), and at most \(53\) in the hardest
balanced pattern. The same R2 observation excludes the five-invertible/
one-dead family, because each invertible vertex needs two distinct
noninvertible neighbours.

This is a genuine narrowing, not a solution of \((8,3)\). The interrupted
trace sampled only selected rank patterns and did not classify (4). Moreover
there is an exact rank-\(55\) packet with \(X=P=Q=z=0\) that satisfies the
selected \(64\) level-two equations, all current support rules, no-independent-
four-set, and the stronger slice-cover activity clause, while failing the full
equation system. Thus support consequences alone cannot finish the proof.

The next useful target is a classification-free use of the **other** level-two
blocks: combine (4) for overlapping endpoint pairs with the exact
dead-or-common-scalar relation

\[
 F_c^{st}=A_e[s,t]H_c,
\]

retaining the \(H_c=0\) branch. The abandoned phrase “three-fold
determination” is too strong unless all three slopes \(H_c\) are proved live.

A subsequent exact guard sharpens the trivial selected-block packet:
[level-two-one-sided-rank55-guard.md](level-two-one-sided-rank55-guard.md)
shows that \(Q=z=0\) leaves a \(72\)-dimensional linear family with arbitrary
\(M,P\), including an everywhere-live rank-\(55\) point satisfying the local
pair-pencil exit at every residual vertex. Thus even a nonzero one-sided star
survives every equation in one selected block; the required continuation must
really use an overlapping block or an L0/L1 value equation.
