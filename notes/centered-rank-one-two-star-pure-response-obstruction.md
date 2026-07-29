# Two pure responses force two singular spokes in the sharp rank-one packet

## 1. Outcome

Consider the sharp centered rank-one mask and its contracted overlap packet
from
[the rank-one overlap note](centered-rank-one-overlap-packet.md).  Thus
\(|B|=2m\geq6\), \(r,u\) are the deleted endpoints, \(x,y\) are internal
sites, and

\[
 A_{x\mid y}=e_0e_0^{\mathsf T},\qquad
 t_{1,x}=t_{2,x}=0.                                      \tag{1}
\]

On the common-kernel vector \(h=e_1-e_2\), the complete overlap equations
give one cofactor \(F_{hh}\) with

\[
 t_0F_{hh}=0,\qquad t_1F_{hh}=X_1,\qquad t_2F_{hh}=X_2. \tag{2}
\]

This note proves a support-free consequence of (1)--(2).

**Theorem 1.1 (two singular spokes).**  Put

\[
 Z=B\setminus\{r,u,x,y\}.
\]

For at least two sites \(z\in Z\), the two rows

\[
                         t_{1,z},\ t_{2,z}              \tag{3}
\]

are linearly dependent.  Consequently at least two of the blocks
\(A_{y\mid z}\) are singular.

The theorem is uniform for every even order \(N\geq6\).  It allows arbitrary
non-coordinate and multisite stars, arbitrary internal quadratic, and all
complex cancellation.  It uses neither a monomial support assumption nor a
choice of representatives modulo an annihilator.

For \(N=8\), the three blocks from \(y\) to \(r,u,x\) in the sharp mask
already have rank one, while \(Z\) has four sites.  Theorem 1.1 therefore
gives

\[
                         \deg_R(y)\leq2,\qquad
 R=\{vw:\operatorname{rank}A_{vw}=3\}.                  \tag{4}
\]

Thus the sharp rank-one survivor exports a second literal low-degree vertex
in the eight-site rank-three graph.

## 2. A two-star pure-response lemma

Let \(S\) be a finite set of \(n\geq2\) sites and work in the
site-square-zero algebra

\[
 {\cal A}_S=\bigotimes_{z\in S}(\mathbb C\oplus V_z).
                                                               \tag{5}
\]

Products of two positive-degree factors at one site are zero.  Let

\[
 a=\sum_{z\in S}a_z,\qquad b=\sum_{z\in S}b_z
 \quad(a_z,b_z\in V_z),                                  \tag{6}
\]

let \(G\in{\cal A}_S^{n-1}\), and let

\[
                         X=\bigotimes_{z\in S}x_z\ne0.   \tag{7}
\]

Define the local dependence set

\[
 D(a,b)=\{z\in S:\dim\operatorname{span}(a_z,b_z)\leq1\}.
                                                               \tag{8}
\]

**Lemma 2.1 (two-star pure response).**  If

\[
                         aG=X,\qquad bG=0,              \tag{9}
\]

then \(D(a,b)\ne\varnothing\).  More precisely, if
\(D(a,b)=\{r\}\), then

\[
             x_r\in\operatorname{span}(a_r,b_r).        \tag{10}
\]

In particular, the span in (10) is then a nonzero line.

### 2.1 No-defect case: the Hamming-level identity

The argument in this subsection is valid for every \(n\geq1\).
Suppose first that every pair \(a_z,b_z\) is independent.  For each site
choose a linear map

\[
 \pi_z:V_z\longrightarrow\mathbb C^2
 \quad\text{with}\quad
 \pi_z(a_z)=e_0,\quad\pi_z(b_z)=e_1,\quad\pi_z(x_z)\ne0.
                                                               \tag{11}
\]

There is no hidden genericity in this choice.  On
\(\operatorname{span}(a_z,b_z)\), the first two conditions define an
isomorphism.  If \(x_z\) lies in that plane, its image is automatically
nonzero.  If it lies outside, extend the map to \(x_z\) with any chosen
nonzero image.

