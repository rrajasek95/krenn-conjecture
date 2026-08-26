# Twisted-4+4 orbit scope audit (UNAUDITED)

## Verdict

The orbit claim needed by the fixed W33-D5 obstruction is true, with the
following precise scope.

Let a binary exact source on `K_8` have diagonal support equal to two perfect
matchings whose union is two disjoint four-cycles.  Require all eight diagonal
cells to be nonzero and require exactly four nonzero endpoint-ordered
cross-colour cells.  Over **every field**, every such source is related to the
fixed W33-D5 representative by a site permutation, the binary palette swap,
and a target-preserving diagonal site-colour gauge.

This conclusion does not use the equality of a stratum dimension and an orbit
dimension.  It follows from a complete characteristic-free support census and
an explicit, root-free construction of the gauge.

Status: **UNAUDITED EXACT AUDIT**.  No certified/spine file was edited.

## 1. What W33 actually defined and established

The definition is in
`computations/unaudited-x4general-w33-2026-08-20/REPORT.md` and the support
sweep is in `run_10_44sweep.py`.  W33-D5 calls the following object
“twisted 4+4”:

1. the two diagonal matchings have union `C4 disjoint-union C4` rather than a
   Hamiltonian eight-cycle;
2. exactly four cross-colour cells are nonzero; and
3. the binary source is exact.

W33 enumerated the cross supports modulo the stabilizer of a standard
diagonal pair.  It reported 6,123 support orbits and exactly one non-unit
support orbit.  Its summarizer then recorded

```text
stratum_dim_saturated = 8
gauge_orbit_dim = 8
note = "single gauge orbit"
```

but these three items are literal constants in `summarise.py`; no W33 stratum
producer establishes transitivity.  Even if both dimensions had been
independently computed, their equality alone would not rule out extra
components, finite-index torus images, or distinct orbits of the same
dimension.  That was the genuine residual behind the fixed-representative
certificate.

The present checker imports no W33 code or stored data.  It reconstructs the
105 perfect matchings twice, the binary coefficient equations, all support
subsets, and the symmetry action from the endpoint-ordered cell definition.

## 2. Standard diagonal support and fixed representative

The standard diagonal matchings are

```text
M0 = {01, 23, 45, 67}
M1 = {03, 12, 47, 56}.
```

Their union consists of the cycles on `{0,1,2,3}` and `{4,5,6,7}`.  A direct
enumeration of all ordered pairs among the 105 perfect matchings finds 1,260
ordered pairs of this `4+4` type.  They are exactly the site-permutation and
palette-swap orbit of `(M0,M1)`.  Thus fixing this standard pair loses no
generality.

The surviving standard cross support is

```text
A04[0,1], A05[1,0], A17[0,1], A34[1,0].
```

The fixed representative has all eight diagonal weights equal to `1`, the
first two displayed cross weights equal to `1`, and the last two equal to
`-1`.  Direct expansion of all 256 binary words verifies exactness.  A sign
flip of `A17[0,1]` fires the expected word `00001111`, providing a must-fire
control.

## 3. Complete support classification without Groebner bases

There are 56 possible endpoint-ordered cross cells: two orientations on each
of 28 edges.  For a proposed support `X`, expand every mixed binary word over
the 105 perfect matchings.  If some word has exactly one supported matching
term, its equation is a single monomial with coefficient `1`.  Because every
cell in the declared support is nonzero, that equation cannot vanish over any
field.

The complete raw census is:

| number of cross cells | raw supports | supports with no singleton word |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 56 | 0 |
| 2 | 1,540 | 0 |
| 3 | 27,720 | 0 |
| 4 | 367,290 | 32 |

The checker independently builds the 64-element stabilizer of the standard
diagonal pair, acting correctly on endpoint order.  The orbit counts for
support sizes `0,1,2,3,4` are respectively

```text
1, 3, 44, 502, 6123.
```

This reproduces W33’s `550` orbits at size at most three and `6,123` orbits at
size four.  More importantly, the orbit of the displayed fixed support has
size 32 and is **exactly** the set of all 32 supports with no singleton word.
Every other four-cell support is therefore killed by an explicit raw
coefficient equation over every field.  No Gröbner interpretation or
characteristic transfer is needed.

The 32 survivors automatically consist of cells crossing between the two
four-cycle vertex components, so this census also justifies W33’s word
“crossing”; it was not assumed in the enumeration.

