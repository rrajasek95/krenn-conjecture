# Physical provenance of a common overlap factor is a first-jet condition

## 1. Outcome

The remaining provenance claim in
[the common-factor filtered theorem](common-factor-cocycle-filtered-kill-or-factor.md)
does not follow merely by calling an annihilator representative
“physical.” The canonical source construction remembers one more term.

Fix a fan centre \(p\), put \(U=B\setminus\{p\}\), and let
\(L_a\in{\cal R}_1(U)\) vary the colour-\(a\) row of the physical
\(p\)-star. In the chart which also deletes \(q\), the derivative of the
canonical pair cap is

\[
 J_q(L)^{ab}
   =t(L_a|_{W_q})S_{q,b}+(L_{a,q})_bq_q,\qquad t=m-1.             \tag{1}
\]

The common-factor cocycle retains only the first term. The second is not
optional: the component of the \(p\)-star at \(q\) is the same physical
block as the direct \(pq\) coefficient. Thus

\[
                         (L_a|_{W_q})S_{q,b}                       \tag{2}
\]

is generally the tangential projection of a physical first jet, not a
physical cap variation by itself.
The overlap note absorbs the nonzero scalar \(t\) into \(L_a\), so this
normalization difference has no mathematical content.

This trace gives two exact replacements for the unproved provenance claim.

1. If \(L\) is a \(p\)-local source tangent which preserves the top
   tensor, the annihilator equations and \(q_q^{[t]}\ne0\) force
   \(L_{a,q}=0\) at every fan site. A full fan kills \(L\); the standard
   good fan confines it to at most six exceptional sites.
2. If the visible top response \(L_aQ^{[t]}\) lies merely in the diagonal
   target span, then \(L\) belongs to the physical \(p\)-star span modulo
   \(\ker(H\mapsto HQ^{[t]})\). Its visible coefficient matrix has rank at
   most one and selects one target colour.

The response fork itself supplies neither condition. Its canonical caps
obey an inhomogeneous connection, while alternative annihilator lifts form
an affine torsor. A nonzero homogeneous correction requires an additional
normalization or liftability theorem.

## 2. The canonical cap and its full first jet

Let \(|B|=2m\), set

\[
 U=B\setminus\{p\},\qquad |U|=2t+1,\qquad t=m-1,
\]

and decompose the physical source at \(p\) as

\[
 A=Q+\sum_{a=0}^2e_{p,a}P_a,
 \qquad Q\in{\cal R}_2(U),\quad P_a\in{\cal R}_1(U).              \tag{3}
\]

For \(q\in U\), write

\[
 W_q=U\setminus\{q\},\qquad
 Q=q_q+\sum_{b=0}^2e_{q,b}S_{q,b}.                               \tag{4}
\]

In endpoint order \(p,q\),

\[
                         (P_{a,q})_b=A_{pq}(a,b).                  \tag{5}
\]

The left side is a component of the \(p\)-star; the right side is the
direct pair entry. The canonical unnormalized pair cap is

\[
 {\cal P}_{pq}^{ab}
      =t(P_a|_{W_q})S_{q,b}+(P_{a,q})_bq_q.                       \tag{6}
\]

Now vary only blocks incident with \(p\):

\[
 \dot A=\sum_ae_{p,a}L_a,\qquad
 L_a=L_a|_{W_q}+L_{a,q}.                                        \tag{7}
\]

The internal \(q_q\) and the \(q\)-star into \(W_q\) do not vary.
Differentiating (6), with the incidence identity (5), proves:

**Lemma 2.1 (physical first-jet completion).** The map from a \(p\)-star
variation to pair-cap variations is

\[
 L\longmapsto J(L),\qquad
 J_q(L)^{ab}=t(L_a|_{W_q})S_{q,b}+(L_{a,q})_bq_q.                  \tag{8}
\]

Hence the pure product \(t(L_a|_{W_q})S_{q,b}\) is a literal \(p\)-local
cap variation on a chart with \(q_q\ne0\) only if \(L_{a,q}=0\).

This is coordinate-free. Intrinsically \(L_{a,q}\in V_q\); pairing it
with the colour-\(b\) covector at \(q\) produces the normal coefficient
in (8).

Put

\[
 \mu_Q:{\cal R}_1(U)\longrightarrow{\cal R}_{2t+1}(U),
 \qquad \mu_Q(H)=HQ^{[t]},\qquad C_q=q_q^{[t]}.                    \tag{9}
\]

Contraction at \(q,b\) gives

\[
 \iota_{q,b}\mu_Q(L_a)
   =(L_{a,q})_bC_q
     +(L_a|_{W_q})S_{q,b}q_q^{[t-1]}.                             \tag{10}
\]

Since \(q_qq_q^{[t-1]}=tC_q\), equations (8)–(10) yield the exact
commutative first-jet identity

\[
             J_q(L)^{ab}q_q^{[t-1]}
                    =t\,\iota_{q,b}\mu_Q(L_a).                    \tag{11}
\]

The normal term in (8) is exactly what makes contraction of the cap
variation equal contraction of the source variation.

## 3. Target-preserving provenance kills the fan components

