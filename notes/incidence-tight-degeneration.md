# Tight degenerations of perfect-matching incidence tensors

This note isolates the exact point at which a tight/free-subrank argument
would have to use perfect-matching incidence.  It gives a clean conditional
bridge from a row-monomial restriction to an induced diagonal, but also
shows why the bridge is not automatic: all cancellation mates in one
coloring fiber have exactly the same tight weight.  Thus a tight
one-parameter subgroup cannot retain one of them and discard the others.

## 1. Incidence tensor and row-monomial restrictions

Let (Gamma) be a finite multigraph on the even vertex set (B).  At a
vertex (v), use one basis vector (e_{v,a}) for every source edge (a)
incident to (v).  Its perfect-matching incidence tensor is

\[
 T_\Gamma=\sum_{M\in\operatorname {PM}(\Gamma)}
                  \bigotimes_{v\in B}e_{v,a_v(M)},          \tag{1}
\]

where (a_v(M)) is the unique source of (M) incident to (v).

A row-monomial local map has the form

\[
 L_v(e_{v,a})=\lambda_{v,a}e_{k(v,a)}.                     \tag{2}
\]

After deleting columns with (lambda_{v,a}=0), every source (a=uv)
has nonzero matching weight

\[
                         z_a=\lambda_{u,a}\lambda_{v,a}.   \tag{3}
\]

Thus ((\bigotimes_vL_v)T_\Gamma=\Delta_{B,3}) is exactly the original
decorated weighted perfect-matching problem.  Parallel sources having the
same underlying pair and the same ordered endpoint colors may be aggregated
because their weights enter every partner choice linearly.

The support of (1) is free: two distinct perfect matchings cannot differ at
only one vertex.  It is also tight whenever there are injective local
integer weights (alpha_{v,a}) satisfying

\[
 \sum_{v\in B}\alpha_{v,a_v(M)}=0
                         \qquad(M\in\operatorname {PM}(\Gamma)).\tag{4}
\]

For example, assigning opposite generic weights at the two ends of every
source makes every matching term have weight zero; generic choices can be
made injective at each vertex.

## 2. The exact tight-normalization calculation

Fix a tight weight (4).  For every vertex and output color occurring in
(2), put

\[
 m_{v,i}=\min\{\alpha_{v,a}:k(v,a)=i\}.                    \tag{5}
\]

Let (h_v(t)e_{v,a}=t^{\alpha_{v,a}}e_{v,a}), and normalize the output
rows by (D_v(t)e_i=t^{-m_{v,i}}e_i).  Every entry of

\[
                         \widetilde L_v(t)=D_v(t)L_vh_v(t) \tag{6}
\]

has a nonnegative exponent and therefore has a finite limit at (t=0).
Because (4) fixes every support monomial of (T_\Gamma), not merely their
sum,

\[
 (\bigotimes_v\widetilde L_v(t))T_\Gamma
   =(\bigotimes_vD_v(t))\Delta_{B,3}
   =\sum_{i=0}^2t^{-\sum_vm_{v,i}}e_i^{\otimes B}.          \tag{7}
\]

On the other hand, if the color-(i) coefficient is nonzero, it contains a
perfect matching (M), and (4)--(5) give

\[
                 0=\sum_v\alpha_{v,a_v(M)}
                   \ge\sum_vm_{v,i}.                       \tag{8}
\]

Thus the exponents on the right of (7) are nonnegative, as the finite limit
on the left already requires.

More is true.  For any fixed coloring (c:B\to\{0,1,2\}) and any
(c)-consistent matching (M), its exponent after (6) is

\[
 \sum_v\bigl(\alpha_{v,a_v(M)}-m_{v,c(v)}\bigr)
                         =-\sum_vm_{v,c(v)}.                \tag{9}
\]

It is independent of (M).  This is the incidence version of the fact
that a target-torus face cannot distinguish matching monomials inside one
coefficient fiber.

**Lemma 2.1 (zero-weight exposure implies an induced diagonal).**  Suppose
((\bigotimes_vL_v)T_\Gamma=\Delta_{B,3}), the tight weights are injective
at each vertex, and

\[
                         \sum_vm_{v,i}=0\qquad(i=0,1,2).    \tag{10}
\]

Then the support of (T_\Gamma) contains an induced matching of size
three.  More precisely, for every color (i) there is a unique constant-
(i) perfect matching using the unique local minima in (5), and the union
of those three source matchings contains no other perfect matching.

**Proof.**  A constant-(i) matching exists because its coefficient is
one.  Equality in (8), together with the termwise nonnegative differences
in (5), forces it to use a minimizing local source at every vertex.
Injectivity of (alpha_v) makes that source unique, so the matching is
unique.

