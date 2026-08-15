# The six terminal-`C6` debts do not assemble into a complementary clean cap

## Outcome

The six forced debts of `844c121` retain enough physical labels to decide
the proposed complementary-face bridge.  Every debt has a retained minority
edge, a four-site window, and two possible `C4` mates.  Within its literal
output word, however, the retained edge has the minority colour and **all
four window sites have one majority colour**.  Both mate edges are therefore
monochromatic.

Colour-swapped debts can have the same physical cap, window, common tail,
and mate geometry.  They cannot be combined source-naturally: their output
word, direct cap colour, and coefficient-operation instance are different.
A live third-colour diagonal cell on the cap is likewise invisible in the
original word; using it creates a third output word rather than a
complementary residue in the same response object.

There is a positive recurrence consequence.  All three cap-colour words
have one common monochromatic residual.  A mixed zero kills that entire
cap-containing residual.  The corresponding pure normalization must then
be supplied by a cap-avoiding escape channel.  Thus the exact local outcome
is

```text
singleton, monochromatic C4 debt, or outside transfer,
```

not an automatic active clean cap.

The exact checker is
`computations/verify_uniform_c6_oriented_complementary_face_naturality.py`.

## 1. Full labelled six-debt ledger

Use the sharp cycle channel

\[
                         M=05\mid12\mid34                 \tag{1}
\]

with colours `1,2` live on all three edges.  Its six mixed edge-colour
assignments give the following complete ledger.  `Core` lists the two
majority-colour edges after deleting the retained cap, and `Mate 1/2` are
the only two alternative pairings of the four-site window.

| word | cap | window | majority/minority/third | core | mate 1 | mate 2 |
|---|---|---|---|---|---|---|
| `111221` | `34` | `0125` | `1/2/0` | `05,12` | `01,25` | `02,15` |
| `122111` | `12` | `0345` | `1/2/0` | `05,34` | `03,45` | `04,35` |
| `122221` | `05` | `1234` | `2/1/0` | `12,34` | `13,24` | `14,23` |
| `211112` | `05` | `1234` | `1/2/0` | `12,34` | `13,24` | `14,23` |
| `211222` | `12` | `0345` | `2/1/0` | `05,34` | `03,45` | `04,35` |
| `222112` | `34` | `0125` | `2/1/0` | `05,12` | `01,25` | `02,15` |

Each row has the literal labels

```text
physical cap, physical window, tail T, output word,
coefficient-operation instance, core fine matching, mate fine matching.
```

For example, the first row has

```text
cap 34, window 0125, tail T, word 111221,
core fine 05|12|34,
mate fines 01|25|34 and 02|15|34.                       (2)
```

Every edge in its core and both mates has colour `1`.  This is forced by
the word, not a choice of presentation.

The rows pair by colour swap at each retained cap:

```text
34 : 111221 <-> 222112
12 : 122111 <-> 211222
05 : 122221 <-> 211112.                                 (3)
```

Within each pair the physical geometry and tail agree, but the words and
operation instances do not.  Among the `2^6=64` choices of one mate per
debt, the number of colour-swapped pairs choosing the same geometry has
histogram

```text
0 paired: 8,   1 paired: 24,   2 paired: 24,   3 paired: 8.  (4)
```

Even the eight geometrically perfect choices in the last class have zero
same-word paired faces.

## 2. Why the complementary-cap criterion fails

The proved binary active-cap lemma has a precise colour condition.  If the
direct cap colour is `a` and the other colours are `b,c`, its star-zero
residue must be exactly the crossed permanent

\[
                       K_{bb}K_{cc}+K_{bc}K_{cb}.          \tag{5}
\]

Equivalently, each of the two oriented shores must see the colour set
`{b,c}`.  Together with the physical typing, the sufficient hypotheses are:

1. one fixed cap, window, tail, word, fine family, and response operation;
2. exactly two star-zero companion monomials, with no third companion;
3. the two source-star roles on each shore carry the two colours
   complementary to `a`; and
4. the directed noncoordinate component has nonzero direct coordinate
   `w_a`.

Under these four conditions the existing denominator-cleared construction
gives

\[
 w^TK=0,\qquad K_{00}=K_{11}=K_{22}\ne0,\qquad
 K_{bb}K_{cc}+K_{bc}K_{cb}=0.                              \tag{6}
\]

The terminal-`C6` debt satisfies none of clauses 1--3 after a colour swap.
For a single word, both shores have profile `{b}`, not `{b,c}`.  Pairing it
with the colour-swapped word changes both the word and direct cap colour.
Activating the third diagonal cap cell changes the cap endpoints to `a`, so
it creates another word.  It does not add a term to the original
coefficient.

