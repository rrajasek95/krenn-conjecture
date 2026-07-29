# Exact extra-singular frontier and a heavy-class closure

## 1. Outcome

Retain the cyclic three-zero branch, with the two forced type-\(22\)
centres removed through their cyclic ports and with shared zero \(z_0\).
For an additional nonzero singular site \(e\), write

\[
 C_e=\{j:e_j\in\operatorname {im}P_e\},\qquad
 M_e=\{0,1,2\}\setminus C_e .                                  \tag{1}
\]

The capacity and shared-star theorems leave the following exact
incidence frontier.

**Theorem 1.1 (exact family census).** Up to interchanging binary axes
\(0,1\), every nonempty extra-site family is one of

\[
\begin{array}{c|c}
\text{contains the sole eligible rescue type }\{2\}
 & \{2\},\quad \{2\}+\{0\},\quad \{2\}+\{0\}+\{1\},\\[1mm]
\text{contains no eligible extra rescue}
 & \{0\},\quad \{0,2\},\quad \{0\}+\{1\},
       \quad \{0\}+\{1,2\}.
\end{array}                                                       \tag{2}
\]

There are eleven nonempty families before quotienting by the binary
swap, and seven orbits in (2). Only an \(M_e=\{2\}\) member can have
\(\operatorname {rank}q_{e z_0}=3\), and there is at most one such
member.

If there are \(k\) extra sites and \(L\) live sites in the residual, then

\[
                              L+k\equiv1\pmod2.                   \tag{3}
\]

Thus a sole extra has \(L=2r\), two extras have \(L=2r-1\), and three
extras have \(L=2r\). For the sole eligible plane, the existing
all-order notes close exactly

\[
                 0\le t\le\min(2r,r+2),                          \tag{4}
\]

including all \(r=1,2\). Its arbitrary-beta frontier is

\[
 r\ge3,\qquad r+3\le t\le2r,\qquad
 h:=t-r-1\in\{2,\ldots,r-1\}.                                   \tag{5}
\]

The first two layers of this sole-plane frontier, \(t=r+3\) and \(t=r+4\),
are now closed uniformly by
[live-three-zero-sole-plane-first-high-layer-uniform-closure.md](live-three-zero-sole-plane-first-high-layer-uniform-closure.md).
Its forced-pair \(P_r/S_r\) deletion argument covers arbitrary beta
repetitions and every row plane without a profile census, while
[live-three-zero-sole-plane-second-high-closure.md](live-three-zero-sole-plane-second-high-closure.md)
uses deletion, initial-jet, and residue fibres on the next layer.  The first
point of the following layer, \((r,t)=(5,10)\), is closed by
[live-three-zero-sole-plane-third-high-first-point-closure.md](live-three-zero-sole-plane-third-high-first-point-closure.md).
The uniform one-deletion Hermite and Robin argument in
[live-three-zero-sole-plane-third-high-layer-uniform-closure.md](live-three-zero-sole-plane-third-high-layer-uniform-closure.md)
then closes the full layer \(t=r+5\).  Thus the remaining sole-plane
frontier is \(r\ge7,\ r+6\le t\le2r\).  No sole-plane proof deletes a
second singular site.

On the first remaining layer \(t=r+6\),
[live-three-zero-sole-plane-fourth-high-frontier.md](live-three-zero-sole-plane-fourth-high-frontier.md)
closes every profile containing a class of multiplicity at least three,
the all-distinct profile, the one-double profile, and every profile with at
least two doubles and at least eleven value classes.  The all-distinct
closure uses the full four-anchor DR4 theorem and an overlapping-core
quadratic-fibre contradiction.  At \((r,t)=(7,13)\), exactly four profiles
remain: \(2^3 1^7,2^4 1^5,2^5 1^3,2^6 1\).  Across the layer, the only
remaining profiles form a finite dense-double tail, empty for \(r\ge15\).

This note also removes a uniform part of (5).

**Theorem 1.2 (heavy exceptional beta class).** Suppose there is exactly
one extra singular site \(e\), with \(\operatorname {rank}P_e=2\). Let
the live shore have size \(2r\), let \(t\ge r+2\) live sites be
exceptional, and suppose some exceptional beta value occurs at least
\(r\) times. Then every residual block at \(z_0\) has rank at most two.
Hence this configuration is impossible.

Consequently every surviving sole eligible-plane profile in (5) has

