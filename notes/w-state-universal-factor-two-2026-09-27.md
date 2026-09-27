# A universal factor-two guarantee for exact W-state design

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted global optimum is not established.

[Exact replay](../computations/w-universal-factor-two-2026-09-27/README.md) ·
[Illustrated guide](../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../research/w-state-design/README.md)

## 1. The unrestricted result

Let $n=2m\ge4$, and allow arbitrary complex colored entries on every edge.
Suppose the matching output is exactly $\lambda W_n\ne0$, with
$W_n=\sum_i|a\cdots b_i\cdots a\rangle$.
For total squared source strength $S$, put

$$
R=\frac{n|\lambda|^2}{S^m},\qquad
B_n=\frac{((n-1)!!)^2}{\binom n2^{\,m}}.
$$

**Theorem.** Every such source satisfies

$$
\boxed{R\le U_n:=\frac{2B_n}{n}.}
\tag{1}
$$

There is no support, phase, block-rank, or local-neighborhood restriction.
In particular, supported ground perfect matchings may cancel.

The [known one-root construction](w-state-optimal-design-2026-09-26.md)
attains $R_*=nB_n/((n-1)^2+1)$. Consequently the unrestricted optimal
rate obeys

$$
R_*\le R_{\rm opt}\le
\frac{2((n-1)^2+1)}{n^2}R_*<2R_*.
\tag{2}
$$

Thus the explicit design achieves more than half the best possible rate
at every even count, with the sharper size-dependent guarantee
$R_*/R_{\rm opt}\ge n^2/[2((n-1)^2+1)]$.
This is a global approximation guarantee, not an exact global optimum.

| Sites | Attained $R_*$ | New unrestricted upper bound $U_n$ | Upper bound divided by attained rate |
| --- | ---: | ---: | ---: |
| 4 | $1/10$ | $1/8$ | $5/4$ |
| 6 | $1/65$ | $1/45$ | $13/9$ |
| 8 | $9/3136$ | $225/50176$ | $25/16$ |
| 10 | $49/83025$ | $49/50625$ | $41/25$ |
| 12 | $3675/28579232$ | $1225/5622144$ | $61/36$ |

At six sites this improves the earlier unrestricted $4/135$ upper
bound by 25%. The four-site upper bound is unchanged.

## 2. A general derivative bound at a polynomial zero

The useful ingredient is not specific to hafnians.
Let $P$ be a homogeneous holomorphic polynomial of degree $m\ge2$
on a finite-dimensional complex Euclidean space, satisfying

$$
|P(z)|^2\le B\|z\|^{2m}\quad\text{for every }z.
\tag{3}
$$

Use the holomorphic derivative vector
$g(z)=(\partial P/\partial z_j)_j$, without a factor of two.

**Lemma.** If $P(z)=0$, then

$$
\boxed{\|g(z)\|^2\le
\frac{m^m}{(m-1)^{m-1}}B\|z\|^{2m-2}.}
\tag{4}
$$

This constant is sharp for the class of all such polynomials.

### Proof

By homogeneity it suffices to take $\|z\|=1$. The zero vector and
the case $g(z)=0$ are immediate. Otherwise put
$v=\overline{g(z)}/\|g(z)\|$. Euler's identity gives
$\sum_j z_jg_j(z)=mP(z)=0$, hence $\langle z,v\rangle=0$.
Thus

$$
\|z+t e^{i\theta}v\|^2=1+t^2,\qquad
P(z+t e^{i\theta}v)=
\sum_{j=1}^m a_j t^j e^{ij\theta},
\quad a_1=\|g(z)\|.
$$

Average the squared modulus over the circle. Different powers
$e^{ij\theta}$ are orthogonal, so (3) implies

$$
t^2\|g(z)\|^2
+\sum_{j=2}^m|a_j|^2t^{2j}
\le B(1+t^2)^m.
\tag{5}
$$

Discard the nonnegative higher terms and set $t^2=1/(m-1)$.
This minimizes $(1+t^2)^m/t^2$, proving (4).

For sharpness take $P(z_1,z_2)=z_1^{m-1}z_2$.
Its squared maximum on the unit sphere is
$(m-1)^{m-1}/m^m$, by elementary one-variable maximization.
At $(1,0)$ it vanishes and its derivative norm is one.
Equality holds in (4). ∎

The argument is elementary complex analysis. No claim of priority for
this general polynomial lemma is made.

## 3. A sharp cofactor bound on the entire zero-hafnian set

Let $D$ be an arbitrary complex symmetric ground matrix, indexed by
its independent unordered edges. Set

$$
a=\sum_{i<j}|D_{ij}|^2,\qquad
C_{ij}=\operatorname{haf}(D[V\setminus\{i,j\}]),\qquad
T=\sum_{i<j}|C_{ij}|^2.
$$

The established scalar hafnian norm inequality is

$$
|\operatorname{haf}(D)|^2\le B_n a^m.
\tag{6}
$$