The tensor product of the maps (11) is an algebra homomorphism.  It sends
(9) to a binary system of the same form with nonzero pure target.  We may
therefore assume

\[
 a_z=e_0^{(z)},\qquad b_z=e_1^{(z)},\qquad
 x_z=\alpha_ze_0^{(z)}+\beta_ze_1^{(z)},                \tag{12}
\]

where \((\alpha_z,\beta_z)\ne(0,0)\).

Every monomial of \(G\) misses exactly one site.  For a binary word
\(\epsilon\) on \(S\), let \(g_{z,\epsilon\setminus z}\) denote the
coefficient of the corresponding monomial of \(G\) missing \(z\).
Coefficient comparison gives

\[
\begin{aligned}
 [\epsilon](aG)
   &=\sum_{z:\epsilon_z=0}g_{z,\epsilon\setminus z},\\
 [\epsilon](bG)
   &=\sum_{z:\epsilon_z=1}g_{z,\epsilon\setminus z}.     \tag{13}
\end{aligned}
\]

Let \(A_k\) be the sum of the first line over all words of Hamming weight
\(k\), and let \(B_{k+1}\) be the sum of the second line over all words of
weight \(k+1\).  Both sums contain, exactly once, every coefficient of
\(G\) whose \((n-1)\)-site missing-site word has weight \(k\).  Hence

\[
                         A_k=B_{k+1}\qquad(0\leq k<n).  \tag{14}
\]

The equation \(bG=0\) makes every \(B_{k+1}\) zero.  Also \(A_n=0\),
because the all-one word has no zero position at which \(a\) can enter.
Thus every Hamming-level sum of \(aG\) is zero.

For the pure target in (12), those same sums are the coefficients of

\[
                 \prod_{z\in S}(\alpha_z u+\beta_z v). \tag{15}
\]

All coefficients of (15) would vanish.  This is impossible because
\(\mathbb C[u,v]\) is a domain and every factor in (15) is nonzero.
Therefore \(D(a,b)\) is nonempty.

This proof collects complete coefficient levels.  It does not infer that an
individual term in the zero product \(bG\) vanishes.

### 2.2 The unique-dependent-site case

Now assume \(D(a,b)=\{r\}\).  If (10) failed, there would be a covector
\(\lambda\in V_r^*\) such that

\[
 \lambda(a_r)=\lambda(b_r)=0,\qquad \lambda(x_r)\ne0.   \tag{16}
\]

Contract the \(r\)-slot in (9) by \(\lambda\).  The component of \(G\)
missing \(r\) contributes only after multiplication by \(a_r\) or \(b_r\),
so (16) kills it.  Contracting all components of \(G\) which contain \(r\)
produces an element

\[
                 \widetilde G\in
                 {\cal A}_{S\setminus\{r\}}^{n-2}.      \tag{17}
\]

Writing \(a'=\sum_{z\ne r}a_z\) and \(b'=\sum_{z\ne r}b_z\), the contracted
equations are exactly

\[
 a'\widetilde G
   =\lambda(x_r)\bigotimes_{z\ne r}x_z\ne0,\qquad
 b'\widetilde G=0.                                     \tag{18}
\]

Every remaining pair \(a_z,b_z\) is independent.  Section 2.1, applied on
\(S\setminus\{r\}\), contradicts (18).  Hence (10) holds and Lemma 2.1 is
proved.

Notice the precise strength of the singleton conclusion.  One pure
response alone does not rule out a unique dependent site; it only forces
the target factor at that site onto the dependent line.

## 3. Apply both colour slices of \(F_{hh}\)

Write \(|B|=2m\), so

\[
 Y=B\setminus\{r,u,y\},\qquad |Y|=2m-3,\qquad
 Z=Y\setminus\{x\},\qquad |Z|=2m-4.                    \tag{19}
\]

In the contracted packet,

\[
 F_{hh}=(h^{\mathsf T}A_{r\mid u}h)q^{[m-2]}
                         +p_hs_hq^{[m-3]}              \tag{20}
\]

