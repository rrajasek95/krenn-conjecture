# Sharper rate estimates, smaller constants, and the remaining cancellation problem

September 26, 2026. **Written research with exact supporting checks; awaiting
independent audit.** The preceding quantitative packages remain unchanged.
This note pursues the three proposed follow-ups rather than claiming that all
of their strongest targets have been solved.

| Direction | Outcome here | Still open |
|---|---|---|
| Sharp exponent | A stronger unrestricted exponent, and a sharp square-root exponent under a measurable cancellation condition | Unrestricted complex square-root bound |
| Useful constants | Much smaller six-site constants; a numerically meaningful bound when cancellation is controlled | Tight unrestricted constants and optimal rates |
| Other applications | A paired-hafnian inequality and stability corollary, with a separate provenance note | No independently new unrelated open-problem resolution is claimed |

[Explainer](../explainers/RATE-FOLLOWUPS.md) · [Replay](../computations/rate-sharpness-followup-2026-09-26/README.md) · [Paired-hafnian application](paired-hafnian-application-2026-09-26.md)

## 1. A parity projection improves the general exponent

Use the notation of the [general complex rate proof](general-complex-rate-bound-2026-09-26.md):
\(n=2m>4\), source norm \(S=1\), \(H=A^{[m]}\), pure average \(\lambda\),
\(\ell=|\lambda|\), and \(\epsilon=\|H-\lambda\Delta\|_2\).
Write \(A=A_0+O\), where \(A_0\) is the literal diagonal projection and
\(O\) consists of off-color cells. Set \(\eta=\|O\|_{\rm edge}\).

Let \(\Pi_{\rm even}\) retain only receiving words in which every color
appears an even number of times. Then

\[
 \Pi_{\rm even}H(A_0)=H(A_0),\qquad
 \Pi_{\rm even}DH(A_0)[O]=0.                         \tag{1}
\]

Every diagonal edge adds two copies of one color. Exactly one off-color edge
adds one copy of each of two different colors, leaving those two counts odd.
Thus (1) is an exact selection rule on every matching, at every size.

Pure amplitudes are unchanged by diagonal projection. Since orthogonal word
projection cannot increase error,

\[
 \epsilon_0:=\|H(A_0)-\lambda\Delta\|_2
 \le\epsilon+C_m\eta^2,\qquad C_m=2^m(2m-1)!!.       \tag{2}
\]

Indeed expand each matching product in \(A_0,O\). The linear term is removed;
a term with \(j\ge2\) off-color factors has tensor norm at most
\(\eta^j\|A_0\|^{m-j}\le\eta^2\). Sum over the at most \(2^m\) terms
and \((2m-1)!!\) matchings. No approximation or change of physical model
is made by this output-space projection.

The preceding approximate-diagonality theorem, with its constant \(G\), gives

\[
 \eta\le8G\ell^{-2}(\xi/\ell)^{1/m},\qquad
 \xi\le3^m\epsilon,
\]

provided \(x=\xi/\ell\le1\) and
\(G\ell^{-1}x^{1/m}\le\ell/2\). Consequently

\[
 \epsilon_0\le\epsilon+K\epsilon^{2/m}\ell^{-4-2/m},
 \qquad K=576C_mG^2.                                \tag{3}
\]

This replaces the previous linear dependence on \(\eta\).

### Explicit all-size theorem

