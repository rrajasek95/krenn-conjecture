# The unary top cannot be added to the Segre--K4 guard by pure cells

## Exact theorem

Let (H) be the fourteen-cell common quadratic of
[`n8-one-bad-segre-cube-k4-closure-counterguard.md`](n8-one-bad-segre-cube-k4-closure-counterguard.md).
It realizes the dense repeated-carrier mate cube and satisfies

\[
                              H^{[3]}=0.                \tag{1}
\]

Every cell of (H) has exactly one endpoint of colour (1) or (2) and
one endpoint of colour (0).  Let

\[
                 d=\sum_{0\le i<j\le5}d_{ij}x_i^0x_j^0 \tag{2}

be an **arbitrary** pure-zero quadratic on all fifteen physical edges.  Then

\[
                         (H+d)^{[3]}\ne X_0             \tag{3}

for every complex specialization of the (d_{ij}).

This closes the top-null counterguard against all pure-cell unary repairs at
once; it is not a bounded support search.

## Defect grading

Because every (H)-cell carries exactly one nonzero-colour endpoint, the
number of nonzero-coloured sites separates the binomial expansion:

\[
 (H+d)^{[3]}
   =d^{[3]}+d^{[2]}H+dH^{[2]}+H^{[3]},                  \tag{4}

where the four terms have respectively (0,1,2,3) nonzero-colour sites.
The exact coefficient ledger has

```text
defect 0:  1 row
defect 1:  6 nonzero rows
defect 2:  8 nonzero rows
defect 3:  0 rows       (H^[3]=0)
```

Thus no cancellation between the four summands of (4) is being assumed.

## Six-row ordinary certificate

Order the scalar variables lexicographically by physical edge,

```text
d0=01, d1=02, d2=03, d3=04, d4=05,
d5=12, d6=13, d7=14, d8=15,
d9=23, d10=24, d11=25, d12=34, d13=35, d14=45.
```

Write (g_w=[(H+d)^{[3]}]_w) for a mixed word.  Literal expansion gives
the integral identity

\[
\boxed{
\begin{aligned}
 [d^{[3]}]_{000000}
 ={}&d_{14}g_{000020}+d_{13}g_{000100}-d_{11}g_{002000}\\
 &+(d_4d_7+d_3d_8)g_{100020}\\
 &+(d_4d_6+d_2d_8)g_{100100}\\
 &-(d_4d_5+d_1d_8)g_{102000}.
\end{aligned}}                                             \tag{5}
\]

All six right-hand rows are mixed, so exact monochromaticity sets them to
zero.  Equation (5) forces the pure-zero hafnian to be zero, contradicting
the unary requirement ([d^{[3]}]_{000000}=1).  This proves (3) over every
characteristic-zero field and retains all complex cancellations.

The standard-library checker
[`verify_n8_one_bad_segre_cube_unary_extension_unit.py`](../computations/verify_n8_one_bad_segre_cube_unary_extension_unit.py)
reconstructs all matchings and verifies (5) as an exact sparse-polynomial
identity.

## Scope and next gate

The theorem consumes the actual unary row, rather than merely observing
that the preceding guard has (H^{[3]}=0).  It allows every pure-zero cell
and arbitrary coefficients on them.  It does not allow new mixed-colour
cells or deformation of the fourteen fixed (H)-cells.  Therefore the
remaining one-bad escape must change the mixed carrier at the same time as
it restores the unary top.  The next useful theorem is a leading-form or
anchor-preserving normalization showing that an arbitrary common-(q)
packet degenerates to the fixed (H+d) form, or else that the first mixed
deformation supplies the clean cap/curved-overlap descent.
