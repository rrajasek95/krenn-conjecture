# Full mixed-row cancellation forces a Segre cube of mates

## Exact theorem

Fix one physical perfect matching with edges (e_1,\ldots,e_h).  Suppose
two nonzero decorated occurrences differ on (k) of those edges, with
decorated cells (a_i,b_i\ne0) on the differing edges.  Recombining the
two choices gives (2^k) selected matching monomials

\[
                 m_\epsilon=\prod_{i=1}^k
                   \begin{cases}a_i,&\epsilon_i=0,\\
                                 b_i,&\epsilon_i=1.
                   \end{cases}                         \tag{1}
\]

Assume their endpoint words are distinct and mixed.  In the complete source
coefficient of the word (\epsilon), let (R_\epsilon) be the sum of every
matching monomial except the selected physical matching.  Exact
monochromaticity says

\[
                         m_\epsilon+R_\epsilon=0.       \tag{2}
\]

Consequently

\[
 \boxed{R_\epsilon=-m_\epsilon}                         \tag{3}
\]

is a dense rank-one tensor on the Boolean cube.  In particular every entry
is nonzero, and every (2\times2) minor of every flattening vanishes.  For
each coordinate (i) and residual bit strings (u,v),

\[
              R_{0u}R_{1v}-R_{1u}R_{0v}=0.             \tag{4}
\]

This is elementary, but it is stronger than the matching-exchange support
statement: arbitrary cancellation mates cannot be chosen independently in
the (2^k) output grades.  Their **aggregate coefficients** must glue to the
one Segre point prescribed by the repeated source occurrence.

## Canonical multiplicity-two boundary

For the source-labelled support-eleven circuit in
[`n8-one-bad-multiplicity-cube-boundary.md`](n8-one-bad-multiplicity-cube-boundary.md),
the doubled matching has three cell-disjoint decorated edges.  At the pinned
rational point every selected cube monomial has value (1).  The six-row
guard already has alternate sum (-1) at

```text
000, 011, 100, 111,
```

and alternate sum (0) at

```text
001, 010, 101, 110.
```

An exact full packet must therefore add aggregate alternate value exactly
(-1) in each of the latter four grades.  After completion, the full
alternate array is the dense rank-one tensor

\[
                         (R_\epsilon)_{\epsilon\in\{0,1\}^3}
                              =(-1,-1,-1,-1,-1,-1,-1,-1). \tag{5}
\]

Thus the remaining carrier theorem has a precise coefficient target.  It is
not enough to exhibit one mate in each missing word: all mates, including
later contaminants, must collectively satisfy the Segre minors (4).

## Proof and scope

Equation (1) is a tensor product of the two cell choices on each differing
edge, hence is rank one.  Equation (2) holds coefficientwise because every
word is mixed.  Negation preserves tensor rank and proves (3)--(4).  No
positivity, genericity, support uniqueness, or quotient is used.

The exact checker
[`verify_recombination_cube_segre_cancellation.py`](../computations/verify_recombination_cube_segre_cancellation.py)
audits all flattening minors over exact rationals and replays the canonical
three-cube.  This theorem is a necessary global coupling condition, not by
itself a contradiction and not a Krenn counterexample.  A proof-completing
continuation must show that the genuine common-(q) response rows cannot
produce the dense Segre mate tensor (3), or that doing so yields the clean
cap/source descent.

