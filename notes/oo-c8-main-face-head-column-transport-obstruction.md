# Main clean-face head-column transport obstruction

The clean-face colour gate leaves a dominant sector of 47 profiles with
exclusive colours

\[
                         (q,r)=(0,2).                    \tag{1}


The `pr` leader is already in its selected head column `q=0`, while the
`pq` leader must be transported at the opposite endpoint from `r=2` to
the selected `r=1` column before the fixed-label Bianchi row can see both.

## Exact shifted-Hessian test

Keep the same clean common-word face and change only the exclusive colour
of the `pq` cofactor from `r=2` to `r=1`.  In every one of the 47 profiles,

\[
 \nabla^2 Q_{pq}^{,r=2}\ne0,
 qquad
 \boxed{\nabla^2 Q_{pq}^{,r=1}=0}.                       \tag{2}


Thus there is no Laurent support overlap after the one-column colour
change.  A fixed-colour Bianchi coefficient cannot silently replace the
active leader by a nonzero `r=1` leader.

## What the good-star Cramer minor actually does

At endpoint `r=4`, rows 1 and 2 of the deleted star have the constant
pivot columns

\[
             (24)_{11},\qquad(34)_{22},                  \tag{3}


with `2x2` determinant one and zero cross entries.  On the first canonical
main face, the `pr` endpoint-response Hessians, decomposed by the physical
partner of `r`, are exactly

\[
 R_1=0,qquad
 R_2=m\,[(34)_{22}],                                     \tag{4}


where `m` is the active `pq` leader monomial.  No other neighbor grade
survives.  Hence the Cramer minor separates two independent star channels;
it does not provide an equality transporting `m` from row 2 to row 1.

At the present sparse layer, the literal off-diagonal full-nine equation
`p_1 r_2 q^[2]=0` kills `m` directly—this is the private Hall unit already
certified.  In a denser hypothetical support, additional terms can mate
that row.  Good-star injectivity alone gives no relation forcing those
mates into the diagonal row `p_1 r_1 q^[2]`.

## Verdict

The one-column Cramer repair is unavailable on all 47 main profiles.  The
exact missing provenance datum is an **off-diagonal head-column transport
identity**, not merely a nonzero deleted-star minor.  Any successful use of
the power-free curvature row must retain the entire `r=2` off-diagonal
fibre (including its future mates) and couple it to the `r=1` diagonal
fibre before taking the common-word Hessian.

These 47 profiles are support relaxations, not exact Krenn sources, so the
result is a counterguard to the proposed shortcut rather than a global
counterexample.

## Reproduction

```text
python computations/verify_oo_c8_main_face_cramer_transport.py
python -O computations/verify_oo_c8_main_face_cramer_transport.py
```

The checker audits all shifted cofactor Hessians exactly and gives a
matching-by-matching Cramer-column decomposition for the first canonical
profile.
