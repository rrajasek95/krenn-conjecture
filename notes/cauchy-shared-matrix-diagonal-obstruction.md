# The shared-matrix chart is incompatible with the diagonal pair equations

## 1. Outcome

The Cauchy/shared-matrix alternative in
[`hessian-corank-two-osculating-dichotomy.md`](hessian-corank-two-osculating-dichotomy.md)
does not survive the full nine pair equations.  In fact, the additive
Cauchy form of the scalar edge weights is not needed.  The obstruction is
the common nondegenerate colour matrix itself.

Let `W` be the internal even set and suppose that, after invertible changes
of basis at its sites,

\[
                   q_{ij}=w_{ij}H \qquad(i<j),           \tag{1}
\]

where `H` is one invertible symmetric `3 by 3` matrix with zero diagonal.
Let

\[
 p_c=\sum_{i\in W}e_c^{(i)},\qquad s_c=t p_c,qquad t\ne0. \tag{2}
\]

Then the equations

\[
 {p_cs_dq^{r-1}\over(r-1)!}+a_{cd}{q^r\over r!}
                         =\delta_{cd}X_c                 \tag{3}
\]

cannot hold for three linearly independent nonzero tensors `X_0,X_1,X_2`.
Thus alternative 3 of Theorem 6.2 in the preceding note is empty whenever
all the local star matrices `P_i` are invertible.

The proof is uniform in the internal size.  It uses the simultaneous
`SO(H)` colour symmetry of (1).  Modulo the invariant line spanned by
`Q=q^r/r!`, the three off-diagonal equations kill the whole symmetric-square
colour representation, including the three diagonal directions.  The
diagonal equations would then put all three pure targets on the one line
`C Q`, a contradiction.

## 2. The common-matrix normalization is global

Recall the local-full conclusion of equations (37)--(40) in the preceding
note.  There are invertible matrices `P_i`, an invertible symmetric
zero-diagonal matrix `H`, and scalars `alpha_i,b` such that

\[
 P_iHP_j^{\mathsf T}=(\alpha_i+\alpha_j-b)q_{ij}        \tag{4}
\]

for every pair `i<j`.  The left side is invertible.  Consequently

\[
 \alpha_i+\alpha_j-b\ne0,
 \qquad \operatorname {rank}q_{ij}=3                    \tag{5}
\]

for every pair, not only for the edges originally known to belong to
`G_3(q)`.  Applying `P_i^{-1}` at site `i` changes (4) into (1), with

\[
                       w_{ij}={1\over\alpha_i+\alpha_j-b}. \tag{6}
\]

The same changes of basis send the local columns of `p_c` to `e_c`, so
the proportional-star conclusion `s_c=t p_c` becomes (2).  They also send
the three target tensors through one invertible operator on the full tensor
space, and therefore preserve their nonzeroness and linear independence.
Column rescalings made earlier in the osculating argument merely multiply
the three right sides of (3) by nonzero scalars and do not affect the proof
below.

## 3. A colour-equivariant Hessian map

Put `V=C^3` and

\[
 Q={q^r\over r!},\qquad
 \mathcal H_q(Z)={Zq^{r-1}\over(r-1)!}.                 \tag{7}
\]

For `u in V`, write `p(u)=sum_i u^(i)`.  Polarization defines a linear map

\[
 \Phi:\operatorname {Sym}^2V\longrightarrow
          \bigotimes_{i\in W}V_i,
 \qquad
 \Phi(u\mathbin\odot v)=\mathcal H_q(p(u)p(v)).        \tag{8}
\]

No convention concerning the factor two in `u odot v` matters below.

Let

\[
 G=\{g\in\operatorname {SL}(V):gHg^{\mathsf T}=H\}
                         \simeq SO_3(\mathbb C).         \tag{9}
\]

Act by the same `g` at every internal site.  Equation (1) says that this
action fixes `q`, hence fixes `Q`.  Moreover it sends `p(u)` to `p(gu)`.
It follows directly from (8) that

\[
                 g^{\otimes W}\Phi(U)=\Phi(gUg^{\mathsf T}). \tag{10}
\]

