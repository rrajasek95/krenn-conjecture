# The actual trapped-carrier endpoint map leaves one protection covector

## Result

The exhaustive endpoint map can be written without the open Gate-I `Phi`,
but only after fixing what “exhaustive” means.  Fix a unary-compatible
common residual `q` and the two right endpoint rows `s_1,s_2`.  Let `R_P`
be the derivative in all 36 literal coordinates of `p_1,p_2` of the four
physical response equations

\[
                 p_i s_j q^{[2]}=\delta_{ij}X_i.       \tag{1}
\]

This is the complete fixed-`q`, fixed-right endpoint map.  Its rows retain
the response head `ij`, complete six-letter output word, endpoint
site/colour and orientation, and the common-`q` grade.  It has `4*3^6=2916`
conceptual response rows and 36 columns.

The unary block contributes no endpoint rank:

\[
              D_{(p_1,p_2)}(q^{[3]}-X_0)=0.           \tag{2}
\]

Thus the unary equation first selects the allowed `q` fibre.  If its
residual is nonzero, one has the already pinned ordinary unit exit.  At an
actual source it is zero, and all 729 zero unary derivative rows may be
deleted from the endpoint Jacobian.

The actual response entry is explicit.  For a column `(i,u,a)` and row
`(k,j,w)`, where `w` is a word on the six residual sites,

\[
 (R_P)_{(k,j,w),(i,u,a)}=
 \delta_{ki}\delta_{a,w_u}
 \sum_{v\ne u}s_j[v,w_v]
 \operatorname {Haf}_{q}
       (R\setminus\{u,v\};w|_{R\setminus\{u,v\}}).   \tag{3}
\]

The four-site Hafnian is the sum over its three perfect matchings, so every
generic nonzero entry of (3) has exactly `5*3=15` decorated monomials.  The
checker independently enumerates every physical matching occurrence and
verifies (3) coefficient by coefficient: there are 17,496 generic nonzero
entries and 262,440 monomial terms.  The right map is the same formula with
`p` and `s` interchanged and must be rebuilt after a left move.

Checker:
[`verify_h3_trapped_carrier_actual_endpoint_map_boundary.py`](../computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py).

## What the anchor border actually is

A selected marked anchor occurrence, for example

```text
p1[0,1] s1[1,1] q23[0,0] q45[0,0],
```

is one of the fifteen monomials in aggregate response row `11:110000`.
On a fixed `q,s` fibre with its displayed tail nonzero, preserving that
marked occurrence is equivalent, after dividing by the fixed tail, to
preserving the literal coordinate `p1[0,1]`.  Hence selected-anchor safety
is imposed by bordering (3) with the appropriate coordinate selectors

\[
                         H_Ap=a.                       \tag{4}
\]

This is a valid and exact protection constraint.  It is not automatically
a physical source equation.  The aggregate physical response coefficient
is the sum of all fifteen occurrences in (3), whereas a marked-occurrence
selector retains just one summand.  A proof that uses a dual multiplier on
`H_A` must therefore either cite a source row realizing that selector or
call the result a constrained-fibre covector, not a physical source/Fitting
dual.

This distinction corrects the fourth branch stated too strongly in
`54cd9c9/8f64a9b`.

## Refined support-minimal alternative

Write

\[
                     C=\begin{bmatrix}R_P\\H_A\end{bmatrix},
                 \qquad Cx=\binom{t}{a},              \tag{5}
\]

and choose a solution of minimum support `B`.  Then `C_B` is injective.
For every additional effective endpoint column, exact linear algebra gives
the following usable alternatives.

1. If `|B|=1`, the constrained fibre has literal coordinate access.
2. If an outside column raises the rank of the **physical** response map
   relative to `R_{P,B}`, it is a physical response/Fitting rank exit.
3. If an outside column belongs to `span(C_B)`, its fundamental circuit
   lies in both `ker R_P` and `ker H_A`; this is an anchor-safe complete-
   column dependence.
4. An outside column can be dependent in the physical response map but
   independent only after adjoining `H_A`.  This is a protection-only rank
   exit, not a physical transverse-rank theorem.
5. If there is no outside effective column, an occupied coordinate `j` is
   a genuine physical fixed-`q` dual precisely when

   \[
             e_j^*\in\operatorname {row}(R_P),
       \quad\text{equivalently}\quad
             \operatorname {rank}R_P
          =\operatorname {rank}\begin{bmatrix}R_P\\e_j^*\end{bmatrix}.
                                                               \tag{6}
   \]

   Membership only in `row(C)` gives a genuine covector of the protected
   endpoint fibre, but not a physical response dual.

The checker contains sharp rational packets realizing every one of these
branches.  In particular

\[
 R=(1\;1),\qquad H_A=(1\;0),\qquad (t,a)=(2,1)         \tag{7}
\]

has the unique full-support point `(1,1)`.  The selector `(1,0)` lies in
`row([R;H_A])` but not in `row(R)`.  Thus no abstract complete-map argument
can remove the protection-only survivor.

## Consequence for the trapped carrier

The actual fixed-common-`q` endpoint map is no longer missing: (2)--(4)
give all unary, four-response, label, and selected-anchor entries.  After
evaluation at a unary-compatible trapped source, the support-minimal
argument unconditionally yields constrained coordinate access, physical
response rank, an anchor-safe complete-column circuit, or the exact
protection obstruction above.

What remains is smaller and sharply typed:

> **Anchor/source-row or relative-`q` extension.**  If the evaluated packet
> lands in the protection-only branch, either realize its selected-anchor
> selector by an actual protected source row, or append all simultaneous
> `q`-deformation columns (including the unary derivative) and rerun the
> complete rank alternative.

A covector which kills all endpoint columns at fixed `q` need not kill
those `q` columns.  Therefore this result closes the local endpoint
accessibility calculation but not the global full-source duality claim.

The standard `X1+Y,-Y` affine guard does not realize the survivor: its
frozen `q` violates the unary equation by the constant generator
`q^[3][000000]-1=-1`, as pinned in `5ba50c8`.

## Scope and verification

This is a universal coefficient-level construction of the full fixed-`q`
endpoint Jacobian and a sharp physical/protection row-space separation.  It
does not choose one rank branch uniformly at an unknown source, promote a
marked occurrence selector to a source equation, or provide a dual against
simultaneous `q` motion.

Run:

```text
python3 computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py
python3 -O computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py
python3 -I -S computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py
```

Frozen ledger SHA-256:

```text
e3ec6fc86bb0b50ad42b8a24bc77c49d67e15954abebf151e0ddab17270f5355
```
