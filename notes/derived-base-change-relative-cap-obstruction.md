# The split cap block does not manufacture the target-zero cap class

Research obstruction and candidate lemma only. The unified overlap theorem,
SP-CLEAN-BRIDGE, and Krenn's conjecture remain open.

## 1. Outcome

There is a canonical derived class near the desired \(h=3\) response, but it
has the opposite logical meaning from the hoped-for proof class. Put

\[
 R=\mathbb Q[A,B,F,U,Y,(\kappa Y)^{-1}],
 \qquad \kappa=AU-BF.                                      \tag{1}
\]

The universal target-augmented cap block is the two-term cochain complex

\[
 G^1=R\langle T,\rho\rangle
 \mathop{\longrightarrow}^{d}
 G^2=R\langle w\rangle,
 \qquad dT=-Yw,\qquad d\rho=w.                            \tag{2}
\]

Here \(T\) is physical target, \(\rho\) is ordinary odd response, and \(w\)
is the cap-relation row. The unimodular change of basis

\[
                 g=T+Y\rho,\qquad \rho=\rho               \tag{3}
\]

splits (2) as a free cycle \(Rg\) plus the contractible identity block
\(R\rho\to Rw\). Consequently

\[
 H^1(G)=Rg,\qquad H^2(G)=0,                               \tag{4}
\]

and target projection is an isomorphism on \(H^1(G)\). In particular,
there is no nonzero target-zero cap class in \(G\), before or after any
flat or non-flat base change.

Let \(B=Rw[-2]\subset G\). In the relative quotient \(G/B\), the element

\[
                         p_c=-\kappa Y\rho                 \tag{5}
\]

is target-zero and has the desired response \(-\kappa Y\). The exact
triangle \(B\to G\to G/B\to B[1]\) has connecting morphism

\[
                \partial[p_c]=-\kappa Y[w].               \tag{6}
\]

Thus \(-\kappa Y\) is canonical as a **relative lifting obstruction**, not
as an absolute Tor, Yoneda, Massey, or Atiyah class. On the active open set
(1), the connecting map from the target-zero line \(R\rho\) to \(Rw\) is an
isomorphism. The associated Yoneda operation certifies that (5) does not
lift to the augmented cap complex.

The exact positive datum still missing is a second, source-provenant lift of
the same row \(w\), invisible to target and ordinary residue. If the full
two-chart complex contains \(n_c\) with

\[
 d n_c=\kappa Yw,\qquad
 \operatorname {tgt}(n_c)=0,\qquad
 \operatorname {ores}_c(n_c)=0,                          \tag{7}
\]

then

\[
                 z_c=n_c-\kappa Y\rho                     \tag{8}
\]

is a target-zero cycle with response \(-\kappa Y\). Formula (7), together
with control of degree-zero indeterminacy, is a well-typed version of the
adjacent-power/cross-quotient nullhomotopy requested by the filtered-\(d_2\)
calculation. It is not supplied by ordinary derived base change.
Constructing it from the full all-label cross-word relations is the
genuinely new mathematics isolated by this viewpoint.

Here "ordinary derived base change" refers only to the already split cap
block and formal occupancy modules.  Non-flat base change of the **full
source complex** can enlarge the module of chains whose unwanted boundary
and readouts vanish.  Section 4 records that separate positive-Tor
mechanism; it is absent from the bare cap block.

## 2. Why the universal occupancy split survives every base change

Let \(\mathscr R\) be the polynomial ring in the universal direct entries,
endpoint-star coefficients, and internal matching coefficients. For an
exposed labelled set \((S,\gamma)\), put

\[
 \mathsf P_{\mathscr R}(S,\gamma)
   =\bigoplus_{M\in\operatorname {Match}(S)}\mathscr R[M]. \tag{9}
\]

For a distinguished site \(x\), the occupancy sequence is

\[
 0\longrightarrow\mathsf K_x
 \longrightarrow\mathsf P_{\mathscr R}(S,\gamma)
 \mathop{\longrightarrow}^{\pi_x}
 \mathsf P_{\mathscr R}(S\setminus\{x\},\gamma|)
 \longrightarrow0.                                      \tag{10}
\]

The coefficient-one exposure section is

\[
 s_x[N]=[N]+\sum_{y\notin\{x\}\cup V(N)}[N\cup\{xy\}],
 \qquad \pi_xs_x=1.                                     \tag{11}
\]

This is an actual \(\mathscr R\)-linear splitting, not a generic-rank
statement. Therefore for every \(\mathscr R\)-algebra \(S\), including a
non-flat quotient by all full-nine coefficient equations,

\[
 s_x\otimes1:S\otimes\mathsf P(S\setminus x)
       \longrightarrow S\otimes\mathsf P(S)              \tag{12}
\]

still splits (10). Its extension class and connecting morphism remain zero.
Since all terms are free, replacing tensor by derived tensor does not change
this conclusion.

