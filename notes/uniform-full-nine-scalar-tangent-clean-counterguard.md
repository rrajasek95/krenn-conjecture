# A uniform scalar full-nine counterguard to a formal tangent-or-clean dichotomy

Research counterguard only.  This note works in a common scalar coefficient
quotient of the nine endpoint equations.  It is not a physical
site-square-zero matching source and does not refute the unified overlap
theorem.  It proves that the desired tangent-or-clean alternative cannot be
deduced from the nine scalar anchor equations, Segre star factorization,
and the Hasse--Schmidt cokernel alone.  A valid proof must use literal
multisite/source grading or cross-chart coupling before taking this scalar
quotient.

## 1. Outcome

For every \(h\ge3\) there is an exact rational packet with one common
internal scalar, a literal rank-one star response matrix, all nine endpoint
equations, three nonzero diagonal targets, and nonzero direct curvature.
Nevertheless, it has both

\[
 [\text{shift obstruction}]\in
   \operatorname {coker}J_{\rm star}\setminus\{0\},
 \qquad
 \alpha Q_{h-1}+Q_h\in\mathbb Q\setminus\{0\}.            \tag{1}
\]

This is uniform, not an \(h=3\) response-grade accident.  If \(o_h\) is
the shifted-comparison class and \(\tau_h\) the reciprocal clean
coefficient, then

\[
                       \tau_h o_h\in
        \operatorname {coker}J_{\rm star}\setminus\{0\}.  \tag{2}
\]

Consequently a positive proof has a precise extra obligation: the literal
full-source overlap must construct the annihilator identity
\(\tau_h o_h=0\) before the data are collapsed to scalar anchor rows.
Merely observing that all three anchors are present does not give it.

## 2. The uniform nine-row packet

Fix

\[
 p=(2,-3,5)^{\mathsf T},\qquad
 s=(7,11,-13)^{\mathsf T},\qquad
 t=(17,19,23)^{\mathsf T}.                               \tag{3}
\]

For every \(h\ge3\), put

\[
 q=1,\qquad
 D=\operatorname {diag}(t)-hps^{\mathsf T},
 \qquad
 X_i={t_i\over h!}.                                      \tag{4}
\]

Then all nine equations hold exactly:

\[
\begin{aligned}
 d_{ij}q^{[h]}+p_is_jq^{[h-1]}
 &= {d_{ij}\over h!}+{p_is_j\over(h-1)!}\\
 &= {d_{ij}+hp_is_j\over h!}
  =\delta_{ij}X_i.
\end{aligned}                                             \tag{5}
\]

The response is the common outer product \(ps^{\mathsf T}\), so every
scalar Segre rectangle holds, and all three targets are nonzero.  Select
\((a,b)=(0,1)\) and write

\[
 r=p_0s_1=22,
 \qquad
 \alpha=d_{01}=-hr=-22h.                                 \tag{6}
\]

The direct matrix retains the nonzero curvature minor

\[
 d_{01}d_{12}-d_{02}d_{11}=-494h.                        \tag{7}
\]

Thus neither the selected direct scalar nor elementary curvature vanishes.

## 3. Exact shifted-comparison cokernel

Temporarily regard \(q\) and the six star coordinates as variables, while
\(D\) and the targets remain fixed.  Clear the harmless factorial and set

\[
 G(q,p,s)=Dq^h+hps^{\mathsf T}q^{h-1}
                         -\operatorname {diag}(t).         \tag{8}
\]

At (3)--(4), \(G=0\).  A star tangent
\((u,v)\in\mathbb Q^3\oplus\mathbb Q^3\) has image

\[
                  J_{\rm star}(u,v)=us^{\mathsf T}+pv^{\mathsf T}.
                                                               \tag{9}
\]

This is the five-dimensional Segre tangent space

\[
 {\cal T}_{p,s}=\{us^{\mathsf T}+pv^{\mathsf T}\},
 \qquad \dim{\cal T}_{p,s}=5.                           \tag{10}
\]

After dividing the derivative of (8) by \(h\), the unit \(q\)-direction is

\[
 A_q=D+(h-1)ps^{\mathsf T}
     =\operatorname {diag}(t)-ps^{\mathsf T}.             \tag{11}
\]

Since \(ps^{\mathsf T}\in{\cal T}_{p,s}\), its obstruction is

\[
 o_h=[A_q]=[\operatorname {diag}(t)]
       \in\operatorname {Mat}_3(\mathbb Q)/{\cal T}_{p,s}. \tag{12}
\]

The class is nonzero.  Suppose instead that

\[
             \operatorname {diag}(t)=us^{\mathsf T}+pv^{\mathsf T}.
                                                               \tag{13}
\]

