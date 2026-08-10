# The fixed-star response rectangle has an arbitrary-direct counterguard

## Verdict

The four response identities in the fixed first one-bad star do not imply a
determinant or flattening constraint strong enough to decide the six-site top
tensor.  They have an exact nine-cell rational solution whose selected
response rectangle is

\[
 \begin{pmatrix}K_{24}&K_{25}\\K_{34}&K_{35}\end{pmatrix}
 =\begin{pmatrix}E_{00}&0\\0&E_{11}\end{pmatrix}.       \tag{1}
\]

The common direct block is the rank-two off-diagonal matrix

\[
 D=A_{01}=E_{01}+E_{10}.                               \tag{2}
\]

It cancels the cross response at `34`.  Thus the selected `2x2` compound in
(1) has determinant one, but the packet is nevertheless source-feasible.
The direct-zero shared-two-zero-fan unit cannot be extended by simply allowing
an arbitrary direct block.

The exact checker is
`computations/verify_n8_one_bad_fixed_star_flattening_counterguard.py`.

## The rational source

For orbit 0, the nonzero endpoint-coloured cells are

```text
01:01 =  1       01:10 =  1
02:00 =  1       03:11 =  1
04:00 =  1       05:11 =  1
13:11 =  1       14:00 =  1
34:10 = -1.
```

Direct matching expansion gives the complete tensor identities

\[
 H_{0124}=X_0,\qquad H_{0135}=X_1,\qquad
 H_{0125}=H_{0134}=0.                                  \tag{3}
\]

These are full endpoint-colour tensors, not only the four selected scalar
coefficients.  The cancellation in `H0134` is literal:

```text
01:01 * 34:10  cancels  04:00 * 13:11,
01:10 * 34:10  cancels  03:11 * 14:00.
```

Contracting residual sites `2,3,4,5` against colours `0,1,0,1` gives (1).
In the pair-chart decomposition

\[
 K_{rs}=a_{rs}D+u_rv_s^T+u_sv_r^T,                    \tag{4}
\]

the direct-free star residue in `K34` is exactly `D`, while
`a34=-1`.  This identifies the load-bearing cancellation without a Gröbner
or Macaulay computation.

## The response variety has a mixed-top line

The nine-cell source has `H012345=0`.  Add one cell

\[
                         A_{45}(2,2)=t.                 \tag{5}
\]

No response set in (3) contains both sites 4 and 5, so every identity in (3)
is unchanged.  The only complete matching using (5) is its product with
`02:00*13:11`.  Therefore, identically over `Q[t]`,

\[
                         H_{012345}=tX_{010122}.         \tag{6}
\]

This is a genuine nonzero tangent and affine direction of the response
variety.  Swapping residual sites 2 and 4 transports the construction to the
second sharp orbit:

\[
 H_{0145}=H_{0123}=0,\qquad
 A_{25}(2,2)=t,qquad H_{012345}=tX_{012102}.            \tag{7}
\]

The complete exact Jacobian calculation at the nine-cell point gives

```text
four-response Jacobian rank:             105 of 135
response tangent dimension:               30
full top Jacobian rank:                    42
top image of the response tangent:         20
rank after adjoining the pure X2 vector:   21.
```

Hence the desired pure `X2` direction is not in the first-order top image of
the response-preserving tangent, even though the mixed directions in (6)--(7)
are.  This is an exact rational rank statement, not a numerical tangent test.
It transports to orbit 1 by the same site swap.

## Exact consequence

Equations (3) alone neither force the top tensor to vanish nor restrict it to
the desired pure target line.  In particular, the natural plan

```text
two pure responses + two cross zeros
    -> rank-one response flattening or determinant zero
    -> contradiction with the top target
```

is false at its first implication.  The obstruction is not a high-degree
component: it is a nine-cell rational point and a one-parameter affine line.

This does **not** solve all five identities.  Both lines in (6)--(7) point in
mixed top directions and never equal `X2`.  A successful compact identity
must therefore use coefficients of the fifth equation essentially, coupling
the pure top grade to the arbitrary-direct response cancellation.  A
response-only condensation or flattening cannot close the whole packet.  The
tangent exclusion is local and first-order; it does not rule out a different
response component or a higher-order path.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_fixed_star_flattening_counterguard.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_fixed_star_flattening_counterguard.py
```

Both modes freeze the ledger hash printed by the checker.