Let \(P=(n-1)!!\), and let \(c_n\) and
\(k=3+3(m-1)/2\) be the diagonal amplitude constants from the
[diagonal theorem](quantitative-proof-identities-2026-09-26.md#8-a-global-rate-bound-for-diagonal-complex-sources).
Define

\[
 \begin{aligned}
 b&=\min\{c_n,1/(2P^{\lceil k-1\rceil})\},\\
 q&=1+\frac m2(k+4),\\
 \gamma_n&=\min\left\{
 \frac1{3^{2m}P^{2\lceil q-1\rceil}},\quad
 \left(\frac1{6GP^{\lceil k/2\rceil}}\right)^{2m},\quad
 \left(\frac b{4P^{\lceil q-k\rceil}}\right)^2,\quad
 \left(\frac b{4K}\right)^m\right\}.
 \end{aligned}                                      \tag{4}
\]

These constants are positive and rational. The amplitude constant is
\(\sqrt{\gamma_n}\); no rationality of its square root is needed.

**Theorem 1.** Every normalized complex three-color source satisfies

\[
 \epsilon^2\ge\gamma_n\ell^{2q},\qquad
 R\le\left(\frac{3^q}{\gamma_n}\right)^{\alpha_n}
          \frac{(1-F)^{\alpha_n}}{F^{1+\alpha_n}},
 \quad \boxed{\alpha_n=\frac{16}{n(3n+22)}}.          \tag{5}
\]

The rate statement assumes nonzero output and \(F>0\).
For \(d\ge3\) target colors replace \(3^q\) by \(d^q\), using the
three-color subset argument from the preceding note.

**Proof.** Assume \(\epsilon<\sqrt{\gamma_n}\ell^q\), with \(\ell>0\).
The first two terms of (4) imply the two inverse hypotheses above, since
\((q-1)/m-1=k/2+1\). The last two terms, inserted in (3), imply
\(\epsilon_0<(b/2)\ell^k\le\ell/4\). Apply the diagonal amplitude theorem
after normalizing \(A_0\); its squared source norm is at most one, so it gives
\(\epsilon_0\ge c_n\ell^k\). This is a contradiction. The case \(\ell=0\)
is immediate. Substitute \(\epsilon^2=(1-F)R\), \(\ell^2=FR/3\) to obtain (5).

| Sites | Previous general exponent | Improved general exponent |
|---|---:|---:|
| 6 | \(1/24\) | \(1/15\) |
| 8 | \(1/38\) | \(1/23\) |
| 10 | \(1/55\) | \(2/65\) |

This does not settle the optimal exponent. The improvement comes from
retaining a parity constraint that the preceding norm estimate discarded.
At six sites it also sharpens the allowed cancellation order: for a bounded
analytic source family with nonzero leading target amplitude of order \(t^r\)
and error of order \(t^s\), the amplitude inequality forces \(s\le16r\),
improving the previous \(s\le25r\). Rescaling a bounded family by one fixed
constant gives \(S\le1\), which is sufficient for the same inequality.

## 2. Six-site constants from the actual source norm

Counting each source cell as independently bounded by one wastes the constraint
that their squared magnitudes sum to one. This section replaces those counts
by norm budgets. It keeps all endpoint colors and arbitrary complex phases.

We use the existing sharp inequalities

\[
 |\operatorname{haf}_6(x)|\le S_x^{3/2}/\sqrt{15},\qquad
 \sum_e|\operatorname{haf}_4(x[V\setminus e])|^2\le(3/5)S_x^2.
                                                               \tag{6}
\]

They follow from [Roos, Theorem 2.3, equations (38)–(42)](https://arxiv.org/html/1906.06176).
The workspace also has an elementary six-site proof in
[the hafnian norm note](six-site-sharp-hafnian-norm-slack.md).
In particular, that note's proposed all-size Frobenius bound is already a
consequence of Roos's published inequality; it should not be presented as a
new open conjecture.

Triangle inequality on matching tensors gives
\(\|H(A)\|_2\le S^{3/2}/\sqrt{15}\).
For the three diagonal color energies \(S_h\), (6) gives

\[
 \ell\le\frac1{3\sqrt{15}}\sum_h S_h^{3/2}
 \le\frac1{3\sqrt{15}}<\Lambda:=1/10.                \tag{7}
\]

### Uniform root-response bounds

Fix a five-site receiving word and let \(r_i\) be the coefficient norm of
its root mean at site \(i\). Let \(a\) bound the squared norm of the relevant
root cells and \(b\) that of the retained cells. Then
\(a+b\le1\), \(\sum_i r_i^2\le3a\).
Let \(P_j\) be the absolute partial-matching sum with \(j\) singletons.
Cauchy–Schwarz, the four-site bound \(\operatorname{haf}_4(|x|)\le S_x/2\),
and the elementary symmetric mean inequality give

\[
 P_1\le1/\sqrt3,\quad
 P_3\le27\sqrt2/80,\quad
 P_5\le(3/5)^{5/2}.
\]

For the first estimate, each retained edge occurs in three of the five
four-site cores. Hence the sum of their squared scalar hafnians is at most
\(3b^2/4\), and \(P_1\le(3/2)\sqrt a\,b\).
For the second, use
\(P_3\le\sqrt b\sqrt{e_3(r_1^2,\ldots,r_5^2)}
\le(3\sqrt6/5)a^{3/2}\sqrt b\).
For the third use the product bound on the five means.
Their individual maxima sum to less than \(3/2\). Thus the previous
per-word count \(M=6318\) can be replaced by

\[
                              M=3/2.                \tag{8}
\]

For a literally diagonal root each receiving word has only one root parameter
per site, so the same argument without the factor three gives

\[
 P_3+P_5\le3\sqrt6/80+1/(25\sqrt5)<11/100.           \tag{9}
\]

This replaces the diagonal higher-response count \(I_5=26\).

### Better omission constants for the general source

On a four-site binary core the retained tensor coefficient norm is at most
\(2\): its Euclidean norm is at most \(1/2\), and there are sixteen words.
The degree-two mean response has coefficient norm at most \(2\sqrt2<3\).
For the latter, let \(r_i\) sum the six root-parameter/receiving-color entries
at site \(i\). Then \(\sum r_i^2\le6a\), and an edge block has coefficient
norm at most twice its Euclidean norm. Cauchy–Schwarz gives
\(2\sqrt b\sqrt{e_2(r_i^2)}\le3\sqrt6a\sqrt b\le2\sqrt2\).

In the general-rate proof set

\[
 \begin{aligned}
 U&=32M=48,&V&=2(\Lambda+M)=16/5,\\
 T&=9\cdot33(\Lambda+U)(U+V)=18285696/25,\\
 Z&=T/(4M^2)=2031744/25.
 \end{aligned}
\]

Use the actual cube root in the cubic-response estimate: the exact inequality
\(165^3\ge(64/7)3!Z\) gives

\[
 K_3=32M(1+12\cdot165)=95088,\qquad
 G=6[2(2K_3+3\Lambda)+\Lambda^2]=114105783/50.         \tag{10}
\]

Here the core bounds \(2,3\) replace the previous \(160,1440\).
These estimates prove the same conditional approximate-diagonality statement
as before, with the new \(G\).

### Better transfer constants for the diagonal source

Use the literal two-root notation of the diagonal proof, on four retained
sites: means \(px+qy\), derivative rows \(u,v\), retained binary edges,
and direct edge \(e\). Let their squared energy budgets be
\(a,s_u,s_v,b,s_e\), whose sum is at most one. Set
\(r_i=|x_i|+|y_i|\); then \(\sum r_i^2\le2a\).

Cauchy–Schwarz on the partial matchings bounds the two parts of \(E_u\) by
\(2\sqrt{2s_uab}\) and \(\sqrt{s_ua^3/2}\), respectively. Their maxima
are \(\sqrt{8/27}<11/20\) and \(3\sqrt6/32<1/4\).
The same holds for \(E_v\), so

\[
                          M_u,M_v\le4/5.
\]

The two parts of \(E_{uv}\) are at most
\(2\sqrt{s_us_vb}\) and \(\sqrt3a\sqrt{s_us_v}\), whose maxima are less
than \(2/5\) and \(9/40\). The three parts of \(eE\) are at most
\(\sqrt{s_e}b\), \(\sqrt{3s_e b}\,a\), and \(\sqrt{s_e}a^2/4\);
their maxima are less than \(2/5,9/40,3/40\). Hence

\[
 M_Z\le53/40,\qquad
 B=M_v+M_Z+28(M_u+M_v)=1877/40.                      \tag{11}
\]

The number 28 is the previously verified covariance projection factor for
\(D=2\), with projection norm eight. All differentiated singleton slots
are included in the displayed sums.

By (9), the diagonal boundary bound is
\(\epsilon_b\le\xi[1+16(11/100)/\tau]\).
When \(\epsilon\le\ell/2\), every pure amplitude has modulus at least
\(\tau=\ell/2\). Thus

\[
 \|r_A\|_1\le K_d\epsilon/\ell,\quad
 K_d=27B(\Lambda+88/25)=9172899/2000.
\]

The retained tensor now has Euclidean norm at most \(1/2\). The endpoint
estimate of the diagonal proof therefore gives, for \(|d|\ge\kappa\),

\[
 |\beta-d\alpha|\le Q\kappa^{-2}\epsilon/\ell^2,
 \qquad Q=4K_d+\Lambda=9172949/500.                  \tag{12}
\]

### A less conservative edge threshold

Set \(\kappa^2=\ell^3/(16P)\), with \(P=15\). The light contribution at a
vertex is at most \((5/2)\kappa\le\ell/16\), using (7).
If \(\epsilon<c_d\ell^6\), where

\[
              c_d=1/(80PQ)=5/110075388,              \tag{13}
\]

then every heavy edge has endpoint defect less than \(\ell/5\).
For a vertex with \(j\) heavy neighbors, the hafnian expansion would give
\((j-1)\ell/2<j\ell/5+\ell/16\) if \(j\ge2\), which is impossible.
There cannot be zero heavy neighbors either. Each color's heavy edges
therefore form a perfect matching.

A non-heavy competing matching uses at least two light edges. Its total
contribution is at most \(P\kappa^2=\ell^3/16\).
Each heavy pure product is at least
\(\ell/2-\ell^3/16\ge49\ell/100\).
The mixed heavy matching from the preceding proof therefore leaves output
of magnitude at least
\([(49/100)^3-1/16]\ell^3>\ell^3/20\).
But \(c_d\ell^6<\ell^3/20\), a contradiction.
If \(\epsilon>\ell/2\), (13) is automatic by (7).
We have proved the unconditional diagonal amplitude bound
\(\epsilon\ge c_d\ell^6\), with the same exponent as before and a much
larger amplitude constant.

### Quadratic projection has a small six-site constant

In (2) one can replace \(C_3=120\) by \(3/4\).
Write \(H(A_0+zO)=\sum_{j=0}^3z^jH_j\) and
\(a_0=\|A_0\|\). Orthogonality of the source-cell supports and (6) give
\(\|H(A_0+zO)\|\le(a_0^2+|z|^2\eta^2)^{3/2}/\sqrt{15}\).
The coefficient estimate on the circle of radius
\(\sqrt2a_0/\eta\) yields
\(\|H_2\|\le3a_0\eta^2/(2\sqrt5)\); direct homogeneity gives
\(\|H_3\|\le\eta^3/\sqrt{15}\). Their sum is at most
\(\sqrt{31/60}\,\eta^2\le(3/4)\eta^2\), since
\(a_0^2+\eta^2\le1\). Zero cases follow directly or by continuity.
The circle estimate is just the vector-valued coefficient formula and the
triangle inequality, not a numerical fit.

Thus \(K=432G^2\) in (3). With \(q=16,k=6\), use

\[
 \gamma_6=\min\left\{
 \frac1{27^2\Lambda^{30}},\quad
 \left(\frac1{6G\Lambda^3}\right)^6,\quad
 \left(\frac{c_d}{4\Lambda^{10}}\right)^2,\quad
 \left(\frac{c_d}{4K}\right)^3\right\}.              \tag{14}
\]

The replay checks every budget exactly. The resulting prefactors, in
\(R\le C(1-F)^\alpha/F^{1+\alpha}\), are

| Six-site scope | Previous \(\alpha,C\) | New \(\alpha,C\) |
|---|---|---|
| Diagonal complex | \(1/5,\ 1.46\times10^9\) | \(1/5,\ 3233.21\) |
| Arbitrary complex | \(1/24,\ 7.14\times10^{10}\) | \(1/15,\ 147338.83\) |

These are substantial improvements but the unrestricted estimates remain
numerically weak. The next section supplies useful constants on a broad
class with controlled cancellation.

## 3. A sharp square-root law when cancellation is controlled

This result allows all 135 complex endpoint-color cells at six sites.
Let \(a_{M,w}\) be a matching's contribution to word \(w\), and put

\[
 P_w=\sum_M|a_{M,w}|=H_w(|A|),\qquad
 \kappa=\min_{w\in\mathcal W,\,P_w>0}\frac{|H_w(A)|}{P_w}.
                                                               \tag{15}
\]

Here \(\mathcal W\) consists of the 180 mixed words whose three color counts
are all even: types \((4,2,0)\) and \((2,2,2)\). An empty minimum is one.
The number \(\kappa\in[0,1]\) measures cancellation of actual full output
amplitudes; it is not assumed positive on arbitrary sources.

The existing nonnegative certificate, applied to \(|A|\), gives

\[
 |\tau_a\tau_b\tau_c|
 \le\frac1\kappa\sqrt{41/1440}\,S^3\|E_{\rm mix}\|_2
                                                        \tag{16}
\]

when \(\kappa>0\). Indeed \(|\tau_h(A)|\le\tau_h(|A|)\), while
\(P_w\le|H_w(A)|/\kappa\) on every word used by that certificate.
For arbitrary endpoint colors the pure outputs still use only diagonal
cells. Adding nonnegative off-color cells can only increase the mixed
envelopes and the source norm, so the same certificate applies.
The [original exact cover](universal-rate-bound-feasibility-2026-09-26.md#4-an-explicit-universal-six-site-bound-without-cancellation)
is replayed over all 3,375 matching triples; it is not replaced by the false
rainbow-only shortcut described below.

Since the target-orthogonal component of a pure basis vector has norm
\(\sqrt{2/3}\),
\(|\tau_h|\ge\sqrt{R/3}(\sqrt F-\sqrt{2(1-F)})\) when \(S=1\).
For \(F>2/3\), (16) proves

\[
 \boxed{R\le\frac{\sqrt{123/160}}{\kappa}
 \frac{\sqrt{1-F}}{[\sqrt F-\sqrt{2(1-F)}]^3}.}       \tag{17}
\]

On every class with \(\kappa\ge\kappa_0>0\), the exponent \(1/2\) is optimal:
the positive prism family belongs to that class when \(\kappa_0\le1\) and
has square-root scaling. The constant is not claimed optimal.

### A phase condition guarantees the required cancellation bound

Suppose that, for some local port phases \(\theta_p(i)\), every nonzero cell
can be written

\[
 A_{pq}(i,j)=r_{pq}(i,j)
 e^{i[\theta_p(i)+\theta_q(j)+\varepsilon_{pq}(i,j)]},
 \quad r_{pq}(i,j)>0,\quad |\varepsilon_{pq}(i,j)|\le\phi<\pi/6.
\]

Every matching contributing to a fixed word has the same sum of port phases.
Its remaining phase is in \([-3\phi,3\phi]\). Projection onto the central
ray therefore gives \(|H_w|\ge\cos(3\phi)P_w\), so

\[
                         \kappa\ge\cos(3\phi)>0.     \tag{18}
\]

For diagonal sources alone, it suffices to control phases within every
four-site pure cofactor; a cell phase error at most \(\phi<\pi/4\) after
port gauges gives the better \(\kappa\ge\cos(2\phi)\). Three-color words
then have a single compatible matching, and two-color words are an edge
times a four-site cofactor. No phase condition is imposed on zero cells.

The six-site Gaussian probability conversion previously derived in the
specified zero-displacement, exact-number-selection model gives

\[
 P_{\rm success}\le\frac3{4\kappa}
 \frac{\sqrt{1-F}}{[\sqrt F-\sqrt{2(1-F)}]^3}.         \tag{19}
\]

This uses the conservative bound on its conversion constant from the earlier
note. For a ten-degree cell-phase tolerance, \(\kappa\ge\sqrt3/2\).
The saved calibration table evaluates (17)–(19); these are upper bounds,
not predictions or claims of achievability.
Its final column also applies the independent norm bound
\(P_{\rm success}\le(243/256)^3/15\), obtained by combining (6) with
the same Gaussian conversion. These probability statements use the
three-color model with no ancillary modes from that conversion argument.

### What beating the prism would require

Rearranging (17) bounds \(\kappa\) from above in terms of an observed
\(F,R\). A family with \(R\) comparable to \((1-F)^\beta\),
\(\beta<1/2\), must satisfy
\(\kappa=O((1-F)^{1/2-\beta})\).
It must develop increasingly complete cancellation in at least one of the
180 specified mixed words. Thus the remaining sharp-rate question is
concentrated in a quantitatively identifiable cancellation regime.
This does not prove that such a family exists or cannot exist.

## 4. Discarded shortcut and exact scope

A tempting claim was that three six-site perfect matchings without a rainbow
matching must share one edge and form the three distinct matchings on the
other four vertices. Exhaustive checking refutes it. Of 3,375 ordered triples,
1,530 have no rainbow matching. Their sorted pairwise intersection sizes are

| Intersection sizes | Count |
|---|---:|
| \((0,0,1)\) | 1080 |
| \((0,0,3)\) | 360 |
| \((1,1,1)\) | 90 |

Only the last class has the proposed form. For example,
\((01|23|45),(01|23|45),(02|14|35)\) is a counterexample.
The false claim is not used in any theorem above. No unrestricted
square-root theorem follows from the phase-controlled result.

The [application note](paired-hafnian-application-2026-09-26.md) answers a
posted hafnian inequality question and derives a quantitative corollary,
while explicitly crediting the existing result that already implies its
qualitative answer. No new unrelated conjecture is reported as solved.
