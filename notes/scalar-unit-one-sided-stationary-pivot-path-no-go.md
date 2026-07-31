# The one-sided scalar-unit pivot is exact, but exceptional-row stationarity is not yet a filtered homotopy

## 1. Outcome

Work over a characteristic-zero field.  Fix $h\geq3$, a physical pair
$p,q$, and the complete endpoint-ordered rows

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                      \tag{1}
\]

Put

\[
 R=R_{aa},\qquad r=\alpha^{-1}R,\qquad
 q^\sharp=q+r,
\]

and

\[
 \begin{aligned}
 U&=(\alpha q+R)^{[h]}-\alpha^{h-1}X_a,\\
 \Theta&=(\alpha q+R)^{[h-1]}
              -\alpha^{h-1}q^{[h-1]}.
 \end{aligned}                                           \tag{2}
\]

Let \(\{a,b,c\}=\{0,1,2\}\), and assume the one-sided six-row
annihilation

\[
 U=0,
 \qquad R_{ij}\Theta=0
       \quad(i\in\{b,c\},\ j\in\{a,b,c\}).              \tag{3}
\]

There are two exact positive conclusions.

1. Replacing $q$ by $q^\sharp$, setting $p_a=0$, and retaining all
   three $s$-rows gives another exact ternary source on the same vertex
   set.  Thus (3) gives a genuine **one-sided pivot**.
2. Along the literal affine block path

   \[
         q_t=q+tr,\qquad p_a(t)=(1-t)p_a,                 \tag{4}
   \]

   with every other row fixed, all nine matching-row defects are visibly
   divisible by $t(t-1)$.  The exceptional $(a,a)$ defect has the
   stronger factor $t(t-1)^2$.  Its derivative at $t=1$ is zero.

The stronger proposed conclusion does **not** follow.  The hypotheses
certify exactness only at the endpoints of (4); they do not certify a curve
of exact sources.  (The displayed relations allow the interior defect
coefficients to vanish identically; no nonvanishing hypothesis rules this
out.)  Polynomial divisibility in the evaluated site algebra is not
membership in the literal boundary submodule of the source-filtered
five-site complex.
Moreover, the endpoint derivative has two uncontrolled selected-row
components, and the ordered-square part of that derivative depends on the
speed of the parametrization.  Ordinary integration of the full derivative
instead gives the zero endpoint difference.  Consequently (3)--(4) alone
neither construct the value $\lambda=0$ in the ordered-five-site lift
torsor nor prove zero indeterminacy.

The path is nevertheless useful.  Its endpoint derivative contains the
source-ordered square

\[
 \alpha^{-1}R_{ia}R_{aj}(q^\sharp)^{[h-2]},              \tag{5}
\]

and its coefficientwise integral is the exact adjacent-power comparison

\[
 \alpha^{1-h}\Theta
   =(q^\sharp)^{[h-1]}-q^{[h-1]}
   =\int_0^1 r q_t^{[h-2]}\,dt.                          \tag{6}
\]

Thus (4) nominates a concrete Chern--Simons-shaped candidate for the
missing comparison.  Turning it into a transgression still requires a
filtered cross-complement chain map, literal boundary membership for the
other row defects, the zero-lower-response target lift, and a
zero-indeterminacy theorem.  Those are additional data, not consequences
of the stationary factor.

This is a sharp no-go for the stated inference, not a no-go for a future
path/Rees construction and not a proof of Krenn's conjecture.

## 2. The endpoint pivot is an exact source

Since $\alpha q+R=\alpha q^\sharp$, equations (2)--(3) give

\[
 \alpha^h(q^\sharp)^{[h]}=\alpha^{h-1}X_a,
 \qquad
 \Theta=\alpha^{h-1}\bigl((q^\sharp)^{[h-1]}
                                      -q^{[h-1]}\bigr).   \tag{7}
\]

Hence

\[
             \alpha(q^\sharp)^{[h]}=X_a.                 \tag{8}
\]

For $i\in\{b,c\}$ and every $j$, the second equality in (7), (3),
and the old row (1) give

