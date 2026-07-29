# Higher splits: a uniform value-core exchange theorem for collision strata

## 1. Statement

Put

\[
 h=t-r-1,\qquad p=r-1=h+k,\qquad k\ge1,\qquad h\ge7,
 \tag{1}
\]

and let the exceptional beta profile be

\[
 \lambda=(\lambda _1,\ldots,\lambda _c),\qquad
 \sum_{i=1}^c\lambda_i=p+h+2=2h+k+2=:M.                 \tag{2}
\]

Thus $c$ is the number of distinct exceptional value classes.  Let
$n_j=|\{i:\lambda_i=j\}|$, and put

\[
                         e=M-c=\sum_i(\lambda_i-1).        \tag{3}
\]

This note gives three uniform sufficient conditions which close a collision
profile on every structurally admissible value stratum.

**Theorem 1.1.**  Some isolated-star pivot is nonzero if any one of the
following holds.

1. **One large class:** \(\max_i\lambda_i\ge h\).
2. **A short Hermite core:** one can select $h$ labels from at most two
   value classes and leave a singleton value class in the complement.
3. **Uniform distinct-value cores:**

   \[
      c\ge h+1,\qquad
      \boxed{\ n_1\ge h+1\quad\hbox{or}\quad n_2\ge c-h+1\ }, \tag{4}
   \]

   and either

   \[
                               e\le2,                       \tag{5}
   \]

   or the Wronskian number in (6) below is positive.

For the latter condition set

\[
 \ell=\max(0,c-2h-2).
\]

For a genuine collision $e\ge1$, one has automatically
$0\le\ell\le k-1$, and the required number is

\[
 \boxed{\quad
 \Omega(c,h,k)=9-c+(\ell+1)\max(3-k+\ell,0)>0.
 \quad}                                                     \tag{6}
\]

Condition (4) is exact, not merely sufficient: it says precisely that
*every* $h$-set of value classes, selected once each, leaves a singleton
row class.  Conditions (4)--(6) therefore depend only on the multiplicity
profile and the split integers.

In the common range $c\le2h+2$, so that \(\ell=0\), (6) has the sharp
simple form

\[
 \begin{array}{c|c}
 k&\text{Wronskian closure}\ \\ \hline
 1&c\le10,\\
 2&c\le9,\\
 k\ge3&c\le8.
 \end{array}                                                \tag{7}
\]

For example, (7) simultaneously contains the seventh-split terminal
profiles \((2^8,1)\) and \((2^7,1^3)\), with respectively $c=9,10$,
instead of treating them as isolated configurations.  It also supplies
new higher-split closures whenever (4) and the displayed bounds hold.

The result is a sufficient theorem, not a claim that (1)--(6) exhaust all
higher collision profiles.  Its value is that no determinant
classification or genericity assertion occurs in it.

## 2. The two elementary closures

### 2.1 A class of multiplicity at least \(h\)

Choose $h$ labels of a value $a$ for the selected columns.  After the
standard nonzero row factors are removed, a pivot is

\[
                         h!e_h(x_i:i\in L),\qquad
                    x_i={\nu_i+\mu\over\nu_i+a}\ne0.       \tag{8}
\]

Here $N$, before deleting the marked pair, has $p+2$ labels, and
$L\subset N$ has $p$ labels.  Suppose all two-deletion expressions in
(8) vanish.  If all $x_i$ are equal, (8) is the nonzero number
$h!\binom phx^h$.  Otherwise choose $x_j\ne x_k$, and put
$U=N\setminus\{j,k\}$, so $|U|=p$.  Comparing the deletions
\(\{i,j\}\) and \(\{i,k\}\) gives

\[
                  (x_k-x_j)e_{h-1}(U\setminus\{i\})=0
                  \qquad(i\in U).                         \tag{9}
\]

The identities

\[
 \sum_{i\in U}e_d(U\setminus\{i\})=(p-d)e_d(U),\qquad
 e_d(U)=e_d(U\setminus\{i\})+x_i e_{d-1}(U\setminus\{i\}) \tag{10}
\]

descend from $d=h-1$ to $d=1$.  Every coefficient $p-d$ is nonzero,
and the last step forces an $x_i$ to vanish.  This contradicts (8).

### 2.2 Short Hermite cores

More explicitly, the second condition of Theorem 1.1 asks for integers
$r_i$, supported on one or two classes, such that

\[
 0\le r_i\le\lambda_i,\qquad \sum_i r_i=h,qquad
 \lambda_j-r_j=1\quad\hbox{for some }j.                   \tag{11}
\]

