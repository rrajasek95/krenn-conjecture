# The all-zero exact-three path is impossible

## 1. Result

The preceding boundary reductions leave one exact-three candidate, up to
block-row and block-column permutations and transposition:

\[
                    B_{00}=B_{01}=B_{10}=0,qquad
                    B_{ij}\text{ invertible otherwise}.       \tag{1}
\]

**Theorem 1.1.**  The array (1) cannot satisfy the left dead-slab
four-cross equations.

Consequently the two-`K_4` dead slabs force at least four singular cross
blocks.  The exact-three stratum is empty.

No two-cross coefficient or live target normalization is needed.  The
proof closes (1) using the actual sparse-row cofactor equations, an exact
one-defect `Per_3` lemma, and projective-frame contractions.  The checker is
[`verify_two_k4_exact_three_allzero_path_obstruction.py`](../computations/verify_two_k4_exact_three_allzero_path_obstruction.py).

## 2. The two sparse-row cofactors

Use the two oriented-triangle dead coordinate lines with hole 0.  Their
fixed assignments, in the standard order, are

\[
\begin{split}
 t_0&:(1,1),(2,2),(3,0),\\
 t_1&:(1,2),(2,0),(3,1).                                \tag{2}
\end{split}
\]

For either line, contraction of the four right factors gives

\[
                \sum_{j=0}^3B_{0j}y_jC_j=0.                  \tag{3}
\]

In (1), only the reference maps `B_02,B_03` are nonzero, and both are
invertible.  Their generic images are independent.  The sparse-reference
cofactor lemma from
[`two-k4-exact-three-path-zero-collapse.md`](two-k4-exact-three-path-zero-collapse.md)
therefore gives

\[
                              C_2=C_3=0                       \tag{4}
\]

for both lines in (2).

The local tensor `C_2` uses physical block columns `0,1,3`, while `C_3`
uses columns `0,1,2`.  In both, the map in physical column 0 has exactly one
zero coordinate image: selected block row 1 meets `B_10=0`, whereas the
selected rows from `B_20,B_30` are nonzero.  Every coordinate image in the
other two factors is nonzero.

## 3. Exact one-defect `Per_3` lemma

Let `A,B,C` be three local maps and write `a_i=Ae_i`, and similarly for
`b_i,c_i`.

**Lemma 3.1.**  Suppose `a_0=0`, while `a_1,a_2` and every `b_i,c_i` are
nonzero.  If

\[
                 (A\otimes B\otimes C)\operatorname {Per}_3=0, \tag{5}
\]

then:

1. if `a_1,a_2` are independent, both `B` and `C` have rank one;
2. if `a_1,a_2` are proportional and `B` has rank three, (5) is impossible.

**Proof.**  With `a_1,a_2` independent, (5) separates into

\[
 b_0\otimes c_2+b_2\otimes c_0=0,
 \qquad
 b_0\otimes c_1+b_1\otimes c_0=0.                           \tag{6}
\]

Equality of nonzero pure tensors gives
`b_0 proportional b_1 proportional b_2` and
`c_0 proportional c_1 proportional c_2`.

In the second case, rescale so that `a_2=lambda a_1`.  Equation (5) becomes

\[
 b_0\otimes(c_2+\lambda c_1)
 +(b_2+\lambda b_1)\otimes c_0=0.                           \tag{7}
\]

If `B` has rank three, `b_0` and `b_2+lambda b_1` are independent.  Hence
(7) forces `c_0=0`, contrary to the hypothesis.  \(\square\)

The statement is invariant under coordinate and factor permutations.

For a triangle `t`, let `r_tj` say that its local map in physical column
`j` has rank at most one.  Applying the first part of Lemma 3.1 to (4)
gives the necessary implications

\[
\begin{split}
 r_{t0}&\ \text{or}\ (r_{t1}\text{ and }r_{t3}),\\
 r_{t0}&\ \text{or}\ (r_{t1}\text{ and }r_{t2})
 \qquad(t=0,1).                                         \tag{8}
\end{split}
\]

If `r_t0` holds, the second part will instead give a contradiction as soon
as one clean factor is certified to have rank three.

## 4. Generalized frame-singleton contraction

The projective-frame lemma used earlier may contract any nonempty subset of
the four right factors, not only three of them.

**Lemma 4.1.**  Suppose the relevant row lines in each factor of a set `J`
belong to a known projective frame.  Group the active permutations in a
dead four-cross tensor by their frame-line signature on `J`.  If one
signature is used by exactly one permutation, the tensor is nonzero.

Indeed, contract each factor in `J` by the corresponding frame dual.  The
singleton leaves a tensor product of nonzero vectors in the uncontracted
factors, or a nonzero scalar if all four factors were contracted.

The frames in the audit are always the three rows of specified invertible
physical blocks.  Thus accidental proportionalities cannot merge their
distinct lines.

## 5. Exhaustion of the all-zero path

The prior exact incidence system has 46,854 simultaneous four-column status
models for the all-zero path.  Imposing the four necessary implications
(8) leaves 892.

Generalized frame-singleton contractions eliminate 838 of those models.
A representative certificate is

\[
 (m_0,m_1,m_2,m_3)=(f3,0c,64,98),
 \qquad(a,J,\pi)=(0110,03,2103).                            \tag{9}
\]

Exactly 54 models remain.  Every one has both of the following properties,
for each `t=0,1`:

1. `r_t0` holds, so the two active vectors in the dirty physical-column-0
   map are proportional;
2. the three selected lines in physical column 1 are identified with the
   three rows of one invertible block and hence form a basis.

The second part of Lemma 3.1, applied to either zero tensor in (4), now
contradicts these two properties.  Thus none of the 54 residual models can
come from an actual array.

For drift detection, the complete 838 contraction records have SHA-256
digest

```text
02af118f831dfad0bdb941e5b053a3d3037fd95e093bd92c10dc4e99740285be
```

and the sorted 54 residual masks have digest

```text
d3e28974994bd4adbe7f1c85bb47c73f92b04e650ca1fde63de1c10a2e9146d6
```

All finite relaxations are conservative: zero-`Per_3` equations contribute
only necessary rank implications, and the projective union-find records
only forced proportionalities.  Therefore the exhaustion contains every
actual complex array of the form (1).  This proves Theorem 1.1.

## 6. Boundary after exact-three closure

Combining this theorem with the position-orbit, matching, and sparse-path
obstructions gives the sharp current statement

\[
          \#\{(i,j):\det B_{ij}=0\}\geq4.                    \tag{10}
\]

for every two-`K_4` chart satisfying both dead slabs.  The remaining
frontier begins with four or more singular cross blocks; the two-cross and
live target equations have still not been needed in reaching (10).
