# The target full family does not kill the quartic cap tail

## Exact counterguard

The cap reduction in
`shared-reciprocal-two-bad-common-radical-cap-tail.md` leaves

\[
                 H_0=2P Q_t^{[2]}R_t^{[2]}.
\]

It is tempting to kill this tensor from the two kernel equations and the
localized target family alone.  That statement is false over `Q`.

On five sites, with colours `a,c,t`, take the eight nonzero cells

```text
12:tt=1, 12:ta=-2, 34:tt=1, 34:aa=-2,
13:ta=1, 24:aa=2, 14:ta=-2, 23:aa=-2.
```

Put

\[
 h=e_t@1+e_a@2+e_a@3+e_a@4,
 \qquad P=e_t@0,
 \qquad Q_t=R_t=h,
 \qquad D_{22}=1.
\]

Equivalently, if `r=h*h`, this q is `g-r` for

\[
 g=(12:tt)+(34:tt)+3(13:ta)+4(24:aa),
\]

and the two perfect-matching channels of `g^[2]` are exactly `t^4` and
`12 h^[4]`.  This explains the cancellation in (1); the checker still
verifies it directly from the eight cells.

The exact replay verifies all 243 coefficients of

\[
       \Phi_q(h)=0,
 \qquad Pq^{[2]}+Ph^2q=X_t,
 \qquad R=(Pq^{[2]})(t^5)=1.                         \tag{1}
\]

Thus the complete target full tensor and its localized chord hold.  However,

\[
 H_0=P(h^2)^{[2]}
   =12,e_t@0\,e_t@1\,e_a@2\,e_a@3\,e_a@4\ne0.      \tag{2}
\]

All q-cells avoid site 0, so only the hole-0 cofactor is nonzero.  It is

\[
 K_0=t^4-2t^2a^2-2ta t^2+10ta^3,
\]

with the literal site ordering frozen by the checker.  Hence
`rank(Phi)=3`; every image tensor with colour `t` at site 0 is a scalar
multiple of `e_t@0*K0`.  Since `K0` has nonzero `t^4` coefficient while
the nonzero tensor (2) has zero all-target coefficient, `H0` is not in
`im(Phi)`.

## Consequence and scope

This counterguard does **not** satisfy the old bright equations
`Phi(Q_c)=X_c`, `Phi(R_a)=X_a`, nor the other eight full families.  It proves
exactly that those rows are load-bearing: neither `H0=0` nor
`H0 in im(Phi)` follows from the kernel rows, `D22 R=1`, and `F22=X_t`.

The remaining theorem-level question is therefore narrower: do the two
bright source rows together with the 1,936 off-target source determinants
force the tail to vanish or enter `im(Phi)`?  This artifact gives no answer
to that full common-provenance question.

## Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_cap_tail_target_family_counterguard.py
python3 -O computations/verify_shared_reciprocal_two_bad_cap_tail_target_family_counterguard.py
```

Both modes must print ledger digest
`bf798e2c7ce2b0addd0aef0e9eb12cfc4cf6c351ac9bb80c5bf37d699da53094`.
