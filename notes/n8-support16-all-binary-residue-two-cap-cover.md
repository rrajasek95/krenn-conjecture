# Support 16: binary cap or complete-row singleton

## Outcome

The complete 281-orbit directed-incidence register at the 22 two-RRX
support-16 graphs has no source-compatible anchor guard left.

The rank construction first extends from `(2 target,2 residue)` faces to
**every** cap face whose star-zero residue is a crossed pair of oriented
monomials.  That extension alone does not close a new orbit uniformly: every
one of the prior 148 orbits has a two-coordinate anchor completion avoiding
all such cap landings.  The exact-source rows do close them.  Among 81,685
symmetry-reduced completions which both avoid every binary-cap landing and
retain all three pure rows, every completion has a singleton mixed fibre.
Therefore none can be an exact source.

The final finite dichotomy is

| route | stabilizer orbits | directed incidences |
|---|---:|---:|
| original forced-distinct two-cap | 22 | 25 |
| complete private cap | 110 | 153 |
| pure-normalization collision exit | 1 | 1 |
| binary cap, missing pure row, or mixed singleton | 148 | 197 |

Thus all `281/376` directed incidences in this register land or contradict a
complete source row.  The theorem is for the mutual-coordinate anchor chart
of the 22 two-RRX support-16 orbits; it does not by itself classify the four
three-seal support graphs or arbitrary higher support.

The exact checker is

```text
python3 computations/verify_n8_support16_all_binary_residue_two_cap_cover.py
python3 -O computations/verify_n8_support16_all_binary_residue_two_cap_cover.py
python3 -I -S computations/verify_n8_support16_all_binary_residue_two_cap_cover.py
```

## 1. The larger binary-face rank lemma

Fix a directed noncoordinate source-star block `X` in a physical cap
response.  Split the fully oriented response into monomials containing `X`
and its star-zero residue.  Suppose the residue has two monomials, crossed on
the same two source-star edges at each cap endpoint.

Let the cap edge have direct anchor colour `a`.  If the two residue stars on
each shore carry the complementary colours `b,c`, the residue is, up to
shore ordering,

```text
K_bb K_cc + K_bc K_cb.
```

If `w_a != 0` for the vector `w` of `X`, noncoordinate `w` has at least one
nonzero coordinate among `b,c`.  The imported denominator-cleared rank-two
matrix then satisfies

```text
w^T K = 0,
K_aa = K_bb = K_cc != 0,
K_bb K_cc + K_bc K_cb = 0.
```

The transpose gives the right-endpoint version `K w=0`.  Crucially, the
number of target-containing monomials is irrelevant: the literal `X` kernel
kills all of them.  The checker re-verifies all 12 left charts and all 12
transposed right charts.

The exact combinatorial landing criterion is therefore:

1. the star-zero residue is a crossed pair;
2. the cap and both residue shores use the three complementary colours; and
3. the direct coordinate of `w` is nonzero.

Merely seeing two residue monomials is not enough.  At degree five or six,
the residue shore colours need not complement the cap colour; this is why a
coarser direct-colour count incorrectly predicts extra exits.

## 2. Exhaustive source-row dichotomy

After the original two-cap, complete-private, and collision-normalization
routes, 148 stabilizer orbits remain.  Their counts of binary-compatible cap
faces are

```text
0 faces : 47 orbits
1 face  : 43 orbits
2 faces : 39 orbits
3 faces : 19 orbits.
```

For every orbit the checker searches both possible noncoordinate support
types:

- support two, with the missing coordinate fixed to 0 by colour symmetry;
- support three, with one anchor colour fixed by global symmetry.

Every non-target support edge is assigned one coordinate colour, and every
site must see all three anchor colours.  A search branch is rejected as soon
as a binary cap meets the three conditions above.  Pure-support feasibility
is monotone-pruned using the literal perfect matchings of the support graph.

At each surviving complete colouring, the checker expands every decorated
perfect-matching occurrence, including each live component of the target
nonanchor, and groups occurrences by the exact eight-site word.  An exact
source must have

- at least one occurrence in each of the three pure words; and
- no mixed word with exactly one occurrence.

The second condition is coefficient-independent: a singleton coefficient is
a product of live anchor weights and one live target component, hence cannot
vanish or cancel.

The exhaustive ledger is

```text
search nodes                         5,088,249
pure-support monotone prunes           423,289
pure-supported avoiding completions     81,685
those with a mixed singleton             81,685
singleton-free necessary guards               0.
```

So every anchor chart has one of three exits: a binary active-clean cap, a
missing normalized pure row, or a mixed singleton/unit row.

## 3. Smallest local cap obstruction

The sharpest warning against trying more two-cap or three-cap rank algebra is
graph index 11, the shared orbit of size two at directed incidence `2 -> 02`:

```text
01 02 03 05 07 13 14 15 16 24 25 27 34 37 46 56.
```

It has only two physical cap occurrences:

```text
cap24 : 12 target terms + 4 residue terms
cap25 :  4 target terms + 4 residue terms.
```

Neither face is private or binary, and there is no third cap on which to run
a three-cap construction.  This is the smallest genuine local obstruction
to the present cap-rank method.

The checker freezes a two-coordinate global anchor completion for it.  That
completion has exactly one occurrence in each pure word, so normalization
support does not remove it.  It has twelve singleton mixed words; the
lexicographically first is `00100001`.  Hence its first complete-source
failure is a singleton mixed row, not another cap polynomial.

This distinguishes local persistence from an exact-source counterexample.
Adding support can retain or enlarge the four-monomial residues on these two
faces, but any higher-support exact source must add mates for the singleton
words or create a new cap landing.  That matching-debt alternative is the
right invariant to carry to support 17 and above.
