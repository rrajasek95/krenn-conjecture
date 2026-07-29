# Nonzero-star erasure on the exact-nine $K_{3,3}$ frontier

## 1. Result

Work in the four-site square-free algebra

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad \dim V_i=3,                    \tag{1}
\]

over a characteristic-zero field.  Let $U,W$ be three-spaces, let
$K\subset U$ and $L\subset W$ be arbitrary planes, and put

\[
 p_x=\sum_iP_ix,\qquad s_y=\sum_iS_iy.                \tag{2}
\]

**Theorem 1.1 (three nonzero exceptional components).**  Suppose every
$S_i$ and $P_3$ is an isomorphism, while

\[
                         P_0,P_1,P_2\ne0              \tag{3}
\]

are otherwise arbitrary.  If $q\in\mathcal R_2$ satisfies

\[
 q p_xs_y=0\qquad(x\in K\text{ or }y\in L),           \tag{4}
\]

then $q=0$.

The planes $K,L$ are unrelated.  In particular, normalizing the four
$S_i$ does not also normalize $P_3$ or align the erased planes.  No
simultaneous normal form for $P_0,P_1,P_2$ is used.

There are sharp one- and two-zero extensions.

**Theorem 1.2 (one literal zero).**  Suppose $P_h=0$ for one
$h\in\{0,1,2\}$, the other two maps among $P_0,P_1,P_2$ are nonzero,
and every $S_i,P_3$ is invertible.  Every kernel vector in (4) vanishes
on the three blocks incident with $h$.  More precisely, any residual is
supported only on the two edges from the other exceptional sites to site
$3$.

**Theorem 1.3 (two literal zeros).**  Suppose $P_h=P_k=0$ for distinct
$h,k\in\{0,1,2\}$, let $i$ be the remaining site in
$\{0,1,2\}$, and assume $P_i\ne0$.  If every $S_j$ and $P_3$ is
invertible, the kernel in (4) is exactly

\[
                              V_i\otimes V_3.          \tag{4a}
\]

In particular every residual is supported only on edge $i3$, and all
blocks incident with either zero site vanish.

The exact audit is
[`verify_two_k4_k33_nonzero_star_erasure.py`](../computations/verify_two_k4_k33_nonzero_star_erasure.py).

Applied to the residual exact-nine position mask

\[
                         012\mid012\mid012\mid\varnothing,          \tag{5}
\]

these theorems force every block in the top-left $K_{3,3}$ to be literal
zero.  Its nonzero cross graph then has matching number two, contradicting
the proved low-matching obstruction.  Combined with the exact-nine frontier
census, this closes exact nine:

