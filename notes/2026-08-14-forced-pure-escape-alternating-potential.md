# Forced pure escapes have an alternating-cycle potential, but need a parent selector

## Outcome

The pure escape forced by `bad70ef` has a uniform occurrence-level normal
form.  Relative to any cap-containing parent occurrence, its symmetric
difference has a unique alternating component through the cap.  Flipping
only that component produces another live cap-avoiding occurrence with

1. one alternating cycle through the cap;
2. a literal common matching tail outside that cycle; and
3. a strictly smaller lexicographic occurrence potential whenever the
   original parent--escape difference had any other alternating component.

This is the correct graph-theoretic recurrence.  It is not automatically a
source recurrence.  The cap-containing residual is a sum of matching
parents, and the parent giving the shortest alternating cycle need not be a
physical coefficient restriction.  Arbitrary cancellation among the parent
terms prevents selecting it.

The smallest exact guard has nine live cells.  Two mixed rows vanish, the
selected pure row is normalized to one, and its unique escape differs by a
`C4` from one cap parent and by a full `C6` from the other.  The `C4`
restriction has value `-1`, while the physical rows have values only `0` and
`1`; it is not a source row.  Thus the missing hypothesis is a
source-labelled parent/occurrence restriction carrying the complete word,
fine, operation, and companion ledger.

The checker is
`computations/verify_uniform_forced_pure_escape_alternating_potential.py`.

## 1. Uniform alternating escape normal form

Let `M` be a live perfect-matching occurrence in the killed cap sector, let
`e` be its cap edge, and let `N` be a live pure escape occurrence with
`e notin N`.  Since `M` and `N` have the same output word, every edge in
their symmetric difference carries the same prescribed endpoint colours.
The graph

\[
                            M\mathbin\triangle N            \tag{1}
\]

is a disjoint union of alternating even cycles.  Exactly one component
`C_e` contains `e`.  Define

\[
                          N_e=M\mathbin\triangle C_e.        \tag{2}
\]

Then `N_e` is a perfect matching, is live in the same word, avoids `e`, and
uses only cells already occurring in `M` or `N`.  Moreover

\[
 M\mathbin\triangle N_e=C_e,\qquad
 M\cap N_e=M\setminus C_e.                                  \tag{3}
\]

The second equality is a literal matching-monomial tail.  No coefficient or
genericity assumption enters.

Use the lexicographic occurrence potential

