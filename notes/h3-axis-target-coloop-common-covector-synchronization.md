# The two one-sided minors synchronize over one output covector

## Result

After `1a2713d`, both endpoint pairs in the target-coloop residual have
nonproportional complete response columns.  Work in the no-external-corner
branch of `6dc3bd5`, and let `d` be the selected mixed-word coefficient.
The two selected tails make the `P` and `S` column-value pairs at `d`
nonzero.  Hence nonproportionality says that

\[
 f_P(e)=\det(P(d),P(e)),\qquad
 f_S(e)=\det(S(d),S(e))                                \tag{1}
\]

are two nonzero linear functionals of an output covector `e`.

Choose separate witnesses `e_P,e_S`.  Over characteristic zero, among

\[
                       e_P+c e_S,\qquad c=0,1,2,       \tag{2}
\]

at most one value lies in `ker(f_P)` and at most one lies in `ker(f_S)`.
Therefore some choice satisfies

\[
                f_P(e_P+c e_S)f_S(e_P+c e_S)\ne0.     \tag{3}
\]

This supplies one common two-output quotient on which both endpoint column
pairs have rank two.

Checker:
[`verify_h3_axis_target_coloop_common_covector_synchronization.py`](../computations/verify_h3_axis_target_coloop_common_covector_synchronization.py).

## Source validity

The complete full-`H8` response rows are tensor equalities.  Contracting a
tensor row with the covector in (2) is exactly the corresponding linear
combination of its fine coefficient rows.  Thus (3) is a source-valid
Fitting carrier: it uses no division, Ward derivative, formal cofactor, or
termwise replacement.  A nonzero contraction also certifies that the
physical cofactor tensor being evaluated is nonzero.

The argument is coordinate-free.  It needs no literal coefficient row that
simultaneously witnesses both minors.

## Sharp fine-word caveat

Such a literal common word need not exist.  The checker freezes the smallest
four-coordinate guard.  In the basis `(d,e_P,e_S,r)`, take

```text
P columns: (1,1,0,0), (1,0,0,0),
S columns: (1,0,1,0), (1,0,0,0).
```

The `P` Pluecker support is only `(d,e_P)`, while the `S` support is only
`(d,e_S)`.  Their literal supports are disjoint.  Nevertheless the covector
`e_P+e_S` gives both minors equal to `-1`.  Therefore a proof which requires
one matching-grade monomial is strictly stronger than the tensor/Fitting
statement and cannot be obtained from column rank alone.

## Downstream scope

The common covector removes the fine-word synchronization issue.  It does
not supply the data absent from the target-coloop packet:

```text
distinct endpoint heads,
rank-three deleted stars on the coloop arm,
or an alternate bright matching avoiding that arm.
```

In particular the strict `K2,2` unit requires localized opposite diagonal
star factors, including a second selected-colour port.  That factor is
exactly an alternate bright matching in the present chart; if it exists,
the coloop has already broken upstream.  The smallest remaining physical
gate is therefore to route the common-covector bistar/Fitting carrier to a
rank-restoring crossed response base, or to derive an anchor-safe same-star
dependence from the full five-row packet.

## Verification

Run

```text
python3 computations/verify_h3_axis_target_coloop_common_covector_synchronization.py
python3 -O computations/verify_h3_axis_target_coloop_common_covector_synchronization.py
python3 -I -S computations/verify_h3_axis_target_coloop_common_covector_synchronization.py
```

Frozen ledger SHA-256:

```text
c8ed7d47ea898868ee08211395946d648e5910daef8912e7007e134f1c445c9f
```
