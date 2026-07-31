# Oriented scalar-unit curvature leaves a genuine adjacent-power torsion class

## 1. Outcome

Fix a minimum-entry-support exact ternary aggregate source, a good physical
pair \(p,q\), and \(2h\) residual sites with \(h\ge3\), as in the
[full normal-jet ledger](scalar-unit-full-normal-jet-unary-anchor-ledger.md).
Assume that the pair is the intrinsic scalar unit

\[
 A_{pq}=\alpha E_{aa},\qquad \alpha\ne0,
\]

and assume that its unary cap is clean, \(U_a=0\).  The ledger proves that

\[
 \Theta_a=R_{aa}H_a\ne0.
\]

There are two endpoint-ordered curvature minors at a residual physical pair
\(\{r,s\}\).  If

\[
 \begin{array}{lll}
 B=(p_a)_{r,c},&F=(s_a)_{s,d},&U=q_{rs}(c,d),\\
 E=(p_a)_{s,d},&C=(s_a)_{r,c},&
 \end{array}
\]

then, in the orientation of the power-free four-cut connection, they are

\[
             \kappa^{\rightarrow}=\alpha U-BF,
 \qquad      \kappa^{\leftarrow}=\alpha U-EC.             \tag{1}
\]

The two star pairings \(BF\) and \(EC\) are the two summands of the
coefficient of \(R_{aa}=p_as_a\) at \((r,c;s,d)\).  Consequently, after
choosing an order on the residual sites, the two global oriented curvature
quadratics \(K^{\rightarrow},K^{\leftarrow}\) satisfy the literal identity

\[
 K^{\rightarrow}+K^{\leftarrow}=2\alpha q-R_{aa}.          \tag{2}
\]

This note gives a negative answer to one possible closing move.  Even grant
the **strong global annihilation hypotheses**

\[
 K^{\rightarrow}H_a=K^{\leftarrow}H_a=0,                  \tag{3}
\]

which are stronger than vanishing of selected exposed coefficients.  Their
orientation-free summed consequence is

\[
                    (R_{aa}-2\alpha q)H_a=0.               \tag{4}
\]

One may not cancel \(H_a\).  More sharply, for every \(h\ge3\), the clean
unary equation and the two relations (3) do **not** imply, in the universal
commutative divided-power algebra,

\[
                         R_{aa}q^{[h-1]}=0.                 \tag{5}
\]

Equation (5) is the response vanishing needed by the existing
minimum-entry-support deletion argument.  Section 5 proves an exact
homogeneous ideal nonmembership over \(\mathbb Q\): there is a formal graded
quotient in which \(U_a=0\), both oriented curvature actions vanish,
\(\Theta_a\ne0\), and the class of \(R_{aa}q^{[h-1]}\) is still nonzero.
Thus simultaneous curvature annihilation does not, by the audited
divided-power identities alone, yield the claimed source-minimality
contradiction.

There is nevertheless a clean conditional closing lemma.  If a new
source-faithful result made multiplication by \(H_a\) injective on the
quadratic span containing (4), then (4) would give
\(R_{aa}=2\alpha q\).  Cleanliness would then force

\[
             (3^h-1-2h)q^{[h]}=0,                         \tag{6}
\]

whereas the exceptional target row would make
\((1+2h)q^{[h]}\ne0\).  Since \(3^h-1-2h\ne0\) in characteristic zero,
this would close the branch without a support enumeration.  Carrier
faithfulness—or a source-relative substitute for it—is therefore the
natural decisive lemma, but it is not supplied by goodness or by
\(\Theta_a\ne0\).

This is a no-go theorem for the unqualified inference, not a counterexample
to Krenn's conjecture.  The formal quotient does not assert the full-nine
target tensors, physical site support, goodness, or minimum aggregate
support.  A positive continuation must use precisely such source-specific
information to rule out the torsion class; multiplication faithfulness and
coefficientwise curvature vanishing remain unavailable.

## 2. Divided-power normalization

Normalize the exceptional response by

\[
                         r=\alpha^{-1}R_{aa}.              \tag{7}
\]

Put

\[
 \begin{aligned}
 g&=q+r,\\
 \theta_h&=g^{[h-1]}-q^{[h-1]},\\
 h_h&=\sum_{\ell=0}^{h-2}{1\over\ell+1}
          q^{[h-2-\ell]}r^{[\ell]},\\
 u_h&=g^{[h]}-q^{[h]}-r q^{[h-1]}.
 \end{aligned}                                             \tag{8}
\]

