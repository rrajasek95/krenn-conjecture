# The `h=4` overlap needs two different physical connection edges

## Verdict

The three-window overlap has an exact intrinsic Čech triangle, but it has no
lift in the currently executable physical constructor grammar.  The failure
is already at degree-zero arrows, before a protected scalar readout can
obstruct the lift.

For the fixed tail `23|45|67`, the three cap presentations are

```text
p0  0121221222 / t_23*q_(v,45|67) / (45|67; removed 23; reinserted 23)
p1  0121122222 / t_45*q_(v,23|67) / (23|67; removed 45; reinserted 45)
p2  0121122222 / t_67*q_(v,23|45) / (23|45; removed 67; reinserted 67).
```

Thus there are three physical presentation objects but only two literal word
strings.  The last two objects are still orthogonal summands because their
fine, window, removal, and reinsertion idempotents differ.

The sharp current-grammar result is

```text
formal full-label edge rank                         2
word-quotient edge rank                             1
registered physical cross-presentation edge rank   0.
```

A standard mapping cylinder called on any of `p0->p1`, `p0->p2`, or
`p1->p2` raises `MissingPhysicalArrow`: the constructor requires a physical
input chain map and does not manufacture one.

Exact checker:
[`verify_h4_collision_ks_three_presentation_connection_grammar_gate.py`](../computations/verify_h4_collision_ks_three_presentation_connection_grammar_gate.py).

## 1. The formal three-presentation complex

Let `uij` be the oriented edge from `pi` to `pj`.  The intrinsic source
overlap constructed in `f073abd` is

\[
\begin{aligned}
du_{01}&=p_1-p_0,&du_{02}&=p_2-p_0,&du_{12}&=p_2-p_1,\\
d\tau&=u_{01}-u_{02}+u_{12},&\varepsilon(p_i)&=1.
\end{aligned}                                                    \tag{1}
\]

Its dimensions and ranks are

```text
C2 -> C1 -> C0 -> Q
 1      3      3     1

ranks  1      2     1.
```

In particular `d^2 tau=0`, and the augmented complex is exact.  If all three
edges are installed without `tau`, the one-skeleton has the primitive
one-cycle

\[
                         u_{01}-u_{02}+u_{12}                       \tag{2}
\]

and `H1=Q`.  A coherence cell with boundary (2) kills it.  Edge existence
does not force that cell merely from `d^2=0`.

The same complex occurs independently for each of the four fixed collision
families

```text
forward_01=-D*s1, reverse_01=+p0*q01,
forward_02=-D*s0, reverse_02=+p1*q01.
```

Over all four families the formal dimensions are `4,12,12,4` and the ranks
are `4,8,4`.

## 2. The word quotient hides one required edge type

At the literal word level, `p1` and `p2` both carry `0121122222`.  Projecting
(1) to the two word idempotents sends

```text
u01 -> word_B-word_A,
u02 -> word_B-word_A,
u12 -> 0.
```

This projected incidence has rank one.  It shows that a word-changing
connection is necessary, but it is not the full lift problem.

Retain the three fine idempotents.  Their edge boundaries are

```text
u01: t_45*q_(v,23|67) - t_23*q_(v,45|67),
u02: t_67*q_(v,23|45) - t_23*q_(v,45|67),
u12: t_67*q_(v,23|45) - t_45*q_(v,23|67).             (3)
```

The boundary matrix in (3) has rank two.  The literal window/removal/
reinsertion labels have the identical rank-two incidence.  Their primitive
tree generators may be taken to be

```text
t_45*q_(v,23|67) - t_23*q_(v,45|67),
t_67*q_(v,23|45) - t_45*q_(v,23|67).                  (4)
```

This is the first boundary debt exposed after granting a word-only
connection.  Coarsening the three repeated labels to `P3+K2` sends (3) to
zero, but the PP bridge retains the labels in (3), so that coarsening is not
a physical filler.

Consequently a concrete spanning-tree lift needs two different instances:

1. `phi01:p0->p1`, changing the word and carrying all fine/removal/
   reinsertion labels;