Evaluation is an additional operation. It sends a formal state \([M]\) to
the product of its direct entries, stars, and divided matching power, and
distinct states can then coincide or cancel. If
\(E\subset\mathsf P_{\mathscr R}(S,\gamma)\) is the submodule of evaluated
relations, the obstruction to descending the canonical section is

\[
 \omega_{s_x}:\pi_x(E)\longrightarrow
          {\mathsf K_x\over E\cap\mathsf K_x},
 \qquad
 \omega_{s_x}(e')=[e-s_x(e')],\quad \pi_x(e)=e'.         \tag{13}
\]

The class is well defined, and \(s_x\) descends exactly when (13) vanishes.
If \(E=J\mathsf P\) comes only from a base-ring ideal \(J\), then the split
decomposition gives

\[
 J\mathsf P=(J\mathsf K_x)\oplus
             J s_x\mathsf P(S\setminus x),               \tag{14}
\]

so (13) is zero. A nonzero occupancy Bockstein must therefore come from a
relation submodule which couples the two occupancy pieces, such as cap
multiplication followed by evaluation. It cannot be blamed on non-flat
base change of the formal state module.

For one chart, the familiar block

\[
 \overline\Theta\longmapsto
 [\overline\Theta t_cq_0^{[h-2]}]                         \tag{15}
\]

is precisely such a section defect. The still-open issue is to produce a
pair-chart, cross-word version of (13) whose invisible component gives (7).

## 3. The exact \(h=3\) relative calculation

In the basis \((T,\rho)\), the matrix of (2) is

\[
                         \begin{pmatrix}-Y&1\end{pmatrix}. \tag{16}
\]

The coefficient \(1\) is important: it makes the cap-relation block split
over the universal ring itself. The target-zero vector (5) satisfies

\[
       d(0,-\kappa Y)=-\kappa Yw\ne0,                    \tag{17}
\]

whereas the actual filtered-\(d_2\) representative is the graph vector

\[
       -\kappa g=(-\kappa,-\kappa Y),                    \tag{18}
\]

which is a cycle and is killed by the common diagonal-anchor mode. This is
exactly the selected-row obstruction already observed in the bounded
filtered packet.

Adjoin a formal generator \(n\) only as a diagnostic, with

\[
 d(T,\rho,n)=(-YT+\rho+\kappa Yn)w,\qquad
 (\operatorname {tgt},\operatorname {ores})(n)=(0,0).    \tag{19}
\]

Then the kernel of (19) has basis

\[
                   g=T+Y\rho,\qquad
                   z=n-\kappa Y\rho.                     \tag{20}
\]

The target-zero part of the kernel is exactly \(Rz\), and \(z\) has response
\(-\kappa Y\). Thus (19)--(20) are the smallest exact \(h=3\) test which any
proposed full-source construction of \(n_c\) must pass. Merely changing the
base ring leaves the two-column matrix (16) and cannot add the third column
in (19).

## 4. Tor, Yoneda, and Atiyah classification

The splitting (3) gives a quasi-isomorphism

\[
                              G\simeq R[-1].              \tag{21}
\]

Hence for any \(R\)-algebra \(S\),

\[
 H^1(G\otimes_R^{\mathbf L}S)=S,\qquad
 \operatorname {Tor}_i^R(H^1(G),S)=0\quad(i>0).          \tag{22}
\]

There is no \(\operatorname {Tor}_1\) or \(\operatorname {Tor}_2\) in the
cap block from which (5) could arise. The same statement holds for the
formal occupancy modules, which are finite free with an explicit splitting.

The triangle in Section 1 does define a canonical Yoneda/connecting
operation, but its value is (6). It is the obstruction to lifting the
relative class, rather than a construction of the absolute class. An
ordinary product of the chart-comparison boundary with the cap relation
still vanishes for the independent Leibniz and site-degree reasons recorded
in the five-exposed-site audit.

Nor is \(\kappa=AU-BF\) an Atiyah curvature of (2). The cap complex is
quasi-isomorphic to a free rank-one module, so its Atiyah class vanishes;
the universal occupancy modules are free as well. Here \(\kappa\) is the
determinant of the selected two-column overlap contraction. Turning it into
an Atiyah or excess-intersection class would require a new cross-chart
object and a specified connection/nullhomotopy. Those are the missing data,
not consequences of the present universal modules.

There is nevertheless a useful place for Tor after the full complex is
defined.  Let \(C^1\) be its universal degree-one chain module, let

\[
 b:C^1\longrightarrow V
\]

collect every forbidden component (target, ordinary residue, and all
boundary rows other than the selected cap row \(w\)), and let
\(a:C^1\to\mathscr Rw\) be the selected cap-row coordinate.  Put

\[
 K=\ker b,\qquad Q=\operatorname {coker}b,
 \qquad I_c=a(K),\qquad \mathcal O_c=\mathscr Rw/I_c.    \tag{23}
\]

