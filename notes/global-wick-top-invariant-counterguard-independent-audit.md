# Independent audit: global Wick top-invariant counterguard

Audit target: commit `f88b514`.  The Laurent construction, its propagation to
every even arity at least six, the covariance determinant, the tensor-space
closure consequence, and the Bell-chain local image are correct in their
stated algebraic setting.  The independent checker does not import the
primary checker and reconstructs the graph and local projection from scratch.

Three scope qualifications should be kept explicit:

1. “Wick system” here means the polynomial Wick functional of an arbitrary
   complex symmetric covariance.  It does not mean a real positive
   semidefinite probabilistic covariance.  Indeed, zero same-site blocks and
   nonzero cross blocks are incompatible with positive semidefiniteness.
2. The source family is defined for `t != 0`; its entries include `t^-1`.
   The determinant is exactly `(-1)^(3n/2)` on that punctured parameter line,
   while only the **output tensor** extends to `t=0`.
3. The internal Bell-chain map acts on four virtual modes.  Its three accepted
   basis patterns have Hamming weights `0,2,2`, not one.  Thus “accepts four
   virtual half-edges” must be read as “has four virtual half-edge inputs,”
   not as a claim that all four are occupied.

These qualifications do not weaken the counterguard against identities of
the algebraic top tensor.

## 1. Six-site Laurent seed

Independently enter the nine edges as

```text
colour 0: 03:t, 12:t^-1, 45:1
colour 1: 14:1, 02:1,    35:1
colour 2: 25:1, 01:1,    34:1.
```

A bit-mask perfect-matching enumeration gives exactly

```text
matching colour word  valuation
--------------------------------
000000                 0
012012                 1
111111                 0
222222                 0.
```

The three constant words are the three colour classes.  The fourth matching
is `03|14|25`, so its product is `t`.  Hence the independently reconstructed
top tensor is exactly

```text
Delta_(6,3) + t e_012012.
```

There is no hidden cancellation: in a properly edge-coloured cubic graph, a
word fixes at each vertex the unique incident edge of its requested colour.
It therefore determines at most one perfect matching.

## 2. Vertex-to-triangle propagation

Let the edge of colour `i` at the split vertex be `v u_i`.  Replace `v` by
`s_0,s_1,s_2`, attach `u_i s_i`, and colour the edge opposite `s_i` by `i`.
For shifts `a_i`, assign

```text
nu(u_i s_i) = nu(v u_i) + a_i,
nu(s_j s_k) = -a_i,  {i,j,k}={0,1,2}.
```

Every perfect matching uses an odd number of the three external edges,
because the unmatched part of the three-vertex triangle must have even
cardinality.  There are only two cases.

* With one external edge `u_i s_i`, the opposite internal edge is forced.
  Contracting those two edges gives an old matching containing `v u_i`.
  The two new valuations sum to `nu(v u_i)`, and all three new output sites
  have colour `i`.  This gives a valuation-preserving bijection between old
  matchings and the one-external sector.
* With three external edges, no internal edge occurs.  Relative to zero
  shifts, every such valuation changes by `a_0+a_1+a_2`.

There are finitely many matchings in the second sector.  Taking
`a_0=a_1=0` and an integer

```text
a_2 >= max(0, 1 - minimum three-external base valuation)
```

makes all of them positive.  Each colour class belongs to the first sector:
its external and opposite internal shifts cancel.  Thus its total valuation
remains zero, while the old mixed matchings retain their positive valuations.
Proper cubic edge-colouring is preserved as well.

This local argument is an induction, not a finite-data extrapolation.  Each
split increases the number of vertices by two, so the six-site seed reaches
every even `n >= 6`.  The audit checker additionally reconstructs every local
contraction and verifies the bijection through `n=20`; it obtains matching
counts

```text
n:          6  8  10  12  14  16  18  20
matchings:  4  5   6   8  10  12  16  20.
```

## 3. Exact covariance determinant

Order the `3n` ports by colour.  Proper edge-colouring makes the covariance a
direct sum of three weighted perfect-matching adjacency matrices.  For one
colour there are `n/2` blocks

```text
[ 0  w_e ]
[ w_e  0  ],
```

