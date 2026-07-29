# Physical Plücker rectangles give a second-order E2 closure

## 1. Outcome

The literal source products contain one compatibility which is not visible
in the response-transition law alone.  If

\[
                         Z_{cd}=p_cs_d,
\]

then every two-by-two minor of the product table vanishes before applying
any common power:

\[
                         Z_{ab}Z_{cd}=Z_{ad}Z_{cb}.       \tag{1}
\]

When two entries in one row are E2 gauges, (1) produces a canonical
quadratic Hessian annihilator.  On a gauge-rigid chart the annihilator is
again an E2 response.  Thus a dense defect-three response space is not
merely spanned by the six physical products: it is closed under six
explicit first-order operations involving the diagonal products.

This is a genuine extra constraint beyond the exact transition equations.
Those equations are response-wise: once one literal equality
`p_c s_d=Gamma_q(alpha_cd)` holds, all of its third-site transition rows
follow without referring to any other colour pair.  They cannot by
themselves put two further defect directions in the plane bundle of one
selected response.

Section 4 gives an exact twelve-site guard.  All six star rows have support
three, the defect has dimension three, the six off-diagonal products span
it, every off-diagonal pair equation and every transition equation carried
by those six responses (the 18 unequal-endpoint triple rows) is literal,
and one response factors globally through planes which miss the other two
directions.  The guard is not gauge-rigid.  Its failure is explained by
one displayed Plücker annihilator, nonzero on a block where
`q` is zero.  Hence it is an explicit extra Hessian class rather than a
numerical rank accident.

The resulting conditional frontier is sharp:

\[
 \boxed{\text{transition flatness alone does not propagate the planes;}\quad
 \text{gauge rigidity adds differential Plücker closure.}}       \tag{2}
\]

It remains to prove that a three-dimensional physical response space with
this closure lies in the selected plane bundle, or that failure exports a
clean cap.  The separated support pattern below cannot survive that step.

## 2. Gauge integration by parts

Let `W` have `2t` sites and work in its site-square-zero algebra.  For a
site weight `alpha`, let

\[
 (D_\alpha R)_{ij}=(\alpha_i+\alpha_j)R_{ij},\qquad
 \Gamma_q(\alpha)=D_\alpha q,\qquad
 \sigma(\alpha)=\sum_i\alpha_i.                         \tag{3}
\]

Define the first-order operator on quadratics

\[
                         K_\alpha(R)=
             \sigma(\alpha)R-D_\alpha R.               \tag{4}
\]

**Lemma 2.1 (gauge integration by parts).**  For every quadratic `R`,

\[
 K_\alpha(R)q^{[t-1]}
       =\Gamma_q(\alpha)R q^{[t-2]}.                    \tag{5}
\]

**Proof.**  Apply the site-scaling derivation `D_alpha` to
`R q^[t-1]`.  Every full-site monomial has weight `sigma(alpha)`, while

\[
 D_\alpha(q^{[t-1]})=\Gamma_q(\alpha)q^{[t-2]}.
\]

Moving `(D_alpha R)q^[t-1]` to the other side gives (5).  Divided powers
remove every binomial coefficient.  \(\square\)

## 3. Differential Plücker closure on a gauge-rigid chart

Assume the exact pair equations

\[
 a_{cd}q^{[t]}+Z_{cd}q^{[t-1]}=\delta_{cd}X_c,
 \qquad Z_{cd}=p_cs_d.                                  \tag{6}
\]

For `c!=d` on the E2 branch, write

\[
                         Z_{cd}=\Gamma_q(\alpha_{cd}),
 \qquad \sigma(\alpha_{cd})=-a_{cd}.                   \tag{7}
\]

**Theorem 3.1 (Plücker-Hessian annihilators).**  Suppose `a,b,d` are
pairwise distinct.  Then

\[
\begin{aligned}
 N^{(b)}_{a;b,d}
   &=K_{\alpha_{ab}}(Z_{bd})-K_{\alpha_{ad}}(Z_{bb}),\\
 N^{(d)}_{a;b,d}
   &=K_{\alpha_{ab}}(Z_{dd})-K_{\alpha_{ad}}(Z_{db})
\end{aligned}                                                   \tag{8}
\]

belong to `ker(R -> R q^[t-1])`.

If the chart is gauge-rigid, each tensor in (8) belongs in fact to

\[
                         \Gamma_q(D),\qquad
 D=\ker B_3(q).                                        \tag{9}
\]

In particular, when `dim D=3` and the six off-diagonal primitives span
`D`, every tensor in (8) is a scalar combination of the six physical
off-diagonal products.

**Proof.**  The two relevant literal minors are

\[
 Z_{ab}Z_{bd}=Z_{ad}Z_{bb},\qquad
 Z_{ab}Z_{dd}=Z_{ad}Z_{db}.                             \tag{10}
\]

Apply (5) to the two sides of each equality, using (7) for the first
factor.  This proves that (8) is killed by `q^[t-1]`.

Under gauge rigidity, write `N=Gamma_q(gamma)` with `sum gamma=0`.
On a rank-three edge every off-diagonal product in (6) vanishes.  In each
line of (8), the only possibly nonzero block is therefore a scalar
multiple of one diagonal product, and has rank at most two.  Equality
with `(gamma_i+gamma_j)q_ij`, where `q_ij` has rank three, forces
`gamma_i+gamma_j=0`.  Hence `gamma in D`, proving (9).  \(\square\)

