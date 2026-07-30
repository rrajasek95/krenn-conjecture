# Independent audit: pure-binary three-channel common-power guard

## 1. Verdict

**PASS.**  The alternating-cycle matching power, the literal
three-channel factorization, injectivity of both endpoint triples, the
seven-edge common-power guard, the list of exactly five distinguished-edge
terms, and the six-dimensional shore obstruction in
[the primary note](curved-pure-binary-three-channel-response-guard.md) all
check over the site-square-zero algebra.

The accompanying checker also passes:

    curved pure-binary common-power guard: PASS

At the time of this audit the audited files have SHA-256 hashes

    6eab87c822fdde832f35c738aab79bfbc25dce97604241ec6e2fb30408e33b31  notes/curved-pure-binary-three-channel-response-guard.md
    16d18bc8c74ab10f503ace8da95d779405c1fb31b2879f4e3f5871941e7fe942  computations/verify_curved_pure_binary_common_power_guard.py

There is one scope distinction, but no error.  The checker exhausts all
\(3^6=729\) word coefficients of the two matching-power identities.  Its
last assertions only check the support facts used by the shore argument;
they do not construct the \(6\times6\) shore matrix or certify its rank.
The mathematical proof in the note does supply that missing linear-algebra
step, and Section 4 below writes the matrix explicitly.

The contracted positive residual is **false**.  Section 7 gives an exact
five-edge response and six-edge common quadratic with injective endpoint
triples such that

\[
                         r^{[3]}=-X_0,\qquad
                    rq^{[2]}=X_0+X_1+X_2.
\]

Thus the three-channel factorization and the common-power equation remain
insufficient even when imposed simultaneously.  This new guard does not
supply the other eight physical pair rows.

Sections 5--6 also prove two structural reductions.  In particular, the
weighted alternating cycle is not merely incompatible with the one
appended chord: **no arbitrary third-colour extension of that fixed binary
core can remain a three-channel binary-pure response.**  The simultaneous
guard escapes through a unary component with common cofactor holes.

## 2. Divided powers and the literal channel factorization

Work in

\[
 {\cal R}_W=\bigotimes_{x=0}^5(\mathbb C\oplus V_x),
 \qquad V_xV_x=0.
\]

For a quadratic \(f\), the coefficient of a six-site word in \(f^{[3]}\)
is its scalar hafnian.  Each unordered perfect matching occurs once: the
\(3!\) orders in \(f^3\) are removed by the divided power.  Similarly, a
term of \(rq^{[2]}\) is one perfect matching with one distinguished
\(r\)-edge and the other two edges from \(q\), again with no factor \(2\)
or \(3\).

For the definitions in the primary note,

\[
 p_k=u_k+i v_k,\qquad t_k={1\over2}(u_k-i v_k),
\]

commutativity gives

\[
 p_kt_k={1\over2}(u_k^2+v_k^2).
\]

Each \(u_k\) and \(v_k\) is the sum of two ports at distinct sites, so its
square is twice the corresponding physical edge.  Thus the factor
\(1/2\) leaves that edge with coefficient one.  The two cross terms cancel
before the site-square-zero quotient is used.  Hence

\[
 \sum_{k=0}^2p_kt_k=r
\]

literally, not just after taking the third matching power.

The decorated supports of the three \(p_k\)'s are mutually disjoint, and
each is nonempty.  Projection onto one support therefore kills the other
two rows and proves linear independence.  The same argument applies to
the \(t_k\)'s.  No ordinary rank interpretation is being substituted for
the two required injective star maps.

The six supported physical edges form one alternating six-cycle.  It has
only its two alternating perfect matchings, of constant colours zero and
one, so

\[
                         r^{[3]}=X_0+X_1.
\]

## 3. The five distinguished-edge terms

For the seven-edge response \(\widehat r\) and six-edge quadratic
\(\widehat q\), direct enumeration gives exactly the following five
nonzero distinguished-edge terms.  The two \(q\)-edges in a row are an
unordered matching; reversing their display order creates no second term.

\[
\begin{array}{c|c|c|c}
\text{word}&\widehat r\text{-edge}&\widehat q\text{-edges}&\text{weight}\\ \hline
000000&01_0&23_0,45_0&1\\
111111&12_1&50_1,34_1&1\\
120021&50_1&14_2,23_0&1\\
120021&23_0&50_1,14_2&-1\\
222222&02_2&14_2,35_2&1
\end{array}                                                     \tag{A1}
\]

