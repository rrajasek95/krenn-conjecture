# Off-target scalar-unit resonance forces a pure factor and a target-leaking radial kernel

## 1. Outcome

Work at a clean intrinsic scalar-unit good pair on $2h$ residual sites,
$h\geq3$, with the literal nine rows

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                    \tag{1}
\]

Put

\[
 Q=q^{[h]},\quad D=\operatorname {span}\{X_a,X_b,X_c\},
 \quad r=R_{aa},\quad G=\alpha q+r,
\]

and assume

\[
 G^{[h]}=\alpha^{h-1}X_a.                              \tag{2}
\]

As usual,

\[
 \Theta=G^{[h-1]}-\alpha^{h-1}q^{[h-1]}=rH,            \tag{3}
\]

where $H$ is the literal divided-difference carrier.  Suppose
$Q\notin D$ and every entry $Z_{jk}$, $j,k\in\{b,c\}$, is annihilated
by every selector $\nu\in{\cal A}_i(Q)$ for each of the three labels $i$.
The affine-selector theorem then gives scalars \(\lambda_{jk}\), for
\(j,k\in\{b,c\}\), such that

\[
                         R_{jk}rH=\lambda_{jk}Q.         \tag{4}
\]

At the anchor-first lexicographic representative, the matrix
\(\Lambda=(\lambda_{jk})\) is nonzero: otherwise the exact scalar-unit
pivot raises the mutual-anchor potential.  The full-nine and exceptional
rows now impose the following normal form.

> **Theorem 1.1 (off-target radial quotient).**  For a complementary cap
> coefficient matrix $K=(K_{jk})$, put
> \[
>  R_K=\sum_{j,k\in\{b,c\}}K_{jk}R_{jk},\quad
>  \lambda(K)=\sum_{j,k}K_{jk}\lambda_{jk},\quad
>  T_K=K_{bb}X_b+K_{cc}X_c.
> \]
> Then
> \[
>  \boxed{R_KrH=\lambda(K)Q,\qquad
>         R_Kq^{[h-1]}=T_K.}                            \tag{5}
> \]
> Consequently the radial kernel
> \(\mathcal K=\ker\lambda\subset\operatorname {Mat}_2\) has
> dimension three, but the old target map does not vanish identically on it:
> \[
>       \boxed{T(\mathcal K)\ne0.}                     \tag{6}
> \]
> More precisely,
> \[
> \dim T(\mathcal K)=
> \begin{cases}
> 2,&(\lambda_{bc},\lambda_{cb})\ne(0,0),\\
> 1,&(\lambda_{bc},\lambda_{cb})=(0,0).
> \end{cases}                                           \tag{7}
> \]
> The kernel contains a normal direction with both complementary diagonal
> entries nonzero, so $E_{aa}+zK$ is active for $z\ne0$, unless
> \(\Lambda\) is supported on exactly one of $E_{bb},E_{cc}$.

Thus multiplication by the full carrier $rH$ is already nonfaithful on
the literal complementary response span, and the same kernel direction is
detected by a nonzero pure or mixed target at the adjacent old power.  A
carrier-cancellation argument cannot close this branch.

There is also an exact pure-factor consequence.  Choose any
\((u,v)\in\{b,c\}^2\) with \(\lambda_{uv}\ne0\), and put

\[
 C_{uv}=q^{[h-1]}+{\alpha\over\lambda_{uv}}R_{uv}H.     \tag{8}
\]

Then the exceptional row and (4) give

\[
                       \boxed{p_as_aC_{uv}=X_a.}        \tag{9}
\]

The two selected off-diagonal rows give a simultaneous primitive-square
packet.  Namely, with

\[
 A_{uv}=R_{ua}=p_us_a,\qquad B_{uv}=R_{av}=p_as_v,
\]

one has

\[
 \boxed{A_{uv}q^{[h-1]}=B_{uv}q^{[h-1]}=0,qquad
        A_{uv}B_{uv}H=\lambda_{uv}Q.}                  \tag{9a}
\]

Thus the off-target power is recovered by the product of two literal
rank-one $q^{[h-1]}$-primitive responses.  The obstruction is already a
lower-power zero-divisor square, not absence of physical provenance.

