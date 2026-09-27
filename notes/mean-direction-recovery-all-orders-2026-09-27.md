# Recovering mean directions from one cross moment at every odd order

Research note, 2026-09-27. Written proof with an exact five-site base
certificate, symbolic checks of the attachment lemma, and finite-field
checks of the deformation formula. Not Lean formalized or independently
peer reviewed. The Krenn–Gu manuscript is unchanged.

## 1. Result and its limits

**Theorem 1 (all-orders mean-direction recovery).** Let `n>=5` be odd,
and let every local vector space have dimension at least three. For a
generic complex monomer–dimer source, its single full cross-moment tensor
determines every local mean line, among all source representations of
that tensor. In particular, an alternative representation cannot have a
zero local mean. The recovered lines are rational functions on suitable
charts of the model's image.

For three-dimensional local spaces, a stronger observable statement
holds: the exterior kernel contains exactly one product-tensor line,
and its intersection with the product-tensor variety is reduced at that
point. This statement is proved by induction, without a formula for the
dimension of the entire exterior kernel.

This extends the earlier five- and seven-site direction result to every
odd order at least five. It supplies the mean-direction part of
single-output source recovery. It does **not** by itself recover the
covariance from one output. The subsequent
[covariance-rank induction](single-cross-moment-all-orders-2026-09-27.md)
now completes that recovery at every odd order at least seven. The existing
[one-direction span theorem](one-direction-source-reconstruction-2026-09-27.md)
recovers the covariance class once that space is supplied or recovered.

The proof supplies a rational inverse in principle, through polynomial
elimination. It does not give an all-orders algorithm using only the two
linear systems in the earlier finite-dimensional recovery programs, nor
a complexity or statistical-stability bound.

The subsequent [blind-search implementation](blind-source-search-and-local-conditioning-2026-09-27.md)
now finds and exactly verifies mean lines on seven-, nine-, and
eleven-site examples, and recovers complete rational sources in the
first two cases. It also gives local conditioning bounds and retains
a failed search. It does not supply global convergence guarantees.

## 2. The observable zero set

First take `V_i=C^3`. A local mean is a vector `l_i` and a cross-site
block is `R_ij in V_i tensor V_j`. The observed tensor is

$$
T=G(L,R)=[\exp(L+R)]_{\mathrm{full}},\qquad
L=\sum_i l_i,\quad R=\sum_{i<j}R_{ij}.
$$

Products use the commutative site algebra
`tensor_i(C direct_sum V_i)`, with two factors at the same site equal
to zero. Equivalently, `G` sums matchings, placing `l_i` at each
unmatched site and `R_ij` at each matched pair. For a real Gaussian
source it is `E[X_1 tensor ... tensor X_n]`.

For nonzero vectors `u_i`, let `q_(u_i):V_i -> V_i/Cu_i` be the quotient
map. Define a closed set in a product of projective planes by

$$
Z(T)=\left\{([u_1],\ldots,[u_n]):
       (\bigotimes_i q_{u_i})T=0\right\}. \tag{1}
$$

The equations also define a scheme. For an isolated point, absence of
a nonzero projective tangent direction certifies that its scheme
structure is **reduced**, with no infinitesimal multiplicity.
The local spaces have dimension two after
taking quotients, so (1) is a system of `2^n` equations in `2n` local
coordinates.

The map `v -> u_i wedge v` factors through an isomorphism from
`V_i/Cu_i` to `u_i wedge V_i`. Consequently (1) is equivalent to

$$
\mathcal B_2(T,u_1\otimes\cdots\otimes u_n)=0.
$$

After choosing volume forms, this says that the product tensor belongs
to `ker A(T)`, for the already used tensor-product Koszul flattening

$$
A(T)_{a,b}=\sum_c T_c\prod_i\epsilon_{a_i b_i c_i}.
$$

Since `n` is odd, every matching contributing to `T` has a monomer.
Projecting away all the actual mean lines kills every term. Thus the
actual mean tuple always belongs to `Z(T)` when all means are nonzero.

We shall construct, at every odd order, a source for which `Z(T)` is
exactly this one reduced point.