The two middle weights are respectively

\[
 1\cdot1\cdot1=1,
 \qquad
 1\cdot(-1)\cdot1=-1.
\]

They cancel on the sole mixed word \(120021\).  The two negative
colour-one entries of \(\widehat q\) multiply to \(+1\) on \(111111\).
Thus, coefficient by coefficient,

\[
       \widehat r\widehat q^{[2]}=X_0+X_1+X_2.          \tag{A2}
\]

This list is exhaustive.  Equivalently, replaying all 729 words produces
the nonzero coefficient dictionary

\[
 \{000000:1,\ 111111:1,\ 222222:1\}.
\]

The added edge \(02_2\) lies in no perfect matching of the response
support: after deleting sites \(0,2\), site \(1\) is isolated.  Hence the
response cube remains

\[
                      \widehat r^{[3]}=X_0+X_1.         \tag{A3}
\]

No positivity or termwise-vanishing inference occurs in (A1)--(A3).

## 4. Exact six-dimensional shore obstruction

Suppose

\[
                       \widehat r=\sum_{k=0}^2p_kt_k.
\]

For a decorated port \(z\), let

\[
 g_z=(P_z,T_z)\in\mathbb C^6,
 \qquad
 J=\begin{pmatrix}0&I_3\\I_3&0\end{pmatrix}.
\]

For ports at distinct physical sites, their response coefficient is
\(g_zJg_w^{\mathsf T}\).  Order the binary ports on the even and odd
shores by

\[
 E=(x_{0,0},x_{0,1},x_{2,0},x_{2,1},x_{4,0},x_{4,1}),
\]

\[
 O=(x_{1,0},x_{1,1},x_{3,0},x_{3,1},x_{5,0},x_{5,1}).
\]

The cross-shore response matrix is

\[
 C=(g_eJg_o^{\mathsf T})_{e\in E,o\in O}
  =\begin{pmatrix}
 1&0&0&0&0&0\\
 0&0&0&0&0&1\\
 0&0&1&0&0&0\\
 0&1&0&0&0&0\\
 0&0&0&0&1&0\\
 0&0&0&1&0&0
 \end{pmatrix},
 \qquad \det C=1.                                      \tag{A4}
\]

Writing \(G_E,G_O\) for the two \(6\times6\) row matrices gives

\[
                         C=G_EJG_O^{\mathsf T}.
\]

Invertibility of \(C\) forces both \(G_E\) and \(G_O\) to be invertible.
Thus the six odd-shore vectors form a basis of \(\mathbb C^6\).

The port \(z=x_{0,2}\) has zero response against every port in \(O\).
Consequently

\[
                        g_zJG_O^{\mathsf T}=0.
\]

Since both \(J\) and \(G_O\) are invertible, \(g_z=0\).  It then has zero
response against \(x_{2,2}\), contradicting the unit \(02_2\) edge.
This proves that \(\widehat r\) is not a three-channel response.  Neither
endpoint injectivity is needed for the contradiction.

For a general invertible pairing
\(\sum_{ij}K_{ij}p_is_j\), replace the second triple by \(K s\).  This
retains injectivity and reduces to the same \(J\)-Gram calculation, so the
scope asserted in the primary note is exact.

## 5. A common-cofactor-hole selector

The first structural reduction applies beyond the displayed cycle.  Call
a response quadratic \(r\) **colour-diagonal** when its physical cells
join equal endpoint colours only.  Let \(R_c\) be its scalar six-site
matrix on the constant colour \(c\), and let \(Q_c\) be the corresponding
constant-colour scalarization of an arbitrary quadratic \(q\).  Put

\[
 H(Q_c)_{xy}=\operatorname {haf}
      ((Q_c)_{W\setminus\{x,y\}}).
\]

**Proposition 5.1 (common-cofactor-hole selector).**  Suppose

\[
 r^{[3]}=\sum_{a\in C}\mu_aX_a,
 \qquad \varnothing\ne C\subsetneq\{0,1,2\},
 \qquad \mu_a\ne0,
                                                               \tag{A5}
\]

and \(rq^{[2]}\) is pure.  If \(d\notin C\) and

\[
                       [rq^{[2]}]_{d^6}\ne0,            \tag{A6}
\]

then there is an edge \(e=\{x,y\}\) such that

