# Response Plücker syzygies reach the sharp non-forcing degree

## Outcome

Ordinary rank-one response Plücker identities do not force the simultaneous
Bezout kernel required by \(\operatorname {Tr}_h\). Their full polarization
already contains a sharp counterguard: on the \(q=0\) associated-graded
face, the clean coordinates can be the complete degree-\(h\) Veronese
family

\[
                  g_j=u^{h-j}v^j,\qquad0\le j\le h.      \tag{1}
\]

These forms have the \(h\) adjacent linear syzygies

\[
                  vg_j-ug_{j+1}=0,\qquad0\le j<h,        \tag{2}
\]

and (2) generates their full linear syzygy space. The corresponding
Hilbert--Burch matrix has \(h\) columns, all of degree one, so its total
column degree is exactly \(h\). Its maximal minors are (1), which are
coprime. This is precisely the sharp boundary of the previously isolated
criterion: a common factor is forced only when the total column degree is
strictly below \(h\).

At the first two orders the result is completely explicit.

For \(h=3\),

\[
\begin{array}{c}
u^3,\ u^2v,\ uv^2,\ v^3,\\[2mm]
vu^3-u(u^2v)=0,\quad
v(u^2v)-u(uv^2)=0,\quad
v(uv^2)-uv^3=0.
\end{array}                                               \tag{3}
\]

There are three linear Hilbert--Burch columns, of total degree \(3\);
forcing would require total degree at most \(2\).

For \(h=4\),

\[
              u^4,\ u^3v,\ u^2v^2,\ uv^3,\ v^4          \tag{4}
\]

have four adjacent linear syzygies, of total degree \(4\); forcing would
require at most \(3\).

Thus response Plücker/Bianchi must do more than reproduce the ordinary
rank-one syzygies. A positive proof needs a genuinely new source identity
which lowers the Hilbert--Burch degree by one, or directly proves

\[
                         \bigwedge^h\mathcal M_f=0.       \tag{5}
\]

The most concrete local target remains

\[
 [u^h]\!\left(
   \sum_{j=2}^h\alpha_i^{h-j}
       R_i^{[j]}q_i^{[h-j]}
 \right)=0
 \quad\text{for every clean coordinate }i.               \tag{6}
\]

The tempting shortcut that (6) is merely a nonconstant GHZ target
coefficient is false. The word label may be the same, but the source
grades are different. A mixed target row contains response-count grades
\(j=0,1\); the clean tail in (6) contains \(j=2,\ldots,h\). Setting the GHZ
target coefficient to zero gives the mixed pair equation and is exactly
what removes \(j=0,1\). It does not set the remaining clean error to zero.

An exact \(q=0\) guard makes this distinction literal. Put \(h\) residual
sites on each of two shores and choose rank-one star rows so that

\[
                       R(u,v)=uZ_{01}+vZ_{22}.            \tag{7}
\]

On the mixed residual words \(0^h|1^h\) and \(2^h|0^h\), the two clean
coordinates are

\[
                         h!u^h,\qquad h!v^h.             \tag{8}
\]

Every mixed pair row is zero because \(q^{[h]}=q^{[h-1]}=0\), but (8) is
nonzero. Therefore the complete mixed target rows do not already include
\(\chi_i\). The guard does not satisfy the diagonal GHZ anchors; it refutes
only the simple word-projection identification. Any successful use of the
diagonal anchors must supply a new nonlinear higher-Bianchi/cross-chart
coupling between the disjoint source grades.

## 1. Literal response Plücker provenance

Write

\[
                         Z_{ab}=p_as_b.
\]

Before any matching power is applied, the rank-one response table satisfies

\[
                         Z_{ab}Z_{cd}=Z_{ad}Z_{cb}.       \tag{9}
\]

Choose two response directions \(Z_0,Z_1\) in one physical cap line and
write

\[
                         r(u,v)=uZ_0+vZ_1.               \tag{10}
\]

On \(q=0\), target elimination leaves

\[
                         \mathcal E(u,v)=r(u,v)^{[h]}.   \tag{11}
\]

