# Generic source recovery from one cross moment at all odd orders at least seven

Research note, 2026-09-27. Written proof with an exact base certificate,
rational checks of a fixed nine-dimensional calculation, and supporting
deformation checks. Not Lean formalized or independently peer reviewed.
The Krenn–Gu manuscript is unchanged.

## 1. The result

**Theorem 1 (single-output source identifiability).** Let `n>=7` be odd,
and let each local vector space have dimension at least three. For a
generic complex source, its single Gaussian cross-moment tensor

$$
T=\mathbb E[X_1\otimes\cdots\otimes X_n]
$$

determines all local means and all cross-site covariance blocks, up to

$$
\mu_i\mapsto\lambda_i\mu_i,\qquad
R_{ij}\mapsto\lambda_i\lambda_jR_{ij},\qquad
\lambda_i\ne0,\quad\prod_i\lambda_i=1.
$$

Here the complex model means the polynomial Gaussian matching expansion;
it does not require a complex probability distribution. Uniqueness is
against every alternative source representation, including exceptional
ones. A representative is rational in the observed tensor on suitable
charts. No lower moments or mean directions are supplied.

At five sites, the generic single-output fiber has exactly two such
classes. Their means agree, and the covariance quadratics are related by
`R -> -R-mu^2/3`. Two generic outputs with a shared covariance remove
that ambiguity.

The five-site statement, calibration, and global covariance-rigidity
argument were proved in the earlier notes. The new result here is an
all-orders proof of their remaining rank hypothesis. The proof separates
exact identifiability from efficient or stable estimation: it does not
give a polynomial-time bound in `n`, a noise guarantee, or a classification
of nongeneric fibers. Within-site covariance blocks remain unobservable.

## 2. The remaining rank hypothesis

First work with `V_i=C^3`, basis `x_i,y_i,z_i`, and normalize mean-line
representatives to `x_i`. In the commutative site algebra
`tensor_i(C direct_sum V_i)`, with `V_i V_i=0`, put

$$
L=\sum_i x_i,\qquad R=\sum_{i<j}R_{ij},\qquad
T=[\exp(L+R)]_{\mathrm{full}}.
$$

The subscript selects the component using every site once. Thus `T`
sums matchings, using the mean at each unmatched site. Write

$$
k=\frac{L^n}{n!},\qquad e=\frac{L^{n-2}}{(n-2)!}R.
$$

These are the terminal and one-edge responses. Let `F_d` be the space
of tensors with at most `d` factors outside the mean lines. The exterior
matrix is

$$
A(T)_{a,b}=\sum_c T_c\prod_i\epsilon_{a_i b_i c_i},
\qquad a,b,c\in\{0,1,2\}^n.
$$

The copy identity gives `A(T)k=A(T)e=0` and annihilates every response
layer. The [restricted-kernel criterion](single-output-covariance-low-degree-2026-09-27.md)
proves that the only remaining order-dependent condition needed for
Theorem 1 is

$$
\ker A(T)\cap F_3=\mathbb Ck+\mathbb Ce. \tag{1}
$$

**Theorem 2 (all-orders restricted-kernel rank).** For every odd `n>=7`,
(1) holds generically. A witness exists even with

$$
R_{ij}\in U_i\otimes U_j,\qquad U_i=\mathrm{span}(y_i,z_i). \tag{2}
$$

Condition (2) is used only to build witnesses. The conclusion is generic
in the unrestricted source parameter space. At five sites (1) was already
certified in the preceding note.

The proof of Theorem 2 adds two sites at a time. We first establish the
auxiliary conditions needed at an old source, at every order. This avoids
assuming that an auxiliary rank persists merely because it holds in one
degeneration.

## 3. A local edge-row calculation

**Lemma 3 (two-row multiplication).** Let `s>=6` be even and let each
site have dimension two. For generic linear rows `L_1,L_2` and generic
cross-site quadratic `C`, the map

