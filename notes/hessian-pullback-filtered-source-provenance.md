# A Hessian pullback has a second, source-grade lift obstruction

## 1. Outcome

Work after one fixed scalar coefficient cut on the six residual sites.  Let

\[
 L_q:{\cal A}_2\longrightarrow {\cal A}_4,
 \qquad b\longmapsto bq,
 \tag{1}
\]

where \({\cal A}=\mathbb C[x_0,\ldots,x_5]/(x_0^2,\ldots,x_5^2)\).
In edge/four-set coordinates this is exactly the weighted \(K_6\) Hessian
\(T_q\).  Let \(C\subseteq {\cal A}_2\) be the physical cap family and
suppose, for some \(\beta\in C\),

\[
                     L_q^*\mu=\lambda=d\kappa_q,
 \qquad \lambda(\beta)\ne0.                                \tag{2}
\]

Equation (2) proves an aggregate degree-four coefficient identity.  It does
not yet make \(\mu\) a consequence of the physical cap equation, which
lives two degrees higher.  There is a second multiplication map

\[
 U_q:{\cal A}_4\longrightarrow {\cal A}_6,
 \qquad c\longmapsto cq,                                    \tag{3}
\]

and, with \(M_q(b)=bq^{[2]}\), the exact filtered identity is

\[
                         U_qL_q=2M_q.                         \tag{4}
\]

Consequently a Hessian pullback is induced by the top cap equation on a
physical cap subspace \(C\subseteq{\cal A}_2\) if and only if

\[
 \boxed{\quad
 \mu\in\operatorname {im}U_q^*+(L_qC)^\perp.
 \quad}                                                       \tag{5}
\]

For \(C={\cal A}_2\), this says that the affine pullback class of \(\mu\)
must meet \(\operatorname {im}U_q^*\).  If \(T_q\) is invertible, the
pullback is unique, but (5) remains an independent condition.  Thus
invertibility removes \(\ker L_q^*\); it does not solve source provenance.
The factor two in (4)--(5) is not absorbed into the definition of \(U_q\):
applying a top functional \(\nu\) produces
\(\lambda(b)=2\nu(bq^{[2]})\).  Since the field is \(\mathbb C\), one may
rescale \(\nu\), but retaining the factor is essential when comparing the
literal divided-power rows.

The distinction already survives on a two-dimensional pencil consisting
entirely of rank-one caps.  At the uniform physical scalarization
\(q_{ij}=1\), take the four-cycle \(01,23,03,12\).  Then \(T_q\) is
invertible, \(T_qc=c\) for its alternating vector \(c\), and the unique
pullback of \(d\kappa_q=c\) is \(\mu=c\).  Nevertheless

\[
 C=\operatorname {span}(x_0x_1,x_0x_3)
   =\{x_0(ux_1+vx_3):u,v\in\mathbb C\}                       \tag{6}
\]

is a rank-one cap pencil on which

\[
 d\kappa_q\bigl(x_0(ux_1+vx_3)\bigr)=u-v,
 \qquad
 M_q\bigl(x_0(ux_1+vx_3)\bigr)=3(u+v)x_{[6]}.               \tag{7}
\]

No one top-row functional turns \(3(u+v)\) into \(u-v\).  In particular,
the member \(\beta=x_0x_1\) is a literal rank-one cap with
\(d\kappa_q(\beta)=1\) and \(\beta q^{[2]}=3x_{[6]}\), while the pencil has
no source-grade lift.  This is a scalarized filtered guard, not a complete
full-nine Krenn source.

The complete full-nine overlap can add source-valid degree-four rows, but
it must do so before multiplication by the common power.  If
\({\mathscr O}_{\rm gr}\subseteq{\cal A}_4^*\) denotes the span of rows
whose direct/star/internal companions have been cancelled by literal
overlap equations, the exact remaining provenance module is

\[
 \boxed{
 {\mathfrak P}_{q,C}({\mathscr O}_{\rm gr})=
 { {\cal A}_4^* \over
   \operatorname {im}U_q^*+(L_qC)^\perp+{\mathscr O}_{\rm gr}}.}
 \tag{8}
\]

The selected pullback is source-valid precisely when \([\mu]=0\) in (8).
This gives a concrete target for the overlap argument.  The known Bianchi
connection supplies necessary representatives and their grade companions;
it has not yet been shown to kill this class.

