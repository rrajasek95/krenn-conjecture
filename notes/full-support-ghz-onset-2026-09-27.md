# Uniform fifth-power GHZ onset at every full-support single-color zero

September 27, 2026. **Written proof with exact supporting checks;
independent audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/full-support-ghz-onset-2026-09-27/README.md) ·
[Illustrated guide](../explainers/FULL-SUPPORT-ONSET.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. The full-support onset theorem

Let $A_0$ be a six-site single-ground-color zero with every ground
entry nonzero.

For every nearby ternary source, write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|.
$$

**Theorem.** There are constants and a neighborhood of $A_0$ such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5.}
\tag{1}
$$

This holds in every source direction and at every matrix rank.
No non-ground support, arm-size, or selected ground-cofactor
condition is imposed. Constants may depend on the fixed ground
source $A_0$.

Two arguments close the configurations left by the
[cofactor-graph classification](cofactor-graph-ghz-frontier-2026-09-27.md).
Sections 2--7 treat two anchored triangles joined by an anchored
bridge, using an exact response isometry on a balanced four-cycle.
Section 8 treats any anchored four-cycle by projecting away a
large outside edge. The final section combines the cases.

This completes the full-support single-color **source-distance
onset** bound. It does not establish the error-versus-signal
inequality required for the unrestricted square-root rate law.

## 2. A balanced flat four-cycle has an isometric attachment response

Consider four core sites $0,1,2,3$ with arbitrary finite local
color spaces. Only edges $01,03,12,23$ are present, every block
has Frobenius norm one, and their four-site matching output is zero:

$$
C_{01}C_{23}+C_{03}C_{12}=0.
\tag{2}
$$

For an outside site, let $X_i$ be its attachment to core site $i$.
The response on each core triple is

$$
(\mathcal M_C X)_{ijk}
=X_i C_{jk}+X_j C_{ik}+X_k C_{ij}.
$$

Products always place factors at their labelled sites.

**Isometry lemma.** For every outside color space,

$$
\boxed{\|\mathcal M_C X\|^2=2\sum_{i=0}^3\|X_i\|^2.}
\tag{3}
$$

To prove this, flatten (2) across $01\mid23$.
The first product has flattening rank one. The second has rank
$\operatorname{rank}C_{03}\operatorname{rank}C_{12}$, so both
of those edge matrices have rank one. Flattening across $03\mid12$
shows the same for $C_{01},C_{23}$.
Equality of the nonzero product tensors identifies a unit local
vector $u_i$ at each site and unit-modulus scalars $c_{ij}$ such that

$$
C_{ij}=c_{ij}u_i u_j^{\mathsf T},\qquad
c_{01}c_{23}+c_{03}c_{12}=0.
$$

In the Gram matrix $\mathcal M_C^*\mathcal M_C$, every diagonal
block is $2I$: the other three vertices contain exactly two
unit-norm cycle edges. Adjacent core vertices have no common
neighbor, so their off-diagonal Gram block is zero.
For opposite vertices $i,j$, with the other two vertices $k,l$,
the off-diagonal block is proportional to

$$
c_{ik}\overline{c_{jk}}+c_{il}\overline{c_{jl}}
=\frac{c_{ik}c_{jl}+c_{il}c_{jk}}{c_{jk}c_{jl}}=0.
$$

Thus the Gram matrix is $2I$. Tensoring with the outside color
space proves (3).

We also need its elementary stability consequence. For fixed
finite local dimensions, there is a tolerance $\tau>0$ such that
a core with the following properties has
$\|\mathcal M_C X\|\ge\|X\|$:

- edges $01,03,12$ have norm one;
- edge $23$ has norm in $[1/2,2]$;
- edges $02,13$ have norm at most $\tau$;
- the full four-site output has norm at most $\tau$.

Otherwise a sequence with $\tau\to0$ would, by compactness,
converge to a core satisfying (2), contradicting (3) and
continuity of the smallest singular value.
No internal smoothness or block-invertibility hypothesis is needed.

## 3. Retain the original mixed-output equations

Throughout sections 3--7, assume the nonzero ground cofactors
contain two disjoint triangles and a bridge joining them.
Additional anchors are allowed.