In particular each selected star form has a literal $a$-pure local
component: for some residual sites $x,y$,

\[
 (p_a)_x\in\mathbb C^*e_a^{(x)},\qquad
 (s_a)_y\in\mathbb C^*e_a^{(y)}.                       \tag{10}
\]

This does not force $x\ne y$, single-site support, or a partition
factorization.  If $(p_a)_x=c e_a^{(x)}$, the exact unresolved term is

\[
 K_x=s_aC_{uv}-c^{-1}X_a^{\widehat x},qquad p_aK_x=0.  \tag{11}
\]

There is a symmetric class in \(\ker m_{s_a}\).  These multiplication
kernels are the first uncontrolled factors after the pure target is
exposed; no certified argument currently shows that they are zero.
Nor is $C_{uv}$ known to be an $(h-1)$-st matching power of a residual
quadratic, so (9) is not a raw order descent.

Finally, the off-target class cannot be removed by the target-only
generalized pivot.  With $q^\sharp=\alpha^{-1}G$,

\[
 R_{jk}(q^\sharp)^{[h-1]}
   =\delta_{jk}X_j+\alpha^{1-h}\lambda_{jk}Q.           \tag{12}
\]

Invertible changes of the two surviving complementary endpoint rows send
the coefficient of $Q$ to
\(L\Lambda R^{\mathsf T}\), which is nonzero.  Direct terms at the fixed
base $q^\sharp$ contribute only $X_a$.  Since $Q\notin D$, no
such complementary rewrite or target-preserving gauge makes (12) exact.
A successful generalized pivot must first change the internal quadratic
by a source-valid radial rewrite; it cannot be obtained by gauging this
packet.

This is a sharp structural normal form, not an order descent or a proof of
Krenn's conjecture.

## 2. Proof of the radial quotient and target leakage

Equation (5) is just the linear contraction of (1), (3), and (4).  It is
important that both equalities are literal: no power of $q$, $Q$, or
$H$ is cancelled.

The target image of \(\ker\lambda\) is elementary but useful.  If an
off-diagonal coefficient of \(\Lambda\) is nonzero, arbitrary prescribed
values of $K_{bb},K_{cc}$ can be completed by one off-diagonal entry to
satisfy \(\lambda(K)=0\).  Hence the image is all of
\(\operatorname {span}\{X_b,X_c\}\).  If both off-diagonal coefficients
vanish, the only diagonal condition is

\[
                \lambda_{bb}K_{bb}+\lambda_{cc}K_{cc}=0. \tag{13}
\]

Because \(\Lambda\ne0\), its solution image is a nonzero line: it is the
mixed line
\(\mathbb C(\lambda_{cc}X_b-\lambda_{bb}X_c)\) when both
diagonal coefficients are nonzero, and the other coordinate target line
when exactly one is nonzero.  This proves (6)--(7).  The same calculation
shows that both diagonals can be chosen nonzero except when (13) is one
nonzero coordinate equation and there is no off-diagonal coefficient to
absorb it.  Every direction with nonzero target image is also a nonzero
literal response quadratic, by the second equality in (5).

For a kernel direction $K$ with both diagonals nonzero, the full normal
jet therefore gives the exact stationary active line

\[
 {\cal E}(E_{aa}+zK)
   =\sum_{m=2}^h z^m R_K^{[m]}G^{[h-m]}.                \tag{13a}
\]

Every $z\ne0$ is active, while the first normal coefficient vanishes.
Equation (13a) is not a clean-root theorem: its vector coefficients can
still have no common nonzero root.  The sole branch without such a
stationary active direction is the single-coordinate diagonal spike in
Theorem 1.1.

Equivalently, normalization at one nonzero entry gives the literal
torsion representatives

\[
 S_{jk}=R_{jk}-{\lambda_{jk}\over\lambda_{uv}}R_{uv},
 \qquad S_{jk}rH=0,                                    \tag{14}
\]

with the fully routed old responses

\[
 S_{jk}q^{[h-1]}
  =\delta_{jk}X_j
    -{\lambda_{jk}\over\lambda_{uv}}
       \mathbf 1_{u=v}X_u.                              \tag{15}
\]

