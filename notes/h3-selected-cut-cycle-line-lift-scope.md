# Correction: the selected cut cycle still needs one full-row equality

## Corrected result

Commit `de74a1a` claimed that the twelve-label collapse and the physical
output cell

\[
                         M_v=-O_\alpha+K
\]

already define a chain map on the selected two-term line.  That conclusion
was too strong and is withdrawn here.

The exact reduction proved by `6fd2412` is instead this.  For

\[
 v=P_{024}-P_{012},\qquad \ell=u_{024}-u_{012},
\]

the three shared repeated-`02` coordinates of `ell` are zero.  Hence a full
map on all fifteen collision labels is unnecessary for this selected
branch.  But one complete physical chain equation is still required:

\[
                         J_3(M_v)=A J_{\rm col}(\ell).       \tag{1}
\]

The current collapse computes only the occurrence projection of the
right-hand side.  The `M_v` audit computes the complete output packet on the
left.  Neither result exposes the undisclosed protected/source-labelled
rows of `J_col(ell)`, so they do not prove (1).

Checker:
[`verify_h3_selected_cut_cycle_line_lift_scope.py`](../computations/verify_h3_selected_cut_cycle_line_lift_scope.py).

## Why occurrence agreement is insufficient

The checker pins the hidden-row counterguard of `6fd2412`.  Two complete
input boundary maps have identical disclosed occurrence rows but values
zero and one, respectively, on `ell` in one additional private row.  Only
the first can agree with a candidate whose value in that row is zero.
Thus the twelve-label support identity and the 360-feature output census do
not determine (1).

The correct local simplification is therefore

```text
full U15 comparison:               unnecessary for the selected vector;
one full-row equality on ell:       still necessary and currently open.
```

This keeps the useful part of `de74a1a`—the shared-loop values do not enter
the selected vector—while removing its tautological `1 x 1` chain square.
A formal square with identity differentials cannot substitute for the
physical equality (1).

## The physical anchor cannot yet be evaluated

There is not yet a completed physical selected cycle: its existence depends
first on (1).  Consequently

\[
 h_{\rm phys}\bigl((A(P_{024}-P_{012}),M_v)\bigr)
\]

is presently **undefined**, rather than known to be zero or nonzero.
The ordinary occurrence marker still reads one on the filtered top, but it
is an auxiliary occurrence covector and must not be identified with the
physical pure/target anchor row.

There is, however, an exact conditional reduction.  The physical `M_v`
packet has

```text
D, W, target, ainc = 0.
```

Therefore, if (1) is proved, its correction contributes zero to the anchor
readout and

\[
 h_{\rm phys}\bigl((A v,M_v)\bigr)=h_{\rm top}(A v).        \tag{2}
\]

The smallest required anchor theorem is the single scalar comparison

\[
                 h_{\rm top}(A(P_{024}-P_{012}))\ne0        \tag{3}
\]

in the exact selected word/fine/repeated physical source grade.  No
basiswise identification of `h_phys` with all fifteen occurrence coordinates
is required.  Conversely, the pinned data allow anchor extensions with the
same zero value on `M_v` and values zero or one on the selected top, so the
occurrence marker alone cannot decide (3).

## Shortest corrected proof interface

```text
filtered top/lower occurrence cycle
        |
        v
twelve-label collapse fixes the candidate M_v
        |
        v
OPEN: expose J_col(ell) and prove J3(M_v)=A J_col(ell)
        |
        v
completed physical selected cycle
        |
        v
compute h_top(A(P024-P012)); M_v contributes zero
        |
        `-- nonzero -> rectangular marked landing
```

The full `U15` comparison remains relevant for uniform reuse and
whole-kernel `q`/Fredholm transport, but not for the single equality (1).

## Scope and verification

This note supersedes the positive chain-map claim in `de74a1a`.  It does not
construct (1), assign an anchor value before the cycle exists, or identify
the occurrence marker with the physical anchor.

Run:

```text
python3 computations/verify_h3_selected_cut_cycle_line_lift_scope.py
python3 -O computations/verify_h3_selected_cut_cycle_line_lift_scope.py
python3 -I -S computations/verify_h3_selected_cut_cycle_line_lift_scope.py
```

Frozen ledger SHA-256:

```text
a40a8a9ffe3f4aadafc82ee7245186a56a32fbb3aa434fde1c34c0a26964ec1a
```
