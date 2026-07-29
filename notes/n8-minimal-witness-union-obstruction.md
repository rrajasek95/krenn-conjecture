# The three-vertex zero-witness branch at eight sites is impossible

## 1. Statement

Let `B` have eight vertices and suppose

\[
 H_B(A)=\Delta_{B,3}=\sum_{r=0}^2 e_r^{\otimes B}.
\]

Fix an edge `pq` for which `A_pq` is invertible, put
`R=B\setminus\{p,q\}`, and use the cross matrices

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T\qquad(u\in R,\ 0\le r\le2).
\]

By the one-hole identities, every color has at least two zero witnesses,
and by the two-hole determinant identity their union has at least three
vertices.  This note excludes equality.

**Theorem 1 (strict witness-union bound).**  For every invertible edge
`pq` in an eight-site solution,

\[
 \left|\bigcup_{r=0}^2\{u\in R:C_{u,r}=0\}\right|\ge4.       \tag{1}
\]

No genericity, support, rank-one, or noncancellation assumption is used.

## 2. The equality normal form

Assume for contradiction that the union in (1) is a three-set

\[
                         W=\{w_0,w_1,w_2\},
 \qquad Z=R\setminus W.                                  \tag{2}
\]

The minimal three-vertex witness theorem in
[`two-vertex-annihilation-identities.md`](two-vertex-annihilation-identities.md)
gives permutations `sigma,tau:W -> {0,1,2}` and nonzero vectors `a_i,b_i`
such that

\[
 A_{p w_i}=a_i e_{\sigma(i)}^T,
 \qquad
 A_{q w_i}=b_i e_{\tau(i)}^T,                            \tag{3}
\]

and

\[
 \sigma^{-1}(r)\ne\tau^{-1}(r)\qquad(r=0,1,2).           \tag{4}
\]

Thus `tau sigma^{-1}` is one of the two three-cycles.  The argument below
does not require choosing between them.

Put

\[
 g=\alpha^TA_{pq}\beta,
 \qquad
 \mathcal R=\mathbb C[\alpha,\beta]/(g).                 \tag{5}
\]

Since `A_pq` has rank three, `g` is irreducible and `mathcal R` is a
domain.  For `z in Z`, let

\[
 \gamma_z=(\alpha^TA_{pz})\mathbin\times(\beta^TA_{qz}). \tag{6}
\]

There is no zero witness in `Z`.  Consequently every class
`gamma_(z,r)` is nonzero in `mathcal R`: a bilinear form vanishes modulo
`g` only when its coefficient matrix is proportional to `A_pq`.  Indeed,
membership in the principal ideal `(g)` at the same bidegree `(1,1)` allows
only a scalar multiple.  Such proportionality is impossible here unless
the rank-at-most-two cross matrix is zero.

## 3. Reverse-star contradiction

Contract the three sites in `Z` by (6), leave the three sites in `W` open,
and reduce the matching equation modulo `g`.  A matching avoiding `pq`
is killed whenever `p` or `q` is matched to a contracted site.  Hence it
must match `p,q` to two distinct vertices of `W`.

For each `k`, define the common residual vector

\[
v_k=
 \left\langle
 H_{\{w_k\}\cup Z}(A),\bigotimes_{z\in Z}\gamma_z
 \right\rangle
\in V_{w_k}\otimes\mathcal R.                          \tag{7}
\]

This vector is genuinely common to the two ordered star assignments.  Once
`p,q` have been matched to `w_i,w_j`, the unmatched vertex set is exactly
`{w_k} union Z`; neither the remaining edge blocks nor their contractions
remember which of `p,q` used which removed vertex.  Thus reversing
`p w_i,q w_j` to `p w_j,q w_i` changes only the two displayed star factors,
not `v_k`.

Also put

\[
 \lambda_i=\alpha^Ta_i,\qquad \mu_i=\beta^Tb_i.          \tag{8}
\]

All six classes `lambda_i,mu_i` are nonzero in the domain `mathcal R`: the
quadratic principal ideal `(g)` contains no nonzero linear polynomial.
The exact three-hole equation is

\[
 \sum_{r=0}^2 t_r e_r^{\otimes W}
 =\sum_{i\ne j}
   \lambda_i\mu_j\,
   e_{\sigma(i)}^{(w_i)}e_{\tau(j)}^{(w_j)}v_k^{(w_k)},  \tag{9}
\]

where `{i,j,k}={0,1,2}` and

\[
 t_r=\alpha_r\beta_r\prod_{z\in Z}\gamma_{z,r}.         \tag{10}
\]

Every `t_r` is nonzero in `mathcal R`: its cross factors were checked
above, its two coordinate-linear factors are not in `(g)`, and
`mathcal R` is a domain.

Fix a color `r` and set

\[
 i=\sigma^{-1}(r),\qquad j=\tau^{-1}(r),                 \tag{11}
\]

so `i!=j` by (4), and let `k` be the third index.  The ordered assignment
`p w_i,q w_j` is the unique summand in (9) which can produce the constant
word `e_r^(tensor W)`.  Its `r` coefficient at the remaining site is
therefore

\[
             t_r=\lambda_i\mu_j(v_k)_r.                  \tag{12}
\]

In particular `(v_k)_r` is nonzero.

Now reverse the two star assignments, matching `p w_j,q w_i`, and retain
the same `r` component of the same residual vector `v_k`.  It produces the
coordinate word `d` given by

\[
 d_i=\tau(i),\qquad d_j=\sigma(j),\qquad d_k=r.           \tag{13}
\]

This word is not constant: `tau(i)!=r` because `j` is the unique inverse
image of `r` under `tau`.

Moreover this occurrence of `d` in (9) is unique.  Indeed, in any summand
producing `d`, its `p`-partner `w_a` must satisfy `d_a=sigma(a)`.  Equation
(13) and the uniqueness of inverse images show that this holds only for
`a=j`: it fails at `i` because `tau(i)!=sigma(i)=r`, and at `k` because
`sigma(k)!=r`.  Symmetrically, its `q`-partner must satisfy
`d_b=tau(b)`, which holds only for `b=i`.  Thus the coefficient of this
off-diagonal word is exactly

\[
                    \lambda_j\mu_i(v_k)_r.               \tag{14}
\]

The left side of (9) has no off-diagonal word, so (14) is zero.  The first
two factors are nonzero and `mathcal R` is a domain; hence `(v_k)_r=0`,
contradicting (12).  This proves Theorem 1. `QED`

## 4. Exact finite audit

[`verify_n8_minimal_witness_union.py`](../computations/verify_n8_minimal_witness_union.py)
enumerates all twelve pairs `(sigma,tau)` satisfying (4), all six ordered
star assignments, and all three residual coordinates.  For every color it
checks that the constant target word has exactly one source and that its
reversed assignment produces a nonconstant word with exactly one source.
The script audits only the finite coordinate-incidence step; the domain and
matching-decomposition arguments are proved above.