\[
 R_{ij}(q^\sharp)^{[h-1]}
    =R_{ij}q^{[h-1]}=\delta_{ij}X_i.                      \tag{9}
\]

After $p_a$ is set to zero, all response rows with first endpoint colour
$a$ vanish.  Equation (8) restores the $(a,a)$ target, and the two
off-diagonal $a$-rows have zero target.  Equations (8)--(9) therefore
check all nine rows of the transformed source.  No $s_j$ is removed,
no matching power is divided out, and no surviving star row is cancelled
from an equality.

If the original pair is good, the transformed $p$-star has rank two and
the transformed $q$-star still has rank three.  The direct block
$\alpha E_{aa}$ is consequently essential at $p$, while $p$ is not
essential at $q$: this is genuinely one-sided, unlike the complementary
pivot which removes both selected endpoint rows.

There is also a small support consequence.  If the original source has
globally minimum aggregate-entry support and

\[
 \mu=|\operatorname{supp}p_a|,
 \qquad \nu=|\operatorname{supp}s_a|,
\]

then exactness of the pivot forces

\[
 |\operatorname{supp}q^\sharp|-|\operatorname{supp}q|
       \geq\mu,
 \qquad
 |\operatorname{supp}q^\sharp|-|\operatorname{supp}q|
       \leq|\operatorname{supp}R|\leq\mu\nu.            \tag{10}
\]

This accounting is a structural cost, not a filtered transgression.

## 3. The full nine-row path-defect ledger

Let

\[
 c_i(t)=\begin{cases}1-t,&i=a,\\1,&i\in\{b,c\},\end{cases}
\]

and retain the target throughout the path.  The row and its defect are

\[
 \begin{aligned}
 F_{ij}(t)&=\alpha\delta_{ia}\delta_{ja}q_t^{[h]}
              +c_i(t)R_{ij}q_t^{[h-1]},\\
 D_{ij}(t)&=F_{ij}(t)-\delta_{ij}X_i.                    \tag{11}
 \end{aligned}
\]

The divided-power binomial formula is

\[
 q_t^{[m]}=\sum_{k=0}^{m}t^kq^{[m-k]}r^{[k]}.            \tag{12}
\]

### 3.1 The six complementary first-endpoint rows

Take $i\in\{b,c\}$, any $j$, and put $m=h-1$.  From (1), (7),
and (3),

\[
 \begin{aligned}
 D_{ij}(t)
   &=R_{ij}\bigl(q_t^{[m]}-q^{[m]}\bigr)\\
   &=\sum_{k=1}^{m}t^kR_{ij}q^{[m-k]}r^{[k]},\\
 \sum_{k=1}^{m}R_{ij}q^{[m-k]}r^{[k]}&=0.               \tag{13}
 \end{aligned}
\]

Subtracting $t$ times the last equality gives the literal factorization

\[
 \boxed{
 D_{ij}(t)=t(t-1)B_{ij}(t)}                              \tag{14}
\]

where

\[
 B_{ij}(t)=R_{ij}\sum_{k=2}^{h-1}
       (1+t+\cdots+t^{k-2})q^{[h-1-k]}r^{[k]}.           \tag{15}
\]

### 3.2 The two selected first-endpoint off-diagonal rows

For $j\in\{b,c\}$, the old off-diagonal row is
$R_{aj}q^{[h-1]}=0$.  Hence

\[
 \boxed{
 \begin{aligned}
 D_{aj}(t)&=(1-t)R_{aj}q_t^{[h-1]}\\
   &=t(1-t)C_{aj}(t),\\
 C_{aj}(t)&=R_{aj}\sum_{k=1}^{h-1}
       t^{k-1}q^{[h-1-k]}r^{[k]}.
 \end{aligned}}                                         \tag{16}
\]

No hypothesis in (3) says that $C_{aj}(1)$ is zero or a boundary.
These are the two selected-row leakage terms which are hidden if only the
exceptional diagonal is inspected.

### 3.3 The exceptional diagonal row

