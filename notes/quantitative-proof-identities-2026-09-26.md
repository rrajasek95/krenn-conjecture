# Quantitative proof identities and a global diagonal rate bound

Date: September 26, 2026.

**Status: new written deductions with an exact standard-library replay;
not independently audited or admitted to the certified proof spine.**
The all-orders written proof remains unchanged. In addition to quantitative
identities, Section 8 proves an explicit architecture-independent rate bound
for every diagonal complex three-color source at each even size \(n>4\):
the exponent is \(4/(3n+2)\). The constants are conservative. Arbitrary
endpoint colors and sharp global exponents remain outside this result.

## 1. Results and scope

The [all-orders proof](../proofs/krenn-gu-all-orders-two-replica-proof.md)
uses two quite different finite-polynomial arguments. Their quantitative
behavior is also different.

| Step | Quantitative result | Limitation exposed |
|---|---|---|
| The response scaling equation | An explicit bound with sharp exponent \(1/(D+1)\) for an even polynomial of degree at most \(2D\) | Truncated exponentials rule out a general linear bound |
| The endpoint differential equation | An exact finite inverse and its sharp coefficient-norm constant | The constant diverges as the edge weight approaches zero |
| Extracting the endpoint | A denominator-free polynomial certificate on any diagonal two-color source | Small edge weights require explicit accounting |
| Literal diagonal three-color sources | A linear bound from physical mixed output to every higher binary response and root-boundary residual | It assumes actual diagonality and nonzero pure amplitudes |
| Stable matrix covariance | A finite projection transfers boundary errors to the scalar endpoint residual | Constants depend on polynomial degree |
| Global diagonal sources | A rate exponent \(4/(3n+2)\), with explicit constants and no lower edge-weight assumption | The exponent and constants are not claimed sharp |

The word “sharp” refers to the exponent in the first row and the operator
norm in the second. The constants in the first row are conservative.
The sharp polynomial examples are not claimed to be realizable as
near-GHZ physical sources.

The useful new bridge is Section 4: it defines the endpoint scalar on an
arbitrary source, even when the special matrix form in the exact proof
fails. Thus its residual is an observable algebraic diagnostic, rather
than an assumption that the exact proof already applies.

Read the [replay guide](../computations/quantitative-proof-identities-2026-09-26/README.md).
No historical-priority claim is made for finite differential inversion,
formal logarithms, or polynomial stability methods.

## 2. Stability of the finite response scaling equation

Let \(L=(L_1,\ldots,L_s)\) be auxiliary variables. For a polynomial \(p\),
let \(\|p\|_1\) be the sum of the absolute values of its coefficients.
It is submultiplicative. Truncating high-degree terms cannot increase it.

Let \(g\) be even, of total degree at most \(2D\), where \(D\ge1\), with

\[
 g(0)=1,\qquad \|g-1\|_1\le\tfrac12.
\]

Write \(q=g_2\) for its homogeneous quadratic part and define

\[
 r(L)=g(L/\sqrt2)^2-g(L),\qquad
 \varepsilon=\|r\|_1,\qquad C=\frac{64}{7}.
\]

**Theorem 1.** The following bounds hold:

\[
 \left\|g-\sum_{j=0}^{D}\frac{q^j}{j!}\right\|_1
 \le C\varepsilon,\qquad
 \|q^{D+1}\|_1\le C(D+1)!\varepsilon.                 \tag{1}
\]

In particular, on the closed unit polydisc \(|L_i|\le1\), put

\[
 t=\min\left\{\tfrac12,\,
       [C(D+1)!\varepsilon]^{1/(D+1)}\right\}.
\]

Then

\[
 \sup |q(L)|\le t,\qquad
 \sup |g(L)-1|\le 2t+C\varepsilon.                   \tag{2}
\]

For a coefficient-norm version, a quadratic has at most
\(M=s(s+1)/2\) monomials. Each coefficient is bounded by its supremum
on the unit torus, so

\[
 \|q\|_1\le Mt,\qquad
 \|g-1\|_1\le2Mt+C\varepsilon.                       \tag{3}
\]

These are bounds on the polynomial scaling residual. They do not identify
\(\varepsilon\) with the physical output error.

### Proof

Work in the finite algebra that discards monomials of total degree greater
than \(2D+2\). All following logarithms and exponentials are finite formal
series in its positive-degree ideal. Define

\[
 h=\log g.
\]

Its coefficient norm is at most
\(-\log(1-\|g-1\|_1)\le\log2\). Its degree-two part is \(q\).
Since \(g-1\) starts in degree two,

\[
 \|g(L/\sqrt2)-1\|_1\le\tfrac14,\qquad
 \|g(L/\sqrt2)^2-1\|_1\le\tfrac{9}{16}.
\]

For two elements \(1+u,1+v\) with norms of \(u,v\) at most \(a<1\),
the power-series identity for the logarithm and the telescoping identity
for \(u^k-v^k\) give

\[
 \|\log(1+u)-\log(1+v)\|_1
 \le\frac{\|u-v\|_1}{1-a}.
\]

Apply this with \(a=9/16\). The formal logarithm respects products in this
commutative algebra, hence

\[
 \|2h(L/\sqrt2)-h(L)\|_1\le\frac{16}{7}\varepsilon.
\]