**Theorem 3.1 (target-tangent provenance).** Let \(F\subseteq U\). Assume
for every \(q\in F\) and every \(a,b\) that

\[
 (L_a|_{W_q})S_{q,b}q_q^{[t-1]}=0,\qquad C_q=q_q^{[t]}\ne0.       \tag{12}
\]

If the \(p\)-local source variation (7) preserves the top tensor to first
order,

\[
                         L_aQ^{[t]}=0\qquad(0\le a\le2),           \tag{13}
\]

then

\[
                         L_{a,q}=0
              \qquad(a=0,1,2,\ q\in F).                           \tag{14}
\]

Thus every \(L_a\) is supported on \(U\setminus F\). A full fan \(F=U\)
forces \(L=0\); a good fan of size at least \(|B|-7\) leaves support on
at most six sites.

**Proof.** Insert (12)–(13) into (10). It gives
\((L_{a,q})_bC_q=0\) for every \(b\). Since \(C_q\ne0\), every coordinate
of \(L_{a,q}\) is zero. \(\square\)

The hypothesis (13) is exactly the tangent equation for a variation
supported at \(p\). Indeed,

\[
 A^{[m]}=\sum_ae_{p,a}P_aQ^{[t]},
\]

so differentiation in the direction (7) gives

\[
                         \dot A\,A^{[m-1]}
                   =\sum_ae_{p,a}L_aQ^{[t]}.                      \tag{15}
\]

The site-\(p\) colour components are independent. Therefore a fixed-target
tangent is equivalent to (13).

Notice the distinction between two notions of provenance:

* literal equality of the pure product with the full first jet forces the
  omitted normal term to vanish already in \({\cal R}_2(W_q)\);
* equality only after the Hessian product, together with (13), forces it
  to vanish when \(C_q\ne0\).

Both retain the direct block; neither is a claim about a representative
modulo an annihilator.

## 4. Physical provenance modulo the one-site kernel

Let \(E_p\simeq\mathbb C^3\) be the colour-row space at \(p\), and regard
the physical star and the factor family as maps

\[
                         P,L:E_p\longrightarrow{\cal R}_1(U).     \tag{16}
\]

For an exact ternary source, the one-site rows say

\[
                 \mu_Q(P(e_c))=X_c^U\qquad(0\le c\le2).           \tag{17}
\]

Put

\[
                         D_U=\operatorname{span}
                           \{X_0^U,X_1^U,X_2^U\}.                  \tag{18}
\]

Equation (17) identifies \(\operatorname{im}P\) with \(D_U\), so

\[
                  \operatorname{im}P\cap\ker\mu_Q=0.              \tag{19}
\]

Literal physical-span provenance means
\(L_a=\sum_cM_{ac}P_c\) for one coefficient matrix \(M\).
Coordinate-freely, this says the variation is induced by a single
endpoint-colour endomorphism at \(p\). An arbitrary change of physical
blocks incident with \(p\) is an arbitrary element of
\(\operatorname{Hom}(E_p,{\cal R}_1(U))\), and need not be of this form.

**Proposition 4.1 (quotient provenance).** If

\[
                         \mu_Q(\operatorname{im}L)\subseteq D_U,   \tag{20}
\]

then there are unique coefficients \(M_{ac}\) and
\(K_a\in\ker\mu_Q\) such that

\[
                         L_a=\sum_cM_{ac}P_c+K_a.                  \tag{21}
\]

Thus \(L\) lies in the physical star span modulo the one-site
catalecticant kernel. If, in addition, the common-factor annihilator
equations (12) hold for one \(q\) with \(C_q\ne0\), all nonzero rows of
\(M\) select one common target colour. In particular,

\[
                              \operatorname{rank}M\le1.            \tag{22}
\]

**Proof.** By (17), \(\mu_Q|_{\operatorname{im}P}\) is an isomorphism
onto \(D_U\). Condition (20) therefore defines the unique coefficients
\(M_{ac}\) for which
\(\mu_Q(L_a-\sum_cM_{ac}P_c)=0\); define \(K_a\) by (21). Uniqueness
follows from (19).

For the final assertion, (10) and (12), followed by reconstruction from
the three \(q\)-contractions, give

\[
                    \mu_Q(L_a)=L_{a,q}\otimes C_q.                 \tag{23}
\]

Equations (17) and (21) also give

\[
                    \mu_Q(L_a)=\sum_cM_{ac}X_c^U.                  \tag{24}
\]

The singleton flattening of (24) at \(q\) has rank equal to the number of
nonzero entries in row \(a\) of \(M\), whereas (23) has rank at most one.
Thus every row has support at most one. If two nonzero rows chose distinct
colours \(c\ne d\), the common factor \(C_q\) would be proportional to both
\(X_c^{W_q}\) and \(X_d^{W_q}\), impossible. Hence all nonzero rows choose
one column, proving (22). \(\square\)

This strictly weakens \(L\in\operatorname{im}P\). It gives the same
one-colour conclusion for the visible quotient class, while naming the
exact residue \(K\in\ker\mu_Q\). In the fixed-target tangent case \(M=0\),
and Theorem 3.1 controls that residue on the fan.

