# Torus osculation: exact first jets and a uniform top-half countermodel

## Outcome

Uniform scaling of one target colour gives a clean osculating filtration,
but the extremal-to-middle half of that filtration does not force a ternary
contradiction or a six-site realization.

There are two exact conclusions.

1. At the pure endpoint, `c^m/m!=X_2` says only that one scalar hafnian is
   one.  The first osculating equation is one independent cofactor-row
   equation at each site and for each of the other two colours.  Its kernel
   has dimension exactly `n-2` per row.  If all two-hole cofactors of `c`
   are nonzero, the second osculating equation then determines every binary
   cell of `a` independently.  The first cross-pair compatibility occurs at
   order three, not order two.
2. For every `n=2m>=6`, there is a unit-weight diagonal source

   \[
                             q(t)=a+t^2c
   \]

   such that `H(a)=X_0+X_1`, `H(c)=X_2`, every principal two-colour face is
   exact, and every reversed osculating coefficient from the pure endpoint
   through order `m` vanishes.  Nevertheless the full tensor has explicit
   singleton genuinely ternary errors, beginning in original `t`-degree
   two.

Thus a top-down argument must cross the middle and meet genuinely ternary
low-degree equations.  The construction is a diagnostic countermodel, not
a realization of ternary equality.

## 1. The exact torus expansion

Let `n=2m`, use local variables `x_i,y_i,z_i`, and work in the squarefree
site algebra

\[
 \mathcal R=\mathbb C[x_i,y_i,z_i:i\in B]/
 (u_iv_i:u_i,v_i\in\{x_i,y_i,z_i\}).                     \tag{1}
\]

For a quadratic source `q`, put

\[
                              H(q)=\frac{q^m}{m!}.         \tag{2}
\]

Split `q` according to the number of `z` endpoints on one source cell:

\[
                              q(t)=a+t b+t^2c.             \tag{3}
\]

Here `a,b,c` have respectively zero, one, and two `z` labels.  A hypothetical
ternary realization would give

\[
 H(q(t))=X_0+X_1+t^{2m}X_2,                              \tag{4}
\]

where `X_r` is the constant colour-`r` tensor.  The coefficient of `t^d` is

\[
 E_d(a,b,c)=
 \sum_{j=\max(0,d-m)}^{\lfloor d/2\rfloor}
 \frac{a^{m-d+j}b^{d-2j}c^j}
 {(m-d+j)!(d-2j)!j!}.                                    \tag{5}
\]

Thus `E_0=X_0+X_1`, `E_{2m}=X_2`, and all intermediate `E_d` vanish.

The same equations viewed from the pure endpoint are obtained by putting
`s=t^{-1}` and using homogeneity:

\[
 H(c+s b+s^2a)=X_2+s^{2m}(X_0+X_1).                     \tag{6}
\]

In particular,

\[
 \frac{bc^{m-1}}{(m-1)!}=0,                              \tag{7}
\]

\[
 \frac{ac^{m-1}}{(m-1)!}
 +\frac{b^2c^{m-2}}{2(m-2)!}=0,                          \tag{8}
\]

and the first equation coupling three holes is

\[
 \frac{bac^{m-2}}{(m-2)!}
 +\frac{b^3c^{m-3}}{6(m-3)!}=0.                          \tag{9}
\]

Equation (4) is of course equivalent to the original coefficient system.
The point of (6) is to test whether its high-order half has more rigidity
than is apparent coefficientwise.

## 2. Exact classification through the second pure-endpoint jet

Write

\[
 c=\sum_{i<j}c_{ij}z_iz_j
\]

and let `C=(c_ij)` be the symmetric zero-diagonal scalar matrix.  For a set
of deleted sites define

\[
 h_{i_1\cdots i_r}
   =\operatorname{haf}C[B\setminus\{i_1,\ldots,i_r\}],
 \qquad h_B=1.                                           \tag{10}
\]

The pure endpoint equation is exactly

\[
                         \operatorname{haf}C=1.           \tag{11}
\]

It imposes no support uniqueness on `c`.

For `r in {0,1}`, let `b^r_ij` be the directed cell with colour `r` at site
`i` and colour `2` at site `j`, so

\[
 b=\sum_{r=0}^1\sum_{i\ne j}b^r_{ij}x_{i,r}z_j.         \tag{12}
\]

Similarly, write `a_ik^{rs}` for the cell with binary colours `r,s` at
`i,k`.  Direct matching expansion gives the following complete
classification.

**Lemma 2.1 (first two pure-endpoint jets).**  Equations (7)--(8) are
equivalent to

\[
             \sum_{j\ne i}b^r_{ij}h_{ij}=0
             \qquad(i\in B,\ r\in\{0,1\}),              \tag{13}
\]

and

\[
 a_{ik}^{rs}h_{ik}
 +\sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       b^r_{ij}b^s_{k\ell}h_{ikj\ell}=0                 \tag{14}
\]

for every pair `i<k` and `r,s in {0,1}`.