On homogeneous degree \(2j\), the operator on the left multiplies by
\(2^{1-j}-1\). Its kernel among even positive degrees is exactly degree
two. For \(j\ge2\), the absolute value of this multiplier is at least
\(1/2\). Consequently

\[
 \|h-q\|_1\le\frac{32}{7}\varepsilon.                \tag{4}
\]

The exponential difference satisfies

\[
 \|\exp h-\exp q\|_1
 \le \exp(\max\{\|h\|_1,\|q\|_1\})\,\|h-q\|_1
 \le 2\|h-q\|_1.
\]

Here \(\|q\|_1\le1/2\), and \(\exp h=g\) in the truncated algebra.
Its degrees at most \(2D\) give the first inequality in (1). Its
degree \(2D+2\) gives the second, because \(g\) has no such term.

For every point of the unit polydisc,
\(|q(L)|^{D+1}\le\|q^{D+1}\|_1\). Also \(|q(L)|\le1/2\).
Equation (1) now gives

\[
 |g(L)-1|\le e^{|q(L)|}-1+C\varepsilon
            \le2t+C\varepsilon.
\]

The coefficient bound follows by the same argument with \(\|q\|_1\),
using its existing upper bound \(1/2\). This proves (1)–(3).

### Why the exponent cannot improve for this polynomial problem

In one variable take

\[
 g_t(L)=\sum_{j=0}^{D}\frac{t^jL^{2j}}{j!},
 \qquad 0<t\le\tfrac14.
\]

It satisfies the norm hypothesis. All residual terms through degree
\(2D\) cancel, and the first surviving term is

\[
 g_t(L/\sqrt2)^2-g_t(L)
 =\frac{1-2^{-D}}{(D+1)!}\,t^{D+1}L^{2D+2}
    +O(t^{D+2}).                                    \tag{5}
\]

Meanwhile \(g_t-1\) has quadratic coefficient \(t\). Thus no uniform
bound of the form distance \(\le K\varepsilon^\theta\) can hold here
with \(\theta>1/(D+1)\).

In the original \(n\)-site odd-response argument, \(D=(n-2)/2\).
The corresponding exponents for this isolated polynomial step are
\(1/3,1/4,1/5\) at six, eight, and ten sites.
**These are not fidelity–rate exponents.**

For a polynomial with a larger coefficient norm, the smallness assumption
can always be arranged by shrinking the auxiliary parameter polydisc.
For example, with \(M_0=\|g-1\|_1\), take
\(\rho=[2\max\{1,M_0\}]^{-1/2}\) and replace \(L\) by \(\rho L\).
This rescales proof parameters, not source weights. Restoring the original
parameter domain incurs degree-dependent factors; they cannot be dropped.

## 3. The finite differential inverse and its exact norm

