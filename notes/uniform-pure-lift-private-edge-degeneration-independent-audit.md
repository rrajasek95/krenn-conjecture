# Independent audit of the uniform pure-lift obstruction

## 1. Verdict

This is a clean-room adversarial audit of
[the uniform pure-lift note](uniform-pure-lift-private-edge-degeneration.md).
The theorem is correct. Its second step is stronger and simpler than an
orbit degeneration: the \(t=0\) map is a **unital local algebra
endomorphism**, so it can be applied directly to the two power equations.
There is no limiting, compactness, or closed-orbit issue.

I found no substantive gap. The response argument retains arbitrary
multi-site rows, both endpoint orders, transverse coordinates, repeated
supports, zero aggregate coefficients, and complex cancellation. The local
projection retains arbitrary endpoint-ordered blocks of \(q\) and arbitrary
local dimensions. Its image falls exactly under the already independently
audited distinct-missing-pair theorem.

The associated filtration in Section 6 of the primary note is also correct,
but it only describes the remaining non-pure jet. It does not claim to close
that branch, and nothing in the pure theorem relies on it.

The standalone
[independent checker](../computations/audit_uniform_pure_lift_private_edge_degeneration_independent.py)
imports neither the primary checker nor project code. It uses a different
site order, bit-mask pairs, site-labelled frozenset words, symbolic row
monomial provenance, and exact Gaussian-integer arithmetic.

## 2. Ambient algebra and exact aggregation

For each site let

\[
 A_u=\mathbb C\oplus V_u,\qquad
 (\alpha,v)(\beta,w)=(\alpha\beta,\alpha w+\beta v).  \tag{A1}
\]

Thus \(V_u^2=0\), and the full algebra is

\[
                  \mathcal R_U=\bigotimes_{u\in U}A_u.              \tag{A2}
\]

Choose a basis of each \(V_u\) beginning with the three independent target
vectors \(e_0^{(u)},e_1^{(u)},e_2^{(u)}\). All later coefficient arguments
refer to the tensor-product basis obtained from these choices. Additional
basis vectors are called transverse; their number is unrestricted.

Parallel sources with the same pair of neighbours and the same ordered
endpoint decoration add in the corresponding coordinate of the edge block.
Sources on the same pair with different endpoint decorations remain different
coordinates of that block. This aggregation is exact: every matching uses at
most one source on a fixed neighbour pair, so expanding a product of aggregate
edge blocks gives exactly the sum over the original parallel-source choices.

The same convention must be used for the pure multiplier. The tensors

\[
 E_c(P)=\bigotimes_{u\notin P}e_c^{(u)}
 \quad(c=0,1,2,\ P\in\tbinom U2)                       \tag{A3}
\]

are linearly independent: different \(P\)'s lie in different four-site
multidegrees, and for fixed \(P\) the three displayed tensors are different
coordinate words. Hence every coefficient \(\lambda_{cP}\) is the unique
aggregate coefficient after all parallel descriptions and complex
cancellation have been combined. Define

\[
                         H_c=\{P:\lambda_{cP}\ne0\}.    \tag{A4}
\]

A coefficient which cancels to zero is not active. A pair may nevertheless
belong to several different \(H_c\)'s; no cross-colour aggregation is made.

## 3. Independent reconstruction of the response argument

Write the arbitrary rows as

\[
 p_i=\sum_{u\in U}p_{i,u},\qquad
 s_j=\sum_{u\in U}s_{j,u},\qquad p_{i,u},s_{j,u}\in V_u. \tag{A5}
\]

Fix \(P=\{a,b\}\). A component at a site outside \(P\) collides with a
factor of \(E_d(P)\) and vanishes by \(V_u^2=0\). Two row components at the
same missing site also vanish. Therefore the complete surviving endpoint
block is, with factors reordered into the named site order,

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
           +s_{j,a}\otimes p_{i,b}.                    \tag{A6}
\]

This derives the two endpoint orders from arbitrary multi-site rows; it does
not assume that the rows were supported at \(a,b\). Define

\[
             \beta_c(P)=(e_c^*\otimes e_c^*)B_{cc}(P). \tag{A7}
\]

