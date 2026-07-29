# Independent audit of the injective-star/Hessian bridge frontier

## Verdict

**PASS with a strict sharpening, and with the scope warning in the primary
note essential.** A clean-room
reconstruction confirms all four substantive claims in
[injective-star-hessian-bridge-frontier.md](injective-star-hessian-bridge-frontier.md):

1. at least $N(N-13)/2$ unordered pairs are aggregate-injective at both
   endpoints for every hypothetical exact source with $N\geq14$;
2. on a gauge-rigid full-nine chart, connectedness forces a localized zero
   row, while connected nonbipartiteness forces all six nonzero aggregate
   rows to have site support at most two;
3. the exact binary six-site source has a both-injective active pair for
   which every covector retaining both target colours has a nonzero cap
   correction; and
4. the displayed rational fourteen-site family has all $91$ pairs
   aggregate-injective, but every internal rank-three graph is disconnected
   and every deleted star retains blocks with two zero rows.

The first claim is valid but nonsharp. A simpler mode-support argument,
found during this audit, shows that at most $3N$ directed pairs are
deficient. It improves the guaranteed number of both-injective unordered
pairs to

\[
                         \frac{N(N-7)}2,                 \tag{S}
\]

already for $N\ge8$. Thus $N=14$ guarantees at least $49$, rather than
merely seven, and some vertex belongs to at least $N-7$ good pairs. This
sharpening does not alter the primary bridge obstruction: aggregate
injectivity remains weaker than every Hessian or clean-cap hypothesis at
issue.

The fourteen-site family has its three constant coefficients normalized to
one, but it has the positive mixed coefficient $4/29$. It is therefore
**not** a ternary GHZ realization and not a counterexample to Krenn's
conjecture. It is an exact countermodel only to the proposed implication
from aggregate injection, rank/zero-mask data, pure normalization, and pair
exchange alone. Any successful bridge must use vanishing of the mixed target
residuals in a source-specific way.

The independent executable audit is
[audit_injective_star_hessian_bridge_frontier_independent.py](../computations/audit_injective_star_hessian_bridge_frontier_independent.py).
It imports neither the primary proof nor its checker.

## Frozen inputs

The primary files audited here had SHA-256 digests

    f49a525ddd7b95b3915c9aaa254c2854f2c3ed15d50cf00127fa3337feb7fa62  notes/injective-star-hessian-bridge-frontier.md
    6c5652d05ac4f355b183a725b99c705ed69f3b42464985775805a4dc25679ed8  computations/verify_injective_star_hessian_bridge_frontier.py

The independent checker has SHA-256 digest

    c8312401b1ab91e9fd697d0c2672b5bf51d8d5f027df6a0c4347664effa30d21

## 1. The primary good-pair count and a sharpening

For distinct physical sites $r,u$, let $(r,u)$ be deficient when the
aggregate span at $u$, after excluding $r$, is proper. The independently
audited full-nine incidence theorem gives at most six deficient $u$'s for
each fixed $r$. Hence there are at most $6N$ deficient directed pairs.

If an unordered pair is not injective at both endpoints, at least one of its
two orientations is deficient. Choosing one such orientation for each bad
pair is injective: different unordered pairs cannot yield the same directed
pair. Therefore

\[
 \#\{\text{both-injective pairs}\}
 \ge {N\choose2}-6N
 =\frac{N(N-13)}2.                                      \tag{A1}
\]

This gives seven good pairs at $N=14$ and twenty-four at $N=16$. The
good-pair graph has average degree at least $N-13$, so some site belongs to
at least $N-13$ good pairs.

The integer step behind the six-defect bound is also sound. If $b_r$ is
the number of deficient $u$'s for fixed $r$, the cap double count says

\[
                         b_r(N-2)\le6(N-1).
\]

For $N\ge10$, the right-side quotient is strictly less than seven, whence
the integer $b_r\le6$. The checker replays this ledger through order sixty.
No edge entry is selected and no cancellation or blockwise nonzero condition
enters this argument. Its conclusion is only aggregate direct-sum
injectivity.

There is a stronger count which does not need the full-nine incidence
ledger. Fix an endpoint $u$ and put

\[
 L_{ur}=\operatorname{im}_u(A_{ur}),\qquad
 T_u=\sum_{r\ne u}L_{ur}.                               \tag{A1a}
\]