The decorated response-count-\(j\) coefficient of (11) is

\[
                    Z_0^{[h-j]}Z_1^{[j]}\,u^{h-j}v^j.   \tag{12}
\]

When the decorated products in (12) are nonzero and retained as separate
physical tensor coordinates, the scalar clean-coordinate span contains all
forms in (1). This realization is compatible with (9): the Plücker
relations govern products among the decorations but do not impose a
linear relation among the distinct parameter monomials.

The two-shore construction realizes this without formal independent
response symbols. Let the left-shore components of \(p_0,p_2\) be supported
on local labels \(0,2\), and let the right-shore components of \(s_1,s_2\)
be supported on local labels \(1,0\), respectively. Then

\[
 Z_0=Z_{01}=p_0s_1,\qquad Z_1=Z_{22}=p_2s_2.
\]

On the two words in (8), the response cross matrix is respectively the
all-\(u\) and all-\(v\) \(h\times h\) matrix. Its matching sum is \(h!u^h\)
or \(h!v^h\). Intermediate colour-count words retain the remaining
decorated profiles. All entries still come from the same rank-one star
table and hence obey (9).

## 2. Exact Hilbert--Burch calculation

Order the generators in (1) by increasing \(v\)-degree. Their standard
syzygy matrix is

\[
 H_h=
 \begin{pmatrix}
 v&0&\cdots&0\\
 -u&v&\ddots&\vdots\\
 0&-u&\ddots&0\\
 \vdots&\ddots&\ddots&v\\
 0&\cdots&0&-u
 \end{pmatrix}
 \in\operatorname {Mat}_{h+1,h}(\Bbbk[u,v]).            \tag{13}
\]

Equation (2) says

\[
                 H_h^{\mathsf T}(g_0,\ldots,g_h)^{\mathsf T}=0. \tag{14}
\]

Deleting row \(j\) from (13) gives, up to the harmless cofactor sign,

\[
                              u^{h-j}v^j.                \tag{15}
\]

Thus \(H_h\) has generic rank \(h\), its signed maximal-minor vector is
exactly the clean family, and

\[
             \sum_{\text{columns}}\deg H_{h,\bullet j}=h. \tag{16}
\]

The first and last minors are \(u^h\) and \(v^h\), so their gcd is one.
This proves at once that (13) cannot force a common factor.

It also proves that (2) is the full space of linear syzygies. A general
linear relation has \(2(h+1)\) scalar coefficients and lands in
\(S_{h+1}\), of dimension \(h+2\). The multiplication map is surjective
because the \(u\)- and \(v\)-multiples of (1) contain every monomial of
degree \(h+1\). Hence its kernel has dimension

\[
                         2(h+1)-(h+2)=h,                 \tag{17}
\]

equal to the dimension of the independent adjacent relations.

The clean Macaulay map is also surjective: the forms \(u^h\) and \(v^h\)
alone have \(2h\) disjoint degree-\((h-1)\) shifts spanning
\(S_{2h-1}\). Consequently

\[
                    \ker\mu_{\mathcal E_h}^*=0,          \tag{18}
\]

and no simultaneous Bezout kernel exists.

## 3. Why differential Plücker is not yet the missing syzygy

The committed gauge-rigid response theorem strengthens (9). If
\(Z_{ab}=\Gamma_q(\alpha_{ab})\), gauge integration by parts gives

\[
 K_{\alpha_{ab}}(Z_{bd})
       -K_{\alpha_{ad}}(Z_{bb})
       \in\ker(R\mapsto Rq^{[h-1]}).                    \tag{19}
\]

This is a genuine cross-response Hessian relation. It is not yet a
Hilbert--Burch column for the clean family \(G_h\):

* (19) lives in the quadratic response/gauge module;
* the kernel condition is after multiplication by \(q^{[h-1]}\);
* \(G_h\) begins with two response factors and contains every higher
  response-count grade; and
* no committed polarization sends (19) to one relation among all of the
  same degree-\(h\) clean coordinates while lowering total syzygy degree.

