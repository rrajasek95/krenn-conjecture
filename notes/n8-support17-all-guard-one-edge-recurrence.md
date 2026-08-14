# Support 17: uniform one-edge recurrence over all 148 cap-dark guards

## Theorem

Every coordinate one-edge augmentation of every pure-supported,
binary-cap-dark completion in the 148-orbit support-16 frontier has an exact
exit.  The new edge either creates an active-clean cap or fails to repair the
inherited singleton mixed-row debt.

This is an augmentation theorem, not a fresh support-17 graph census.  It
reuses the complete support-16 completion search and adds only perfect
matchings that contain the inserted edge.

The exact totals are

```text
support-16 completion charts                81,685
  two-coordinate target support             54,891
  full target support                       26,794

coordinate edge/colour augmentations     2,940,660
  active-clean cap exits                    71,751
  inherited singleton by cardinality     2,868,903
  inherited singleton by literal check           6
  necessary exact-source counterguards            0.
```

The checker is

```text
python3 computations/verify_n8_support17_all_guard_one_edge_recurrence.py
python3 -O computations/verify_n8_support17_all_guard_one_edge_recurrence.py
python3 -I -S computations/verify_n8_support17_all_guard_one_edge_recurrence.py
```

## Exact recurrence mechanism

Fix one support-16 completion and let `S` be its set of singleton mixed
words.  For a missing edge `e`, every genuinely new perfect matching in
`G+e` contains `e`.  Therefore the coefficient of an inherited word can
change only if one of those new matchings has exactly the same literal
eight-site colouring.

The audit precomputes, for each missing edge:

1. the new matchings containing that edge;
2. every complete physical cap response through the fixed directed
   nonanchor;
3. newly private cap faces; and
4. newly complementary crossed-binary cap faces.

For each coordinate colour of `e`, it first tests the cap exits.  If the cap
remains dark, it compares `|S|` with the maximum number of new decorated
matching occurrences.  When the latter is smaller, at least one inherited
singleton survives without any word expansion.  This cardinality certificate
settles `2,868,903` augmentations.

Only six augmentations pass that bound.  Direct source-labelled word
comparison shows that each still misses at least one inherited debt.  No
case even reaches the stage of producing a singleton-free new word ledger.

## Strength of the debt bound

Every support-16 completion in the census has at least seven singleton mixed
words.  The full inherited-debt histogram is

```text
 7:     6    8:    30    9:   336   10:  2,328
11: 19,887   12:18,288   13:21,481   14:  9,639
15:  2,634   16: 5,438   17:   996   18:    384
19:    238.
```

This explains why the recurrence is nearly uniform before any detailed cap
algebra: one new edge almost never creates enough matching occurrences to
mate the old debt set.

## Scope

The theorem closes all coordinate one-edge descendants of the 148
support-16 completions that survived until the binary-cap/complete-row
dichotomy.  It does not yet cover

- descendants of the 133 support-16 orbits already landed by the original
  two-cap, complete-private, or collision-normalization routes; or
- a genuinely noncoordinate inserted edge.

Those are different persistence questions.  For an old active cap, new
response monomials may destroy the old zero and the cap covector must be
deformed.  For a noncoordinate insertion, one new matching can contribute
two or three decorated words and the coordinate-colour cap classification no
longer applies directly.  The finite failure strata of those two mechanisms
are the remaining support-17 task.