Consider first the literal word \(X_c=e_c^{\otimes U}\) in the diagonal
response \(p_cs_cF=X_c\). A contribution with base colour \(d\ne c\) fixes
four sites to the \(d\)-axis, so it cannot produce \(X_c\). For base colour
\(c\), every missing pair contributes exactly
\(\lambda_{cP}\beta_c(P)\). Consequently

\[
                  \sum_P\lambda_{cP}\beta_c(P)=1.      \tag{A8}
\]

Now fix \(d\ne c\) and an active \(P\in H_d\). Inspect the coordinate word

\[
 Y_{c,d,P}(u)=
 \begin{cases}
 e_c^{(u)},&u\in P,\\
 e_d^{(u)},&u\notin P.
 \end{cases}                                           \tag{A9}
\]

Its provenance is unique. If a base-\(d\) term with missing pair \(Q\)
produces it, the four fixed \(d\)-sites \(U\setminus Q\) must be the four
\(d\)-sites \(U\setminus P\), so \(Q=P\). A base-\(c\) term would fix the
\(c\)-axis at four sites although (A9) has it at only two. A term in the
third base colour fixes an axis absent from (A9). Transverse row components
produce transverse coordinate words and cannot enter this coefficient.

The two endpoint monomials that remain are exactly the same two monomials
in (A7), including their order. Since the right side \(X_c\) has zero
coefficient at (A9),

\[
                 \lambda_{dP}\beta_c(P)=0,\qquad
                 \beta_c(P)=0.                         \tag{A10}
\]

No termwise conclusion has been drawn from a multi-term zero sum: (A10)
comes from a word with a single aggregate \((d,P)\)-origin. Internal
cancellation between the two endpoint orders is allowed inside the scalar
\(\beta_c(P)\).

Equation (A10) holds whenever \(P\) is active in any colour other than \(c\).
Deleting those zero summands from (A8) gives

\[
 \sum_{P\in H_c\setminus\bigcup_{d\ne c}H_d}
              \lambda_{cP}\beta_c(P)=1.                \tag{A11}
\]

Thus every colour has a private pair. Choose

\[
              P_c\in H_c\setminus\bigcup_{d\ne c}H_d.  \tag{A12}
\]

The three choices are pairwise distinct: equality \(P_c=P_d\) would make
that pair active in both \(H_c\) and \(H_d\), contradicting privacy. Notice
that only the three diagonal equations among the nine products were needed.
The exact right-side coefficient \(1\), rather than mere nonvanishing of an
unspecified response, is fully retained in (A8)--(A11).

## 4. Direct local projection, including transverse directions

For every site \(u\), define a linear map \(\pi_u:V_u\to V_u\) by

\[
 \pi_u(e_c^{(u)})=
 \begin{cases}
 0,&u\in P_c,\\
 e_c^{(u)},&u\notin P_c,
 \end{cases}                                           \tag{A13}
\]

and let it fix every vector in the chosen transverse complement. Extend it
by \(1\mapsto1\) to \(A_u\). This extension really is a unital algebra
endomorphism: for arbitrary \((\alpha,v),(\beta,w)\in A_u\),

\[
 (1\oplus\pi_u)((\alpha,v)(\beta,w))
 =(\alpha\beta,\alpha\pi_u(w)+\beta\pi_u(v))
 =(1\oplus\pi_u)(\alpha,v)(1\oplus\pi_u)(\beta,w).     \tag{A14}
\]

The potentially missing term \(\pi_u(v)\pi_u(w)\) is zero because all
products inside \(V_u\) are zero. Tensoring the six local maps therefore
gives a unital algebra endomorphism

\[
 \Pi=\bigotimes_{u\in U}(1\oplus\pi_u):
                  \mathcal R_U\longrightarrow\mathcal R_U.        \tag{A15}
\]

For a pure lift \(E_c(P)\), every factor is fixed unless its site belongs
to \(P_c\setminus P\), in which case that factor is killed. Hence