Divide the exceptional row by $\alpha$ and put

\[
 f(t)=q_t^{[h]}+(1-t)r q_t^{[h-1]}.
\]

For $k\geq1$, the coefficient of
$q^{[h-k]}r^{[k]}$ in $f(t)$ is

\[
 c_k(t)=t^{k-1}\bigl(k-(k-1)t\bigr).                    \tag{17}
\]

Thus $c_k(1)=1$ and $c_k'(1)=0$ term by term.  Direct differentiation
also gives

\[
                 f'(t)=(1-t)r^2q_t^{[h-2]}.              \tag{18}
\]

The old exceptional row says $f(0)=\alpha^{-1}X_a$, while $U=0$
says $f(1)=\alpha^{-1}X_a$.  Equivalently,

\[
       \sum_{k=2}^{h}q^{[h-k]}r^{[k]}=0.                 \tag{19}
\]

Using

\[
 c_k(t)-1=-(t-1)^2\sum_{\ell=0}^{k-2}(\ell+1)t^\ell
\]

and using (19) once more at $t=0$ gives

\[
 \boxed{
 D_{aa}(t)=-\alpha t(t-1)^2C_{aa}(t)}                   \tag{20}
\]

with

\[
 C_{aa}(t)=\sum_{k=3}^{h}
   \left(\sum_{\ell=0}^{k-3}(\ell+2)t^\ell\right)
       q^{[h-k]}r^{[k]}.                                 \tag{21}
\]

Equations (18) and (20) prove $F'_{aa}(1)=0$ and the advertised double
endpoint factor without root counting.  Together, (14), (16), and (20)
retain all nine rows and show that the full defect has a common
factor $t(t-1)$, with one additional $t-1$ in the exceptional row.

## 4. What the endpoint jet and path integral actually give

Because the target is constant, put

\[
                         Z_{ij}=D'_{ij}(1)=F'_{ij}(1).
\]

Equations (11) and (18) give the complete endpoint jet

\[
 \boxed{
 \begin{array}{rcll}
 Z_{aa}&=&0,\\[2mm]
 Z_{aj}&=&-R_{aj}(q^\sharp)^{[h-1]}
       =-\alpha^{1-h}R_{aj}\Theta,
       &j\in\{b,c\},\\[2mm]
 Z_{ij}&=&R_{ij}r(q^\sharp)^{[h-2]}
       =\alpha^{-1}R_{ia}R_{aj}(q^\sharp)^{[h-2]},
       &i\in\{b,c\},\ j\in\{a,b,c\}.
 \end{array}}                                           \tag{22}
\]

The last equality retains the named endpoint path

\[
 R_{ij}R_{aa}=R_{ia}R_{aj}
       =(p_i s_a)(p_a s_j).                              \tag{23}
\]

Commutativity proves (23), but does not transpose the $p$- and
$q$-endpoint slots.  Formula (22) is therefore a real physical
ordered-square jet.  Whenever one of its displayed nonexceptional
components is nonzero, (4) is not tangent to the exact-source locus at
$t=1$ and so cannot be a curve of exact sources near that endpoint.  The
hypotheses do not force such a component to be nonzero; in a degenerate
case an exact entire path is not ruled out.

Formal coefficientwise integration in characteristic zero gives (6).
For the six complementary rows, (3) says

\[
 \int_0^1R_{ij}r q_t^{[h-2]}\,dt=0.                    \tag{24}
\]

For every one of the nine full rows, the fundamental theorem instead gives

\[
                  \int_0^1F'_{ij}(t)\,dt
                     =F_{ij}(1)-F_{ij}(0)=0.             \tag{25}
\]

Thus ordinary path integration sends the full matching-image loop to zero.  To
retain the endpoint integrand (22) while (24)--(25) vanish is precisely to
ask for a secondary connecting morphism.  It is not ordinary integration.

There is also an exact parametrization guard.  Let
$\phi(0)=0$, $\phi(1)=1$, and run the same geometric block curve with

