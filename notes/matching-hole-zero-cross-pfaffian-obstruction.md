# The matching-hole, zero-cross Pfaffian boundary is impossible

## 1. Outcome

Work in the three-symbol paired Pfaffian chart of
[`paired-pfaffian-local-rank.md`](paired-pfaffian-local-rank.md).  Thus each
site has modes `h_i,p_i,q_i`, with local codewords

\[
 0\leftrightarrow\varnothing,\qquad
 1\leftrightarrow\{h_i,p_i\},\qquad
 2\leftrightarrow\{h_i,q_i\}.                              \tag{1}
\]

Let `H=(G_{h_i h_j})` be the nonsingular hole block.  The following closes
the chart containing the signed prism border family.

**Theorem 1.1 (matching-hole, zero-cross obstruction).**  On six sites,
there is no finite paired Pfaffian realization of `Delta_(6,3)` satisfying

1. the support of `H` is one perfect matching; and
2. every hole-particle entry vanishes:
   `G_(h_i p_j)=G_(h_i q_j)=0` for all `i,j`.

The proof works over every field.  It allows arbitrary particle-particle
entries and arbitrary cancellation.  In the original transverse covariance
`K=[[A,B],[-B^T,D]]`, condition 2 is exactly `B=0`, because the paired cross
block is `A^(-1)B`.

The Laurent family in
[`signed-pfaffian-six-border.md`](signed-pfaffian-six-border.md) has exactly
this source form: the reference covariance is supported on one matching and
there are no inter-color cells.  The theorem therefore proves that its pole
cannot be removed while remaining in the same localized source chart.

## 2. Reduction to a binary particle tensor

Relabel the hole matching as

\[
                         M=01|23|45.                        \tag{2}
\]

Its three entries are nonzero.  The one- and two-site zero equations, or
Lemma 1.1 of the local-rank note, imply that the full inter-site block on
each edge of `M` is pure hole.  Under the zero-cross hypothesis this says in
particular

\[
              G_{p_i p_j}=G_{p_i q_j}=G_{q_i p_j}=G_{q_i q_j}=0
                         \qquad(ij\in M).                  \tag{3}
\]

Let `Q` be the particle-particle block of `G`.  Switch precisely the four
sites in the union of two edges of `M`.  Hole-particle entries vanish, so
the selected paired matrix is block diagonal between its holes and
particles.  Its Pfaffian is, up to a fixed sign,

\[
        \operatorname{Pf}H[S]\operatorname{Pf}Q[r_i:i\in S]. \tag{4}
\]

The first factor is the product of two nonzero matching entries.  The target
coordinate is zero.  Hence every binary transversal Pfaffian of `Q` on each
four-site union is zero.

When all six sites are switched, the same factorization shows that the full
binary transversal tensor of `Q` must be a nonzero scalar multiple of

\[
                         e_p^{\otimes6}+e_q^{\otimes6}.     \tag{5}

The tensor in (5) has flattening rank two across every nonempty proper cut.
We now show that the four-site zero equations force the full tensor of `Q`
to have rank at most one across at least one such cut.

## 3. The five components of one cross block

Group the sites into `I={i_0,i_1}` and `J={j_0,j_1}`, two edges of `M`.
Since (3) removes the internal blocks, write the covariance between the two
groups as four arbitrary `2 by 2` color matrices

\[
                         X_{st}\quad(s,t\in\{0,1\}).       \tag{6}
\]

For colors `a,b,c,d`, the four-site Pfaffian in (4) is

\[
 X_{00}(a,c)X_{11}(b,d)-X_{01}(a,d)X_{10}(b,c)=0.          \tag{7}

**Lemma 3.1 (five-component lemma).**  Every solution of (7) lies in at
least one of the following five components:

* the assembled `4 by 4` matrix `X` has rank at most one;
* all entries incident to `i_0` vanish;
* all entries incident to `i_1` vanish;
* all entries incident to `j_0` vanish; or
* all entries incident to `j_1` vanish.

**Proof.**  If one block is zero, (7) says that the tensor product of the
opposite two blocks is zero.  Over a field, one of those blocks is therefore
zero as well, giving a zero site-row or site-column.

Otherwise all four blocks are nonzero.  Choose `b_*,d_*` with
`X_11(b_*,d_*) != 0`.  Equation (7) gives

\[
 X_{00}(a,c)=
 {X_{01}(a,d_*)X_{10}(b_*,c)\over X_{11}(b_*,d_*)},       \tag{8}

so `X_00` has rank one.  Repeating (7) after fixing a nonzero entry in each
of the other blocks gives vectors `u_0,u_1,v_0,v_1` such that

\[
                         X_{st}=u_s v_t^{\mathsf T}        \tag{9}

for all `s,t`.  Thus the assembled matrix is rank one. `QED`

Apply Lemma 3.1 independently to the three group pairs

\[
                   (01,23),\qquad(23,45),\qquad(45,01).   \tag{10}

There are only `5^3=125` resulting component triples.

## 4. Exact finite rank lemma

**Lemma 4.1 (three-block rank collapse).**  Let `Q` be a binary covariance
on six sites, zero on `01,23,45`, and suppose its three cross blocks satisfy
(7).  Then the full six-site transversal Pfaffian tensor of `Q` has a
nonempty proper physical cut whose flattening rank is at most one.

**Proof.**  Parameterize a rank-one component in (9) by its eight endpoint
coordinates.  Parameterize a site-isolating component by the eight free
entries on its two remaining site blocks.  Expand the fifteen signed
perfect matchings over the integers.  For every component triple, all
`2 by 2` minors of one nontrivial flattening vanish identically as sparse
integer polynomials in these formal parameters.

The cases group as follows:

\[
\begin{array}{c|c|c}
\text{rank-one cross blocks}&\text{number of component triples}
 &\text{sizes of certified cuts}\ \hline
3&1&2\ (1\text{ case})\\
2&12&1\ (12\text{ cases})\\
1&48&1\ (42\text{ cases}),\ 3\ (6\text{ cases})\\
0&64&1\ (24\text{ cases}),\ 2\ (40\text{ cases}).
\end{array}                                                \tag{11}
\]

This is a finite algebraic case split, not a numerical rank test.  The
checker represents each coefficient as a signed sparse polynomial over
`Z`; after choosing a nonzero pivot entry of a flattening it verifies

\[
                         F_{ab}F_{a_0b_0}=F_{ab_0}F_{a_0b} \tag{12}

for every row and column.  Equation (12) is exactly the vanishing of all
`2 by 2` minors.  The five components cover every field-valued point by
Lemma 3.1, including their intersections and all zero degeneracies.  This
proves the lemma. `QED`

Lemma 4.1 contradicts the rank-two statement following (5), proving
Theorem 1.1.

## 5. Audit and scope

Run

```text
.venv/bin/python computations/verify_matching_hole_zero_cross_pfaffian_obstruction.py
```

The checker constructs all `64` coefficients for every one of the `125`
formal component triples, with canonical Pfaffian crossing signs, and
certifies an identically rank-one flattening over `Z`.

The remaining matching-hole chart has nonzero hole-particle couplings on
off-matching pairs.  There the two-site equations orient each such pair:
at most one of the two directed hole-particle vectors can be nonzero.  A
complete characteristic-zero obstruction must next couple that directed
cross graph to the three four-site equations; Theorem 1.1 shows that every
escape from the signed prism boundary must use such a nonzero directed
coupling.

