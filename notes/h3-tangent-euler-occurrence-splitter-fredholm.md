# Tangent Euler cubes recover nine occurrence directions and expose five determinants

## Outcome

For a mixed six-site hafnian row, the raw logarithmic Euler cube along the
three cells of a marked perfect matching does select that one occurrence:

\[
       \prod_{e\in\mu}(x_e\partial_{x_e})H_z=m_\mu.      \tag{1}
\]

Equation (1) is not a physical splitter.  The three individual edge Euler
fields are not known tangents to the GHZ source fibre; differentiating the
point equation `H_z(A)=0` is invalid without solving the Jacobian equations.

There is, however, an exact tangent correction.  Colour-diagonal GHZ
stabilizers produce source-valid commuting Hasse cubes.  At `h=3`, their top
distinct-cell faces span a rank-nine subspace of the fourteen-dimensional
matching augmentation module.  The first obstruction is sharp: the
remaining rank-five cokernel is spanned by alternating matching covectors
whose polynomial realizations are decorated `3 x 3` cross-cut determinants.

Thus for every matching-centered profile `c` there is an exact alternative:

1. every alternating `K3,3` determinant annihilates `c`, in which case a
   source-tangent corrected Euler-cube combination has top face `c`; or
2. one six-term determinant reads nonzero on `c`, and is its first filtered
   occurrence-module obstruction.  It becomes a Jacobian/Fitting carrier
   only if its evaluated decorated minor is nonzero.

Every centered individual occurrence lies in the second branch.  Tangent
Euler structure therefore advances the formal occurrence-localization space
from rank zero to rank nine, but it cannot localize one matching.

The simultaneous all-component Cartan theorem `bcc75e1` means this
localization is **not needed** for dark-component absorption.  Its remaining
possible uses are narrower: anchor-critical global entry and transverse
Fitting landing.  Identifying the residual determinant with a protected
physical carrier is the exact additional typing theorem for either use.

Checker:
[`verify_h3_tangent_euler_occurrence_splitter_fredholm.py`](../computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py).

## 1. Why the raw selector is illegal

Write

\[
 H_z=\sum_{\nu\in\mathcal M_6}m_\nu,
 \qquad m_\nu=\prod_{e\in\nu}x_e,                      \tag{2}
\]

where the edge variables carry the endpoint colours prescribed by `z`.
The monomials are squarefree and a perfect matching containing every edge of
`mu` is `mu` itself.  This proves (1) as a polynomial identity.

At an exact source `A`, a physical first jet `xi` must satisfy

\[
                              J_A\xi=0.                 \tag{3}
\]

The equation `H_z(A)=0` does not imply
`x_e partial_e H_z(A)=0`, much less the corresponding equations in every
other output word and protected target row.  Hence applying the edge Euler
operators to the value equation is not a source construction.  This is the
same distinction between a polar symbol and a corrected Hasse jet used by
the existing marked-polar theorems.

## 2. Physical tangent lifts of arbitrary selected-word site weights

Use the balanced mixed word

\[
                              z=001122.                 \tag{4}
\]

For colour-diagonal site weights `lambda_(i,c)`, let

\[
 X_\lambda(x_{ij}^{ab})
   =(\lambda_{i,a}+\lambda_{j,b})x_{ij}^{ab}.           \tag{5}
\]

If

\[
                         \sum_i\lambda_{i,c}=0
                         \quad(c=0,1,2),                \tag{6}
\]

then `X_lambda` preserves every pure GHZ coefficient.  It scales every
mixed output row `H_w` by `sum_i lambda_(i,w_i)`, so at an exact GHZ source,
where those rows vanish, it also satisfies (3).  These are actual
coefficient-space torus tangents, not formal presentation differences.

Every site-weight vector on the selected word (4) lifts through (6).  To
realize the basis vector at site `i`, put `+1` in `(i,z_i)` and `-1` in the
same colour at any site whose selected colour is different.  The negative
weight is invisible in (4), while (6) holds.  Thus on the selected row the
edge weight is simply

\[
                              a_i+a_j.                  \tag{7}
\]

This extension through unused colour slots is the load-bearing advantage
over colour-blind site Euler gauge.

## 3. The top Hasse face is a cut permanent

Choose three sites `S={i,j,k}` and use their three lifted basis directions.
On a perfect matching `nu`, the distinct-cell part of the mixed third Hasse
coefficient is the permanent of the direction-by-edge weight matrix.  Each
direction is nonzero on the unique matching edge incident to its site.
Consequently that permanent equals one exactly when the three sites lie on
three different matching edges:

\[
 P_S(\nu)=
 \begin{cases}
 1,&\nu\text{ crosses }S\mid S^c,\\
 0,&\text{otherwise}.
 \end{cases}                                           \tag{8}
\]