\[
       \boxed{\text{every exceptional beta multiplicity is at most }r-1.}
                                                                    \tag{6}
\]

The proof permits arbitrary values and repetitions outside the selected
heavy class. It uses no genericity or Cauchy noncancellation assertion:
the selected \(r\)-set makes every surviving matching carry the same
nonzero monomial.

## 2. Proof of the family census

The capacity theorem says that the nonempty sets \(M_e\) are pairwise
disjoint and that none contains both \(0\) and \(1\). Hence every member
belongs to

\[
 \{\{0\},\{1\},\{2\},\{0,2\},\{1,2\}\}.                          \tag{7}
\]

Enumerating disjoint subfamilies of (7) gives the eleven nonempty
families represented by (2). A family containing \(\{2\}\) can contain
only \(\{0\}\), only \(\{1\}\), or both.

If \(M_e\cap\{0,1\}\ne\varnothing\), the shared-star theorem gives

\[
                     \operatorname {im}q_{e z_0}
                           \subseteq\operatorname {im}P_e,       \tag{8}
\]

so this block is singular. The only set in (7) not covered by (8) is
\(\{2\}\), and disjointness permits only one such member. A singleton
missed set also forces the corresponding coordinate plane:

\[
\begin{aligned}
 M_e=\{0\}&\Longrightarrow\operatorname {im}P_e=\langle e_1,e_2\rangle,\\
 M_e=\{1\}&\Longrightarrow\operatorname {im}P_e=\langle e_0,e_2\rangle,\\
 M_e=\{2\}&\Longrightarrow\operatorname {im}P_e=\langle e_0,e_1\rangle.
\end{aligned}                                                     \tag{9}
\]

For a double missed set, the image may instead be a coordinate line or a
noncoordinate plane containing the sole recorded coordinate axis. This
rank-one possibility must not be merged with the plane analysis.

After removing the two type-\(22\) centres and two zero sites, the
vanishing response is supported on the \(L\) live sites, the two
type-\(10\) centres, the \(k\) extras, and \(z_0\). Perfect-matching
parity gives \(L+2+k+1\equiv0\pmod2\), proving (3). Formulae (4)-(5)
then follow from the exact ranges of the existing sole-plane notes.

## 3. The homogeneous-shore coefficient

Normalize as in the sole-plane proofs:

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 \mu=1,\qquad
 P_i=I\ (i\text{ live}),\qquad
 P_c=P_d=\operatorname {diag}(1,1,0).                            \tag{10}
\]

Also \(\beta_e=1\). Let \(E\) be the exceptional live labels. Choose

\[
 R\subset E,\quad |R|=r,\quad \beta_x=\nu\ (x\in R),\qquad
 B\subset E\setminus R,\quad |B|=2.                              \tag{11}
\]

This is possible because \(t\ge r+2\). Give the labels of \(B\) output
colour \(2\) and use diagonal source \(22\). Every other live site and
both type-\(10\) centres receive a binary output row. At the extra site
we use a contraction with source row \(p_2=0\), or an annihilator of
\(P_e\). Thus \(B\) is the unique marked pair. The direct term is zero
because \(B_{22}=0\).

Put

\[
              {\cal O}=(U\setminus B)\sqcup\{c,d\},
              \qquad |{\cal O}|=2r.                              \tag{12}
\]

Give \(R\) colour zero and \(Y={\cal O}\setminus R\) colour one.
Every perfect matching is a bijection \(R\to Y\), and all its row
parameters on the first shore equal \(\nu\). Hence the balanced cofactor
is

\[
 r!\prod_{y\in Y}{1\over\nu+\beta_y}.                             \tag{13}
\]

Every denominator is structurally nonzero. Define

\[
                 C_R=2r!\prod_{y\in Y}{1\over\nu+\beta_y}\ne0.   \tag{14}
\]

The factor two is the diagonal marked coefficient of \(B\).

## 4. The extra block is singular

Choose \(0\ne\theta\in\operatorname {Ann}(\operatorname {im}P_e)\)
and contract the output at \(e\) by \(\theta\). Retain the binary word
of Section 3. If the star is not \(e\), the zero local row
\(\theta^{\mathsf T}P_e\) remains in the cofactor. If the star is \(e\),
(13) applies. The exact response is the singleton

\[
                         C_R\,\theta^{\mathsf T}q_{e z_0}=0.      \tag{15}
\]

Therefore

