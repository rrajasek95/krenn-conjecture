# A sharp six-site hafnian norm bound and an unbounded stationary slack family

## 1. Outcome

There is a sharp Frobenius inequality for a scalar hafnian on six sites.  If

\[
 p(x)=\operatorname {haf}(x),\qquad
 S(x)=\sum_{e\in\binom{[6]}2}|x_e|^2,
\]

then

\[
 \boxed{\quad |p(x)|\le {S(x)^{3/2}\over\sqrt {15}}.\quad}       \tag{1}
\]

Apart from the zero point, equality holds precisely on the vertex-gauged
complete graph

\[
                    x_{uv}=r\,\zeta_u\zeta_v,
 \qquad r>0,\quad |\zeta_v|=1.                                \tag{2}
\]

Consequently, the three diagonal scalar slices of a hypothetical six-site
ternary equality source have total squared energy strictly greater than

\[
                              3\sqrt[3]{15}.                  \tag{3}
\]

The strict inequality does **not** furnish the missing variational
contradiction.  In fact, Sections 5--8 give an exact algebraic family with
all three complete pure coefficients equal to one, full isotropy, injective
star and triangle maps, and only the five universal gauge directions in the
full derivative kernel, while each of the three pure-slice energies tends to
infinity.  Every generic member is a smooth local norm minimum in the fiber
of its own output.  Thus balance and all presently available block normal
equations cannot force equality in (1).  The family is not a GHZ preimage:
one displayed mixed coefficient is nonzero.  Any positive norm argument
must use the simultaneous vanishing of the remaining mixed coefficients.

The exact audit is
`computations/verify_six_site_hafnian_norm_slack.py`.

## 2. The cofactor-square inequality

For an edge `e`, put

\[
                   h_e=\operatorname {haf}(x[[6]\setminus e]),
 \qquad Q(x)=\sum_e|h_e|^2.                                \tag{4}
\]

Thus `h_e` is a sum of the three products belonging to the three pairings
of the four vertices outside `e`.

**Lemma 2.1.**  For arbitrary complex edge weights on `K_6`,

\[
                         Q(x)\le {3\over5}S(x)^2.           \tag{5}
\]

If equality holds and `x` is nonzero, all fifteen entries of `x` are
nonzero and have one common magnitude.

**Proof.**  Write `r_e=|x_e|`.  Let `D` be the set of the 45 unordered
pairs of disjoint edges of `K_6`.  Let `C` be the following set of 45
four-cycles: choose an omitted edge `e`; on the other four vertices choose
two of their three perfect matchings, whose union is a four-cycle.  Expanding
the squares in (4) and applying the triangle inequality only to the cross
terms gives

\[
 Q(x)\le
 \sum_{\{f,g\}\in D}r_f^2r_g^2
 +2\sum_{C\in\mathcal C}\prod_{f\in C}r_f.                 \tag{6}
\]

For one four-cycle with cyclic edge magnitudes `z_1,z_2,z_3,z_4`, weighted
AM--GM gives

\[
\begin{split}
 2z_1z_2z_3z_4\le{}&{1\over20}\sum_i z_i^4
   +{2\over5}\sum_i z_i^2z_{i+1}^2\\
 &+{1\over10}(z_1^2z_3^2+z_2^2z_4^2).                    \tag{7}
\end{split}
\]

Indeed, after multiplication by 20, the right side consists of 40
monomials counted with multiplicity: four fourth powers, eight copies of
each of the four adjacent-pair squares, and two copies of each of the two
opposite-pair squares.  The total exponent of each `z_i` is 40, so their
geometric mean is `z_1z_2z_3z_4`.

In the 45 cycles, each edge occurs 12 times, each adjacent edge pair occurs
three times, and each disjoint edge pair occurs twice.  Summing (7) therefore
gives

\[
 2\sum_{C\in\mathcal C}\prod_{f\in C}r_f
 \le {3\over5}\sum_f r_f^4
    +{6\over5}\sum_{f\sim g}r_f^2r_g^2
    +{1\over5}\sum_{\{f,g\}\in D}r_f^2r_g^2.             \tag{8}
\]

