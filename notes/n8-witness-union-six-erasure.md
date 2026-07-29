# Erasing-colour fibres on the full six-witness stratum

## 1. Outcome

Fix an invertible deleted block `A_pq` in the eight-site problem and suppose
all six outside sites are zero-cross witnesses.  The union-five table does
not include this stratum.  Applying the same hard-capacity, two-hole, and
erasing-colour tests gives the following exact audit.

There are `138` mask orbits with all six masks nonempty and every colour
having at least two witnesses.  Of these, `130` admit `1133` hard-capacity
assignments.  The previously proved nontriple two-hole and free-plane tests
leave `597` assignments in `72` mask orbits.

On that residual boundary:

* `498` assignments admit a nonconstant erasing pattern on five sites, so
  a complete three-word fibre of the internal six-site matching tensor
  vanishes;
* `82` more admit such a pattern on four sites, so a complete nine-word
  fibre vanishes;
* in `47` of those four-site cases the two un-erased sites are nontriple,
  and the common four-site coefficient on the erased sites vanishes too.

Thus only `17` assignments in `10` mask orbits have no four- or five-site
erasure certificate.  These are listed exactly in Section 3.  This is a
zero-fibre theorem, not by itself an exclusion of the other `580`
assignments.

## 2. Four erasures do not require nontriple leftovers for the fibre

For a word `x` on the outside six-set `R`, recall the uncapped identity

\[
 D_x=h_xA_{pq}+
 \sum_{\{u,v\}\subset R}h_{uv,x}
 \bigl(P_u(x_u)Q_v(x_v)^T+P_v(x_v)Q_u(x_u)^T\bigr).
 \tag{1}
\]

At an erasing site both displayed star columns are zero.  If a fixed
nonconstant erasing pattern occupies five sites, at most one site remains,
so the correction sum is zero.  Exactness and invertibility of `A_pq`
give `h_x=0` for all three extensions of the pattern.

If four sites are erased, only the pair of remaining sites can contribute.
Its correction is a sum of two rank-one matrices and has rank at most two.
It cannot cancel a nonzero multiple of the rank-three block `A_pq`.
Consequently `h_x=0` for all nine extensions.  This part does **not**
require the remaining sites to be nontriple.

When both remaining sites are nontriple, the nine now-zero corrections and
the two-site zero-block classification additionally force the common
four-site coefficient on the erased sites to be zero.  If a remaining site
is triple, only the nine-word fibre conclusion is asserted.

The available erasing colours are exactly:

1. the missing colour at an exact-double witness;
2. either off-hard colour at a triple-zero site hard for one colour.

Singleton witnesses and hard-mask-zero triple sites supply no erasing
colour by this lemma.

## 3. Exact no-certificate boundary

Use the mask convention

\[
0=\varnothing,\quad1=\{0\},\quad2=\{1\},\quad
3=\{0,1\},\quad4=\{2\},\quad5=\{0,2\},\quad
6=\{1,2\},\quad7=\{0,1,2\}.
\tag{2}
\]

After the two-hole and free-plane filters, the assignments with no
nonconstant erasing pattern on four or five sites are:

\[
\begin{array}{c|c|c}
\text{witness masks}&\text{hard masks at triple sites}&\#\\ \hline
(1,1,1,1,6,6)&\text{no triples}&1\\
(1,1,1,6,6,6)&\text{no triples}&1\\
(1,1,1,6,6,7)&(0)&1\\
(1,1,1,6,7,7)&(2,4),(4,2)&2\\
(1,1,2,3,6,7)&(4)&1\\
(1,1,2,5,6,6)&\text{no triples}&1\\
(1,1,2,5,7,7)&(2,4),(4,2)&2\\
(1,2,3,3,4,7)&(4)&1\\
(1,2,3,4,5,6)&\text{no triples}&1\\
(1,2,4,7,7,7)&\operatorname{Perm}(1,2,4)&6
\end{array}
\tag{3}
\]

Here a displayed hard-mask tuple is ordered along the triple sites in the
sorted witness-mask row.  The first two rows are the union-six analogues of
the exceptional singleton/double geometry: too few sites possess erasing
colours for the rank argument to start.

Seven of the ten rows in (3) contain a componentwise selected copy of the
union-five exceptional core `(0,1,1,1,6,6)`: select one colour at three
sites, the complementary double at two disjoint sites, and discard all
incidences at the sixth.  The three rows which do not are

\[
 (1,2,3,3,4,7),\qquad(1,2,3,4,5,6),\qquad
 (1,2,4,7,7,7).                                      \tag{4}
\]

This is only a downset statement.  The discarded sixth site remains a
genuine witness, an upgraded triple site is not an exact double, and the
union-five argument's nonwitness row is absent.  What the union-six branch
does add is a pure selector on that sixth triple shore.  Exploiting that
extra selector requires a shared-response argument; incidence containment
alone does not import the exceptional-row normal form.

For comparison, before the two-hole and free-plane filters the `1133`
hard-capacity assignments split into `748` five-erasure certificates,
`252` four-erasure certificates, and `133` no-certificate assignments.
The earlier filters are therefore essential for the short list (3).

## 4. What the sixth selector adds

Every witness site is a degenerate triple shore, so the union-six branch
has a pure three-cross selector at all six outside sites.  This strengthens
the five-selector coverage in two exact but presently nonterminal ways.

1. Every four-set `W` is the complement of **two** selector sites, so the
   arbitrary-open-row equations exist in both omitted-site directions.
2. If the six chosen selector colours have multiplicities `n_0,n_1,n_2`,
   at least
   \[
      \sum_r\binom{n_r}{2}\ge3                         \tag{5}
   \]
   omitted pairs have equal selector colour.  Their complements therefore
   carry the bidirectional equal-target overlap syzygies.  The minimum is
   the balanced distribution `(2,2,2)`.

Likewise, if `m` of the six selectors are nontermwise, the all-complement
bridge forces at least `ceil(m/2)` distinct four-site complements into its
excess-kernel or bipartite/disconnected branch; for six nontermwise
selectors this is at least three.

None of these counts alone kills the selected `011166` cores.  The
degeneracy colour of a selector need not be a zero-cross colour, and the
known all-selector sector countermodel satisfies even more selector
declarations without satisfying the uncapped matching identity.  Thus the
sixth selector supplies a second response on every complement, but using
it requires coupling those responses to the zero fibres above; it is not
an automatic reduction to the exact union-five row.

## 5. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_witness_union_six_erasure.py
```

The checker regenerates the `138` incidence orbits and all hard assignments,
reapplies the two prior obstruction stages, verifies every erasing colour
and nonconstant pattern, distinguishes the `47` cofactor-zero cases, and
checks the exact `10`-orbit/`17`-assignment list (3), including the seven
selected-core rows and the three exceptions (4).
