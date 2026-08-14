# The `h=4` overlap first fails at the physical cap word

## Verdict

The canonical shuffle triangle from `f073abd` is exact in the intrinsic
coefficient/Koszul--PP source, but it does not descend to the current
decorated collision/Kodaira--Spencer cap packet.  The first nonzero mismatch
is the physical word idempotent, before target, `q`, anchor, ordinary
residue, `W`, or ridge can become an issue.

For the tail `23|45|67`, the three presentations use the windows

```text
45|67 with spectator 23,
23|67 with spectator 45,
23|45 with spectator 67.
```

Extending each relabelled physical `01211222` window by the natural remote
`22` spectator gives

```text
0121221222,  0121122222,  0121122222.                 (1)
```

The idempotent of the first word has presentation values `(1,0,0)`, so

```text
(1,-1,0) reads 1,      (1,0,-1) reads 1.              (2)
```

This is not an artefact of the chosen endpoint ordering or the `22`
display.  There is no common six-tail-site word whose restriction to all
three four-site windows has the required cap multiset `{1,2,2,2}`.

Exact checker:
[`verify_h4_collision_ks_decorated_presentation_mismatch.py`](../computations/verify_h4_collision_ks_decorated_presentation_mismatch.py).

## 1. Fixed twelve-face packet

Use the four collision families

```text
forward_01=-D*s1       DSQ, missing/doubled 0/S,
reverse_01=+p0*q01     PQQ, missing/doubled S/0,
forward_02=-D*s0       DSQ, missing/doubled 1/S,
reverse_02=+p1*q01     PQQ, missing/doubled S/1.
```

Each has the three window presentations above, giving the requested twelve
presentation-labelled new faces.  The response-side extension is harmless:
each presentation has physical response word

```text
1111000000
```

and the same intrinsic occurrence top.  Its word, fine degree, and coarse
missing/doubled grade are therefore presentation-independent.

The cap side is different.  On every physical `h=3` cap window, the four
tail letters of `01211222` are

```text
1,2,2,2.                                                (3)
```

The operation prefix `0121` is fixed by the collision family and cap
normalization.  In particular, independent colour permutations cannot be
used to change (3) while claiming that all three presentations occupy one
fixed physical grade.

## 2. Choice-free word obstruction

Let the three disjoint tail edges be `e_i`.  If one common six-site word
existed, let `x_i` be the number of colour-`1` endpoints on `e_i`, and put

\[
                              X=x_0+x_1+x_2.
\]

Restricting away `e_i` must leave the multiset (3), hence exactly one
colour-`1` endpoint.  Therefore

\[
                             X-x_i=1
                     \quad (i=0,1,2).                 \tag{4}
\]

Thus every `x_i=X-1`, and summing gives

\[
                              X=3(X-1),
                     \qquad 2X=3,                    \tag{5}
\]

which is impossible for the integer `X`.  The checker also exhausts all
`3^6=729` six-site words and finds zero solutions.

Equation (1) is one explicit normalized representative.  Its first word
idempotent has values and overlap pairings (2).  Hence the desired decorated
structure map is not degree zero.  A coefficient-level shuffle cannot be
declared a physical word-changing homotopy.

## 3. Fine and repeated grades

The response occurrence top has one intrinsic fine label on `23|45|67`,
independent of which two edges are called the window.  The cap fine degree,
however, is the literal `t*q_(v,N)` label.  The PP bridge retains both the
removed/reinsertion edge `t` and the window matching `N`.  Its three values
are therefore

```text
t_23*q_(v,45|67),
t_45*q_(v,23|67),
t_67*q_(v,23|45).                                      (6)
```

They are three distinct fine-degree labels, while the response values are
`(g,g,g)`.

The coarse repeated topology remains `P3+K2` in all three copies, and the
missing/doubled operation grade remains fixed within a collision family.
That coarse equality is insufficient.  The literal PP-to-cap bridge retains
the window, removed edge, and reinsertion edge.  These full labels are

```text
(45|67; 23),  (23|67; 45),  (23|45; 67),               (7)
```

so all three are distinct.  Thus both fine degree and the full repeated/
removed-edge grade fail, even though the undecorated topology agrees.

## 4. Protected-row values and their exact scope

There is no unconditional physical value table for

```text
target, q, anchor/ainc, ores, W, ridge
```

on these collision/KS presentation cells.  The reason is not an omitted
calculation: the physical `11:110000 -> 01211222` collision/KS bridge is the
missing `h=3` theorem.  The universal response KS generator does not define
physical `q`, `ainc`, `W`, or the labelled ridge before that placement.

The strongest existing presentation-safe collision dual has a zero-cap
extension.  Its three presentation-coordinate values are

```text
target      (0,0,0)       q       (0,0,0)
anchor      (0,0,0)       ores    (0,0,0)
W           (0,0,0)       ridge   (0,0,0).             (8)
```

These are coordinates of the extended dual, not physical terminal values of
the absent source cells.  Equation (8) proves only that the already admitted
block does not create a later mismatch.

There is also an exact conditional table.  Suppose each presentation is
given a transported local bridge to its `B_0` cap corner, with coefficients

\[
                         \mu=(\mu_0,\mu_1,\mu_2).
\]

The known `r0,T,rho,K` cap/Cartan equations force

\[
\begin{array}{c|c}
\text{row}&\text{three presentation values}\\ \hline
\text{target}&-\mu\\
q&0\\
\text{anchor/ainc}&0\\
\text{ores}&\mu\\
W&-\mu\\
\text{ridge}&\mu.
\end{array}                                           \tag{9}
\]

For the normalized equal choice

\[
                    \mu_0=\mu_1=\mu_2=1/30,
\]

both primitive difference detectors vanish on every row in (9).  Thus there
is no additional scalar obstruction after granting three equal transported
bridges.  They still lie in the incompatible word/fine/repeated summands of
Sections 2--3, so this conditional scalar equality is not physical descent.

As a control, one isolated bridge with
`mu=(1/30,0,0)` is read by `(1,-1,0)` as

```text
target -1/30, q 0, anchor 0, ores +1/30,
W -1/30, ridge +1/30.                                  (10)
```

This recovers the exact local cap/Cartan extension formula and confirms that
the overlap test sees an unequally installed bridge.

## Consequence

The source-level `h=4` Leibniz and triangle signs are closed, but physical
uniformization stops at a degree-zero grade problem:

> Construct a word-changing `h=4` overlap/connection cell between the three
> window-labelled `01211222` copies, retaining fine, removed-edge, and
> reinsertion labels.

Only after this cell exists do the equal-`mu` formulas (9) supply the
protected scalar descent.  Without it, the word-idempotent row (2) is the
first exact mismatch.

## Scope

The checker covers the fixed tail `23|45|67`, all four collision families,
all twelve presentations, the choice-free `729`-word exhaustion, and the
known cap/Cartan protected-row formulas.  The counting proof is invariant
under tail relabeling and window orientation.

This is not a spectator-suspension argument and makes no tensor
factorization of the GHZ target.  It does not construct the missing `h=3`
physical bridge, assert an exhaustive global terminal covector, or call the
formal zero-cap extension a physical terminal assignment.
