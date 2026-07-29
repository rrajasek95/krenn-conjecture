# Flag averaging is exact, but it does not select a clean six-cap

## 1. Outcome

There is a uniform closed formula for averaging matching sectors over all
five- or six-subsets.  If `|B|=2m` and `T_j^U` denotes the part of the full
matching tensor whose matching has exactly `j` edges crossing
`U | (B\setminus U)`, then

\[
 \boxed{
 \sum_{\substack{U\subset B\\|U|=k}}T_j^U
 =2^j\binom mj\binom{m-j}{(k-j)/2}\,H_B(A).}
                                                               \tag{1}
\]

The binomial coefficient is understood to be zero unless its lower entry
is an integer in the usual range.  In particular,

\[
 \boxed{\sum_{|U|=5}T_1^U=m(m-1)(m-2)H_B(A).}             \tag{2}
\]

Thus the proposed averaging identity really does give a scalar multiple of
`Delta_(B,3)` under the hypothetical exact GHZ equation.  It does **not**
force one summand to satisfy the one-crossing kernel criterion.  Row-space
containment is nonlinear in the summand, and the other crossing sectors have
their own independent scalar averages.

The same gap occurs for all-colours product caps.  An exact-arithmetic
complete-graph ternary model on eight sites has all of the following
properties:

* every physical pair has nonzero all-colours cap scalar;
* all three constant GHZ coefficients are exactly one;
* every mixed coefficient at Hamming distance one from a constant word is
  zero;
* every vertex and colour has an active coordinate anchor;
* all 56 five-set one-crossing kernel tests fail by the full three target
  rows; and
* all 28 retained six-set product caps have nonzero top cumulant correction.

The model is not an exact GHZ source: mixed coefficients at distance at
least two remain.  It is therefore not a counterexample to the conjecture,
nor to a selection theorem which genuinely uses every mixed GHZ equation.
It is an exact matching-realizable falsifier to deriving such a selection
from flag averaging, constant-fibre normalization, first-jet vanishing,
anchors, or cap nonvanishing.  The dependency-light exact audit is
[`verify_six_cap_flag_countermodel.py`](../computations/verify_six_cap_flag_countermodel.py).

## 2. The complete crossing-sector incidence formula

Fix a perfect matching `M` of `B`.  To choose a `k`-set `U` for which
exactly `j` edges of `M` cross the cut, one must:

1. choose the `j` crossing edges of `M`;
2. choose which endpoint of each crossing edge belongs to `U`; and
3. choose `(k-j)/2` of the remaining matching edges to lie wholly in `U`.

This gives exactly

\[
                    N_{m,k,j}
 =2^j\binom mj\binom{m-j}{(k-j)/2}                       \tag{3}
\]

choices.  The number is independent of `M`.  Summing first over `U` and
then over the formal matching monomials proves (1), with no genericity,
support, or noncancellation assumption.

For five-sets the three possible multipliers are

\[
\begin{aligned}
N_{m,5,1}&=2m\binom{m-1}{2}=m(m-1)(m-2),\\
N_{m,5,3}&=8\binom m3(m-3),\\
N_{m,5,5}&=32\binom m5.
\end{aligned}                                             \tag{4}
\]

For six-sets they are

\[
\begin{aligned}
N_{m,6,0}&=\binom m3,\\
N_{m,6,2}&=4\binom m2\binom{m-2}{2},\\
N_{m,6,4}&=16\binom m4(m-4),\\
N_{m,6,6}&=64\binom m6.
\end{aligned}                                             \tag{5}
\]

Their sum over the allowed `j` is `binom(2m,k)`, as it must be.  At order
eight, equations (4)--(5) specialize to

\[
 \sum_{|U|=5}T_1^U=24H_8,\qquad
 \sum_{|U|=5}T_3^U=32H_8,                                \tag{6}
\]

and

