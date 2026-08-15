# Recovering the direct block and scalar-zero response after labelled GHZ normalization

## Result

Assume the full-rank involution split has passed the labelled GHZ quotient
criterion of `81bbb0f`, and first work in the nondegenerate branch

\[
 q^{[3]}\notin X=\langle X_0,X_1,X_2\rangle.            \tag{1}
\]

Then the normalized endpoint-star bases, the common direct matrix `a`, and
the response cross matrix `K` are recovered exactly.  For a fixed labelled
off-diagonal selected pair `(a,b)`, existence of a residual diagonal scaling
for which

\[
 K=\operatorname {tr}(a)E_{ab}-a_{ab}I                 \tag{2}
\]

has a four-line basis-invariant test.  In any normalized bases, put

\[
 \tau=\operatorname {tr}(a),\qquad \alpha=a_{ab},
 \qquad \kappa=K_{00}.                                \tag{3}
\]

The test is

1. every off-diagonal entry of `K` except `K_ab` is zero;
2. `K_00=K_11=K_22=kappa`;
3. `alpha*tau+kappa*K_ab=0`;
4. in the full-rank layer, `alpha*kappa*det(K)` is nonzero.

These conditions are necessary and sufficient.  A witnessing residual
scaling is

\[
                         {d_a\over d_b}=-{\kappa\over\alpha}. \tag{4}
\]

No target `GL_3` is used.  The labels `a,b` and `X_0,X_1,X_2` remain fixed.

The exact checker is
`computations/verify_h3_labelled_ghz_direct_response_compatibility.py`.

## 1. Exact recovery in the independent branch

Let `C_ij=C(p_i,s_j)` in any bases of the two involution eigenspaces.  Since
the four vectors

\[
                         X_0,X_1,X_2,q^{[3]}             \tag{5}
\]

are independent, there are unique dual functionals on their span satisfying

\[
\begin{aligned}
 \lambda_c(X_d)&=\delta_{cd},&\lambda_c(q^{[3]})&=0,\\
 \eta(X_d)&=0,&\eta(q^{[3]})&=1.                       \tag{6}
\end{aligned}
\]

The checker constructs them on an exact four-coordinate minor.  Define

\[
 B_c=(\lambda_c(C_{ij}))_{ij},\qquad
 D_q=(\eta(C_{ij}))_{ij}.                              \tag{7}
\]

By the labelled GHZ criterion, each `B_c` is nonzero rank one and its three
left and right factor lines are bases.  Choose exact factors

\[
 B_c=\ell_c r_c^{\mathsf T},\qquad
 L=[\ell_0\ \ell_1\ \ell_2],\quad
 R=[r_0\ r_1\ r_2].                                   \tag{8}
\]

The labels fix the order of the columns.  Put

\[
 G=L^{-\mathsf T},\qquad H=R^{-\mathsf T}.             \tag{9}
\]

Then

\[
 G^{\mathsf T}B_cH=E_{cc}.                             \tag{10}
\]

Apply the same changes to the remaining data.  The recovered matrices are

\[
 \boxed{a=-G^{\mathsf T}D_qH},\qquad
 \boxed{K=G^{\mathsf T}J_{PS}H}.                       \tag{11}
\]

The first formula is just the literal row

\[
 C(p_i,s_j)=\delta_{ij}X_i-a_{ij}q^{[3]};              \tag{12}
\]

the second is the cross block of the response form `J` in the same
recovered bases.  Thus no independent operation label or guessed direct
matrix is inserted.

The factorization in (8) has only the expected ambiguity

\[
 \ell_c\mapsto t_c\ell_c,\qquad r_c\mapsto t_c^{-1}r_c.
\]

It becomes the residual normalized-basis torus

\[
 p_c\mapsto d_cp_c,\qquad s_c\mapsto d_c^{-1}s_c.      \tag{13}
\]

Consequently both recovered matrices transform by the same diagonal
conjugation

\[
                         a\mapsto DaD^{-1},\qquad
                         K\mapsto DKD^{-1}.             \tag{14}
\]

## 2. Eliminating the residual torus

For fixed `a != b`, equation (2) after (14) reads entrywise

\[
 {d_i\over d_j}K_{ij}
 =\tau\delta_{ia}\delta_{jb}
  -{d_a\over d_b}\alpha\delta_{ij}.                   \tag{15}
\]

