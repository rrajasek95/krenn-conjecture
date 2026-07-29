# Stable pairification of a six-boundary signature, and why it loses the target

## 1. Outcome

There is an exact way to remove every four- and six-boundary cumulant from
an arbitrary six-boundary matching gadget.  Take three parallel copies,
scale the boundary incidences of the copies by three algebraic numbers, and
identify their six boundary vertices.  The resulting gadget is equivalent,
at **every** boundary order, to a scalar times an ordinary pair-edge
signature.

This does not give an all-even descent.  The operation necessarily deletes
the original six-boundary component: its new top tensor depends only on the
old two-boundary component.  An exact rational binary `Delta_(8,2)` source
has two product pair caps with the same scalar and the same capped target
`Delta_(6,2)`, but their stably pairified tensors are respectively

\[
             \Delta_{6,2},\qquad
             \Delta_{6,2}-2e_{001000}.                    \tag{1}
\]

Thus even for a genuine exact source, the scalar and the complete capped
top tensor do not determine the pairification.  Any use of parallel-copy
cumulant cancellation must bring in lower boundary data or relations among
several caps; the GHZ equation by itself lives only in the top component.

The exact audit is
`computations/verify_stable_six_boundary_pairification.py`.

## 2. Full boundary signatures and parallel composition

Let `U` be a set of six boundary vertices.  A scalarized matching gadget
with internal vertex set `W` has the even boundary signature

\[
                 F=F_0+F_2+F_4+F_6\in\mathscr S_U,        \tag{2}
\]

where `F_S` is the sum of the matchings of `W union S` which cover every
internal vertex and precisely the named boundary vertices in `S`.  Edges
inside `S` are allowed.  Here

\[
 \mathscr S_U=\bigoplus_{S\subseteq U}\bigotimes_{u\in S}V_u
\]

has the square-free product: tensors on disjoint supports tensor together,
and products with overlapping supports are zero.  Write

\[
                         s=F_\varnothing .                \tag{3}
\]

The scalarization arises, for example, by capping every internal site with
a product covector.  Endpoint order and arbitrary boundary vectors are
retained; only the internal slots have become scalars.

Take gadgets with disjoint internal sets and identify equally named
boundary vertices.  There are no edges between the internal sets.  A
matching of the union assigns disjoint boundary subsets to the gadgets and
chooses one matching inside each gadget.  Consequently its boundary
signature is exactly the square-free product

\[
                         F^{(1)}F^{(2)}\cdots F^{(m)}.     \tag{4}
\]

This remains true when different copies contribute parallel tensors on the
same boundary pair: expansion of the aggregate tensor simply records which
copy supplied that occurrence.

For `z in C`, choose `t` with `t^2=z`.  In one copy multiply every
boundary--internal edge by `t` and every boundary--boundary edge by `t^2`;
leave internal--internal edges unchanged.  Every matching contributing to
`F_S` then acquires the factor `t^{|S|}`.  Thus this physical dilation is
the algebra automorphism

\[
       \delta_z(F_{2k})=z^kF_{2k}\qquad(0\le k\le3).      \tag{5}
\]

## 3. Three-copy pairification

Assume `s ne 0` and use the finite nilpotent logarithm

\[
       \log(F/s)=K_2+K_4+K_6.                             \tag{6}
\]

Let `z_1,z_2,z_3` be the three roots, counted with multiplicity, of

\[
                  z^3-z^2+\frac12z-\frac16.              \tag{7}
\]

Vieta's formulas and Newton's identities give

\[
 \sum_jz_j=1,\qquad \sum_jz_j^2=0,\qquad
 \sum_jz_j^3=0.                                         \tag{8}
\]

Choose square roots `t_j^2=z_j`, make the three dilated physical copies,
and identify their boundary vertices.

**Theorem 3.1 (stable six-boundary pairification).**  The boundary
signature `F^sharp` of the three-copy gadget is

\[
 \boxed{
       F^\sharp=\prod_{j=1}^3\delta_{z_j}(F)
               =s^3\exp(F_2/s).}                         \tag{9}
\]

In particular it is fully equivalent to a pair-only boundary gadget with
pair family `F_2/s` and overall scalar `s^3`.  Its six-boundary tensor is

\[
                  F^\sharp_U={F_2^3\over3!}=H_U(F_2).    \tag{10}
\]

**Proof.**  Dilation is an algebra automorphism, so it commutes with the
finite logarithm.  Equations (4)--(6) give

\[
 \begin{aligned}
 \log(F^\sharp/s^3)
   &=\sum_{j=1}^3\delta_{z_j}\log(F/s)\\
   &=\left(\sum_jz_j\right)K_2
     +\left(\sum_jz_j^2\right)K_4
     +\left(\sum_jz_j^3\right)K_6=K_2.
 \end{aligned}                                           \tag{11}
\]

