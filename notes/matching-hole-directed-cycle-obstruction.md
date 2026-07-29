# Directed cross cycles are impossible in the matching-hole chart

## 1. Outcome

Continue in the six-site paired Pfaffian chart of
[`matching-hole-zero-cross-pfaffian-obstruction.md`](matching-hole-zero-cross-pfaffian-obstruction.md).
Normalize the nonsingular hole block to the pure matching

\[
                         01|23|45.                         \tag{1}
\]

For sites on different matching edges define the directed two-vector

\[
 a_{i\to j}=\bigl(G_{h_i p_j},G_{h_i q_j}\bigr).          \tag{2}
\]

The two-site equations say that at most one of
`a_(i->j),a_(j->i)` is nonzero.  Thus the nonzero hole-particle entries
form an oriented subgraph of the complete tripartite graph with parts
`{0,1},{2,3},{4,5}`.

**Theorem 1.1 (directed four-cycle obstruction).**  Between any two parts
of (1), this oriented graph contains no alternating directed four-cycle.
Equivalently, in the four-site Schur complement, the two opposite
*transversal* cap tables (one entry for each choice of one particle at each
site of the opposite pair) cannot both be nonzero.

The proof is field-uniform and uses only the three- and four-site zero
coordinates.  Together with the zero-cross theorem it leaves a precise
smaller escape: a finite source would need nonzero directed cross entries,
no alternating directed four-cycle, and at least one nonzero global
cross-site entry in a decomposable Schur correction.

## 2. The local four-site calculation

Take two matching edges `a_0 a_1` and `b_0 b_1`.  If both opposite cap
corrections are nonzero, their support contains a directed perfect matching
from the `a` pair to the `b` pair and another in the reverse direction.
The two matchings cannot share a physical edge, by the two-site equation.
The only two perfect matchings of `K_(2,2)` are complementary.  Hence the
four directed vectors are nonzero and, after exchanging the two endpoints
if necessary, have the form

\[
 a_0\longrightarrow b_0\longrightarrow a_1
       \longrightarrow b_1\longrightarrow a_0.            \tag{3}
\]

Write `X_st` for the `2 by 2` particle-particle block between `a_s` and
`b_t`.  Switch the three sites `a_0,a_1,b_0`.  The hole edge
`h_(a_0)h_(a_1)` must be used: without it, the two holes on the `a` side
would have only one selected particle on the `b` side available.  The
remaining term is, up to sign,

\[
       a_{b_0\to a_1}(r_{a_1})
       X_{00}(r_{a_0},r_{b_0}).                            \tag{4}
\]

All eight color choices vanish.  The directed vector in (4) is nonzero,
so `X_00=0`.  Applying the same argument to the other three triples gives

\[
                         X_{00}=X_{01}=X_{10}=X_{11}=0.    \tag{5}
\]

Now switch all four sites.  Because of (5), no particle-particle edge can
occur.  There is exactly one surviving paired perfect matching: the four
directed hole-particle edges in (3).  Choose at each target site a color on
which its incoming vector is nonzero.  The coefficient is then, up to sign,

\[
 \prod_{i\to j\text{ in }(3)} a_{i\to j}(r_j)\ne0,        \tag{6}

\]

contradicting the four-site zero coordinate.  This proves Theorem 1.1.

For the asserted equivalence with caps, let `U,V` be the two rows of
hole-particle entries belonging to one matching edge.  Its contribution to
the particle Schur complement is the decomposable alternating form
`U wedge V`.  The `2 by 2` table obtained by selecting one particle mode at
each site of the opposite pair is nonzero only if the directed support
contains a perfect matching to those two sites.  Nonzero transversal tables
in both directions would therefore give exactly the forbidden configuration
above.  (A wedge entry using both particle modes at one site is irrelevant
to every transversal coefficient and is not called a cap here.)

## 3. Precise surviving escape

Let `M_k` be the two hole-particle rows on the `k`-th edge of (1), and put

\[
             R_k=M_k^{\mathsf T}H_k^{-1}M_k.              \tag{7}
\]

Each `R_k` is alternating, decomposable, has rank at most two, and is
supported on particles outside the `k`-th pair.  If every cross-site entry
of all three `R_k` vanishes, the full particle Schur complement agrees with
the particle block `Q` on every transversal selection.  By Theorem 1.1,
the opposite caps on every four-site union have zero product, so its proper
four-site equation is precisely the five-component equation of the
zero-cross note.  The exact `5^3` rank-collapse lemma then contradicts the
full binary equality face.

Consequently every remaining matching-hole candidate must satisfy all of
the following:

1. some directed vector (2) is nonzero;
2. at least one global wedge `R_k` in (7) has a nonzero cross-site entry;
   and
3. no two matching pairs carry an alternating directed four-cycle.

What remains is to couple the three allowed decomposable corrections
`R_0,R_1,R_2` across different four-site faces.  The local cap on one face
is removed from that face's Schur complement but reappears in the full
six-site particle tensor; this is why the existing `125`-component
flattening audit does not by itself cover the last stratum.

## 4. Exact audit

Run

```text
.venv/bin/python computations/verify_matching_hole_directed_cycle_obstruction.py
```

The checker enumerates all `3^4` absent/forward/backward orientations of a
`K_(2,2)`, verifies that only the two alternating cycles can support caps
in both directions, and expands every relevant paired Pfaffian as a sparse
integer polynomial.  It checks all three-site colorings and all sixteen
four-site colorings for both cycles.