\[
 \begin{aligned}
 \Pi(E_c(P))\ne0
 &\Longleftrightarrow (U\setminus P)\cap P_c=\varnothing\\
 &\Longleftrightarrow P_c\subseteq P\\
 &\Longleftrightarrow P=P_c.                           \tag{A16}
 \end{aligned}
\]

The last equivalence uses \(|P|=|P_c|=2\). In the surviving case the tensor
is fixed, not merely nonzero. It follows coefficientwise that

\[
             \Pi(F)=\sum_{c=0}^2\lambda_{cP_c}E_c(P_c),             \tag{A17}
\]

with three nonzero coefficients and three distinct missing pairs.

No coordinate restriction is placed on \(q\). A block
\(q_{uv}\in V_u\otimes V_v\) may be arbitrary, may have asymmetric endpoint
coordinates, and may contain target and transverse components. The map
\(\Pi\) simply applies \(\pi_u\otimes\pi_v\) to that entire block. Since each
matching power is a sum of products on disjoint sites and \(\Pi\) is an
algebra endomorphism,

\[
             (\Pi q)^{[r]}=\Pi(q^{[r]})\qquad(r=2,3).   \tag{A18}
\]

Therefore a hypothetical \(q^{[2]}=F,\ q^{[3]}=0\) would give, with
\(q_0=\Pi q\),

\[
 q_0^{[2]}=\sum_{c=0}^2\lambda_{cP_c}E_c(P_c),
 \qquad q_0^{[3]}=0.                                   \tag{A19}
\]

This is an affine algebra-map image of the original equations, not a limit
of chosen solutions. Rows are not transformed or normalized and play no
role after (A12).

## 5. Coefficientwise audit of the equivalent nonnegative degeneration

For completeness, replace each zero in (A13) by multiplication by \(t\).
Give the basis vector \(e_c^{(u)}\) weight

\[
                    w_u(e_c)=\mathbf 1_{u\in P_c},     \tag{A20}
\]

and give every transverse basis vector weight zero. A coordinate
\(v_u\otimes v_v\) of an arbitrary edge block of \(q\) then has exponent
\(w_u(v_u)+w_v(v_v)\in\{0,1,2\}\). Thus every coordinate of \(T_t(q)\)
is a polynomial in \(t\), including all components outside the target axes.

For every matching monomial, its edge factors partition the output sites.
Its exponent is consequently

\[
             \sum_{u\text{ in the output word}}w_u(v_u),           \tag{A21}
\]

independent of which matching produced that word. This proves
coefficientwise functoriality even in the presence of cancellation: all
contributions to one output coordinate carry the same power of \(t\).
It also proves that setting \(t=0\) commutes with both matching powers.

For a pure lift,

\[
 \operatorname{val}_t T_t(E_c(P))
 =|P_c\cap(U\setminus P)|=|P_c\setminus P|.            \tag{A22}
\]

This is zero exactly for \(P=P_c\), and is one or two otherwise. Thus the
nonnegative one-parameter argument is sound, but the direct specialization
\(T_0=\Pi\) in Section 4 makes orbit closure and source divergence irrelevant
from the outset.

## 6. Scope of the imported obstruction

[The distinct-missing-pair theorem](distinct-missing-pair-common-power-obstruction.md),
with its
[independent audit](distinct-missing-pair-common-power-obstruction-independent-audit.md),
states over every field of characteristic different from two that no
quadratic has square

\[
       \lambda_0E_0(P_0)+\lambda_1E_1(P_1)+\lambda_2E_2(P_2)
\]

and vanishing cube when the three pairs are distinct and all three scalars
are nonzero. It explicitly allows arbitrary local dimensions and arbitrary
endpoint-ordered tensors in the quadratic. Equation (A19) meets every one
of these hypotheses over \(\mathbb C\). The theorem is power-only and was
proved before the present private-pair argument, so its invocation is not
circular. This contradiction proves the uniform pure-lift obstruction.

The conclusion is exactly the \(45\)-dimensional span of (A3). For a
general degree-four \(F\), the projection \(\Pi(F)\) can also retain mixed
coordinate words of weight zero. It then need not equal the three-term
right side of (A19), so the distinct-pair theorem cannot be invoked. The
finite coefficient equations in Section 6 of the primary note correctly
record this non-pure jet as a next frontier; they do not close it.

