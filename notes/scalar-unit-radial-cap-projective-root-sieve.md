# A projective root sieve closes every visible two-parameter radial cap family

## 1. Outcome

Fix a good physical pair \(p,q\) in an exact ternary aggregate source and
leave the residual site set \(U\), where \(|U|=2h\) and \(h\geq3\).
Suppose the direct block is the intrinsic scalar unit

\[
                         A_{pq}=\alpha E_{aa},\qquad \alpha\ne0.       \tag{1}
\]

Write \(q\) for the residual internal quadratic, write
\(R_{ij}=p_i s_j\) for the nine endpoint-ordered aggregate response
quadratics, and identify a cap covector
\(K\in(V_p\otimes V_q)^*\) with its matrix in the fixed target-colour
bases.  Put

\[
 r(K)=\sum_{i,j}K_{ij}R_{ij},\qquad
 s(K)=\alpha K_{aa},\qquad
 T(K)=\sum_iK_{ii}X_i,                                      \tag{2}
\]

where \(X_0,X_1,X_2\) are the three linearly independent constant-colour
words on \(U\), and retain the literal contracted row

\[
                 s(K)q^{[h]}+r(K)q^{[h-1]}=T(K).             \tag{3}
\]

The exact descent target calls a cap active when
\(s(K)K_{00}K_{11}K_{22}\ne0\).  Since
\(s(K)=\alpha K_{aa}\) and \(\alpha\ne0\), this is equivalent to

\[
                         K_{00}K_{11}K_{22}\ne0.             \tag{4}
\]

The homogeneous, denominator-cleared clean error from that same target is

\[
 {\cal E}(K)=(s(K)q+r(K))^{[h]}-s(K)^{h-1}T(K).             \tag{5}
\]

It scales by the \(h\)-th power under rescaling of \(K\), so both activity
and cleanliness are projective conditions.  No affine normalization
\(s=1\) has been imposed.

This note isolates a linear family on which (5) becomes a one-variable
scalar equation.  Let

\[
 {\cal L}=\{K:r(K)\in\mathbb Cq\}.                         \tag{6}
\]

The complementary diagonal labels are denoted by \(b,c\).  Since
\(q\ne0\), there is a unique linear functional \(\beta:{\cal L}\to
\mathbb C\) such that

\[
                         r(K)=\beta(K)q.                     \tag{7}
\]

Here \(q\ne0\) is forced by (3): if \(q=0\), then, since \(h\ge3\), the
complementary diagonal row \(K=E_{bb}\) would read \(0=X_b\), impossible
for the nonzero constant-colour word.  Thus \(\beta\) really is uniquely
defined; no choice of a coefficient of a zero quadratic is involved.

The main result is the following projective sieve.

**Theorem 1.1 (radial-cap root sieve).**  Assume \(h\ge3\).  If

1. the two linear forms \(s,\beta\) on \({\cal L}\) are independent; and
2. neither \(K_{bb}\) nor \(K_{cc}\) vanishes identically on
   \({\cal L}\),

then \({\cal L}\) contains an active clean cap.  Therefore the exact
clean-pair theorem gives the order descent \(N=2h+2\mapsto N-2\).

Equivalently, in the no-clean-cap branch at \(h\ge3\), the radial locus
has one of only two structural defects:

\[
 \boxed{\operatorname {rank}(s,\beta)\le1}
 \quad\text{or}\quad
 \boxed{{\cal L}\subseteq\{K_{ii}=0\}
        \text{ for some }i\in\{b,c\}.}                    \tag{8}
\]

In the first box, if \(s\) is nonzero on \({\cal L}\), then
\(\beta=ts\) for one fixed scalar \(t\), so every radial cap with
\(s(K)\ne0\) has that projective response ratio.  If \(s\) vanishes
identically, the radial family is entirely scalar-zero instead.  The
second box is not merely an activity failure: it supplies a linear
functional on the response space modulo \(\mathbb Cq\) which selects the
pure diagonal response \(R_{ii}\) and kills the other eight response
columns.