Let \(p(z)\) have degree at most \(D\), let \(d\ne0\) be fixed, and set
\(r=p'+dp\). Differentiation to order \(D+1\) is zero. Therefore

\[
 p=\sum_{j=0}^{D}\frac{(-1)^j}{d^{j+1}}r^{(j)}.
                                                               \tag{6}
\]

This is a finite geometric-series inverse of differentiation plus
multiplication by \(d\). Multiplying by \(d^{D+1}\) gives the polynomial
identity

\[
 d^{D+1}p=\sum_{j=0}^{D}(-1)^j d^{D-j}r^{(j)}.        \tag{7}
\]

Unlike (6), equation (7) is meaningful and valid also at \(d=0\).
It does not supply an inverse there.

**Theorem 2.** In the ordinary coefficient norm,

\[
 \|p\|_1\le K_D(d)\|r\|_1,\qquad
 K_D(d)=\sum_{j=0}^{D}
       \frac{D!}{(D-j)!\,|d|^{j+1}}.                 \tag{8}
\]

This operator norm is exact. The inverse sends the monomial \(z^k\)
to coefficients in distinct degrees whose absolute sum is
\(\sum_{j=0}^{k} k!/(k-j)!\,|d|^{-j-1}\).
These column sums increase with \(k\), so their maximum occurs at \(D\);
the input \(r=z^D\) attains it.

The bound also applies when coefficients are polynomials in additional
parameters and the norm sums the absolute values of all coefficients.
Only the degree in \(z\) enters \(K_D\).

For evaluating the constant term, a smaller sharp functional norm is
available:

\[
 |d\,p(0)|\le J_D(d)\|r\|_1,\qquad
 J_D(d)=\max_{0\le j\le D}\frac{j!}{|d|^j}
       =\max\left\{1,\frac{D!}{|d|^D}\right\}.        \tag{9}
\]

Indeed \(d\,p(0)=\sum_j(-1)^j j!d^{-j}r_j\).
The sequence \(j!|d|^{-j}\) has increasing consecutive ratios, so its
maximum occurs at an endpoint. A suitable monomial attains the bound.

### Why a small edge weight cannot be ignored

Take \(p_d(z)=\sum_{j=0}^{D}(-dz)^j/j!\). Then exactly

\[
 p_d'+dp_d=\frac{(-1)^D d^{D+1}}{D!}z^D.
\]

As \(d\to0\), its residual tends to zero while \(p_d(0)=1\).
There can be no uniform inverse bound without accounting for \(d\).
For \(D=3,d=1/100\), the exact inverse norm is \(606030100\).
This is a demonstrated obstruction to a proposed estimate, not a
counterexample to a physical rate bound.

## 4. A literal-source endpoint diagnostic without exact rigidity assumptions

Let \(n=2D+2\ge4\). Take any two diagonal color matrices \(B,H\), with
arbitrary complex symmetric hollow entries. We do not assume a pure
output, nonzero amplitudes, or vanishing higher responses.

Choose roots \(p\ne q\), put \(U=V\setminus\{p,q\}\), and use the actual
retained binary quadratic \(Q\). Define

\[
 d=B_{pq},\quad e=H_{pq},\quad
 \beta=\operatorname{haf}(B),\quad
 \eta=\operatorname{haf}(H),\quad
 \alpha=\operatorname{haf}(B[U]).
\]

Let \(x,y\) be the \(B\)-colored root rows from \(p,q\) into \(U\), and
let \(u,v\) be the corresponding \(H\)-colored rows. The even response is

\[
 E(L)=\sum_{j=0}^{D}\frac{L^{2j}}{(2j)!}\,Q^{[D-j]},
 \qquad F=E(0).
\]

Products using a site twice are zero. Directional derivatives \(E_u,E_v\)
keep the source fixed. Let \(K\) be the complementary alternating pairing
from the full proof; \(K(b^U,h^U)=1\).

For two parameter columns \(P,Q_c\in\mathbb C^2\), set
\(L_i=P_i x+(Q_c)_i y\), and form the polynomial matrix

\[
 \begin{aligned}
 T_{11}&=K(E_{uv}(L_1),E(L_2))+eK(E(L_1),E(L_2)),\\
 T_{22}&=K(E(L_1),E_{uv}(L_2))+eK(E(L_1),E(L_2)),\\
 T_{12}&=K(E_u(L_1),E_v(L_2)),\\
 T_{21}&=K(E_v(L_1),E_u(L_2)).
 \end{aligned}                                      \tag{10}
\]

Universal two-copy covariance applies to every such source.
No target equations were used in defining (10).

### A scalar that exists even when the special matrix form fails

The trace of \(T\) is an orthogonal scalar invariant. Its antisymmetric
component transforms by the determinant. For two parameter vectors this
implies

\[
 T_{12}-T_{21}=(P_1(Q_c)_2-P_2(Q_c)_1)
                 b(\sigma,\rho,z),
\]

with polynomial \(b\), where
\(\sigma=P\cdot P,\rho=Q_c\cdot Q_c,z=P\cdot Q_c\).
One elementary proof uses the weight-zero generators
\(\sigma,\rho,r,s\) of the exact proof: reflection exchanges \(r,s\),
and every antisymmetric expression is divisible by \(r-s\).
The quotient is a polynomial in \(\sigma,\rho,r+s\).

Define

\[
 a=\tfrac12(\operatorname{tr}T-zb).
\]

This is polynomial and invariant. It agrees with the exact proof's \(a\)
when \(T=aI+bPQ_c^{\mathsf T}\). In general there is an additional
symmetric trace-zero matrix; **we do not assume that it vanishes**.

There is a division-free way to extract \(A(z)=a(0,0,z)\):

\[
 P=(1,i),\qquad Q_c=(z/2,-iz/2),\qquad
 \boxed{A(z)=\tfrac12\{\operatorname{tr}T-i(T_{12}-T_{21})\}.} \tag{11}
\]

Here the parameter dot products are \(0,0,z\), and the determinant is
\(-iz\). Thus (11) involves neither division by \(z\) nor the choice of
a physical inverse.

In any nonzero complementary pairing there are exactly \(|U|=2D\)
slots of color \(B\). Only these can contain \(B\)-mean parameters.
Consequently the matrix entries have parameter degree at most \(2D\).
Each scalar invariant has degree two, and

\[
                         \deg A\le D.                \tag{12}
\]

### Origin error and endpoint certificate

At zero parameters,

\[
 Z_0=E_{uv}(0)+eF,\qquad
 A(0)=K(F,Z_0).
\]

The tensor \(Z_0\) is precisely the full binary output with both roots
fixed to color \(H\). Its all-\(H\) coefficient is \(\eta\). Define

\[
 W=Z_0-\eta h^U,\qquad
 \omega=A(0)-\eta\alpha=K(F,W),\qquad
 r_A(z)=A'(z)+dA(z)-\beta\eta.                       \tag{13}
\]

The first equality for \(A(0)\) follows also directly from (10):
at zero means \(E_u(0)=E_v(0)=0\), and the two diagonal entries agree.
The invariant evaluation in (11) at \(z=0\) has the same scalar value,
since all three scalar invariants vanish.

**Theorem 3.** Every source above satisfies the polynomial certificate

\[
 \boxed{
 d^D\eta(d\alpha-\beta)
 =\sum_{j=0}^{D}(-1)^j d^{D-j}r_A^{(j)}(0)
       -d^{D+1}\omega.}                             \tag{14}
\]

It is valid even when \(d=0\) or \(\eta=0\); it makes no endpoint
equality assertion at those degeneracies.

For \(d\ne0\), with Euclidean tensor coefficient norms, it gives

\[
 \boxed{
 |\eta|\,|\beta-d\alpha|
 \le J_D(d)\|r_A\|_1+|d|\,\|F\|\,\|W\|.}            \tag{15}
\]

To prove (14), apply (7) to
\(p=A-\beta\eta/d\), evaluate at zero, and use
\(A(0)=\eta\alpha+\omega\). Clearing denominators gives a polynomial
identity, hence also the \(d=0\) case. Equivalently, the derivative
terms telescope directly without dividing.
Equation (9) and Cauchy–Schwarz for the signed permutation pairing \(K\)
prove (15).

The norm \(\|W\|\) is bounded by the binary mixed-output norm. For a
diagonal three-color source it is also bounded by the full target error
norm, because projection and taking a slice cannot increase that norm.

There is a simple explicit bound for the remaining factor. If the
retained squared edge-block norm is \(S_U\), then

\[
 \|F\|\le(2D-1)!!\,(S_U/D)^{D/2}.                  \tag{16}
\]

Each retained matching tensor has norm equal to the product of its \(D\)
edge-block norms. Arithmetic–geometric mean gives \((S_U/D)^{D/2}\);
there are \((2D-1)!!\) matchings. This proves (16).

### An explicit necessary premise

On four sites take \(B\) to be the unit-weight graph with edges
\(02,03,12,13\), and \(H\) the unit matching \(01,23\).
Its entire output is exactly \(2b^4+h^4\). For roots \(p=0,q=2\),

\[
 d=1,\quad\beta=2,\quad\eta=1,\quad\alpha=1,\quad
 A(z)=1+z,\quad r_A(z)=z,\quad W=0.
\]

The endpoint defect is \(1\), despite zero mixed output. Thus no estimate
controlling \(r_A\) solely by binary mixed-output error can hold.
Any source-to-residual bound must use the third active color (or an
appropriate higher-response hypothesis). The replay reproduces this
example exactly.

## 5. A quantitative diagnostic for the graph step

For a color matrix \(B\) with nonzero \(\beta\), at a vertex \(p\) define
\(\Delta_{pq}=\beta-B_{pq}\operatorname{haf}(B[V\setminus\{p,q\}])\)
for its \(k\) supported neighbors. Hafnian expansion gives exactly

\[
 (k-1)\beta=\sum_{q:\,B_{pq}\ne0}\Delta_{pq}.
\]

Therefore \(k\ge2\) implies

\[
             \max_q|\Delta_{pq}|\ge\tfrac12|\beta|. \tag{17}
\]

This requires no positivity. Combine it with (15).
For a diagonal three-color source with total squared edge-block norm at
most one, all three pure amplitudes at least \(\tau>0\), and every nonzero
colored edge weight at least \(\kappa>0\) in modulus, put
\(L_D=(2D-1)!!D^{-D/2}\). Some color having degree at least two implies

\[
 \max \|r_A\|_1
 \ge \frac{\tau^2/2-L_D e_{\rm mix}}{J_D(\kappa)}    \tag{18}
\]

whenever the numerator is positive. The maximum includes the relevant
ordered color choices and supported root pairs. We used \(|d|\le1\),
\(\|W\|\le e_{\rm mix}\), and \(J_D(d)\le J_D(\kappa)\).

If every color instead has degree one everywhere, the graph argument of
the full proof supplies a mixed matching for \(n>4\), including the case
where two colors share a physical pair. Its word has a unique compatible
matching and hence

\[
                         e_{\rm mix}\ge\kappa^{n/2}. \tag{19}
\]

This dichotomy is a computable diagnostic on a nondegenerate diagonal
stratum. It is not an unrestricted fidelity bound: (18) allows an
auxiliary residual to be large.

## 6. Physical output controls higher responses on diagonal sources

There is a useful route around Theorem 1 when the source is already
diagonal. The pure higher responses then involve only one root parameter
each, so a coefficient comparison replaces the nonlinear scaling argument.

Assume the source is literally diagonal in three colors \(a,b,c\),
all individual colored edge weights have modulus at most one, and
all three pure amplitudes have modulus at least \(\tau>0\).
Normalization to total squared edge norm at most one is sufficient for
the edge-weight hypothesis, but is not required.

Let \(\xi\) be the coefficient sum of the mixed full output:

\[
 \xi=\sum_{\text{mixed }w}|H_w|,\qquad
 \xi\le\sqrt{3^n-3}\,e_{\rm mix}.                    \tag{20}
\]

Delete a root and put \(N=n-1\). In three independent root parameters
\(s_a,s_b,s_c\), write \(L=\sum_h s_hY_h\) for the actual colored rows.
Let

\[
 \Psi(L)=\sum_{j=0}^{(N-1)/2}
       \frac{L^{2j+1}}{(2j+1)!}R^{[(N-2j-1)/2]},
 \quad \Phi(L)=L R^{[(N-1)/2]},\quad
 \mathcal H=\Psi-\Phi.
\]

The norm of a polynomial tensor below sums absolute coefficients over
both its receiving words and its root-parameter monomials.
Let \(I_N\) be the number of partitions of \(N\) labeled elements into
singletons and pairs. Thus

\[
 I_0=I_1=1,\qquad I_N=I_{N-1}+(N-1)I_{N-2}.
\]

For example \(I_3=4,I_5=26,I_7=232\).

**Theorem 4.** For each receiving word \(w\) using at most two colors,

\[
 \|\mathcal H_w\|_1\le I_N\xi/\tau.                  \tag{21}
\]

Consequently every binary projection satisfies

\[
 \|\mathcal H_{\rm binary}\|_1\le 2^N I_N\xi/\tau.   \tag{22}
\]

For each of the four literal root-boundary equations (7) in the complete
proof, let its residual be the left side minus the displayed pure right
side, as a polynomial tensor in the two root parameters. Then

\[
 \boxed{\|\text{boundary residual}\|_1
 \le \xi\left(1+\frac{2^{n-2}I_{n-1}}{\tau}\right).} \tag{23}
\]

All odd degrees, including the terminal one, are included.

The count \(I_N\) is deliberately coarse. It can be replaced throughout
by the source-specific quantity \(M_p\): the maximum, over receiving
words, of the sum of absolute weights of partial matchings with at least
three singletons, using the actual root rows and retained edges.
Taking absolute values before summation makes this an upper bound even
with interference. It is directly computable and satisfies \(M_p\le I_N\)
under the edge-weight hypothesis.

For the replay's perturbed six-site prism, \(\tau=1/10\), \(\xi=1/500\),
and \(M_p=1/10\). The source-specific bound for each binary higher
response is \(1/500\); the largest actual response has norm \(1/1000\).
The count-only bound \(13/25\) is much looser.

### Proof

For each fixed receiving word, the coefficient polynomial of
\(\mathcal H\) is a sum over partial matchings with at least three
singletons. Each contribution has coefficient of modulus at most one.
There are at most \(I_N\) partial matchings, so
\(\|\mathcal H_w\|_1\le I_N\) without using small output error.

The linear response is the literal full output expanded at the root.
Write

\[
 \Phi(L)=\sum_h\tau_h s_h h^\Omega+\mathcal E(L).
\]

Its mixed-error coefficient norm is exactly \(\xi\): each full mixed word
appears once, with its root color recorded by the corresponding parameter.
Pure one-defect coefficients vanish identically for a diagonal source,
since an edge always supplies two vertices of the same color.

The universal reflection identity (3) in the complete proof holds at
every odd degree. Divide each by its raw-power factorial and sum over
degrees at least three. For any choice of distinct local color pairs it
gives the same alternating coefficient identity for \(\mathcal H,\Phi\).
Replacing \(\Phi\) by its pure part moves an error to the other side
whose coefficient norm is at most

\[
 I_N\sum_{\text{selected complementary words }v}
                         \|\mathcal E_v\|_1
 \le I_N\xi.                                       \tag{24}
\]

For a mixed word \(w\) avoiding the active color \(h\), pair the local
color \(w_i\) with \(h\) at each vertex. Only the constant complementary
word \(h^\Omega\) survives in the pure part. Its contribution is
\(\tau_hs_h\mathcal H_w\). Multiplication by the monomial \(s_h\)
preserves coefficient norm, proving (21) for mixed words.

For a pure word \(a^\Omega\), pair colors \(a,h\) everywhere. The
pure-part relation is

\[
 \tau_hs_h\mathcal H_{a^\Omega}
       -\tau_as_a\mathcal H_{h^\Omega}
       =\text{error}.
\]

Diagonality means
\(\mathcal H_{a^\Omega}=\sum_{j\ge1}c_js_a^{2j+1}\) and
\(\mathcal H_{h^\Omega}=\sum_{j\ge1}d_js_h^{2j+1}\).
The two terms on the left occupy disjoint parameter monomials:
\(s_a^{2j+1}s_h\) and \(s_as_h^{2j+1}\).
Their norms therefore add. Equation (24) gives
\(|\tau_h|\|\mathcal H_{a^\Omega}\|_1\le I_N\xi\).
This proves the pure case and then (22).

Finally a root-boundary residual is a fixed-color slice of
\(\mathcal E+\mathcal H\), with two root parameters retained. The error
slice has norm at most \(\xi\). There are \(2^{N-1}=2^{n-2}\) remaining
binary receiving words, each controlled by (21). This proves (23).

### Interpretation

For this class, small physical mixed output gives small original higher
responses with explicit dependence on the third pure amplitude. Thus the
fragile general scaling step can be bypassed after literal diagonality
is available.

Section 7 now propagates these errors through matrix covariance.
Theorem 4 still does not permit assuming that a general approximately
correct source is approximately diagonal.

## 7. Quantifying the covariance and divisibility step

Write \(P=(p_1,p_2),Q_c=(q_1,q_2)\). Give a polynomial matrix the sum
of the coefficient norms of its four entries. Let \(T\) be any orthogonally
covariant matrix of parameter degree at most \(2D\). Define its axis map

\[
 \mathcal S(T)=(T_{12}|_{p_1=0},\,T_{12}|_{q_2=0}).   \tag{25}
\]

The kernel of this map consists exactly of matrices
\(aI+bPQ_c^{\mathsf T}\), with invariant polynomial coefficients.
Indeed zero axis restrictions give divisibility by \(p_1q_2\);
covariance gives the other off-diagonal divisibility. The polynomial
matrix lemma in the full proof then applies.

### A bounded projection onto this kernel

The orthogonal invariant theorem gives the following spanning family:

\[
 I\,\sigma^i\rho^jz^k\quad(i+j+k\le D),\qquad
 PP^{\mathsf T},\,Q_cQ_c^{\mathsf T},\,PQ_c^{\mathsf T},\,
 Q_cP^{\mathsf T}
 \quad\hbox{times }\sigma^i\rho^jz^k,\quad i+j+k\le D-1.
\]

To see why this standard theorem gives the matrix statement, append
vectors \(u,v\) and apply the scalar theorem to \(u^{\mathsf T}Tv\).
Terms linear in both appended vectors are \(u\cdot v\) or
\((u\cdot P_i)(v\cdot P_j)\), giving precisely these generators.
This is an application of classical invariant theory, not a new
invariant-ring assertion; see
[Lehrer–Zhang, Section 3](https://arxiv.org/pdf/1102.3221).

Form the coefficient columns of the axis map on this spanning family.
Choose independent columns and an invertible square submatrix of rows.
Invert that submatrix. Composing this inverse with the corresponding
original matrix columns gives a linear map \(J\) satisfying

\[
 \mathcal S(J\mathcal S(T))=\mathcal S(T).
\]

Thus \(T_0=T-J\mathcal S(T)\) has the special matrix form, and

\[
 \|T-T_0\|_1\le C_D\|\mathcal S(T)\|_1,\qquad
 C_D=\|J\|_{1\to1}.                                 \tag{26}
\]

All matrices here are finite rational coefficient matrices. The replay
verifies the defining identity on every generator, computes \(J\)'s
operator norm exactly, and also checks the scalar extraction below.

| \(D\) | Sites \(2D+2\) | Generators | Axis rank | Verified \(C_D\) |
|---|---:|---:|---:|---:|
| 1 | 4 | 8 | 3 | 4 |
| 2 | 6 | 26 | 11 | 8 |
| 3 | 8 | 60 | 26 | 24 |
| 4 | 10 | 115 | 50 | 72 |

These are norms of the specified projections, not optimal projection constants.
For every \(D\ge1\), a completely explicit fallback is

\[
 C_D=4R_D!\,2^{(D-1)R_D},\qquad
 R_D=3\binom{D+2}{3}.                               \tag{27}
\]

For proof, the \(I\) and \(PQ_c^{\mathsf T}\) columns have zero axis
map. There are at most \(R_D\) other columns, each with matrix norm at
most \(4H\), where \(H=2^{D-1}\). Entries of the integer axis matrix
are at most \(H\) in modulus. A nonzero integer minor has determinant
of modulus at least one; the cofactor formula bounds the inverse's
column sums by \(r!H^{r-1}\) for its rank \(r\le R_D\).
This gives \(\|J\|\le4r!H^r\) and hence (27).

### Propagating the actual boundary residuals

For the literal source matrix (10), define

\[
 \begin{aligned}
 R_1&=T_{12}|_{p_1=0},&
 R_2&=T_{12}|_{q_2=0},\\
 R_3&=(\partial_{q_1}T_{12}+dp_1T_{12})|_{q_1=0},&
 R_4&=(\partial_{q_1}T_{22}+dp_1T_{22}-p_1\beta\eta)|_{q_1=0}.
 \end{aligned}                                      \tag{28}
\]

As always, differentiate the full polynomial before restricting it.
For a matrix of the special form, its invariant scalar satisfies

\[
 p_1R_4-p_2R_3
 =p_1^2(\partial_z a+da-\beta\eta)
        (p_1^2+p_2^2,q_2^2,p_2q_2).
\]

Substitute \(p_1=is,p_2=s,q_2=t\).
The negative coefficient of \(s^{j+2}t^j\) is precisely the coefficient
of \(z^j\) in \(r_A\): it selects zero powers of both \(\sigma\) and
\(\rho\). Therefore, for a special-form matrix,
\(\|r_A\|_1\le\|R_3\|_1+\|R_4\|_1\).

For a general \(T\), apply this to \(T_0\) from (26). The extraction
of \(A\) in (11) has norm at most \(1/2\) on matrix coefficients.
Differentiating \(A\) costs at most \(D\).
The operation \((\partial_{q_1}\,\cdot)|_{q_1=0}\) just extracts the
coefficient of \(q_1\), so its coefficient norm is at most one.
Consequently

\[
 \|r_A\|_1\le \|R_3\|_1+\|R_4\|_1
 +\frac{D+2+3|d|}{2}\,C_D(\|R_1\|_1+\|R_2\|_1).
                                                               \tag{29}
\]

Let \(\epsilon_b\) bound the norms of all four source root-boundary
residuals. Denote by \(M_u,M_v,M_Z\) the polynomial tensor norms of
\(E_u(px+qy), E_v(px+qy)\), and
\(Z(px+qy)=E_{uv}(px+qy)+eE(px+qy)\), respectively.
The literal formulas give

\[
 \|R_1\|_1\le\epsilon_b M_v,\quad
 \|R_2\|_1\le\epsilon_b M_u,\quad
 \|R_3\|_1\le\epsilon_b M_v,\quad
 \|R_4\|_1\le\epsilon_b M_Z.                         \tag{30}
\]

For example \(R_1\) pairs \(E_u(q_1y)\), a boundary residual, with
\(E_v(p_2x+q_2y)\). For \(R_3\), differentiating the first boundary
residual in its second parameter at zero gives
\(E_{yu}(p_1x)+dp_1E_u(p_1x)\).
For \(R_4\), use that the pure-\(H\) coefficient of \(Z\) is exactly
\(\eta\) for every source: positive \(B\)-mean insertions cannot
contribute to that word. These observations prove (30).

Set \(N=2D\) and \(W_N=4^N I_N\).
When each edge weight has modulus at most one, direct partial-matching
counts give

\[
 M_u,M_v\le N W_N,\qquad M_Z\le[N(N-1)+1]W_N.
\]

There are \(2^N\) receiving words, at most \(I_N\) partial matchings
per word, and at most \(2^N\) mean coefficients per term.
One or two differentiated singleton slots add factors at most \(N\)
or \(N(N-1)\). Also \(|e|\le1\).
Using \(|d|\le1\) in (29) yields the explicit transfer:

\[
 \boxed{\|r_A\|_1\le B_D\epsilon_b,\qquad
 B_D=W_N[N^2+1+N(D+5)C_D].}                         \tag{31}
\]

The source-specific factors in (30) often give much better constants.
Equations (23) and (31) complete the physical-error-to-endpoint-residual
bridge for literal diagonal three-color sources.

## 8. A global rate bound for diagonal complex sources

This step also removes a fixed lower bound on nonzero edge weights.
Small edges are retained in all source equations. A comparison with
the larger-edge subgraph is used only to bound output contributions;
no claim that deletion preserves the target equations is made.

Let \(n=2m>4\), \(D=m-1\), and normalize the diagonal three-color source
by \(S=\sum_{p<q,h}|A_{pq}(h,h)|^2=1\). Define

\[
 \Delta=a^n+b^n+c^n,\quad
 \lambda=(H_{a^n}+H_{b^n}+H_{c^n})/3,\quad
 E=H-\lambda\Delta,\quad \ell=|\lambda|,\quad
 \epsilon=\|E\|_2.
\]

For nonzero output, \(R=\|H\|_2^2\) in this normalization, and

\[
 F=\frac{3\ell^2}{R},\qquad
 \epsilon^2=(1-F)R.
\]

Let

\[
 \begin{aligned}
 P&=(n-1)!!,& P_{\rm core}&=(n-3)!!,\\
 A_n&=2^{n-2}I_{n-1},&
 K_n&=B_D\,3^m(P+2A_n),\\
 Q_n&=2[K_nD!+P_{\rm core}P],&
 c_n&=\frac1{256(1+Q_n)(64P^2)^D},\\
 k_n&=3+\frac{3D}{2},&
 \alpha_n&=\frac1{k_n-1}=\frac4{3n+2}.
 \end{aligned}                                      \tag{32}
\]

Use any valid \(C_D\) in (31), including the exact table above or (27).
All constants in (32) are explicit; \(c_n\) is positive and rational.

**Theorem 5 (global diagonal bound).** If \(F\ge12/13\), then

\[
 \boxed{\epsilon\ge c_n\ell^{k_n},\qquad
 R\le
 \left(\frac{3^{k_n}}{c_n^2}\right)^{\alpha_n}
 \frac{(1-F)^{\alpha_n}}{F^{1+\alpha_n}}.}           \tag{33}
\]

For an unnormalized source, use
\(R=\|H\|^2/S^m\); rescaling to \(S=1\) leaves \(F,R\) unchanged.
There is no assumption of nonnegative weights, minimum nonzero weight,
fixed support, nonzero response rank, or proximity to the prism.
Literal diagonality is required.

### Proof

The fidelity floor implies
\(\epsilon/\ell=\sqrt{3(1-F)/F}\le1/2\).
Each pure amplitude therefore has modulus at least \(\ell/2\).
Also \(\ell\le P\), by the pure matching expansion and the individual
edge-weight bound \(|A_{pq}(h,h)|\le1\).

Equations (20), (23), and (31) give, for every ordered color pair and
root pair,

\[
 \|r_A\|_1
 \le B_D3^m\epsilon(1+2A_n/\ell)
 \le K_n\epsilon/\ell.                             \tag{34}
\]

Each retained matching tensor has norm at most one under \(S=1\),
so \(\|F\|\le P_{\rm core}\). Equations (9) and (15) show that an edge
of modulus at least \(\kappa\), where \(0<\kappa\le1\), has endpoint
defect at most

\[
 |\beta-d\alpha|
 \le Q_n\kappa^{-D}\epsilon/\ell^2.                 \tag{35}
\]

We used \(|\eta|\ge\ell/2\), \(J_D(d)\le D!\kappa^{-D}\),
\(|d|\le1\), \(\|W\|\le\epsilon\), and \(\ell\le P\).

Suppose for contradiction that \(\epsilon<c_n\ell^{k_n}\), and set

\[
                  \kappa=\frac{\ell^{3/2}}{64P^2}.  \tag{36}
\]

Call an edge heavy if its modulus is at least \(\kappa\).
Then \(\kappa<1\), \(P\kappa\le\ell/64\), and (35) gives a defect
less than \(\ell/256\) on every heavy edge.

At a vertex of a color graph, let \(k\) be its number of heavy neighbors.
The total contribution of light edges in its hafnian expansion has modulus
at most \(P\kappa\): there are at most \(n-1\) terms, each with retained
pure cofactor at most \(P_{\rm core}\).
Writing each heavy contribution as \(\beta-\text{defect}\) gives

\[
 (k-1)\beta=\text{sum of heavy defects}
                    -\text{light contribution}.
\]

If \(k=0\), this contradicts \(|\beta|\ge\ell/2\).
If \(k\ge2\), it would imply
\((k-1)\ell/2<k\ell/256+\ell/64\), also impossible.
Thus each color's heavy edges form a perfect matching.

A different perfect matching of the same color differs from this heavy
matching in at least two edges. Both differing edges are light, so its
contribution has modulus at most \(\kappa^2\). If \(t_h\) is the product
of the heavy color-\(h\) matching, then

\[
 |t_h|\ge|\tau_h|-P\kappa^2\ge\ell/4.               \tag{37}
\]

Here \(P\kappa^2=\ell^3/(4096P^3)\le\ell/4096\),
using \(\ell\le P\) and \(P\ge1\).

The three heavy matchings have a mixed perfect matching for \(n>4\):
if two share a physical pair, choose that pair in one color and the
rest of the other matching; otherwise use the graph lemma in the full
proof. Let \(w\) be its mixed receiving word and \(t_w\) its product.
Its colored edges are a subset of the three pure heavy matchings.
Every complementary edge has modulus at most one, hence

\[
 |t_w|\ge |t_a t_b t_c|\ge\ell^3/64.
\]

There is only one all-heavy matching for \(w\), since each vertex has
one heavy edge of its requested color. Any other compatible matching
differs in at least two edges, both light. Parallel edges have already
been aggregated. Consequently

\[
 |H_w|\ge |t_w|-P\kappa^2
       \ge\ell^3(1/64-1/4096)>\ell^3/128.            \tag{38}
\]

But the assumed error bound gives

\[
 \epsilon<c_n\ell^{k_n}
 \le c_nP^{2D}\ell^3\le\ell^3/256,
\]

because \(3D/2\le2D\), \(\ell\le P\), and (32) has the stated
denominator. Equation (38) contradicts \(|H_w|\le\epsilon\).
This proves the first assertion of (33).

Finally \(\epsilon^2=(1-F)R\) and
\(\ell^2=FR/3\) give
\(R^{k_n-1}\le3^{k_n}(1-F)/(c_n^2F^{k_n})\),
which is exactly the second assertion.

### Explicit small-size values and interpretation

| Sites | Amplitude power \(k_n\) | Rate exponent \(\alpha_n\) |
|---|---:|---:|
| 6 | 6 | \(1/5\) |
| 8 | \(15/2\) | \(2/13\) |
| 10 | 9 | \(1/8\) |

Using the verified six-site projection constant \(C_2=8\) gives

\[
 B_2=616960,\quad Q_6=56437033050,\quad
 c_6=\frac1{2995912492404572160000}.
\]

These constants are intentionally loose and do not provide a sharp
experimental prediction. The substantive gain is a specified exponent
for every complex diagonal architecture, including vanishing-edge and
zero-output limits. The previously proved local prism exponent \(1/2\)
is stronger on its smaller domain. Neither result establishes a sharp
global exponent for complex sources.

## 9. What remains

The diagonal physical-error chain is now complete: original higher
responses, root boundaries, matrix covariance, the endpoint scalar,
and a controlled comparison with three matchings. The proof permits
arbitrarily small nonzero weights and does not assume rank stability.

The main remaining generalization is a quantitative reduction from
arbitrary endpoint-color matrices to the diagonal setting. The exact
cofactor inverse does not automatically supply a uniform approximate
reduction near zero output. Theorem 1 gives a controlled version of one
needed polynomial step, but that general source-to-diagonal argument
has not been completed.

Sharper exponents and much smaller constants are also open. In particular,
the square-root law has not been proved globally for complex diagonal
sources, although it is known in the earlier local prism theorem.

Separately, the all-orders exclusion extends the existing
[Nullstellensatz existence argument](universal-rate-bound-feasibility-2026-09-26.md#2-a-universal-power-law-exists-for-arbitrary-complex-sources)
to every fixed even \(n>4\), including arbitrary endpoint colors.
That existence argument still supplies no comparable useful explicit
exponent for the general model. None of the isolated scaling exponents
in Section 2 should be substituted into a physical rate statement.

## 10. Reproducibility

From the repository root:

    python3 computations/quantitative-proof-identities-2026-09-26/verify.py

The checker uses exact rational and Gaussian-rational arithmetic. It checks
finite inverses, sharp norm examples, formal logarithms, truncated-exponential
controls, and literal partial-matching kernels on four, six, and eight sites.
It additionally verifies the complete finite covariance projections through
ten sites, scalar ODE extraction on every generator, all displayed rate
constants, and the error budgets used in the heavy/light comparison.
The four-site allowed source, zero-edge boundary, and binary-only negative
control remain explicit. The saved output pins this note and the checker.

Finite checks validate formulas, conventions, and examples. The
dimension-independent bounds and arbitrary-size certificate are justified
by the written arguments above, pending independent mathematical audit.