For this selection the simultaneous-Hermite singleton-row lemma gives a
nonzero rational column dependence.  If $m_R\le2$ value classes occur
among the selected labels, its denominator and numerator degrees are

\[
 \deg D_R=(k+1)+h+m_R=p+m_R+1,qquad
 \deg Q_R\le p+m_R-1\le p+1.                              \tag{12}
\]

The $p+2$ complementary row jets divide $Q_R$, which is impossible.
This proves the second closure without any restriction on $c$.

## 3. Exactly when every distinct-value core is legal

Let $R$ be an $h$-set of value classes, selecting one label in each.
Its complement has a singleton row class exactly when

\[
 \text{some selected class has multiplicity two, or some unselected
 singleton class exists}.                                 \tag{13}
\]

Thus an illegal $R$ contains every singleton class and contains no
double class.  Such an $h$-set exists precisely when

\[
                           n_1\le h\le c-n_2.              \tag{14}
\]

Negating (14) gives (4).  Notice that this argument also audits a possible
zero value: a repeated value cannot be zero, so the possible zero class is
a singleton and is treated by the second alternative in (13).  No
nonzero-anchor assumption has been inserted silently.

Assume from now on that (4) holds and that every isolated-star pivot
vanishes.  For each $h$-set $R$ the singleton-row lemma and the Hermite
degree calculation give

\[
                 0\ne q_R\in\mathbb C[z],\qquad
                         \deg q_R\le h-3.                  \tag{15}
\]

To retain all multiplicities exactly, define for every $T\subset V$

\[
 \begin{split}
 B_T(z)&=\prod_{v\in V}(z-v)^{\lambda_v-\mathbf1_{v\in T}},\\
 \Delta_T(z)&=(z+\mu)^{k+1}\prod_{v\in T}(z+v)^2,\\
 F_{T,q}(z)&={B_T(z)q(z)\over\Delta_T(z)}.
 \end{split}                                                \tag{16}
\]

At a selected anchor $a\in T$, absence of a simple pole at $-a$ is a
Robin equation

\[
                     q'(-a)+Y_a(T)q(-a)=0.                 \tag{17}
\]

One completely explicit form is

\[
 \begin{split}
 Y_a(T)&=A_a+\sum_{b\in T\setminus\{a\}}\psi(a,b),\\
 A_a&=-\sum_{v\ne a}{\lambda_v\over a+v}
      -{\lambda_a-1\over2a}-{k+1\over\mu-a},\\
 \psi(a,b)&={1\over a+b}-{2\over b-a}.
 \end{split}                                                \tag{18}
\]

When $a=0$, structural admissibility forces \(\lambda_a=1\), and the
self term in (18) is absent; no $0/0$ is intended.  All other
denominators are structurally nonzero.

## 4. Cubic exchange through all value classes

For $b\in V$, put

\[
                            g_b(z)=(z-b)(z+b)^2.            \tag{19}
\]

The exchange is most transparently checked before taking logarithmic
derivatives.  If $b\notin T$, then

\[
 {B_{T\cup\{b\}}(z)g_b(z)q(z)\over\Delta_{T\cup\{b\}}(z)}
                  ={B_T(z)q(z)\over\Delta_T(z)}.          \tag{20}
\]

Equivalently,