There is a companion response-free dichotomy valid for every \(h\ge3\).
If \(\ker r\) contains no active cap, then for some label \(i\) there is a
linear functional \(\lambda\) on \(\operatorname {im}r\) with

\[
                         \lambda(R_{jk})=\delta_{ij}\delta_{ik}.       \tag{9}
\]

Thus the easy response-free descent either occurs, or one literal pure
response column is linearly separable from all the others.  Formula (9) is
only a linear dual on the evaluated degree-two response span.  It need not
be a restriction or polarization of any operation on the endpoint stars.
Even an arbitrarily chosen extension to the ambient quadratic space gives
no identity such as
\(\lambda(R_{jk}q^{[h-1]})=\lambda(R_{jk})q^{[h-1]}\).
Turning it into a physical higher-cut coefficient operation still requires
source provenance; this note does not extend \(\lambda\) through a
matching power.

The theorem eliminates a broad radial family without carrier cancellation,
path integration, or a case enumeration.  It does not prove that the
radial locus satisfies the two hypotheses, and hence does not resolve the
intrinsic scalar-unit branch by itself.

## 2. The radial error has one scalar polynomial factor

Suppose \(K\in{\cal L}\) and \(s(K)\ne0\).  Put

\[
                         t={\beta(K)\over s(K)}.             \tag{10}
\]

Then (3) and divided-power multiplication give

\[
 \begin{aligned}
 T(K)&=s(K)(1+ht)q^{[h]},\\
 s(K)q+r(K)&=s(K)(1+t)q.
 \end{aligned}                                             \tag{11}
\]

Consequently

\[
 \boxed{{\cal E}(K)=s(K)^hP_h(t)q^{[h]},\qquad
        P_h(t)=(1+t)^h-1-ht.}                              \tag{12}
\]

This can also be read directly from the target-free error

\[
 {\cal E}(K)=\sum_{j=2}^h
       s(K)^{h-j}q^{[h-j]}r(K)^{[j]}.                       \tag{13}
\]

Indeed
\(q^{[h-j]}q^{[j]}={h\choose j}q^{[h]}\), so (13) has scalar
coefficient \(\sum_{j=2}^h{h\choose j}t^j=P_h(t)\).

The root structure is uniform.  Since the coefficients of \(t^0,t^1\)
vanish and the coefficient of \(t^2\) is \({h\choose2}\ne0\), the origin
is an exact double root.  The remaining \(h-2\) roots are nonzero and
simple.  To see the last claim,
suppose \(t\ne0\) is a common root of \(P_h\) and its derivative.  With
\(\zeta=1+t\), one has

\[
 \zeta^{h-1}=1,qquad \zeta^h=1+h(\zeta-1).              \tag{14}
\]

The first equality changes the second into

\[
                    \zeta=1+h\zeta-h,
 \qquad (h-1)(\zeta-1)=0,                                \tag{15}
\]

so \(\zeta=1\) in characteristic zero, contrary to \(t\ne0\).
Thus \(P_h\) has exactly \(h-2\) distinct nonzero roots over
\(\mathbb C\).  Together with the double root at the origin, its set of
**distinct** roots has cardinality \(h-1\).  Every one is a guaranteed
clean ratio by (12).  If \(q^{[h]}\ne0\), these are precisely the clean
ratios on the chart \(s\ne0\); if \(q^{[h]}=0\), every radial ratio is
clean instead.

Neither possible scalar degeneration is hidden among these roots:

\[
             P_h(-1)=h-1\ne0,
 \qquad P_h(-1/h)=(1-1/h)^h\ne0.                           \tag{15a}
\]

Thus every selected root has both \(1+t\ne0\) and \(1+ht\ne0\).  In
particular the effective radial quadratic in (11) is not zero and its
literal target row is not made zero by its scalar coefficient.  The sieve
never cancels \(q^{[h]}\); its possible vanishing only strengthens the
cleanliness conclusion just noted.

There is no omitted active scalar-degenerate case.  At \(t=-1/h\), (11)
would give \(T(K)=0\), incompatible with three nonzero diagonal
coefficients of the independent \(X_i\).  At \(t=-1\), cleanliness would
force \(q^{[h]}=0\) by (12), and then (11) again gives \(T(K)=0\).
Thus \(1+t=0\) cannot hide an active clean cap outside the root sieve.