\[
 R_d(e)H(Q_d)_e\ne0                                   \tag{A7}
\]

and simultaneously

\[
 \operatorname {haf}(R_a|_{W\setminus e})=0
                     \qquad(a\in C).                  \tag{A8}
\]

In words, a missing colour with nonzero common-power response must use an
edge which is a cofactor hole of every surviving pure colour.

**Proof.**  The constant-\(d\) coefficient is

\[
 [rq^{[2]}]_{d^6}
   =\sum_eR_d(e)H(Q_d)_e.
\]

Its nonvanishing selects an \(e\) satisfying (A7).  Fix \(a\in C\), and
give the endpoints of \(e\) colour \(d\) and the other four sites colour
\(a\).  Because \(r\) is colour-diagonal, the two \(d\)-sites must be
paired to one another in every contributing response matching.  The word
coefficient of \(r^{[3]}\) is therefore exactly

\[
                R_d(e)\operatorname {haf}(R_a|_{W\setminus e}).
\]

It is a mixed coefficient and hence is zero by (A5).  Equation (A7)
includes \(R_d(e)\ne0\), proving (A8).  \(\square\)

Consequently a colour-diagonal response for which even one active slice
has all fifteen four-site cofactors nonzero cannot have a nonzero
common-power coefficient in a missing colour.  In the binary case, the
selected missing-colour edge must lie in the intersection of the two
active cofactor-hole graphs.

The chord \(02_2\) in the primary guard is exactly such an edge.  Deleting
\(0,2\) destroys both alternating pure matchings, so \(02\) is a common
cofactor hole of the colour-zero and colour-one slices.  Proposition 5.1
thus explains structurally why the arbitrary tangent guard has to place
its third-colour response there.  Section 4 explains why the latent
six-dimensional channel space nevertheless forbids that placement.

## 6. A latent-channel saturation theorem for the entire cycle fibre

The shore obstruction is stronger than the single dark-chord argument.
It survives arbitrary cells involving the third colour and derives their
darkness from the mixed cube equations.

**Theorem 6.1 (no third-colour extension of a weighted alternating
cycle).**  Let \(r\) be a quadratic admitting a three-channel
factorization

\[
                         r=\sum_{k=0}^2p_kt_k.          \tag{A9}
\]

Assume that the restriction of its physical cells to endpoint colours
\(\{0,1\}\) consists exactly of

\[
\begin{array}{c|ccc}
\text{colour }0&01:a_0&23:a_1&45:a_2\\
\text{colour }1&12:b_0&34:b_1&50:b_2,
\end{array}                                             \tag{A10}
\]

where all six weights are nonzero.  Cells having at least one endpoint of
colour \(2\) are otherwise arbitrary.  If every mixed coefficient of
\(r^{[3]}\) vanishes, then every port vector of colour \(2\) is zero in
the factorization (A9).  In particular every physical cell incident with
colour \(2\) is zero and

\[
                         [rq^{[2]}]_{2^6}=0             \tag{A11}
\]

for every quadratic \(q\).

**Proof.**  Use the vectors \(g_z\) and form \(J\) as in Section 4.  The
weighted version of (A4) is a permutation matrix with determinant

\[
                   \pm a_0a_1a_2b_0b_1b_2\ne0.         \tag{A12}
\]

Hence the six binary port vectors on either shore form a basis of the
six-dimensional latent space.

It remains to show that a colour-two port is dark against the opposite
binary shore; this is now a consequence, rather than an assumption.  For
\(z=x_{0,2}\), the following six mixed words isolate the indicated edge
coefficient.  Each displayed multiplier is a product of two nonzero cycle
weights.

\[
\begin{array}{c|c}
\text{word coefficient}&\text{isolated value}\\ \hline
[r^{[3]}]_{200000}&r_{01}(2,0)a_1a_2\\
[r^{[3]}]_{210000}&r_{01}(2,1)a_1a_2\\
[r^{[3]}]_{211000}&r_{03}(2,0)b_0a_2\\
[r^{[3]}]_{211100}&r_{03}(2,1)b_0a_2\\
[r^{[3]}]_{211110}&r_{05}(2,0)b_0b_1\\
[r^{[3]}]_{211111}&r_{05}(2,1)b_0b_1.
\end{array}                                             \tag{A13}
\]

For example, after selecting the \(03\) edge in the third row, the only
remaining binary matching is \(12_1\mid45_0\).  The other rows are the
same alternating-path argument.  Because (A10) lists every binary cell,
there is no second matching term hidden in any row of (A13).

