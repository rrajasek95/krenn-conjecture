# Zero-Fitting two-cycles are spectator copies of a smaller alternating core

## Outcome

Let two literal binomial matching rows have coefficient matrix

\[
                 M=\begin{pmatrix}A&B\\C&D\end{pmatrix}
\]

in the free Laurent monoid of active endpoint-coloured cells.  If its
Fitting determinant vanishes by the physical exponent identity

\[
                              AD=BC,                    \tag{1}
\]

then there are unique monomials `G,H,U,V` with disjoint signed cores such
that

\[
             A=GU,\quad B=GV,\quad C=HU,\quad D=HV.     \tag{2}
\]

Thus, after localizing the active spectator factors `G,H`, both rows are the
same source relation

\[
                              U+V=0.                    \tag{3}
\]

For perfect matchings on eight sites, `U,V` are the two alternating halves
of a core on exactly four, six, or eight sites.  A zero-Fitting two-cycle is
therefore not intrinsically an eight-site critical object: it is a spectator
transport of one smaller alternating-core binomial.

This is a positive source-switch statement for the first zero-Fitting
boundary in `oo-curved-signed-cycle-fitting-lemma.md`.  It does not yet close
general SCCs.

## 1. Proof of the factorization

Regard a monomial as its exponent vector.  Equation (1) is

\[
                              A-B=C-D.                  \tag{4}
\]

The positive and negative parts of an integral vector with disjoint support
are unique.  Removing `gcd(A,B)` and `gcd(C,D)` from the two sides of (4)
therefore gives the same positive monomial `U` and the same negative
monomial `V`.  Restoring the two gcds gives (2).

For two perfect matchings, removing their common edges leaves a disjoint
union of alternating even cycles.  Distinct perfect matchings of `K8` share
zero, one, or two edges, so the core contains respectively eight, six, or
four sites.  The factors `G,H` are perfect matchings on the complementary
spectator sites, with their literal endpoint colours retained.

The exact `K8` census is:

| core edges in each half | core sites | spectator sites | ordered pairs |
|---:|---:|---:|---:|
| 2 | 4 | 4 | 1,260 |
| 3 | 6 | 2 | 3,360 |
| 4 | 8 | 0 | 6,300 |

The four-site complement has three possible spectator matchings; the other
two complements have one.  This gives 13,440 reconstructed zero rectangles,
all checked directly.

## 2. What the source switch buys

The word difference between two parallel rows lies entirely in the
spectator factors.  The alternating core has the same literal decorated
cells and the same core word in both rows.  Consequently:

* if the two full-word colour multiplicity partitions differ, relation (3)
  can be represented by the word with the lexicographically larger sorted
  multiplicity partition, a label-independent move toward a pure colour;
* if the partitions agree, the spectator move is a genuine residual orbit
  and needs additional source coupling; and
* among all possible spectator decorations, a pure word can occur exactly
  when the core word is monochromatic.  A particular physical packet need
  not contain the required monochromatic spectator cells.

The parallel component in the committed 177-cell curved packet is of the
strict first kind:

```text
20120121 : (3,3,2)
21120121 : (4,3,1).
```

So its zero Fitting minor is not a terminal local obstruction: it is the
same core relation carried one step closer to the pure-colour partition.
This orientation alone does not assert that the pure-1 spectator route is
present in the packet.

This does not resurrect a fixed word order.  Equal-partition transports and
the known equal-word `C4 x C4` square remain, exactly as required by the
existing counterguards.  The useful invariant is the colour partition plus
the source-labelled alternating core, not an absolute site-word lex order.

## 3. Four-site core closure

On four core sites there are exactly three perfect matchings `U,V,W`.  If
source transport supplies all three pair relations

\[
                       U+V=V+W=W+U=0,                  \tag{5}
\]

their coefficient matrix is

\[
 \begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix},
 \qquad \det=2.                                        \tag{6}
\]

After localizing the active cells, (6) is the ordinary odd-hafnian unit.
Hence a four-site zero component can survive only while at least one of the
other two source-labelled pair routes is absent or contaminated.  This
turns the smallest zero-Fitting alternative into a concrete opposite-route
problem rather than an unspecified vanishing minor.

## 4. Remaining theorem

This note proves the source switch only for a two-row zero-Fitting block.
The proof-completing continuation must show that an arbitrary critical SCC
either

1. contains a nonzero signed cycle/Fitting minor;
2. decomposes into these spectator copies and terminates under the colour
   partition/core order; or
3. on an equal-partition or six/eight-site core, the complete full-nine rows
   supply a four-site odd completion, a smaller exact source, or an active
   clean cap.

The known equal-word even square belongs explicitly to item 3.  It is killed
in its complete packet by the separate tensor-fan identity, so it is not a
counterexample to the proposed global alternative.

## Verification

Run

```text
.venv/bin/python computations/verify_oo_zero_fitting_spectator_factorization.py
.venv/bin/python -O computations/verify_oo_zero_fitting_spectator_factorization.py
```

The checker proves the free-monoid factorization, enumerates all 10,920
ordered pairs of distinct `K8` perfect matchings and all 13,440 spectator
replacements, classifies every core size, audits all spectator colour-word
partitions, and verifies the four-site determinant `2`.
