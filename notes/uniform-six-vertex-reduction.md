# Exact six-boundary reduction, and two obstructions to making it uniform

This note addresses the missing all-even step: whether an exact three-color
realization on even `n>=8` must yield one on six vertices.  It gives a valid
reduction criterion in terms of boundary cumulants, an exact `q=2,n=8`
counterexample to arbitrary pair deletion with uniform effective-edge
repair, and a finite counting obstruction to extending the special
six-vertex `P^2` ideal cones verbatim to larger `n`.

It does **not** disprove a specifically three-color or more global reduction.
It identifies exact additional data that such a reduction has to control.

## 1. The complete boundary signature of a cap

Let `B=U disjoint-union W`, where `|U|=6` and `|W|` is even.  Let

\[
 K\in\left(\bigotimes_{w\in W}V_w\right)^*
\]

be an arbitrary, possibly entangled, covector.  Work in the square-free
commutative tensor algebra

\[
 \mathscr S_U=\bigoplus_{S\subseteq U}\bigotimes_{u\in S}V_u
\]

from `notes/induction-route.md`.  Put

\[
 x=\sum_{\{u,v\}\in\binom U2}X_{uv}.                       \tag{1}
\]

For every even `S subset U`, define a boundary tensor `C_S` as follows:

\[
 C_S=K\mathbin{\lrcorner}
 \sum_{\substack{N\in\operatorname{PM}(W\cup S)\\
                  N\cap\binom S2=\varnothing}}
       \bigotimes_{e\in N}X_e.                             \tag{2}
\]

Thus the vertices of `S` are all matched across to distinct vertices of
`W`, while the unused vertices of `W` are matched internally.  The
contraction in (2) removes every `W` slot and leaves a tensor on `S`.  Put

\[
                         C=\sum_{S\subseteq U,\ |S|\ {\text{even}}}C_S.
\]

**Lemma 1.1 (exact boundary-signature formula).**

\[
 K\mathbin{\lrcorner}H_B(X)
   =\sum_{S\subseteq U,\ |S|\ {\text{even}}}
      C_S\,H_{U\setminus S}(X)
   =[C\exp(x)]_U.                                          \tag{3}
\]

**Proof.**  In a perfect matching of `B`, let `S` be the vertices of `U`
whose partners lie in `W`.  The remaining vertices `U setminus S` are
matched internally and contribute `H_(U setminus S)(X)`.  The matching on
`W union S` has no `S`--`S` edge and contributes exactly one summand of
(2).  This decomposition is unique, and conversely the two pieces combine
to a unique perfect matching of `B`.  Summing and contracting gives the
first equality.  The square-free exponential identity
`[exp(x)]_T=H_T(X)` gives the second. `QED`

The scalar component is

\[
                 s=C_\varnothing=K\mathbin{\lrcorner}H_W(X).
\]

Assume `s!=0`.  The nilpotent logarithm in `mathscr S_U` is finite, so write

\[
 \log(C/s)=L_2+L_4+L_6,                                    \tag{4}
\]

where the subscript is the vertex-support degree.  Equation (3) becomes

\[
 K\mathbin{\lrcorner}H_B(X)
       =s[\exp(x+L_2+L_4+L_6)]_U.                          \tag{5}
\]

This gives a precise conditional reduction.

**Theorem 1.2 (six-boundary cumulant reduction).**  Suppose
`H_B(X)=Delta_(B,q)`, put

\[
 \kappa_i=K(e_i^{\otimes W}),
\]

and assume `s` and every `kappa_i` are nonzero.  If

\[
 [\exp(x+L_2)\{\exp(L_4+L_6)-1\}]_U=0,                    \tag{6}
\]

then there is a `q`-color matching-tensor realization on the six vertices
`U`.  In particular, `L_4=L_6=0` is sufficient.  Since `|U|=6`, condition
(6) is exactly

\[
                       L_6+L_4(x+L_2)=0.                   \tag{7}
\]

**Proof.**  Condition (6) and (5) give

\[
 sH_U(X+L_2)
 =K\mathbin{\lrcorner}\Delta_{B,q}
 =\sum_i\kappa_i e_i^{\otimes U}.                          \tag{8}
\]

Every degree-two component of `L_2` is an arbitrary tensor on one pair, so
`X+L_2` is a legitimate collection of aggregate edge matrices on `U`.
Apply at one vertex the invertible diagonal map
`e_i mapsto s kappa_i^(-1)e_i`, by applying it to the corresponding endpoint
of every incident edge.  This normalizes (8) to `Delta_(U,q)`.  On six
vertices, the only degree-six contribution in (6) is the expression in
(7). `QED`

### 1.3 Why the large common kernel does not by itself produce a cap

There is a tempting dimension argument when `q=3`.  The conditions
`C_S=0` for `|S|=2,4,6` impose at most