Every matching term in $H_B(A)$ has its mode-$u$ vector in one of the
spaces $L_{ur}$. Hence the mode-$u$ support of the complete source tensor is
contained in $T_u$. The mode-$u$ flattening of the ternary diagonal target
has rank three and support exactly $V_u$, so an exact source forces

\[
                              T_u=V_u.                   \tag{A1b}
\]

The orientation $(r,u)$ is deficient precisely when removing $L_{ur}$ from
the sum in (A1a) leaves a proper subspace. Call such a summand essential.
For every essential $r$, choose

\[
 x_r\in L_{ur}\setminus\sum_{v\notin\{r,u\}}L_{uv}.
\]

The vectors $x_r$ for distinct essential summands are linearly independent:
in any dependence with a nonzero coefficient of $x_r$, solving for $x_r$
would put it in the sum of all the other $L_{uv}$, a contradiction. Since
$\dim V_u=3$, at most three neighbours are essential at each $u$.

Summing over endpoints gives at most $3N$ deficient directed pairs. The same
injection from bad unordered pairs into deficient orientations now yields

\[
 \#\{\text{both-injective pairs}\}
 \ge {N\choose2}-3N
 =\frac{N(N-7)}2.                                      \tag{A1c}
\]

The associated graph has average degree at least $N-7$. This bound applies
for every $N\ge8$, retains endpoint-asymmetric blocks, parallel sources,
zero blocks, and arbitrary complex cancellation, and strictly dominates
(A1). The independent checker exhausts all families of subspaces of
$\mathbb F_2^3$ to verify the underlying essential-summand bound and then
replays (A1c) through order sixty.

## 2. Reconstructing the Hessian frontier

Delete a both-injective pair $p,q$, and write the full nine equations on
the internal set $W$ as

\[
                  a_{cd}Q+\mathcal H_{q_0}(p_cs_d)
                    =\delta_{cd}X_c.                    \tag{A2}
\]

Suppose first that the source Hessian of $q_0$ has only its vertex-gauge
kernel. For $c\ne d$, (A2) puts $p_cs_d$, after adding a scalar multiple
of $q_0$, in that kernel. On a rank-three internal edge $ij$, its block
has the form

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}
                 =\lambda_{ij}(q_0)_{ij}.                \tag{A3}
\]

The left side has matrix rank at most two. The right side has rank three
unless $\lambda_{ij}=0$. Thus both sides of (A3) vanish on every edge of
$G_3(q_0)$.

If $G_3(q_0)$ is connected and every local vector in all six rows is
nonzero, equality of nonzero simple tensors in (A3) makes the proportionality
factor alternate across every edge. Connectivity propagates it; the third
colour synchronizes the three $p$-rows and three $s$-rows into

\[
                         p_{c,i}=t_cz_i,
        \qquad s_{d,i}=u_d\sigma_i z_i,                  \tag{A4}
\]

where $\sigma_i$ changes sign across an edge. In particular the graph must
be bipartite. Substitution into all nine equations packages their output as

\[
                         a_{cd}Q+t_cu_dR.                \tag{A5}
\]

This lies in the two-dimensional span of $Q,R$, whereas the three diagonal
ternary targets are independent. Consequently a connected gauge-rigid
chart cannot be row-full: some individual endpoint colour row vanishes at
some internal block.

If the connected graph is nonbipartite, the source-derivative argument gives
the sharper bounds

\[
                  |\operatorname{supp}_s(p_c)|\le2,
        \qquad |\operatorname{supp}_s(s_d)|\le2.         \tag{A6}
\]

Both aggregate star maps are injective, so their three global rows are
linearly independent and in particular nonzero. This supplies the missing
lower bound $1$ in every case. Each endpoint can therefore meet at most
$2+2+2=6$ internal sites, and is zero toward at least

\[
                         |W|-6=N-8                       \tag{A7}
\]

of them. This chain uses every hypothesis stated in the primary
proposition. In particular, aggregate injection does not prove row-fullness,
connectedness, nonbipartiteness, or gauge rigidity.

## 3. The binary clean-cap boundary

The six-site binary block family was reconstructed directly and all
$2^6=64$ coefficients were expanded. Its only nonzero output coefficients
are the two constant words, both equal to one. On the selected pair
$(1,3)$ in one-based labels, the two aggregate star maps both have rank two.