The six nonzero terms in (8) are the permanent of the decorated `3 x 3`
bipartite edge matrix across the cut.  Complementary subsets give the same
packet, so there are ten unoriented cuts.

Arbitrary triples of selected-word site weights give no larger top-symbol
space.  By trilinearity they reduce to triples of site basis vectors.
Repeated sites have zero distinct-edge face; three distinct sites give
(8).  The checker finds

\[
               \operatorname {rank}\langle P_S\rangle=10.       \tag{9}
\]

The all-ones matching vector lies in this span: each perfect matching
crosses four of the ten cuts.  Therefore the centered differences

\[
                              P_S-P_T                   \tag{10}
\]

span rank nine inside the matching augmentation ideal.

The cut family is stable under `S_6`, and its orthogonal complement is the
determinant family of Section 5.  Over `Q` this gives the exact
`S_6`-module dimension decomposition

\[
 \mathbb Q[\mathcal M_6]
   =\langle\mathbf1\rangle
      \oplus C_{\rm cut}^{0}
      \oplus D_{\rm alt},
 \qquad 15=1+9+5.                                    \tag{10a}
\]

## 4. The full cube is source-valid

Each lifted basis direction has selected-word weight one.  On every
matching monomial, its edge weights therefore sum to one.  For three
directions, the complete mixed Hasse coefficient factors as

\[
 \prod_{r=1}^3\left(\sum_{e\in\nu}w_{r,e}\right)=1.     \tag{11}
\]

The cut permanent (8) is only the distinct-edge face of (11).  Collisions,
including the derivatives of the coordinate-dependent vector fields, form
the lower Hasse face `1-P_S`.  On the full selected row the corrected cube is

\[
                              H_z(A)=0.                 \tag{12}
\]

Taking the difference of the cubes for `S` and `T` makes the complete
coefficient zero even before evaluation.  Its top filtered face is the
nonzero matching-centered profile (10), and its lower face is exactly its
negative.  This is a genuine source-tangent filtered cycle.

It is not yet a degree-zero component projector.  A relative chain map must
kill or land the lower collision face without discarding it by hand.  The
positive theorem here is precisely a top-associated-graded splitter of rank
nine.

## 5. Exact determinant cokernel

Orient a cut `S={s_1<s_2<s_3}` and its complement
`T={t_1<t_2<t_3}`.  Define a covector on matchings by

\[
 D_S(\nu)=
 \begin{cases}
 \operatorname {sgn}(\pi),
   &\nu=\{s_1t_{\pi(1)},s_2t_{\pi(2)},s_3t_{\pi(3)}\},\\
 0,&\nu\text{ does not cross the cut}.
 \end{cases}                                           \tag{13}
\]

This is the literal determinant of the same `3 x 3` bipartite edge matrix.
It has three `+1` and three `-1` matching terms.  Exact incidence gives

\[
        \langle D_S,P_T\rangle=0\quad\text{for all }S,T.          \tag{14}
\]

The ten determinant covectors span rank five.  Since (9) has codimension
five in the fifteen-dimensional matching module, (14) is the full
cokernel:

\[
 \langle P_S\rangle
   =\bigcap_T\ker D_T.                                  \tag{15}
\]

Equations (10), (13)--(15) prove the promised Fredholm alternative for any
matching-centered profile `c`.

For an individual occurrence, center integrally as

\[
                         c_\mu=15e_\mu-\mathbf 1.       \tag{16}
\]

Every matching crosses four cuts, and the determinant on any one of them
reads `+/-15` on (16).  Thus no centered individual occurrence belongs to
the tangent-Euler top image.  The obstruction is already present in the
highest distinct-cell face; lower Hasse corrections cannot repair it.

## 6. Occurrence covectors versus evaluated physical minors

The determinant covector in (13) has a literal polynomial realization, but
the two objects must not be identified prematurely.  Let

\[
 B_S(A)=
 \left(A_{s_i t_j}^{z_{s_i}z_{t_j}}\right)_{1\leq i,j\leq3}       \tag{17}
\]

be the evaluated decorated cross-cut coordinate block.  If

\[
 v_z(A)=\bigl(m_\nu(A)\bigr)_{\nu\in\mathcal M_6},
\]

then direct expansion gives

\[
                    \langle D_S,v_z(A)\rangle=\det B_S(A).         \tag{18}
\]

Thus a nonzero pairing with the **evaluated matching-monomial vector** is an
actual nonzero decorated `3 x 3` minor and hence a rank-three Fitting
carrier.  In contrast, the scalar obstruction pairing
`<D_S,c>` in (15) is only a statement in the occurrence permutation module.
It need not imply (18).