\[
 {g_b'(-a)\over g_b(-a)}=-\psi(a,b)\quad(a\ne b),\qquad
                         g_b(-b)=g_b'(-b)=0.               \tag{21}
\]

The three-lift lemma from the all-distinct exchange proof depends only on
the distinctness and nonoppositeness of the *value classes*, not on their
multiplicities.  It therefore applies verbatim here, including $b=0$:
if $|T|=m+1$ and every deletion has a nonzero residual of degree at most
$m-3$, then the $m+1$ lifts

\[
                         g_bq_{T\setminus\{b\}},\qquad b\in T, \tag{22}
\]

have degree at most $m$, obey (17) on all of $T$, and span at least
three dimensions.  The proof removes the gcd of a hypothetical pencil;
the relations \(\phi(b)=\phi(-b)\) force the rational map to be even, and
the double zeros at $-b$ then exceed the Riemann--Hurwitz ramification
degree.  For $b=0$, $g_0=z^3$, and the same gcd count applies.

Starting from (15), cancel the top two coefficients in (22).  Induction
gives, for every $T\subset V$ with $h\le|T|\le c-1$,

\[
                     0\ne q_T,\qquad\deg q_T\le|T|-3.     \tag{23}
\]

At the final step do **not** cancel the span.  The lifts from the
$(c-1)$-sets produce

\[
 K\subset\mathbb C[z]_{\le c-1},\qquad
 \dim K\ge3,\qquad
 q'(-a)+Y_a(V)q(-a)=0\quad(a\in V,q\in K).                \tag{24}
\]

This is why the assumption $c\ge h+1$ occurs in Theorem 1.1.

## 5. The full-core rational functions

Write

\[
 B(z)=\prod_{v\in V}(z-v)^{\lambda_v-1},\qquad
 P(z)=\prod_{v\in V}(z+v),\qquad
 F_q(z)={B(z)q(z)\over(z+\mu)^{k+1}P(z)^2}.               \tag{25}
\]

The factors $B(-a)$, $B(-\mu)$, $P(-\mu)$, and $a+\mu$ which are
used below are nonzero by the noncollision, no-opposite, and Cauchy
denominator conditions.  This remains true at a zero singleton because
its exponent in $B$ is zero.

At the full value core, (18) becomes

\[
 Y_a(V)={B'(-a)\over B(-a)}-{k+1\over\mu-a}
                   -{P''(-a)\over P'(-a)}.                \tag{26}
\]

Hence (24) is exactly

\[
                          \operatorname {res}_{z=-a}F_q=0
                          \qquad(a\in V).                 \tag{27}
\]

Since \(\deg B=M-c\) and \(\deg q\le c-1\),

\[
                              F_q(z)=O(z^{-2(c-h)}).        \tag{28}
\]

### 5.1 Collision excess at most two

The induction also supplies a nonzero *low* full-core residual

\[
                         q_V\in\mathbb C[z]_{\le c-3}.     \tag{29}
\]

Indeed, apply the same two-top-coefficient cancellation to the final
at-least-three-dimensional lift space in (24); (29) is not an additional
rank assumption.

Suppose \(e=\deg B\le2\).  For any
$t\in\mathbb C[z]_{\le c-1}$, multiply $F_{q_V}$ by

\[
              G_t(z)={(z+\mu)^{k+1}B(z)t(z)\over B(z)}
                     =(z+\mu)^{k+1}t(z).                  \tag{30}
\]

Equivalently, in the general rational-multiplier notation one chooses
$s=Bt$, whose degree is at most $c+1$.  Then

\[
                      G_tF_{q_V}={B t q_V\over P^2}=O(z^{-2}). \tag{31}
\]

If $c_a$ is the double-pole coefficient of $F_{q_V}$ at $-a$, the
residue theorem gives

\[
                \sum_{a\in V}c_a\,G_t'(-a)=0
                \qquad(t\in\mathbb C[z]_{\le c-1}).       \tag{32}
\]

On the shifted basis $t=(z+\mu)^j$, differentiation in (32) is the
diagonally scaled Vandermonde map

\[
       G_t'=(j+k+1)(z+\mu)^{j+k}.                          \tag{33}
\]

Writing the nodes as $x_i=-a_i$, its exact determinant is

\[
 \left(\prod_{j=0}^{c-1}(j+k+1)\right)
 \left(\prod_{i=1}^{c}(x_i+\mu)^k\right)
 \prod_{i<j}(x_j-x_i)\ne0.
\]

It is therefore surjective on the $c$ distinct nodes.  Thus every $c_a=0$, so
$q_V$ vanishes at all $c$ nodes although \(\deg q_V\le c-3\).  This
proves (5).

### 5.2 Polynomial multipliers with stationary exceptional jets

For the Wronskian alternative retain the full space $K$.  Put

\[
                  D=2(c-h)-2,qquad
 \mathcal G_D=\{G\in\mathbb C[z]_{\le D}:P\mid G'\}.      \tag{34}
\]

For $G\in\mathcal G_D$, (27) and $G'(-a)=0$ show that all exceptional
residues of $GF_q$ vanish.  Equation (28) shows that its residue at
infinity also vanishes.  Therefore

\[
 \operatorname {res}_{z=-\mu}G(z)F_q(z)=0
       \qquad(G\in\mathcal G_D,\ q\in K).                 \tag{35}
\]

The multiplier space consists of the constants and the primitives

\[
       G_S(z)=\int_{-\mu}^{z}P(t)S(t)\,dt,qquad
       \deg S\le D-c-1.                                   \tag{36}
\]

Consequently

\[
                \dim\mathcal G_D=\ell+1,qquad
                \ell=\max(0,D-c)=\max(0,c-2h-2).          \tag{37}
\]

Because $P(-\mu)\ne0$, the jets at $-\mu$ of (36), together with the
constant, have successive pivot orders

\[
                              0,1,\ldots,\ell.             \tag{38}
\]

This is the only place where the amount of decay in (28) enters the
Wronskian count.

## 6. The weighted residue--Wronskian inequality

Let $d=\dim K\ge3$, let $H=\gcd K$, and write $g=\deg H$.  Let $b$
be the number of exceptional nodes $-a$ at which $H$ vanishes, and let
$u=\operatorname {ord}_{-\mu}H$.  At an exceptional Robin node a common
root is automatically double: after writing $q=Hf$, choose a reduced
section with $f(-a)\ne0$ in (24), which forces $H'(-a)=0$.  Hence

\[
                              g\ge2b+u.                    \tag{39}
\]

Divide by $H$, obtaining a base-point-free $d$-space of polynomials of
degree at most $c-1-g$.  Every one of the $c-b$ surviving exceptional
nodes has vanishing sequence at least

\[
                              0,2,3,\ldots,d,              \tag{40}
\]

and therefore contributes Wronskian weight at least $d-1$.

It remains to account carefully for a possible common root at $-\mu$.
Put $w=z+\mu$.  The regular factor $B/P^2$ is a unit there, so (35)
is the coefficient identity

\[
       [w^k]\,G(w)w^uU(w)f(w)=0                           \tag{41}
\]

for every multiplier jet in (38), every reduced section $f$, and some
unit $U$.

If $u>k$, (41) is automatic.  If $u\le k$, put $n=k-u$.  The
coefficient pairing on $n$-jets is perfect, while the multiplier jets
have rank \(\min(\ell+1,n+1)\).  Thus the reduced space has $n$-jet
image of dimension at most

\[
                              a=\max(n-\ell,0).             \tag{42}
\]

The case $a=0$ is impossible, since it would make every reduced section
vanish at $-\mu$.  In particular, the easily missed edge $u=k$ has
$n=0$ and is impossible even when \(\ell=0\); it must not be assigned
zero Wronskian weight.  When $a>0$, at most $a$ entries of the vanishing
sequence can be at most $n$.  The smallest possible sequence is

\[
 0,1,\ldots,a-1,\quad n+1,n+2,\ldots,n+d-a,
\]

so the additional Wronskian weight is

\[
 w_{\mu}(d,u)=
 \begin{cases}
  (\ell+1)\max(d-k+u+\ell,0),&u\le k,\ \ell<k-u,\\
  \text{impossible},&u\le k,\ \ell\ge k-u,\\
  0,&u>k.
 \end{cases}                                               \tag{43}
\]

The nonzero polynomial Wronskian of the reduced space has degree at most

\[
                   d\bigl((c-1-g)-d+1\bigr)=d(c-d-g).
\]

Equations (39)--(43) give the necessary inequality

\[
 \boxed{
 (c-b)(d-1)+w_\mu(d,u)
            \le d(c-d-2b-u).}                             \tag{44}
\]

This is the promised weighted complement/residue/Wronskian obstruction.
It explicitly includes every gcd possibility at the common-value pole.

For completeness, subtract the right side of (44) from the left.  The
difference is

\[
             d^2-c+b(d+1)+du+w_\mu(d,u).                  \tag{45}
\]

It is minimized at $b=0$, at $d=3$, and as follows in $u$.
For a genuine collision, \(\ell\le k-1\), so $u=0$ is allowed and is
the minimum.  Formula (45) then becomes exactly

\[
                  9-c+(\ell+1)\max(3-k+\ell,0)=\Omega.    \tag{46}
\]

Thus \(\Omega>0\) contradicts (44) and proves Theorem 1.1.  Equality in
(46) is the sharp boundary of this Wronskian count: it does not by itself
close the next value of $c$.

## 7. Audit

[verify_live_three_zero_higher_split_collision_exchange_wronskian.py](../computations/verify_live_three_zero_higher_split_collision_exchange_wronskian.py)
checks the exact legality criterion against every small multiplicity
profile, the Hermite degrees, the cubic rational-function lift, the zero
anchor convention, all exchange and infinity degrees, the stationary
multiplier dimension, the local coefficient-pairing ranks for every gcd
order, the full Wronskian inequality and its reduction to (6), the
Vandermonde closure for $e\le2$, and the known seventh-split terminal
profiles.
