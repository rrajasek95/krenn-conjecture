# Six-odd-bag incidence reduction

## Outcome

The most general direct incidence quotient to six ordinary matching sites
can be formulated without choosing a pair cap or discarding individual
matching terms.  Partition the original vertex set into six odd bags.  The
sector having exactly one crossing edge at every bag is *automatically* an
ordinary six-site matching tensor after arbitrary local linear maps on the
bags.  Hence a quotient exists as soon as those maps kill the sum of all
remaining crossing sectors.

Combined with the complete arbitrary-matrix six-site obstruction, this gives
a strong necessary condition on any hypothetical larger three-color source:
for every partition into six odd bags, every bag's diagonal three-space must
meet the left Schmidt space of the total unwanted sector.  In particular,
the unwanted sector cannot vanish for any such partition.

This is a rigorous reduction criterion and a simultaneous-contamination
theorem, not yet an all-even proof.  Order minimality does not by itself
produce the required local maps; the exact eight-site countermodel in
`notes/total-sector-six-reduction.md` shows why the already known anchor and
constant-fibre data are insufficient even for the most unbalanced
partition.

## 1. Exact one-crossing factorization

Let

\[
                 B=B_1\mathbin{\dot\cup}\cdots
                     \mathbin{\dot\cup}B_6,\qquad |B_j|\text{ odd},       \tag{1}
\]

and write

\[
 V_j=\bigotimes_{v\in B_j}V_v,qquad
 g_{j,r}=e_r^{\otimes B_j},qquad
 \mathcal G_j=\operatorname{span}\{g_{j,0},g_{j,1},g_{j,2}\}.             \tag{2}
\]

For a perfect matching `M` of `B`, let `d_j(M)` be the number of its edges
with exactly one endpoint in `B_j`.  Parity gives

\[
                         d_j(M)\equiv |B_j|\equiv1\pmod2.                 \tag{3}
\]

Split the matching tensor as

\[
 H_B(A)=T_{\mathrm{one}}+T_{\mathrm{bad}},                                \tag{4}
\]

where `T_one` is the sum over matchings satisfying `d_j(M)=1` for every
`j`, and `T_bad` is the sum over all remaining matchings.  All cancellations
within either total tensor are retained.

For two distinct bags define the two-bag open-edge tensor

\[
 Z_{ij}=\sum_{x\in B_i}\sum_{y\in B_j}
 H_{B_i\setminus\{x\}}(A)\otimes A_{xy}\otimes
 H_{B_j\setminus\{y\}}(A)\in V_i\otimes V_j,                            \tag{5}
\]

with endpoint slots reordered into their named bags.  Let
`Phi_j:V_j -> C^3` be arbitrary linear maps and put

\[
                         Y_{ij}=(\Phi_i\otimes\Phi_j)Z_{ij}.              \tag{6}
\]

**Lemma 1.1 (six-bag incidence factorization).**

\[
 (\Phi_1\otimes\cdots\otimes\Phi_6)T_{\mathrm{one}}
                              =H_6(Y).                                    \tag{7}
\]

**Proof.**  A matching counted by `T_one` has one cross-edge endpoint in
each bag.  Its cross edges therefore induce a perfect matching of the six
bag labels.  After fixing that quotient matching, the choices associated
with one quotient edge `ij` are exactly: its endpoints `x,y`, a perfect
matching of `B_i\setminus{x}`, and a perfect matching of
`B_j\setminus{y}`.  Their sum is (5).  The choices belonging to the three
quotient edges are independent, so summing first over them and then over
the fifteen quotient matchings gives the hafnian expansion on the right of
(7).  Applying the six local maps turns each `Z_ij` into (6).  \(\square\)

No support-level uniqueness is being used here.  In particular, (7) is
valid with parallel sources, asymmetric endpoint colors, and arbitrary
complex cancellation inside every near-perfect tensor in (5).

## 2. Quotient criterion and the six-site contradiction

**Theorem 2.1 (six-odd-bag quotient criterion).**  Suppose

\[
                         H_B(A)=\Delta_{B,3}.                              \tag{8}
\]