$$
(U_1,U_2)\longmapsto
 (U_1L_2-U_2L_1)\frac{C^{(s-2)/2}}{((s-2)/2)!} \tag{3}
$$

has kernel exactly the one-dimensional span of `(L_1,L_2)`.
Each unknown `U_a` is an arbitrary
row in the direct sum of the local spaces, so the domain has dimension
`4s` and the rank is `4s-1`.

**Proof by an all-orders witness.** At site `i` use coordinates `x_i,y_i`
and take

$$
L_1=\sum_i x_i,\quad L_2=\sum_i y_i,\quad
C=\sum_{i<j}(x_ix_j+r_ir_jy_iy_j),\quad
p_i=r_i^{-1}=1+\frac{i}{s+1}. \tag{4}
$$

Thus the `p_i` are distinct real numbers in `(1,2)`. Write
`U_1=sum_i(a_i x_i+b_i y_i)` and
`U_2=sum_i(c_i x_i+d_i y_i)`.
Diagonal covariance separates outputs with odd and even numbers of `y`
coordinates. All matching-count factors used below are nonzero.

For an output with its sole `y` at `j`, vanishing gives

$$
A-a_j-(s-1)d_j=0,\qquad A=\sum_i a_i. \tag{5}
$$

Summing shows `sum_i d_i=A`. For an output whose sole `x` is at `i`,
divide out the nonzero matching coefficient and product of the `r_j`.
The resulting equation is

$$
a_i(P-p_i)-(D_p-p_id_i)=0,\quad
P=\sum_i p_i,\quad D_p=\sum_i p_id_i. \tag{6}
$$

Set `delta_i=d_i-A/s` and `delta D=sum_i p_i delta_i`. Equations
(5)–(6) yield

$$
\delta_i((s-1)P-sp_i)=-\delta D,\qquad \sum_i\delta_i=0.
$$

Every coefficient `(s-1)P-sp_i` is positive: it exceeds `s(s-3)`.
Summing their reciprocal-weighted equations forces `delta D=0`, and
then every `delta_i=0`. Thus all `a_i,d_i` equal one common scalar.

For the even outputs, the all-`x` coefficient gives `sum_i c_i=0`.
An output with `y` exactly at `i,j` then gives

$$
b_i+b_j+r_ir_j(c_i+c_j)=0. \tag{7}
$$

Put `u_i=b_i/r_i`. These equations become
`p_j u_i+p_i u_j+c_i+c_j=0` for every pair.
Subtract the equations involving indices `1` and `2` to express
`u_i=A_0p_i+B_0` and `c_i=C_0p_i+D_0` for `i>=3`.
For pairs among three of those remaining indices,

$$
2A_0p_ip_j+(B_0+C_0)(p_i+p_j)+2D_0=0.
$$

The three coefficient rows are independent for three distinct values
`a,b,c`: their determinant is `4(a-b)(a-c)(b-c)`. Hence
`A_0=D_0=0` and `C_0=-B_0`. The equations with indices `1,2` then
give the same formulas there: `u_i=B_0,c_i=-B_0p_i` for all `i`.
The already known sum of the `c_i` is zero, so `B_0=0`.
All `b_i,c_i` vanish. The kernel is exactly the common scalar multiple
of `(L_1,L_2)`. Rank openness proves the generic statement. QED.

**Corollary 4 (one relation in each vertex row).** For a generic
outside-only source (2), at every odd `n>=7`, fix a vertex `j`.
Restrict `A(T)` to columns with two outside factors, one at `j`, and
rows with their unique zero colour at `j`. This local matrix has
`4(n-1)` columns and a one-dimensional kernel, spanned by the source's
incident outside covariance blocks.

