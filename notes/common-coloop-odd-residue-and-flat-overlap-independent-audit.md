# Independent audit: common-coloop odd residue and flat overlap

Audit date: 2026-07-29.

## Verdict

**PASS after one expository correction.**  The residue is well-defined in
the stated top-degree quotient, kills the genuine vertex-gauge image, and
has exactly the displayed normalization on canonical physical caps.  The
linear overlap identity transports the residual constant-colour class; it
does not annihilate it.  The proposed residue--second-polar/Omega lemma is
still unproved and would be a genuinely nonlinear additional input.

During this audit Section 7 was amended to say explicitly that the proposed
lemma is not the conjecture under a new name: it is confined to the already
reduced common-coloop scalar-zero stratum and asks for the vanishing of one
specified odd-overlap quotient class from the branch-specific nonlinear
bad-locus equations.  No mathematical formula in the source note required
correction.

## 1. Degree and divided-power ledger

On the odd set \(|K|=2h-1\),

\[
 A=q_0^{[h-1]}\in {\cal R}_{2h-2}(K),\qquad
 B=q_0^{[h-2]}\in {\cal R}_{2h-4}(K).
\]

Thus \(TZB\) lies in the top component
\({\cal R}_{2h-1}(K)\), while \({\cal R}_1(K)A\) is a subspace of
that same component.  The two divided-power products used later are

\[
 q_0B=(h-1)A,
 \qquad q q^{[h-1]}=h q^{[h]}.
\]

Both factors are present in the source note in exactly the places where
they are needed.

For a fixed monomial of \(Tq_0^{[h-1]}\), let \(y\) be the site supplied
by \(T\).  Distinguishing one of the \(h-1\) matching edges as the
\(Z_{q_0}^{\beta}\)-edge makes its total endpoint weight

\[
 \sum_{z\in K}\beta_z-\beta_y.
\]

This proves coefficientwise, without a nonvanishing or cancellation
assumption,

\[
 Z_{q_0}^{\beta}Tq_0^{[h-2]}
 =\left(\left(\sum_z\beta_z\right)T-\beta\mathbin\cdot T\right)A.
\]

Consequently the residue map descends through the vertex-gauge quotient.
The note correctly asserts only gauge invariance, not injectivity of the
resulting map \(\Theta_{q_0}\).

## 2. Canonical cap and overlap normalizations

The raw pair row

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i
\]

is equivalent to

\[
 (h p_i s_j+a_{ij}q)q^{[h-1]}=h\delta_{ij}X_i.
\]

After exposing \(x\), the coefficient of \(e_c^{(x)}\) is therefore

\[
 L_c^{ij}A+P_{pq}^{ij}t_cB
   =h\delta_{ij}\delta_{ic}Y_i.
\]

The first term is in \({\cal R}_1A\), giving precisely

\[
 \operatorname{res}_{q_0}(P_{pq}^{ij};t_c)
   =h\delta_{ij}\delta_{ic}\overline Y_i.
\]

There is no missing \(h\) or \(h-1\) factor.  In particular the
\(a_{ij}q_0\)-part has zero residue because
\([t_cq_0B]=(h-1)[t_cA]=0\).

The power-free connection

\[
 P_{pq}^{ij}t_c-P_{px}^{ic}y_j
 =(a_{pq}^{ij}t_c-a_{px}^{ic}y_j)q_0
\]

becomes a multiple of \({\cal R}_1A\) after multiplication by \(B\).
Hence both residues are the same class
\(h\delta_{ij}\delta_{ic}\overline Y_i\).  This is transport, not a
second vanishing equation; the triangle cocycle and its first Bianchi
identity do not change that conclusion.  Gauge changes of either cap do
not change the transported class.

## 3. Scalar-zero contraction and the endpoint-ordered corner

For

\[
 K_*=\tau E_{ab}-\alpha I,\qquad
 \tau=\operatorname{tr}a,\quad \alpha=a_{ab},\quad a\ne b,
\]

one has \(\sum_{ij}(K_*)_{ij}a_{ij}=0\) and
\((K_*)_{cc}=-\alpha\).  Contracting the cap rows first gives
\(P_{pq}^{K_*}=h\overline R_*\); the cap factor \(h\) cancels on the
two sides of the residue formula and yields

\[
 \operatorname{res}_{q_0}(\overline R_*;t_c)
 =-\alpha\overline Y_c.
\]

In the disjoint singleton normalization, \(\overline p_r=0\) and
\(\overline s_s=0\).  The only possible nonzero off-diagonal
\(E_{ab}\)-cell is one of

\[
 \overline p_s\overline s_r,qquad
 \overline p_s\overline s_t,qquad
 \overline p_t\overline s_r,
\]

and every such off-diagonal product has zero residue by the complete cap
formula.  The diagonal contraction therefore leaves exactly the
endpoint-ordered \((t,t)\) corner.  The same computation applies one
label at a time in the unary branches.  Since the \(e_c^{(x)}\) are
independent, distinct missing-label terms cannot cancel.  If
\(\overline Y_c\ne0\), the displayed residue is nonzero, so
\(\overline R_*\) cannot be a vertex gauge; no injectivity of
\(\Theta_{q_0}\) is being smuggled into this conclusion.

## 4. Literal \(h=3\) guard

Name the five edges in (26)

\[
 01_0,\quad23_0,\quad02_1,\quad14_1,\quad34_2.
\]

The complete list of disjoint two-edge matchings is

\[
 (01_0,23_0),\ (01_0,34_2),\ (23_0,14_1),\
 (02_1,14_1),\ (02_1,34_2).
\]

They leave sites \(4,2,0,3,1\), respectively.  Hence the matching
leaving site \(4\) is uniquely the all-0 matching, and the one leaving
site \(3\) is uniquely the all-1 matching, proving the two lift
identities.  There is only one colour-2 edge, so no coefficient of an
element of \({\cal R}_1A\) can equal the all-2 tensor; therefore
\(\overline Y_2\ne0\).

After adjoining \(x\), every cell in the indicated \(2\times2\)
rectangle except \((2,2)\) collides at site \(0\).  For \((2,2)\), the
only possible completing edge of \(B=q_0\) is \(34_2\), and its product
is exactly \(X_2\) with coefficient one.  Thus the example really uses
one quadratic and its consecutive divided powers and realizes one
nonzero residual corner.  It correctly disclaims the missing endpoint
rows and direct matrix, so it is a guard against a one-chart argument,
not a counterexample to the full-nine system.

## 5. Remaining proof obligation

The source note clearly separates the proved linear facts from the open
step.  The proposed residue--second-polar/Omega lemma must use either the
inactive-root Omega bad-locus equations or the rootless saturated
Macaulay condition to force one explicit residue to vanish.  Those are
nonlinear, branch-specific hypotheses absent from the flat connection
calculation.  Accordingly the lemma is a proper localized interface for
future work, but is not established by this note and must not be cited as
closure of the conjecture or of the common-coloop branch.
