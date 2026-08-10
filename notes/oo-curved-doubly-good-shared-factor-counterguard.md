# Curvature and goodness do not force the OO two-row shared factor

## Outcome

The two-row certificate in `726deeb` does **not** generalize from curved
doubly-good activity alone.  The exact obstruction is ordinary source
provenance: additional live matchings can contaminate the selected
off-diagonal coefficient without changing either direct-arm rank, any of the
four good-star ranks, curvature, or either cofactor-activity condition.

There are two separate cautions.

1. Merely sharing a Laurent factor does not yield a unit.  If
   (g_{m diag}=P-1) and (g_{m mix}=(P/x)H), localization only gives
   (H=0); the identity from `726deeb` requires (H) to be a nonzero scalar
   (or to have already been reduced to one by other physical source rows).
2. In the first exact two-cell contamination below, even a factor of the form
   (P/x_i) is lost.

Thus the load-bearing hypothesis is a **private matching**, not shared support
or activity by itself.

## Exact guard

Start with the canonical active packet from `726deeb`, with


```text
x = A03(1,1),  y = A15(1,1),  z = A67(1,1).
```

Its pure and selected mixed rows are


\[
g_{\rm diag}=xyz-1,
\qquad
g_{\rm mix}=yz.
\]

Now localize two further physical cells


```text
a = A01(1,1),  b = A45(1,1).
```

The pure word `11111111` still has exactly the old matching


```text
03 | 15 | 24 | 67,
```

so its row remains (xyz-1).  But the selected off-diagonal word
`11001111` now has two live matchings:


```text
04 | 15 | 23 | 67   -> y*z,
01 | 23 | 45 | 67   -> a*b*z.
```

Consequently


\[
g_{\rm mix}=yz+abz=z(y+ab).
\]

For (P=xyz), the possible one-variable quotients are (yz,xz,xy).
The monomial gcd of the two terms of (g_{\rm mix}) is only (z), so none of
those three quotients divides the complete mixed row.  The old calculation
becomes


\[
xg_{\rm mix}-g_{\rm diag}=1+xabz,
\]

not a unit certificate.  This failure is genuine in the localized two-row
ring: the rational torus point


\[
(x,y,z,a,b)=(1,1,1,1,-1)
\]

annihilates both (g_{\rm diag}) and (g_{\rm mix}).

## Why this is the first relevant source contaminant

The checker inspects only the 105 perfect matchings of the single selected
word; it does not enumerate larger support layers.  Relative to the canonical
support, their missing-cell distances are


```text
distance 0:  1 matching
distance 1:  1 matching
distance 2: 15 matchings
distance 3: 38 matchings
distance 4: 50 matchings
```

The unique one-cell alternate uses `A34(0,1)` and changes the mixed row to
(yz(1+t)).  This already shows that a common factor does not imply a unit,
but it retains the old (yz=P/x) factor.  Of the fifteen two-cell alternates,
fourteen lose that factor.  The lexicographically first is exactly
`A01(1,1), A45(1,1)` above.

## The OO hypotheses really remain present

After adding the two contaminating cells, the checker independently recovers


```text
direct-arm ranks:       (1,1)
four deleted-star ranks:(3,3,3,3)
curvature:              -1
both selected cofactors: active
target-2 ruling sites:  3 and 2
```

The cofactor polynomials on both selected arms remain the same `y, yz`
classes as in the minimal packet.  Hence the contamination is invisible to
the rank, curvature, ruling, and activity data proposed for the transport.

## Exact theorem boundary

A correct transport can use the elementary identity


\[
(x/c)g_{\rm off}-g_{\rm diag}=1
\]

only after physical provenance proves


\[
g_{\rm diag}=P-1,
\qquad
g_{\rm off}=cP/x
\]

with (c) a nonzero scalar.  It is enough to establish either of the
following source-faithful alternatives:

- the chosen off-diagonal fibre has a unique support-live perfect matching;
- every alternate matching in that fibre is annihilated by separately pinned
  physical source equations, leaving a scalar Laurent normal form.

Curvature, direct-arm rank, good-star rank, ruling, and nonzero cofactor
activity alone establish neither alternative.  This private-fibre statement
is the exact missing physical provenance for extending `726deeb`.

## Scope guard

This is a counterguard to the proposed **two-row transport**, not a Krenn
counterexample or a coefficient-feasible curved OO packet.  Reconstructing all
`6561` full-output coefficients exposes fifteen nonzero rows, twelve of them
monomials.  For example, word `00000011` gives the localized zero row (z=0),
so the complete displayed support is independently empty.  That independent
unit does not repair the failed claim that curvature/goodness/activity force
the advertised diagonal/off-diagonal shared-factor identity.

All rows used here are literal physical full-output coefficients.  No Ward,
jet, Hasse, cap-codomain, Gröbner, or finite-field generator is introduced.

## Verification

Run


```bash
uv run python computations/verify_oo_curved_doubly_good_shared_factor_counterguard.py
uv run python -O computations/verify_oo_curved_doubly_good_shared_factor_counterguard.py
```

The frozen ledger digest is


```text
3e51409d068f9ac18a95dd14602dacfdfa573ae2073e671ec34c8a20eb093d14
```