Thus \(K\) is the module of **universally** invisible chains whose complete
boundary has no component except \(w\).  For a universal full-nine ring
\(\mathscr R\), relation ideal \(J\), and active evaluated ring
\(S=(\mathscr R/J)[(\kappa Y)^{-1}]\), the short exact sequence
\(0\to I_c\to\mathscr Rw\to\mathcal O_c\to0\) gives

\[
 \operatorname {Tor}_1^{\mathscr R}(\mathcal O_c,S)
 \lhook\joinrel\longrightarrow I_c\otimes S
 \longrightarrow Sw
 \longrightarrow\mathcal O_c\otimes S\longrightarrow0.  \tag{24}
\]

If one restricts to chains descending from \(K\otimes S\), then, because
\(\kappa Y\) is a unit, (7) exists exactly when

\[
                         [w]=0
       \quad\text{in }\mathcal O_c\otimes S.              \tag{25}
\]

This is a degree-zero cokernel membership, not a positive-Tor class.
The \(\operatorname {Tor}_1\) in (24) measures the failure of the universal
boundary image \(I_c\) to remain embedded after base change and contributes
to ambiguity among descended universal choices.

There is a second, genuinely different Tor term.  Assume, as in the finite
free source resolutions under consideration, that \(C^1\) and \(V\) are
free.  Write

\[
 K_S=\ker(b\otimes S:C^1\otimes S\longrightarrow V\otimes S).
\]

Tensoring the kernel/image/cokernel sequences for \(b\) gives the canonical
exact sequence

\[
 0\longrightarrow \operatorname {im}(K\otimes S)
 \longrightarrow K_S
 \longrightarrow \operatorname {Tor}_1^{\mathscr R}(Q,S)
 \longrightarrow0.                                      \tag{26}
\]

Hence a non-flat specialization can create chains which are invisible only
**after** base change.  Their cap coordinate induces a transgression

\[
 \tau_S:\operatorname {Tor}_1^{\mathscr R}(Q,S)
             \longrightarrow \mathcal O_c\otimes S.     \tag{27}
\]

For the full specialized complex, (7) exists exactly when

\[
       [\kappa Yw]\in\operatorname {im}\tau_S.           \tag{28}
\]

The zero class recovers the sufficient degree-zero condition (25).  Thus
(25) is an if-and-only-if only for descended universal invisible chains. In
the full source problem, positive Tor can contribute the first lift through
(27); it cannot do so in the already split cap or formal occupancy blocks,
where the relevant cokernels are free.

## 5. Sharp candidate lemma for the full source complex

The derived discussion reduces the positive route to the following literal
statement.

> **Invisible cross-word lift lemma at \(h=3\).** In the active localization
> of the full all-label \(pq/pr\) overlap--exposure complex, the pure cap row
> \(w_c\) lies in the boundary image of the target- and ordinary-residue-
> invisible cross-word chains. More precisely, there is \(n_c\) satisfying
> (7), all its other full-nine boundary components vanish, and the odd
> readout vanishes on the degree-zero indeterminacy of the cycle (8).

If this lemma holds, (8) is the required nonzero target-zero filtered class.
Conversely, any class with the stated target and response, after subtracting
\(-\kappa Y\rho\), gives a chain \(n_c\) of the form (7). Thus the lemma is
equivalent to the missing lift at this grade, not merely sufficient.

The existing no-go results locate its source. Same-power anchors span only
the graph line \(Rg\), and all-label target Koszul operations preserve that
graph. The subsequent
[mixed-word reset audit](h3-mixed-word-reset-cross-quotient-chain-lift-no-go.md)
sharpens the word-tag conclusion: three of the four relevant strict
coefficient-reset maps do descend to the odd quotient and send the guard
defect to the pure word with the correct scalar. But on a genuine source
their EqSystem input is zero, so the strict reset has zero boundary and zero
odd output. It is not the invisible chain \(n_c\). What is missing is the
one-higher commutator/syzygy which lifts that reset into the relative cap
complex and produces the third column in (19).

Thus none of the presently constructed **universal chain generators** has
an invisible boundary component along \(w_c\), and the strict-reset audit
proves neither (25) nor a nonzero transgression (27).  A proof must turn a
descended reset into a source-resolution homotopy which remains invisible
in target and ordinary residue, either universally or through a controlled
post-specialization Tor class. This is narrower than inventing another
cross-word map: the map exists, but its one-higher source lift does not.

The dependency-free checker
[verify_derived_base_change_relative_cap_obstruction.py](../computations/verify_derived_base_change_relative_cap_obstruction.py)
audits (16)--(20) over exact rational active and direct-free
specializations, the relative connecting value (6), the universal splitting
rank, and the unique target-zero kernel created by a hypothetical invisible
lift. The arguments (9)--(14) and (21)--(28), rather than the finite samples,
are the categorical proofs.