\[
 \sum_{|S|=6}T_0^S=4H_8,\qquad
 \sum_{|S|=6}T_2^S=24H_8.                                \tag{7}
\]

So under `H_B=Delta_(B,3)`, every crossing sector has a diagonal average;
the mixed cancellations can occur between different cuts inside each
sector.  Equation (2) alone supplies no distinguished cut.

## 3. The exact pair-cap cumulant at order eight

Let `S=B\setminus\{p,q\}` have six sites and cap `p,q` by

\[
                 K_{pq}=\epsilon_p\otimes\epsilon_q,
 \qquad \epsilon=e_0^*+e_1^*+e_2^*.                     \tag{8}
\]

Put

\[
 s_{pq}=(\epsilon_p\otimes\epsilon_q)(A_{pq})            \tag{9}
\]

and let `J=C_2` be the induced two-boundary edge family

\[
 J_{uv}=b_{u,p}\otimes b_{v,q}+b_{u,q}\otimes b_{v,p},
 \qquad
 b_{u,p}=(\operatorname{id}_{V_u}\otimes\epsilon_p)A_{up}.
                                                               \tag{10}
\]

There are only two capped sites, so `C_4=C_6=0` in the monomer formula and

\[
 K_{pq}\mathbin{\lrcorner}H_8(A)
       =s_{pq}H_6(A_S)+JH_4(A_S).                         \tag{11}
\]

Assume `s=s_pq` is nonzero.  The normalized cumulants are

\[
 L_2={J\over s},\qquad
 L_4=-{J^2\over2s^2},\qquad
 L_6={J^3\over3s^3}.                                     \tag{12}
\]

Consequently the top correction left after replacing the cap by the
effective pair family `A_S+J/s` is

\[
\begin{aligned}
 \mathcal E_{pq}
  &:=K_{pq}\mathbin{\lrcorner}H_8(A)
       -sH_6(A_S+J/s)\\
  &=s\{L_6+L_4(A_S+L_2)\}\\
  &=-{J^2A_S\over2s}-{J^3\over6s^2}.                    \tag{13}
\end{aligned}

All products in (11)--(13) are square-free site-graded products.  Formula
(13) is the exact `L_4/L_6` analogue of the linear flag identities.  Unlike
(1), it contains nonlinear powers of a cap-dependent response, so the
matching-incidence count does not diagonalize it.

## 4. A complete ternary model with every six-cap dirty

Use vertices `0,...,7` and the standard one-factorization

\[
\begin{array}{c|l}
F_0&07|16|25|34\\
F_1&02|17|36|45\\
F_2&04|13|27|56\\
F_3&06|15|24|37\\
F_4&01|26|35|47\\
F_5&03|12|46|57\\
F_6&05|14|23|67.
\end{array}                                               \tag{14}
\]

Let

\[
 P=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix},
 \qquad
 P^2=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}. \tag{15}
\]

Put `P` on every edge of `F_0` and `F_5`, put `P^2` on every edge of
`F_1` and `F_6`, and put `E_rr` on `F_(r+2)` for `r=0,1,2`.
The seven factors partition all 28 edges, so this is a complete physical
graph.  Every non-anchor matrix is invertible.  Moreover,

\[
       s_{pq}=\begin{cases}1,&pq\in F_2\cup F_3\cup F_4,\\
                            3,&pq\in F_0\cup F_1\cup F_5\cup F_6,
             \end{cases}                                  \tag{16}
\]

so every product cap is nonzero.

For a constant colour `r`, only the four edges of `F_(r+2)` have a
nonzero `(r,r)` entry.  They form one perfect matching, hence

\[
                 H_8(A)_{r^8}=1\qquad(r=0,1,2).           \tag{17}
\]

The same observation proves that every `E_rr` edge is tensor-active: after
deleting it, the other three edges of its factor give a nonzero constant
six-site cofactor.