2. `phi12:p1->p2`, preserving the displayed word but switching the fine,
   window, removal, and reinsertion labels.

These two arrows are sufficient for connected `H0` descent.  A symmetric
Čech lift uses the direct edge `phi02` as well and needs a coherence cell

\[
                 d\mathsf T=\phi_{01}-\phi_{02}+\phi_{12}.          \tag{5}
\]

One uniform PP-natural connection schema could generate all these concrete
instances.  The rank calculation says the schema must do both jobs; a bare
word operation cannot.

## 3. Exact audit of the current constructor grammar

The pinned executable sources provide the following operations.

| Constructor | Why it does not supply an edge in (1) |
|---|---|
| intrinsic `h=4` shuffle/Čech overlap | It identifies the coefficient/Koszul--PP carrier after forgetting physical word/fine/removal tags. |
| coefficient or Macaulay product | It is objectwise in the response or cap operation parent. |
| PP/Hasse restriction and reinsertion | It emits the three distinct presentation-labelled faces; no degree-zero identification between them is registered. |
| Cartan/Weyl and `K_Eq`/AugP2 | These are cap-internal and retain the incompatible idempotents. |
| residual-matching flip bar | The available statement is conditional at response word `110000`; it explicitly has no transport to cap `01211222/t*q_(v,N)/P3+K2`. |
| standard mapping cylinder | It is functorial on an already supplied chain map and is undefined on all three requested pairs. |

Therefore the literal cross-presentation `C1` image in the current registry
has rank zero.  This is an exact no-go for the constructors actually pinned
by the checker.  It is not a claim that an unwritten full physical source has
no additional operation.

Notice especially that the same-word edge `p1->p2` is not supplied by the
residual matching flips.  Those bars act on individual PP terms in the
response object.  Their pinned theorem says cap-grade transport is missing,
and their action does not by itself change which edge supplies the literal
`t` removal/reinsertion label.

## 4. Protected rows do not create a later obstruction

Unconditionally, target, `q`, anchor, ordinary residue, `W`, and ridge are
not defined on a physical connection because the connection does not exist.
There is nevertheless an exact conditional control inherited from
`bc1d871`.

Grant three transported local `B0` bridges with the equal normalization
`mu=1/30`.  Their protected values are

```text
target  (-mu,-mu,-mu)       q       (0,0,0)
anchor  (0,0,0)             ores   (mu,mu,mu)
W       (-mu,-mu,-mu)       ridge  (mu,mu,mu).         (6)
```

Both primitive presentation differences `(1,-1,0)` and `(1,0,-1)` vanish
on every row in (6).  As a control, they both read one on the first cap-word
idempotent `(1,0,0)`.

Thus no protected scalar debt appears after equal transport.  This does not
construct `phi01` or `phi12`: equal output values cannot pay the rank-two
source-label boundary (3).

## 5. Shortest positive theorem and terminal alternative

The shortest useful positive statement is:

> The physical PP restriction/reinsertion functor on the three overlapping
> `h=3` windows has a degree-zero connection schema which transports the cap
> word, the literal `t_i*q_(v,N_i)` degree, and the removed/reinserted edge,
> and whose three instances possess the coherence face (5).

It is enough to construct one word-changing seed and one same-word
fine/reinsertion-switch seed if relabeling naturality produces their entire
orbit and (5) is verified.

The sharp terminal alternative is also precise: if the executable physical
source grammar is declared exhaustive and still has no operation matrix
unit of either seed type, then the two rank-one differences in (4) survive.
That terminal conclusion requires the exhaustiveness declaration; the
present checker deliberately makes only the current-registry no-go.

## Scope

The result is fibrewise over the fixed tail `23|45|67`, all three window
presentations, and all four collision families.  It retains the exact word,
fine, window, removed-edge, reinsertion-edge, operation-family, and coarse
repeated labels.  It also checks the known conditional protected values.

It does not construct the missing `h=3` response-to-cap comparison, assert
that the pinned registry exhausts a future full decorated source, or promote
the equal scalar table (6) to an unconditional physical value assignment.