\[
 q_t^\phi=q+\phi(t)r,
 \qquad p_a^\phi(t)=(1-\phi(t))p_a.                      \tag{26}
\]

Then

\[
 {d\over dt}F_{aa}^\phi(t)
   =\alpha\phi'(t)(1-\phi(t))r^2
                         (q_t^\phi)^{[h-2]},             \tag{27}
\]

so the exceptional target is still stationary, while every nonexceptional
entry in (22) is multiplied by $\phi'(1)$.  The polynomial

\[
                         \phi(t)=2t-t^2                 \tag{28}
\]

has $\phi'(1)=0$, killing the whole endpoint jet.  Over $\mathbb C$, with
$t\in[0,1]$, it traverses the same real-parametrized segment; over an
arbitrary characteristic-zero field it is simply an endpoint-fixing
polynomial reparametrization.  More generally
$\phi_\mu(t)=t+(\mu-1)t(t-1)$ gives $\phi_\mu'(1)=\mu$.
Therefore endpoint stationarity is intrinsic, but the nonzero endpoint
speed is not.  A construction may choose the affine parameter in (4), but
that choice alone is not a zero-indeterminacy theorem.

### 4.1 The physical-coordinate two-sided pivot square

There is a useful two-parameter refinement.  Scale the selected rows by
$p_a(x)=xp_a$ and $s_a(y)=ys_a$, and put

\[
 z=xy,\qquad q_{x,y}=q+(1-xy)r=q^\sharp-zr.             \tag{29a}
\]

The four corners are the original source, the two one-sided pivots, and
the complementary two-sided pivot.  Under the standing equation $U=0$,
the corner $(0,1)$ is exact under (3), while $(0,0)$ needs only the four
complementary annihilations among the six in (3).  The opposite corner
$(1,0)$ is exact precisely when the reflected annihilations

\[
 R_{ij}\Theta=0
       \quad(i\in\{a,b,c\},\ j\in\{b,c\})          \tag{29b}
\]

also hold.  Thus, together with $U=0$, an exact four-corner square requires
the eight nonexceptional annihilations; it does not derive the two missing
ones.

Let $F_{ij}(x,y)$ be the evident analogue of (11), with response factor
$x^{\delta_{ia}}y^{\delta_{ja}}$, and form the literal mixed divided
difference

\[
 {\mathfrak M}_{ij}(x,y)=
 {F_{ij}(x,y)-F_{ij}(x,0)-F_{ij}(0,y)+F_{ij}(0,0)\over xy}.       \tag{29c}
\]

The numerator is polynomially divisible by $xy$.  At the double-pivot
corner it has the clean value

\[
 \boxed{
 {\mathfrak M}_{ij}(0,0)=
 \begin{cases}
 -\alpha^{-1}R_{ia}R_{aj}(q^\sharp)^{[h-2]},
       &i,j\in\{b,c\},\\
 0,&i=a\text{ or }j=a.
 \end{cases}}                                           \tag{29d}
\]

Indeed the complementary rows depend only on $z$, so (29d) is their
$z$-derivative at zero.  A selected row carries an additional factor
$x$ or $y$ and therefore vanishes in mixed bidegree $(1,1)$.  For the
exceptional row,

\[
 F_{aa}(z)=\alpha\bigl((q^\sharp-zr)^{[h]}
             +zr(q^\sharp-zr)^{[h-1]}\bigr),\qquad
 {dF_{aa}\over dz}=-\alpha z r^2(q^\sharp-zr)^{[h-2]},          \tag{29e}
\]

so its mixed value is zero by stationarity.  The square therefore removes
the two selected-row leakages from the lowest mixed bidegree and isolates
the ordered complementary square.

This is a better candidate representative, but not a new relation.  The
alternating four-corner equality is, row by row, exactly $U=0$ and the
annihilations $R_{ij}\Theta=0$.  Formula (29d) is their divided
difference, not a proof that its class is a literal boundary.  Its
normalization is canonical only after the physical scaling coordinates
$x,y$ and their bidegree are declared part of the source filtration:
replacing them by $\phi(x),\psi(y)$ scales (29d) by
$\phi'(0)\psi'(0)$.  Hence the square cures the affine one-path leakage,
but it neither constructs the filtered chain map nor removes the
$\lambda$/zero-indeterminacy problem below.