Now restrict every local source alphabet to these three minimizing symbols.
Any further perfect matching in their union has some coloring (c).  At
each vertex (c(v)) specifies a unique minimizing source, so at most one
matching has that coloring.  Its product weight is nonzero.  A mixed such
matching would therefore give a nonzero mixed coefficient in the (t=0)
limit of (7), which is still (Delta_{B,3}), a contradiction.  Hence only
the three constant matchings survive, exactly the induced-matching
condition.  (square)

This is the desired exact-versus-degeneration bridge in its sharp form.
The unresolved part is not passage to the limit; it is proving the
zero-weight condition (10).  If (10) fails, (7) simply degenerates GHZ to
a tensor with fewer diagonal colors.

The determinant character makes the same point.  The output normalization
in (7) belongs to the determinant-one local group exactly when

\[
                         \sum_{v,i}m_{v,i}=0.               \tag{11}
\]

Since every color sum is nonpositive by (8), (11) is equivalent to all
three equalities in (10).  Kempf--Ness closedness of the GHZ orbit prevents
loss of colors only under (11); a normalization with negative total
minimum weight is a genuine boundary degeneration, not an exact monomial
restriction.

## 3. Why cancellation itself blocks exposure

Suppose three nonzero constant matching terms (M_0,M_1,M_2) have been
chosen.  They are source-disjoint.  If their union contains another perfect
matching (N), its endpoint coloring (c_N) is mixed, and it is the unique
matching *inside that union* with that coloring: at a vertex, the color
specifies the unique one of the three selected incident sources.

Exactness forces at least one further (c_N)-consistent matching (P)
outside the union to cancel the nonzero term of (N).  Formula (9) says
that (N) and every such (P) have exactly the same exponent under every
tight normalization.  In particular, no tight one-parameter subgroup can
retain (N) and discard all its cancellation mates.  If (N) used local
minima everywhere, then its exponent would be zero; (9) and nonnegativity
would force every cancellation mate to use the very same unique local
minima, hence to equal (N), an impossibility.  Therefore the existence of
the required cancellation is itself a certificate that (10) cannot hold
for that proposed exposed triple.

This explains why tightness alone cannot prove the missing implication.
Finding a tight weight satisfying (10) is already tantamount to finding an
induced diagonal; it is not a consequence of ordinary or row-monomial
subrank three.

There is a compatible minimum-norm identity which makes the gap
quantitative but does not close it.  Fix the incidence support and endpoint
colors, regard the nonzero \(\lambda_{v,a}\) in (2) as variables, and
minimize

\[
                         \sum_{v,a}|\lambda_{v,a}|^2        \tag{12}
\]

over the exact row-monomial fiber.  The fiber is closed, so a minimum
exists.  Source-tight rescalings and target-torus rescalings give,
respectively,

\[
 \sum_{v,a}\alpha_{v,a}|\lambda_{v,a}|^2=0,
 \qquad
 \sum_{a\ni v,\,k(v,a)=i}|\lambda_{v,a}|^2=c_i
                         \quad(v\in B),                    \tag{13}
\]

where \(c_i>0\) is independent of \(v\).  In particular, the tight
cocharacter which is \(+1\) at one end of a source and \(-1\) at the other
shows that the two endpoint magnitudes of every retained source are equal.

Subtracting the local minima (5) from the first identity in (13) yields the
exact slack formula

\[
 \boxed{\displaystyle
 \sum_{v,a}|\lambda_{v,a}|^2
       \bigl(\alpha_{v,a}-m_{v,k(v,a)}\bigr)
       =-\sum_{i=0}^2c_i\sum_vm_{v,i}.}                    \tag{14}
\]

Both sides are nonnegative.  Equality would force every supported local
column to be a minimum in its color; with injective \(\alpha_v\), this is
the monomial/induced situation.  A strictly negative color-minimum sum is
perfectly compatible with a norm minimum: it appears as strictly positive
slack on the left of (14).  Thus the Frobenius moment equations measure the
failure of (10), but supply no inequality forcing that failure to vanish.

## 4. The alternating-cycle closure absent from the five-term example

The abstract counterexample in
`notes/tight-free-subrank-counterexample.md` contains

