# The marked-occurrence graph is canonical but contractible

## Result

Let `R=R_11,110000` be the literal mixed response coefficient at the
trapped source, split as

\[
                         R=f+G=0,                     \tag{1}
\]

where `f` is the active protected occurrence and `G` is the aggregate of
the other 89 occurrences.  Adjoining a graph coordinate `u` gives the
source-valid equations

\[
              E=f-u=0,\qquad M=G+u=0,
              \qquad R=E+M.                           \tag{2}
\]

This does construct the occurrence normalization and its scalar target
correction canonically.  It does **not** construct the missing physical
anchor row or the Interface-I comparison cell: the graph is a contractible
presentation of the original source.

The first remaining positive test is one explicit class.  If
`xi in ker(A)` and `H(xi)=df(xi) != 0`, its order-two obstruction is

\[
                   \mathfrak o_2(\xi)
                    =[F_{[2],x}(\xi)]
                    \in\operatorname {coker}(A).       \tag{3}
\]

Either (3) vanishes and `xi` has a second-order lift, or an output covector
`psi` with `psi A=0` detects it.  The occurrence graph adds no further
class.  Identifying (3) with the physical six-term complex still requires
the source-labelled augmented Spencer comparison sought by Interface I.

Checker:
[`verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py`](../computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py).

## 1. The complete response supplies the normalization cell

The physical coefficient `11:110000` has 90 literal terms: six choices for
the left endpoint, five for the right endpoint, and three matchings on the
four residual sites.  The chosen protected monomial is

\[
 f=p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0].            \tag{4}
\]

At an actual source the mixed target coefficient is zero.  Hence (1)
forces `G=-f`, including its scalar correction; no raw coefficient Euler
operator is used.

The graph extension

\[
 \operatorname {Spec}(S[u]/(f-u))\longrightarrow\operatorname {Spec}S
                                                                  \tag{5}
\]

is an isomorphism.  At first order, on the smallest literal quotient with
coordinates `(f,G,u)`, the two rows in (2) are

\[
                    dE=(1,0,-1),\qquad dM=(0,1,1).     \tag{6}
\]

Their sum is `dR=(1,1,0)`.  The old tangent `(1,-1)` lifts uniquely to
`(1,-1,1)`; in particular `df=du` on the graph, not `df=0`.  The private
`-du` pivot makes the relative cotangent complex of (5) acyclic.

On the active chart `u=f != 0`, adjoin the mate ratio `r=G/u`.  Then

\[
 E=f-u,qquad Q=G-ur,qquad N=1+r,                     \tag{7}
\]

and the exact polynomial identity is

\[
                         R=E+Q+uN.                    \tag{8}
\]

Thus `N` is a canonical augmentation-one normalization cell.  But `r` is
the aggregate of 89 occurrence ratios, and `dN=dr` is another private chart
pivot.  It has no canonical literal matching/repeated-`q` boundary,
ordinary-residue value, eta/sigma terminal, or six-term readout.  Eliminating
`u,r` from (7) returns exactly the old response (1).

This is the precise positive and negative answer to the graph proposal:
the complete response constructs a normalization chart, but the chart does
not itself descend to a new optical source cell.

## 2. The graph preserves the obstruction space

Write the full physical source map as `F:X->Y`, with Jacobian
`A=dF_x`, and put `H=df_x`.  The graph map has Jacobian

\[
       \widetilde A=
       \begin{pmatrix}A&0\\ H&-1\end{pmatrix}.         \tag{9}
\]

The private `-1` gives canonical isomorphisms

\[
 \ker\widetilde A\cong\ker A,
 \quad \xi\longmapsto(\xi,H\xi),
 \qquad
 \operatorname {coker}\widetilde A\cong
 \operatorname {coker}A.                             \tag{10}
\]

The checker verifies this both on the cotangent presentation (6) and on
the literal Hasse coefficients.  Every `p*s*q*q` occurrence has moving
degree three.  The selected term has three order-two Hasse monomials, while
the full 90-term response has 270.  Choosing the second graph jet `u_[2]`
equal to `f_[2]` kills the graph equation's second face, and the mate
equation leaves exactly

\[
                     G_{[2]}+f_{[2]}=R_{[2]}.          \tag{11}
\]

For the full map this proves (3): the occurrence graph neither creates nor
cancels the original Hessian obstruction.

Exact Fredholm duality now gives the physically useful finite alternative:

```text
F_[2](xi) in image(A)  -> choose a second source jet;
F_[2](xi) not in image(A) -> a physical output dual psi kills A and detects it.
```

This is an output-row dual, not the occurrence covector `H` and not the
source-cotangent six-term row `Lambda`.

## 3. Why this is not yet the Interface-I cone

The occurrence graph/ratio cone contracts through the private coordinates
`u` and `r`.  Interface I instead needs an occurrence-local
principal-parts/Weyl-bar cell whose boundary remains nonzero after all
presentation coordinates are forgotten, in one literal word/fine/repeated
grade, with physical `W`, residue, anchor, eta and sigma rows.

There cannot be a canonical identification from graph algebra alone.  The
checker freezes two finite polynomial systems with the same response
`R=f+G`, the same `H=df`, the same graph normalization, the same tangent,
and `Lambda=dR in row(A)`.  An independent output equation has zero Hessian
obstruction in one system and a nonzero obstruction in the other.  In the
second, the primitive output covector `(0,1)` kills `image(A)` and reads one
on the obstruction.  Hence the proposed map

\[
       \operatorname {coker}(A)\longrightarrow
       \text{six-term relative complex}               \tag{12}
\]

is additional source data; it is not induced by (2) or (8).

The smallest remaining Interface-II/Interface-I bridge is therefore a
source-labelled Spencer comparison carrying the single class (3) into the
already exhaustive six-term generator/separator alternative.  If its
six-term value is nonzero, it normalizes to the relative generator; if the
readout kills the complete relative homology, the existing physical
separator descends.  The graph chart supplies the scalar normalization
needed to state that comparison, but not the comparison map itself.

## Scope

This theorem constructs the canonical graph and active mate-ratio
normalization from the literal 90-term physical response, proves that its
relative cotangent and obstruction contributions are contractible, and
isolates the first Hessian class with its physical output-dual alternative.
It does not turn `u` or `r` into optical source coefficients, construct
(12), prove higher formal-arc integrability, or close Interface II.

Run:

```text
python3 computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py
python3 -O computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py
python3 -I -S computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py
```

Frozen ledger SHA-256:

```text
14af41bf3463ca9f89651564eb6456bc766c47ba0ced77d79237102a6b7ac550
```
