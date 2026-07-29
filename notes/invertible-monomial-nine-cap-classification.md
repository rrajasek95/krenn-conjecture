# The invertible-monomial nine-cap boundary

## 1. Outcome

Delete two sites `p,q` and write the exact nine pair slices over the
remaining `2m` sites as

\[
 {\cal H}_q(p_i s_j)+a_{ij}Q=\delta_{ij}X_i,
 \qquad
 Q={q^m\over m!},\qquad
 {\cal H}_q(Z)={Zq^{m-1}\over(m-1)!}.                 \tag{1}
\]

When the direct block `a` is invertible monomial, its permutation has a
literal meaning relative to the diagonal target.  This note records the
two extreme orbits requested here.

* If `a` is diagonal, all six off-diagonal star products are Hessian
  kernel vectors and the three diagonal products lift
  `X_i-lambda_i Q`.
* If `a` is a three-cycle, the three reverse-cycle products are Hessian
  kernel vectors, the three cycle products lift the common line `Q`, and
  the three diagonal products satisfy the uncontaminated factorizations

  \[
                  \boxed{\quad
       p_i s_i{q^{m-1}\over(m-1)!}=X_i.\quad}           \tag{2}
  \]

The nonprincipal `2 by 2` cap minors with a rank-one target do not add a
hidden equation in the three-cycle orbit.  The response rectangle cancels
their quadratic term and each of the three nonzero minors reduces exactly
to one instance of (2).  In the diagonal orbit every nonprincipal
rank-one target cofactor is zero; only the principal two-pure equations
remain.

There is therefore no field-uniform contradiction from the `d=2` minors
and the bare site-graded factorization alone.  Section 4 gives an exact
six-site square-free countermodel satisfying all nine product equations on
the base locus `Q=0`, including every response rectangle.  What it does
not satisfy is the genuinely source-specific condition that its common
degree-four multiplier equal `q^2/2` for one quadratic `q`.  Thus the next
lemma has to use the **power condition**, not unique factorization: the
square-free algebra has zero divisors which invalidate that shortcut.

Two positive restrictions survive this audit.

1. On the gauge-rigid connected nonbipartite rank-three chart, any
   off-diagonal direct entry is impossible.  Hence the three-cycle orbit
   lies entirely in the extra-Hessian-kernel, disconnected/bipartite, or
   zero-row boundary.
2. With only two retained sites, the three-cycle orbit is impossible over
   every field.  A determinant gives a cube equal to a square-free
   coordinate monomial, contradicting unique factorization.  This small
   theorem explains exactly why the same determinant ceases to work after
   more sites are retained: the star response can then have matrix rank
   three.

No actual matching-power countermodel to (1) is asserted here.  In
particular, the formal model of Section 4 is not a Krenn counterexample.

## 2. Exact orbit normal forms

Work in the square-free site algebra

\[
       {\cal R}_U=\bigotimes_{u\in U}(\mathbb F\oplus V_u),
       \qquad |U|=2m,                                   \tag{3}
\]

and retain endpoint order.  Let `p_i` be row `i` of the `p`-star, let
`s_j` be row `j` of the `q`-star, and put

\[
                         r_{ij}=p_i s_j.                 \tag{4}
\]

The common-star construction gives the identities

\[
                   r_{ij}r_{k\ell}=r_{i\ell}r_{kj}      \tag{5}
\]

before any matching power is applied.  Suppose

\[
              a_{i,\sigma(i)}=\lambda_i\ne0,
              \qquad a_{ij}=0\quad(j\ne\sigma(i)).     \tag{6}
\]

Simultaneous permutation of the three target colours conjugates `sigma`.
Diagonal target-preserving rescalings can change the nonzero `lambda_i`,
but it is cleaner, and characteristic-free, to retain them.

For the identity permutation, (1) is precisely

\[
\begin{aligned}
 {\cal H}_q(r_{ii})&=X_i-\lambda_iQ,\qquad &&i=0,1,2,\\
 {\cal H}_q(r_{ij})&=0,&&i\ne j.                       \tag{7}
\end{aligned}
\]

For the cycle `sigma(i)=i+1 mod 3`, it is precisely

\[
\begin{aligned}
 {\cal H}_q(r_{ii})&=X_i,\\
 {\cal H}_q(r_{i,i+1})&=-\lambda_iQ,\\
 {\cal H}_q(r_{i,i-1})&=0,
                       &&i=0,1,2.                       \tag{8}
\end{aligned}
\]

These alternatives include the base locus `Q=0`.  On that locus the
direct block disappears completely from (1), so every monomial orbit has
the same reduced problem