**Proof.** At vertex `j`, let `L_1,L_2` be the two rows of its incident
covariances, viewed as linear rows on the other `s=n-1` sites. Let
`U_1,U_2` be the corresponding unknown edge rows. The alternating symbol
at `j` takes `U_1L_2-U_2L_1`; the other sites contribute their centered
matching tensor. After invertible local changes by the two-dimensional
alternating forms, the restricted map is exactly (3). Its kernel is the
incident source row itself. Lemma 3 supplies a witness for each fixed
vertex, since incident blocks and the remaining covariance are free
parameters. The finitely many resulting open sets intersect. QED.

## 4. Six independent antisymmetric classes

Continue with an outside-only source and write `A=A(T)`. Choose four
distinct old sites, numbered `1,2,3,4`, and vary the mean at each in its
`y` direction. For the corresponding derivative `partial_alpha`, define

$$
f_\alpha=\partial_\alpha T,\quad
h_\alpha=\partial_\alpha k,\quad
v_\alpha=\partial_\alpha e,\quad
h_{\alpha\beta}=\partial_\alpha\partial_\beta k.
$$

Their outside degrees are respectively variable, one, three, and two.
In particular `h_(alpha beta)` are six distinct coordinate tensors.

Differentiating the universal copy identities gives

$$
A(f_\alpha)k=-Ah_\alpha,\qquad
A(f_\alpha)e=-Av_\alpha. \tag{8}
$$

Put `O_(alpha beta)=A(f_alpha)h_beta`. Only the all-outside part of
`f_alpha` contributes, so this vector is supported on rows whose sole
zero colour occurs at site `beta`. Also,

$$
O_{\alpha\alpha}=0,\qquad
O_{\alpha\beta}+O_{\beta\alpha}=-Ah_{\alpha\beta}. \tag{9}
$$

For the second identity, differentiate `A(T)k=0` twice. The additional
term `A(partial_alpha partial_beta T)k` vanishes: after projecting every
old site outside its mean, the remaining `n-2` centered sites have odd
cardinality. This observation will also eliminate a second-order term
in the attachment calculation.

**Lemma 5 (six independent classes).** Under Corollary 4 and nonzero
outside blocks, the six classes

$$
[O_{\alpha\beta}]\quad(1\le\alpha<\beta\le4)
       \quad\text{modulo }A(F_3) \tag{10}
$$

are independent.

**Proof.** The source tensor has only even outside degrees. Since the
number of sites is odd, its exterior matrix preserves outside parity.
The vectors `O` have even parity. Consequently a relation modulo
`A(F_3)` is already a relation modulo `A(F_2)`.

In the row with its sole zero at vertex `j`, such a relation alters
the usual edge equations only on the six selected edges between the
four sites, and only at one endpoint of each selected edge. By
Corollary 4, the remaining local edge row must be a scalar `lambda_j`
times the incident source row.

On every unselected edge, comparison at its two endpoints gives
`lambda_i R_ij=lambda_j R_ij`, so `lambda_i=lambda_j`. The complete
graph with the six selected edges removed is connected (there are
vertices outside the four selected sites). All these scalars coincide.
Comparing endpoints of a selected edge now makes its extra coefficient
zero. This applies to all six coefficients in the proposed relation.
QED.

**Lemma 6 (four response derivatives).** Generically the four vectors
`v_alpha` are independent, at every order considered.

**Proof.** More strongly, all `2n` derivatives in the local outside
directions are independent at
`R=sum_(i<j)(y_i y_j+z_i z_j)`. In their outside-triple coefficients,
an entry with `y` at `i` and `z` at two other sites reads only the
`y_i` derivative coefficient. Interchange the colours to read the other
coefficient. Rank openness gives the claim. QED.

## 5. Fixed algebra on the two new sites

At the two new sites use the same coordinate basis `x,y,z`. Identify
their tensors with three-by-three matrices, with row-major vectorization.
Set

$$
w=x\otimes x=E_{00},\qquad
B=y\otimes y+z\otimes z=E_{11}+E_{22},\qquad S=w+B=I_3,
$$