All forbidden off-diagonal entries must therefore vanish, and all diagonal
entries equal one common `kappa`.  The two remaining equations are

\[
 {d_a\over d_b}K_{ab}=\tau,\qquad
 {d_a\over d_b}\alpha=-\kappa.                        \tag{16}
\]

Eliminating the nonzero ratio gives exactly

\[
                         \alpha\tau+\kappa K_{ab}=0.    \tag{17}
\]

In the full-rank branch, `det K !=0`; once the shape conditions hold this is
equivalent to `kappa !=0`.  Equation (16) then also requires `alpha !=0`.
Conversely, (17), the shape equations, and these two opens give the witness
(4).  This proves necessity and sufficiency.

The closed equations are invariant under (14): zero entries and diagonal
entries are unchanged, while (17) is multiplied by the single nonzero
factor `d_a/d_b`.  Thus the test does not depend on the arbitrary scalar
choices in (8).

An entirely polynomial, non-eliminated version adjoins `d_i,e_i` and uses

\[
 d_ie_i=1,                                             \tag{18}
\]

\[
 d_ie_jK_{ij}
 =\tau\delta_{ia}\delta_{jb}
  -d_ae_ba_{ab}\delta_{ij}.                            \tag{19}
\]

Equations (18)--(19) are useful on a Macaulay chart; conditions 1--4 above
are their saturated elimination for the off-diagonal full-rank case.

If `a=b`, residual conjugation fixes both `E_aa` and `a_aa`.  There is no
ratio to choose: one must require literally

\[
                         K=\tau E_{aa}-a_{aa}I.          \tag{20}
\]

## 3. Exact tests

### Positive designed model

The checker starts with dense nonmonomial left and right factor bases, not
with already diagonal slices.  It uses

\[
 a=\begin{pmatrix}1&2&0\\3&4&5\\0&6&7\end{pmatrix},
 \qquad (a,b)=(0,1),
\]

so `tau=12`, `alpha=2`, and the canonical response is

\[
 K=12E_{01}-2I,qquad\det K=-8.                         \tag{21}
\]

It also chooses

\[
                         q^{[3]}=(1,2,3,5),              \tag{22}
\]

relative to three target coordinates and one independent coordinate.  Thus
the recovery must subtract pure components of `q^[3]`; it is not a trivial
coordinate projection.  Exact pivot factorization recovers normalized
slices, `a`, and `K` up to (13), and the invariant test constructs a torus
witness.  Perturbing only the recovered `K_01` by one makes (17) nonzero and
is rejected.

### The physical 77-cell guard

The 77-cell guard remains outside this layer.  Its labelled quotient slices
have ranks `(0,0,1)`, so normalized bases and hence recovered `a,K` do not
exist.  The checker stops at that exact earlier failure.

For separation of obligations, its literal direct block and the
scalar-zero `K` defined from that block do satisfy the orbit test.  This does
not repair the missing two quotient slices: direct/response compatibility is
a later independent condition, not a substitute for labelled GHZ
normalization.

## 4. The `q^[3]` degeneracies

There are two distinct dependent cases.

1. If `q^[3]=0`, the three labelled quotient slices still live in `X` and
   may be normalized, but no functional `eta` with `eta(q^[3])=1` exists.
   Therefore `C` does not determine `a`; the literal direct endpoint block
   must be supplied as extra data before testing (2).
2. If `q^[3]` is nonzero and lies in `X`, quotienting kills one physical
   target direction.  Three fixed labelled GHZ slices cannot be recovered,
   and the decomposition of a cross value into target and `q^[3]`
   coefficients is nonunique.  This branch needs a separate unquotiented
   compatibility system; the criterion and recovery (6)--(11) do not apply.

These are failures of identifiability, not declarations that a physical
solution exists.

## Scope and reproduction

The theorem treats a fixed labelled selected pair and allows no target
`GL_3`.  A simultaneous colour permutation only renames the entire datum;
it is not an extra orbit in the test.  The proof is exact over any field of
characteristic different from two, with the displayed open conditions.

```text
python3 computations/verify_h3_labelled_ghz_direct_response_compatibility.py --mode structural
python3 -O computations/verify_h3_labelled_ghz_direct_response_compatibility.py --mode full
python3 -I -S computations/verify_h3_labelled_ghz_direct_response_compatibility.py --mode exhaustive
```

All modes return the same frozen ledger digest.