## 3. The tangent matrix and the five-site base

Choose coordinates so that every actual mean is `x_i=(1,0,0)`, and put
`U_i=span(y_i,z_i)`. Write a nearby candidate line as `C(x_i+h_i)`,
where `h_i in U_i`. A convenient quotient is

$$
q_{x_i+h_i}(x_i)=-h_i,\qquad q_{x_i+h_i}|_{U_i}=\mathrm{id}.
$$

Let `H_i` be the centered matching tensor on all sites other than `i`,
using the blocks of `R` projected to their outside-mean spaces. For
`a=1,2`, define `F_(i,a)` by placing `y_i` or `z_i` at site `i` and
`H_i` at the remaining sites. These are tensors in `tensor_i U_i`.

**Lemma 2 (direction tangent matrix).** At the actual means,

$$
\left(\bigotimes_iq_{x_i+h_i}\right)T
   =-\sum_{i,a}h_{i,a}F_{i,a}+O(\|h\|^2). \tag{2}
$$

In particular, the actual point of `Z(T)` is reduced if and only if
the `2n` vectors `F_(i,a)` are linearly independent.

**Proof.** A first derivative of the quotient can survive only when
the differentiated site uses its mean coordinate and every other site
uses an outside coordinate. The only surviving matching terms have
that site as their single monomer and pair all other sites. This gives
exactly (2), with the indicated minus sign. QED.

**Lemma 3 (certified base at five sites).** A five-site source exists
for which `Z(T)` is one reduced point.

**Proof.** Use the source of seed `90127` in the existing
[single-output certificate](../computations/matching-tensor-recovery-2026-09-26/single-source-certificate.json).
Its exterior kernel has dimension three. The restrictions of the
product-tensor flattening minors span a five-dimensional subspace of
the six-dimensional space of quadratics in kernel coordinates.

Those quadratics vanish at the actual product point. Hence they span
*all* quadratics vanishing at that point. In coordinates making it
`[1:0:0]`, their span contains `z_0 z_1,z_0 z_2,z_1^2,z_1 z_2,z_2^2`.
Their projective zero scheme is the one reduced point `[1:0:0]`.
The full product-tensor equations have the same zero scheme there.

The nonzero modular minors in the certificate give characteristic-zero
rank witnesses after clearing pivot denominators. The new replay below
also normalizes the means to `x_i` and directly checks that the matrix
in Lemma 2 has rank ten. QED.

## 4. A two-site linear algebra lemma

For this section let `V=W=C^3`, with distinguished vectors `x,x'`.
Choose bases `x,y,z` and `x',y',z'`. Set

$$
S=x\otimes x'+y\otimes y'+z\otimes z',\qquad
\mathcal H=V\otimes x'+x\otimes W. \tag{3}
$$

Here `S` is an invertible three-by-three matrix and `H` is a
five-dimensional subspace of matrices. The latter is the affine
tangent space to the product-tensor cone at `x tensor x'`.

**Lemma 4 (forcing the two new lines).** For any nonzero `u in V` and
`v in W`, the image `Sbar=(q_u tensor q_v)S` is nonzero. If

$$
(q_u\otimes q_v)\mathcal H\subseteq\mathbb C\overline S, \tag{4}
$$

then `Cu=Cx` and `Cv=Cx'`.

**Proof.** If `Sbar=0`, the invertible map represented by `S` would
send a two-dimensional annihilator space into a one-dimensional line.
This is impossible.

Write `xbar=q_u(x)` and `xbar'=q_v(x')`. The image of `H` is

