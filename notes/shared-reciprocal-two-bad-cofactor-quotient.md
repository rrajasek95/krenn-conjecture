# The two-bad shared packet forces a nonzero cofactor-quotient product

## 1. Exact theorem

Let an exact eight-site ternary matching source have two bad shared
reciprocal arms `pq,pr`.  By
[`the Lemma-E flag normal form`](shared-reciprocal-lemma-e-flag-normal-form.md),
after relabelling colours they are

\[
 A_{pq}=\lambda E_{aa},\qquad A_{pr}=\mu E_{cc},
 \qquad \{a,c,t\}=\{0,1,2\},                             \tag{1}
\]

and the two deleted tensors are

\[
 H_{rC}=\lambda^{-1}X_a,\qquad
 H_{qC}=\mu^{-1}X_c,qquad C=B\setminus\{p,q,r\}.        \tag{2}
\]

Here `C` has five sites.  Put

\[
 K_x=H_{C\setminus\{x\}},\qquad
 \Phi((w_x)_{x\in C})=\sum_{x\in C}w_x^{(x)}K_x.        \tag{3}
\]

The domain is the direct sum of the five endpoint colour spaces and the
codomain is the tensor space on `C`.  It is the literal rowwise
common-cofactor map for adjoining one new controller to the internal source
on `C`.  In this note `X_i` inside `im(Phi)` means the five-site pure tensor
`e_i^(tensor C)`; adjoining the controller row turns it into the corresponding
six-site pure tensor.

> **Theorem 1 (exact quotient obstruction).**  For every hypothetical
> two-bad exact source as above:
>
> 1. `X_a,X_c` belong to `im(Phi)`, but `X_t` does not;
> 2. if `U,V` are the colour-`t` rows of the `q-C,r-C` stars, then
>    `U,V in ker(Phi)` and both are nonzero;
> 3. if `P` is the colour-`t` row of the `p-C` star, then in
>    `coker(Phi)`
>    \[
>       [X_t]=[\mathcal T(P,U,V)]\ne0,                    \tag{4}
>    \]
>    where, at `N=8`,
>    \[
>    \mathcal T(P,U,V)=
>      \sum_{\substack{x,y,z\in C\\\text{pairwise distinct}}}
>       P_x^{(x)}U_y^{(y)}V_z^{(z)}
>       A_{C\setminus\{x,y,z\}}.                         \tag{5}
>    \]

The last factor in (5) is the single physical block on the two sites left
after deleting `x,y,z`.  Thus (4) retains full endpoint order, coefficient
signs, and matching provenance.  It is not an output-only invariant.

This is the sharpest current source-level reduction of the two-bad branch.
It rules out every packet with injective common cofactor map and every
attempt to contract the third colour through an ordinary one-controller
star.  A hypothetical counterexample must instead realize the missing pure
colour as a genuinely nonlinear product of **two cofactor-kernel rows**.

## 2. Why the third pure tensor is outside the image

The colour-`a` row of the first equation in (2), and the colour-`c` row of
the second, are exactly

\[
 \Phi(\lambda A_{rC}(a,\mathord\cdot))=X_a,
 \qquad \Phi(\mu A_{qC}(c,\mathord\cdot))=X_c,           \tag{6}
\]

after identifying the controller colour spaces by their target bases.  So
the first two pure tensors lie in the image.

If `X_t` also lay in the image, choose a third controller star mapping to
it and add the three stars.  The matching tensor on the six sites
`{s} union C` is linear in the entire `s`-star, hence the same internal
blocks on `C` would give

\[
                         H_{sC}=X_a+X_c+X_t=\Delta_{6,3}. \tag{7}

\]

This contradicts Theorem 1.1 of
[`the arbitrary-complex six-site obstruction`](../proofs/six-site-arbitrary-complex-obstruction.md).
Therefore

\[
                       X_t\notin\operatorname{im}\Phi.   \tag{8}
\]

This use of the six-site theorem is exact: the putative new star consists
of arbitrary endpoint-ordered aggregate blocks, exactly the model excluded
there.

## 3. The literal cofactor identity

Let

\[
 d=A_{qr}(t,t),\quad
 U_y=A_{qy}(t,\mathord\cdot),\quad
 V_z=A_{rz}(t,\mathord\cdot),\quad
 P_x=A_{px}(t,\mathord\cdot).                             \tag{9}

\]

Taking the controller-`t` slice of (2) gives

\[
                           \Phi(U)=\Phi(V)=0.             \tag{10}

\]

For `x in C`, expand the actual six-site cofactor at the pair `q,r`:

\[
\begin{aligned}
 L_x&:=H_{qr(C\setminus x)}(t,t,\mathord\cdot)\\
 &=dK_x+
   \sum_{\substack{y,z\in C\setminus x\\y\ne z}}
       U_y^{(y)}V_z^{(z)}H_{C\setminus\{x,y,z\}}.        \tag{11}
\end{aligned}

\]

The first term consists of matchings using the chord `qr`; every other
matching uses one `q`-port and one distinct `r`-port, giving the ordered sum.
The pure-`t` coefficient of the full `p`-expansion says

\[
                         \sum_xP_x^{(x)}L_x=X_t.          \tag{12}

\]

Substituting (11) into (12) gives

\[
                    X_t=d\Phi(P)+\mathcal T(P,U,V).       \tag{13}

\]

