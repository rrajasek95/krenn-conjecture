# A diagonal target arm cannot mate a crossed lock into a distinct-head overlap

## Result

The tempting shortcut from the sharp residual of `016886b` is false for an
exact local reason.  Write the collected lock components on physical pairs
as

\[
 L_{12}^{rs}=p_1^r\otimes s_2^s\otimes K_{12}^{rs},\qquad
 L_{22}^{ts}=p_2^t\otimes s_2^s\otimes K_{22}^{ts}.       \tag{1}
\]

Even when both cofactors in (1) are nonzero, the two arms have the identical
head line `span(s_2^s)` at their common site.  Every centre `2 x 2` minor is
therefore zero.  Dually, `L_12^{rs}` and `L_11^{rt}` repeat the factor
`p_1^r` at `r` and have the same obstruction.

Consequently a selected nonzero diagonal target arm cannot replace the
opposite crossed `L_21` mate in the four-good landing theorem.  The exact
remaining input is still either an opposite crossed mate or a source-valid
arm exchange which changes the shared-site factor.

Checker:
`computations/verify_uniform_five_lock_diagonal_mate_obstruction.py`.

## The same-head identity is coefficient independent

For a completely arbitrary local vector `v=(v_0,v_1,v_2)`, the three
Pluecker coordinates of two copies of its line are

\[
 v_0v_1-v_1v_0,quad v_0v_2-v_2v_0,quad
 v_1v_2-v_2v_1,                                      \tag{2}
\]

and hence vanish over every commutative ring.  Equation (2), not an
axis-purity specialization, is the obstruction.  The checker represents
the entries by independent symbolic monomials and verifies all six minors:
three for the common `s_2` factor and three for the dual common `p_1`
factor.

The nonzero diagonal target coefficient only certifies that its cofactor is
active.  It does not change the local head line in (1), so activity cannot
repair the missing transverse minor.

## Deleted-star rank audit

There are two physically distinct cases.

1.  Take the canonical three pure target matchings

    ```text
    Q0 = 01|23|45|67
    Q1 = 02|13|46|57
    Q2 = 03|12|47|56.
    ```

    For `L_12` on `04` and `L_22` on `14`, both pairs avoid the union of
    the selected anchor edges.  Each pure matching therefore leaves one
    independent coordinate column at each deleted endpoint.  All four
    deleted-star ranks are three.  Nonzero collected lock coefficients
    make both cofactors active, but the two heads at site `4` are both
    `s_2^4`.  This is a four-good active **flat** overlap, not the
    distinct-head/curved landing required by `016886b`.

    The dual audit uses `L_12` on `04` and `L_11` on `05`.  Again all four
    selected-anchor ranks are three, but both heads at site `0` are
    `p_1^0`.

2.  If the diagonal mate lies on a selected anchor edge, the rank shortcut
    also fails.  For `L_12` on `04` and `L_22` on the `Q0` edge `45`,
    deleting `45` removes the `Q0` coordinate column at both endpoints.
    The selected pure anchors guarantee ranks

    ```text
    (3,3) on 04 and (2,2) on 45.
    ```

    Extra source columns could raise the actual ranks on `45`; the claim is
    only that the three fixed pure anchors no longer prove four-goodness.
    Independently of such extra columns, the common head remains `s_2^4`
    and its wedge remains zero.

Thus moving the diagonal arm onto an anchor edge cannot evade (2), and it
introduces a second, separate gap in the automatic rank argument.

## Consequence for the five-lock residual

The sharp residual from `016886b` was an injective five-row lock map with no
complementary crossed wedge.  The present audit rules out the shortest
attempt to fill that wedge with a diagonal row:

\[
 L_{12}+L_{22}\quad\hbox{or}\quad L_{12}+L_{11}
 \quad\Longrightarrow\quad\hbox{same shared head}.      \tag{3}
\]

Therefore the proof must return to common-provenance crossed mating.  It
must either produce an `L_21` component on a pair sharing the appropriate
port, or furnish a source-valid arm exchange/reselection that replaces one
of the repeated factors before applying the four-good theorem.  Unary and
diagonal target nonvanishing alone do not supply that exchange.

## Verification and scope

Run

```text
python3 computations/verify_uniform_five_lock_diagonal_mate_obstruction.py
python3 -O computations/verify_uniform_five_lock_diagonal_mate_obstruction.py
python3 -I -S computations/verify_uniform_five_lock_diagonal_mate_obstruction.py
```

The checker pins the five-lock theorem and the nonanchor good-pair theorem,
verifies the coefficient-independent repeated-factor identity, audits both
off-anchor diagonal mates and the selected-anchor rank loss, and records
the exact remaining crossed-mating requirement.  It does not assert that
the full physical source lacks additional star columns or a source-valid
arm exchange.

Frozen ledger SHA-256:

```text
a4ffd2b3e7afa21c6baab8f56a560d750e794732d0e717eb100bbd8cc496d927
```