This identifies the missing bridge exactly:

> a source-defined **word-changing response comparison** must transport the
> two colour-swapped coefficient faces into one response object while
> preserving the physical cap/window, tail, fine orientations, and proper
> faces; its star-zero projection must then be exactly (5).

Without that operation, matching identical geometry across coefficient
grades is only a projection coincidence.

## 3. Uniform common-residual escape identity

There is nevertheless a useful all-order consequence.  Fix a cap edge `e`,
a colour `b` on the remaining local window, and an arbitrary common external
tail word.  Let `z_c` be the live diagonal cap cell of colour `c`, let `G`
be the total coefficient of all cap-containing residual matchings and the
common tail, and let `E_c` be the total contribution of matchings avoiding
the cap.  The complete coefficient row is

\[
                           F_c=z_cG+E_c.                 \tag{7}
\]

The residual `G` may contain the core only, the core plus either `C4` mate,
or all three four-site matchings.  It may also contain arbitrarily many tail
matchings and cancellations.  It is independent of `c`, because recolouring
the two cap endpoints does not alter the fixed word on the complement.

For every pure colour `b` and mixed cap colour `c`, the exact identity is

\[
              z_cF_b-z_bF_c=z_cE_b-z_bE_c.              \tag{8}
\]

Suppose `z_c` is live, the `c/b` word is mixed, and the cap is terminal in
that word, so `F_c=0` and `E_c=0`.  Pure normalization gives `F_b=1`.
Equation (8) then forces

\[
                              E_b=1.                     \tag{9}
\]

Thus the pure row has a nonzero cap-avoiding escape contribution.  If no
such escape exists, the packet misses a normalized pure row.  This argument
uses the complete coefficient equations and is stable under arbitrary
common-tail reinsertion; no support minimality or genericity is used.

For the canonical `C6`, the two colours already live on every retained cap.
Adding the third colour supplies another instance of (8), not the
complementary permanent (5).  The only way to keep exact normalization is to
leave the proposed terminal component through `E_b`.

## 4. Smallest three-direct labelled counterguard

The checker freezes the smallest diagonal cap-sector packet with every
direct colour live and one binary `C4` residual:

```text
cap cells       34;0  34;1  34;2
core cells      05;1  12;1
mate cells      01;1  25;1.                              (10)
```

It has seven cells.  This is minimal within the stated model: three cells
are needed for the three direct colours, and two distinct perfect matchings
on four vertices use four distinct residual edges.

Complete enumeration of all 729 words and all 15 `K6` matchings gives only

```text
111001 : 2 terms
111111 : 2 terms
111221 : 2 terms.                                        (11)
```

Writing

\[
 H=q^1_{05}q^1_{12}+q^1_{01}q^1_{25},                    \tag{12}
\]

the three rows are `q^c_34 H`, for `c=0,1,2`.  Both mixed rows can vanish
only by killing `H`, which also kills the cap-containing pure row.  There is
no complementary clean-cap face: every residual role has colour `1`.

This packet is a counterguard to the local implication

```text
monochromatic C4 mate + live third direct colour => active clean cap.
```

It is not an exact source.  Its first full-source obligation is precisely
the escape (9) needed to normalize `111111`.  That is the intended sharp
failure: full exactness does not repair the bridge internally; it forces a
new boundary channel to which the terminal recurrence must be applied.

## 5. Consequence for the structural route

The terminal-ear/tight-shore trichotomy can now use the following exact
branch rule.

* No `C4` mate gives a mixed singleton.
* One mate gives a monochromatic binary coefficient face, not an active cap.
* Both mates give a three-term monochromatic `K4` core, not the binary
  response (5).
* Adding a third direct cap colour either misses the old word or, after
  recolouring, invokes (8) and forces a cap-avoiding pure escape.
* Only an independently source-defined, word-changing response comparison
  satisfying clauses 1--4 promotes the face to the active cap (6).

Therefore the best all-order attack is to follow the forced escape channel
and seek a decreasing terminal-core measure.  Trying to infer
three-colour activity directly from the six `C6` coefficient debts is
provably insufficient.

## Reproduction

```bash
python3 computations/verify_uniform_c6_oriented_complementary_face_naturality.py
python3 -O computations/verify_uniform_c6_oriented_complementary_face_naturality.py
python3 -I -S computations/verify_uniform_c6_oriented_complementary_face_naturality.py
```

The checker verifies the six full label records, all three colour-swapped
physical pairs, all 64 geometry choices, the six polynomial identities
(8), and the complete seven-cell counterguard ledger.
