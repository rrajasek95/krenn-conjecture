# A fixed complement plane kills the generic scalar provenance class

Research progress only.  This closes the generic rank-three provenance
class on one branch of the maximal rank-\((1,1)\) scalar shore.  The
common-missing rank-two packet and the fixed dark-shore plane remain open,
so Krenn's conjecture and `SP-CLEAN-BRIDGE` remain open.

## 1. Outcome

Let the six-site residual set be

\[
                 W=A\sqcup B,\qquad
                 B=\{s,u,v\},\qquad |A|=3,
\tag{1}
\]

and retain the scalar clean plane

\[
 {\cal Q}=\{K:\lambda^{\mathsf T}K=0,\ K\mu=0\}.
\tag{2}
\]

The direct scalar vanishes on \({\cal Q}\), and the literal nine rows give
one physical response map \(\Phi:{\cal Q}\to({\cal R}_B)_2\) satisfying

\[
                 \Phi(K)q^{[2]}=\sum_{c=0}^2K_{cc}X_c^W.
\tag{3}
\]

Assume the diagonal map \(\delta(K)=(K_{00},K_{11},K_{22})\) has rank
three.  The released-site theorem supplies, on the complement-plane branch,
one fixed site \(s\in B\) and one fixed colour \(k\) for which

\[
 p_{i,s}(k)=a\lambda_i,\qquad
 t_{j,s}(k)=b\mu_j
 \quad(0\le i,j\le2).
\tag{4}
\]

This note proves

\[
                 \boxed{\ker\delta\subseteq\ker\Phi.}
\tag{5}
\]

In rank three, \(\ker\delta\) is the unique target-free cap line.  Hence the
dual scalar provenance quotient

\[
                  {\ker\delta\over\ker\Phi}
\tag{6}
\]

is zero on this branch.  No assignment-sum row has to be constructed here:
the only cap on which it could be detected already has zero physical
response.  This closes the generic complement-plane alternative of the
scalar shore.  It does not close the rank-two common-missing packet, whose
target-free cap space is two-dimensional, or the alternative in which the
coordinate plane occurs on the dark shore rather than on \(B\).

## 2. The fixed coordinate erases every incident response cell

Write the local response coefficient on an edge \(st\subset B\) as

\[
 \Phi_{st}(K)(k,l)
 =\sum_{i,j}K_{ij}
   \bigl(p_{i,s}(k)t_{j,t}(l)+p_{i,t}(l)t_{j,s}(k)\bigr).
\tag{7}
\]

Using (4) and then (2),

\[
\begin{aligned}
 \Phi_{st}(K)(k,l)
 &=a\,\lambda^{\mathsf T}K\,t_t(l)
   +b\,p_t(l)^{\mathsf T}K\mu\\
 &=0.
\end{aligned}
\tag{8}
\]

Thus every response in the four-dimensional physical family has zero
coefficient whenever it uses colour \(k\) at site \(s\).  This is stronger
than the original cap-dependent coordinate-plane statement: (4) makes it
one fixed-label identity valid for the whole cap plane.

## 3. The opposite edge is completely anchor-provenant

For \(x\in B\), put

\[
                    H_x=q_{A\cup\{x\}}^{[2]}.
\tag{9}
\]

Decomposing (3) by the unique edge of \(\Phi(K)\) in the three-set \(B\)
gives

\[
 \Phi_{uv}(K)H_s+\Phi_{su}(K)H_v+\Phi_{sv}(K)H_u
                    =\sum_cK_{cc}X_c^W.
\tag{10}
\]

Quotient the local space at \(s\) by
\(\Pi_k=\operatorname {span}\{e_c:c\ne k\}\).  Equation (8) kills both
terms incident with \(s\).  Therefore

\[
 \Phi_{uv}(K)\,\overline H_s
                  =K_{kk}X_k^{\{u,v\}}\overline X_k^{A\cup\{s\}}.
\tag{11}
\]

Rank three of \(\delta\) makes the coordinate \(K\mapsto K_{kk}\)
nonzero.  Taking one \(K^{(k)}\) with \(K^{(k)}_{kk}\ne0\) in (11) shows
that \(\overline H_s\ne0\).  Tensor cancellation then gives the exact
family identity

\[
             \boxed{\Phi_{uv}(K)=K_{kk}C_k}
                    \qquad(K\in{\cal Q}),
\tag{12}
\]

for one fixed nonzero pure-\(k\) edge tensor \(C_k\).  In particular every
target-free cap has zero response on the edge opposite \(s\).