Moreover, every cofactor row in (13) is nonzero, and hence its kernel has
dimension exactly `n-2`.  If all `h_ik` are nonzero, every solution of (13)
has a unique lift through (14), namely

\[
 a_{ik}^{rs}=-\frac{1}{h_{ik}}
 \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
       b^r_{ij}b^s_{k\ell}h_{ikj\ell}.                  \tag{15}
\]

**Proof.**  In a one-binary-hole coefficient, the unique `b` cell joins
the hole `i` to some `j`; the remaining sites are matched by `c`.  This is
(13).  In a two-hole coefficient, either one `a` cell joins the two holes,
or two `b` cells join them to distinct sites `j,ell`; the remaining sites
are again matched by `c`.  The factor `1/2` in (8) cancels the two orders of
the two distinct `b` factors, giving (14).

Expanding the hafnian at site `i` gives

\[
                   \sum_{j\ne i}c_{ij}h_{ij}
                   =\operatorname{haf}C=1.               \tag{16}
\]

Thus the row `(h_ij : j != i)` is nonzero.  Equation (13) is one nonzero
linear form on `n-1` variables, proving the dimension assertion.  If
`h_ik` is nonzero, (14) is solved uniquely by (15), independently for each
pair and endpoint-colour pair. `QED`

Consequently the tangent space defined by (7) has dimension

\[
                              2n(n-2)                     \tag{17}
\]

in the `b` variables alone.  Pair-to-pair compatibility has not yet
appeared.  When `h_ik=0`, equation (14) instead constrains its quadratic
`b`-pairing and leaves `a_ik^{rs}` invisible.  Both branches are large.

The cofactor-dense case is nonempty over the rationals for every even
`n>=4`.  Give every edge of `C` weight one except

\[
                  c_{01}=\frac1{(n-3)!!}-(n-2).           \tag{18}
\]

Then (11) holds.  A two-hole cofactor is `(n-3)!!` if deletion removes at
least one of `0,1`; otherwise it is

\[
                 \frac1{n-3}-2(n-5)!!,                   \tag{19}
\]

which is also nonzero.  Thus arbitrary choices in all the row kernels
(13) lift exactly through order two by (15).  The checker constructs a
nonzero rational example at `n=8` and independently enumerates every
one- and two-hole fibre.

## 3. A uniform top-to-middle counterfamily

The following family shows that even all higher equations through the
middle can vanish on the singular pure-endpoint branch.

Put `B={0,...,2m-1}` and define

\[
\begin{aligned}
 P_0&=01|23|\cdots|(2m-2,2m-1),\\
 P_1&=12|34|\cdots|(2m-3,2m-2)|(2m-1,0),                 \tag{20}
\end{aligned}
\]

and write `P_2={e_0,...,e_{m-1}}`, where

\[
\begin{aligned}
 e_0&=02,\\
 e_j&=(2j-1,2j+2)\qquad(1\leq j\leq m-2),\\
 e_{m-1}&=(2m-3,2m-1).                                  \tag{21}
\end{aligned}
\]

The three factors are pairwise edge-disjoint and every pairwise union is a
Hamilton cycle.  For `P_0 union P_1` this is immediate.  After contracting
the `P_1` edges, the `P_2` edges form the cycle

\[
                         m-1,0,1,\ldots,m-2,m-1.
\]

After contracting the `P_0` edges, their quotient edges are

\[
 01,\quad (j-1,j+1)\ (1\leq j\leq m-2),\quad(m-2,m-1),
\]

which again form one cycle.  This proves the claim.

Give the edges of `P_r` the unit diagonal colour-`r` cell and put

\[
 a=\sum_{uv\in P_0}x_ux_v+\sum_{uv\in P_1}y_uy_v,\qquad
 b=0,\qquad c=\sum_{uv\in P_2}z_uz_v.                   \tag{22}
\]

Pairwise Hamiltonicity immediately gives

\[
 H(a)=X_0+X_1,\qquad H(c)=X_2,                          \tag{23}
\]

and every principal binary face is exact.

The complete supported-matching list also has a uniform description.

**Lemma 3.1 (path-independent-set matching classification).**  Besides
`P_0,P_1,P_2`, the perfect matchings in
`Gamma_m=P_0 union P_1 union P_2` are indexed by the nonempty independent
sets

\[
                         I\subseteq\{1,\ldots,m-2\}       \tag{24}
\]

of the path on those indices.  The matching `M_I` uses precisely the
`P_2` edges `e_j`, `j in I`, and its remaining edges are the unique
perfect matching of `P_0 union P_1` after their endpoints are removed.

**Proof.**  The graph `P_0 union P_1` is the natural cyclic order on the
`2m` sites.  If a set of `P_2` edges is prescribed, the remaining cycle
paths have a perfect matching exactly when each has even order; that
matching is then unique.  Equivalently, consecutive deleted vertices in
cyclic order must have opposite parity.

