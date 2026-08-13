# Physical group bars do not yet split a matching component

## Outcome

Let `X` be a transitive orbit of literal matching occurrences.  In the
**formal** permutation module `Q[X]`, the boundaries of occurrence-local
site bars span exactly the augmentation ideal

\[
                 I_X=\ker\bigl(\epsilon_X:\mathbb Q[X]\to\mathbb Q\bigr).
                                                               \tag{1}
\]

Thus a zero-augmentation splitter theorem is elementary once an individual
bar cell is available at every occurrence.  That source-provenance
hypothesis is precisely what is missing here.  A complete physical source
row has occurrence profile

\[
                         {f 1}_X=\sum_{x\in X}e_x.              \tag{2}
\]

Every currently proved site bar and paired Cartan/Weyl prism constructed
from (2) remains in the trivial `X`-representation.  It cannot produce a
nonzero vector in `I_X`, hence cannot isolate a proper matching component.

The exact remaining cokernel has two pieces:

1. every matching-centered component cut; and
2. a word marginal (the surviving side of the Segre excess).

Consequently the placement theorem `6824c9e` does not itself construct a
component splitter, and the dark residual of `a60ee53` cannot automatically
be killed by group averaging.  One still needs an occurrence-local physical
bar/projector, a complement primitive, or a separate invariant argument
showing that the two residual classes vanish.

Checker:
[`verify_uniform_physical_bar_occurrence_splitter_cokernel.py`](../computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py).

## 1. Formal orbit incidence

Give a site-permutation orbit `X` its action graph.  A formal group bar on an
edge `x -> sx` has boundary

\[
                             e_{sx}-e_x.                         \tag{3}
\]

These vectors have augmentation zero.  Conversely, choose a spanning tree
in each orbit.  The tree-edge boundaries express `e_x-e_{x_0}` for every
vertex, so they span the whole orbitwise augmentation kernel.  Therefore

\[
 \operatorname {im}\partial_{\rm formal}
   =\{v:\epsilon_{X_j}(v)=0\text{ on every orbit }X_j\}.          \tag{4}
\]

The checker enumerates perfect matchings at orders six and eight.  Adjacent
site transpositions give one connected orbit of sizes `15` and `105`, hence
formal incidence ranks `14` and `104`.

Equation (4) is not yet a physical theorem.  It assumes a source generator
localized at `x`.  The physical hafnian row is the sum (2); its individual
matching terms are occurrences of one generator, not separate source rows.
This is the same provenance distinction frozen by the complete rectangle
cancellation theorem `7c62988`.

## 2. Exact physical image

Separate three finite transitive factors:

* `X`: matching occurrences;
* `A`: the placement orbit changed by target-preserving site permutations;
* `B`: the local Cartan/Weyl orbit.

Write `I_A,I_B` for their augmentation ideals.  A complete physical site
bar has the form

