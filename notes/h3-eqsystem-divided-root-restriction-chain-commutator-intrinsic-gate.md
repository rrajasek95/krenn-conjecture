# The intrinsic divided-root/restriction commutator is zero

## Result

There is a canonical statement on the original `h=3` EqSystem, independent
of the later protected `B/Eq` duplication.  Let

```text
r = 11110000,       c = 01211222,
changed sites = {0,2,4,5,6,7}.
```

For `q=23` and `q=45`, write `D_r` and `D_c` for differentiation
by the response- and cap-coloured edge variable, `I_c` for cap-coloured
reinsertion, and `Phi` for the product of the divided root operators at the
six changed sites.  After deletion, `Phi_hat` uses divided-root order equal
to the remaining occurrence multiplicity at each site.  On the canonical
first Spencer/Tate stage,

\[
 O_Bd=I_cD_c\Phi d,
 \qquad
 dO_E=dI_c\Phi_{\widehat q}D_r.
\]

The exact source identity is

\[
                 I_cD_c\Phi d=dI_c\Phi_{\widehat q}D_r.       \tag{1}
\]

The checker verifies (1) on all `6,561` official equation rows and all `105`
matching occurrences in each row: `1,377,810` cut-labelled occurrence
squares.  The only nonzero ordinary occurrences are `45` for `q23` and `135`
for `q45`, each with coefficient one.  Both sides kill the scalar term in all
three pure GHZ target equations.  Thus this is an identity of the actual
252-variable EqSystem presentation, not a calculation in formal `B/Eq`
copies.

The executable certificate is
[`verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py`](../computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py).

## Marked collision descendants

At a marked missing/doubled-site collision, deleting one edge need not remove
all occurrences of its endpoints.  This is why `Phi_hat` must be defined by
the **remaining occurrence multiplicity**, rather than by blindly omitting
the two endpoint names.  For example, after deleting `23`, a second edge
incident to site 2 still requires its site-2 root.

With that rule, (1) also holds on the `90` marked `q23` descendants and the
`72` marked `q45` descendants of the `540` operation-labelled collision
branches.  The pinned stronger census checks all `540` parent/trigger squares
and all `1,080` first `P3+K2` deletions.  Parent, missing-site, doubled-site,
word, fine and repeated-site labels are retained.  This is the same
source-derived operation family that constructs the two independent marked
P2 faces.

## What is intrinsic, and what is not

Equation (1) gives a stabilization-invariant scalar on its commutator, but
that scalar is identically zero.  It does **not** construct the protected
quantity `B-Eq`.

The reason is structural.  The original occurrence-labelled EqSystem has one
copy of each coefficient occurrence.  The later PAComp target has two copies,
called `B` and `Eq`.  Forgetting the copy gives

\[
 \pi(B,Eq)=B+Eq,
 \qquad
 \pi^*(\lambda)=(\lambda,\lambda).
\]

The protected detector is anti-diagonal.  Consequently it is not the pullback
of a covector on the original occurrence module.  The exact intrinsic path
difference is zero, while the requested protected landing remains

```text
actual cap composite       (delta_plus,delta_plus)
requested balanced landing (delta_plus,0)
anti-diagonal detector      0 versus 3.
```

Thus the `7/8` protected rank, the `B/Eq` anti-diagonal covector, and any
operation-copy cokernel are presentation data until a physical factorization
from the original operators is proved.  They are not by themselves a
Fredholm observable on actual EqSystem solutions.

## Weakest theorem that closes the balanced branch

A full comparison or quasi-isomorphism of the response and cap resolutions is
unnecessary.  It is enough to prove this one physical identification:

> On the selected normalized endpoint-even PAComp carrier, the protected
> `B` augmentation factors through `I_c D_c Phi d` and the protected `Eq`
> augmentation factors through `d I_c Phi_hat D_r`, with the same
> normalization, including the hidden lower/private `-E` and word-resolved
> ordinary-residue `+E` faces.

If this factorization holds, (1) forces `B=Eq` on every actual normalized
solution.  The balanced right-hand side is `B`-only and the integral detector
reads `3`, so it cannot be a physical boundary.  That gives the desired
contradiction without adjoining an absolute formal `Eq` generator.

This factorization is not proved here.  The current theorem instead makes it
the unique falsifiable interface: evaluate the two displayed composites on
the literal selected PAComp carrier, including the two hidden faces.  One
unequal source-labelled face refutes the proposed factorization; equality on
all protected faces closes the balanced branch.

## Scope

This is an exact `h=3` theorem on the official EqSystem plus its canonical
first Spencer/Tate stabilization.  It covers every equation, every matching
monomial, pure targets, both physical cuts and all marked collision
descendants cited above.  It does not prove the remaining PAComp
factorization, essential surjectivity of a declared operation grammar, or the
full Krenn conjecture.

## Verification

```text
python3 computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py --mode structural
python3 -O computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py --mode full
python3 -I -S computations/verify_h3_eqsystem_divided_root_restriction_chain_commutator_intrinsic_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
2bfbee2d7446a857f4c51cc44930cf48fe809ecea15fa59b9a6fc8ae5ca3a635
```