Finally, a static \(\mu\) does not by itself give the residual Macaulay
annihilator.  At \(h=3\), the rootless contradiction requires one nonzero
\(\theta\in(\operatorname {Sym}^5\mathbb C^2)^*\) satisfying three shifted
identities for every clean coordinate cubic.  Section 5 records these
identities explicitly.  One natural source-faithful construction would be
a degree-two prolongation of the same grade-preserving overlap packet; this
is a proposed sufficient route, not a necessary form of every possible
proof.  In any route, one nonzero evaluation in (2) is not yet the required
common \(\theta\).

## 2. The two multiplication stages

Write \(x_S=\prod_{i\in S}x_i\).  For an edge array
\(b=\sum_{|e|=2}b_ex_e\), the coefficient of \(x_V\), \(|V|=4\), in
\(bq\) is

\[
              (L_qb)_V=\sum_{e\subset V}b_eq_{V\setminus e}. \tag{9}
\]

This is the definition of \(T_q\).  Indexing \(V\) by its complementary
edge \(f=V^c\) turns it into the symmetric Hessian matrix \(H_q\).

The second multiplication has only one scalar output after the fixed
coefficient cut:

\[
                  U_q(c)=\left(\sum_{|V|=4}c_Vq_{V^c}\right)x_{[6]}.
 \tag{10}
\]

Since \(q^2=2q^{[2]}\), equations (1), (3), and (10) prove (4).  Dually,

\[
                         L_q^*U_q^*=2M_q^*.                 \tag{11}
\]

There are therefore two logically different row-space questions:

1. \(\lambda\in\operatorname {im}L_q^*\), the Hessian compatibility
   already assumed in (2);
2. a chosen pullback \(\mu\) belongs, modulo rows invisible on the physical
   cap family, to \(\operatorname {im}U_q^*\).

Only the second condition permits applying a functional directly to
\(\beta q^{[2]}=T\).  It cannot be inferred from the first.

**Proposition 2.1 (relative source-grade criterion).**  Let
\(C\subseteq{\cal A}_2\), let \(\mu\in{\cal A}_4^*\), and put
\(\lambda=L_q^*\mu\).  The following are equivalent.

1. There is \(\nu\in{\cal A}_6^*\) such that

   \[
              \lambda(b)=2\nu(M_qb)\qquad(b\in C).          \tag{12}
   \]

2. Condition (5) holds.

**Proof.**  By (11), equation (12) is

\[
 L_q^*(\mu-U_q^*\nu)(b)=0\qquad(b\in C).
\]

Equivalently, \(\mu-U_q^*\nu\) annihilates \(L_qC\), which is (5).
\(\square\)

For the unrestricted edge module, \((L_qC)^\perp=\ker L_q^*\).  Hence a
pullback exists at both stages exactly when

\[
 \mu\in\operatorname {im}U_q^*+\ker L_q^*,                  \tag{13}
\]

or, equivalently, when
\(\lambda\in\operatorname {im}M_q^*\).  If \(L_q\) is invertible,
\(\ker L_q^*=0\), so its unique inverse makes (13) especially transparent
rather than automatic.

For a single fixed \(\beta\) with \(M_q\beta\ne0\), one can of course
choose a scalar \(\nu\) which reproduces the one number
\(\lambda(\beta)\).  That tautology is not a source lift.  The clean-line
and Macaulay arguments require one linear identity on a cap family and all
of its parameter shifts.  This is why the relative subspace \(C\), rather
than one vector, appears in Proposition 2.1.

## 3. An invertible rank-one-pencil guard

Put \(q=\sum_{i<j}x_ix_j\), and index four-set coordinates by complementary
edges.  Then \(L_q\) is the disjointness matrix \(W\) of \(KG(6,2)\), while
\(\operatorname {im}U_q^*\) is the line spanned by the all-one vector.

Let

\[
 \kappa(a)=a_{01}a_{23}-a_{03}a_{12},
 \qquad
 c=e_{01}+e_{23}-e_{03}-e_{12}.                              \tag{14}
\]

The uniform point is four-cycle-flat and

\[
                         d\kappa_q=c.                         \tag{15}
\]

