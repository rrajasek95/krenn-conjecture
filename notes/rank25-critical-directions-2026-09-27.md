# Critical directions at the full-support rank-25 boundary

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** This classifies first non-ground directions under the
stated vanishing conditions, not full source paths.

[Replay](../computations/flat-core-rigidity-2026-09-27/README.md) ·
[Quantitative application](ghz-critical-direction-normal-form-2026-09-27.md) ·
[Original boundary example](triangle-response-rank-classification-2026-09-27.md)

## 1. The boundary and its first constraints

On sites $0,\ldots,5$, take a single ground-color source $D$ with

$$
D_{01}=D_{23}=1,\quad D_{02}=D_{13}=\omega,\quad
D_{03}=D_{12}=\omega^2,\quad
D_{i4}=D_{i5}=r\ (i<4),\quad D_{45}=-2r^2,
$$

where $\omega^2+\omega+1=0$ and $r\ne0$.
Its ground hafnian vanishes. Its complementary four-site hafnians are
nonzero exactly on $02,03,12,13$.
For real positive $r$ with $r^2=(\sqrt{13}-1)/4$, it is balanced.
The earlier note establishes derivative rank 25; the support argument
below works for every $r\ne0$.

Let $A(t)=A_0+tA_1+t^2A_2+\cdots$ and let $T$ be the binary non-ground
part of $A_1$. Suppose the output coefficients of orders one and two
vanish. The first-order output with non-ground colors only at $i,j$ is
$C_{ij}(D)T_{ij}$. Hence

$$
T_{02}=T_{03}=T_{12}=T_{13}=0.
\tag{1}
$$

The second-order output with ground colors only at $i,j$ is
$D_{ij}H_4(T[V\setminus\{i,j\}])$. All $D_{ij}$ are nonzero, so

$$
\mathcal F_4(T)=0.
\tag{2}
$$

Higher source coefficients cannot enter that output sector at order two:
four non-ground endpoints require two perturbed edges.

## 2. Support classification

**Theorem.** Every colored source satisfying (1)–(2) has either at most
four active sites, or support contained in a star centered at $4$ or $5$.
This holds for any number of non-ground colors.

Here an active site is incident to a nonzero block. Edges are present
when their entire block is nonzero; individual entries may vanish.

**Proof.** If $T_{01}\ne0$, the quartet $0123$ has only one possible
matching, $01|23$. Its tensor vanishes only if $T_{23}=0$, since a
tensor product of two nonzero blocks is nonzero. The quartets $01j4$
and $01j5$, for $j=2,3$, similarly force $T_{j4}=T_{j5}=0$.
Thus sites $2,3$ are isolated and all support is on $\{0,1,4,5\}$.
The case $T_{23}\ne0$ gives the core $\{2,3,4,5\}$.

It remains to consider $T_{01}=T_{23}=0$. The only possible edges are
from leaves $0,1,2,3$ to centers $4,5$, together with edge $45$.
Represent each block by its bilinear polynomial in the local color
variables. Write $A_i=T_{i4}$ and $B_i=T_{i5}$ for these polynomials.
For distinct leaves, the quartet $ij45$ says

$$
r_{ij}:=A_iB_j+A_jB_i=0.
\tag{3}
$$

The polynomial ring over $\mathbb C$ is an integral domain.
If one leaf has both $A_i$ and $B_i$ nonzero, every other active leaf
must also have both: a one-sided leaf would leave one nonzero product
in (3). But three such leaves are impossible, since

$$
B_k r_{ij}+B_j r_{ik}-B_i r_{jk}=2A_iB_jB_k\ne0.
\tag{4}
$$

There can therefore be at most two active leaves, giving at most four
active sites including the centers.

If there is no double-sided leaf, all active leaves must use the same
center; two attached to opposite centers would again leave a unique
nonzero product in (3). All support then lies in the corresponding star,
including the possible edge $45$. ∎

## 3. Exact support census and attainability

The allowed graph has eleven edges. The replay checks all $2^{11}=2048$
edge subsets, with the following exhaustive counts:

| Support class | Count |
| --- | ---: |
| Excluded by a quartet with exactly one matching | 1922 |
| Excluded by three double-sided leaves and (4) | 10 |
| Surviving supports with at most four active sites | 104 |
| Surviving larger stars | 12 |

Every one of the 116 surviving supports is attained by a scalar
four-site-flat source, including the empty support. On a star there are
no four-site matching terms. On at most four active sites, either there
are no matching terms or there are two or three. Distinct matchings on
four sites have disjoint edge sets. Their products can be chosen as
$1,-1$ or $1,\omega,\omega^2$, respectively, without creating a zero
edge. These sums vanish. Thus the enumeration is exact at the support
level even for arbitrary colored blocks; the constructive check uses
only one color.

## 4. What this removes, and what remains

If the first direction has a complete four-site core with all six
binary blocks invertible, that core must be $0145$ or $2345$.
If it is a spanning star with invertible arms, its center must be $4$
or $5$. The [core and star estimates](star-response-identity-and-binary-flat-cores-2026-09-27.md)
give smooth local zero families and quantitative error bounds in both
cases. The [GHZ normal form](ghz-critical-direction-normal-form-2026-09-27.md)
then bounds departures from these families.

This does not eliminate rank-deficient four-site cores, sparse stars, or
directions where $T=0$ at first order. Nor does it set any higher source
jet to zero. Establishing a uniform comparison
$\|E\|\ge c|\lambda|^3$ through all such cases remains open.