\[
 \binom62 3^2+\binom64 3^4+3^6=2079                 \tag{8a}
\]

linear conditions on `K`, independently of `|W|`.  Let `L` be the span in
`tensor_(w in W) V_w` of the corresponding `W`-side boundary tensors.  The
common kernel is `L^perp`.  It is large once `|W|>=8`, but its restrictions
to `H_W(X)` and the three constant tensors need not be nonzero.

In fact the exact GHZ identity explains the obstruction sharply.  Write

\[
 h=H_W(X),\qquad g_i=e_i^{\otimes W},
\]

and let `F_c^U` be the coefficient of the coloring `c` in the matching
tensor formed only from the internal `U` edges.  Reducing the full
boundary expansion modulo `L` gives the tensor identity

\[
 \sum_{i=0}^2 e_i^{\otimes U}\otimes[g_i]
       =H_U(X|_{\binom U2})\otimes[h].                    \tag{8b}
\]

Consequently

\[
 0=F_c^U[h]\quad(c\text{ mixed}),\qquad
 [g_i]=F_{i^6}^U[h].                                     \tag{8c}
\]

If even one internal mixed coefficient `F_c^U` is nonzero, (8c) forces
`h in L`, and then it forces all three `g_i in L` as well.  Every functional
in the large common kernel therefore vanishes on all four target tensors.
On the other hand, if `[h]!=0`, (8c) already says that the internal
six-vertex tensor is diagonal; moreover `[g_i]!=0` is equivalent to the
corresponding internal constant coefficient being nonzero.

Thus the codimension bound (8a) does not supply the missing nonvanishing.
Proving that these four classes survive the quotient is essentially already
proving that the chosen internal six-vertex tensor is a nondegenerate
diagonal tensor.  A successful dimension argument needs an additional
structural reason to keep `h,g_0,g_1,g_2` out of `L`.

For a cap of a pair, `C=s+r`, so (4) reads

\[
 L_2=r/s,\qquad L_4=-r^2/(2s^2),\qquad L_6=r^3/(3s^3).     \tag{9}
\]

Thus Theorem 1.2 contains the clean-pair lemma, while recording exactly the
four- and six-site data discarded by a naive Schur-complement analogy.

## 2. An exact `n=8` pair-cap obstruction

The failure of (7) occurs already for an exact monochromatic tensor whose
cap lands directly on six vertices.

Start with the rational `q=2,n=6` source (9) in
`notes/induction-route.md`.  Its color-zero contribution is precisely the
sum of the two matchings using edge `56`, and its color-one contribution is
the sum of the two matchings avoiding `56`.  Remove `56`, add vertices
`7,8`, and put

\[
 X_{57}=e_0e_0,\qquad X_{68}=e_0e_0,
 \qquad X_{78}=e_1e_1.                                    \tag{10}
\]

Keep every other matrix from the six-vertex example.  The path
`5-7-8-6` has exactly two matching states: using `57,68`, or using `78`.
Consequently old matchings using `56` extend with new colors `00`, and old
matchings avoiding it extend with new colors `11`.  Hence

\[
                         H_8(X)=\Delta_{8,2}.               \tag{11}
\]

Cap vertices `1,5` by

\[
 K=e_0^*\otimes e_0^*+e_1^*\otimes e_1^*.
\]

On `U=(2,3,4,6,7,8)`, the scalar is `s=1/2`.  The nonzero first-jet edges
are

\[
\begin{array}{c|c}
24&\frac34e_0e_1\\
27&e_0e_0\\
34&-\frac34e_0e_1\\
46&\frac34e_1e_1.
\end{array}                                                \tag{12}
\]

In particular `r^2!=0`; for example the disjoint product of the `27` and
`34` terms is nonzero.

**Lemma 2.1 (no uniform scalar repair).**  For arbitrary
`alpha,beta in C`,

\[
\begin{split}
 H_U(\alpha X+\beta R)
  ={}&\alpha^2\beta e_0^{\otimes6}
   -\frac34\alpha\beta^2
      e_0^{(2)}e_0^{(3)}e_1^{(4)}e_0^{(6)}e_0^{(7)}e_0^{(8)}\\
   &+\frac{\alpha^2(2\alpha+3\beta)}4e_1^{\otimes6}.       \tag{13}
\end{split}
\]

Therefore (13) cannot be diagonal with both diagonal coefficients nonzero.

**Proof.**  Direct enumeration of the fifteen matchings on `U` gives (13).
If its all-zero coefficient is nonzero, then `alpha beta!=0`, making the
displayed mixed coefficient nonzero as well. `QED`

The exact audit is
`computations/verify_n8_pair_cap_obstruction.py`.  It independently
enumerates all 105 matchings on eight vertices, checks (11), derives (12)
from the cap formula, and symbolically verifies (13).