The special ratio \(t=0\) is already useful: every response-free active
cap is clean.  This conclusion uses (3) and (5), not cancellation of
\(q^{[h]}\).

## 3. The projective boundary count

For any root \(t\) of \(P_h\), including \(t=0\), set

\[
                         H_t=\ker(\beta-ts)\subseteq{\cal L}.          \tag{16}
\]

Independence of \(s,\beta\) makes \(H_t\) a nonzero hyperplane.  The
selected diagonal functional is \(K_{aa}=s(K)/\alpha\).  It cannot vanish
identically on \(H_t\): otherwise \(s\) would be proportional to
\(\beta-ts\), forcing \(\beta\) to be proportional to \(s\).

Now fix \(i=b\) or \(c\).  By hypothesis the functional
\(d_i(K)=K_{ii}\) is nonzero on \({\cal L}\).  It vanishes identically on
\(H_t\) exactly when

\[
                         d_i\in\mathbb C(\beta-ts).        \tag{17}
\]

As \(t\) varies, the right side traces distinct points of the projective
line \(\mathbb P\langle s,\beta\rangle\).  Hence a fixed \(d_i\) can
block at most one value of \(t\).  The two complementary diagonals block
at most two roots in total.

When \(h\ge4\), Section 2 supplies at least three distinct roots.
Choose an unblocked one.  None of the three diagonal functionals vanishes
identically on its \(H_t\).  Over the infinite field \(\mathbb C\), a
finite union of their three kernels cannot cover \(H_t\).  Some
\(K\in H_t\) therefore has all three diagonal entries nonzero.  Equations
(10), (12), and (16) make it an active clean cap, proving Theorem 1.1.

At \(h=3\) the two distinct polynomial roots are \(0\) and \(-3\).  The two
complementary coordinate boundaries can hide both, so projective counting
alone stops.  Exact target compatibility rules out that last pattern.
Indeed, on each \(H_t\), absence of an active point says that the vector
space \(H_t\) is covered by the three restricted diagonal kernels.  The
selected kernel is proper by the preceding argument, so the finite-union
lemma forces \(H_t\) into the kernel of \(d_b\) or \(d_c\).  Each of these
two nonzero functionals blocks at most one root.  Consequently both block,
and they block different roots.  After swapping \(b,c\),

\[
                    K_{bb}=\mu_b\beta(K),\qquad
                    K_{cc}=\mu_c(\beta(K)+3s(K))           \tag{17a}
\]

on \({\cal L}\), with \(\mu_b,\mu_c\ne0\).  The restrictions of \(s\) to
both hyperplanes are nonzero.  Choose \(K_0\in H_0\) with \(s(K_0)\ne0\)
and \(K_1\in H_{-3}\) with \(s(K_1)\ne0\).  Formula (17a) then forces

\[
 \begin{array}{c|ccc}
       &K_{aa}/s&K_{bb}/s&K_{cc}/s\\ \hline
 K_0   &\alpha^{-1}&0&3\mu_c\\
 K_1   &\alpha^{-1}&-3\mu_b&0 .
 \end{array}                                               \tag{17b}
\]

Thus the required remaining entries are automatically nonzero; no generic
choice inside either hyperplane is being assumed.  Applying the literal
row (3), with \(q q^{[2]}=3q^{[3]}\), gives two equations for the same
global element \(Q=q^{[3]}\):

\[
 \begin{aligned}
 Q&=\alpha^{-1}X_a+3\mu_cX_c,\\
 -8Q&=\alpha^{-1}X_a-3\mu_bX_b.                          \tag{17c}
\end{aligned}
\]

Eliminating the shared \(Q\) gives

\[
             9\alpha^{-1}X_a-3\mu_bX_b+24\mu_cX_c=0.       \tag{17d}
\]

