# The terminal `C6` trichotomy is packet-level, not rowwise

## Outcome

There is a smallest exact source-derived boundary-transfer module for a tight
six-cycle.  Its basis consists of literal compatible matching occurrences,
and it retains

```text
output word, fine matching, restriction/reinsertion operation,
oriented cap window, cap colour, left near-state, right near-state.       (1)
```

On this module the hoped-for **rowwise** trichotomy is false.  Two separated
blocks can have distinct full labels, a common colour, and a normalized sum,
while neither block is private and their complementary exchange is a `C6`,
not a `C4`.  A label-preserving rank-one fold is extra data; it is not created
by forgetting that the labels differ.

The corrected **packet-level** theorem is positive for the sharp terminal
`C6`.  Once its three pure channels and all mixed output rows are retained,
it has six private mixed detectors.  Each detector either remains a literal
source unit or has exactly two local mates, the two oriented complementary
`C4` flips.  All 64 packets obtained by choosing one first mate per debt still
have a private mixed row.  An occurrence outside this local matching universe
is, by definition, a labelled outside-tail exit.

The checker is
`computations/verify_uniform_terminal_c6_labelled_boundary_transfer_trichotomy.py`.
It uses no `B/Eq`, private-nine, `r0`, or declared operation generator.

## 1. The labelled transfer module

Let

```text
L={0,1,2},              R={3,4,5},
A=01|23|45,             B=05|12|34.                         (2)
```

The union of `A` and `B` is the six-cycle.  Both matchings cross the tight
shore exactly once.  Their cap windows, oriented from `L` to `R`, are

```text
A : 2>3,                B : 0>5.                            (3)
```

For a word `w` and support `S`, define the free occurrence module

\[
 {cal T}_{w,S}
   =\bigoplus_{M\text{ compatible with }w,\ C(M,w)\subseteq S}
       k\,[w,M,\mathrm{res/ins},\overrightarrow{pq},c,L_M,R_M].   \tag{4}
\]

Here `C(M,w)` is the literal set of decorated cells used by the occurrence.
The augmentation sends a basis occurrence to the product of those cells.
Its sum is exactly the ordinary coefficient of `w`; thus (4) is a labelled
presentation of an actual source row, not a new physical direct-sum equation.

This last distinction is load-bearing.  A functional selecting one basis
occurrence descends to an actual scalar detector only when the fibre has one
element (or when a separately proved source operation realizes that
functional).  Merely assigning different fine or cap-window labels to two
terms does not split their coefficient equation.

## 2. The smallest rowwise counterguard

Put all three diagonal colours on every edge of the cycle and take the pure
word `000000`.  Its occurrence fibre is exactly

\[
 [000000,A,2>3,01,45]\quad\text{and}\quad
 [000000,B,0>5,12,34].                                   \tag{5}
\]

The labels are different in every boundary slot except word and colour.
Give one selected colour-zero edge in each occurrence coefficient `1/2` and
all its other cells coefficient `1`.  The literal pure coefficient is

\[
                         \tfrac12+\tfrac12=1.             \tag{6}
\]

Hence (5)--(6) is a genuine normalized source coefficient.  It has no private
occurrence.  The two monomials have no common nonconstant cell factor.  The
symmetric difference of their fine matchings is all six cycle edges, so it
has length six and supplies no complementary `C4`.

This is the smallest alternating-cycle obstruction to a rowwise statement:
two perfect matchings have symmetric difference a disjoint union of even
cycles; a nontrivial length-four component is precisely a `C4`, while length
six is the first simple alternative.

The counterguard is deliberately scoped.  It is one exact normalized pure
coefficient, not a complete GHZ tensor.  With all three colours live on the
cycle it also has mixed singleton rows.  It refutes only the inference

```text
different labels + shared colour => private row or complementary C4.     (7)
```

It does not refute a packet theorem that uses those mixed rows.

## 3. What identical separated blocks really give

Suppose three marked local rows have two separated transfer channels and a
source-provenant fold identifies their tail factors as `T_internal` and
`T_through`, independently of the row label.  Their transfer matrix is

\[
 \bigl(u_iE_iT_j\bigr)_{i\in\{xy,xz,yz\},
                              j\in\{\mathrm{internal},\mathrm{through}\}}.
                                                                    \tag{8}
\]

After the fold it factors as

\[
             u_iE_i\,(T_{\rm internal}+T_{\rm through}).          \tag{9}
\]