Adding the first term of (6), and using

\[
 S^2=\sum_f r_f^4+2\sum_{f\sim g}r_f^2r_g^2
                    +2\sum_{\{f,g\}\in D}r_f^2r_g^2,
\]

proves (5).

All inequalities in the sum are between nonnegative quantities.  If (5)
is an equality and some `r_f` is positive, every cycle containing `f` must
be an equality case of (7).  Its right side contains `r_f^4`, so all four
cycle entries are positive; equality in weighted AM--GM makes their
magnitudes equal.  Any two edges of `K_6` occur together in one of the
cycles in `C` (as adjacent or opposite edges).  Hence all fifteen
magnitudes are equal. `QED`

The incidence counts used above are exhaustively checked by the audit, but
they also follow immediately as follows.  A fixed edge has six choices of
an omitted disjoint edge and lies in two of the three cycle unions on the
remaining four-set, giving 12.  A fixed adjacent pair has three choices for
the fourth cycle vertex.  A fixed disjoint pair determines the omitted edge
and can be paired with either of the other two perfect matchings, giving two.

## 3. The sharp hafnian inequality and its equality case

**Theorem 3.1.**  Inequality (1) holds.  Its nonzero equality cases are
exactly (2).

**Proof.**  Euler's identity for the cubic hafnian is

\[
                         3p(x)=\sum_e x_eh_e.              \tag{9}
\]

Cauchy--Schwarz and Lemma 2.1 give

\[
 3|p(x)|\le S(x)^{1/2}Q(x)^{1/2}
          \le \sqrt{3/5}\,S(x)^{3/2},                    \tag{10}
\]

which is (1).

Suppose equality holds and `x` is nonzero.  Lemma 2.1 first makes all
fifteen magnitudes equal.  Equality in (6) says that, on every four-set,
the products belonging to its three pairings have one common phase.
Equality in Cauchy--Schwarz says that the quantities `x_eh_e` have one
common phase.  Hence all fifteen perfect-matching monomials of `p(x)` have
one common phase.

Write `x_e=r z_e`, where `|z_e|=1`.  Comparing the three perfect matchings
which use a fixed pairing of four vertices and the common edge on the other
two vertices gives, for every four distinct vertices,

\[
                 z_{ab}z_{cd}=z_{ac}z_{bd}=z_{ad}z_{bc}.  \tag{11}
\]

The four-point equations imply `z_{uv}=\zeta_u\zeta_v`.  For completeness,
fix vertices 0 and 1.  Equation (11) shows that
`z_(1v)/z_(0v)=K` is independent of `v notin {0,1}`, and then

\[
 z_{uv}={K\over z_{01}}z_{0u}z_{0v}\qquad(u,v\ne0,1).
\]

Taking `C=K/z_(01)`, `eta_0=C^{-1}`, `eta_1=z_(01)`, and
`eta_u=z_(0u)` for the other vertices gives `z_(uv)=C eta_u eta_v` on
every edge.  Absorb a square root of `C` into all the `eta_u`; all factors
may be chosen unimodular.  This proves (2).  Conversely, (2) makes all
fifteen matching monomials equal, and direct substitution gives equality in
(1). `QED`

The same scalar estimate immediately implies the Hilbert-valued bound

\[
 \left\|\sum_{M\in\operatorname {PM}(6)}
                   \bigotimes_{e\in M}A_e\right\|
 \le {1\over\sqrt {15}}
       \left(\sum_e\|A_e\|^2\right)^{3/2},                \tag{12}
\]

by the triangle inequality followed by (1) with `x_e=||A_e||`.

## 4. A strict diagonal-energy floor for ternary equality

Let arbitrary `3 by 3` aggregate matrices `A_e` satisfy

\[
                         H_6(A)=\Delta_{6,3}.              \tag{13}
\]

For each color `i`, put `x_e^i=A_e(i,i)` and
`S_i=sum_e|x_e^i|^2`.  The constant-color coefficient in (13) says
`haf(x^i)=1`.  Theorem 3.1 gives