## 5. Sharp filtered no-go

### 5.1 A polynomial factor is not a literal boundary

Let $M$ be the actual all-label filtered row module, $N_{\rm lit}$ its
literal boundary submodule, and $\epsilon:M\to V$ the evaluated matching
map, with $N_{\rm lit}\subseteq\ker\epsilon$.  Equations (14), (16), and
(20) are identities in the evaluated
site algebra.  To use their quotients inside the source filtration one
needs the relative two-endpoint saturation statements, on the particular
path family $\mathscr U$,

\[
 \begin{aligned}
 \epsilon^{-1}\bigl(t(t-1)V[t]\bigr)\cap{\mathscr U}
   &=\bigl(N_{\rm lit}[t]+t(t-1)M[t]\bigr)\cap{\mathscr U},\\
 \epsilon^{-1}\bigl(t(t-1)^2V[t]\bigr)\cap{\mathscr U}_{aa}
   &=\bigl(N_{\rm lit}[t]+t(t-1)^2M[t]\bigr)
                                      \cap{\mathscr U}_{aa}.       \tag{30}
 \end{aligned}
\]

Even (30) only authorizes source-valid division.  To call the
connection/normal quotients literal boundaries one must further prove
that the all-label restrictions of $B_{ij}(t)$ and $C_{aj}(t)$ have
zero class modulo $N_{\rm lit}$.  None of these memberships occurs in
(1)--(4).

The logical gap already has a one-dimensional exact guard at $h=3$.
Let $z\ne0$ be a cycle and take the boundary submodule to be zero.  The
coefficient choices

\[
 \begin{array}{c|c|c}
 \text{row type}&\text{endpoint relation}&\text{defect}\\ \hline
 i\in\{b,c\}&M_1=z,\ M_2=-z&z(t-t^2),\\
 i=a,\ j\ne a&N_1=z&zt(1-t),\\
 (a,a)&M_2=z,\ M_3=-z&2\alpha zt(1-t)^2
 \end{array}                                             \tag{31}
\]

satisfy all the relevant endpoint and stationarity relations.  Their
displayed quotients are nonzero and are not boundaries.  This is a
universal filtered-module guard, not a claimed matching source; it proves
that root multiplicity alone cannot imply boundary membership.

### 5.2 The lift torsor is unchanged

Write $T$ for the exceptional target and $Z$ for the desired odd
response.  To make the logical scope explicit, take a formal filtered
extension with independent cycles $T,Z$ (and $Z\ne0$ on the branch where a
nonzero response is intended), and, for every scalar $\lambda$ in the
ground field, adjoin a cell $H$ with

\[
                         d_\lambda H=T+\lambda Z.         \tag{32}
\]

On the displayed directions put $F_0=\langle Z\rangle$ and
$F_1=\langle Z,T,H\rangle$.  Then $d_\lambda^2=0$, and all values of
$\lambda$ have the same associated-graded differential
$\operatorname{gr}(d_\lambda)H=T$.  The path identities (7)--(31) live in
the old source/evaluation module and specify no differential from a path
generator to $H$, $T$, or $Z$.  They can therefore be adjoined unchanged
to (32) for every $\lambda$, or direct-summed with this counterextension.
In particular, the stationary exceptional row sees no difference between
$\lambda=0$ and $\lambda=-1$.

The old same-power cell $S$ still has

\[
                         dS=T-Z.                         \tag{33}
\]

Even if one declares the affine path to produce one cell $H_{\rm path}$
with $dH_{\rm path}=T$,

\[
                 d(H_{\rm path}-S)=Z.                   \tag{34}
\]

Thus the desired response is an ordinary indeterminacy unless the source
filtration excludes $S$ from the comparison grade and the odd residue
vanishes on every difference of allowed path lifts.  A single chosen path
does not prove either assertion.

