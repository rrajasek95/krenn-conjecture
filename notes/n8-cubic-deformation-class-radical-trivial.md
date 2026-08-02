# The cubic local deformation is genuine but invisible on all reduced branches

## Exact deformation calculation

Let (I_2\subset\mathbb Q[z_0,\ldots,z_{55}]) be the 39-quadratic
second-lift obstruction ideal and write the normal-eliminated literal lifts
as

\[
 Q_i=q_i+q_i^{(3)}+q_i^{(4)}+\cdots .
\]

The 344-pair first-tail audit proves that
\(q^{(3)}=(q_i^{(3)})\) satisfies every first Schreyer compatibility
equation.  It is therefore an embedded first-order deformation cocycle of
the tangent ideal.

Coordinate changes and changes of ideal generators give the trivial
submodule

\[
 \operatorname{Jac}(q)\,S^{56}+I_2S^{39}\subset S^{39}.
\tag{1}
\]

Exact rational module reduction of all 535 terms of (q^{(3)}) modulo
(1) leaves

\[
 \boxed{\tau=
 a\bigl(z_4(s-r)e_{16}+z_5(s-r)e_{22}-z_4t e_{19}\bigr)\ne0,}
\tag{2}
\]

where (a=z_{3712}) and
\((r,s,t)=(z_{0420},z_{0421},z_{0422})).  In the sparse quadratic list,
the three displayed components have leading forms

\[
 q_3(d+b),\qquad q_3c,\qquad q_4(d+b),
\]

respectively.  The exact module has 1,890 input generators and a
1,704-element standard basis; the normal form (2) has five terms.

Thus the tempting formal-rigidity shortcut is false: the lifted mixed ideal
is not obtained from its tangent ideal merely by a tangent-to-identity
coordinate change and an invertible generator change.  The complete
first-tail cancellation means “cocycle,” not “coboundary.”

## Why the five branches are still the faster route

Every coefficient in (2) lies in

\[
 (ar,as,at)\subset\sqrt{I_2}.
\tag{3}
\]

The exact checker separately reduces all three coefficients to zero on each
of the five linear minimal primes of the Ferrers radical.  Consequently the
nontrivial deformation class is supported entirely on the nilpotent and
branch-intersection structure.  It is invisible on the reduced tangent
support.

This sharply separates the two local proof targets:

* full ideal membership must control the genuine nonreduced deformation
  (2), so a 48-generator all-orders standard-basis argument really does
  require a unit-loop or an equivalent higher obstruction calculation;
* exclusion of geometric local counterexamples only needs radical
  membership.  For that purpose the natural faster attack is to lift and
  analyze the five reduced linear branches separately, then prove that on
  every lifted branch at least one of (H_0,H_1) vanishes.

Equation (3) does not by itself prove that all five branches lift, nor that
there are no additional reduced branches at higher order.  The next exact
branchwise lemma must combine the implicit normal recursion with each
linear prime and certify the restricted pure coefficient (or their product)
to all orders.

## Reproduction

```sh
python3 computations/verify_n8_cubic_deformation_t1_radical_trivial.py
```

The calculation is over (mathbb Q), uses the frozen 48-element tangent
standard basis, and is guarded below 700 MiB RSS.
