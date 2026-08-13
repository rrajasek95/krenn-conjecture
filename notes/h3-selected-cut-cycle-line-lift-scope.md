# The selected cut cycle needs a physical line lift, not a full `U15` map

## Result

For the fixed determinant-dark profile

\[
                         v=P_{024}-P_{012},
\]

the full fifteen-label comparison previously stated as the Gate-I input is
stronger than the constructive marked-cycle proof needs.  Let

\[
                         \ell=u_{024}-u_{012}
\]

be its complete collision lower chain.  It has twelve nonzero physical
labels and coefficient zero on the three shared repeated-`02` labels.  The
only required comparison for this one cycle is the map on the two-term
cyclic subcomplex

\[
                    C_{\rm sel}=\langle \ell\longmapsto v\rangle . \tag{1}
\]

Commit `595334a` constructs the physical shifted image of exactly the
twelve-supported vector `ell`.  After rational normalization its boundary
is the literal 360-feature aggregate

\[
                         B_0+B_2-B_3-B_5.              \tag{2}
\]

Commit `271df91` constructs the corresponding source chain

\[
                         M_v=-O_\alpha+K               \tag{3}
\]

from old cap cells and the physical endpoint-odd Cartan cell, with exactly
the boundary (2), the required Eq corners, zero protected rows and the
physical eta/sigma ridge.  Therefore

\[
                         \ell\longmapsto M_v           \tag{4}
\]

is an actual map of (1), not merely a pushforward of occurrence
coefficients.  A chain map on a cyclic two-term complex has one boundary
condition, and (2)--(3) prove it.  No value on any shared basis label occurs
in that condition.

Checker:
[`verify_h3_selected_cut_cycle_line_lift_scope.py`](../computations/verify_h3_selected_cut_cycle_line_lift_scope.py).

## Why the old shared-loop obstruction does not apply to (4)

The natural site-collapse identifies collision sites `0,2` at physical site
`4`.  Each of the three shared basis labels therefore contains a forbidden
coefficient loop `44`.  This proves that the same termwise construction does
not extend to a physical map

\[
                         \Phi:U_{15}\longrightarrow L_3.           \tag{5}
\]

It does not obstruct (4).  The selected vector `ell` has coefficient zero
on all three shared labels before the shifted image is taken.  Restricting a
physical construction to the line `k ell` is different from declaring the
three shared basis vectors to have zero image: the latter would indeed fail
the occurrence-level chain square, while the former never includes those
basis vectors in its domain.

Thus the exact distinction is

```text
selected marked cycle:       map only C_sel; twelve-label M_v lift suffices;
full collision comparison:   map all U15; two shared-loop orbit images needed.
```

The previous “shared labels cannot be discarded” warning remains correct
for (5), but it should not be used to delay the selected-cycle theorem.

## Terminal and Fredholm scope

The line lift gives one complete protected cycle `c=(Av,M_v)` in the
physical source complex.  If its physical six-term readout is nonzero,

\[
                              q(c)\ne0,
\]

then `c/q(c)` is immediately the relative generator.  No full `Phi` is
needed for that positive arm.

The converse is false.  The equality `q(c)=0` says nothing about another
class in the protected kernel.  The smallest guard is

\[
 J=(1\;0\;0),\qquad c=(0,1,0).
\]

Both `q=(1,0,0)` and `q'=(0,0,1)` kill `c`; the first kills all of
`ker J` and gives Fredholm factorization, while the second sees the other
kernel vector `(0,0,1)` and gives a generator.  Therefore a Fredholm
conclusion still needs one of:

1. a physical comparison on an exhaustive domain, so the quotient-defect
   theorem can use an arbitrary kernel witness;
2. an independent proof that the selected cyclic packet is the whole
   relevant kernel; or
3. direct application of the six-term exhaustive alternative on an already
   constructed canonical physical relative complex.

This is the exact dependency which can force basiswise `Phi`.  It is a
whole-kernel terminal dependency, not a dependency of the selected chain
equation itself.

The same full-domain structure remains necessary when the intended output
is the rootless pentagon map, its cyclic five-face propagation, or an
inactive normal-grade comparison.  Those constructions must be natural on
a family of source classes and cannot be recovered from one value (4).

## Physical anchor scope

The twelve-label construction has zero physical `ainc` on its lower
correction: the four coefficients in (2) sum to zero, and the old cap plus
Cartan cell has protected `ainc=0`.  Hence any already established physical
anchor value on the top candidate is not changed by (4).

What remains is only the familiar marker distinction.  The ordinary
occurrence covector reads one on the top profile and zero on the lower fine
grade, but it is not automatically the physical pure/target anchor row.  For
the constructive rectangular route it is enough to compute directly

\[
                           h_{\rm phys}(c)\ne0.         \tag{6}

The full fifteen-label comparison would not prove (6) by itself.  Thus
removing the shared-loop repair from the selected cycle does not hide a new
anchor assumption; it leaves the same independent physical readout already
isolated by the marked-lift theorem.

## Shortest proof consequence

The determinant-dark constructive branch now has the shorter interface

```text
P024-P012 filtered top/lower cycle
        |
        v
signed twelve-label shifted collapse (595334a)
        |
        v
literal M_v=-O_alpha+K source chain (271df91)
        |
        v
complete selected protected cycle
        |
        +-- q or h_phys visible -> generator / rectangular landing
        `-- whole-kernel decision needed -> full Phi or exhaustive canonical duality
```

The two shared-loop orbit repairs remain valuable for the stronger uniform
Gate-I/Route-B comparison and for inactive propagation.  They are no longer
a prerequisite for existence of the selected determinant-dark marked cycle.

## Scope and verification

This result concerns the canonical selected cut difference and its physical
symmetries.  It does not construct a comparison on every determinant-dark
profile, prove that the selected cycle exhausts the physical kernel, or
identify the occurrence marker with `h_phys`.

Run:

```text
python3 computations/verify_h3_selected_cut_cycle_line_lift_scope.py
python3 -O computations/verify_h3_selected_cut_cycle_line_lift_scope.py
python3 -I -S computations/verify_h3_selected_cut_cycle_line_lift_scope.py
```

Frozen ledger SHA-256:

```text
7ed4589b3dcee068748f376c2373c42828be02202760a94265e23fd328f408f7
```
