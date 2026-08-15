# Minimality makes tight-cut derivatives independent; it does not delete a pure escape

## Outcome

Let an exact finite aggregate source be support-minimal among exact sources at
the same order, where support means occupied endpoint-decorated aggregate
cells.  On a tight cut, every perfect matching uses exactly one cut cell.
Consequently the complete matching tensor is jointly linear in all live cut
coefficients.  The physical derivative tensors of those coefficients are
linearly independent.

This gives a source-natural reduction: if two separated labelled cut states
have equal or proportional physical derivatives—or, more generally, if their
derivatives satisfy any linear relation—move the cut coefficients along that
kernel relation until one live cell becomes zero.  Every output equation is
unchanged, contradicting support minimality.

The statement is exact only **after physical augmentation**.  Formal
independence of word/fine/operation/cap-window labels in a free occurrence
module has no minimality consequence unless those labels define distinct
physical derivative tensors.

A forced pure escape cannot in general be deleted.  The smallest nontrivial
exact counterguard is the ternary one-factor source on `K4`: across a
one-vertex tight shore its three cut derivatives are exactly the three pure
target tensors.  They are linearly independent, and deleting any one loses
its normalized pure row.  Thus pure normalization proves that some escape is
live, but not that it is redundant or contractible.

The exact checker is
`computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py`.

## 1. Joint linearity on a tight cut

Let `L|R` be a cut in the occupied support graph, and let

\[
 J=\{j=(uv,a,b):u\in L,v\in R,\ A_{uv}(a,b)\ne0\}       \tag{1}
\]

be its live endpoint-decorated cells.  Assume every compatible perfect
matching contains exactly one member of `J`.  Write its coefficient as
`q_j`.  Partitioning the literal matching expansion by that unique cell gives

\[
                   H(A)=\sum_{j\in J}q_jD_j,             \tag{2}
\]

where

\[
                       D_j=\frac{\partial H}{\partial q_j} \tag{3}
\]

is the complete physical output tensor of the two near-perfect shore states
and the crossing endpoint basis.  Since no matching contains two cut cells,
`D_j` is independent of every `q_i`.  Thus (2) is simultaneous linearity,
not merely linearity one cell at a time.

The derivative retains source provenance termwise.  A basis occurrence of
`D_j` has the labels

```text
output word, fine matching, tight-cut derivative operation,
oriented cap window L>R, endpoint colours, left/right cofactor states.     (4)
```

But `D_j` in (2) is their scalar augmentation into the original coefficient
tensor.  Minimality applies to this physical tensor.

## 2. The exact minimality argument

Suppose

\[
                         \sum_{j\in J}h_jD_j=0             \tag{5}
\]

with some `h_p != 0`.  Because `p` is live, `q_p != 0`.  Put

\[
 t=-q_p/h_p,\qquad q'_j=q_j+t h_j.                         \tag{6}
\]

Then `q'_p=0`, and (2), (5) give

\[
                 \sum_jq'_jD_j=\sum_jq_jD_j=\Delta.       \tag{7}
\]

Every noncut cell is unchanged.  Other cut cells may also become zero, which
only decreases support further.  Arbitrary complex coefficients are allowed,
so (6) is again a finite decorated aggregate source.  It has strictly smaller
occupied support and the same exact tensor, contradicting minimality.

Hence:

> **Tight-cut minimal derivative theorem.**  In a support-minimal exact
> aggregate source, the complete physical derivative tensors of the live
> cells on a tight cut are linearly independent.

Immediate consequences include:

* a zero derivative cannot occur on a live cut cell;
* two cells with the same physical derivative cannot both remain live;
* proportional separated blocks can be combined and one deleted; and
* the number of live cut cells is at most the dimension of their physical
  output multigrade.

This is the precise minimality lever missing from a purely labelled transfer
module.  It is stronger than comparing support graphs and weaker than a site
contraction.

## 3. What the pure target equation says

For a constant-colour word `c^N`, equation (2) reads

