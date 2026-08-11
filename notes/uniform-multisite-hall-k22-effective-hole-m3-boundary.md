# Reverse-axis holes are ineffective; the `M3` lock is the sole residual

## Exact result

The two interfaces left in `4c4da49` have different outcomes.

The reverse-axis case is fully discharged.  A diagonal Hall family must be
defined by nonzero **complete unordered-hole contributions**

\[
 \sum_{u<v}(p_u s_v+p_v s_u)C_{uv}=1,                \tag{1}
\]

not by the support of one oriented monomial.  The two orientations of the
same physical hole have the same common hafnian cofactor `C_uv`.  Therefore

\[
              p_us_v+p_vs_u=0                        \tag{2}
\]

makes the whole `uv` contribution ineffective.  It is simply absent from
the effective hole family.  Since the target coefficient in (1) is one,
some other complete hole contribution is nonzero and can be selected.
Nothing in the source is modified, no anchor is deleted, and no iterative
support-decrease argument is needed.

The `M3` branch is reduced but not yet closed.  Its complete crossed row
does close every free bridge and every off-anchor mate, but the proved
inputs still permit one exact interface:

```text
anchor-contained off-axis lock map,
injective on the same-star switch directions,
with no complementary off-anchor crossed wedge.
```

Checker:
`computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py`.

## 1. Effective holes, not oriented monomials

At a pure target word, expansion over ordered endpoint holes is

\[
 \sum_{u\ne v}p_us_vC_{\{u,v\}}.
\]

Grouping the two orientations of each physical hole gives (1) identically.
If a selected orientation has a reverse mate, their scalar bracket is the
coefficient of the **entire** common cofactor tensor.  Cancellation does not
produce a kernel translation; it says that this hole was never an effective
member of the Hall family.

This exactly matches the effectiveness qualification in the strict
`K2,2` source reduction.  A nonzero complete contribution supplies both a
nonzero orientation product and a nonzero cofactor coefficient, hence a
literal selected matching witness.  Reselecting it is source-preserving and
anchor-safe because no coefficient changes.

The checker verifies the ordered-to-unordered regrouping over `Q` and the
sharp sample

```text
(p0*s1+p1*s0)*C01 = (1*1+1*(-1))*7 = 0,
(p2*s3+p3*s2)*C23 = 1,
target total = 1.
```

Thus the earlier request for a well-founded reverse-axis support decrease
was stronger than necessary.

## 2. The exact `M3` complete row

For the normalized `M3` alternative, the selected crossed cofactor is

\[
 H_{03}^{11}=q_{12}^{11}q_{45}^{11}
             +q_{14}^{11}q_{25}^{11}
             +q_{15}^{11}q_{24}^{11}.                \tag{3}
\]

The first product is nonzero.  The complete zero row therefore forces one
of the two bridge products or an endpoint-star cancellation mate.

The already proved implications are exact:

1. Either bridge product leaves the selected anchor web and reaches the
   certified free/active route.
2. An off-anchor off-diagonal endpoint mate reaches the target-augmented
   private-site active-minor route with ranks supplied by selected matching
   columns.
3. A nonzero kernel of the complete unary/`11`/`12`/`21`/`22` lock map is
   an exact same-star switch; entry-minimality then deletes a blocker.
4. Complementary `12` and `21` lock components at distinct off-anchor ports
   give the certified distinct-head four-good active wedge.

What remains after all four exits is the injective, no-complementary-wedge
lock from the five-row theorem, confined to the anchor union.

## 3. Why minimum support does not erase the last lock

Entry-minimality is a descent principle, not an existence theorem for a
descent direction.  It applies after a nonzero simultaneous switch lies in
the kernel of all five complete rows.  On the residual interface the lock
map is injective, so no such source modification has been constructed.

Likewise, aggregate target support alone cannot be used to replace an
endpoint row by a coordinate point: the pinned affine-fibre guard shows why
that inference needs the top and companion provenance.  That guard is not a
full one-bad source, so it does not refute the remaining `M3` implication.

The first missing global datum is now precise:

```text
an opposite crossed companion with the same matching provenance,
or a source identity forcing dependence among the five lock columns.
```

No physical full-row guard satisfying the unary target and all four
responses is asserted here.  Accordingly the residual is open, not known
false.

## Scope

This is uniform complete-hole algebra and a source-theorem dependency audit,
not another matching census.  It closes reverse-axis reselection outright
and prevents minimum-support language from being used to hide the remaining
`M3` lock.

Run

```text
python3 computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py
python3 -O computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py
python3 -I -S computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py
```

Frozen ledger SHA-256:

```text
ca3131bd96d85dd6ee4a1f8508a6f51bfa915a4ff9b55671698fdc10afce8a6e
```