The quantities in the full normal-jet ledger are exactly

\[
 G_a=\alpha g,\qquad
 \Theta_a=\alpha^{h-1}\theta_h,\qquad
 H_a=\alpha^{h-2}h_h,\qquad
 U_a=\alpha^h u_h.                                         \tag{9}
\]

Indeed the exceptional full-nine row becomes

\[
                         X_a=\alpha(q^{[h]}+r q^{[h-1]}),  \tag{10}
\]

and hence (9) contains no suppressed factorial.  Divided-power
multiplication gives

\[
                    \boxed{\theta_h=r h_h}.               \tag{11}
\]

The coefficient \(1/(\ell+1)\) in (8) is forced by
\(r r^{[\ell]}=(\ell+1)r^{[\ell+1]}\).  Also

\[
                    \boxed{u_h=\sum_{k=2}^h
                        q^{[h-k]}r^{[k]}.}                 \tag{12}
\]

Thus \(U_a=0\) is \(u_h=0\), while the response which must vanish for the
old deletion proof is, up to the nonzero scalar \(\alpha\),

\[
                         M_1:=r q^{[h-1]}.                 \tag{13}
\]

## 3. The two orientations and their orientation-free sum

Let \(x\) denote the normalized first endpoint-ordered star quadratic, so
that the other one is \(r-x\).  In coefficient form,

\[
 x_{rs}(c,d)=\alpha^{-1}BF,\qquad
 (r-x)_{rs}(c,d)=\alpha^{-1}EC.                            \tag{14}
\]

The normalized curvature quadratics are therefore

\[
 k^{\rightarrow}=q-x,\qquad
 k^{\leftarrow}=q-r+x.                                    \tag{15}
\]

Equations (1)--(2) are exactly

\[
 K^{\rightarrow}=\alpha k^{\rightarrow},\qquad
 K^{\leftarrow}=\alpha k^{\leftarrow},\qquad
 k^{\rightarrow}+k^{\leftarrow}=2q-r.                    \tag{16}
\]

After the nonzero normalization in (9), the strongest global version of
(3) says

\[
                    (q-x)h_h=(q-r+x)h_h=0.                \tag{17}
\]

Adding the two equations gives

\[
                         c_h:=(r-2q)h_h=0.                \tag{18}
\]

This addition is legal; cancelling \(h_h\) is not.  Notice that a literal
four-cut only sees restrictions of (17).  Site collisions can make such a
restriction zero even when the corresponding curvature coefficient is
nonzero, so (17) deliberately gives the proposed argument more information
than the exposed comparison itself supplies.

## 4. What carrier faithfulness would prove

Suppose, conditionally, that (18) implied \(r=2q\).  Using (12),

\[
 \begin{aligned}
 u_h
   &=\sum_{k=2}^h q^{[h-k]}(2q)^{[k]}\\
   &=\left(\sum_{k=2}^h {h\choose k}2^k\right)q^{[h]}\\
   &=(3^h-1-2h)q^{[h]}.                                  \tag{19}
 \end{aligned}
\]

The exceptional target row (10) would simultaneously give

\[
       \alpha^{-1}X_a=q^{[h]}+2q q^{[h-1]}
                     =(1+2h)q^{[h]}\ne0.                 \tag{20}
\]

Hence \(q^{[h]}\ne0\).  The integer in (19) is positive for \(h\ge2\),
so \(u_h=0\) is impossible in characteristic zero.  This proves the
conditional closing lemma with the exact constants \(3^h-1-2h\) and
\(1+2h\).  Nothing in this calculation licenses the first sentence:
Section 5 shows why (18) itself does not.

## 5. Exact universal nonmembership

Work in the graded polynomial ring

\[
                         S=\mathbb Q[q,r,x],\qquad
                         \deg q=\deg r=\deg x=1,           \tag{21}
\]

using divided powers merely as the factorial-normalized monomial basis.
Let \(I_h\) be the homogeneous ideal generated by

\[
 u_h,\qquad (q-x)h_h,\qquad(q-r+x)h_h.                     \tag{22}
\]

Then

\[
 \boxed{
   \theta_h\notin(I_h)_{h-1},\qquad
   M_1=r q^{[h-1]}\notin(I_h)_h
 }
 \qquad(h\ge3).                                           \tag{23}
\]

