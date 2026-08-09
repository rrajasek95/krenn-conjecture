# N=8 D1: the injective two-kernel tripod obstruction

There is a support-independent obstruction behind the rank-two residue
branches.  It classifies the generic two-syzygy case at one residue vertex
and replaces a large Boolean support family by a short piece of multilinear
algebra.

Let `X,Y,Z` be the colour spaces at three vertices opposite a fixed residue
vertex, and let

```text
D in X tensor Y,   E in X tensor Z,   F in Y tensor Z.
```

The two non-target slices at the fixed vertex lie in the kernel of

```text
Phi(x,y,z) = x tensor F + y tensor E + z tensor D.       (1)
```

The lemma treats the case in which they span a two-plane `K` and all three
maps `K -> X,Y,Z` are injective.

## The alternating normal form

Choose one basis of `K` and independently extend its three images to bases
of `X,Y,Z`.  The two relations in (1) then read

```text
e_s tensor F + e_s tensor E + e_s tensor D = 0,
s=0,1,                                                   (2)
```

with the tensor factors placed in their endpoint order.  The `54` scalar
coordinates of (2), as equations in the `27` entries of `D,E,F`, have rank
`26`.  More strongly, integer elimination finds a unit pivot at every one
of those `26` steps.  Hence the statement is field-independent.  The
one-dimensional kernel is

```text
D = [[0,-1,0],[1,0,0],[0,0,0]],
E = [[0, 1,0],[-1,0,0],[0,0,0]],
F = [[0,-1,0],[1,0,0],[0,0,0]]                         (3)
```

up to one common scalar.  Thus the three opposite edges are the same
alternating form on the three projected two-planes, with the required
signs.  This is the first Koszul differential, not an accidental support
pattern.

## No pure companion slice

Suppose an additional triple `(a,b,c)` made `Phi(a,b,c)` a nonzero pure
tensor `p tensor q tensor r`.  Projecting the equality to `X/im(K)` gives

```text
bar(a) F = bar(p) q tensor r.
```

The left side has matrix rank two whenever `bar(a)` is nonzero, whereas the
right side has rank at most one.  Therefore both `a` and `p` lie in the
projected two-plane.  The same argument at `Y` and `Z` puts all six vectors
in their respective two-planes.

Using (3), the resulting `2*2*2` cube is

```text
T000 = T111 = 0,
T001 = -a0+b0,       T010 =  a0-c0,       T100 = -b0+c0,
T011 =  b1-c1,       T101 = -a1+c1,       T110 =  a1-b1.
```

Consequently the weight-one entries sum to zero, as do the weight-two
entries.  A nonzero pure cube with `T000=T111=0` is supported on one
complementary cube edge: one tensor factor loses its zero-coordinate and a
different factor loses its one-coordinate.  That edge has exactly one
weight-one and one weight-two entry, so the two layer sums kill both.  This
is a contradiction.

Thus a residue component whose two non-target slices give two injective
tripod syzygies cannot supply the pure target slice.  The remaining tripod
strata are precisely projection-degenerate: a projected line gives a common
factor/Koszul component (such as escape `85`), while a zero projection gives
a two-term rank-one component.  This identifies a finite, structural next
classification rather than another support-cardinality layer.

The exact checker
[`verify_n8_d1_tripod_two_kernel_obstruction.py`](../computations/verify_n8_d1_tripod_two_kernel_obstruction.py)
audits the field-independent `26/27` relation rank, the alternating kernel,
the companion cube, and all six pure-cube support cases.  Its frozen ledger
SHA-256 is
`56685443cf11a8657f2674b4b3af8cd91644ab8609ea33734173ce65c9683dd9`.