$$
M_1=E_{10},\quad M_2=E_{20},\quad M_3=E_{01},\quad M_4=E_{02}.
$$

Let `D=A(S)` and `D_alpha=A(M_alpha)`, where these are now the
two-site exterior operators, each a nine-by-nine matrix. Unlike the
old odd-site operation, the two-site operation is symmetric in its two
tensor arguments.

**Lemma 7 (pair algebra).** The following identities and kernel
statements hold over the rationals:

1. `D(X)=tr(X) I-X^t`, so `D^-1(Y)=(tr(Y)/2) I-Y^t`.
2. `D^-1 D_alpha(w)=0` and `D^-1 D_alpha(B)=M_alpha`.
3. If `C` has outside degree at most one and every
   `D^-1 D_alpha(C)` is a scalar multiple of `w`, then `C` is also
   a scalar multiple of `w`.
4. The common kernel of
   `D_alpha D^-1 D_beta-D_beta D^-1 D_alpha`, for `alpha<beta`,
   is precisely `span(w,B)`.
5. `D^-1 D_1(M_4)=-E_12`, a nonzero tensor with two outside factors.

**Proof.** The first two formulas follow by contracting the two
alternating symbols. For part 3, write
`C=cw+u tensor x+x tensor v`, with `u,v in span(y,z)`. The images
under `D_alpha` of the latter terms are outside rank-one matrices.
They cannot be nonzero scalar multiples of `D(w)=B`, which has rank
two. Thus `u=v=0`.

For part 4, direct substitution gives the seven independent equations

$$
X_{01}=X_{02}=X_{10}=X_{20}=X_{12}=X_{21}=0,\qquad X_{11}=X_{22}.
$$

The two free coordinates are exactly `w,B`. The final formula is one
more substitution. The replay records rational rank minors and the
row-reduced commutator equations, so this fixed calculation does not
depend on modular sampling. QED.

## 6. The rank induction

**Proposition 8 (two-site extension of (1)).** Suppose (1) holds at
some outside-only source on an odd `n>=7`. Then it holds at some
outside-only source on `n+2` sites.

**Choice of old source.** The rank hypothesis defines a nonempty open
set in the irreducible parameter space of outside blocks. Corollary 4
and Lemma 6 give additional nonempty open sets at every order. Choose
an old source in their intersection, with every outside block nonzero.
It satisfies Lemma 5 as well. Notice that these auxiliary conditions
were proved independently at all orders, not inferred by extrapolating
the old source's numerical ranks.

**Attachment.** Give the new sites means `x,x` and covariance block
`B`. Their two-site moment is `S=I_3`. Add four cross entries of common
weight `t`: from the chosen `y` coordinate at old sites `1,2` to `y,z`
at the first new site, and from old sites `3,4` to `y,z` at the second.
All covariances still satisfy (2).

The tensor is a polynomial of degree at most two in `t`:

$$
T(t)=T\otimes S+t\sum_\alpha f_\alpha\otimes M_\alpha+t^2T_2.
\tag{11}
$$

There cannot be more than two cross edges in a matching. Moreover,

$$
A(T_2)(k\otimes X)=0\quad\text{for every new-site tensor }X, \tag{12}
$$

by the same odd centered-site argument used after (9).

We analyze a formal series `U(t)=U_0+tU_1+t^2U_2+...` in the fixed
space `F_3` satisfying `A(T(t))U(t)=0`. Only its first three coefficients
are needed. At order zero the operator is `A tensor D`. By (1) and
outside-degree comparison,

$$
U_0=k\otimes X+e\otimes C,\qquad C\in F_1(\text{new pair}), \tag{13}
$$

where `X` is an arbitrary three-by-three matrix. This initial kernel
has dimension `9+5=14`.

### 6.1 First order

Using (8), the first-order equation is equivalent to