Put $d=\delta^2$ and $t=\|T\|\le\delta$, where $T$ is the binary
non-ground source. For every quartet $S$, the
[refined output bound](balanced-response-ghz-onset-2026-09-27.md#3-mixed-output-estimates-retain-the-relevant-edges)
is

$$
\|\mathcal F_S(T)\|\le
C\left(\varepsilon+d\sum_{e\subset S}\|T_e\|\right).
\tag{4}
$$

In particular, $f=\|\mathcal F_4(T)\|\le C(\varepsilon+td)$.
Every ground-cofactor anchor has binary block size $O(\varepsilon+d)$.

The cases $T=0$, $\varepsilon>td$, or $t=O(d)$ follow from
$|\lambda|\le\varepsilon+15t^3$. Hence assume

$$
\varepsilon\le td,\qquad f\le Ctd,\qquad t\le1,
\tag{5}
$$

so all seven specified anchor blocks are $O(d)$.
Let the two anchored triangles define parts $P,Q$ of size three.
Choose a largest binary block $G$, of norm
$g\ge t/\sqrt{15}$.
If it is internal to a part or is the anchored bridge, then
$t=O(d)$. If it is a cross edge incident to a bridge endpoint,
its endpoints have a common anchored neighbor, and the
[common-neighbor theorem](balanced-response-ghz-onset-2026-09-27.md#4-a-common-anchored-neighbor)
applies.

It remains to consider a cross edge $G$ between non-bridge vertices.
Label its endpoints $0\in P$ and $1\in Q$. The anchored bridge
then lies entirely among the four outside vertices.
Write $z$ for the norm of all outside binary blocks.
The rank-free edge-removal projection gives

$$
|\lambda|\le\varepsilon+fz.
\tag{6}
$$

Choose an outside cross edge of largest norm $u$.
All outside internal edges are $O(d)$, so $z\le C(u+d)$.
If $u\le Ld$ for a fixed constant $L$, (6) proves (1).
Otherwise take $L$ large enough for the estimates below.

There is a useful second easy case. If $\varepsilon>du$, then
(5)--(6) imply
$|\lambda|\le C\varepsilon+Ctd u\le C'\varepsilon$.
Thus we may further assume

$$
u>Ld,\qquad \varepsilon\le du.
\tag{7}
$$

## 4. The outside edge opposite the largest one is small

Relabel the two remaining sites in each part so that

$$
P=\{0,2,4\},\qquad Q=\{1,3,5\},\qquad
U=T_{23},\quad \|U\|=u,\qquad V=T_{45}.
$$

If $45$ is the anchored bridge, $\|V\|=O(d)$.
Otherwise the bridge is $25$ or $34$: it cannot be $23$ because
$u>Ld$. The outside quartet is

$$
\mathcal F_{\{2,3,4,5\}}=UV+T_{24}T_{35}+T_{25}T_{34}.
$$

Its second term is $O(d^2)$ and its last term is $O(du)$.
Equation (4), with all outside blocks at most $u+O(d)$, gives

$$
u\|V\|\le C(\varepsilon+du+d^2).
$$

By (7), this again proves

$$
\boxed{\|V\|=O(d).}
\tag{8}
$$

## 5. Expose a balanced four-cycle

Let $B=T_{03}$, $C=T_{12}$, with norms $b,c$.
The other two internal core edges $T_{02},T_{13}$ are anchored.
The core quartet equation gives

$$
\|GU+BC\|\le Ctd,\qquad |gu-bc|\le Ctd.
$$

Since $g\ge t/\sqrt{15}$ and $u>Ld$, increasing $L$ ensures

$$
\tfrac12gu\le bc\le2gu,\qquad b,c\ge c_0u,
\tag{9}
$$

where $c_0>0$ is fixed. The latter bounds use $b,c\le t$.
In particular neither $b$ nor $c$ vanishes.

Scale binary blocks by $\widetilde T_{ij}=s_i s_jT_{ij}$ with

$$
s_0=\sqrt{c/b},\quad s_1=\sqrt{b/c},\quad
s_2=s_3=g/\sqrt{bc},\quad
s_4=s_5=\sqrt{bc}/g.
\tag{10}
$$

Their product is one. Each six-site matching uses every site once,
so

$$
H_6(\widetilde T)=H_6(T).
\tag{11}
$$

The rescaled core $K=\widetilde T[\{0,1,2,3\}]$ has cycle norms

$$
\|K_{01}\|=\|K_{03}\|=\|K_{12}\|=g,\qquad
\|K_{23}\|=\frac{g^2u}{bc},
$$

and its two diagonal blocks have norms at most
$Cgd/b,Cgd/c$. Also

$$
\|H_4(K/g)\|=\frac{\|\mathcal F_{\{0,1,2,3\}}(T)\|}{bc}
\le C d/u.
$$

The fourth normalized cycle norm differs from one by $O(d/u)$.
Thus section 2 applies for sufficiently large fixed $L$:

$$
\boxed{\|\mathcal M_K X\|\ge g\|X\|.}
\tag{12}
$$

The scaling is an algebraic device on $T$. We do not apply the
original output estimate to a rescaled ground source. Instead,
we scale each original quartet equation by its exact site factor.

## 6. Absorb the attachment terms

Consider outside site $4\in P$ and put $h_i=T_{i4}$.
The same-part attachments $h_0,h_2$ are $O(d)$.
Under (10),

$$
\widetilde h_0=(c/g)h_0,\quad
\widetilde h_1=(b/g)h_1,\quad
\widetilde h_2=h_2,\quad
\widetilde h_3=h_3.
$$

Let $x=\|(\widetilde h_0,\widetilde h_1,
\widetilde h_2,\widetilde h_3)\|$.
The exact quartet scale factors are:

| Quartet | Scale factor |
| --- | --- |
| $0124$ | $1$ |
| $0134$ | $1$ |
| $0234$ | $g/b$ |
| $1234$ | $g/c$ |

The first two original responses are $O(td)$, hence $O(gd)$
since $t/g\le\sqrt{15}$.
For the last two, keep only the binary edges actually in the
quartet in (4):

$$
\begin{aligned}
\|F_{0234}\|&\le C\{\varepsilon+d(b+u+\|h_3\|+d)\},\\
\|F_{1234}\|&\le C\{\varepsilon+d(c+u+\|h_1\|+\|h_3\|+d)\}.
\end{aligned}
\tag{13}
$$

Multiply by the displayed scale factors and divide by $g$.
Use (7)--(9), $\|h_3\|\le x$,
$\|h_1\|\le(g/b)x$, and $g/(bc)\le2/u$.
Each resulting bound is at most

$$
C d+C(d/u)x.
$$

For example the potentially large $h_1$ term contributes
$dgx/(bc)\le2(d/u)x$, rather than a bound using $t$ alone.
Combining the four responses with (12) gives

$$
x\le C d+C(d/u)x.
$$

For large enough $L$, absorb the last term to obtain $x=O(d)$.
At outside site $5\in Q$, the same-part attachments $T_{15},T_{35}$
are small. Interchange $0,1$ and $2,3$ in the same argument.
Thus

$$
\boxed{\|\widetilde X_4\|+\|\widetilde X_5\|=O(d).}
\tag{14}
$$

## 7. Bound the complete matching output

The fifteen six-site matchings split into three using edge $45$
and twelve using two attachments to sites $4,5$.
The first group is $H_4(K)\widetilde V$. Its scaling factors cancel:

$$
H_4(K)\widetilde V
=\mathcal F_{\{0,1,2,3\}}(T)V.
$$

Its norm is $O(td^2)$ by (5) and (8).
Every remaining term contains one core edge of norm $O(t)$
and two rescaled attachments of norm $O(d)$, so their total
norm is also $O(td^2)$.
By (11),

$$
\|H_6(T)\|=O(td^2)
$$

in the remaining hard case. Comparing the binary output to
$\lambda(b^6+c^6)$ proves
$|\lambda|\le C\varepsilon+Ctd^2\le C\varepsilon+C\delta^5$.
Together with the easy cases, this proves (1) under the bridge-anchor
hypothesis.

## 8. An anchored four-cycle also settles every source direction

Relabel so the anchored cycle is $24,25,34,35$, with the two
other vertices $0,1$. Set $G=T_{01}$ and, for outside pairs, put

$$
Z_{rs}=T_{rs},\qquad
C_{rs}=T_{0r}T_{1s}+T_{0s}T_{1r},\qquad
F_{rs}=GZ_{rs}+C_{rs}.
$$

No lower bound or rank assumption on $G$ is needed.
As before it suffices to assume $\varepsilon\le td$, so
$f\le Ctd$ and the four anchored $Z$ blocks are $O(d)$.
Let $U=Z_{23}$, $V=Z_{45}$, with $u=\|U\|\ge v=\|V\|$.
Write $z$ for the norm of all six outside blocks.

The rank-free edge-removal identity gives

$$
|\lambda|\le\varepsilon+fz.
\tag{15}
$$

For $G\ne0$, project the core space at $0,1$ perpendicular to $G$.
If $G=0$, the identity directly gives $\|H_6(T)\|\le fz$, which
also implies (15). Thus the constant does not deteriorate as $G$
vanishes.

If $u=O(d)$, then $z=O(d)$ and (15) proves (1).
Otherwise $z\le C u$. If $\varepsilon>du$, (15) again gives
$|\lambda|\le C\varepsilon$, since $t\le1$.
In the remaining case, the outside quartet and (4) give

$$
uv\le C(\varepsilon+dz+d^2)\le Cdu,\qquad v=O(d).
\tag{16}
$$

Use the exact matching rearrangement

$$
\begin{aligned}
H_6(T)={}&F_{23}V+C_{45}U\\
&+\sum_{\{r,s\}\in\{24,25,34,35\}}
F_{rs}Z_{\{2,3,4,5\}\setminus\{r,s\}}\\
&-G(Z_{24}Z_{35}+Z_{25}Z_{34}).
\end{aligned}
\tag{17}
$$

Project **at the outside pair $2,3$**, perpendicular to $U$.
This removes $C_{45}U$, since its other factor uses only sites
$0,1,4,5$. The first term is $O(fd)=O(td^2)$ by (16).
The sum has the same bound because its outside factors are
anchored. The final term is $O(td^2)$.

For any unit vector $P$ on two binary sites, the complementary
projection retains

$$
\|Q_P(b^6+c^6)\|^2
=2-|P_{bb}|^2-|P_{cc}|^2\ge1.
$$

Consequently (17) proves
$|\lambda|\le C\varepsilon+Ctd^2$, as required.
This projection handles the large product without estimating its
attachments or requiring a substantial edge on the complementary
two sites. Additional ground anchors are harmless.

## 9. Exhaust the ground graphs

The ground cofactor graph is nonempty and admits edge weights
$w_{ij}=D_{ij}c_{ij}\ne0$ with zero sum at each vertex.
The elementary minimal-support argument in
[section 4 of the graph note](cofactor-graph-ghz-frontier-2026-09-27.md#4-which-graphs-can-be-cofactor-graphs)
shows that it contains at least one of four patterns:

| Pattern of anchored edges | Onset argument |
| --- | --- |
| Four-cycle | Section 8 above |
| Six-cycle | The propagated four-cycle argument in the graph note |
| Two triangles meeting at one vertex | Four anchored arms at that vertex |
| Two disjoint triangles joined by a bridge | Sections 2--7 above |

These possibilities exhaust the minimal nonempty supports on
six vertices. The degree-four and six-cycle arguments were
already proved in the graph note and apply in every nearby
source direction. The two new arguments complete the list,
proving (1) at every full-support single-color zero.
The exhaustive graph certificate independently checks that the
four patterns cover all 10,099 admissible labelled supports;
the conclusion also follows from the written minimal-support
classification.

No critical non-ground directions remain for this local onset
theorem. The error-versus-signal estimate
$\varepsilon\ge c|\lambda|^3$ remains open, even in this branch,
and other zero-output boundary types still matter for the
unrestricted rate law. The unrestricted W-state optimum is a
separate open target.