## 5. The response fork supplies a torsor, not \(L\)

For \(a\ne b\), the canonical augmented response in
[the response-fork note](good-pair-response-fork-and-exact-overlap-flatness.md)
is represented by

\[
             {\cal P}_{pq}^{ab}
               =t(P_a|_{W_q})S_{q,b}+A_{pq}(a,b)q_q.               \tag{25}
\]

It is an annihilator, but not a homogeneous common-factor family. On a
triple overlap its exact connection is

\[
 {\cal P}_{pq}^{ab}S_{r,c}-{\cal P}_{pr}^{ac}S_{q,b}
   =\bigl(A_{pq}(a,b)S_{r,c}-A_{pr}(a,c)S_{q,b}\bigr)z_{qr}.       \tag{26}
\]

Removing the \(Aq\) terms exposes the literal factor
\(tP_aS_{q,b}\), but generally destroys the annihilator equation.
Conversely, adding an annihilator to simplify a representative destroys
its canonical physical origin.

Let \({\cal A}_q\) be the pair-Hessian annihilator and put

\[
 {\cal Z}_p=
 \left\{(N_q)_q\in\prod_q{\cal A}_q:
    N_qS_r-N_rS_q=0\text{ on every overlap}\right\}.               \tag{27}
\]

Once one lift of the contracted cap data satisfying (26) is chosen, every
other such lift is its translate by \({\cal Z}_p\). The target tensor,
all its further contractions, and the inhomogeneous right side of (26)
are unchanged. This is an affine torsor, not a second physical source.

The common-factor module lies in \({\cal Z}_p\) whenever its products are
pair-Hessian annihilators. The response fork defines neither a map
\({\cal Z}_p\to\operatorname{im}P\) nor a preferred common factor. Taking
the canonical lift sets the correction \(N\) to zero. A noncanonical lift
needs a separate normalization theorem before its factor can be called
physical.

Exact target equations can still constrain \({\cal Z}_p\) through the
physical \(Q\); Proposition 4.1 is one such constraint. What they do not
do is turn an arbitrary point of the lift torsor into a source variation.

## 6. Smallest exact guard against the naive variation claim

Even an actual source variation need not lie in the physical star span.
The smallest exact illustration is the ternary \(K_4\) source. On
\(B=\{p,1,2,3\}\), take the three unit monochromatic perfect matchings

\[
 p1\mid23\quad(\text{colour }0),\qquad
 p2\mid13\quad(\text{colour }1),\qquad
 p3\mid12\quad(\text{colour }2).                                  \tag{28}
\]

Its matching tensor is exactly \(X_0^B+X_1^B+X_2^B\), and

\[
 P_0=e_{1,0},\qquad P_1=e_{2,1},\qquad P_2=e_{3,2}.                \tag{29}
\]

The legitimate \(p\)-incident variation

\[
                         L_0=e_{1,1},\qquad L_1=L_2=0              \tag{30}
\]

does not lie in \(\operatorname{span}\{P_0,P_1,P_2\}\). With

\[
 Q=e_{2,0}e_{3,0}+e_{1,1}e_{3,1}+e_{1,2}e_{2,2},
\]

one has

\[
                         L_0Q=e_{1,1}e_{2,0}e_{3,0},               \tag{31}
\]

a mixed top response outside \(D_U\). Thus “comes from physical edge
blocks” is insufficient: condition (20), fixed-target tangency, or
endpoint-colour linearity is essential.

This is not an E1 overlap countermodel. At this order the pair multiplier
is \(q_q^{[0]}=1\), so there is no nonzero pair-annihilator ambiguity.
A full exact ternary E1 countermodel at larger order would cross the
global conjecture boundary. The example is only the minimal exact guard
against the naive provenance inference; the torsor and first-jet lemmas
apply at every order.

## 7. Corrected E1 interface

The common-factor branch separates into three categories.

1. **Canonical cap.** Keep (25), including its direct term, and use the
   inhomogeneous connection (26). There is no \(L\)-provenance problem.
2. **Target-tangent first jet.** Prove that the homogeneous factor is the
   tangential part of a \(p\)-local fixed-target source tangent. Theorem
   3.1 kills it on a full active fan or confines it to the six-site
   exceptional residue.
3. **Arbitrary lift.** Quotient the common-factor torsor, or prove a
   normalization rule satisfying (20) or induced by one endpoint-colour
   endomorphism. Without such a rule, physical-span provenance is not a
   consequence of the response fork.

The remaining proof task is therefore a first-jet liftability or
catalecticant-kernel theorem, not another homogeneous overlap identity.
Nothing here produces an active cap: the common-factor class is flat and
contains no curvature mismatch.

## 8. Audit

No new search or heavy checker is needed. Equation (8) is the literal
derivative of the canonical cap (6), and (11) follows coefficientwise from
the two matching layers in (10). The rank-one conclusion is the same
singleton-flattening argument already audited by
[the filtered theorem’s checker](../computations/verify_common_factor_filtered_kill_or_factor.py).
The \(K_4\) guard has exactly the three displayed perfect matchings; in
(31), the other two \(Q\)-edges collide with the site occupied by \(L_0\).