## 4. A nonzero target-free response would have a common three-site factor

Let \(K_*\) span \(\ker\delta\), and suppose for contradiction that
\(R_*=\Phi(K_*)\ne0\).  By (12),

\[
                    R_*=(R_*)_{su}+(R_*)_{sv}.
\tag{13}
\]

We first note that both \(H_u\) and \(H_v\) are nonzero.  If, say,
\(H_v=0\), then for each of the two colours \(a,b\ne k\), a normalized
diagonal lift \(K^{(a)},K^{(b)}\) in (10) would give

\[
 \Phi_{sv}(K^{(a)})H_u=X_a^W,\qquad
 \Phi_{sv}(K^{(b)})H_u=X_b^W.
\tag{14}
\]

The same nonzero tensor \(H_u\) cannot be proportional to two distinct pure
coordinate tensors.  Hence \(H_v\ne0\), and symmetrically \(H_u\ne0\).

The target-free equation is now

\[
                   (R_*)_{su}H_v=-(R_*)_{sv}H_u.
\tag{15}
\]

If one response edge vanished, (15) and the nonzero cofactors would force
the other to vanish, contrary to \(R_*\ne0\).  Thus (15) is a nonzero tensor
which is rank one across each of the crossing bipartitions

\[
        su\mid Av,\qquad sv\mid Au.
\tag{16}
\]

The intersection is elementary.  If
\(T=X_{su}\otimes Y_{vA}\), then the rank of its
\(sv\mid uA\) flattening is

\[
        \operatorname {rank}(X_{s\mid u})
        \operatorname {rank}(Y_{v\mid A}).
\tag{17}
\]

Since that rank is one, both factors have rank one.  Consequently there are
nonzero local lines \(L_s,L_u,L_v\) and a nonzero three-site tensor \(G_A\)
such that, after absorbing scalars,

\[
\begin{aligned}
 (R_*)_{su}&=L_sL_u,& H_v&=G_AL_v,\\
 (R_*)_{sv}&=-L_sL_v,& H_u&=G_AL_u.
\end{aligned}
\tag{18}
\]

No common factor was cancelled in the source equation; (18) is forced by
the two literal tensor flattenings.

## 5. The two remaining pure targets contradict the common factor

For either \(c\ne k\), normalize a lift \(K^{(c)}\) so that
\(\delta(K^{(c)})=e_c\).  Equation (12) makes its opposite response edge
zero.  Substitute (18) into (10):

\[
 G_A\bigl(\Phi_{su}(K^{(c)})L_v
          +\Phi_{sv}(K^{(c)})L_u\bigr)=X_c^A X_c^B.
\tag{19}
\]

Across the cut \(A\mid B\), equation (19) forces

\[
                         G_A\in\mathbb C^*X_c^A.
\tag{20}
\]

There are two distinct choices \(c\ne k\).  Their pure three-site tensors
span distinct lines, so (20) cannot hold for both.  This contradiction shows
that \(R_*=0\), proving (5).

## 6. Proof impact and remaining branches

The previous provenance quotient theorem reduced the generic scalar shore
to one target-free response \(R_*\).  The released-site theorem then forced
either a dark coordinate plane or the fixed complement identity (4).  The
argument above closes the latter alternative completely in diagonal rank
three.

The scalar-shore assignment-sum problem is therefore narrower than before:

1. the common-missing rank-two packet, with its fixed-row and fixed-column
   target-free caps; and
2. the fixed dark-shore coordinate plane, which does not directly impose
   (4) on the three-site response support.

Any next overlap theorem should be tested only on those two branches.  A new
generic rank-three assignment-sum construction on the complement-plane
branch would be redundant.

## 7. Exact audit

[`verify_n8_rank11_scalar_fixed_plane_provenance_closure.py`](../computations/verify_n8_rank11_scalar_fixed_plane_provenance_closure.py)
exhausts the 736 rank-three noncoordinate endpoint pairs over
\(\mathbb F_5\) and all three fixed colours.  It checks the four-dimensional
cap plane, the unique target-free cap, and every fixed-coordinate incident
response cell for deterministic arbitrary remaining endpoint entries.  It
also exhausts the crossing-flattening rank identity on all 225 nonzero
\(2\times2\) matrix pairs over \(\mathbb F_2\), and checks the pairwise
disjointness of the three pure three-site lines.  The proof above is uniform
over \(\mathbb C\); the finite computation is a regression audit only.
