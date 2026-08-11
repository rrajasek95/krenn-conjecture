# A diagonal alternating-cycle switch is controlled by its full five-row lock

## Outcome

Let the residual quadratic in a one-bad packet be `q` on `2h` sites and
write the five tensors as

\[
 T_0=q^{[h]},\qquad
 T_{ij}=p_i s_j q^{[h-1]}\quad(i,j\in\{1,2\}).       \tag{1}
\]

Suppose two occupied diagonal cells `e=vu:aa` and `f=vw:aa` meet at the
same physical coordinate `(v,a)`.  Let `d` delete or resize only these two
cells.  Then `d^[2]=0`, so the complete finite differences are exactly

\[
 \boxed{
 \begin{aligned}
 T_0(q+d)-T_0(q)&=d q^{[h-1]},\\
 T_{ij}(q+d)-T_{ij}(q)&=p_i s_jd q^{[h-2]}.
 \end{aligned}}                                      \tag{2}
\]

There are no omitted higher terms.  Thus deleting the two incident edges
of a same-word alternating cycle is an exact support descent precisely when
the five tensors in (2) vanish (or lie in nonzero diagonal target lines
which can be renormalized).  If they do not, their ordered tuple is the
literal **cycle lock**.  This is the five-tensor specialization of the
already committed blocker-lock construction, now with the binomial deletion
and mutual-anchor effect made explicit.

Cycle provenance alone does not turn a nonzero lock into the desired
distinct-head, four-good active overlap.  A nine-cell colour-diagonal
common hafnian below has two overlapping `C4` binomials.  Deleting the first
cycle preserves its chosen coefficient but exposes the second coefficient.
Every edge of both cycles has the same target head.  The missing unary and
companion response rows are therefore load-bearing in any positive overlap
theorem.

The exact checker is
[`verify_uniform_diagonal_alternating_cycle_switch_boundary.py`](../computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py).

## 1. The coefficient-preserving binomial deletion

On sites `0,...,5`, take the diagonal cells

```text
01:11 =  1    23:11 =  1    45:00 =  1
02:11 =  1    13:11 = -1

24:11 =  1    35:00 =  1
04:11 = -1    12:11 =  1.
```

There are exactly four supported perfect matchings.  They occur in two
word fibres:

\[
\begin{array}{c|c|c}
\text{word}&\text{matching}&\text{coefficient}\\ \hline
111100&01|23|45& 1\\
111100&02|13|45&-1\\
111010&01|24|35& 1\\
111010&04|12|35&-1.
\end{array}                                           \tag{3}
\]

Hence `q^[3]=0` coefficientwise.  The first pair differs on the alternating
cycle `0-1-3-2-0`.  Put

\[
                  d=-(01{:}11)-(02{:}11).              \tag{4}
\]

Both cells meet `(0,1)`, so `d^[2]=0`.  Passing from `q` to `q+d` deletes
both terms of the first word and therefore preserves its zero coefficient.
But it deletes only the positive term of the second word, leaving

\[
                     [111010](q+d)^{[3]}=-1.           \tag{5}
\]

Equation (5) is the first literal lock row.  It is not a support-shadow
claim: all four matching products and their signs are expanded from the
same decorated quadratic.

For every `h>3`, append `h-3` disjoint diagonal `22` factor edges.  Equations
(3)--(5) tensor with those factors unchanged, so the counterguard is
uniform in the residual order.

## 2. Audit of all five tensors

For an arbitrary pair of endpoint rows `p_i,s_j`, multiaffinity and
`d^[2]=0` give

\[
 (p_i s_j)(q+d)^{[h-1]}
  =(p_i s_j)q^{[h-1]}+(p_i s_j)dq^{[h-2]}.             \tag{6}
\]

The checker constructs arbitrary multisite rational representatives for
all four ordered pairs `11,12,21,22` and verifies (2) and (6) by literal
matching expansion for `3<=h<=8`.  The displayed identities prove the same
statement at every `h>=3`; the finite range is only a regression audit.

The two deleted cells are not mutual coordinate anchors: they share the
coordinate `(0,1)`.  Any old mutual anchor outside them remains unique after
deletion.  The checker verifies this directly on (3), while the coordinate
argument proves it generally.  Consequently, if the five-row lock vanishes,
the move preserves all old mutual anchors and lowers aggregate support by
two, contradicting the maximum-anchor/minimum-support choice.

## 3. Exact remaining split

At a selected full one-bad source, the diagonal cycle therefore gives the
rigorous alternative

\[
 \boxed{\text{anchor-safe support descent}\quad\text{or}\quad
        \text{a nonzero full five-row cycle lock}.}     \tag{7}
\]

The second alternative is not yet the curved overlap.  The web (3) shows
why: a lock can be another same-head diagonal alternating cycle.  Iterating
only the symmetric-difference operation can enter a compatible diagonal
lock web rather than expose an off-diagonal port.

The positive theorem still needed is source-labelled and stronger than a
cycle lemma:

> In the presence of `q^[h]=X0` and all four binary response rows, every
> compatible diagonal lock web either has a simultaneous anchor-safe
> support descent, or one literal lock comparison exits the diagonal
> anchor graph and supplies a transverse active arm with the missing
> deleted-star ranks.

The known private-site identity then routes a nonanchor off-diagonal exit
to an active determinant/cofactor product.  The separate rank-completion
boundary shows that even this product needs a distinct-head one-arm
transport before it is a four-good curved overlap.  Neither step follows
from (3) alone.

## Scope

The packet (3) is a genuine decorated common hafnian and a sharp
counterguard to a **cycle-only** implication.  It is not a Krenn
counterexample and does not refute the full five-row theorem: its top is
zero rather than `X0`, and it does not supply the two diagonal and two
crossed response targets.  Those omitted source rows are exactly the
additional data a proof must use.  No claim of a full one-bad survivor is
made.

Reproduce with

```sh
python3 computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py
python3 -O computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py
python3 -I -S computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py
```