The three constant words are linearly independent over \(\mathbb C\), and
all three displayed coefficients are nonzero.  Hence (17d) is impossible,
including with arbitrary complex phases or cancellation.  It also shows
directly that \(Q=0\) cannot rescue the hidden-boundary pattern.  This
closes \(h=3\) and completes the proof of Theorem 1.1 at every allowed
order.

## 4. Boundary trapping gives a quotient response selector

Let

\[
 \bar r:\operatorname {Mat}_3\longrightarrow
          {\operatorname {im}r+\mathbb Cq\over\mathbb Cq},
 \qquad K\longmapsto[r(K)].                               \tag{18}
\]

Its kernel is exactly \({\cal L}\).  If
\({\cal L}\subseteq\{K_{ii}=0\}\), then the coordinate functional
\(d_i(K)=K_{ii}\) vanishes on \(\ker\bar r\).  It therefore factors
through \(\bar r\): there is a linear functional \(\bar\lambda_i\) on
\(\operatorname {im}\bar r\) such that

\[
              \bar\lambda_i([R_{jk}])
                         =\delta_{ij}\delta_{ik}.          \tag{19}

\]

Indeed \(\bar r(E_{jk})=[R_{jk}]\), while
\(d_i(E_{jk})=\delta_{ij}\delta_{ik}\); no choice of representatives is
being made in (19).

Equivalently, pulling \(\bar\lambda_i\) back along the quotient map gives
a functional \(\widetilde\lambda_i\) on
\(\operatorname {im}r+\mathbb Cq\) satisfying

\[
 \widetilde\lambda_i(q)=0,
 \qquad \widetilde\lambda_i(R_{jk})=\delta_{ij}\delta_{ik}. \tag{19a}
\]

This proves the selector assertion following (8).  The condition on \(q\)
is essential: an ordinary selector through \(r\) need not factor through
\(\bar r\).  Equations (19)--(19a) are exact finite-dimensional quotient
statements, not permission to apply a quadratic functional to an unmarked
factor of \(R_{jk}q^{[h-1]}\).

The response-free version is identical without quotienting.  If
\(\ker r\) has no active matrix, then every element of this linear space
lies in one of the three diagonal hyperplanes.  A vector space over an
infinite field cannot be a finite union of proper linear subspaces, so

\[
                         \ker r\subseteq\{K_{ii}=0\}       \tag{20}

\]

for some \(i\).  Hence \(d_i\) factors through \(r\), giving a functional
\(\lambda\) with (9).  This response-free \(\lambda\) is not required to
annihilate \(q\); that extra constraint belongs only to the quotient
selector (19a).  Here (9) follows from the same literal identities
\(r(E_{jk})=R_{jk}\) and \(d_i(E_{jk})=\delta_{ij}\delta_{ik}\).

These selectors identify the exact residue left by failure of the easy
cap argument.  A positive continuation must realize one of them by a
source-faithful polarization, physical coefficient restriction, or
filtered comparison.  Arbitrary linear extension through the evaluated
site algebra would repeat the carrier-cancellation error ruled out by the
existing torsion guards.

## 5. Scope and exact audit

The argument is linear over \(\mathbb C\), takes place in the full physical
cap-covector space, retains the endpoint order in the nine
\(R_{ij}=p_i s_j\), and uses only aggregate source identities.  It permits
zero blocks, parallel decorated sources, and arbitrary complex
cancellation.  No individual matching summand or source coefficient is
selected.  Only the active clean \(K\) is fed to the exact descent theorem;
the auxiliary boundary covectors in the \(h=3\) contradiction need not be
active.

The dependency-free checker
[`verify_scalar_unit_radial_cap_projective_root_sieve.py`](../computations/verify_scalar_unit_radial_cap_projective_root_sieve.py)
audits the divided-power collapse, the nonzero simple-root count, the
two-boundary projective sieve, the shared-target \(h=3\) obstruction, and
the distinct response-free and mod-\(\mathbb Cq\) selector
factorizations.  It includes dependency-free adversarial mutations.  The
finite checks guard constants and signs; Sections 2--4 are the uniform
proof.

This is a research reduction, not a certified-spine supersession and not a
proof of Krenn's conjecture.