\[
 \mu_e(M,N)=
 \left(|V(C_e)|, |V(M\triangle N)|,
              \#\pi_0(M\triangle N)\right).                 \tag{4}
\]

Equation (2) keeps the first coordinate and replaces the last two by
`(|V(C_e)|,1)`.  Therefore it strictly lowers (4) whenever (1) has another
cycle.  If `C_e` is a proper subset of the old terminal component, its first
coordinate is itself a strict vertex-potential decrease.  The only
support-terminal case is one primitive alternating cycle occupying the
whole component.

The checker exhausts all labelled parent/cap/escape triples at orders six
and eight:

```text
N=6: 15 matchings,   540 triples
      180 C4, 360 C6

N=8: 105 matchings, 37,800 triples
      2,520 C4, 10,080 C6, 20,160 C8,
      5,040 C4+C4, all reduced strictly to the cap C4.       (5)
```

These finite counts audit the uniform proof; the proof itself is just the
alternating-cycle decomposition and applies at every even order.

## 2. Terminal ear and tight-shore interpretation

For a tight odd shore, both `M` and `N` use exactly one crossing edge.  The
cycle `C_e` contains the old cap crossing and the new escape crossing.
Flipping (2) changes precisely that boundary state and leaves the matching
tail outside `C_e` fixed.  If the new crossing has the same labelled
near-perfect cofactors, (3) is the desired rank-one tail.  If it has a new
endpoint/tail label, it is an explicit outside boundary channel.

For a terminal odd ear, (2) is the same two-mode recurrence: the cap cycle
switches between the through and internal ear patterns, while every matching
edge outside the cycle is unchanged.  Thus the intrinsic potential is the
size of the alternating component carrying the ear/cut-state change, not
the total support size of the source.

This gives the intended three support-level outcomes:

* `|C_e|=4`: an exposed `C4` flip;
* `4<|C_e|<|V(core)|`: a strictly smaller alternating core with a common
  matching tail; or
* `C_e=core`: a primitive full-cycle terminal packet.

The closed six-cycle in `844c121` handles the last alternative when that
packet carries all three normalized pure supports.

## 3. What source-natural promotion requires

The occurrence statement is useful only if the selected pair is a physical
restriction of complete source rows.  A sufficient hypothesis is a
**parent-resolving restriction** `Pi_(M,C_e)` with all of the following.

1. It retains the literal output word, source grade, operation, cap, window,
   fine matching, and tail labels.
2. It selects every companion occurrence with the same retained tail; it
   does not select one monomial from a cancelling aggregate by decree.
3. In each of the three permanent-triangle rows, restriction/reinsertion is
   a Cartesian product with one row-independent tail family.
4. Its proper boundary faces are existing source operations, so applying
   the restriction does not change `H0` or add an absolute presentation
   cell.

Under these conditions, (3) gives the promised recurrence.

* If the selected mixed restriction has one occurrence, it is a singleton
  unit.
* If the selected three rows have the same nonzero total tail, the permanent
  triangle identity applies.
* Otherwise (2)--(4) replace the terminal component by a strictly smaller
  labelled alternating core.

If the tail total cancels, or a companion uses a different word/fine/tail
label, none of these conclusions is source-valid.  A support monomial is
not a substitute for the total cofactor required by the complete row.

## 4. Exact nine-cell parent-selector guard

On six sites take cap `34` with all three direct colours live.  In colour
one use

```text
long parent    M0 = 05|12|34,       weight  2
short parent   M1 = 01|25|34,       weight -2
escape         N  = 01|23|45,       weight  1.             (6)
```

One rational cell assignment realizing these products is

```text
34;0=34;1=34;2=1,
05;1=2, 12;1=1,
01;1=-2, 25;1=1,
23;1=-1/2, 45;1=1.                                    (7)
```

Complete expansion over all 729 words and all 15 perfect matchings has only
three nonempty rows:

```text
111001 : M1(-2) + M0(2)                  = 0
111111 : N(1)  + M1(-2) + M0(2)         = 1
111221 : M1(-2) + M0(2)                  = 0.             (8)
```

Thus both selected mixed equations and the colour-one pure normalization are
exact, and the forced escape `N` is unique.  Nevertheless its alternating
intersection depends on which live cap parent is chosen:

```text
M0 triangle N : one C6, no common edge,
M1 triangle N : one C4, common tail 01.                   (9)
```

The occurrence-minimal choice is `M1,N`.  Restricting the pure row to terms
containing `01` gives

\[
                            -2+1=-1.                       \tag{10}
\]

This is neither a zero row nor the normalized pure row.  It is a proper
sub-sum with no coefficient-word label of its own.  The valid physical
combination `F_111111-F_111001=1` isolates the total escape scalar, but it
does not transport the other `3^(N-2)` output rows required for a smaller
exact source or a permanent-triangle section.

This guard is robust against choosing the support-minimal escape: `N` is the
only escape.  The ambiguity is in its cancelling cap parent, not in the
escape sum.

## 5. Scope and exact remaining theorem

The nine-cell packet is not a Krenn source: the pure words `000000` and
`222222` are absent.  It is a genuine exact guard to the proposed local
inference from

```text
nonzero pure escape + shortest alternating intersection
```

to a source-natural row or contraction.  Completing its other pure rows may
create a singleton, active cap, or a new escape; the checker does not claim
otherwise.

The weakest all-order theorem still needed is therefore:

> In a full exact source, for at least one forced pure escape and one
> cap-sector parent, the alternating-component restriction (2) is realized
> by a complete source-labelled parent-resolving restriction; or a companion
> omitted by that restriction is itself a singleton/active outside channel.

This is the same occurrence-selector issue exposed independently by the
local comparison route.  Without it, the potential (4) is monotone on
matching occurrences but not on physical coefficient equations.

## Reproduction

```bash
python3 computations/verify_uniform_forced_pure_escape_alternating_potential.py
python3 -O computations/verify_uniform_forced_pure_escape_alternating_potential.py
python3 -I -S computations/verify_uniform_forced_pure_escape_alternating_potential.py
```

All modes audit the uniform normal form, the exact order-six/eight ledgers,
the rational cell weights, all complete word coefficients, and the first
unavailable shortest-cycle restriction.