On \(q=0\), (19) loses its gauge content while the Veronese family survives.
Thus any positive differential-Plücker construction must use nonzero
\(q\), the diagonal products, and a higher polarization before taking this
associated graded. Its required leading term must defeat (13), not merely
reproduce one of its columns.

The sharp source target at \(h=3\) is therefore one additional relation
which replaces the three-column degree total in (3) by a full-rank
presentation of total degree at most two, or directly annihilates every
\(3\times3\) residual minor. At \(h=4\), the corresponding threshold is
three. Uniformly it is \(h-1\).

## 4. The nonconstant-word shortcut fails by source grading

Fix a residual physical word \(w\). The pair row at a non-GHZ word is

\[
 \left(sq^{[h]}+rq^{[h-1]}\right)_w=0.                  \tag{20}
\]

The target-eliminated clean coordinate is

\[
\begin{aligned}
 \mathcal E_w
 &=\left((sq+r)^{[h]}-
      s^{h-1}(sq^{[h]}+rq^{[h-1]})\right)_w\\
 &=\left(
   \sum_{j=2}^hs^{h-j}r^{[j]}q^{[h-j]}
   \right)_w.                                           \tag{21}
\end{aligned}
\]

Equations (20) and (21) have the same residual word projection but
disjoint response-count source grades:

\[
\begin{array}{c|c}
\text{row}&\text{response-count grades}\\ \hline
\text{mixed target row (20)}&0,1\\
\text{clean error (21)}&2,3,\ldots,h.
\end{array}                                              \tag{22}
\]

The vanishing target is already used in passing from the first line of
(21) to the second. Applying it again cannot kill (21).

At \(q=0\), (20) is identically zero for \(h\ge3\), while (21) is
\(r^{[h]}_w\). Construction (7)--(8) makes this coefficient nonzero on two
literal mixed words. This is the smallest exact counterguard to the claim
that \(\chi_i\) is “a nonconstant target word, hence zero.”

Complete diagonal anchors live at the three constant GHZ words and are
absent from this guard. They could, in principle, enter a cubical,
Plücker--Hessian, or cross-chart identity whose other face is (21). No such
identity is currently committed. Merely placing the constant-word anchor
rows beside (20) does not change the grade table (22).

## 5. Exact missing source relation

The response route now has one finite pass/fail condition.

> **Higher response--Fitting identity.** Construct from the complete
> diagonal anchors, crossed rows, and response Bianchi/Plücker faces a
> source-valid identity whose projection to the pure-divisor chart is (6)
> for every clean coordinate. Equivalently, construct a full-rank
> Hilbert--Burch matrix for the same clean family whose column-degree sum
> is at most \(h-1\), or prove (5) directly.

The identity must retain:

* the residual word and physical colour labels;
* the response-count/repeated-insertion fine grade;
* the complete target and anchor faces;
* the common binary cap-line parameter;
* boundary independence; and
* a nonzero physical terminal or a valid boundary/terminal alternative.

An ordinary response Plücker relation satisfies the first item but lands at
the degree-\(h\) boundary (13). A scalar or wordwise equality which forgets
the response-count grade cannot supply the second. A separate syzygy for
each coordinate does not supply one common Bezout kernel.

## 6. Exact checker and scope

The dependency-pinned checker
[verify_uniform_response_plucker_veronese_hilbert_burch_gate.py](../computations/verify_uniform_response_plucker_veronese_hilbert_burch_gate.py)
audits over exact rationals:

* the literal rank-one response Plücker identity;
* all \(h+1\) decorated response-power profiles;
* exact \(h=3,4\) Hilbert--Burch maximal minors;
* the all-order bidiagonal minor formula;
* dimension \(h\) of the complete linear-syzygy space;
* full rank \(2h\) of the clean Macaulay map for \(3\le h\le10\);
* the source-grade separation (22); and
* the \(q=0\) mixed-word target/clean-error guard.

The guard is an associated-graded physical response packet, not a complete
global Krenn source: it omits the diagonal target anchors. It rules out
ordinary Plücker polarization and the nonconstant-word shortcut. It does
not rule out the exact higher response--Fitting identity stated above.