\[
                  {\cal H}_q(r_{ij})=\delta_{ij}X_i.    \tag{9}
\]

Consequently an argument distinguishing diagonal from cyclic `a` must
either prove `Q\ne0` or use information below the top value `Q`.

## 3. Complete `2 by 2` minor audit

For ordered two-sets `I,J`, the uniform cap-minor identity is

\[
 {2\over m!}q^{m-2}
 \det\left(qa_{I,J}+{m\over2}r_{I,J}\right)
 =\sum_{i\in I\cap J}
       \operatorname {Cof}^{I,J}_{ii}(a)X_i.            \tag{10}
\]

Take three distinct colours `i,k,l`, with row set `I=(i,k)` and column
set `J=(i,l)`.  The only possible target term is

\[
             \operatorname {Cof}^{I,J}_{ii}(a)X_i
                         =a_{k l}X_i.                   \tag{11}
\]

In the diagonal orbit `a_kl=0`.  Hence all six nonprincipal minors have
zero target.  A principal set `{i,k}` instead gives

\[
                         \lambda_kX_i+\lambda_iX_k.     \tag{12}
\]

In the three-cycle orbit choose `k,l` so that `l=k+1`; `i` is the third
colour.  The restricted direct block has only its bottom-right entry
`lambda_k`.  Its determinant is

\[
\begin{aligned}
 &\det\begin{pmatrix}
  {m\over2}r_{ii}&{m\over2}r_{il}\\
  {m\over2}r_{ki}&\lambda_kq+{m\over2}r_{kl}
 \end{pmatrix}\\
 &\qquad={m\lambda_k\over2}qr_{ii}
   +{m^2\over4}(r_{ii}r_{kl}-r_{il}r_{ki})
 ={m\lambda_k\over2}qr_{ii},                           \tag{13}
\end{aligned}
\]

where the last equality is the response rectangle (5).  Substitution in
(10) gives

\[
 \lambda_k r_{ii}{q^{m-1}\over(m-1)!}=\lambda_kX_i,    \tag{14}
\]

which is exactly the diagonal equation in (8).  The opposite orientation
has `a_kl=0` and reduces to the corresponding reverse-cycle kernel
equation.  Principal minors also have zero target because all three
diagonal entries of `a` vanish.

Thus every `d=2` member is accounted for: in a monomial chart it is an
alternating packaging of one of the nine first-jet equations, not an
additional constraint.

## 4. Exact square-free countermodel to the divisibility shortcut

The following model keeps both pieces which a naive argument is most
likely to use: one common site-graded multiplier and the literal product
matrix `(p_i s_j)`.  Let

\[
 U=\{u_0,v_0,u_1,v_1,u_2,v_2\},\qquad P_i=\{u_i,v_i\}. \tag{15}
\]

In degree four put

\[
 F=F_0+F_1+F_2,
 \qquad
 F_k=\bigotimes_{w\in U\setminus P_k}e_k^{(w)},         \tag{16}
\]

and take the six linear star rows

\[
                 p_i=e_i^{(u_i)},\qquad
                 s_i=e_i^{(v_i)}.                       \tag{17}
\]

The product `p_i s_j F_k` is nonzero only if both `u_i` and `v_j` are
missing from the support of `F_k`.  Since the three pairs `P_k` are
disjoint, this occurs exactly when `i=j=k`.  Therefore

\[
                         \boxed{p_i s_jF=\delta_{ij}X_i.} \tag{18}
\]

All response rectangles hold identically because `r_ij=p_i s_j`.  If one
formally calls multiplication by `F` the Hessian and sets `Q=0`, (18)
satisfies all nine equations (9), and consequently all the `2 by 2` minor
identities, for both monomial orbits and arbitrary nonzero `lambda_i`.

This refutes the tempting UFD step

\[
 p_i s_iF=X_i\text{ for three }i
       \quad\Longrightarrow\quad F\text{ is a common monomial factor}.
                                                               \tag{19}
\]

The implication fails because distinct missing-site components of `F`
annihilate the wrong star products.  The missing source condition is

\[
                 F={q^2\over2},\qquad Q={q^3\over6}=0   \tag{20}
\]

for one quadratic `q`.  Nothing in (16)--(18) asserts (20).  A valid
impossibility proof must exploit that common-power relation (or an
equivalent lower-cofactor identity).

## 5. A uniform generic-chart exclusion

There is a useful positive conclusion when the internal Hessian has only
its unavoidable vertex gauges.  Work over a field in which `2m` is
nonzero.  Suppose