More explicitly, if \(T_t(p_i)=p_i^{(0)}+tp_i^{(1)}\), similarly for
\(s_j\), and \(T_t(F)=\sum_{r=0}^4t^rF^{(r)}\), then
\(T_t(X_i)=t^2X_i\). Convolution gives exactly the primary note's orders
zero, one, and two, and every higher-order coefficient of the transformed
product is zero. The analogous quadratic and cubic expansions are finite
because all local weights are zero or one. No assertion about the
solvability of that remaining hierarchy is used here.

## 7. Adversarial cases

### Repeated supports and nonreal weights

The repeated-pair exception to the power-only theorem is sharp over the
complex numbers, not merely at unit real weights. On sites \(0,1,2,3\), use
the three one-factors

\[
 \{01,23\},\qquad\{02,13\},\qquad\{03,12\}
\]

in colours \(0,1,2\). Give their two edges respectively the weights

\[
 (1+i,\,2-i),\qquad(-i,\,3+2i),\qquad(2,\,1+3i).       \tag{A23}
\]

Any two edges in different one-factors meet, while the two edges in one
factor are disjoint. On a six-set, with \(P=\{4,5\}\), the resulting
quadratic therefore satisfies exactly

\[
 q^{[2]}=(3+i)E_0(P)+(2-3i)E_1(P)+(2+6i)E_2(P),
 \qquad q^{[3]}=0.                                     \tag{A24}
\]

All three missing pairs are the same. This does not challenge the audited
proof: the product equations force private pairs before projection, whereas
(A24) has none.

### Parallel sources and zero aggregates

Combining parallel sources is done separately in each ordered endpoint
coordinate. Exact cancellation can delete one coordinate without deleting
other decorations on the same neighbour pair. The checker expands a family
of parallel, asymmetrically decorated sources before aggregation and verifies
that its square agrees exactly with the square of the aggregate edge tensor.
It also checks a Gaussian-integer pure coefficient that cancels to zero and
a pair shared by two nonzero colour aggregates. Thus neither parallelism nor
zero coefficients are silently replaced by a simple support graph.

### Complex cancellation

The proof uses no positivity, ordering, conjugation, or genericity. Its only
division is the inference from \(\lambda_{dP}\beta_c(P)=0\) with the
aggregate \(\lambda_{dP}\ne0\). Equation (A11) permits arbitrary cancellation
among private terms; it uses only that a finite sum equal to \(1\) cannot have
an empty index set.

### Nonclosed or divergent orbits

There is no orbit quotient. The projection \(\Pi\) is defined everywhere and
is applied once to a fixed \(q\). In the equivalent \(T_t\) description every
coordinate exponent is nonnegative, so \(T_t(q)\) has an affine limit as
well. No inverse rescaling of \(q\) or of the rows occurs.

## 8. Independent machine audit

Running

    uv run python computations/audit_uniform_pure_lift_private_edge_degeneration_independent.py

checks the following exact data:

* \(20{,}250\) symbolic row-monomial provenance terms across all nine
  responses, including both endpoint orders and two independent transverse
  labels;
* disjoint response-word spaces for different base colours and the exact two
  monomial origins of every shared-pair word;
* all \(15^3\) possible selected-pair triples and the \(2{,}730\) pairwise
  distinct triples allowed by privacy;
* every pure-lift valuation and every target/transverse edge-coordinate
  valuation for those \(2{,}730\) triples;
* the ordered graph census \(90,1080,1080,360,120\) for
  \(3K_2,P_3\sqcup K_2,P_4,K_{1,3},K_3\);
* symbolic incidence vectors for all four-site and six-site matchings, which
  certify (A21) for arbitrary local coordinate weights;
* exact parallel-source aggregation with asymmetric endpoint decorations;
  and
* the nonreal repeated-pair \(K_4\) witness (A23)--(A24).

These finite checks support the bookkeeping. The arbitrary-dimensional
proof is the algebraic argument in Sections 2--6 above.