Modulo `im(Phi)`, equations (8) and (13) are exactly (4).  In particular
`U` and `V` cannot vanish and `Phi` cannot be injective.  This is the
precise common-hafnian identity missing from the preceding relaxed packet.

Algebraically, (4) is a second-order or Massey-product obstruction: the two
outer colour-`t` rows are vertical first-order directions, and their
bilinear product carries the missing target class.

## 4. A fully provenance-faithful rational counterguard

The quotient product is not universally zero or universally in
`im(Phi)`.  The checker reuses the genuine binary matching power from
[`simultaneous-star-syzygy-boundary.md`](simultaneous-star-syzygy-boundary.md).
On `C={1,2,3,4,5}` its internal cells are

```text
23:00=3/5, 13:00=4/5, 45:00=1, 12:11=1, 34:11=1.
```

Its ternary common-cofactor map has rank `11`, nullity `4`, contains
`X_0,X_1`, and excludes `X_2`.  The signed vector

\[
 U=V={4\over5}e_0^{(1)}-{3\over5}e_0^{(2)}              \tag{14}

\]

is an actual kernel vector.  With `P=e_2` at site `3`, the two ordered
routes through the remaining `45:00` block give

\[
 \mathcal T(P,U,V)=-{24\over25}
 e_0^{(1)}e_0^{(2)}e_2^{(3)}e_0^{(4)}e_0^{(5)},          \tag{15}

\]

and this standard-basis tensor lies outside `im(Phi)`.

The checker goes further than an abstract module.  It adjoins literal `q`
and `r` stars whose complete deleted tensors are respectively `X_1` and
`X_0`, adds (14) as their colour-2 kernel rows, reconstructs every six-site
cofactor `L_x` from the same internal block family, and recovers (15) from
the left side of (12).  Thus all `K_x`, kernel rows, internal blocks, and
six-site cofactors have common matching provenance.

This packet is **not** an eight-site exact source: (15) is mixed rather than
the missing pure `X_2`.  Its role is sharp.  It refutes a universal claim
that the bilinear kernel product in (4) automatically vanishes or belongs
to `im(Phi)`.  The target grade in (4), not cofactor provenance by itself,
is the remaining rigidity.

## 5. The finite theorem-completing target

The two-bad shared-reciprocal branch is now equivalent to the following
five-site algebra question:

> **Pure kernel-product exclusion (open).**  For a ternary quadratic on five
> sites, if two pure tensors lie in the common-cofactor image and the third
> does not, can that third pure class lie in
> \[
>  \operatorname{im}\Phi+
>  \{\mathcal T(P,U,V):U,V\in\ker\Phi\}?                 \tag{16}
> \]

A negative answer closes every two-bad flag orbit uniformly at `N=8`.  A
positive rational example is the smallest honest algebraic seed for an
eight-site counterexample search.  The rational guard (15) shows that an
ungraded containment theorem is false, but it does not answer the pure
class question.

## 6. Exact one-cell span theorem on the two sparse binary charts

The stronger linear-span claim survives the first coefficient-complete
charts.  Put

\[
 \mathcal S(q)=\operatorname{im}\Phi_q+
 \operatorname{span}\{\mathcal T(P,U,V):
              P\in A_1,\ U,V\in\ker\Phi_q\}.             \tag{17}
\]

For the rational Pythagorean common power in Section 4, adjoining all
`15*4^2=240` kernel-product columns raises the ambient image rank from `11`
to `16`, but

\[
 \mathcal S(q)\cap\operatorname{span}\{X_0,X_1,X_2\}
 =\operatorname{span}\{X_0,X_1\}.                         \tag{18}

\]

The checker also starts from two exact binary six-site charts:

1. the six-cell alternating Hamilton cycle; and
2. the eight-cell Pythagorean cancellation source of Section 4.

For each chart it adjoins every possible new endpoint-coloured internal
cell, recomputes the literal five-site hafnian cofactors, retains only the
charts in which `X_0,X_1` still lie in `im(Phi)`, and constructs the **full**
space (17), not a sample of kernel vectors.  The exact census is

| base chart | candidate cells | retain both old pure images | acquire `X_2` in (17) |
|---|---:|---:|---:|
| Hamilton | 86 | 36 | 0 |
| Pythagorean | 85 | 43 | 0 |

The unit weights lose no nonzero coefficient strata.  The checker forms the
diagonal-torus character vector of every base cell and candidate cell; in
both base charts every candidate character is independent of the base
characters.  Hence the stabilizer of the base weights scales the candidate
weight arbitrarily.  Over the algebraically closed field, every nonzero
one-cell coefficient is torus-equivalent to the checked unit.  Zero is the
already-checked base chart.

Thus (18) is an exact theorem on both complete one-cell extensions, not a
coefficient grid.  It is still not the arbitrary-`q` pure kernel-product
exclusion of Section 5.  A counterexample, if one exists, needs at least two
independent deformations away from each of these sparse binary charts (or a
different binary component altogether).

## 7. Reproduction

```sh
.venv/bin/python computations/verify_shared_reciprocal_two_bad_quotient.py
.venv/bin/python -O computations/verify_shared_reciprocal_two_bad_quotient.py
```

The checker performs exact rational rank and image tests, reconstructs the
kernel product from literal matchings, and rebuilds both pure deleted stars
and all queried six-site cofactors from one endpoint-ordered block family.
