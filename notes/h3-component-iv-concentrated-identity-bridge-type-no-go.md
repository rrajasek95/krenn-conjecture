# The concentrated unit identity cannot supply the physical Component-IV bridge

Research boundary only.  This closes one proposed construction route; it
does not prove that the larger relative source resolution lacks the missing
row, define the physical \(d_2\), or prove Krenn's conjecture.

## Outcome

Polarizing or differentiating the universal concentrated source identity
does not promote the all-order cyclotomic chart-comparison class to the
physical cap coordinate \(Yw\).  The obstruction is a discrete source type,
not another coefficient-rank failure.

The concentrated identity has the form

\[
 F_{01}(1111)F_{23}(2222)H(000000)=\sum_j c_jm_jg_j.    \tag{1}
\]

It is an ordinary scalar coefficient-ring identity.  Its target fine degree
has site multiplicities

\[
                         (2,2,2,2,3,3),                \tag{2}
\]

fourteen endpoint tokens and hence internal \(q\)-edge degree seven.  The
complete identity contains 143 literal top/cofactor rows and 5,230
fine-compatible polynomial columns.

The desired Component-IV initial has \(h_v\), of \(q\)-edge degree two, but
it is additionally:

1. denominator-relative;
2. cap-degree one; and
3. chart-odd.

In the feature order

\[
 (\deg_q,\deg_{\rm cap},\deg_{\rm denominator},
   \mathrm{chart\ parity}),                            \tag{3}
\]

the desired type is \((2,1,1,1)\).

## Why polarization cannot change the type

An ordinary \(q\)-cell Hasse polarization of (1) lowers only \(\deg_q\).
After \(k\) polarizations its type is

\[
                         (7-k,0,0,0).                  \tag{4}
\]

The scalar degree first matches \(\deg_q=2\) at order five, but both the
cap and denominator-relative degrees remain zero.

Duplicating (1) in the two chart presentations and taking their difference
can change the last entry of (4), giving

\[
                         (7-k,0,0,1).                  \tag{5}
\]

That difference is a chart-comparison kernel.  It still has no physical cap
cell and no denominator-relative mark.  Thus even the order-five class of
(5) is not the required \((2,1,1,1)\).

This distinction is stable under polynomial multiplication and scalar
localization.  It also survives an all-colour extension of the concentrated
identity as long as the added columns remain ordinary top/cofactor
coefficient rows.  Additional internal colours can change the number of
columns and the scalar membership identity, but not the two missing module
degrees.  If an extension introduces a denominator-relative cap row, it has
introduced precisely the new datum sought here rather than deriving it by
polarization of (1).

There is a second scope mismatch: (1) is proved after concentration of the
four response spokes.  Its scalar target and ordinary-residue maps are not
the physical relative readouts of the two-chart Component-IV packet.
Consequently those readouts cannot be assigned to its chart difference by
analogy.

## Primitive physical separator

The all-order normal calculation already supplies an exact completed
chart-odd comparison boundary with zero literal target and old residue.
The remaining proposed identification would send that class to

\[
                         K=(0,1,0,0)
\]

in physical coordinates \((E,W,T,O)\).  The committed primitive separator

\[
                         \lambda=E+W+T-O               \tag{6}
\]

annihilates every currently typed physical column but has
\(\lambda(K)=1\).  The physical rank rises from three to four with determinant
\(\pm1\).  Hence the failure is primitive and integral; it cannot be repaired
by choosing different rational coefficients in (1).

## Minimal extra source row

The minimal new source type remains the five labelled rows

\[
 d\widetilde\tau_v
   =h_vY_0+\delta(\eta_v)
      +(\text{higher/full-nine rows}),                 \tag{7}
\]

with zero physical target and ordinary residue.  Their face words are

\[
 2112,\quad1112,\quad1212,\quad1212,\quad1211,          \tag{8}
\]

where the two `1212` occurrences belong to distinct labelled deletion
faces.  One equivariant generator may package these components, but its
associated graded must contain all five.  The exact cyclotomic Rees chain
now supplies the chart-comparison side of (7); a source-provenant
denominator/cap comparison map is still required for its physical side.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_concentrated_identity_bridge_type_no_go.py
.venv/bin/python -O computations/verify_h3_component_iv_concentrated_identity_bridge_type_no_go.py
```

The checker reconstructs all 143 source rows and 5,230 fine-degree columns
of the concentrated identity, verifies the complete polarization-type
ladder, and rechecks the primitive physical separator and minimal five-face
relative type.