The degree-two part of a logarithm is `K_2=F_2/s`, proving (9).
Taking support `U` gives (10); the factor `3!` is exactly the number of
orders of each perfect matching in the square-free cube.  `QED`

The roots in (7) need not be written in radicals.  They are nonzero because
their product is `1/6`, and every complex number has a square root, so the
three physical dilations exist over `C`.

## 4. Pairification necessarily erases the old top tensor

The loss in (10) is not special to the three roots above.  Take any number
`m` of parallel dilated copies and put

\[
                         p_k=\sum_{j=1}^m z_j^k.          \tag{12}
\]

Their normalized logarithm is

\[
                         p_1K_2+p_2K_4+p_3K_6.           \tag{13}
\]

Hence a dilation-convolution which removes both higher cumulants must have
`p_2=p_3=0`.  Under those equations its full signature and top component
are

\[
 \prod_j\delta_{z_j}(F)
       =s^m\exp(p_1F_2/s),\qquad
 [\prod_j\delta_{z_j}(F)]_U
       ={s^{m-3}p_1^3\over6}F_2^3.                       \tag{14}
\]

In the direct expansion, the coefficient of the old `F_6` is
`s^(m-1)p_3`, and the coefficient of `F_4F_2` is
`s^(m-2)(p_1p_2-p_3)`; both vanish.  Newton's identity

\[
       6e_3=p_1^3-3p_1p_2+2p_3=p_1^3                  \tag{15}
\]

leaves only the product of three `F_2` components.  Therefore every
parallel-copy dilation which genuinely pairifies the signature discards
the single-copy top component.  Knowing

\[
                         F_U=\Delta_{6,q}                 \tag{16}
\]

places no formal constraint on the tensor in (14).

## 5. Exact equal-top separation inside a genuine source

The preceding warning occurs inside one exact global matching source, not
only for abstract signatures.  On vertices `1,...,8` use colors `0,1` and
the following nonzero aggregate tensors:

\[
\begin{array}{c|c}
12&(e_0+e_1)e_0\\
34,24&e_0e_0\\
13&-e_1e_0\\
16,23&e_1e_1\\
45&\frac34e_1e_1\\
15,46&\frac12e_1e_1\\
57,68&e_0e_0\\
78&e_1e_1.
\end{array}                                               \tag{17}
\]

The four underlying matching states inherited from the six-site source,
with the two states of the path `5-7-8-6`, give exactly

\[
                         H_8(A)=\Delta_{8,2}.             \tag{18}
\]

Cap a deleted pair `p,q` by the product covector

\[
                  \epsilon_p\otimes\epsilon_q,
       \qquad \epsilon=e_0^*+e_1^*.                      \tag{19}
\]

For both pairs `23` and `16`, the scalar component is one, and (18) gives
the same top boundary tensor `Delta_(6,2)`.

For `pq=23`, in the boundary order `(1,4,5,6,7,8)`, the nonzero entries of
`F_2` are

\[
\begin{array}{c|c@{\qquad}c|c}
14&e_0e_0&45&\frac34e_1e_1\\
15&\frac12e_1e_1&16&e_1e_1\\
46&\frac12e_1e_1&57&e_0e_0\\
68&e_0e_0&78&e_1e_1.
\end{array}                                               \tag{20}
\]

Its fifteen six-site matching terms sum to

\[
                         H_6(F_2)=\Delta_{6,2}.           \tag{21}
\]

For `pq=16`, in the boundary order `(2,3,4,5,7,8)`, they are

\[
\begin{array}{c|c@{\qquad}c|c}
23&e_1e_1&24&e_0(e_0+e_1)\\
28&2e_0e_0&34&e_0(e_0-\frac12e_1)\\
38&-e_0e_0&45&e_1e_1\\
57&e_0e_0&58&\frac12e_1e_0\\
78&e_1e_1.&&
\end{array}                                               \tag{22}
\]

Exact enumeration gives

\[
 H_6(F_2)=e_0^{\otimes6}+e_1^{\otimes6}
 -2e_0^{(2)}e_0^{(3)}e_1^{(4)}e_0^{(5)}e_0^{(7)}e_0^{(8)}. \tag{23}
\]

Equations (21) and (23), together with Theorem 3.1, prove (1).  Thus two
product caps of the same exact source have identical `(F_0,F_6)` but
different pairified top tensors.

## 6. Scope

Theorem 3.1 is a genuine physical closure theorem for product-capped
matching gadgets: it removes higher cumulants without pretending they were
zero.  Section 4 also gives a complete no-go for using that operation as a
black-box order descent from the top GHZ equation.  The binary example does
not refute a specifically ternary theorem which couples the lower boundary
components of many different caps.  Rather, it identifies exactly what
such a theorem must control: the two-boundary components `F_2`, since every
dilation-convolution pairification forgets the known top component.