When $u\ne v$, two such kernel directions still carry the two separate
pure targets.  When $u=v$, one direction carries either the other pure
target or a nonzero two-target difference.  Formula (15) is the precise
target leakage which a source lift must retain.

For the chosen nonzero entry, the remaining selected row and column of
the full-nine table are exactly (9a): both factors vanish against the old
matching power separately, but their product survives against $H$.  No
inference from either zero row can therefore divide out $q^{[h-1]}$ or
replace $H$ by its leading $q^{[h-2]}$-term.

## 3. The pure factor and its sharp kernel ambiguity

The exceptional row of (1) is

\[
                   \alpha Q+r q^{[h-1]}=X_a.           \tag{16}
\]

Substitute \(Q=\lambda_{uv}^{-1}R_{uv}rH\) from (4).  Commutativity and
the literal Segre square give

\[
 r\left(q^{[h-1]}+{\alpha\over\lambda_{uv}}R_{uv}H\right)
 =X_a,
\]

which is (9), with

\[
 R_{uv}rH=R_{ua}R_{av}H.                               \tag{17}
\]

Thus every nonzero coefficient of the radial entry has the common
four-star localization $p_u,s_a,p_a,s_v$ against one coefficient of the
same $H$-complement.  This is before evaluation by a selector and before
any attempted power cancellation.

We use the standard pure-factor lemma.  In the top component of the
site-square-zero algebra, if a global one-site form $L=\sum_zL_z$
satisfies

\[
                         LF=\rho X_a,\qquad\rho\ne0,    \tag{18}
\]

then $L_z\in\mathbb C^*e_a^{(z)}$ for some site $z$.  Indeed, quotient
each local colour space by \(\mathbb CL_z\).  The left side becomes zero.
If no $L_z$ is on the $a$-coordinate line, every factor of the pure
tensor $X_a$ remains nonzero in its local quotient, a contradiction.
Apply this first to $p_a(s_aC_{uv})=X_a$, and then to
\(s_a(p_aC_{uv})=X_a\), to prove (10).

For a chosen $x$ as in (10), multiplication by $p_a$ sends
\(c^{-1}X_a^{\widehat x}\) exactly to $X_a$: the $x$-component gives
the target, while every other component collides with the already occupied
site.  Subtraction from (9) proves (11).

The kernel term can be nonzero even in a uniform literal factorization.
On any site set containing $0,1$, choose a one-site vector
\(u\notin\mathbb Ce_a^{(1)}\), and put

\[
 p=e_a^{(0)}+u,\qquad
 s=e_a^{(0)}+e_a^{(1)}-u,\qquad
 C=X_a^{\widehat{\{0,1\}}}.                            \tag{19}
\]

Same-site products vanish, while the two opposite assignments at sites
$0,1$ add to $e_a^{(0)}e_a^{(1)}$.  Hence

\[
                              psC=X_a.                  \tag{20}
\]

Both forms have two-site support, their only $a$-pure local component is
at the common site $0$, and the two non-pure terms cancel.  Thus (9)
cannot be sharpened to distinct pure sites or a split factor without a
new theorem killing (11).

The primitive-square phenomenon in (9a) is also sharp in the literal
site algebra at its leading layer.  On six one-colour coordinates write

\[
 q=e_{01}+e_{23}+e_{45},\quad
 A=(x_0+x_2)(x_1-x_3),\quad
 B=(x_0+x_4)(x_1-x_5).                                  \tag{20a}
\]

Then $A,B$ are rank-one products and direct expansion gives

\[
                   Aq^{[2]}=Bq^{[2]}=0,qquad ABq=-q^{[3]}. \tag{20b}
\]

Decorating the six coordinates by any prescribed word makes the last
term that same pure or mixed word.  This is a leading-carrier guard, not a
completion of the exceptional row; it shows that the two primitive zero
rows in (9a) are not themselves contradictory.

## 4. A literal off-target radial guard

The pure-factor and carrier conclusions are physically sharp before the
remaining full-nine compatibility is imposed.  Take $h=3$, \(\alpha=1\), residual sites
$0,\ldots,5$, and labels $a,b,c$.  Write
\(x_r^d\) for colour $d$ at site $r$, and set