Thus `Phi` is a `G`-map and `C Q` is a `G`-submodule.  Let

\[
 \overline\Phi:\operatorname {Sym}^2V
       \longrightarrow\left(\bigotimes_{i\in W}V_i\right)/\mathbb C Q
                                                               \tag{11}
\]

be the induced equivariant map.  This notation also covers `Q=0`, when
the quotient line is simply zero.

Because `t` in (2) is nonzero, the six off-diagonal instances of (3) give

\[
              \overline\Phi(e_c\mathbin\odot e_d)=0
                       \qquad(c\ne d).                  \tag{12}
\]

The key point is that the `G`-span of these three directions is already
all of `Sym^2 V`.

## 4. The three off-diagonal directions generate the full module

We record the elementary representation fact in exactly the form needed.

**Lemma 4.1.**  Let `H` be a nondegenerate symmetric `3 by 3` matrix with
zero diagonal.  Under the congruence action of the group (9), the smallest
invariant subspace of `Sym^2 V` containing

\[
 K=\operatorname {span}\{e_0\mathbin\odot e_1,
                          e_1\mathbin\odot e_2,
                          e_2\mathbin\odot e_0\}         \tag{13}
\]

is all of `Sym^2 V`.

**Proof.**  The invariant trace functional is

\[
                         \tau(U)=\operatorname {tr}(H^{-1}U). \tag{14}
\]

Consequently

\[
 \operatorname {Sym}^2V=\mathbb C H\oplus S_0,
 \qquad S_0=\ker\tau.                                  \tag{15}
\]

The five-dimensional module `S_0` is irreducible for `SO_3(C)`.  One may
see this after a congruence taking `H` to the identity: `S_0` becomes the
traceless symmetric matrices, equivalently the harmonic quadrics in three
variables, the irreducible degree-two spherical representation.  More
elementarily, the three infinitesimal coordinate rotations acting on

\[
 E_{00}-E_{11},\quad E_{00}+E_{11}-2E_{22},\quad
 E_{01}+E_{10},\quad E_{02}+E_{20},\quad E_{12}+E_{21}
                                                               \tag{16}
\]

generate the full `5 by 5` matrix algebra.  The exact row-reduction audit
referenced in Section 6 verifies this last statement.

Since `H` has zero diagonal, `H in K`.  Also `tau(H)=3`, so the restriction
of `tau` to the three-space `K` is nonzero.  It follows that

\[
                         \dim(K\cap S_0)=2.              \tag{17}
\]

Thus the invariant span of `K` contains the invariant line `C H` and a
nonzero vector of the irreducible module `S_0`.  It contains both summands
in (15), proving the lemma. `QED`

## 5. Contradiction from the diagonal equations

The kernel of the equivariant map `bar Phi` is a `G`-invariant subspace.
By (12) it contains `K`, so Lemma 4.1 gives

\[
                         \overline\Phi=0.                \tag{18}
\]

For `c=d`, equation (3) now yields, after quotienting by `C Q`,

\[
                              [X_c]=0                    \tag{19}
\]

for `c=0,1,2`.  Hence all three `X_c` lie in the one-dimensional space
`C Q`.  This is impossible because the three target tensors are nonzero
and linearly independent.  This proves the claimed obstruction.

Notice that no nonvanishing statement about a Cauchy hafnian was used.
All scalar weights `w_ij` may be arbitrary.  Only their shared
nondegenerate colour matrix and the exact off-diagonal and diagonal pair
equations matter.

## 6. Exact audit

[`verify_cauchy_shared_matrix_diagonal_obstruction.py`](../computations/verify_cauchy_shared_matrix_diagonal_obstruction.py)
checks over the rationals that

1. the trace-free intersection in (17) has dimension two for a symbolic
   zero-diagonal invertible `H`; and
2. the associative algebra generated by the three infinitesimal rotations
   on the basis (16) has dimension `25`.

The second calculation implies irreducibility directly: a subspace
invariant under the three rotations is invariant under the algebra they
generate, which is every endomorphism of the five-space.