\[
                 \sum_{j\in J}q_j(D_j)_{c^N}=1.           \tag{8}

Therefore at least one cut derivative has a nonzero pure projection.  If an
internal packet has already been killed by a mixed equation, a reinsertion
decomposition such as `qH+Escape=1` similarly proves that the total escape
projection is nonzero.

Neither assertion supplies a relation of the form (5).  In fact a derivative
which is the only contributor to one pure coordinate is visibly essential:
deleting it changes the right side of (8) from one to zero.  Thus minimality
turns dependence into deletion, but pure liveness by itself points in the
opposite direction.

## 4. Exact `K4` counterguard

On vertices `0,1,2,3`, take the three one-factors

```text
colour 0 : 01|23,
colour 1 : 02|13,
colour 2 : 03|12,                                      (9)
```

with every displayed decorated cell equal to one and every other cell zero.
Direct expansion of all `3^4=81` words is exactly

\[
       e_0^{\otimes4}+e_1^{\otimes4}+e_2^{\otimes4}.    \tag{10}
\]

Use the shore `{0}|{1,2,3}`.  Every perfect matching crosses it exactly once.
The three live cut cells, with all labels retained, are

```text
01;00, word 0000, fine 01|23, cap 0>1, cofactor 23;0,
02;11, word 1111, fine 02|13, cap 0>2, cofactor 13;1,
03;22, word 2222, fine 03|12, cap 0>3, cofactor 12;2.    (11)
```

Project their derivative tensors to the three pure coordinates.  The matrix
is exactly

\[
                              I_3.                         \tag{12}
\]

Thus their physical derivative rank is three.  Deleting `01;00`, for example,
sets the `0000` coefficient to zero; the other two derivatives have no
`0000` component and cannot repair it.  The same holds cyclically.  The
checker also verifies that all six decorated cells in (9) are indispensable
and checks joint linearity under a nontrivial rational perturbation of all
three cut cells at once.

There is an even smaller degenerate example at order two, where the three
diagonal cells of the single edge are already the pure derivative basis.
The `K4` example is the smallest one with a nonempty cofactor state, so it is
the relevant boundary-transfer counterguard.

This is a full exact ternary source, not merely a selected coefficient row.
It does not contradict the conjecture, whose nonexistence range begins at
larger even order.

## 5. Consequence for terminal-ear contraction

Minimality proves a coefficient-cell deletion precisely when a physical
kernel relation (5) is available.  It does **not** itself contract vertices
or produce an exact source on `N-2` sites.  A terminal-ear contraction still
needs one of the following structural inputs:

1. a labelled restriction/reinsertion factorization identifying two cut
   derivatives after physical augmentation;
2. a common rank-one tail whose graph contraction is known to preserve all
   output rows; or
3. an explicit physical relation expressing the forced escape derivative in
   the span of the other live cut derivatives.

The first falsifiable next test on the contaminated permanent-triangle or
sharp `C6` packet is therefore not whether the escape has nonzero pure
coefficient.  It is whether its **complete derivative tensor**, across all
words and endpoint labels after scalar augmentation, lies in the span of the
remaining tight-cut derivatives.  If yes, (6) deletes it source-naturally; if
no, minimality certifies it as a genuinely necessary new transfer channel.

## Scope

The theorem assumes minimality among occupied aggregate decorated cells at
fixed order and a genuinely tight support cut.  It allows arbitrary complex
coefficients and cancellation.  It does not assume diagonal blocks; the
checker uses a diagonal exact source only to realize the counterguard.

It does not prove a terminal-ear exists, that a forced escape is dependent,
an `N -> N-2` descent, or an active clean cap.  It also does not promote a
left kernel in an auxiliary `B/Eq` presentation: relation (5) must hold on the
actual physical output tensors.

Run:

```text
python3 computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py --mode structural
python3 -O computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py --mode full
python3 -I -S computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
b8f641baa5a66822f2215f5243f453f460d2fa1aad0d4eb2f12e09ac6544c78f
```