\[
\begin{aligned}
q={}&x_0^ax_3^b+x_1^bx_5^a+x_2^ax_4^a
      +x_3^bx_4^a+x_3^ax_5^a+x_4^ax_5^a,\\
p_a={}&x_0^a,&s_a={}&x_1^a-x_2^a,\\
p_b={}&x_1^b,&s_b={}&x_0^c,\\
p_c={}&x_0^c,&s_c={}&x_3^b.
\end{aligned}                                           \tag{21}
\]

Both endpoint triples are linearly independent.  The quadratic $q$ has
the unique supported perfect matching $03|15|24$, so

\[
 Q=q^{[3]}=x_0^ax_1^bx_2^ax_3^bx_4^ax_5^a\notin D.     \tag{22}
\]

With $r=p_as_a=x_0^ax_1^a-x_0^ax_2^a$, the only two response
complements give

\[
                         rq^{[2]}=X_a-Q,qquad r^{[2]}=0. \tag{23}
\]

Thus the exceptional row and unary clean equation both hold:

\[
                  Q+rq^{[2]}=X_a,qquad(q+r)^{[3]}=X_a. \tag{24}
\]

Here $H=q+\tfrac12r$ and \(\Theta=rH=rq\).  The complementary packet is

\[
 R_{bc}\Theta=-Q,qquad
 R_{bb}\Theta=R_{cb}\Theta=R_{cc}\Theta=0,             \tag{25}
\]

and the old off-diagonal row used by the nonzero entry is literal:

\[
                         R_{bc}q^{[2]}=0.                \tag{26}
\]

The two selected factors reveal the first omitted full-nine condition:

\[
             R_{ba}q^{[2]}=-Q,\qquad R_{ac}q^{[2]}=Q,   \tag{26a}
\]

whereas an exact chart would require both to vanish as in (9a).

The nonzero term in (25) occupies the four star sites $1,2,0,3$, in
the order $p_b,s_a,p_a,s_c$, and uses the common carrier cell
$x_4^ax_5^a$.  Moreover

\[
       r\bigl(q^{[2]}-R_{bc}H\bigr)=X_a,                \tag{27}
\]

which is (9) for \(\lambda_{bc}=-1\).  This guard retains literal
factorization, goodness, the exceptional row, clean unary data, an actual
off-target radial jet, its four-site carrier, and its corresponding old
zero row.  Two further off-diagonal rows vanish by site collision, but
five rows fail, so this is not a Krenn counterexample.  Its role is only
to show that the pure-factor and
localization steps themselves do not contradict physical occupancy.

## 5. Scope and audit

The theorem retains the full-nine chart: (5) uses all four complementary
rows, (9) uses the exceptional row, and (9a) uses the selected row and
column through every nonzero radial entry.  Maximum-anchor extremality is
used only to make
\(\Lambda\ne0\); goodness makes the basic pivot's anchor gain strict and
the endpoint triples injective.  No dual is extended through a product,
and no matching power, $Q$, or carrier is cancelled.

The exact remaining obstruction is now twofold but lives at one interface:

1. the radial carrier quotient has the nonzero target-leaking kernel
   (6)--(7); and
2. the pure inverse has the multiplication-kernel ambiguity (11).

A source-valid radial rewrite must kill these kernel classes while changing
the internal quadratic, preserve all nine adjacent-power rows and the
anchor stratum, and only then apply a generalized pivot.  The fixed-base
endpoint rewrite is impossible by (12).

The dependency-free checker
[`verify_scalar_unit_off_target_radial_quotient_pure_factor.py`](../computations/verify_scalar_unit_off_target_radial_quotient_pure_factor.py)
audits the target-leakage ranks and active-direction fork, the pure-factor
kernel guard, every coefficient in (21)--(27), both star ranks, the Segre
square, and the four-site localization.  It uses explicit exceptions and
runs unchanged under `python -O`.

This note is a theorem and a sharp no-go for carrier cancellation and
fixed-base complementary rewrites on the off-target radial branch.
It is not a clean-cap theorem, a raw order descent, or a proof of Krenn's
conjecture.