This is the exact rank-one common-tail criterion in `bf8ccd3`.  If the
resulting tail is nonzero, the permanent-triangle unit survives reinsertion.
If the graph operation is a genuine removable terminal-ear contraction, the
same factorization is its coefficient identity.

Equation (9) is conditional on the labelled fold.  Distinct fine matchings or
the two cap windows in (3) do not imply it.  Conversely, equality after an
unlabelled scalar projection is insufficient: it can conceal two independent
near-states.  This is the intrinsic content behind the earlier rank-two `C6`
guard and has nothing to do with an auxiliary `B/Eq` presentation.

## 4. The corrected packet-level trichotomy

The sharp three-pure support is

```text
A edges 01,23,45 : colour 0,
B edges 05,12,34 : colours 1 and 2.                        (10)
```

Its three pure fibres are literal single occurrences with fines `A,B,B`, so
all three normalization channels are retained.  Decorating the three `B`
edges by both colours produces eight words.  Two are pure and the other six
are

```text
111221  122111  122221  211112  211222  222112.            (11)
```

Because `A union B` is connected, no nonconstant word is compatible with
both cycle matchings.  Each row in (11) therefore has a one-dimensional
occurrence fibre.  Its labelled basis occurrence is an actual private source
detector, not merely a projection from (4).

Every word in (11) has type `4+2`.  Its minority-colour pair is forced in
every compatible perfect matching.  On the four majority-colour vertices
there are exactly three pairings: the original fine and its two complementary
pairings.  The latter are the two oriented `C4` operations

```text
oriented_complementary_C4_left,
oriented_complementary_C4_right,                            (12)
```

both retaining the ordered minority cap window.  Each needs exactly two new
majority-colour cells.  The checker records the word, fine, operation, cap
order, both near-states, changed edges, and missing cells for all twelve
mates.

Consequently the exact local alternative is:

> **Tight-`C6` packet theorem.**  In the sharp pure-normalized packet (10),
> every one of the six mixed rows is either a literal private monomial, is
> repaired by one of its two oriented complementary `C4` mates, or receives
> a matching occurrence with a different tail/operation label and therefore
> exits the terminal component.

This is the requested blockwise theorem after correcting its quantifier from
one row to the full pure-normalized packet.

## 5. First repairs do not close the packet

Choosing one mate for each row in (11) gives `2^6=64` minimal repair packets.
Every choice adds twelve distinct cells.  Direct expansion of all `3^6`
words gives the residual private-row histogram

```text
 6:3   8:6   10:6   15:8   17:12   18:1
19:6  23:6   24:7   28:3   30:6.                           (13)
```

Thus every first repair packet remains terminal by a literal mixed monomial;
the best three still have six.  All three pure sectors remain present, with
occurrence-count distribution

```text
(1,4,4):16,  (1,4,6):16,  (1,6,4):16,  (1,6,6):16.        (14)
```

Equations (13)--(14) retain the pure channels rather than proving a terminal
only after discarding them.

This is a first-layer theorem, not monotonicity under arbitrary later support
additions.  It also produces an oriented monochromatic `C4` coefficient face,
not an active clean cap: no statement here constructs one covector with all
three diagonal `kappa` values nonzero or proves the full homogeneous clean
error vanishes.

## 6. Exact scope and next datum

What is proved is intrinsic to literal diagonal source coefficients:

1. the free labelled transfer object (4) and its scalar augmentation;
2. the failure of the rowwise trichotomy at the normalized `C6` row (5);
3. the packet-level private/`C4`/outside-exit theorem for (10);
4. persistence of a private detector through all 64 minimal first repairs.

What remains for a global terminal-ear theorem is one of:

* a source-derived rank-one fold producing the common tail (9);
* persistence or a source-ideal unit after arbitrary repair layers; or
* an exact theorem assembling oriented local faces into a three-colour active
  clean cap or a full-output smaller source.

The first missing datum is therefore not an operation-changing `B/Eq` arrow.
It is the intrinsic treatment of an alternating length-six labelled fibre
after it ceases to have a private word.

Run:

```text
python3 computations/verify_uniform_terminal_c6_labelled_boundary_transfer_trichotomy.py --mode structural
python3 -O computations/verify_uniform_terminal_c6_labelled_boundary_transfer_trichotomy.py --mode full
python3 -I -S computations/verify_uniform_terminal_c6_labelled_boundary_transfer_trichotomy.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
b75dd428c950a94ce6d2ec4fc4cb22e4a63a48d0f14d9607b2f97ee7a4d5f5ce
```