This is not a counterexample to a source-global or specifically
three-color reduction: `Delta_(6,2)` of course has other graph
realizations.  It is an exact counterexample to the claim that an arbitrary
active pair of an exact `n=8` source can be deleted by retaining only a
uniform scalar combination of its old and first-jet edge matrices.  Any
uniform proof must select a cap satisfying (6), or retain the higher
boundary cumulants rather than silently discarding them.

## 3. Why the six-vertex `P^2` cones do not extend verbatim

Let `K_off` denote the ideal of bichromatic edge variables in the source
ring.  For a coloring `c` of `n` vertices, let its three color-class sizes
be `m_0,m_1,m_2`.  The associated-graded leading part of its matching
coefficient `F_c` uses the minimum possible number of bichromatic edges.

**Lemma 3.1 (minimum-crossing matching count).**  If all `m_i` are even,
the minimum bichromatic degree is zero and the number of leading matching
monomials is

\[
                       \prod_{i=0}^2(m_i-1)!!.              \tag{14}
\]

If exactly two class sizes, say `m_a,m_b`, are odd, the minimum degree is
one and the number is

\[
 m_am_b(m_a-2)!!(m_b-2)!!(m_c-1)!!,                       \tag{15}
\]

where `c` is the even class and `(-1)!!=1`.  For `q=3` and every even
`n>=8`, both (14) and (15) are at least three.

**Proof.**  With all class sizes even, a minimum matching is independently
a perfect matching inside each color class, giving (14).  With two odd
classes, exactly one minimum cross edge joins them.  Choose its endpoints in
`m_am_b` ways and match the three even remainders internally, giving (15).
For (14), equality one would require every nonempty even class to have size
two, so the total would be at most six.  For (15), equality one would require
the two odd classes to have size one and the even class size at most two, so
the total would be at most four.  Directly, the smallest value at `n>=8` is
three, attained in (14) at class sizes `2,2,4`. `QED`

Multiplying `F_c` by a fixed residual monomial `Q` cannot identify two of
these terms: `QM_1=QM_2` as monomials implies `M_1=M_2`.  Consequently no
associated-graded Macaulay column at `n>=8` is initially one-term.  The
special six-vertex coloring `2+2+2`, whose diagonal part is one rainbow
perfect matching, has no literal all-even analogue.  Thus the one-term
cones which start the successful `n=6` collapses in
`notes/ideal-membership-route.md` cannot simply be placed on six selected
vertices and copied to larger `n`; a new multi-term homotopy is required.

There is a second obstruction to a naive six-vertex ideal retraction.

**Lemma 3.2 (no disjoint-factor ideal retraction).**  Let `B=U disjoint W`
with `|U|=6` and `W` nonempty.  Specialize every cross-edge variable to zero
and specialize the internal `W` variables to scalars.  Write `G_d` for the
resulting matching coefficient on `W`.  Then

\[
                  F_c^{(B)}\longmapsto
                  F_{c|U}^{(U)}G_{c|W}.                    \tag{16}
\]

If all three constant scalars `G_(r^W)` are nonzero--equivalently, if this
specialization sends `P_B` to a nonzero multiple of `P_U`--then the mixed
ideal `I_B` does not map into the mixed ideal `I_U`.

**Proof.**  Equation (16) follows because every surviving perfect matching
is the disjoint union of matchings on the two shores.  Choose distinct colors
`r,s`, let `c` be constantly `r` on `U` and constantly `s` on `W`.  It is a
mixed coloring of `B`, but

\[
                         F_c^{(B)}\mapsto G_{s^W}F_{r^U}^{(U)}. \tag{17}
\]

The scalar is nonzero, and the constant coefficient `F_(r^U)` is not in
`I_U`.  This last assertion follows directly from the vertex-color
multigrading: a mixed generator has degree one at some node `(u,a)` with
`a!=r`, which no multiplier of nonnegative degree can remove.  Thus (17) is
not in `I_U`. `QED`

Lemma 3.2 also applies to a proposed disjoint extension/restriction of a
`P^2` certificate.  Color synchronization between the six-site move and the
complement, or genuine cross-edge correction terms, is unavoidable.

## 4. Current uniform conclusion

Theorem 1.2 is a genuine all-even-to-six reduction whenever one can find a
cap with vanishing top higher-cumulant correction (6).  The exact example in
Section 2 shows that such a cap cannot be arbitrary, even for a monochromatic
input.  Lemmas 3.1--3.2 show independently that the successful six-vertex
source-ideal computation is not hereditary by its two most direct local
extensions.

Thus the remaining uniform theorem can be stated sharply: prove that every
hypothetical `q=3,n>=8` realization admits some six-boundary covector `K`
for which `s`, the three `kappa_i`, and (6) have the required values; or find
a different operation that transports the higher boundary cumulants instead
of forcing them to vanish.
