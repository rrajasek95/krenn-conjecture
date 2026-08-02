# Full all-spokes tangent and a five-parameter incidence family

Research evidence only. Krenn's conjecture remains open and the certified
spine is unchanged.

## Outcome

At the exact `1I+3R+2Z` all-spokes rank-`55/53` survivor, let all 32 entries
of the eight free core-to-zero spoke blocks vary. The exact first
determinantal obstruction has rank six. Consequently the Zariski tangent
space to the mixed-rank-at-most-53 locus has dimension 26, with reduced
linear equations

\[
\begin{aligned}
 \dot M_{14}(1,0)&=0, & \dot M_{15}(1,1)&=0,\\
 \dot M_{24}(0,0)&=0, & \dot M_{25}(0,1)&=0,\\
 \dot M_{34}(0,1)&=\dot M_{34}(1,1), &
 \dot M_{35}(0,0)&=\dot M_{35}(1,0).
\end{aligned}                                               \tag{1}
\]

This is only a tangent-space calculation. It does **not** prove that the
26-plane in (1), or a 26-dimensional component tangent to it, is contained
in the determinantal incidence locus. Direct rational-function rank
attempts on all 26 variables over both characteristic zero and finite
fields exceeded 300 seconds and are not part of the committed certificate.

Inside (1), however, the exact five-parameter family

\[
 M_{34}=\begin{pmatrix}a&b\\c&b\end{pmatrix},\qquad
 M_{04}=\begin{pmatrix}x&85\\0&87\end{pmatrix},\qquad
 M_{35}=\begin{pmatrix}0&y\\0&96\end{pmatrix}               \tag{2}
\]

has function-field ranks `55/53`. On its rank-55 locus it retains both pure
linear incidences and literal R2, but its full compatible L1 product space
misses both pure targets. Thus every rank-55 member of (2) is excluded.

The companion checker is
[`verify_level_two_one_invertible_three_rank_one_all_spokes_full_tangent_and_five_parameter_family.py`](../computations/verify_level_two_one_invertible_three_rank_one_all_spokes_full_tangent_and_five_parameter_family.py).

## 1. The full 32-variable determinantal tangent

Delete the two pure rows from the 64-by-60 differential at the committed
survivor. The resulting mixed matrix has rank 53, right nullity seven, and
left nullity nine. If \(N\) and \(L\) are exact rational bases for the right
and left kernels and \(E\) is a spoke direction, the first obstruction to
remaining in rank at most 53 is

\[
                         L^{\mathsf T}EN=0.                 \tag{3}
\]

The 63 scalar equations (3), evaluated on all 32 spoke-cell directions,
have exact row rank six. Their reduced row space is precisely (1). The
ordered direction ledger and reduced row space are pinned by SHA-256

```text
5bb8f8b24e8ff22628b12a278e370f925217e7b8c170a304dc5b5da26f6cda49
```

This enlarges the previously visible four-parameter germ to a substantially
larger first-order frontier, but no higher-order integration statement is
made.

## 2. Exact function-field family

Keep every other endpoint, potential, core block, and spoke at the committed
values and impose (2). Singular over \(\mathbb Q(a,b,c,x,y)\) gives

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53.                       \tag{4}
\]

On the subfamily `M_34=0`, computed over \(\mathbb Q(x,y)\), the ranks fall
to `50/49`. The in-memory Singular program is pinned by

```text
5e43c4b39fce8115296ec5c247a5a6eaba0bd6b4b5f55a9f21c676bfcc818c85
```

Because the mixed rank in (4) is a function-field upper bound, it holds at
every specialization. At a specialization with full rank 55, deleting two
rows can lower rank by at most two, so the mixed rank must equal 53. Hence
both pure rows are incident there. The exact point
`(a,b,c,x,y)=(1,2,3,4,5)` independently has ranks

```text
D = 55, D_mixed = 53,
D|e0 = 55, D|e1 = 55, D|e0,e1 = 55
```

over \(\mathbb Q\), \(\mathbb F_{101}\), \(\mathbb F_{32003}\), and
\(\mathbb F_{1000003}\). The selected equation still uses all 64 rows with
`z=-2`.

## 3. Uniform literal R2

For every nonzero root and each output colour, the checker fixes a pure
column and a complementary cofactor independent of all five parameters.
The eight cofactor values are

\[
 4416,\ 6336,\ 4416,\ 28,\ 33,\ 6336,\ 8624,\ 6216,          \tag{5}
\]

and are nonzero. Origin, coordinate, doubled-coordinate, pair, and mixed
parameter evaluations audit the full degree-at-most-two dependence. Thus
literal R2 holds uniformly on (2), including its rank-55 locus.

## 4. Constant L1 spaces on the rank-55 locus

For both P/V and Q/U, an exact rational nullspace basis consists of two
genuine star modes and the vacuous `rho_45` mode. Each displayed basis solves
the full five-parameter system coefficient by coefficient. Their digests are

```text
P/V e63aa09838b43d51f3de060f427bb45628e446e61e99f28ea790c80a5ea1f1a6
Q/U 45b6de4a61f4b66e7afae27574483e06bc4843218eff9a600dab6fff52bc03c3
```

After omitting the variable `M_34` rows, the `x` row of `M_04`, and the `y`
row of `M_35`, a fixed subsystem has rank 23. Rank 55 implies `M_34 != 0`,
because the `M_34=0` subfamily has rank at most 50. Its unique `rho_34`
column then raises the L1 rank to at least 24. The three fixed nullvectors
give the opposite bound, so both L1 systems have rank 24 and nullity three
throughout the rank-55 locus.

## 5. Uniform direct-plus-factored exclusion

The four products of the two Q/U modes with the two P/V modes are polynomial
of degree at most two in the five parameters. Collect their constant,
linear, and pair-quadratic coefficients into one uniform enlargement. Exact
ranks in all four audited fields are

\[
\begin{array}{c|ccccc}
 &\text{product coefficients}&+\text{direct}&+e_0&+e_1&+e_0,e_1\\ \hline
\operatorname{rank}&16&16&17&17&18.
\end{array}                                                  \tag{6}
\]

The direct slope satisfies the exact pointwise identity

\[
 \Psi(M)=2\sum_{i,j=1}^{2}d\Psi_M(N_{ij}),                  \tag{7}
\]

so it adds no direction. The coefficient matrix in (6) is pinned by

```text
d28dc4a21a918d6b7089a9ee4d8b67ffe6ad89324ed571ecae7f8da4f4f3b477
```

Every specialized compatible product lies in the rank-16 coefficient
space, while either pure target raises its rank. Therefore neither pure
target belongs to the genuine product span at any specialization. This
excludes the entire rank-55 part of (2) by the full direct-plus-factored L1
test.

## 6. Remaining frontier

The certified conclusion is the exclusion of the rank-55 five-parameter
family (2). The 26-dimensional space in (1) is a determinantal tangent
space, not a global component certificate; its nonlinear integration and
the rest of the all-spokes envelope remain open. In accordance with the
current strategic pivot, this follow-up records that residual boundary and
does not continue the level-two search.