In particular, the affine parameter does not itself define a map from the
polynomial path module to this filtered extension.  Declaring
$dH_{\rm path}=T$ is exactly the choice $\lambda=0$; it is not a consequence
of (4), its endpoint jet, or coefficientwise integration.  This formal
counterextension is not asserted to be a matching source.  It shows only
that the stated source identities are compatible with every lower
coordinate until a source-provenant chain construction is supplied.

There is a further cross-complement issue.  The endpoint target belongs to
the complex built from $q^\sharp$, whereas the original odd response is
defined in the quotient built from $q$.  The identity map on the ambient
site algebra does not automatically descend between the following
quotients (here $q,q^\sharp$ denote their restrictions after the chosen
fifth site is exposed):

\[
 {\cal R}_{2h-1}/({\cal R}_1q^{[h-1]})
 \quad\text{and}\quad
 {\cal R}_{2h-1}/({\cal R}_1(q^\sharp)^{[h-1]}).         \tag{35}
\]

Equation (3) compares their denominators only after multiplication by the
six special quadratics $R_{ij}$; it gives no comparison for an arbitrary
linear numerator and no all-label five-site chain map.  Calling the
$q^\sharp$-target a zero-response lift in the $q$-quotient silently
assumes exactly the missing transport.

The carrier guards are consistent with this conclusion.  In the additional
clean intrinsic branch, the prior minimum-support unary-cap ledger gives
$\Theta=R H\ne0$; nothing in (1)--(4) alone forces $\Theta\ne0$.  When that
extra branch hypothesis is present, the one-sided assumptions put the
nonzero carrier in the annihilator of six rows.  Good-star injectivity does
not make multiplication by the carrier faithful.  Hence neither (24) nor
the ordered factorization (23) may be cancelled to manufacture the missing
comparison.

## 6. Exact additional datum and scope

A successful stationary-pivot construction must add the following
source-filtered data.

1. **A path/Rees comparison grade.**  Place the affine block path in a
   specified relative filtered complex, separate from the old same-power
   cell, and prove the two-endpoint saturation needed in (30).
2. **A cross-complement, all-label chain map.**  Construct a filtered map
   from the $q^\sharp$-complex to the $q$-complex, or their mapping
   cone, whose physical coefficient map is the ordered five-site
   restriction--insertion operation.  It must retain all outer
   $(i,j)$-rows and the ordered factors in (23).
3. **Literal boundary control.**  Prove that the images of every
   nonexceptional quotient in (15)--(16), including the two uncontrolled
   $C_{aj}$, lie in the literal connection/normal boundary submodule.
4. **The $\lambda=0$ target equation.**  Exhibit a cell
   $H_{\rm path}$ whose leading differential is $+T$, whose
   filtration-lowering odd coordinate is zero, and whose remaining
   connection/normal component is one of the literal boundaries in item
   3.  The double factor in (20) is a candidate principal part for this
   cell; it is not the cell itself.
5. **Zero indeterminacy.**  For any two cells satisfying items 1--4, prove
   that the odd residue of their difference is zero.  This must handle the
   same-power competitor (33), path loops, and reparametrizations such as
   (26)--(28).

Equivalently, what is missing is a source-provenant Gauss--Manin/Chern--
Simons transport along $q_t$ whose connecting map converts (6) into the
ordered physical response, sends (14) and (16) to boundaries, and is
injective on the surviving odd-response line.  The stationary pivot gives
the endpoints and the candidate integrand, but no such transport or
indeterminacy theorem.

The dependency-free checker
[`verify_scalar_unit_one_sided_stationary_pivot_path_no_go.py`](../computations/verify_scalar_unit_one_sided_stationary_pivot_path_no_go.py)
audits the endpoint source, all nine defect factors, the exceptional
coefficient and derivative formulas, the ordered endpoint jet, the
coefficientwise path integral, the two-sided mixed square, the
reparametrization guard, and the filtered torsor/cycle countermodels under
ordinary Python and
`python -O`.  The algebraic proofs above, not its finite order range, are
uniform in $h$.