It suffices to specialize \(x=q\).  The first oriented generator becomes
zero, the second becomes \((2q-r)h_h=-c_h\), and \(u_h\) is unchanged.  If
either membership in (23) held before specialization, its specialization
would hold in \(\mathbb Q[q,r]\).

For the first membership, use the degree-\((h-1)\) divided-power basis

\[
                         N_k=q^{[h-1-k]}r^{[k]}
                         \quad(0\le k\le h-1).             \tag{24}
\]

The coefficient of \(N_0\) in \(\theta_h=rh_h\) is zero, while its
coefficient of \(N_1\) is one.  On the other hand, the coefficient of
\(N_0\) in \(c_h=(r-2q)h_h\) is \(-2(h-1)\ne0\).  Hence
\(\theta_h\) is not a scalar multiple of \(c_h\), which proves the first
claim.

For the top-degree claim, put

\[
                         M_k=q^{[h-k]}r^{[k]}
                         \quad(0\le k\le h).               \tag{25}
\]

Write \(c_h=\sum_{k=0}^{h-1}c_kN_k\).  Direct divided-power multiplication
gives

\[
 c_k=\mathbf 1_{k\ge1}-{2(h-1-k)\over k+1},               \tag{26}
\]

and in particular

\[
                    c_0=-2(h-1),\qquad
                    c_1=3-h,\qquad c_{h-1}=1.             \tag{27}
\]

Because \(u_h=\sum_{k=2}^hM_k\), membership of \(M_1\) after specialization
would have to take the form

\[
                    M_1=Aq c_h+Br c_h+C u_h               \tag{28}
\]

for constants \(A,B,C\in\mathbb Q\).  The \(M_0\)-coefficient forces
\(A=0\).  The \(M_1\)- and \(M_h\)-coefficients then force

\[
                    B=-{1\over2(h-1)},\qquad
                    C={h\over2(h-1)}.                      \tag{29}
\]

But the \(M_2\)-coefficient of the right side is

\[
             2Bc_1+C={3(h-2)\over2(h-1)}\ne0,             \tag{30}
\]

whereas the \(M_2\)-coefficient of \(M_1\) is zero.  This contradiction
proves the second claim.  It uses only the four displayed coefficients and
is uniform in \(h\); no genericity, root argument, or cancellation of a
matching power occurs.

Equivalently, the homogeneous quotient \(S/I_h\) is a formal exact guard:
the clean unary class and both oriented curvature actions are zero, but the
adjacent comparison and the response required for source-row deletion
survive.  One may truncate this quotient above degree \(h\) without changing
the argument.

## 6. Consequence for the proof frontier

The existing minimum-support contradiction starts only after proving
\(R_{aa}q^{[h-1]}=0\); the other eight full-nine rows then erase every
response with \(p\)-endpoint colour \(a\).  Equations (17) do not reach that
premise.  They instead place \(h_h\) in the common annihilator of two
oriented curvature quadratics, and (23) shows that the desired response is
not a universal consequence of that placement and \(U_a=0\).

A successful continuation must therefore add a genuinely source-relative
statement, for example one of the following:

1. a physical-cut selection theorem proving that one oriented curvature
   action on the actual \(H_a\)-layer is nonzero;
2. a colon/saturation theorem for the literal site algebra which excludes
   the torsion quotient represented by (21)--(23); or
3. a full-nine overlap identity involving the exceptional target row which
   puts \(r q^{[h-1]}\) in the **source-specific** ideal generated by the two
   oriented comparisons and \(u_h\).

The first option must not replace nonzero curvature by nonzero curvature
times \(H_a\).  The second and third must use information absent from the
universal ring above.  This is the exact remaining gap; simultaneous
curvature annihilation by itself is not the minimality contradiction.

The dependency-free
[checker](../computations/verify_intrinsic_scalar_unit_oriented_curvature_torsion_no_go.py)
audits (9), (11)--(12), the orientation sum (16), the conditional constants
(19)--(20), every coefficient in (26), and the nonmembership obstruction
(27)--(30) for \(3\le h\le128\).  It uses explicit exceptions rather than
Python assertions, runs unchanged under python -O, and rejects five
independent mutations: the divided-power denominator, the factor two in
(2), an oriented star-term sign, the clean-unary coefficient ledger, and
the exceptional-target sign in (20).  The checker certifies the formal
divided-power no-go only; it does not realize \(S/I_h\) as a Krenn source.