All six words are mixed, so their coefficients vanish.  Thus \(g_{0,2}\)
is \(J\)-orthogonal to the six binary port vectors on the odd shore.
Those vectors form a basis, and \(J\) is nondegenerate, hence
\(g_{0,2}=0\).

Rotation by two sites and the reflection \(x\mapsto1-x\pmod6\) preserve
the two coloured one-factors in (A10).  They transport (A13) to every
site.  Therefore \(g_{x,2}=0\) for all \(x\), proving (A11).  \(\square\)

The theorem is exact and nonlinear.  It does not merely say that a dark
chord cannot be appended, and it does not assume that initially unknown
third-colour cross cells vanish.  Six selector words per site force those
cross cells to vanish; shore saturation then kills the latent port itself.
Endpoint injectivity is again unnecessary.

Thus a simultaneous binary-pure three-channel/common-power counterguard
cannot be an extension of the support-minimal alternating cycle.  It must
use at least one additional active-palette cell (with cancellation), or
use response cells joining different colours, so that the isolations in
(A13) no longer apply.

## 7. Exact simultaneous unary counterguard

Define the response

\[
\begin{aligned}
r={}&x_{0,0}x_{4,0}+x_{1,0}x_{3,0}-x_{2,0}x_{5,0}\\
   &+x_{0,1}x_{1,1}+x_{0,2}x_{2,2},                  \tag{A14}
\end{aligned}
\]

and the common quadratic

\[
\begin{aligned}
q={}&x_{0,0}x_{4,0}+x_{2,0}x_{5,0}\\
   &+x_{2,1}x_{4,1}+x_{3,1}x_{5,1}\\
   &+x_{1,2}x_{3,2}+x_{4,2}x_{5,2}.                  \tag{A15}
\end{aligned}
\]

All coefficients belong to \(\{0,\pm1\}\).

### 7.1 Literal three-channel factorization

Put

\[
\begin{array}{lll}
u_0=x_{0,0}+x_{4,0},&&v_0=x_{0,1}+x_{1,1},\\
u_1=x_{1,0}+x_{3,0},&&v_1=x_{0,2}+x_{2,2},
\end{array}                                             \tag{A16}
\]

and set

\[
\begin{array}{lll}
p_0=u_0+i v_0,&&t_0={1\over2}(u_0-i v_0),\\
p_1=u_1+i v_1,&&t_1={1\over2}(u_1-i v_1),\\
p_2=x_{2,0},&&t_2=-x_{5,0}.
\end{array}                                             \tag{A17}
\]

As in Section 2,

\[
 p_0t_0=x_{0,0}x_{4,0}+x_{0,1}x_{1,1},
\]

\[
 p_1t_1=x_{1,0}x_{3,0}+x_{0,2}x_{2,2},
\qquad
 p_2t_2=-x_{2,0}x_{5,0}.
\]

Therefore

\[
                              r=\sum_{k=0}^2p_kt_k.     \tag{A18}
\]

The decorated supports of \(p_0,p_1,p_2\) are pairwise disjoint and
nonempty; the same is true of \(t_0,t_1,t_2\).  Both endpoint triples are
therefore injective.

### 7.2 Unary response cube

The three colour-zero edges \(04,13,25\) form one perfect matching, with
weight \(1\cdot1\cdot(-1)=-1\).  An \(01_1\) response edge leaves only
\(25_0\) available on the other four sites, and an \(02_2\) response edge
leaves only \(13_0\).  The two extra edges cannot occur together because
both use site \(0\).  Hence there is exactly one response perfect matching
and

\[
                              r^{[3]}=-X_0.             \tag{A19}
\]

### 7.3 Exact common-power identity

There are exactly five distinguished-edge terms in \(rq^{[2]}\):

\[
\begin{array}{c|c|c|c}
\text{word}&r\text{-edge}&q\text{-edges}&\text{weight}\\ \hline
000000&13_0&04_0,25_0&1\\
020200&04_0&13_2,25_0&1\\
020200&25_0&04_0,13_2&-1\\
111111&01_1&24_1,35_1&1\\
222222&02_2&13_2,45_2&1.
\end{array}                                             \tag{A20}
\]

The two mixed terms cancel.  Thus

\[
                         rq^{[2]}=X_0+X_1+X_2.          \tag{A21}
\]