All entries of \(p,s\) are nonzero, so put \(x_i=u_i/p_i\) and
\(y_j=v_j/s_j\).  The six off-diagonal entries give

\[
                         x_i+y_j=0\qquad(i\ne j).          \tag{14}
\]

With three labels, (14) forces all \(x_i\) to have one common value and
all \(y_j\) its negative.  Every diagonal entry on the right of (13) is
then zero, contradicting \(t_i\in\mathbb Q^\times\).  Hence

\[
 \operatorname {rank}{\cal T}_{p,s}=5,
 \qquad
 \operatorname {rank}({\cal T}_{p,s},A_q)=6.             \tag{15}
\]

This allows every first-order star correction but holds the direct and
target anchors fixed.  If the anchors are erased, (11) becomes
\(-ps^{\mathsf T}\), which a star scaling absorbs.  Thus the anchor
numerators are exactly the surviving shifted-comparison class; they do not
supply its nullhomotopy.

## 4. The reciprocal endpoint remains dirty

Put

\[
                 Q_j=r^{[j]}q^{[h-j]}
                    ={r^j\over j!(h-j)!},
                 \qquad0\le j\le h.                      \tag{16}
\]

The admitted endpoint row is

\[
                         \alpha Q_0+Q_1=0,                \tag{17}
\]

because \(\alpha=-hr\).  Its reciprocal terminal relation would set
\(\alpha Q_{h-1}+Q_h\) to zero.  Instead,

\[
\begin{aligned}
 \tau_h:=\alpha Q_{h-1}+Q_h
 &= -{hr^h\over(h-1)!}+{r^h\over h!}\\
 &= -{(h^2-1)r^h\over h!}
    \in\mathbb Q^\times.                                  \tag{18}
\end{aligned}
\]

Even the complete target-eliminated nonlinear clean error survives:

\[
 \sum_{j=2}^h\alpha^{h-j}Q_j
 ={r^h\over h!}\left((1-h)^h-(-h)^h-h(-h)^{h-1}\right)
 ={r^h(1-h)^h\over h!}
 \in\mathbb Q^\times.                                    \tag{19}
\]

The last expression is nonzero for every \(h\ge2\).

The obstruction space (12) is a rational vector space.  Multiplication by
the nonzero scalar (18) is injective, proving (2).  Thus the formal
implication

\[
 o_h\in\operatorname {coker}J_{\rm star}\setminus\{0\}
 \quad\Longrightarrow\quad\tau_h=0                       \tag{20}
\]

is false at the common scalar full-nine level.

## 5. Exact consequence for a uniform proof

The packet preserves more than an isolated response recurrence:

- all nine rows use the same \(q\), star triples, and direct matrix;
- the response matrix is literally rank one;
- all three diagonal targets are nonzero;
- selected direct and curvature values are nonzero; and
- the comparison is tested modulo all six star tangent parameters.

Therefore presence of the three scalar anchors, scalar Segre
factorization, nonzero curvature, or the bare Hasse--Schmidt class cannot
by itself prove tangent-or-clean.  A positive physical proof must produce

\[
                         \tau_h o_h=0                     \tag{21}
\]

in the physical augmented cokernel.  Over a field, (21) gives exactly the
desired alternative: if \(\tau_h\) is nonzero then \(o_h=0\), and
contrapositively failure of the shifted comparison forces the reciprocal
tail to vanish.  Equation (21) is a concrete test for a proposed
construction, but this family proves it is not a formal consequence of the
nine scalar equations.

## 6. Scope relative to the dashed arrow

This is not a decorated matching source.  The internal quadratic is
collapsed to \(q=1\), site-square-zero grading is absent, and the three
targets are not simultaneous pure-colour tensor fibres.  The packet does
not satisfy the automatic physical packet of the unified theorem and
cannot refute its dashed arrow.

That limitation is the useful conclusion.  Any successful proof must use
at least one structure destroyed by scalar contraction: simultaneous
labelled pure targets, multisite matching support, all-label
connection/normal rows, the tilted or direct-free second chart, or a
source-provenant higher Hasse--Schmidt comparison intertwining them.  A
proof which first reduces to nine scalar anchor equations has already lost
the required annihilator identity.

## Exact verification

The dependency-free checker
[verify_uniform_full_nine_scalar_tangent_clean_counterguard.py](../computations/verify_uniform_full_nine_scalar_tangent_clean_counterguard.py)
uses exact rational arithmetic.  For every \(3\le h\le15\) it verifies all
nine equations, all targets, (7), (15), the anchor-free lift, (18), (19),
and the nonvanishing product (2).  Its frozen ledger digest is

    e3cdcc445d69b6f07ab283cfcbc7489d9973e8da476bdd7a3b20bd62b86ea57d

The formulas prove the family for every \(h\ge3\); the finite range is a
regression audit, not the theorem's scope.