## 4. The entire surviving coefficient stratum

Name the twelve nonzero cells, in order, by

```text
a=A01[0,0]  b=A23[0,0]  c=A45[0,0]  d=A67[0,0]
e=A03[1,1]  f=A12[1,1]  g=A47[1,1]  h=A56[1,1]
i=A04[0,1]  j=A05[1,0]  k=A17[0,1]  l=A34[1,0].
```

Raw matching expansion finds exactly four nonzero binary coefficient
equations:

```text
00000000 : a*b*c*d - 1
11111111 : e*f*g*h - 1
00001111 : a*b*g*h + b*h*i*k
11110000 : c*d*e*f + d*f*j*l.
```

On the support torus all variables are nonzero, so these are equivalent to

```text
a*b*c*d = 1,
e*f*g*h = 1,
a*g + i*k = 0,
c*e + j*l = 0.
```

Consequently every point is uniquely parameterized by arbitrary nonzero
`a,b,c,e,f,g,i,j`, followed by

```text
d = 1/(a*b*c),
h = 1/(e*f*g),
k = -a*g/i,
l = -c*e/j.
```

Thus the stratum is indeed an irreducible eight-dimensional torus over any
field.  This is a useful corollary, but it is not the orbit proof.

## 5. Constructive gauge transitivity

For site-colour scalars `lambda_(v,c)`, the diagonal gauge acts by

```text
(gA)_uv[a,b] = lambda_(u,a) * lambda_(v,b) * A_uv[a,b].
```

Given an arbitrary exact point on the fixed support, label each support cell
by the ratio of that cell to the fixed representative.  Form the graph whose
16 vertices are `(site,colour)` and whose 12 edges are the support cells.  Its
connected components have sizes

```text
4, 4, 2, 2, 2, 2,
```

and every component is bipartite.  Set one `lambda` to `1` in each component
and propagate across an edge labelled `rho` by

```text
lambda_neighbor = rho / lambda_current.
```

No roots or algebraic closure are used.  The two four-cycle consistency
conditions are precisely `a*g=i*k` and `c*e=j*l` for ratios (the minus signs
are already in the fixed representative).  The four two-vertex components
have no consistency condition.  Hence the propagation always constructs a
gauge over the original field.

Finally,

```text
product_v lambda_(v,0) = (a*b*c*d)_ratio = 1,
product_v lambda_(v,1) = (e*f*g*h)_ratio = 1.
```

So the constructed gauge preserves the two pure binary targets.  Taking all
colour-2 gauge factors to be `1` extends it to a target-preserving ternary
gauge.  This proves transitivity constructively and excludes the finite-index
and extra-component failure modes that a dimension comparison would miss.

## 6. Exact scope and consequence

This audit proves the orbit statement for exactly the W33-D5 combinatorial
stratum: diagonal `4+4`, eight live diagonal cells, and exactly four live
binary cross cells.  It does **not** classify supports with five or more cross
cells, binary exact sources outside the PM-pair diagonal stratum, or general
ternary sources.

Combined with the separately checked 21-equation obstruction for the fixed
representative, the conclusion transports to every twisted-4+4 object in this
scope over every field.  In other words, the former orbit-scope caveat in the
fixed-representative report can be discharged; this audit does not itself
recheck that 21-equation certificate.

## 7. Reproduction and controls

From the repository root, all three modes pass with identical digest:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  computations/unaudited-codex-twisted44-orbit-scope-2026-08-20/audit_orbit_scope.py

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  computations/unaudited-codex-twisted44-orbit-scope-2026-08-20/audit_orbit_scope.py

PYTHONDONTWRITEBYTECODE=1 python3 -I -S \
  computations/unaudited-codex-twisted44-orbit-scope-2026-08-20/audit_orbit_scope.py
```

The declared-versus-executed manifest contains ten controls: two independent
perfect-matching engines, diagonal-pair transitivity, fixed-point exactness, a
sign mutation, an outside-support singleton, complete raw and symmetry
censuses, equality of the survivor set and fixed orbit, raw-equation rebuild,
and constructive gauges on nontrivial rational points.

Digest of `results.json` before insertion of its digest field:

```text
c986af3530781a50a0274847c2f1b8fd1b2ad533c842daf1b86e5a822c04bd2a
```