$$
U_1-\sum_\alpha h_\alpha\otimes D^{-1}D_\alpha X
    -\sum_\alpha v_\alpha\otimes D^{-1}D_\alpha C
        \in\ker(A\otimes D). \tag{14}
$$

For a new-pair coordinate with one or two outside factors, the allowed
old part of `U_1` has degree at most two or one. The other displayed
terms have old degrees one and three, respectively. Every old coefficient
of (14) belongs to `F_3`, so its kernel part lies in `span(k,e)`.
Comparing old degree three and using Lemma 6 gives

$$
D^{-1}D_\alpha C\in\mathbb Cw\quad\text{for every }\alpha.
$$

Lemma 7 forces `C=cw`, and these four images are then zero. Thus the
first-order equations remove four of the fourteen possible directions.

The full one-edge response of the attached source is the exact kernel
vector

$$
e(t)=e\otimes w+k\otimes B+t\sum_\alpha h_\alpha\otimes M_\alpha.
\tag{15}
$$

Subtract `c e(t)`. We may therefore assume `U_0=k tensor X` and

$$
U_1=\sum_\alpha h_\alpha\otimes D^{-1}D_\alpha X
                       +k\otimes X_1+e\otimes C_1,
\qquad C_1\in F_1(\text{new pair}). \tag{16}
$$

The last degree restriction follows again from `U_1 in F_3`.

### 6.2 The commutator obstruction at second order

Project the second-order equation onto the quotient by `A(F_3)` in
the old factor. Its `A tensor D` term vanishes there, and (12) removes
the `T_2` term. The two last terms in (16) also vanish in this quotient
after applying the first-order operator, by (8).

Using (9), the remaining equation is

$$
\sum_{\alpha<\beta}[O_{\alpha\beta}]\otimes
 (D_\alpha D^{-1}D_\beta-D_\beta D^{-1}D_\alpha)X=0.
$$

Lemma 5 makes its six old coefficients independent. Lemma 7 therefore
gives `X in span(w,B)`. Subtract a terminal kernel vector to reduce to

$$
U_0=\lambda k\otimes B. \tag{17}
$$

This removes seven further directions. One covariance direction remains
to be excluded; the commutator calculation alone would not suffice.

### 6.3 The last second-order obstruction

Every `T(t)` has even outside parity, so `A(T(t))` preserves that parity.
We can replace `U(t)` by its even part without changing (17). Equation
(16) then has `C_1=c_1w`, since `e` has degree two and `C_1` had degree
at most one. Lemma 7 gives

$$
U_1=\lambda\sum_\alpha h_\alpha\otimes M_\alpha
                              +k\otimes X_1+c_1e\otimes w.
$$

Use the symmetry `D_alpha M_beta=D_beta M_alpha`, (9), and (12) in
the unprojected second-order equation. With

$$
F_{\alpha\beta}=D^{-1}D_\alpha M_\beta,
$$

it follows that

$$
U_2-\lambda\sum_{\alpha<\beta}h_{\alpha\beta}\otimes F_{\alpha\beta}
       -\sum_\alpha h_\alpha\otimes D^{-1}D_\alpha X_1
                   =k\otimes X_2+e\otimes C_2 \tag{18}
$$

for some matrices `X_2,C_2`. This use of (1) is legitimate: every old
coefficient on the left belongs to `F_3`, even though the displayed
tensor before cancellation may have total outside degree four.

Fix a new-pair coordinate with two outside factors. Its old part in
`U_2` has degree at most one. Comparing degree two in (18) gives

$$
\lambda\sum_{\alpha<\beta}h_{\alpha\beta}
                    (F_{\alpha\beta})_{ab}+e(C_2)_{ab}=0.
\tag{19}
$$

The six `h_(alpha beta)` use only the selected four old sites. The
one-edge tensor `e` has a nonzero coefficient on an edge involving a
fifth old site. That coefficient in (19) forces `(C_2)_(ab)=0`.
The six coordinate tensors are independent, so
`lambda (F_(alpha beta))_(ab)=0` for every pair and every outside
new coordinate. Lemma 7 gives `F_14=-E_12`, forcing `lambda=0`.

