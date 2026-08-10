# The first independent mixed transition has a private-word gate

## 1. Unique primitive two-cycle

Work in the coefficient-complete tilted chart from
[`the mixed bright-completion theorem`](shared-reciprocal-two-bad-mixed-bright-completion.md).
It contains

```text
12:aa, 34:cc, 02:ta, 01:cc, 03:aa,
an arbitrary block B on 04 with b_tt!=0.
```

The existing `02:ta` cell can belong to a primitive two-transition
matching exchange only by pairing the pure cells `04:tt` and `12:aa`.
The other transition is uniquely

```text
14:at.                                                (1)
```

Indeed, the `t` endpoint left by `02` must be site `4`, and the `a`
endpoint left by `12` is site `1`.  The other pure `aa` leader `03` meets
`04` and cannot form a four-site exchange.  This classifies the two-edge
transition graph up to the already-fixed site and colour symmetries.

## 2. The unpaired transition kills a bright class

Give (1) an arbitrary nonzero coefficient `y`.  In the cofactor `K_2`, the
matching `03:aa,14:at` creates

```text
(a,a,a,t) on sites (0,1,3,4), coefficient y.
```

After inserting colour `c` at hole `2`, this becomes the five-site private
word

```text
Omega=(a,a,c,a,t).                                    (2)
```

The same column `(2,c)` is the unique column carrying `X_c`, with
coefficient `1`, and it is also the unique column carrying (2), with
coefficient `y`.  Therefore the pure row would force its coefficient to be
`1`, while the mixed row would force `y=0`.  For `y!=0`,

```text
X_c notin im(Phi).                                    (3)
```

This argument is uniform in all nine coefficients of the arbitrary block
`B`; it is a literal coefficient obstruction, not a support relaxation.
Thus the first independent transition cannot be adjoined naked.

## 3. A source-faithful path-switch repair

The primitive cycle is not itself a contradiction.  The checker freezes
the rational packet

```text
12:aa=1, 34:cc=1, 02:ta=1, 01:cc=1, 03:aa=1,
04:tt=1, 14:at=1,
04:at=-1, 13:aa=1, 03:ta=-1.                           (4)
```

The `04:at,13:aa` path cancels the private word (2).  Its induced
contamination of the `a`-bright cofactor is canceled by `03:ta`, which at
the same time cancels the second mixed word in `K_2`.  Literal matching
reconstruction gives

```text
K_0 = AACC,
K_1 = TACC,
K_2 = CCCC,
K_3 = 2 TAAT - AAAT,
K_4 = AAAA.                                            (5)
```

Consequently `X_a,X_c` lie in `im(Phi)`, while `X_t` does not.  Exact
linear algebra over `Q` gives

```text
rank(Phi)=14,
ker(Phi)=<e_t@0-e_a@1>,
rank(im(Phi)+all kernel products)=16,
augmented pure intersection=span{X_a,X_c}.             (6)
```

Thus the first primitive colour cycle has two sharply different outcomes:
unrepaired it loses a bright target by a private row; after the smallest
displayed path switch it becomes coefficient-feasible but still has only
one tilted kernel and cannot carry the missing nonlinear pure class.

## 4. Scope

This is an exact theorem/counterguard on the canonical first-transgression
chart.  It is not an exhaustive classification of arbitrary multi-centre
bright lifts, and (4) is not an eight-site source or a counterexample to
Krenn's conjecture.  It shows that the next genuine escape needs a second
independent cofactor-kernel direction, not merely a primitive colour cycle.

## 5. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_mixed_primitive_cycle_gate.py
uv run python -O computations/verify_shared_reciprocal_two_bad_mixed_primitive_cycle_gate.py
```

Both modes reproduce

```text
cbcb78393ffb64bb63989c9a486f9bfea509679eb981e3c7aa05294273caa41b
```