has site degree

\[
                         2m-4=|Y|-1.                   \tag{21}
\]

Decompose it by its \(x\)-slot:

\[
 F_{hh}=F_{\widehat x}
          +e_0^{(x)}G_0+e_1^{(x)}G_1+e_2^{(x)}G_2,     \tag{22}
\]

where \(F_{\widehat x}\) occupies every site of \(Z\), and

\[
                         G_c\in{\cal A}_Z^{|Z|-1}.      \tag{23}
\]

By (1), the stars \(t_1,t_2\) have no component at \(x\).  Their product
with \(F_{\widehat x}\) is zero because that term already occupies every
site of \(Z\).  Comparing the \(x\)-colours in (2) therefore gives

\[
\begin{array}{lll}
 t_1G_1=X_1^Z,&\qquad&t_2G_1=0,\\
 t_2G_2=X_2^Z,&&t_1G_2=0.                              \tag{24}
\end{array}
\]

Set

\[
 D=\{z\in Z:
       \dim\operatorname{span}(t_{1,z},t_{2,z})\leq1\}. \tag{25}
\]

If \(D\) were empty, the first row of (24) would contradict Lemma 2.1.
If \(D=\{z\}\), apply the singleton conclusion first to the first row of
(24), and then to the second row with the two stars interchanged.  It gives

\[
 e_1^{(z)},e_2^{(z)}
        \in\operatorname{span}(t_{1,z},t_{2,z}).        \tag{26}
\]

The right side has dimension at most one, whereas the two vectors on the
left are independent.  This is impossible.  Thus

\[
                              |D|\geq2.                 \tag{27}
\]

Orient \(A_{y\mid z}\) with \(y\) first.  The vectors
\(t_{0,z},t_{1,z},t_{2,z}\) are its three rows.  At every site in \(D\),
two of those rows are dependent, so

\[
                         \operatorname{rank}A_{y\mid z}\leq2. \tag{28}
\]

Equations (27)--(28) prove Theorem 1.1.

## 4. The eight-site graph export

For \(N=8\), the set \(Z\) in (19) has four sites.  The sharp local mask
also has

\[
 \operatorname{rank}A_{y\mid r}
 =\operatorname{rank}A_{y\mid u}
 =\operatorname{rank}A_{y\mid x}=1.                    \tag{29}
\]

At least two of the remaining four incident blocks are singular by
Theorem 1.1.  Hence at most two blocks incident with \(y\) have rank three,
which is exactly (4).  More generally the same count gives

\[
                         \deg_R(y)\leq N-6              \tag{30}
\]

for this sharp mask at every even order \(N\geq6\).

## 5. Exact scope and false shortcuts

1. The result concerns the specific sharp rank-one mask whose two-dimensional
   common kernel supplies \(F_{hh}\).  Other rank-one local orbits need
   their own contraction normal form.
2. A dependent pair in (25) makes \(A_{y\mid z}\) singular; it does not make
   the block zero or rank one.
3. Lemma 2.1 does not exclude a singleton defect for one target.  The two
   independent target slices in (24) are essential.
4. No summandwise vanishing is used.  The Hamming-level identity (14)
   retains every cancellation in \(bG=0\).
5. The proof never compares quadratic cofactor representatives.  It is
   unaffected by additions from \(\operatorname{Ann}(q)\), extra cells of
   \(q\), or cancellation among several physical origins.
6. The common-\(q\) relaxation in the preceding overlap note is consistent
   with the theorem: its \(t_1,t_2\) row pairs are dependent at all four
   sites of \(Z\).

The dependency-free checker
[verify_centered_rank_one_two_star_pure_response.py](../computations/verify_centered_rank_one_two_star_pure_response.py)
audits the binary Hamming-level incidence identity, the pure-product level
bookkeeping, the unique-site contraction indexing, the overlap degrees, and
the \(N=8\) rank-graph count.  The uniform implication is the coefficient
proof above, not a bounded search.