An exact replay of all 729 words gives

\[
\operatorname {supp}(r^{[3]})=\{000000:-1\},
\]

\[
\operatorname {supp}(rq^{[2]})
  =\{000000:1,\ 111111:1,\ 222222:1\}.
\]

The exact 729-word replay can be run from the repository root as follows:

    from itertools import product
    from computations.verify_curved_pure_binary_common_power_guard import (
        cube_coefficient, tangent_coefficient,
    )

    R = {
        (0, 4, 0): 1, (1, 3, 0): 1, (2, 5, 0): -1,
        (0, 1, 1): 1, (0, 2, 2): 1,
    }
    Q = {
        (0, 4, 0): 1, (2, 5, 0): 1,
        (2, 4, 1): 1, (3, 5, 1): 1,
        (1, 3, 2): 1, (4, 5, 2): 1,
    }
    cube = {}
    tangent = {}
    for word in product(range(3), repeat=6):
        if value := cube_coefficient(R, word):
            cube[word] = value
        if value := tangent_coefficient(R, Q, word):
            tangent[word] = value
    assert cube == {(0, 0, 0, 0, 0, 0): -1}
    assert tangent == {
        (0, 0, 0, 0, 0, 0): 1,
        (1, 1, 1, 1, 1, 1): 1,
        (2, 2, 2, 2, 2, 2): 1,
    }

This is a simultaneous counterguard to every theorem using only
three-channel factorization, endpoint injectivity, unary/binary purity of
\(r^{[3]}\), and the ternary common-power equation.  Proposition 5.1
locates its mechanism: the missing-colour response edges \(01_1\) and
\(02_2\) are cofactor holes of the active matching \(04_0|13_0|25_0\).
The mixed cancellation in (A20) then pays the remaining cross-word
condition.

The data do **not** supply a direct block \(a\) or the other eight physical
pair equations.  Accordingly they do not give an eight-site source and do
not refute the full-nine residual.

In fact, the displayed factorization has an immediate exact full-row
failure.  Put

\[
 Y=x_{0,0}x_{1,2}x_{2,0}x_{3,2}x_{4,0}x_{5,0}.
\]

Direct matching expansion gives

\[
                         q^{[3]}=Y,\qquad
                    p_0t_0q^{[2]}=Y+X_1.
\]

Thus no scalar \(a_{00}\) can make
\(a_{00}q^{[3]}+p_0t_0q^{[2]}=X_0\): its \(X_1\)-coefficient is always
one.  This proves that the natural \(K=I\) rectangle attached to (A17)
does not extend the guard.  It does not exclude a different set of stars
or a different full-nine realization of the same contracted response.

## 8. Exact remaining full-nine lemma

For the complete physical packet, write the nine wordwise rows as

\[
 P_\omega^{\mathsf T}H(Q_\omega)S_\omega
     =D_\omega-\operatorname {haf}(Q_\omega)a,          \tag{A22}
\]

and let \(K_*\) be the invertible scalar-zero contraction.  The smallest
remaining positive statement is now necessarily a full-nine theorem.

> **Missing-colour full-nine response/cohafnian lemma.**  Under one shared
> global \(q,P,S,a\) satisfying (A22) for every word, assume both endpoint
> stars are injective and
> \(r=\sum_{ij}(K_*)_{ij}p_is_j\) has no mixed top coefficient.  If
> \([r^{[3]}]_{d^6}=0\), then
>
> \[
> \sum_{x<y}(R_{d^6})_{xy}H(Q_{d^6})_{xy}=0.           \tag{A23}
> \]

The complete pair rows give the left side of (A23) as the nonzero diagonal
entry \((K_*)_{dd}\) (equal to \(-\alpha\) in the canonical off-diagonal
cap).  Hence (A23) would exclude a unary or binary pure response.  It is
deliberately a cross-word, full-rectangle statement: at one constant word,
a zero hafnian and a nonzero directional derivative are compatible for
arbitrary scalar matrices, and Section 7 proves that even all contracted
word equations plus the three-channel factorization are compatible.

Theorem 6.1 proves (A23) on the alternating-cycle fibre before the other
eight rows are used.  Proposition 5.1 explains the common-hole mechanism
of the simultaneous guard.  The smallest precise gap left by this audit is
therefore to use the uncontracted entries of (A22) to forbid that mechanism,
not to seek a theorem from the contracted response and common power alone.