\[
             {\bf 1}_X\otimes(a'-a)\otimes b,                    \tag{5}
\]

and a paired endpoint-odd prism has the rectangle form

\[
             {\bf 1}_X\otimes(a'-a)\otimes(b'-b).                \tag{6}
\]

The target statements are the already proved physical facts: site
permutations preserve the GHZ target, while the Weyl defect is killed only
after the disjoint site oddization.  Assuming every edge in the displayed
orbits is available, (5)--(6) give

\[
\begin{aligned}
 B_{\rm prism}&={\bf 1}_X\otimes I_A\otimes I_B,\\
 B_{\rm site+prism}&={\bf 1}_X\otimes I_A\otimes\mathbb Q[B].     \tag{7}
\end{aligned}

The second equality also shows that paired prisms add no linear image once
all complete site bars are admitted.  Their role is physical word-changing
typing, not occurrence localization.

Let `m=|X|`, `a=|A|`, and `b=|B|`.  Inside the total augmentation kernel,
the paired-prism cokernel has dimension

\[
       (m-1)ab+(a+b-2).                                         \tag{8}

The first summand is the full matching-centered module
`I_X tensor Q[A] tensor Q[B]`.  The second is the Segre excess

\[
      (I_A\otimes{f 1}_B)\ \oplus\
      ({\bf 1}_A\otimes I_B).                                   \tag{9}

Before restricting to augmentation zero there is one additional global
trivial class.  After adjoining all complete site bars, the first marginal
in (9) is filled, but the exact residual dimension is still

\[
                         (m-1)ab+(b-1).                          \tag{10}

Thus the remaining classes are all matching cuts plus the pure Weyl
marginal `1_X tensor 1_A tensor I_B`.  A pure Weyl bar could fill the latter,
but it is not target-preserving in the present physical fibre.  An
occurrence-local site bar could fill the former, but it has not been
constructed from complete source rows.

## 3. Smallest sharp counterguards

Already for `m=a=b=2`, three zero-augmentation vectors separate the images.

* `(e_{x_0}-e_{x_1}) tensor e_{a_0} tensor e_{b_0}` is a matching cut.  It
  is outside every complete site/prism boundary because those are constant
  in `x`.
* `1_X tensor (e_{a_0}-e_{a_1}) tensor e_{b_0}` is a site marginal.  It is
  a complete site-bar boundary but not a paired-prism boundary.
* `1_X tensor 1_A tensor (e_{b_0}-e_{b_1})` is the pure Weyl marginal.  It
  remains outside the combined site/prism image.

The double difference

\[
 {f 1}_X\otimes(e_{a_0}-e_{a_1})
             \otimes(e_{b_0}-e_{b_1})                            \tag{11}
\]

is the paired rectangle.  The all-ones vector is the additional trivial
class and has nonzero total augmentation.  These four pieces are exactly
the trivial/Segre decomposition; no hidden finite case remains.

## 4. Why asymmetric placement does not change the answer

The complete physical prism is

\[
                    (1-s)(w-1)H_z.                               \tag{12}

If `s` fixes both endpoint words, summing over all matchings makes (12)
zero, exactly as in `7c62988`.  If `s` changes the word, (12) can be nonzero;
this is the asymmetric placement used by `6824c9e`.  But the matching sum is
still permuted by `s`, so every word fibre of (12) has constant matching
profile.  The checker records the nonzero four-corner word rectangle and
verifies that its matching-centered projection has rank zero.

Projection to a proper critical component can of course be nonzero.  That
is why `6824c9e` correctly proves `g=pi_M G != 0`.  The complementary
projection supplies the balancing terms.  Replacing `G` by only its
component projection would require multiplication by a component selector,
which is exactly the unproved source-valid splitter.

## 5. Consequence for the dark residual

For the complete-lift identity of `a60ee53`,

\[
                         R=G-Cy,\qquad \pi_MR=0,                  \tag{13}

define the matching-centered quotient by removing, in every word/fine-grade
fibre, its average over the matching orbit.  Every complete physical bar in
(7) maps to zero in this quotient.  Hence:

* a nonzero matching-centered class of `R` cannot be removed by the known
  group/bar cells;
* even if that class vanishes, the pure Weyl marginal can remain; and
* only after both vanish can `R` lie in the maximal complete site/prism
  image described here.

This does not weaken the typed-exit conclusion of `a60ee53`: a saturated
nonzero `R` is still a literal exit.  It says only that bar symmetry does not
turn the exit into an internal boundary without the extra splitter.

## 6. Conditional positive theorem and frontier

A zero-augmentation splitter theorem becomes sound under two new
source-typing hypotheses:

1. occurrence-local site bars exist on a connected graph in every physical
   word/fine-grade fibre; and
2. target-preserving pure Weyl bars span `I_B`, or an equivalent relative
   cell fills that marginal.

Then the occurrence bars fill
`I_X tensor Q[A] tensor Q[B]`, the complete site bars fill the `I_A` part,
and the pure Weyl bars fill the last `I_B` part.  Their combined image has
rank `mab-1`, exactly the total augmentation kernel.

Neither hypothesis follows from the existing Cartan placement and
complete-row covariance theorems.  The shortest component-splitter target
is therefore not another rectangle census.  It is a source-provenant
operator whose degree-zero boundary has a nonzero matching-centered
projection, followed by a check of the pure Weyl marginal.

## Verification

```text
python3 computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py
python3 -O computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py
python3 -I -S computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py
```

Frozen ledger SHA-256:

```text
04b066649d09c0412d6aaeb319583288d408592d516791bcc32b7a765563b25a
```