If there are maps `Phi_j` such that

\[
 \Phi_j(g_{j,r})=e_r\quad(1\le j\le6,\ 0\le r\le2),
 \qquad
 (\Phi_1\otimes\cdots\otimes\Phi_6)T_{\mathrm{bad}}=0,                  \tag{9}
\]

then the matrices (6) realize `Delta_(6,3)`.

**Proof.**  The prescribed values in (9) send the right side of (8) to
`Delta_(6,3)`.  Equations (4), (7), and the second part of (9) therefore
give

\[
                         H_6(Y)=\Delta_{6,3}.                              \tag{10}
\]

This is an ordinary aggregate-edge matching tensor on six sites.  \(\square\)

The proved arbitrary-complex six-site theorem rules out (10).  It follows
that a hypothetical larger realization cannot admit maps (9), whether or
not it was chosen order-minimal.

There is a useful one-bag sufficient condition.  For
`T in V_1 tensor ... tensor V_6`, write

\[
 \operatorname{LS}_j(T)=
 \{(\operatorname{id}_{V_j}\otimes\beta)T:
       \beta\in(\bigotimes_{k\ne j}V_k)^*\}\subseteq V_j                 \tag{11}
\]

for its left Schmidt space at bag `j`.

**Corollary 2.2 (simultaneous incidence contamination).**  Under the
hypothetical identity (8), for every partition (1) and every bag `j`,

\[
             \boxed{\mathcal G_j\cap
                    \operatorname{LS}_j(T_{\mathrm{bad}})\ne0.}          \tag{12}
\]

**Proof.**  If the intersection were zero, define `Phi_j` on the direct
sum

\[
       \mathcal G_j\oplus\operatorname{LS}_j(T_{\mathrm{bad}})
\]

by sending `g_(j,r)` to `e_r` and the Schmidt space to zero, then extend it
linearly to all of `V_j`.  At every other bag choose any linear map with the
three prescribed values; the constant tensors there are independent.  The
map at bag `j` alone kills the total bad tensor, so (9) holds.  Theorem 2.1
would contradict the six-site obstruction.  \(\square\)

When `B_j` is a singleton, `G_j=V_j`; hence (12) says simply that the bad
tensor is nonzero.  Thus every six-odd-bag partition of a putative source
has genuine, noncancelling multi-cross incidence.  If all six bag cuts were
tight, `T_bad` would be zero and the familiar tight-cut quotient would be
recovered as a special case.

## 3. All overlapping partitions are compatible in the occurrence relaxation

It is tempting to combine (12) for many overlapping partitions and hope
that the diagonal contamination directions become inconsistent.  Incidence
bookkeeping and the exact output equations alone cannot do this.  There is
an exact rational countermodel once the shared-edge compatibility between
different perfect matchings is removed.

Let `N=|PM(B)|`.  For every perfect matching `M` and color `r`, introduce
an abstract occurrence tensor

\[
                         t_{M,r}=N^{-1}e_r^{\otimes B}.                    \tag{13}
\]

It is pair-factorized along `M`: choose one distinguished edge of `M` with
tensor `N^(-1)e_r tensor e_r` and put `e_r tensor e_r` on its other edges.
However, these factors are labeled by the whole occurrence `(M,r)` and are
not allowed to recombine with factors belonging to another matching.  Thus
this is an occurrence relaxation, not an aggregate-edge source.

Summing every occurrence gives the target exactly:

\[
                         \sum_M\sum_{r=0}^2t_{M,r}
                              =\Delta_{B,3}.                              \tag{14}
\]

Fix any partition of `B` into six nonempty odd bags.  There is a good
matching: pair the six bag labels, use one cross edge for each paired pair
of bags, and match the even remainder of every bag internally.  Since
`|B|>6`, some bag has at least three vertices.  There is also a bad
matching: send three vertices of that bag to three other bags, join the two
remaining bags by one cross edge, and again match every even remainder
internally.  Hence the numbers `N_one` and `N_bad` of the two matching
types are both positive.  The occurrence tensors in their total sectors
are