\[
                              S_i\ge\sqrt[3]{15}.          \tag{14}
\]

Thus the full source energy is at least `3 root(3)(15)`.  Equality is
impossible.  Indeed, equality would make every off-diagonal matrix entry
zero and put every scalar slice in (2), in particular with all entries
nonzero.  Color the endpoints of any partition of the six vertices into
three pairs by colors 0, 1, and 2 respectively.  Diagonality makes the
three named pairs the unique compatible perfect matching, and its product
is nonzero.  This is a forbidden mixed coefficient.  Therefore

\[
             \boxed{\quad \|A\|_F^2>3\sqrt[3]{15}.\quad}  \tag{15}
\]

This is an unconditional consequence of all GHZ equations, but it is only
a lower bound.  Norm minimality supplies no comparison point in the
hypothetical exact fiber which would turn (15) into a contradiction.

## 5. An algebraic family with unbounded pure-slice slack

Use the five one-factors

\[
\begin{aligned}
 P&=01|23|45,&P'&=05|12|34,\\
 Q_0&=02|14|35,&Q_1&=03|15|24,&Q_2&=04|13|25.             \tag{16}
\end{aligned}
\]

They partition all edges of `K_6`.  Put

\[
 N=\begin{pmatrix}
 1&-2/3&2\\2&1&-2/3\\-2/3&2&1
 \end{pmatrix},
 \qquad NN^{\mathsf T}=N^{\mathsf T}N={49\over9}I_3.     \tag{17}
\]

Give the three edges `01,12,23` sign `-1` and every other edge sign `+1`;
write the resulting sign as `sigma_e`.  Choose `a>0`, and let `b=b(a)>a`
be the unique positive solution of

\[
                              b^3-a^2b=1.                 \tag{18}
\]

Existence and uniqueness follow because the left side minus one is `-1` at
`b=a`, is increasing for `b>a`, and tends to infinity.  Define

\[
 A_e=\begin{cases}
       \sigma_e aN,&e\in P\cup P',\\
       bE_{ii},&e\in Q_i.
      \end{cases}                                        \tag{19}
\]

Every full matrix in (19) has all nine entries nonzero.  Hence `P` and
`P'` give two supported monomials in every coloring, while the `Q_i` give
coordinate anchors at every port.

## 6. Exact pure normalization and isotropy

For a fixed color `i`, the pure support is `P union P' union Q_i`.  It has
exactly four perfect matchings: those three factors and

\[
\begin{aligned}
 H_0&=05|14|23,&H_1&=03|12|45,&H_2&=01|25|34.             \tag{20}
\end{aligned}
\]

The sign products on `P,P',Q_i,H_i` are respectively `+,-,+,-`.  Since the
diagonal of `N` is `(1,1,1)`, the complete pure coefficient is

\[
                    a^3-a^3+b^3-a^2b=1.                  \tag{21}
\]

Thus all three constant-color equations are normalized exactly.

At every vertex there is one incident edge from each factor.  Equation
(17) gives, at either endpoint,

\[
 R_v(A)=2a^2{49\over9}I_3+b^2\sum_iE_{ii}
       =\left({98\over9}a^2+b^2\right)I_3.               \tag{22}
\]

The family is therefore fully isotropic, not merely diagonally balanced.
Its pure color-`i` scalar energy and its full source energy are

\[
 S_i=6a^2+3b^2,\qquad
 \|A\|_F^2=98a^2+9b^2.                                  \tag{23}
\]

Both tend to infinity with `a`.  Thus the slack in (14) is unbounded under
the pure equations and full moment-map equations.

The model also contains genuine cancellation equations.  For example, the
mixed coefficient at `000111` vanishes identically: its two terms are
`-2a^3/3` and `+2a^3/3`.  On the other hand,

\[
                       [e_{000001}]H_6(A)={2\over3}a^2b\ne0, \tag{24}
\]

so (19) is not falsely advertised as a GHZ preimage.