$$
(V/Cu)\otimes\overline{x'}+overline x\otimes(W/Cv).
$$

Its dimension is three when both distinguished images are nonzero,
two when exactly one is nonzero, and zero when both vanish. A subspace
of the line `C Sbar` has dimension at most one. Thus both distinguished
images vanish, which gives the claimed lines. QED.

**Lemma 5 (the two new lines are simple).** Near `([x],[x'])`, the
equations (4), using any basis of `H`, have zero tangent kernel in
the four projective line coordinates.

**Proof.** At the distinguished point the projected matrix `Sbar` is
the invertible two-by-two matrix `B=y tensor y'+z tensor z'`. Let
`u=x+h` and `v=x'+k`. For a matrix `a tensor x'`, with `a in span(y,z)`,
the first projected variation is `-a tensor k`. Condition (4) to first
order requires this matrix to belong to `C B`. Its rank is at most
one, whereas a nonzero multiple of `B` has rank two. Varying `a`
forces `k=0`. The matrices `x tensor b` force `h=0` in the same way.
QED.

The replay checks this lemma independently by symbolic elimination
over the rationals in **all nine projective chart pairs**. The chart
containing `([x],[x'])` has reduced ideal `(h_1,h_2,k_1,k_2)`; the
other eight charts have unit ideal. A selected four-by-four tangent
minor is a unit.

## 5. Attaching two sites

**Proposition 6 (induction step).** Suppose an odd-site source has
`Z(T)` equal to its one reduced mean tuple. Then an `(n+2)`-site
source with the same property exists.

**Construction.** Normalize the old means to `x_i`. Give the two new
sites, called `p,q`, means `x_p,x_q` and edge

$$
R_{pq}=y_p\otimes y_q+z_p\otimes z_q.
$$

Their two-site output is the matrix `S` of (3). With no cross edges
between old and new sites, the full output is `T_0=T tensor S`.

Now add edges from old sites to `p,q`, with a common scalar parameter
`t`. Their outside-mean rows are vectors `v_(i,a) in V_p` and
`w_(i,a) in V_q`, respectively. Choose them so that the matrices

$$
M_{i,a}=v_{i,a}\otimes x_q+x_p\otimes w_{i,a} \tag{5}
$$

span all of `H`. This needs only five of the `2n` available rows.
For example, use the following five matrices in the slots
`(i,a)=(1,1),(1,2),(2,1),(2,2),(3,1)`:

$$
x_p x_q,\quad y_p x_q,\quad z_p x_q,\quad x_p y_q,\quad x_p z_q. \tag{6}
$$

All other cross rows can be zero, as can the cross rows at the old mean
coordinates. Let `T_t` be the resulting Gaussian matching tensor. Its
actual means remain fixed for every `t`.

**First-order formula.** Write `h` for the old candidate-line changes
and keep arbitrary candidate lines `[u],[v]` at the new sites. In local
quotient coordinates put `Sbar=(q_u tensor q_v)S` and similarly `Mbar`.
By Lemma 2 and a matching expansion,

$$
\left(\bigotimes_{\text{old }i}q_{x_i+h_i}\otimes q_u\otimes q_v\right)T_t
=\sum_{i,a}F_{i,a}\otimes
       \bigl(t\overline M_{i,a}-h_{i,a}\overline S\bigr)
 +O(\|h\|^2+|t|\|h\|+|t|^2). \tag{7}
$$

Indeed, one cross edge leaves the other new site as a monomer. After
projecting every old site, the remaining old sites must be perfectly
matched, giving `F_(i,a)` and (5). At `h=0` this projected identity is
actually linear in `t`: with zero cross edges an old monomer survives,
and with two cross edges an odd number of old sites remains. Both
contributions vanish under the old quotients.

### 5.1 Excluding other limiting line tuples

At `t=0`, Lemma 4 shows that the projection of `S` never vanishes.
Thus the zero set of `T_0=T tensor S` has the old lines fixed at their
known values, while the two new lines are arbitrary.

Consider any sequence `t -> 0`, `t!=0`, of solutions of (1) for `T_t`.
The product of projective planes is compact. Passing to a subsequence
gives a limiting tuple; its old lines must be the original ones. Choose
quotient charts near its new lines. There `Sbar` stays nonzero.

The vectors `F_(i,a)` are independent by the reduced-point hypothesis.
It follows from (7), by applying dual linear functionals and absorbing
the terms quadratic in `h`, that `h=O(t)`. Divide (7) by `t`, and pass
to a further subsequence along which `h/t` converges. Independence of
the `F_(i,a)` gives

$$
\overline M_{i,a}\in\mathbb C\overline S\quad\text{for every }(i,a).
$$

Their span is `H`, so Lemma 4 forces both limiting new lines to be
the actual means. Therefore **every** possible limiting solution is
the full actual mean tuple. This excludes solutions elsewhere in
projective space, including those outside the mean-coordinate charts.

### 5.2 Excluding several branches through that tuple

The preceding limit argument alone would not prove uniqueness: several
solutions could converge to the same point. We now use Lemma 5 to
exclude that possibility.

Near the actual tuple, choose dual functionals for the `F_(i,a)` and
one nonzero entry of `Sbar` (at the actual means, choose the `y_p y_q`
entry of the identity matrix `B`). Extract `2n` scalar equations from
(7). Their Jacobian in the old coordinates `h` is invertible at `t=0`.
The analytic implicit-function theorem solves them uniquely as

$$
h=h(t,u,v),\qquad h(0,u,v)=0.
$$

Substitute this expression in the remaining equations. They vanish
identically at `t=0`, so divide them by `t`. Their equations at `t=0`
are precisely the matrices `Mbar_(i,a)` modulo the line `C Sbar`.
More explicitly, the selected entry first determines each coefficient
`h_(i,a)/t`; the remaining entries assert that the corresponding `Mbar`
is that scalar multiple of `Sbar`.

Lemma 5 says that this residual system has rank four in the four new
line coordinates. Choose four independent scalar equations and apply
the implicit-function theorem again. They have a unique nearby solution
for small `t`. The actual, unchanged means are always a solution, so
they are that unique solution.

The same calculation proves simplicity for sufficiently small nonzero
`t`: a selected full Jacobian determinant has leading term `c t^4`,
with `c!=0`. Section 5.1 ensures that all possible solutions lie in
this neighborhood once `t` is sufficiently small. Hence `Z(T_t)` is
exactly the actual mean tuple, reduced, for all sufficiently small
nonzero `t`. This proves Proposition 6. QED.

## 6. Genericity and alternatives

**Lemma 7 (one reduced fiber persists generically).** In this source
family, existence of one source with a unique reduced point of `Z(T)`
implies that property on a nonempty Zariski-open set of sources.

**Proof.** Restrict source space to nonzero means, and form the incidence
scheme of source parameters and tuples in `Z(T)`. Its projection to
source space is proper, since the line tuples range over a product of
projective spaces. It has a section given by the actual mean tuple.

A proper morphism is finite on a neighborhood of a finite fiber.
On that neighborhood, let `A` be the finite algebra of the incidence
scheme over the base. At a one-point reduced fiber, the unit map
`O -> A` is surjective after tensoring with the residue field. Nakayama's
lemma makes it surjective on a smaller neighborhood. The section makes
the unit map injective. Thus `A=O` there: the incidence scheme is just
the actual-mean section. QED.

For the finiteness step see the Stacks Project,
[Lemma 30.21.2, Tag 02OH](https://stacks.math.columbia.edu/tag/02OH).
This use of properness is also why the global limit argument in
Section 5.1 cannot be replaced by a tangent-rank calculation alone.

**Proof of Theorem 1 in local dimension three.** Lemma 3 starts the
induction at five sites, and Proposition 6 advances by two sites.
Lemma 7 gives the generic statement at each odd order.

Any alternative source with all means nonzero supplies a product point
in the same observable zero set. Hence it has exactly the recovered
mean lines. If an alternative has zero means at some sites, replace
those means by `t u_i`. The quotient identity for nonzero `t`, or the
equivalent exterior identity after dividing out the terminal power of
`t`, shows at `t=0` that the product of these arbitrary `u_i` and the
remaining nonzero means belongs to the same exterior kernel. Varying
one `u_i` gives multiple product lines, a contradiction.

Finally, on the image of the source model, the observable incidence
projection has generic fiber one reduced point. In characteristic zero
its dominant component is birational to that image. The inverse mean
lines are therefore rational on suitable nonzero-denominator charts.
They can also be specified constructively as the unique projective
solution of the exterior equations together with the product-tensor
minor equations. No efficient uniform elimination bound is asserted.
QED.

**Corollary 8 (arbitrary local dimensions at least three).** The same
mean-direction conclusion holds for unequal local dimensions at least
three.

**Proof.** Apply the three-dimensional theorem to a baseline coordinate
projection `{0,1,2}` at every site. For each additional coordinate at
site `i`, replace coordinate `2` by that coordinate, keeping the other
sites at baseline. Every projected source map is surjective, so finitely
many required nonempty open conditions hold simultaneously on a
nonempty open set. Also require the actual mean's coordinate `0` to be
nonzero at every site.

The unique mean lines in these views determine all coordinate ratios
to coordinate `0`. Every alternative full source must project to the
same lines; a zero projected mean is excluded by the preceding argument.
Thus all full mean lines are determined, and the recovery is rational
by combining the projected rational ratios. QED.

**Corollary 9 (generic response combinations).** The mean-direction
conclusion also holds for a generic source and generic coefficients in

$$
T=\sum_{k\ \mathrm{odd}}c_kP_k(L,R).
$$

The coefficients need not be known. Every alternative one-direction
response representation of this tensor has the same nonzero local mean
lines.

**Proof.** The actual mean tuple still gives a section of (1), since
every term has a monomer. The larger source-and-coefficient parameter
space includes the witnesses just constructed, at `c_k=1`. Lemma 7
therefore gives a nonempty open set in this larger irreducible space.
The alternative-representation argument is unchanged. QED.

This is an identifiability statement for a generic joint choice of source
and coefficients. It does not assert the conclusion for every fixed
coefficient pattern, or for every hidden-graph parametrization of those
coefficients.

## 7. Exact checks and remaining work

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/mean_direction_induction.py
```

The [program](../computations/matching-tensor-recovery-2026-09-26/mean_direction_induction.py)
and [certificate](../computations/matching-tensor-recovery-2026-09-26/mean-direction-induction-certificate.json)
record:

* Exact rational Groebner bases in all nine projective chart pairs for
  Lemma 4, and a unit tangent minor for Lemma 5.
* A normalized version of the existing five-site source, including all
  edge blocks and an explicit unique-product certificate.
* The matching-expansion identity (7), checked after projection of the
  old sites for the attachments `5 -> 7` and `7 -> 9`.
* Direction Jacobian ranks `10,14,18` at the resulting five-, seven-,
  and nine-site sources, with selected determinant residues `991,703,786`
  modulo `1009`.
* At five and seven sites, full exterior-kernel and quadratic-restriction
  checks. Their kernel dimensions are `3,5`; their selected quadratic
  minor residues are `753,637`.

The nine-site check certifies only local simplicity at that particular
integer specialization. It does **not** compute the full exterior kernel
or prove global uniqueness at that particular specialization. The
all-orders global theorem follows from Proposition 6 and Lemma 7.

The covariance step has now been completed separately. Given the recovered
mean lines, the subsequent
[low-degree criterion](single-output-covariance-low-degree-2026-09-27.md)
and its [all-orders induction](single-cross-moment-all-orders-2026-09-27.md)
recover the covariance at every odd order at least seven. A stronger
sufficient condition, not needed for that conclusion, would be

$$
\ker A(T)\cap\ker\!\left(\bigotimes_i q_{l_i}\right)=W(L,R).
$$

The induction here deliberately makes no claim about this larger linear
kernel. Its exact completion is still unproved at nine and higher sites,
even though the covariance can now be recovered at every odd order at
least seven without it.
Small structured tests show that recovering its product point and
saturating its response dimension are distinct problems.

## 8. Attribution

The observable exterior matrix is the established tensor-product Koszul
flattening of Hauenstein–Oeding–Ottaviani–Sommese,
[*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090),
Section 5.1; their Section 5.2 develops kernel-based reconstruction.
The projective incidence, deformation, and implicit-function arguments
are standard techniques, not new mathematical machinery.

Gaussian matching expansions and moment tensors are standard; see
Pereira–Kileel–Kolda,
[*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930).
The five-site computational base and the copy identity are cited above.
The additional model-specific argument is that attaching a full-rank
two-site moment and five cross rows forces the two new mean lines while
preserving uniqueness and reducedness. No literature-priority claim is
made for that argument or for the resulting identifiability statement.