Every supported edge of \(c\) has exactly one disjoint supported edge,
with the same sign, while an unsupported edge sees either zero supported
edges or two opposite signs.  Thus

\[
                         Wc=c.                                \tag{16}
\]

The matrix \(W\) is invertible, so \(\mu=c\) is the unique pullback.
But \(c\) is not a multiple of the all-one vector.  More sharply, on the
pencil (6), formulas (7) follow from

\[
 c_{01}=1,\qquad c_{03}=-1,
 \qquad \operatorname {Haf}_{[6]\setminus e}(q)=3.          \tag{17}
\]

If (12) held, some scalar \(a\) would satisfy

\[
                         u-v=6a(u+v)                           \tag{18}
\]

for all \(u,v\), which is impossible.  This proves the guard.

Notice that every pencil member in (6) has the literal factorization
\(LS\), with \(L=x_0\) and \(S=ux_1+vx_3\).  Thus factor rank one and a
nonzero physical four-cycle differential do not remove the second lift
obstruction.  What the guard omits is the complete decorated full-nine
overlap; that omitted structure is exactly what must kill (8).

## 4. What the full-nine overlap must add

Let \(C\) now be the scalarized edge-grade image of the actual cap line (or
of the full cap matrix if all nine rows are retained).  Define
\({\mathscr O}_{\rm gr}\) to contain only those four-set covectors which
occur as the residual edge-grade part of a literal source identity after
all other grades and target terms have been accounted for.  A raw arbitrary
four-set coefficient functional is not, by that definition, an element of
\({\mathscr O}_{\rm gr}\).

Proposition 2.1 immediately gives the exact overlap target:

**Proposition 4.1 (overlap lift criterion).**  A Hessian pullback \(\mu\)
is source-valid on \(C\), using top cap rows and the admitted
grade-preserving overlap rows, if and only if there are

\[
 \nu\in{\cal A}_6^*,\qquad o\in{\mathscr O}_{\rm gr}
\]

such that

\[
 \boxed{\quad
             \mu-U_q^*\nu-o\in(L_qC)^\perp.
 \quad}                                                       \tag{19}
\]

Equivalently, \([\mu]=0\) in (8).

The signs in (19) follow the convention that the admitted overlap row
\(o\) is added to the top-row representative \(U_q^*\nu\).  Reversing the
orientation of an overlap replaces \(o\) by \(-o\) and does not change the
linear space \({\mathscr O}_{\rm gr}\) or the quotient (8).

This statement identifies exactly which known overlap formulas must be
retained when constructing \(o\).

* The power-free connection

  \[
        P_{pq}t-P_{pr}y-(At-By)z=0                            \tag{20}
  \]

  fixes the actual cap representatives.  Its version only after
  multiplication by a common power is not enough.
* The normal-row companion

  \[
        L_{pq;r}-L_{pr;q}=-(m-2)(At-By)                       \tag{21}
  \]

  is required to cancel the adjacent star grade with the correct divided-
  power normalization.
* At a fourth exposed site, both the curvature row

  \[
  UP_{pq}+tL_{pq;s}-FP_{pr}-yL_{pr;s}
       =(At-By)v+(AU-BF)z                                    \tag{22}
  \]

  and the direct-double companion

  \[
       M_{pq;rs}-M_{pr;qs}=-(m-2)(AU-BF)                     \tag{23}
  \]

  are needed.  They keep the direct--direct--internal and
  direct--star--star pieces in the same filtration.
* Two differently labelled diagonal anchors and their crossed target-zero
  row must cancel the target grade and the relative diagonal gauge before
  the resulting row is placed in \({\mathscr O}_{\rm gr}\).  Merely adding
  the two anchor equations at top degree puts only an element of
  \(\operatorname {im}U_q^*\) into (19).

For normalization, the upstream canonical cap is
\(P_{pq}=(m-1)xy+Az\).  Hence the normal-row difference has coefficient
\((m-1)-1=m-2\), giving (21), and the direct-double difference is
\(-(m-2)(AU-BF)\), giving (23).  Taking one literal fourth-site coefficient
of (20) gives (22) with coefficient one on every displayed term; there is
no extra factor two.  These are exactly the orientations and factorial
shifts in the power-free Bianchi note.