Theorem 3.1 is the first source-level coupling between different E2
directions which is not a tautological transition cancellation.  It also
uses exactly the data omitted by the 24 target-zero triple rows: the
diagonal products `Z_bb,Z_dd`.

## 4. A dense physical transition guard

Let

\[
 W=P_0\sqcup P_1\sqcup P_2\sqcup\{m_0,m_1,m_2\},
 \qquad |P_c|=3.                                       \tag{11}
\]

Every local space is `C^3` with its displayed target basis.  Define the
linear rows

\[
 (x_c)_i=\begin{cases}e_c^{(i)},&i\in P_c,\\0,&i\notin P_c,
             \end{cases}
 \qquad p_c=s_c=x_c.                                   \tag{12}
\]

Thus all six physical rows have site support exactly three.  Define `q`
by the following blocks and set every other block to zero:

\[
 q_{i m_c}=I_3\quad(i\in P_c),\qquad
 q_{ij}=e_c^{(i)}\otimes e_d^{(j)}
       \quad(i\in P_c,j\in P_d,c<d).                  \tag{13}
\]

The rank-three graph is the disjoint union of three claws
`P_c * {m_c}`.  Its defect basis is

\[
 \zeta^c_i=\begin{cases}1,&i\in P_c,\\-1,&i=m_c,\\0,&\text{otherwise}.
              \end{cases}                              \tag{14}
\]

Put

\[
\begin{aligned}
 \alpha^{01}&=(\zeta^0+\zeta^1-\zeta^2)/2,\\
 \alpha^{02}&=(\zeta^0-\zeta^1+\zeta^2)/2,\\
 \alpha^{12}&=(-\zeta^0+\zeta^1+\zeta^2)/2,
\end{aligned}                                                   \tag{15}
\]

and use the same primitive in the reverse orientation.  Direct block
comparison gives

\[
                  x_cx_d=\Gamma_q(\alpha^{cd})\quad(c\ne d).
                                                               \tag{16}
\]

The three displayed primitives are independent and span `D`.  Since each
`zeta^c` has sum two,

\[
                         \sigma(\alpha^{cd})=1.          \tag{17}
\]

Taking every off-diagonal direct entry `a_cd=-1`, equations (16)--(17)
give all six exact source identities

\[
                  -q^{[6]}+p_cs_dq^{[5]}=0.             \tag{18}
\]

The nonzero-block graph is connected and nonbipartite, so the vertex-gauge
map is injective.  It also has a perfect matching after deleting any two
vertices; hence every pair complement is active.  The model is therefore
not exploiting a primitive ambiguity or an inactive pair complement.

Select `Z_01=x_0x_1` and put

\[
                         L_i=\operatorname{span}
                                  \{(x_0)_i,(x_1)_i\}.   \tag{19}
\]

Then `Z_01` factors through `L`, but `L_i=0` on `P_2`, while `Z_02` has
nonzero blocks on `P_0 \times P_2`.  Thus neither `Z_02` nor the full
three-dimensional response space lies in `L_2`.

Adjoin two deleted sites `r,u`, use (12) as their endpoint-oriented star
rows, and take their off-diagonal direct entries to be `-1`.  These are
one set of actual source blocks.  For every third site `v`, restricting
(16) to blocks away from `v`, to blocks incident with `v`, and to the
scalar coordinate gives exactly the three equations of the physical
transition law.  Consequently all 18 target-zero triple rows whose
`r,u` colours are unequal cancel by the near-perfect gauge identity.  The
other six nonconstant rows would use an off-diagonal response in an
adjacent pair chart and are not claimed here.  No response table has been
specified independently.

## 5. The guard's exact extra Hessian class

The Plücker identity

\[
                         Z_{01}Z_{12}=Z_{02}Z_{11}       \tag{20}
\]

produces

\[
                         N=K_{\alpha^{01}}(Z_{12})
                              -K_{\alpha^{02}}(Z_{11}). \tag{21}
\]

Lemma 2.1 and (20) give `N q^[5]=0`.  But for distinct `i,j in P_1`,

\[
                         q_{ij}=0,\qquad
                         N_{ij}=-4e_1^{(i)}e_1^{(j)}\ne0. \tag{22}
\]

Indeed, `Z_11=x_1^2` has block `2e_1e_1`, both endpoint weights of
`alpha^02` are `-1/2`, and `sigma(alpha^02)=1`.  Therefore `N` cannot be
any vertex gauge.  This proves directly that the guard is outside the
gauge-rigid stratum.

The logical message is precise.  Exact off-diagonal identities, dense
rows, defect-three spanning, synchronized factorization of one direction,
pair-complement activity, and every source transition row do not propagate
the plane bundle.  Gauge rigidity rules out this guard through (21)--(22),
and Theorem 3.1 records the additional closure that any surviving
gauge-rigid configuration must obey.

The dependency-free checker
[`verify_plucker_hessian_closure_and_defect_three_transition_guard.py`](../computations/verify_plucker_hessian_closure_and_defect_three_transition_guard.py)
audits (13)--(22), all six primitives and direct balances, all third-site
transition equations, pair-complement activity, the missed plane blocks,
the Plücker identity, and the displayed non-gauge Hessian annihilator.