It follows from [Roos, Theorem 2.3 and equations (40), (42)](https://arxiv.org/html/1906.06176).
The factor $n(n-1)$ there counts ordered matrix entries; converting
to the unordered edge norm gives exactly $B_n$ above.

The hafnian is homogeneous of degree $m$, and its derivative with
respect to the independent edge $D_{ij}$ is $C_{ij}$. Applying
(4) gives

$$
\boxed{\operatorname{haf}(D)=0
\quad\Longrightarrow\quad
T\le K_n a^{m-1},\qquad
K_n=B_n\frac{m^m}{(m-1)^{m-1}}.}
\tag{7}
$$

Unlike the earlier odd-core response bound, this holds on the whole
zero-hafnian set, with arbitrary complex cancellation.

It is sharp for every even $n$: take a complete unit-weight core
on $N=n-1$ sites and an isolated site. With $q=m-1$ and
$c=(n-3)!!$,

$$
a=Nq,\qquad C_{0i}=c,\qquad C_{ij}=0\ (i,j\ne0),
\qquad T=Nc^2=K_n(Nq)^q.
$$

At six sites, (7) is $T\le(9/20)a^2$.

## 4. Derive the W-rate bound

For an exact W source the all-ground output vanishes, so (7) applies.
Define the squared cofactor row norms and their reciprocal sum:

$$
r_i^2=\sum_{j\ne i}|C_{ij}|^2,\qquad
\beta=\sum_i r_i^{-2}.
$$

Every row is nonzero because its single-excitation output is $\lambda$.
Those output equations give the
[unrestricted response bound](w-state-unrestricted-response-bound-2026-09-27.md):

$$
S\ge a+|\lambda|^2\beta,\qquad
R\le\frac{n(m-1)^{m-1}}{m^m a^{m-1}\beta}.
\tag{8}
$$

Each unordered cofactor occurs in two rows. Cauchy--Schwarz and
(7) therefore give

$$
\beta\ge\frac{n^2}{\sum_i r_i^2}
=\frac{n^2}{2T}
\ge\frac{n^2}{2K_n a^{m-1}}.
$$

Insert this in (8). The factors $m^m/(m-1)^{m-1}$ cancel exactly,
leaving $R\le2B_n/n$. This proves (1).
All omitted colored entries only add source strength; the derivation
does not restrict them.

## 5. Keep the two losses separate

The bound can be refined using quantities computed from the ground
source alone:

$$
\eta=\frac{T}{K_n a^{m-1}}\le1,\qquad
\xi=\frac{2T\beta}{n^2}-1
=\frac1{n^2}\sum_{i<j}
\frac{(r_i^2-r_j^2)^2}{r_i^2r_j^2}\ge0.
$$

Then

$$
\boxed{R\le U_n\,\frac{\eta}{1+\xi}.}
\tag{9}
$$

Here $\eta$ measures cofactor efficiency and $\xi$ measures imbalance
between the cofactor rows. At the known construction,

$$
\eta=1,\qquad \xi=\frac{(n-2)^2}{n^2},
$$

and (9) gives exactly $R_*$. Consequently a source beating $R_*$
would necessarily satisfy both

$$
\xi<\frac{(n-2)^2}{n^2},\qquad
\eta>\frac{n^2(1+\xi)}{2((n-1)^2+1)}.
\tag{10}
$$

Its responses must be more uniform than those of the known design
while retaining sufficient total strength. At six sites these
requirements are $\xi<4/9$ and $\eta>(9/13)(1+\xi)$.

The circle argument gives an additional exact diagnostic.
For $T>0$, expand

$$
\operatorname{haf}(D+s\overline C)=\sum_{j=0}^m d_j s^j.
$$

Then $d_0=0$, $d_1=T$, and
$\sum_{i<j}\overline{D_{ij}}\,\overline{C_{ij}}=0$.
Apply the same circle average with $|s|^2=a/((m-1)T)$.
It yields

$$
T+\sum_{j=2}^m
\frac{|d_j|^2a^{j-1}}{(m-1)^{j-1}T^j}
\le K_n a^{m-1}.
\tag{11}
$$

The higher coefficients therefore give a certified reduction in
$\eta$ whenever they are nonzero. Sharp cofactor efficiency forces
every one of them to vanish. This is not a classification of all
equality sources.

## 6. Weighted W targets

For $H=\lambda\sum_i w_i|a\cdots b_i\cdots a\rangle\ne0$,
replace $\beta$ by $\beta_w=\sum_i |w_i|^2/r_i^2$.
A required nonzero weight needs a nonzero row; zero weights contribute
zero, including on zero rows. Weighted Cauchy--Schwarz gives

$$
\beta_w\ge\frac{(\sum_i|w_i|)^2}{2T}.
$$

The same optimization and (7) prove the unrestricted bound

$$
\boxed{R\le 2B_n\,
\frac{\sum_i|w_i|^2}{(\sum_i|w_i|)^2}.}
\tag{12}
$$

One may also take the minimum with $B_n$. Indeed the triangle
inequality bounds the norm of any matching tensor by the scalar
hafnian of the edge-block norms, and (6) bounds its square by
$B_n S^m$. Neither weighted bound is claimed optimal.

## 7. What remains

The exact unrestricted all-even optimum still requires closing the
factor in (2). One sufficient scalar route is to prove

$$
\eta\le
\frac{n^2}{2((n-1)^2+1)}(1+\xi).
$$

At six sites this is precisely the earlier open harmonic-response
inequality, now decomposed into strength and imbalance.
At four sites that scalar statement is false, so the equations
suppressing multiple excitations must enter.

The present argument establishes a uniform global approximation
guarantee and a sharp unrestricted zero-hafnian derivative bound.
It does not certify an exact global W optimizer, classify every
equality case, or prove the GHZ square-root rate law.