\[
 T_{\mathrm{one}}^{\mathrm{occ}}
       ={N_{\mathrm{one}}\over N}\Delta_{B,3},\qquad
 T_{\mathrm{bad}}^{\mathrm{occ}}
       ={N_{\mathrm{bad}}\over N}\Delta_{B,3}.                           \tag{15}
\]

Consequently, for every bag of every six-odd-bag partition,

\[
 \operatorname{LS}_j(T_{\mathrm{bad}}^{\mathrm{occ}})=\mathcal G_j.     \tag{16}
\]

This single construction satisfies the exact target, every mixed
coefficient equation, and maximal contamination for **all overlapping
partitions simultaneously**.  It even retains pair factorization inside
each named occurrence.  What it omits is precisely the incidence closure
of a real source: an edge tensor is shared by every perfect matching using
that source, so factors chosen for different `M` cannot be kept from
recombining around alternating cycles.

The first exact consequence of that missing axiom is already recorded in
`proofs/selected-one-factor-cancellation-cycle.md`: three selected constant
matching occurrences force a fourth, mixed occurrence and hence an external
cancellation mate.  What is not yet proved is that the resulting family of
alternating-cycle mates is incompatible with (12) over all partitions.

Thus a simultaneous-partition proof must use that shared-edge/alternating-
cycle compatibility.  Linear combinations of sector equations, Schmidt
dimensions, and the fact that the total output is diagonal cannot by
themselves contradict (12).  This identifies a narrower missing mechanism
than merely saying that one partition may be contaminated.

The obstruction is not that six-bag partitions fail to distinguish
matchings.

**Lemma 3.1 (six-bag sector signatures separate matchings).**  If
`|B|>=8` is even and `M!=N` are distinct underlying pairings of `B`, there
is a partition of `B` into six odd bags for which `M` is in the
one-crossing sector and `N` is in the bad sector.  (Parallel source choices
on the same underlying pairing have, of course, the same cut signature;
they have already been aggregated into one edge tensor here.)

**Proof.**  Choose an edge `ab in M\setminus N`.  At most two vertices are
the `N`-partners of `a,b`; since `|B|>=8`, choose
`x notin {a,b}` which is neither of them.  Then

\[
                             S=\{a,b,x\}
\]

has one `M`-edge crossing its boundary (the edge at `x`) and three
`N`-edges crossing its boundary.  Use `S` as the first bag.  In the
complement, put the `M`-partner of `x` alone in a second bag.  Choose two
further `M`-edges and put their four endpoints alone in the other four
bags.  Distribute every remaining whole `M`-edge arbitrarily among these
five bags.  All six bag sizes remain odd.  The three selected crossing
`M`-edges pair the six bags, while `N` already has crossing degree three at
`S`.  Thus `M` is good and `N` is bad.  \(\square\)

Accordingly the full family of partitions remembers occurrence identity
at the Boolean level.  What it does not impose is the rectangular
recombination law saying that factors on a shared source edge participate
in every compatible perfect matching.  Turning Lemma 3.1 into a
contradiction therefore still requires algebraic relations among
alternating-cycle recombinations, not more cut incidence data.

## 4. Relation to the one-shore cap

For the partition

\[
|B_1|=|B|-5,\qquad |B_2|=\cdots=|B_6|=1,                                \tag{17}
\]

the bad sector is precisely the sum of matchings crossing the first shore
three or five times.  Corollary 2.2 at the first bag is exactly the
simultaneous-contamination conclusion of
`notes/total-sector-six-reduction.md`.  The present formulation shows that
this is not peculiar to a single large shore: the same obstruction occurs
at every bag of every six-odd-bag incidence quotient.

The logical boundary is important.  The complete six-site theorem proves
that all the intersections (12) must be nonzero *if* a larger source
exists; it does not force one of them to vanish.  To finish the uniform
problem along this route, one needs a new use of the simultaneous mixed
coefficient equations showing that (12) fails for at least one bag and one
partition.  Graph support, forced rank-one anchors, and order minimality
without such coefficient compatibility do not supply that implication.