For an interior chord `e_j`, its endpoints are the odd site `2j-1` and the
even site `2j+2`.  Two chosen interior chords preserve the required parity
alternation exactly when their indices are not consecutive.  Choosing
`e_0=02` forces `e_1` in order to cover the intervening odd site; the same
argument propagates through every chord and gives all of `P_2`.  The last
boundary chord behaves symmetrically.  Hence every proper nonempty choice
is exactly an independent subset of the interior path.  Conversely, the
endpoints of any such independent set alternate in parity around the
cycle, so all remaining paths have even order and possess their unique
cycle matching. `QED`

There are `F_m-1` nonempty independent sets in (24), with
`F_0=0,F_1=1`.  Hence `Gamma_m` has `F_m+2` perfect matchings in all.  If
`|I|=r`, then `M_I` has colour-edge counts

\[
                              (r,m-2r,r).                 \tag{25}
\]

Indeed, each selected interior chord forces the two enclosed sites onto
their `P_0` edge; after deleting these disjoint four-site intervals, the
remaining cycle paths use `P_1`.

Its induced colouring determines it uniquely, because each site has only
one incident edge of each colour.  Consequently every error coefficient is
a singleton of weight one, and the exact source output is

\[
 H(a+t^2c)=X_0+X_1+t^{2m}X_2
   +\sum_{\substack{\varnothing\ne I\subseteq\{1,\ldots,m-2\}\\
                     I\text{ independent}}}
       t^{2|I|}X_{w(I)}.                                  \tag{26}
\]

The largest independent set in a path of length `m-2` has size

\[
                     \left\lfloor\frac{m-1}{2}\right\rfloor.
\]

Every error in (26) therefore has `t`-degree strictly less than `m`.  In
the reversed expansion,

\[
 H(c+s^2a)=X_2+s^{2m}(X_0+X_1)
   +\sum_I s^{2(m-|I|)}X_{w(I)},                          \tag{27}
\]

so every coefficient of `s,s^2,...,s^m` is zero.  The first error occurs
at degree `m+1` for odd `m` and at degree `m+2` for even `m`.

This is precisely the extremal-to-middle test.  It passes for every
`m>=3`, together with the exact binary endpoint (23), yet (26) is not
ternary equality.  For a singleton `I={j}`, the error matching consists of
`e_j in P_2`, the enclosed edge `(2j,2j+1) in P_0`, and `m-2` edges of
`P_1`.  It has one colour-zero edge and one colour-two edge and hence is a
genuinely ternary `t^2` coefficient, invisible in every binary face.

## 4. The pure endpoint need not be a one-factor

The preceding family makes `c` one matching only to expose the uniform
combinatorics.  Even at six sites, (11) does not justify that reduction.
Here is a rational cancellation example.  In each row below, the first edge
is shared by the two displayed monochromatic matchings:

\[
\begin{array}{c|c|c}
\text{colour}&\text{shared edge}&\text{two remaining pairs}\ \hline
0&01=1&(23=1,45=1/2),\ (24=1,35=1/2)\\
1&34=1&(02=1,15=1/2),\ (05=1,12=1/2)\\
2&25=1&(03=1,14=1/2),\ (04=1,13=1/2).
\end{array}                                               \tag{28}
\]

Each pure coefficient is `1/2+1/2=1`, and each principal binary face has
only its four displayed pure matchings.  The full support has nine further
perfect matchings.  Every one uses one edge of each colour, induces a
distinct colouring with two sites of each colour, and has nonzero rational
weight.

Take colours zero and one as `a`, colour two as `c`, and again set `b=0`.
Then `c` has five cells and two nonzero perfect-matching terms, while

\[
 H(a)=X_0+X_1,\qquad H(c)=X_2,\qquad
 ac^2=0.                                                  \tag{29}
\]

Thus the reversed coefficients through the middle `s^3` vanish exactly,
and the first error is the genuinely ternary `s^4` sector.  This
adversarial example rules out silently replacing a cancellation-supported
pure endpoint by one selected matching.

## 5. Consequence for the route

The torus decomposition is useful bookkeeping, and Lemma 2.1 identifies
the first genuinely coupled equation: (9).  But neither of the tempting
shortcuts is valid:

* a pure endpoint is not support-pure; and
* even a support-pure endpoint, an exact binary opposite endpoint, every
  exact binary face, and all osculating identities through the middle do
  not force the missing ternary equations.

In particular, factoring `c^{m-3}` or contracting a selected pure matching
cannot be justified from the top half alone.  In the family (20)--(22), the
first omitted equation is the singleton `t^2` matching in (26); a
top-derived contraction necessarily forgets it.  A viable continuation
must combine the low-side genuinely ternary two-`z` equations with the
third and higher pure-endpoint Bianchi equations, while retaining all
cofactor-zero branches.  The one-parameter torus by itself supplies no
six-site descent.

The dependency-free exact audit is
`computations/verify_torus_osculation_top_half_countermodel.py`.  It checks
the uniform family through `m=14`, the Fibonacci matching classification,
all pairwise binary faces, exact contact orders, the dense rational
first/second lift at `n=8`, and the six-site two-term pure-endpoint example.

The complementary bottom/top collision and its sharp twelve-site model are
recorded in `torus-osculation-bottom-top-collision.md`.