\[
 \ker {\cal H}_q=
 \{Z^\alpha:(Z^\alpha)_{uv}=(\alpha_u+\alpha_v)q_{uv},
                         \ \sum_u\alpha_u=0\}.          \tag{21}
\]

If `a_{ij}\ne0` for `i\ne j`, the off-diagonal equation gives

\[
                    mp_i s_j+a_{ij}q\in\ker{\cal H}_q. \tag{22}
\]

On an internal rank-three edge `uv`, comparison with (21) gives

\[
 m(p_{i,u}\otimes s_{j,v}+s_{j,u}\otimes p_{i,v})
       =(\alpha_u+\alpha_v-a_{ij})q_{uv}.               \tag{23}
\]

The left side has matrix rank at most two.  Hence on every rank-three
edge

\[
                         \alpha_u+\alpha_v=a_{ij}.       \tag{24}
\]

If their graph is connected and nonbipartite, (24) makes every
`alpha_u=a_ij/2`.  The zero-sum normalization then gives
`m a_ij=0`, a contradiction.  Thus:

**Proposition 5.1.**  On the gauge-rigid connected nonbipartite
rank-three chart, every off-diagonal entry of the direct block is zero.
In particular an invertible three-cycle direct block is impossible.

For a connected bipartite rank-three graph, the same calculation gives
the antipodal branch.  The connected-pair theorem in
`source-hessian-bipartite-rankdrop.md` then says that a solution must have
a literal zero local row on one of the two deleted stars.  Consequently a
three-cycle pair can survive only through an extra Hessian kernel, a
disconnected/low-rank graph, or an actual zero-row boundary.

There is a second, independent all-order restriction.  Every staircase
matrix in `five-set-contamination-normal-form.md` is permutation-similar
to a triangular matrix.  A three-cycle monomial matrix contains a directed
cycle and is not of that form.  Hence Corollary 3.3 of that note gives:

**Proposition 5.2.**  For a three-cycle direct pair and every third vertex,
at least one constant one-cross row is degenerate.  Equivalently, every
triple through that pair carries a pure three-cross selector.  This holds
without a Hessian-rigidity assumption.

The selector overlap is genuine extra data, but it is not converted here
into a lower-order source.

## 6. Field-uniform two-site obstruction for the three-cycle orbit

Let `m=1`, so the retained set is `U={u,v}`.  Contract the two retained
slots by covectors `x,y`.  The target slice at `p,q` is

\[
 D(x,y)=\operatorname {diag}(x_0y_0,x_1y_1,x_2y_2).     \tag{25}
\]

There are only two star assignments: `p` goes to `u` and `q` to `v`, or
the reverse.  Their contracted response is a sum of two rank-one matrices.
Thus (1) implies

\[
                  \operatorname {rank}(D(x,y)-q(x,y)a)\le2
                  \quad\text{for all }x,y.              \tag{26}
\]

For a three-cycle `a`, determinant expansion has only the identity and
cycle permutations:

\[
 \det(D-q(x,y)a)
  =x_0x_1x_2y_0y_1y_2
       -\lambda_0\lambda_1\lambda_2q(x,y)^3.            \tag{27}
\]

Equation (26) makes (27) the zero polynomial.  In the polynomial ring
`F[x_0,x_1,x_2,y_0,y_1,y_2]`, this would make the cube of `q(x,y)` a
nonzero scalar multiple of the product of the six distinct coordinate
variables.  Unique factorization is impossible: every irreducible
valuation on a cube is divisible by three, while every coordinate
valuation on the right is one.  The proof works in every characteristic.

**Proposition 6.1.**  No exact four-site ternary matching tensor has an
invertible three-cycle monomial block on a physical pair, over any field.

For more retained sites the contracted star response is a sum over many
ordered pairs and may have rank three.  Therefore (26), rather than the
factorial normalization, is the precise step which prevents Proposition
6.1 from being an all-order proof.

## 7. Exact audit and next target

Run

```sh
python computations/verify_invertible_monomial_nine_cap.py
```

The checker verifies the two orbit tables, all three nonzero cyclic
`2 by 2` minors after the response rectangles, the six-site square-free
model (18), and the determinant formula (27).

The sharp remaining monomial problem is now:

> exclude the square-free model (18) after imposing simultaneously
> `F=q^(m-1)/(m-1)!` and `qF=mQ`, or use its failure to force a clean
> cap/selector overlap.

That is strictly narrower than the original nine equations and identifies
the common-power condition which the cap-minor hierarchy by itself does
not see.