There is also no supported word at Hamming distance one from a constant
word.  Indeed, suppose only `x` differs from colour `r`.  The other seven
vertices can pair through `(r,r)` entries only along `F_(r+2)`.  If `x` is
paired to `y`, the remaining six vertices can be covered by that factor
only when `x,y` are its paired vertices; but their edge is `E_rr` and is
zero at the colour of `x`.  This contradiction proves the first mixed
layer vanishes.

Exact enumeration gives the support census by distance from the nearest
constant word

\[
\begin{array}{c|rrrrrr}
\text{distance}&0&1&2&3&4&5\\\hline
\#\text{ nonzero words}&3&0&53&270&773&445.
\end{array}                                               \tag{18}
\]

Thus the unused full-GHZ information starts precisely at distance two.

## 5. Every one-crossing cut and every product cap fails

For a three-set `C` and its five-set complement `U`, write the
one-crossing flattening as a `27 by 243` matrix `F_(1,U)`.  Let `delta_U`
be the three target rows supported at `0^5,1^5,2^5`.  Exact rational row
reduction gives

\[
\begin{array}{c|c|c}
\operatorname{rank}F_{1,U}&
\operatorname{rank}\binom{F_{1,U}}{\delta_U}
       -\operatorname{rank}F_{1,U}&\#\text{ cuts}\\\hline
9&3&54\\
8&3&2.
\end{array}                                               \tag{19}
\]

The two rank-eight three-shores are `C=023` and `C=127`.  The defect is
three on every cut, so not even one nonzero target row belongs to the
one-crossing row space.  In particular

\[
                  \ker F_{1,U}\not\subseteq\ker\delta_U
                  \qquad\text{for all 56 five-sets }U.    \tag{20}
\]

For the 28 product pair caps, evaluate the label-independent diagonal
trace

\[
                  \tau(\mathcal E_{pq})
       =\sum_{r=0}^2(\mathcal E_{pq})_{r^6}.              \tag{21}
\]

Using (13), exact rational arithmetic gives the following complete table.

\[
\begin{array}{c|l|c}
\tau&\text{deleted pairs }pq&\#\\\hline
-118&01,04,06,26,56&5\\
-96&13,15,24,27,35,47&6\\
-114&37&1\\
-8&17,23,34,57&4\\
-6&02,05,16,46&4\\
-26/3&03,07,36,67&4\\
-32/3&12,45&2\\
-20/3&14,25&2.
\end{array}                                               \tag{22}
\]

Every trace is nonzero, hence every top cumulant correction is nonzero.
Their total trace is

\[
                 \sum_{p<q}\tau(\mathcal E_{pq})
                              =-{4216\over3}\ne0.         \tag{23}
\]

Thus there is no universal zero-sum or trace cancellation for the
`L_4/L_6` corrections, even with complete cap nonvanishing, exact constant
fibres, first mixed-jet vanishing, and active ternary anchors.

The checker independently obtains each cap in two ways: by contracting the
enumerated eight-site tensor, and by expanding exactly the terms in
`H_6(A+J/s)` which use at least two `J` edges.  It verifies (13) coefficient
by coefficient on all `3^6` words.  The correction support sizes over the
28 caps are

\[
 \begin{array}{c|rrrr}
\#\operatorname{supp}\mathcal E&616&665&697&729\\\hline
\#\text{ caps}&2&2&16&8.
\end{array}                                               \tag{24}
\]

Run the full audit with

```sh
python computations/verify_six_cap_flag_countermodel.py
```

## 6. Exact boundary of the result

Equations (1)--(7) settle the proposed averaging calculation completely:
under a hypothetical exact source, each averaged crossing sector is indeed
a known multiple of the target.  Equations (14)--(24) show why this cannot
by itself select a cut or cap.  The missing input cannot be another linear
incidence average, nonvanishing of the cap scalars, constant-fibre data, or
the first mixed jet.  It must use simultaneous cancellation beginning at
the two-defect mixed fibres (or an equivalent nonlinear consequence of all
GHZ equations).