## 7. All exact-linear block equations are vacuous generically

For `a=1`, let `beta` be the positive root of

\[
                              \beta^3-\beta-1=0.          \tag{25}
\]

The verifier reduces the source (19) modulo 19 by the valid specialization
`beta -> 6`; indeed `6^3-6=1 mod 19`.  Exact Gaussian elimination gives

\[
\begin{array}{c|c|c}
\text{block}&\text{number of columns}&\text{rank over }\mathbf F_{19}\\\hline
\text{each of six stars}&45&45\\
\text{each of twenty triangles}&27&27\\
\text{all fifteen edges}&135&130.
\end{array}                                               \tag{26}
\]

A nonzero minor after reduction is a nonzero minor over
`Q(beta) subset C`.  Thus every star and triangle map is injective at this
exact algebraic point.  Their least-norm block equations impose no further
condition.  The full derivative has the smallest possible kernel: its five
dimensions are exactly

\[
 X_{uv}=(p_u+p_v)A_{uv},\qquad \sum_vp_v=0.               \tag{27}
\]

The same conclusions hold for all but finitely many points of (18).  To
justify the generic statement, the curve
`b^3-a^2b-1=0` is irreducible: over `C(b)` it would factor as a quadratic in
`a` only if `(b^3-1)/b` were a square, which its simple zeros and pole rule
out.  Each nonzero minor selected at (25) restricts to a nonzero regular
function on this irreducible curve and consequently has only finitely many
zeros.  There are finitely many selected blocks.  Since the positive real
branch in (18) is unbounded, it contains arbitrarily large points at which
all ranks in (26) persist.

## 8. Smooth local norm minimality and the exact boundary of the route

At a generic point from Section 7, select 130 output coordinates with
independent differentials.  Their fixed level set is a smooth
five-dimensional manifold near `A`.  The scalar vertex-gauge orbit (27) is
contained in that level set and has the same tangent dimension, so it is an
open neighborhood in the local fixed-output fiber.

Along the real part of that orbit, write `|lambda_v|=exp(p_v)` with
`sum_v p_v=0`.  Its norm is

\[
 f(p)=\sum_{u<v}e^{2(p_u+p_v)}\|A_{uv}\|_F^2.             \tag{28}
\]

Full isotropy makes every weighted vertex degree equal, so `p=0` is a
critical point.  Moreover

\[
 D^2f(0)[p,p]=4\sum_{u<v}(p_u+p_v)^2\|A_{uv}\|_F^2>0     \tag{29}
\]

for nonzero real `p` of zero sum; all fifteen matrices in (19) are nonzero.
Phase gauges preserve the norm.  Hence these points are smooth local norm
minima in their own exact fibers, modulo compact phases.

This family proves the precise negative statement needed for the norm
route: pure normalization, strict squared-incidence balance, full isotropy,
all star/triangle least-norm equations, gauge-only infinitesimal rigidity,
support multiplicity, coordinate anchors, and even some exact mixed
cancellations do not bound the slack in (1), let alone force equality.
What the family omits is exactly the full set of GHZ mixed equations.  A
successful continuation has to derive a new global identity from their
simultaneous vanishing; no presently available moment-map or block-normal
equation supplies it.

## 9. Scope at larger even order

The natural proposed extension of (1) to `n=2m` is

\[
 |\operatorname {haf}(x)|\stackrel{?}{\le}
 { (2m-1)!!\over [m(2m-1)]^{m/2}}
 \left(\sum_e|x_e|^2\right)^{m/2},                       \tag{30}
\]

with the dense vertex-gauged matrix as equality case.  Formula (30) is
sharp if true, and it agrees with the elementary four-site bound and
Theorem 3.1.  The proof above does not establish (30) for `m>=4`: after one
cofactor differentiation, pairs of complementary matchings can have
several longer alternating-cycle types, whereas the six-site proof has only
the single four-cycle allocation (7).  Accordingly, (30) is recorded here
only as a candidate inequality, not used as a lemma or as part of any
obstruction.