so its determinant is

```text
(-1)^(n/2) product_e(w_e)^2.
```

The colour-class valuation sum is zero before the split and remains zero
after it.  With `w_e=t^nu(e)`, each colour product is one.  Multiplying the
three colour blocks gives

```text
det Z(A^(n)(t)) = (-1)^(3n/2),  t != 0.
```

This proves nonsingularity for every stage of the induction.  Separately from
that formula, the audit builds the full `3n x 3n` matrix at `t=3/2` and uses
exact rational Gaussian elimination through `n=20`; the results alternate
`-1,+1` as predicted.

## 4. Polynomial and regular-rational closure implication

The propagated top tensor has a coordinatewise expansion

```text
H_n(A(t)) = Delta_(n,3) + sum_(k>=1) t^k T_k.
```

Although the source contains negative Laurent powers, every output coordinate
lies in `C[t]`.  Therefore, for any polynomial `P` in top-tensor coordinates,
`P(H_n(A(t)))` also lies in `C[t]`, and its constant term is
`P(Delta_(n,3))`.  If `P` vanishes on the Wick image, this polynomial vanishes
for all nonzero `t`, hence identically, so its constant term vanishes.  This
proves both statements:

* taking positive real `t -> 0` puts the target in the ordinary tensor-space
  closure;
* every polynomial vanishing on the image also vanishes at the target, which
  puts it in the Zariski closure.

Any fixed local linear map, tensor product, permutation, contraction, or
linear (anti)symmetrization has polynomial coordinates in the input tensor.
Pulling a polynomial identity back through such a construction gives exactly
the preceding case.

For a rational expression `P/Q`, the necessary hypothesis is
`Q(Delta_(n,3)) != 0`.  Then `Q(H_n(A(t)))` has nonzero constant term and is
nonzero for generic nonzero `t`.  If the rational identity is zero wherever
defined on the image, `P(H_n(A(t)))` vanishes on that generic set and hence
identically.  Again `P(Delta_(n,3))=0`.  This justifies the primary note's
“regular at the target” qualification; no statement is made about a rational
separator with a pole at the target.

The checker encodes the constant-term mechanism independently: for all
coordinate monomials of degrees zero through four in the final audited
family, including an absent coordinate, it verifies that substitution's
constant term is the monomial evaluated at the target.  The general result is
the elementary multiplication argument above.

## 5. Bell-chain image and exact non-one-hot caveat

For each link use two Bell pairs.  Label their common two bits by
`d in {00,01,10,11}`.  A Bell pair `|00>+|11>` is the even two-mode Gaussian
state `exp(a^* b^*)|0>`, and tensor products on disjoint modes remain
Gaussian/matchgate signatures.  Thus the unprojected link product is in the
claimed algebraic Gaussian class.

Keep the three labels

```text
d_0=00, d_1=01, d_2=10.
```

The endpoint maps send `d_c` to `e_c` and kill `11`.  At an internal block,
send `(d_c,d_c)` to `e_c` and kill every other pair.  A chain assignment
survives exactly when every link has the same retained label.  There is one
surviving assignment for each `c`, each with coefficient one, so the exact
output is

```text
sum_(c=0)^2 e_c^(tensor r).
```

The independent enumerator verifies this for arities three through nine.
More importantly, it records the accepted internal four-bit support:

```text
0000, 0101, 1010,
```

whose Hamming weights are `0,2,2`.  None is one-hot.  This is an exact local
image under arbitrary blockwise linear maps, but it is not a Krenn local
projection and supplies no counterexample to the conjecture.

## 6. Audit result and scope

Run the independent checker with

```text
python3 computations/verify_global_wick_top_invariant_counterguard_independent_audit.py
```

Normal, optimized, isolated, and optimized-isolated execution produces

```text
7bf07ad7e7e3a697ebfc32088c36ec600c6b4fca6fbede532072f1a2cd08e1bb
```

The counterguard is valid: top-tensor polynomial equations, their fixed
polynomial contractions, and rational equations regular at the target cannot
separate ternary GHZ from the algebraic Wick image.  A surviving proof route
must retain non-closed source data, lower sectors, or the actual one-hot local
incidence restriction.