\[
 0000,\quad1111,\quad0101,\quad p1p1                     \tag{15}

with the last two terms cancelling after (p\mapsto0).  If (12) came from
four-vertex perfect matchings, compatibility of the first three tuples
would put the selected (0)-sources and (1)-sources on the same
underlying pairing.  Switching the two alternating components would force
the missing complementary tuple (1010).  The parallel (p)-source would
also force (p0p0).

Writing the aggregate source weights on one pair as (a_0,a_1,a_p) and on
the other as (b_0,b_1), the six rectangle corners have weights

\[
 a_0b_0, a_0b_1, a_1b_0, a_1b_1, a_pb_0, a_pb_1.     \tag{16}
\]

Cancellation of the two (0101) images says
(b_1(a_0+a_p)=0).  Since (b_1\ne0), it also cancels the all-zero partners:

\[
                         b_0(a_0+a_p)=0.                   \tag{17}
\]

After aggregate-cell summation, this is simply one zero edge entry.  Thus
the five-term mechanism cannot selectively cancel its mixed term while
leaving its displayed diagonal term intact in an incidence tensor.

This local closure is useful but not sufficient globally.  Distinct
underlying perfect matchings can cancel along an alternating cycle.  If a
mixed coloring fiber has exactly two matching monomials (z^M,z^N), then

\[
 z^{\chi_M-\chi_N}=-1,                                    \tag{18}
\]

and (chi_M-\chi_N) is a vertex-balanced alternating-cycle circulation.
An odd integral dependence among such circulation vectors is impossible,
because multiplying (15) would give (1=-1).  These are the exact toric
certificates used elsewhere in the project.  The active-rank-two binary
gadget in `computations/verify_active_ranktwo_binary_gadget.py` shows that a
single incidence-valid cycle cancellation can nevertheless occur.  A
three-color proof needs a global incompatibility among the cancellation
cycles; rectangle completion by itself does not supply it.

## 5. Exact status of the proposed implication

For even order at least six, the statement

> every row-monomial restriction (T_\Gamma\to\Delta_{B,3}) yields an
> induced diagonal triple

would immediately give the desired upper bound.  The row-monomial
restriction is precisely a putative monochromatic graph, while the following
elementary lemma rules out the asserted induced triple.

**Lemma 5.1 (three one-factors force a fourth).**  Let (n\ge6), and let
(M_0,M_1,M_2) be three source-disjoint perfect matchings on (n) vertices.
Their union contains a fourth source perfect matching.

**Proof.**  The union of two of the matchings is a disjoint union of
alternating even cycles, with a length-two cycle allowed when their sources
are parallel.  If, say, (M_0\cup M_1) has at least two components,
switching just one component gives the required fourth matching.  Thus it
is enough to treat the case in which every pairwise union is a Hamilton
cycle.

Write the Hamilton cycle (M_0\cup M_1) as
(0,1,\ldots,n-1,0), with its two matchings alternating, and regard the
edges of (M_2) as chords.  If an (M_2)-edge has endpoints of opposite
parity on the cycle, delete its endpoints and perfectly match each of the
two remaining even paths with cycle edges.  Together with the chord this is
a fourth source matching.

It remains to suppose that every (M_2)-edge joins vertices of the same
parity.  Put \(m=n/2\), and write the even and odd cycle vertices as
\(E_j=2j\) and \(O_j=2j+1\), cyclically for
\(j\in\mathbb Z/m\mathbb Z\).
There must be an (E)-chord crossing an (O)-chord.  Otherwise, an
(E)-chord (E_aE_b) encloses a set of (b-a) consecutive (O)-vertices
which must be paired internally by the (O)-chords; hence (b-a) is even.
Thus the (E)-matching pairs indices of the same parity.  The identical
argument for an (O)-chord shows that the (O)-matching does too.  Restrict
to either parity class of indices.  In its inherited cyclic order the
remaining (E)- and (O)-vertices still alternate, and the same no-crossing
argument applies.  Iteration would make the positive integer (m) divisible
by arbitrarily high powers of two, a contradiction.

Choose a crossing (E)-chord and (O)-chord.  Their four endpoints
alternate in parity around the Hamilton cycle, so each intervening path has
an even number of internal vertices.  Match all four paths with cycle edges
and include the two chords.  This is a perfect matching distinct from
(M_0,M_1), and (M_2).  Source-disjointness ensures distinctness even when
two sources have the same underlying endpoints.  (square)

Consequently Lemma 2.1 proves the desired row-monomial implication under the
additional zero-Hilbert--Mumford-weight condition (10), and Lemma 5.1 would
then contradict it.  Equations (7)--(9) prove that neither tightness nor the
known exact cancellation equations make (10) automatic.  The missing
assertion is therefore a genuine global cancellation theorem for matching
fibers, rather than a formal GIT or tight/free-subrank fact.