Equations (20)--(23) are necessary bookkeeping, but their total residual in
(22) is the radial internal term \((AU-BF)z\).  Under a scalarization which
identifies \(z\) with the base array \(q\), its four-cycle derivative is

\[
           d\kappa_q\bigl((AU-BF)q\bigr)
                  =2(AU-BF)\kappa(q).                        \tag{24}
\]

It vanishes on the four-cycle-flat chart.  When \(\kappa(q)\ne0\), scalar
rescaling by \(1/(2\kappa(q))\) gives the desired differential value, so
there is no normalization obstruction off that chart.  This aggregate
rescaling still does not prove that the total Bianchi equation supplies the
literal filtered representative required by (19), and on the flat chart
the radial term is invisible.  The missing filtered splitting must produce
a row \(o\) satisfying (19).  On the flat finite-curvature side, its
associated primal edge component must also give a transverse correction
\(\beta_{\rm src}\) satisfying

\[
                         d\kappa_q(\beta_{\rm src})=AU-BF,    \tag{25}
\]

while its other graded components are cancelled by (20)--(23).  Equation
(25) alone is only one scalar consequence; condition (19) is the dual
family-level provenance assertion needed for the cap line.

Thus the additional overlap lemma is not another invertibility theorem.  It
is the construction of one explicit \(o\) in (19), from the two anchors and
crossed row, with the same coefficient probes and the same direct/star/
internal filtration on all four complementary cuts.

## 5. The separate Macaulay prolongation

Let the scalar clean coordinates on a binary cap line be

\[
 e_\omega(u,v)=\sum_{k=0}^3c_{\omega,k}u^{3-k}v^k.          \tag{26}
\]

Choose the already nonvanishing coordinate \(f\) and let \(L'\) be the
span of the remaining cubics.  A residual Macaulay annihilator is a nonzero

\[
                  \theta=(\theta_0,\ldots,\theta_5)
                    \in(\operatorname {Sym}^5\mathbb C^2)^* \tag{27}
\]

which kills \(f\operatorname {Sym}^2\) and
\(L'\operatorname {Sym}^2\).  In coordinates, for every \(\omega\), this
is exactly

\[
 \boxed{\quad
       \sum_{k=0}^3c_{\omega,k}\theta_{k+j}=0,
       \qquad j=0,1,2.
 \quad}                                                       \tag{28}
\]

The three rows of (28) are the transpose of the Toeplitz block in the
six-row Macaulay matrix.  Including the coordinate \(f\) makes \(\theta\)
descend to \(Q_f^*\); including every other coordinate makes it annihilate
the residual image.  A nonzero solution is therefore exactly the desired
Macaulay rank defect, hence exactly a common clean root by the proved
residual-gcd theorem.

The indices of \(\mu\) are fifteen four-set cuts.  The indices of
\(\theta\) are the six degree-five monomials.  Equation (2) supplies one
static coefficient comparison and does not define a map between these two
spaces.  A concrete sufficient continuation is to prolong the overlap
construction in Section 4 by \(u^2,uv,v^2\) and prove all three equations
in (28) with one common nonzero \(\theta\).  This would amount to a
grade-preserving chain map from the source quotient (8) to the dual
Macaulay complex.  No claim is made that every possible construction of a
Macaulay cokernel functional must factor through that chain map.

This isolates the exact remaining module:

\[
 \boxed{
 \begin{gathered}
 [\mu]\in{\mathfrak P}_{q,C}({\mathscr O}_{\rm gr})
       \quad\text{must first be killed by a literal filtered overlap,}\\
 \text{while the rootless contradiction separately requires}
       \quad\theta\in\ker(\operatorname {Mac}_{\cal E}^*)\setminus\{0\}.
 \end{gathered}}                                             \tag{29}
\]

The first line is a source-provenance obstruction.  The second is the
rootless clean-line obstruction.  Aggregate Hessian compatibility proves
neither one; prolonging the same literal overlap is the most direct
candidate for proving both together, not an asserted equivalence.

The dependency-free checker
[`verify_hessian_pullback_filtered_source_provenance.py`](../computations/verify_hessian_pullback_filtered_source_provenance.py)
verifies (4), the exact uniform \(K_6\) inverse data used in (14)--(18),
the rank-one pencil formulas (7), and the Toeplitz/Hankel form (28).