We have proved that the leading term of every formal kernel vector lies
in the span of the two genuine leading responses `k tensor w` and
`e tensor w+k tensor B`.

### 6.4 Why the formal calculation proves a rank witness

If the kernel over `C(t)` had dimension more than two, impose two
constant linear normalizations separating those genuine leading
responses. A nonzero rational kernel vector satisfying both would
remain. Clear denominators and divide out its lowest power of `t`.
It gives a formal kernel vector with nonzero leading term satisfying
the same two normalizations. The conclusion just proved forces that
leading term to be zero, a contradiction.

Thus the generic kernel in the family has dimension at most two.
The two universal responses give equality. A corresponding maximal
minor is a nonzero polynomial in `t`, so some specialization is a rank
witness at `n+2`. Proposition 8 follows. QED.

## 7. Completing the theorem and shared-source recovery

**Proof of Theorem 2.** The exact seven-site outside-only source in the
certificate has `rank(A(T)|_(F_3))=377`, with `dim F_3=379`.
Proposition 8 therefore gives witnesses at every odd order at least
seven. A nonzero minor makes the property generic in the outside-only
family and hence supplies a witness in the unrestricted family as well.
The universal two-dimensional kernel gives the matching generic upper
rank bound. QED.

**Proof of Theorem 1.** Combine Theorem 2 with the all-orders
[mean-direction theorem](mean-direction-recovery-all-orders-2026-09-27.md)
and the global [covariance-rigidity criterion](single-output-covariance-low-degree-2026-09-27.md).
The latter reconstructs `aR+bL^2` using two linear correction systems,
then applies the [single-output calibration formulas](calibrated-source-reconstruction-all-orders-2026-09-27.md#4-one-calibrated-output-the-threshold-is-seven-sites).
At odd orders at least seven, the cubic, fifth, and seventh response
coordinates determine the calibration uniquely and rationally.

Unequal local dimensions at least three follow by overlapping
three-coordinate views, using a common nonzero mean coordinate to align
site scalings and two-site coordinate replacements to cover every edge
entry. The five-site fiber and its removal by two outputs are the
previously proved covariance involution and alignment results. QED.

**Corollary 9 (shared covariance and observed mean spaces).** At every
odd `n>=7`, any finite generic labelled family of cross moments with a
shared covariance determines that covariance and all its actual mean
rows, up to one common product-one site scaling. In particular, it
determines the span of the observed mean rows. No response-span input
or bound relating the number of mean directions to local dimension is
needed beyond local dimension at least three.

**Proof.** Apply Theorem 1 separately to every output. The finitely many
generic conditions hold simultaneously, since each projection from
joint source parameters onto a single-output source is surjective.
For generic nonzero edge blocks, two sets of scalings producing the
same covariance have ratios `g_i` with `g_i g_j=1` on every edge.
All `g_i` are equal to a sign, and their product is one; the odd number
of sites excludes the negative sign. Thus all individual recoveries
align uniquely, modulo a common scaling.

The alignment is rational. If block ratios between two representatives
are `c_ij=g_i g_j`, choose a perfect matching `M_i` on the complement
of site `i` and set `g_i=(product_(jk in M_i)c_jk)^-1`. Product one
gives this formula. It then aligns their mean rows. QED.

This corollary recovers the span actually sampled. It does not identify
additional unobserved directions in a larger postulated mean space.

**Corollary 10 (one generic response determines its response space).**
At every odd `n>=5`, for a generic one-direction source and generic
unknown coefficients in

$$
T=\sum_{j=0}^{(n-1)/2}c_j\,
       \frac{L^{n-2j}}{(n-2j)!}\frac{R^j}{j!},
$$

the single tensor determines the full response space and the source's
mean lines and covariance class. The remaining source ambiguity is the
one classified by the span theorem: site scalings, mean rescaling, and
`R -> aR+bL^2`, with `a!=0`.

**Proof.** The mean-direction theorem already covers generic unknown
response coefficients. The rank in Theorem 2 also holds generically in
the enlarged source-and-coefficient parameter space: its Gaussian
witness has `c_j=1`, and the two response null vectors remain universal.
The same holds at five sites by its existing restricted-rank witness.

The covariance-rigidity argument used only annihilation of response
layers and a nonzero top-outside component of the observed tensor;
it did not use Gaussian calibration. It therefore recovers `aR+bL^2`
here as well, against every alternative one-direction response
representation. Generate the response layers of that representative.
Their span is invariant under the listed ambiguities and is exactly
the original response space. The listed source transformations can be
absorbed by changing the unknown coefficients, so they really remain
ambiguities. QED.

This applies to an auxiliary-vertex model with one visible coupling
direction whenever its resulting source and layer coefficients satisfy
these open conditions. It does not assert that every fixed auxiliary
graph reaches that generic set. The distinction between these arbitrary
coefficients and the actual Gaussian coefficients is essential: the
latter permit the calibration that removes the covariance-class freedom.

## 8. Certificates, reproduction, and provenance

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/covariance_induction.py
```

The [program](../computations/matching-tensor-recovery-2026-09-26/covariance_induction.py)
and [certificate](../computations/matching-tensor-recovery-2026-09-26/covariance-induction-certificate.json)
contain the rational pair calculations, local-row examples on six,
eight, and ten sites, the seven-site base, and two deformation checks.
The base rank-377 minor has residue `15` modulo `1009`; all seven
local edge-row matrices have rank `23`. The six antisymmetric classes
have a rank-six minor of residue `123`. The fixed rational pair
minors in Lemma 7 are `1/4` and `9/8` for ranks four and seven.
The latter compute an actual Schur complement of the restricted
exterior matrix through order two:

| Attachment | Initial kernel | First obstruction rank | Second obstruction rank | Kernel at `t=1` |
| --- | ---: | ---: | ---: | ---: |
| 5 to 7 sites | 14 | 4 | 8 | 2 |
| 7 to 9 sites | 14 | 4 | 8 | 2 |

The first minors are `626,127`, and the second minors are `908,500`,
respectively, modulo `1009`. The first line checks the mechanism at
an additional small instance; the analytic induction starts at seven.
The polynomial dependence of the observed tensor is also checked at
a fourth parameter value. None of these finite computations is used
to extrapolate a rank pattern to higher orders; Proposition 8 proves
the general step.

The exterior map and kernel-recovery framework are established tools:
Hauenstein–Oeding–Ottaviani–Sommese,
[*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090),
Sections 5.1–5.2. The matching moment model and formulas are standard;
see Pereira–Kileel–Kolda,
[*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930),
and the calibration references in the preceding note.

Deformation arguments also appear in Gaussian-moment identifiability,
for example Blomenhofer,
[*Gaussian Mixture Identifiability from Degree 6 Moments*](https://arxiv.org/abs/2307.03850).
That paper concerns homogeneous mixture moments and secant geometry,
whereas the observations here are single multilinear cross-site tensors.
The present fixed pair calculation and local edge-row argument must not
be attributed to that different theorem.

For statistical estimation of asymmetric Gaussian moment tensors,
Al-Ghattas–Chen–Sanz-Alonso,
[*On the Estimation of Gaussian Moment Tensors*](https://arxiv.org/abs/2507.06166),
give error bounds for moment estimators at even orders. Those forward
estimation bounds do not provide the inverse-conditioning theorem needed
here. Conditioning, sample complexity, efficient implementation, and
singular source strata remain separate questions. No exhaustive
literature-priority claim is made for the identifiability result.
