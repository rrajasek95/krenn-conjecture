# Independent audit of the shared-matrix diagonal obstruction

## Verdict

The argument in
[`cauchy-shared-matrix-diagonal-obstruction.md`](cauchy-shared-matrix-diagonal-obstruction.md)
is valid.  In particular, none of the following creates a gap:

* the site-dependent normalization by the matrices `P_i`;
* the fact that this normalization no longer leaves the targets in their
  original coordinate-pure form;
* the congruence, rather than conjugation, action on `Sym^2 V`;
* either standard factor convention for `u odot v`; or
* the possible vanishing of `Q`.

The proof uses only that the three transformed targets remain linearly
independent.  It never needs the simultaneous colour symmetry to fix those
targets.

## 1. Audit of the global normalization

Let `T_i=P_i^{-1}`.  A sitewise change by `T_i` sends a block and a star
column according to

\[
 q_{ij}\longmapsto q'_{ij}=T_iq_{ij}T_j^{\mathsf T},
 \qquad p_{c,i}\longmapsto T_ip_{c,i}.
\]

Since the columns of `P_i` are the three vectors `p_{c,i}`, one has
`T_i p_{c,i}=e_c`.  Equation (40) of the osculating note gives

\[
 H=(\alpha_i+\alpha_j-b)q'_{ij}.
\]

The matrix `H` is invertible, so the scalar on the right cannot vanish.
Thus every pair, including a pair not initially known to be in `G_3(q)`,
has

\[
 q'_{ij}=\frac{1}{\alpha_i+\alpha_j-b}H.
\]

This justifies both the global extent of the normalization and the claim
that all normalized blocks have rank three.  If the normalized osculating
argument gives `S_i=tP_i`, then the same change sends `s_c` to `t p_c`.
The standing support assumptions exclude `t=0`.

On top support the change is the single invertible map

\[
                         T=\bigotimes_{i\in W}T_i.
\]

Consequently the right sides become `T X_c`, up to the preceding nonzero
column-rescaling constants.  They need not still equal
`e_c^{\otimes W}`, but they are nonzero and linearly independent because
`T` is invertible.  Linear independence is the only target property used
in Section 5 of the obstruction note.

## 2. Audit of equivariance

With the normalized blocks `q'_{ij}=w_{ij}H`, let

\[
 G=\{g\in SL(V):gHg^{\mathsf T}=H\}.
\]

The simultaneous site action sends a block to
`gq'_{ij}g^T=w_{ij}H`; hence it fixes `q'` and every divided power of
`q'`, including `Q`.  It also sends

\[
 p(u)=\sum_i u^{(i)}\quad\hbox{to}\quad p(gu).
\]

Therefore the symmetric bilinear map

\[
 (u,v)\longmapsto \mathcal H_q(p(u)p(v))
\]
factors through `Sym^2 V` and satisfies

\[
 g^{\otimes W}\Phi(U)=\Phi(gUg^{\mathsf T}).
\]

Because `Q` is fixed, the same identity holds after quotienting the target
by `C Q`.  Thus `ker(bar Phi)` is invariant.  Notice that no assertion that
`g` fixes the three transformed `X_c` is made or required.

## 3. Audit of the `Sym^2 V` module

Under the matrix model for `Sym^2 V`, the action is congruence
`U -> gUg^T`.  The functional

\[
                         \tau(U)=\operatorname{tr}(H^{-1}U)
\]
is invariant: from `gHg^T=H` one obtains
`g^T H^{-1}g=H^{-1}`, and cyclicity of trace gives
`tau(gUg^T)=tau(U)`.  Since `tau(H)=3`,

\[
                  \operatorname{Sym}^2V=\mathbb C H\oplus\ker\tau.
\]

A congruence taking `H` to the identity identifies `ker tau` with the
five-dimensional traceless symmetric-square representation of
`SO_3(C)`, which is irreducible.

Let `K` be the span of the three off-diagonal coordinate tensors.  Under
either convention

\[
 e_c\odot e_d=\tfrac12(e_c\otimes e_d+e_d\otimes e_c)
 \quad\hbox{or}\quad
 e_c\odot e_d=e_c\otimes e_d+e_d\otimes e_c,
\]

`K` is exactly the space of symmetric matrices with zero diagonal.  The
normal-form matrix `H` has zero diagonal, hence `H in K`; the convention
only changes its coordinates by a nonzero scalar.  Moreover `tau(H)=3`,
so `tau|K` is nonzero and `K intersect ker tau` has dimension two.  The
invariant span of `K` consequently contains both `C H` and the whole
irreducible trace-free summand.  It is all of `Sym^2 V`.

## 4. Audit of the equations and the zero-power branch

For `c != d`, proportionality of the stars gives

\[
 t\mathcal H_q(p(e_c)p(e_d))+a_{cd}Q=0.
\]

Here `t != 0`, so the class of each of the three off-diagonal symmetric
directions is killed by `bar Phi`.  (There are six ordered equations but
only three symmetric directions.)  Invariance and the preceding module
calculation force `bar Phi=0` on all of `Sym^2 V`.

For a diagonal equation this implies

\[
                         [X_c]=0\quad\text{modulo }\mathbb C Q.
\]

Thus the three targets lie in a space of dimension at most one, contrary
to their independence.  If `Q=0`, then `C Q={0}` and the quotient is the
unchanged target space; the same argument gives the still stronger
conclusion `X_c=0`.  No division by `Q` or nonvanishing of a hafnian occurs.

## 5. Minimal editorial clarifications

No mathematical correction is needed.  Three small wording changes would
make the proof maximally resistant to misreading:

1. In Section 2, display explicitly
   `q'_{ij}=P_i^{-1}q_{ij}P_j^{-T}` and rename the transformed right sides
   `X'_c`; state that only their independence is retained.
2. After (10), add the one-line calculation
   `g^T H^{-1}g=H^{-1}` proving invariance of `tau`.
3. Replace “when the quotient line is simply zero” after (11) by
   “when `C Q` is the zero subspace, so the quotient is the original target
   space.”

These changes are expository only and do not alter the conclusion.