For a completely general bilinear covector with coordinates
$(k_{00},k_{01},k_{10},k_{11})$, the direct and target scalars are

\[
                 s=-k_{10},\qquad
                 \kappa_0=k_{00},\qquad
                 \kappa_1=k_{11}.                       \tag{A8}
\]

An independent construction of every first-jet block $R_K$, followed by
the three perfect matchings on the four internal sites, gives

\[
 [e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}]H_4(R_K)
                         =k_{10}k_{11}.                  \tag{A9}
\]

Thus $s\kappa_0\kappa_1\ne0$ forces a nonzero higher correction. Neither
off-diagonal covector coordinate can cancel (A9). This is a fully exact
warning at the binary boundary, but it does not rule out a ternary theorem
which essentially uses the third-colour equations.

## 4. Independent reconstruction of the fourteen-site family

Put seven sites on each shore. Each shore carries a seven-cycle whose
stored, lower-to-higher endpoint matrix is

\[
 D=\begin{pmatrix}1&1&1\\1&2&4\\1&3&9\end{pmatrix},
 \qquad\det D=2.                                        \tag{A10}
\]

The matrix is nonsymmetric. Traversing an edge from the opposite endpoint
therefore uses $D^{\mathsf T}$, a convention tested explicitly by the
checker. Across the shores are three edge-disjoint one-factors $M_c$,
with $E_{cc}$ on the edges of $M_c$. Every other block is literally zero.

For a constant colour with $d=D_{cc}$, a separate bit-mask matching
recurrence gives the cycle-edge histogram

\[
                    1+7z^2+14z^4+7z^6.                  \tag{A11}
\]

Hence the three constant coefficients before normalization are

\[
                         29,\quad701,\quad3{,}812{,}509. \tag{A12}
\]

Multiply every colour-$c$ row at site zero by the reciprocal of the
corresponding number in (A12). This is one invertible local diagonal map,
not three matching-dependent rescalings. Every perfect matching uses
exactly one block at site zero, so all three constant coefficients become
exactly one. Matrix ranks, endpoint row-zero masks, and asymmetry under
endpoint reversal are unchanged.

Now delete any pair $p,q$.

* Each endpoint retains at least one of its two cycle neighbours. The
  aggregate star therefore contains an invertible $D$, $D^{\mathsf T}$,
  or diagonally rescaled version, and has rank three.
* Each endpoint retains at least two of its three cross-shore anchor
  neighbours. Each such oriented $E_{cc}$ block has exactly two literal
  zero endpoint rows, so blockwise row-fullness fails at both endpoints.
* The only rank-three blocks are the two shore cycles. Both shores retain at
  least five sites, and no rank-three edge crosses the shores. The internal
  graph $G_3$ is therefore disconnected.

The checker verifies these statements rather than only this counting proof:
it computes both aggregate ranks, every retained anchor zero mask, and every
internal rank-three component for all $\binom{14}{2}=91$ deletions.

Finally, all block entries after normalization are nonnegative rational
numbers. Exact matching recurrence at the mixed word $01010111010101$
gives coefficient $4/29>0$. The source therefore fails a mixed GHZ
equation despite satisfying the three pure normalizations. This is the
decisive guard against overclaim.

## 5. Pair exchange and the remaining gate

For any deleted pair, the set of all $13!!=135{,}135$ perfect matchings
splits into

\[
       11!!=10{,}395\quad\text{direct-edge matchings},
       \qquad124{,}740\quad\text{two-star matchings}.    \tag{A13}
\]

The independent checker builds the matchings by a different recursion and
audits (A13) in the overlapping charts $(0,7)$ and $(0,1)$. For all three
constant words and the mixed witness above, the exact weighted sums in each
chart reconstruct the same full coefficient. Reversed endpoint traversal
uses the transposed stored matrix. Thus pair contraction commutes and the
exchange formula is a genuine polynomial identity, but the two charts are
two partitions of the same matching monomials, not independent target
equation systems.

The audit therefore supports the primary note's proposed next gate. One
must eliminate the shared mixed residual polynomials through their different
source-variable factorizations, or show that the extra-kernel/disconnected
escapes cannot cover the guaranteed good-pair graph. More incidence counts,
pure normalization, or exchange reindexing alone cannot supply that step.
