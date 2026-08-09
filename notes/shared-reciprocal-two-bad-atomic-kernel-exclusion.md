# Atomic two-bad kernel products cannot carry the third pure class

## 1. Result

Continue in the exact five-site quotient of
[`shared-reciprocal-two-bad-cofactor-quotient.md`](shared-reciprocal-two-bad-cofactor-quotient.md).
Write

\[
 K=q^{[2]},\qquad \Phi(w)=wK,
\]

and suppose the two known pure classes are `X_a,X_c in im(Phi)`, while
`U,V in ker(Phi)` are the two third-colour rows.  The following natural
atomic subcase is impossible.

> **Atomic kernel-product lemma.**  Assume:
>
> 1. every internal cell of `q` has the same colour at its two endpoints;
> 2. `U` and `V` are each supported at one site;
> 3. `X_a` and `X_c` each have a one-centre preimage under `Phi`; and
> 4. `T(P,U,V)=PUVq` has a nonzero `X_t` coefficient.
>
> Then the equations are inconsistent over every integral domain.

Consequently any genuine two-bad survivor must use at least one of

\[
 \boxed{\text{a mixed-colour internal cell}},\qquad
 \boxed{\text{a multi-site kernel row}},\qquad
 \boxed{\text{a multi-centre pure lift}}.                 \tag{1}
\]

This closes a structural subcase of the pure kernel-product question.  It
does not exclude the three alternatives in (1), and hence does not yet
close the two-bad branch.

There is one useful strengthening.  A two-centre zero syzygy whose two
factor lines are the target line is also impossible under assumptions 1,
3, and 4.  After normalization it is

\[
 U=e_t^{(0)}-e_t^{(1)},\qquad
 K_0=e_t^{(1)}\otimes Z,\qquad
 K_1=e_t^{(0)}\otimes Z.                                \tag{4}
\]

Thus the minimal signed two-centre bridge does not by itself evade the
argument.  With one-centre bright lifts, a survivor must tilt a bridge
factor away from the target line or use at least three centres.

## 2. Normalization

If `U` and `V` are nonzero one-site kernel rows and `PUVq` has a nonzero
all-`t` coefficient, factor uniqueness lets us normalize five sites as

```text
U at 0, V at 1, a selected t-entry of P at 2, q_34(t,t) != 0.
```

Because `U K=V K=0`, the four-site cofactors `K_0,K_1` vanish.  A
one-centre lift of `X_a` has the form `w_h K_h=X_a`; uniqueness of tensor
factors makes `w_h` an `a`-coordinate vector and `K_h` a nonzero pure
`a` tensor.  The analogous statement holds for `X_c`.  Their centres are
distinct and cannot be `0` or `1`, so their ordered centres are two of
`{2,3,4}`.

Choose a nonzero all-`a` matching monomial in the first pure cofactor and
a nonzero all-`c` matching monomial in the second.  There are

\[
  3\cdot2\cdot3\cdot3=54                              \tag{2}
\]

ordered choices after the normalization.

## 3. The unique mixed coefficient

In a colour-diagonal quadratic, a four-site word containing two occurrences
of one colour and two of another has only one compatible matching: the two
equal-colour sites must be paired to each other.  Therefore, whenever two
mandatory edges of different colours are disjoint inside a constrained
four-site cofactor, their product is a unique mixed monomial.  It cannot
cancel, regardless of any additional colour-diagonal support.

For each of the 54 choices, the checker finds such a pair in one of

\[
 K_0=0,\qquad K_1=0,\qquad K_{h_a}=\text{pure }a,
 \qquad K_{h_c}=\text{pure }c.                            \tag{3}
\]

The deterministic first-witness histogram is

```text
K_0: 30, K_1: 18, K_ha: 6.
```

Every displayed product is nonzero by construction but belongs to a zero
target coefficient in (3), giving the contradiction.  This is a finite
case split in a hand reduction, not a Boolean support search.  The checker
also deletes either kernel equation as a mutation test; four witness
configurations then survive in each case.

For the bridge (4), replace `K_0=K_1=0` by the weaker requirements that
`K_0` have target colour at site 1 and `K_1` have target colour at site 0.
The same 54 configurations are excluded, with first-witness histogram

```text
K_0 wrong factor: 30, K_1 wrong factor: 18, pure-a: 6.
```

This is exactly the two-centre Koszul normal form, not a support
approximation.

## 4. Consequence for the main proof

The theorem identifies where a genuine nonlinear survivor must hide.  The
fully provenance-faithful mixed-class guard in the quotient note uses a
multi-site signed kernel.  The present result explains why that complexity
is necessary in the colour-diagonal chart.  A target-line two-centre bridge
can produce a pure kernel product before the two old pure images are imposed,
but two one-centre bright lifts are incompatible with it by the bridge audit.
To close the complete packet, the next lemma must straighten tilted or
larger kernels and multi-centre bright lifts while preserving all nine rows,
or show directly that their Koszul bridges cannot produce a pure quotient
class.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_atomic_kernel_exclusion.py
python3 -O computations/verify_shared_reciprocal_two_bad_atomic_kernel_exclusion.py
```

The checker uses only the Python standard library and audits both sets of
54 normalized matching-witness configurations.