\[
              \operatorname {im}q_{e z_0}
                    \subseteq\operatorname {im}P_e,\qquad
              \operatorname {rank}q_{e z_0}\le2.                 \tag{16}
\]

For the eligible missed set \(\{2\}\), this is precisely the new
assertion that its formerly unrestricted transverse row vanishes.

## 5. Every common-beta residual block is singular

The row space of \(P_e\) is a two-plane, so choose

\[
                0\ne p=(p_0,p_1,0)=\eta^{\mathsf T}P_e.          \tag{17}
\]

Suppose first that \(p_1\ne0\). Fix any common-beta live site or either
type-\(10\) centre \(i\). Give the \(r+1\) sites \(R\sqcup\{i\}\)
output colour zero, give the other \(r-1\) sites of \({\cal O}\) colour
one, contract \(e\) to \(p\), and retain marked source \(22\).

For the star at \(i\), the extra site must pair with one of the \(r\)
equal-\(\nu\) labels. The remaining matching is a bijection from the
other \(r-1\) equal-\(\nu\) rows to the opposite shore. The
\(r(r-1)!=r!\) terms give exactly

\[
                              C_Rp_1 Z_{i,0}.                     \tag{18}
\]

The other labels in \(R\sqcup\{i\}\) are exceptional and have zero
star blocks because \((\nu-1)q_{x z_0}=0\). A star outside that set,
or at \(e\), leaves unbalanced binary shores. Thus (18) is a singleton
after adjoining the structural exceptional zeros, and \(Z_{i,0}=0\).

If \(p_1=0\), then \(p_0\ne0\). Swap binary colours. The identical
coefficient is \(C_Rp_0\), and \(Z_{i,1}=0\). The choice of killed row
is uniform in \(i\). Repeating for all three coordinates at \(z_0\)
kills one complete output row of every common-beta live and type-\(10\)
block. All these blocks have rank at most two.

Exceptional live blocks vanish structurally, the extra block is singular
by (16), the two removed type-\(22\) blocks are singular ports, and the
zero-zero blocks at \(z_0\) vanish by beta parity. Thus \(z_0\) has no
rank-three neighbour, proving Theorem 1.2.

## 6. Exact remaining frontier

After Theorem 1.2 and the uniform closures of the layers
\(t=r+3,r+4,r+5\), the sole eligible-plane gap has
\(r\ge7\), \(r+6\le t\le2r\), and every exceptional class size at most
\(r-1\). For more than one extra site,
the unresolved rescue geometries are

\[
\begin{array}{c|c|c}
\text{missed sets}&\text{live size}&\text{currently untreated }t\\ \hline
\{2\}+\{0\}&2r-1&
 \begin{array}{l}1,2,3\quad(r=2),\\0,\ldots,2r-1\quad(r\ge3),\end{array}\\
\{2\}+\{0\}+\{1\}&2r&
 \begin{array}{l}1,2\quad(r=1),\\0,\ldots,2r\quad(r\ge2).\end{array}
\end{array}                                                       \tag{19}
\]

The omitted minimal cases \((r,t)=(2,0)\) and \((1,0)\) are now closed
uniformly, respectively, by
[live-three-zero-minimal-two-extra-response-frontier.md](live-three-zero-minimal-two-extra-response-frontier.md)
and
[live-three-zero-minimal-three-extra-response-frontier.md](live-three-zero-minimal-three-extra-response-frontier.md).
The nonrescue
orbits in the second row of (2) are also not deletable: (8) makes their
own shared-zero blocks singular but does not remove their internal
matching rows. A continuation must retain those rows.

## 7. Exact audit

[verify_live_three_zero_extra_singular_exact_frontier.py](../computations/verify_live_three_zero_extra_singular_exact_frontier.py)
enumerates all families and binary-symmetry orbits, checks parity and the
sole-plane ranges, and reconstructs (15), (18), and its colour swap by
exact rational perfect-matching expansion. The stress cases assign
different rational values to every exceptional label outside \(R\).
The displayed proof is uniform and independent of the finite audit.
The finite \((3,6)\) closure has its own literal response and twelve
localized-ideal audit in
[verify_live_three_zero_sole_plane_first_high_closure.py](../computations/verify_live_three_zero_sole_plane_first_high_closure.py).
Its uniform extension to every \(t=r+3\) is audited in
[verify_live_three_zero_sole_plane_first_high_layer_uniform.py](../computations/verify_live_three_zero_sole_plane_first_high_layer_uniform.py).