\[
 \boxed{\#\{(i,j):\det B_{ij}=0\}\ge10}.              \tag{5a}
\]

## 2. Three elementary coefficient kernels

We use three small square-free multiplication facts.  They are recorded
explicitly because all rank degeneracies matter.

### 2.1 A two-plane star in four sites

Let $M$ be a two-plane and let $R_i:M\to V_i$, with $R_3$
injective.  Put $r_x=\sum_iR_ix$ and

\[
 A=\{i\in\{0,1,2\}:R_i=0\}.                           \tag{6}
\]

Assume every $R_i$ outside $A$ is nonzero.  Direct coefficient
comparison in $H r_x=0$ for $H\in\mathcal R_2$ gives

\[
\begin{array}{c|c|c}
|A|&\dim\{H:Hr_M=0\}&\text{support}\ \hline
0&0&0\\
1&1&\text{the triangle complementary to }A\\
2&9&\text{the edge joining the two active sites}\\
3&27&\displaystyle\bigoplus_{h=0}^2V_h\otimes V_3.
\end{array}                                            \tag{7}
\]

For $|A|=1$, the generator is the three-site Koszul boundary

\[
 \Omega_R=(R_iu\,R_jv-R_iv\,R_ju,
           -R_iu\,R_3v+R_iv\,R_3u,
            R_ju\,R_3v-R_jv\,R_3u),                  \tag{8}
\]

for a basis $u,v$ of $M$, with the three displayed blocks ordered
$ij,i3,j3$.

Here is a short proof of the table.  Choose generic $x\in M$, so every
active $R_ix$ is nonzero.  The kernel of multiplication by this single
linear element is obtained by pure-factor cancellation on each triangle.
If no component vanishes, write

\[
 H_{ij}=z_{ij}R_ix\otimes R_jx,\qquad
 z_{ij}+z_{ik}+z_{jk}=0.                              \tag{9}
\]

Use an independent $x'\in M$.  Projection of the $ij3$ equation
modulo $\mathbb F R_3x$ kills $z_{ij}$; the three remaining odd-cycle
relations kill every $z_{i3}$.  This gives the first row of (7).

With one zero component, the same triangle comparison kills every block
incident with the zero site, and the standard three-site two-plane kernel
is the line (8).  With two zero components, comparison for $x,x'$ kills
the two Koszul bridges and leaves precisely the block on the active edge.
With three zero components, multiplication repeats site $3$ on the three
edges $h3$, while every block among $0,1,2$ is detected.  This proves
(7) without choosing normal forms for two different maps.

### 2.2 Multiplication by a three-site plane boundary

In the $|A|=1$ row, write the two nonzero nonregular maps as $R_i,R_j$.
The kernel of multiplication by $\Omega_R$ on arbitrary degree-one
elements has two cases:

\[
 \ker(\Omega_R\cdot)=
 \begin{cases}
   \{(R_iz,R_jz,R_3z):z\in M\},&\text{normally},\\
   \{(\lambda a,\lambda b,w):\lambda\in\mathbb F,
                  w\in V_3\},&\text{exceptionally}.
 \end{cases}                                           \tag{10}
\]

The exceptional case occurs exactly when $R_i,R_j$ both have rank one
and the same kernel in $M$.  If $u$ is outside that common kernel and
$v$ spans it, then $a=R_iu,b=R_ju$, the $ij$ block of $\Omega_R$
is zero, and its other two blocks are nonzero pure tensors with common
factor $R_3v$.  Equation (10) then follows immediately.  Outside this
case, the coefficient proof of the plane-boundary kernel is the same as
Lemma 4.4 of
[`two-k4-exact-eight-checkerboard-hessian-obstruction.md`](two-k4-exact-eight-checkerboard-hessian-obstruction.md):
projection to the three image planes leaves two common source
coefficients, hence exactly $R(M)$.

### 2.3 A cubic killed by a regular two-plane

Let every $S_i:W\to V_i$ be invertible and restrict $s$ to a plane
$L\subset W$.  Suppose a cubic $T$ has zero component on the triangle
$012$, so every nonzero component contains site $3$.  Then

\[
 T s_y=0\quad(y\in L)
 \quad\Longleftrightarrow\quad
 T=\Omega_{S,L}^{012}\otimes v_3
                         \quad(v_3\in V_3),            \tag{11}
\]

where $\Omega_{S,L}^{012}$ is the quadratic Koszul boundary of the three
injective plane maps $S_0|_L,S_1|_L,S_2|_L$.  The kernel in (11) has
dimension three.  This follows by comparing first the coefficients with
two output directions transverse to the three image planes; the remaining
three alternating scalars agree with signs $(+,-,+)$.  The checker verifies
the complete 81-column map and the displayed basis exactly.

## 3. The full regular star removes the determinant response

Because every $S_i$ is invertible, the degree-three annihilator of the
full star $s(W)$ is the generalized determinant line
$\mathbb F\Omega_S$.  Consequently the six-cell slab $K\times W$ in
(4) gives a linear form $\rho\in K^*$ with

\[
                         q p_x=\rho(x)\Omega_S
                                      \qquad(x\in K).  \tag{12}
\]

We claim that $\rho=0$.  Otherwise choose a basis $x_0,x_1$ of $K$
with $\rho(x_0)=0$, and put

\[
                         a_i=P_ix_0,\qquad b_i=P_ix_1. \tag{13}
\]

Since $P_3$ is invertible, $a_3\ne0$ and $a_3,b_3$ are independent.
On every three-site subset $J$, equations (12) read

\[
 q_Ja_J=0,\qquad
 q_Jb_J=\rho(x_1)(\Omega_S)_J.                        \tag{14}
\]

Suppose first that all three $a_i$, $i\in J$, are nonzero, and let $h$
be the fourth site.  If $a_h\ne0$, the full four-site fixed-star
comparison (9) gives $q_{uv}=z_{uv}a_u\otimes a_v$ on every edge.  Thus
the tensor $q_Jb_J$ has mode-$i$ factors only in
$\operatorname{span}(a_i,b_i)$ and has mode rank at most two.  It cannot
equal $(\Omega_S)_J$, whose three mode ranks are all three.

If instead $a_h=0$, the $hij$ component of $q p_{x_0}=0$ is

\[
                    q_{hi}a_j+q_{hj}a_i=0
                         \qquad(i,j\in J).             \tag{15}
\]

Quotienting successively by $\mathbb Fa_i$ and $\mathbb Fa_j$ writes
$q_{hi}=t_i\otimes a_i$ and $q_{hj}=t_j\otimes a_j$, with
$t_i+t_j=0$.  The three pair equations on $J$ form an odd cycle, so
every $t_i=0$ and hence every block incident with $h$ is zero.  On the
triangle $hij$, the second equation in (14) is now just
$q_{ij}b_h$.  Its mode-$h$ rank is at most one, whereas the determinant
tensor has mode-$h$ rank three, again a contradiction.

It follows that every three-site subset contains a zero component of
$a$.  Since $a_3\ne0$, at least two among $a_0,a_1,a_2$ vanish; call
them $a_i,a_j$.  On the triangle $ij3$, the first equation in (14) gives
$q_{ij}a_3=0$, hence $q_{ij}=0$.  The second lies in

\[
 V_i\otimes\mathbb Fb_j\otimes V_3
       +\mathbb Fb_i\otimes V_j\otimes V_3.           \tag{15a}
\]

After quotienting the first two modes by $\mathbb Fb_i,\mathbb Fb_j$,
the tensor in (15a) vanishes.  The projected determinant tensor does not:
both quotient spaces have dimension at least two, and a nonzero volume
form survives any such pair of line quotients.  This contradicts (14) and
proves

\[
                              q p_x=0\qquad(x\in K).    \tag{16}
\]

Notice that this argument retains the relative position of $P_3(K)$ and
$S_3(L)$; no alignment is being assumed.

## 4. Proof of Theorem 1.1

Put $R_i=P_i|_K$ and let $A$ be (6).  Choose $z\notin K$.  If
$h\in A$, then $P_h\ne0$ and $P_h|_K=0$, so

\[
                              u_h=P_hz\ne0.             \tag{17}
\]

Equation (16) and the table (7) leave four cases.

### 4.1 No axial component

If $A=\varnothing$, the first row of (7) gives $q=0$.

### 4.2 One axial component

Let $A=\{h\}$, let $J$ be the complementary triangle, and write
$q=\lambda\Omega_R$.  For $y\in L$, the remaining erased equations are

\[
 u_h\otimes(\Omega_R s_y^J)
       +S_hy\otimes(\Omega_R p_z^J)=0.                \tag{18}
\]

Choose $y\in L$ for which $S_hy$ is not proportional to $u_h$.
Pure-factor comparison in the $h\mid J$ flattening gives

\[
                \Omega_Rp_z^J=0,qquad
                \Omega_Rs_y^J=0.                     \tag{19}
\]

Equation (18) then gives the second equality for every $y\in L$.

In the normal row of (10), the first equality in (19) would put
$p_z^J=R(w)$ for some $w\in K$.  Its site-$3$ component says
$P_3z=P_3w$, impossible because $P_3$ is invertible and $z\notin K$.
In the exceptional row of (10), the plane $s^J(L)$ cannot lie in the
kernel: its component at either rank-one site spans a two-plane, whereas
the corresponding component in (10) is confined to a line.  Thus
$\lambda=0$.

### 4.3 Two axial components

Let $A=\{h,k\}$, with active sites $i,3$.  By (7), $q=q_{i3}$ is an
arbitrary block on that edge.  All active insertions repeat a site, so (4)
reduces to

\[
 q_{i3}\otimes
   \bigl(u_h\otimes S_ky+S_hy\otimes u_k\bigr)=0
                                      \qquad(y\in L). \tag{20}
\]

If $q_{i3}\ne0$, pure-factor equality would put the two-plane $S_h(L)$
inside $\mathbb Fu_h$, impossible.  Hence $q=0$.

### 4.4 Three axial components

Write

\[
                    q=Q_0+Q_1+Q_2,qquad
                    Q_h\in V_h\otimes V_3.             \tag{21}
\]

Let $T=q(u_0+u_1+u_2)$.  It is a cubic supported only on triples
containing site $3$, and (4) says $Ts_L=0$.  By (11),

\[
                         T=\Omega_{S,L}^{012}\otimes v_3              \tag{22}
\]

for some $v_3\in V_3$.  If $v_3=0$, the three equations

\[
                         Q_hu_k+Q_ku_h=0               \tag{23}
\]

and the three-leg cancellation lemma kill every $Q_h$.

If $v_3\ne0$, project (22) modulo $\mathbb Fv_3$ at site $3$.
The same three-leg lemma shows $Q_h=t_h\otimes v_3$.  Cancelling the
nonzero $v_3$ leaves

\[
              (t_0+t_1+t_2)(u_0+u_1+u_2)
                         =\Omega_{S,L}^{012}.           \tag{24}
\]

Every block on the right has matrix rank two.  The rank-two factorization
lemma (Lemma 4.5 of the exact-eight note) says that (24) has no solution:
the first two edge equations make the third edge symmetric, whereas the
required boundary block is nonzero alternating.  This final contradiction
proves Theorem 1.1.

## 5. Proof of the one-zero extension

Let $P_h=0$, and let the other two exceptional maps be nonzero.  The
determinant-line argument in Section 3 is unchanged and again gives (16).
Now $h\in A$, but $u_h=0$.

If $A=\{h\}$, the one-axial residual is $\Omega_R$ on the complementary
triangle.  Equation (18) reduces to

\[
                         S_hy\otimes(\Omega_Rp_z^J)=0. \tag{25}
\]

The normal row of (10) is impossible by the site-$3$ component as before.
In the exceptional row, the $ij$ block of $\Omega_R$ is zero, so its
support consists only of the two edges $i3,j3$.

If one further map is axial on $K$, (7) leaves a block $q_{i3}$; the
nonzero outside component at the other axial site and the factor $S_hy$
force this block to vanish.  If all three restrictions vanish on $K$,
use (22).  The $hi$ equation is

\[
                         Q_hu_i=(\Omega_{S,L})_{hi}\otimes v_3.       \tag{26}
\]

Its left side has mode rank at most one at site $i$, while the right side
has rank two if $v_3\ne0$.  Thus $v_3=0$, and then $Q_h=0$.  The only
possible survivors are $Q_i,Q_j$, on edges $i3,j3$.  In every case all
blocks incident with $h$ vanish, proving Theorem 1.2.

## 6. Proof of the two-zero extension

Let $P_h=P_k=0$, and let $i$ be the remaining exceptional site.  First,
the determinant response in (12) still vanishes.  Indeed, if $\rho\ne0$,
choose $x_0,x_1$ as in (13).  On the triangle $hk3$ one has
$a_h=a_k=b_h=b_k=0$.  Restricting the two identities in (12) for
$x_0,x_1$ to this triangle first gives $q_{hk}a_3=0$, hence
$q_{hk}=0$ because $a_3\ne0$.  The $x_1$ identity then has zero left
side and the nonzero determinant tensor
$\rho(x_1)(\Omega_S)_{hk3}$ on the right, a contradiction.  Thus (16)
holds.

Put $R_i=P_i|_K$.  If $R_i\ne0$, then the two-axial row of (7) says
immediately that $q$ is an arbitrary block on $i3$.  Conversely, every
such block is invisible in (4): multiplication by $p_x$ either repeats
site $i$ or site $3$, since the components at $h,k$ are zero.

It remains to treat $R_i=0$.  Choose $z\notin K$ and put $u_i=P_i z$.
Because $P_i\ne0$ and its kernel contains the plane $K$, one has
$u_i\ne0$.  The three-axial row of (7) gives

\[
 q=Q_h+Q_k+Q_i,
 \qquad Q_t\in V_t\otimes V_3.                       \tag{26a}
\]

Set $T=q p_z$.  Only the $Q_hu_i$ and $Q_ku_i$ components can occur, so
$T$ is supported on triples through site $3$ and its component with hole
$i$ is zero.  The remaining erased equations say $T s_y=0$ for every
$y\in L$.  By (11),

\[
                         T=\Omega_{S,L}^{012}\otimes v_3.           \tag{26b}
\]

Every one of the three hole components of the right side is a nonzero
rank-two boundary block when $v_3\ne0$.  Since the hole-$i$ component of
$T$ is zero, (26b) forces $v_3=0$ and hence $T=0$.  Injectivity of tensoring
with $u_i\ne0$ now gives $Q_h=Q_k=0$.  The block $Q_i$ is invisible for
the reason above and is arbitrary.  This proves that the kernel is exactly
$V_i\otimes V_3$, and proves Theorem 1.3.

## 7. Consequence for the exact-nine $K_{3,3}$

In (5), pair one of the first three block rows with the completely
invertible row $3$.  Fix the complementary two rows to their common
internal color $c$, and form the actual two-/four-cross quadratic

\[
 q_{\mathrm{eff}}
   =\lambda_{ab}q_R+p_{a,c}p_{b,c},                  \tag{27}
\]

where $\lambda_{ab}\ne0$.  The eight nonconstant color cells give exactly
(4).  There are three possibilities whenever the selected row contains a
nonzero singular block:

- if all three blocks are nonzero, Theorem 1.1 gives
  $q_{\mathrm{eff}}=0$;
- if exactly two are nonzero, Theorem 1.2 makes all three blocks of
  $q_{\mathrm{eff}}$ incident with the zero endpoint vanish;
- if exactly one is nonzero, Theorem 1.3 supports $q_{\mathrm{eff}}$ only
  on the edge from that site to site $3$, so all three blocks incident
  with either zero endpoint vanish.

Each conclusion is impossible by the endpoint-plane obstruction.  At a
right endpoint $h$ where the three incident effective blocks vanish, the
three blocks of $\lambda_{ab}q_R$ have endpoint lines

\[
 \mathbb F\bigl(\lambda_{ab}\rho_{hj}
       e_{\kappa(hj)}\bigr),\qquad j\ne h,            \tag{28}
\]

where every right-edge weight $\rho_{hj}$ is nonzero.  These are the three
distinct coordinate lines and span dimension three.  Every incident block
of the product correction in (27), however, has its endpoint image in the
fixed plane

\[
 \operatorname{span}\!\left(
   \operatorname{row}_c(B_{ah})^{\mathsf T},
   \operatorname{row}_c(B_{bh})^{\mathsf T}\right).  \tag{29}
\]

The vanishing effective blocks would put all three lines (28) in (29), a
contradiction.  Thus a selected top-left row cannot contain even one
nonzero singular block.  Applying this to each of the first three rows
forces all nine top-left $K_{3,3}$ blocks to be literal zero.

The nonzero cross graph then consists only of the seven blocks through
left site $3$ or right site $3$.  Its matching number is exactly two.
To invoke the unit-shore form of the low-matching obstruction, fix a color
and let its two complementary internal edge weights be $\alpha,\beta$.
Their constant-word coefficient gives $\alpha\beta=1$.  Choose nonzero
diagonal local scalars $d_{u,c}$ so that
$\alpha d_{u,c}d_{v,c}=\beta d_{r,c}d_{s,c}=1$ on those two edges.
Their product over the four sites is automatically one, so this local
change preserves the GHZ tensor.  Applying the change independently on
both shores multiplies every cross block by invertible diagonal matrices;
it preserves literal zeros, singularity, and the nonzero position graph.
The proved unit-weight low-matching obstruction now gives a contradiction.
The exact-nine frontier census already excludes the other eight position
orbits, so exact nine is impossible and (5a) follows.

## 8. Exact audit

Run

```text
python computations/verify_two_k4_k33_nonzero_star_erasure.py
```

The checker verifies:

1. the four plane-star annihilator strata (0,1,9,27), including literal
   residual supports;
2. both kernels in (10), of dimensions two and four;
3. the three-dimensional supported cubic annihilator (11);
4. both determinant-response branches in Section 3: fixed-star nullities
   two and eight, incident-block vanishing in the axial case, and exact
   augmented-rank inconsistency with the determinant response;
5. full rank of the eight-cell map in 666 exact nonzero-map cases,
   including 648 rank-one configurations with three unrelated choices
   of $P_3(K)$, and eighteen mixed rank-two configurations;
6. the one-zero incident conclusion in 36 exact configurations;
7. the exact single-edge residual in 21 two-zero configurations;
8. the arbitrary-weight endpoint rank in (28); and
9. matching number two for the all-zero top-left $K_{3,3}$ graph.

Its final line is

```text
two-K4 K3,3 nonzero-star erasure audit: PASS
```
