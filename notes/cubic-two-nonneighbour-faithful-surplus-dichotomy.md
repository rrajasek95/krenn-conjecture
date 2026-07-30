# Cubic two-nonneighbour reduction: faithful surplus or a pure crossing

## 1. Outcome

Let \(B\) have even size \(N\ge8\), and suppose

\[
                         H_B(A)=\Delta_{B,3}.                    \tag{1}
\]

Assume that \(p\) is cubic.  After indexing its neighbours by target
colour, cubic rigidity gives distinct sites \(a_0,a_1,a_2\) and nonzero
scalars \(\lambda_c\) such that

\[
 A_{pa_c}=\lambda_c e_c^{(p)}\otimes e_c^{(a_c)},\qquad
 H_{B\setminus\{p,a_c\}}(A)
   =\lambda_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}.           \tag{2}
\]

Choose two distinct sites

\[
 q,q'\in R:=B\setminus\{p,a_0,a_1,a_2\}.                       \tag{3}
\]

For each colour \(c\), put

\[
 L_c=B\setminus\{p,a_c,q,q'\},\qquad P_c=H_{L_c}(A),           \tag{4}
\]

and let \(\Phi_{q,c}\) and \(\Phi_{q',c}\) be the two leave-one-anchor
cofactor maps from
[the cubic nullity-web theorem](cubic-vertex-leave-one-anchor-nullity-web.md).
Write

\[
 \nu_{q,c}=\dim\ker\Phi_{q,c},\qquad
 E_q=\{c:\nu_{q,c}=1\},                                      \tag{5}
\]

and define \(\nu_{q',c}\) and \(E_{q'}\) similarly.

**Theorem 1 (two-nonneighbour dichotomy).**  One of the following exact
alternatives holds.

1. **Faithful surplus.**  There is a colour
   \(c\notin E_q\cup E_{q'}\) for which \(P_c\ne0\).  Both cofactor maps
   then have nullity at least two, and restriction of either kernel to
   the common port space

   \[
                  \bigoplus_{v\in L_c}V_v                       \tag{6}
   \]

   is injective.  Thus two genuine dimension-at-least-two defect spaces
   are faithfully visible on the same exterior star.

2. **Concentrated pure-crossing boundary.**  The nonzero common cofactors
   are confined to at most two exceptional colours:

   \[
               \{c:P_c\ne0\}\subseteq E_q\cup E_{q'},
               \qquad |E_q\cup E_{q'}|\le2.                     \tag{7}
   \]

   For every colour outside this union, \(P_c=0\), and the full pair of
   physical stars obeys the pure two-crossing Hessian packet

   \[
    \Theta_c(s^q_{d,L_c},s^{q'}_{j,L_c})
       =\delta_{cd}\delta_{cj}\lambda_c^{-1}
          e_c^{\otimes L_c}\qquad(0\le d,j\le2).                \tag{8}
   \]

   Hence eight responses vanish and the ninth is a nonzero decomposable
   tensor.  There is always at least one colour for which (8) holds.

If the exact source is entry-minimal and \(A_{qq'}\ne0\), then at least
one \(P_c\) is nonzero.  In the second alternative this forces

\[
                             \operatorname{rank}A_{qq'}\le2.    \tag{9}
\]

Consequently, in an entry-minimal exact source, every invertible block
between two nonneighbours of the cubic centre lies in the
faithful-surplus alternative.

This is a coordinate-free two-site reduction.  It uses the entire
matching cofactors and the physical endpoint-ordered block; it does not
choose matching monomials or enumerate supports.

## 2. The common surplus colour

The cubic nullity-web theorem says, separately for \(q\) and \(q'\),

\[
 |E_q|\le1,\qquad |E_{q'}|\le1.                                \tag{10}
\]

Indeed all three maps are singular and at least two of the three have
nullity at least two.  Therefore

\[
                 \{0,1,2\}\setminus(E_q\cup E_{q'})\ne\varnothing.
                                                                    \tag{11}
\]

If \(P_c\ne0\) for some colour in (11),
[the local-port classification](cubic-nullity-common-cofactor-zero-boundary.md)
applied on both sides says that restriction of each kernel to (6) is
injective.  Its dimension is unchanged and is at least two.  This is the
first alternative.

If no such colour exists, (7) holds.  For every colour outside the union,
the exact two-deletion gluing equation is

\[
 A_{q\mid q'}(d,j)P_c+
 \Theta_c(s^q_{d,L_c},s^{q'}_{j,L_c})
 =\delta_{cd}\delta_{cj}\lambda_c^{-1}e_c^{\otimes L_c}.       \tag{12}
\]

Putting \(P_c=0\) gives (8).  Notice that on this boundary the automatic
local-port kernels

\[
                  V_{q'}\subseteq\ker\Phi_{q,c},\qquad
                  V_q\subseteq\ker\Phi_{q',c}                  \tag{13}
\]

carry no common-star information.  Equation (8), rather than the raw
nullity in (13), is the surviving datum.

## 3. The faithful residual in quotient form

The first alternative can be compressed without losing any kernel
directions.  Fix its colour \(c\), and define

\[
 \begin{aligned}
 Z_{q,c}&=\operatorname{res}_{L_c}(\ker\Phi_{q,c}),\\
 Z_{q',c}&=\operatorname{res}_{L_c}(\ker\Phi_{q',c}).
 \end{aligned}                                               \tag{14}
\]

Both spaces have dimension at least two.  Since \(P_c\ne0\), every
element \(z\in Z_{q,c}\) has a unique lift
\((\eta_{q,c}(z),z)\in V_{q'}\oplus\bigoplus_{v\in L_c}V_v\)
to \(\ker\Phi_{q,c}\).  The gluing formula gives, for every physical
colour row at \(q'\),

\[
 \Theta_c(z,s^{q'}_{j,L_c})
       =-e_j^*(\eta_{q,c}(z))P_c.                              \tag{15}
\]

There is a symmetric map \(\eta_{q',c}:Z_{q',c}\to V_q\).  Thus all
three Hessian responses of either defect space land in the one line
\(\mathbb CP_c\).  Moreover, modulo that line, (12) becomes

\[
 [\Theta_c(s^q_{d,L_c},s^{q'}_{j,L_c})]
   =\delta_{cd}\delta_{cj}\lambda_c^{-1}
       [e_c^{\otimes L_c}]
       \quad\text{in }
       \left(\bigotimes_{v\in L_c}V_v\right)/\mathbb CP_c.     \tag{16}
\]

So the two large cofactor maps reduce on this chart to two
faithful defect spaces, two boundary-value maps, one common tensor line,
and a quotient response matrix of rank at most one.  Proving that the two
defect spaces meet compatibly, or that (16) supplies a clean cap, is the
remaining faithful-chart gate; neither conclusion follows from dimension
alone.

## 4. Why concentration forces a rank drop

Expand the full cofactor of the block \(qq'\) at the cubic centre:

\[
 H_{B\setminus\{q,q'\}}(A)
   =\sum_{c=0}^2\lambda_c e_c^{(p)}\otimes
        e_c^{(a_c)}\otimes P_c.                                \tag{17}
\]

By
[star irredundancy](fixed-star-common-cofactor-rigidity.md),
at an entry-minimal source a nonzero block has nonzero full cofactor.
The three \(p\)-colours in (17) are independent, so \(A_{qq'}\ne0\)
implies \(P_c\ne0\) for at least one \(c\).

Suppose now that (7) holds.  Every active \(P_c\) is charged to an
exceptional colour on at least one side.  If \(c\in E_q\), the exact
nullity-one classification supplies a wrong colour \(\rho_q(c)\ne c\)
whose entire \(q\)-star row is supported at the deleted anchor \(a_c\).
Since \(q'\ne a_c\),

\[
               (e_{\rho_q(c)}^*\otimes\operatorname{id})
                         A_{q\mid q'}=0.                         \tag{18}
\]

Thus the physical \(qq'\)-block has a zero row.  If instead
\(c\in E_{q'}\), the same argument from the other endpoint gives a zero
column.  In either case its rank is at most two, proving (9).

The conclusion is deliberately a reduction, not a proof of the cubic
branch.  The two remaining coordinate-free gates are now explicit:

1. close the faithful packet (14)--(16) by a common kernel direction or
   an active clean cap; or
2. rule out the decomposable rank-one Hessian packet (8), using its shared
   physical edge system for at least two colours or two overlapping pairs.