The distinction is sharp even when the marked matching monomial is nonzero.
On the balanced cut `024|135`, take every cross-cut coordinate to have value
one.  Then the marked monomial `01|23|45` has value one and

\[
 \langle D_{024},15e_{01|23|45}-\mathbf1\rangle=15,
 \qquad
 \det B_{024}(A)=0.                                    \tag{19}
\]

So the rank-five abstract debt is not automatically a nonzero physical
minor at the source.

Even when (18) is nonzero, active/Hall landing is conditional.  For the
word `001122`, the ten cuts have an exact colour split.

* Four cuts contain one site of each colour on both sides.  Their
  determinants span rank four.  The identity block across `024|135` has
  determinant one using only the diagonal cells `01,23,45`.  It supplies no
  offdiagonal active occurrence at all.
* Six cuts have colour multiplicities `(2,1,0)|(0,1,2)`, up to colour
  permutation.  Their determinants also span rank four.  Every crossing
  matching term contains at least two offdiagonal cells.  Hence a nonzero
  evaluated determinant contains a nonzero offdiagonal occurrence and can
  enter the bidirectional private-site fan/Hall attack.

The second bullet is entry, not landing.  The two forced offdiagonal cells
can be disjoint edges of one selected anchor matching.  A cross-cut minor
does not make them share a fan centre, escape the anchor union, give three
colour heads at one deleted star, or supply the common nonzero hafnian
cofactor required by the active-minor identity.  The checker freezes an
unbalanced determinant-one block with exactly two disjoint offdiagonal
cells, both allowed to be anchor-contained.

The balanced and unbalanced determinant families each have rank four but
together have rank five.  Therefore the five-dimensional debt does not
split into a disposable diagonal part and an automatically active part.  A
physical colour/head typing theorem is necessary.

## 7. Relation to global entry and transverse landing

The complete-group-bar theorem `4f2472b` left the whole fourteen-dimensional
matching augmentation module.  Tangent Euler cubes fill a canonical
rank-nine part.  The exact remainder is the rank-five alternating
determinant module:

```text
matching augmentation (14)
        |
        +-- tangent Euler cut differences (9)
        |
        `-- alternating determinant debt (5)
```

The new simultaneous-projection theorem changes the role of this
decomposition.  Commit `bcc75e1` analytically projects one complete Cartan
column to every actual anchor-critical component at once.  A bright
component, a typed exit, or a global unit kernel follows without ever
constructing a component-supported physical chain.  Therefore neither the
rank-nine cut packets nor the five determinants are needed to assemble dark
Cartan potentials.

The six signed monomials in (13) give a literal `3 x 3` determinant
polynomial.  Only the nonzero evaluated branch (18) is a Jacobian/Fitting
carrier.  This can matter in two still-open places.

1. **Global entry.** A marked occurrence not yet in an exhaustive
   anchor-critical cover can be tested against (15).  The cut branch gives a
   source-tangent filtered packet; the determinant branch gives an explicit
   dual carrier.  A theorem must still show that one branch joins the cover
   or lands in an existing protected row.
2. **Transverse landing.** An unbalanced nonzero evaluated minor supplies an
   offdiagonal occurrence and enters the existing active/Hall machinery.  To
   become the required landing it still needs a nonzero deleted-star
   cofactor, off-anchor support, and distinct centre heads.  The present
   matching-module computation supplies none of those implications.

There is no automatic `q` transport here.  Every determinant in (13) has
three positive and three negative matching terms, hence matching aggregate
zero.  Since physical

\[
                         q=\sum_{i=1}^6m_i-\operatorname {ainc},    \tag{20}
\]

its value on a determinant packet depends entirely on the separately typed
anchor-incidence row.  The shifted-Kähler/anchor comparison isolated by
`3b74774` remains necessary.

The matching aggregate of every determinant covector is zero.  This makes
the determinant debt a natural **transverse-candidate** module, not a new
terminal module.  It is not yet identified with the existing transverse
residual: that residual lives in local head/deleted-star quotients, whereas
the five-dimensional module lives in site/matching incidence.  Moreover,
physical `q` still depends on the independent anchor-incidence term in
(20).  Target, residue, fine grade, anchor incidence, and indeterminacy all
remain to be checked by an augmented physical comparison.

Accordingly this branch should be continued only through one of the two live
interfaces:

1. prove that cut packets or their determinant duals give anchor-critical
   global entry; or
2. land the alternating determinant module in an existing transverse
   cofactor/Fitting readout.

A higher component-projector construction is no longer a priority.

## Verification

```text
python3 computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py
python3 -O computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py
python3 -I -S computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py
```

Frozen ledger SHA-256:

```text
744792ff8ad294896129f9fffa8cb818c60a37b529e545c59dd51dd440652fd7
```
