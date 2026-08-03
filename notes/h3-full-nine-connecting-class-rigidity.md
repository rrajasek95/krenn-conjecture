# Every literal chart-odd tail is a kernel-vector tail

The literal \(h=3\) no-go
[`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md)
proves the five marked polar cochains have source-relative connecting
matrix \(I_5\).  Its scope statement leaves three escapes: the
denominator-marked cell, a larger source-provenant Hasse/Spencer
totalization, and "a different literal operation whose added tail cancels"
the class.

The denominator-marked cell is **not** closed: see
[`h3-denominator-face-decoration-fork.md`](h3-denominator-face-decoration-fork.md),
which withdraws an earlier closure claim and shows the escape forks on the
chart decoration of one face.
This note proves what the literal chart-labelled source rows can and
cannot supply, by an exhaustive sweep over all \(3^8\) global words rather
than a chosen family: every chart-odd tail they produce is a kernel-vector
tail, and the connecting map over the whole literal complex is \(I_5\).

Krenn's conjecture remains open.  This constrains the escapes and
constructs no replacement.

## 1. The two charts carry the same marked tail

Two facts.  Fact A is marking-independent and is checked once per word;
Fact B is checked on every one of the 6561 words and every one of the five
markings \((a_{xv}^{00},a_{pq}^{00})\):

**A.  The two charts partition the same row.**  The \(pq\)-chart splits the
90-term direct-free row as \(15+75\); the \(pr\)-chart splits it as
\(0+90\), because the direct-free hypothesis \(A_{pr}=0\) empties the
\(pr\)-direct piece.  Both are partitions of the *same* \(H_w\).
Consequently

\[
 k_w=r_w^{pq}-r_w^{pr}\in\ker A'
 \qquad\text{for every global word }w,                       \tag{1}
\]

not merely for the five selected polar rows.

**B.  The two chart marked tails are the same polynomial.**  Write
\(X_{v,w}=\partial_{a_{xv}^{00}}\partial_{a_{pq}^{00}}H_w\).  Then

\[
 \bigl(\text{$pq$-chart tail}\bigr)=(X_{v,w})_{pq,\mathrm{direct}},
 \qquad
 \bigl(\text{$pr$-chart tail}\bigr)=(X_{v,w})_{pr,\mathrm{two\text{-}star}}.
                                                             \tag{2}
\]

The reason is exact and one-sided: differentiating by \(a_{pq}^{00}\) forces
the \(pq\) edge, so all \(pq\)-chart marked material is \(pq\)-direct; and
\(A_{pr}=0\) empties the \(pr\)-direct piece, so all \(pr\)-chart marked
material is \(pr\)-two-star.  The checker confirms that the \(pq\)-star and
\(pr\)-direct tails are identically zero, and that the two surviving tails
are equal as polynomials, on all \(5\times6561\) cases.

Exactly \(405=5\times81\) of those tails are nonzero — the marking needs
colour zero at \(x,v,p,q\), leaving the other four odd sites free.

## 2. Every chart-odd tail is a kernel-vector tail

Fix a deletion site \(v\).  A general literal combination of chart-labelled
columns in its marked support is

\[
 \sum_w\bigl[\ell_w\,r_w^{pq}+\rho_w\,r_w^{pr}\bigr],       \tag{3}
\]

with tail \(\sum_w[\ell_w(X_{v,w})_{pq}+\rho_w(X_{v,w})_{pr}]\).  By (2)
the two sector copies carry the same polynomial, so the chart-odd part of
that tail is

\[
 \sum_w\frac{\ell_w-\rho_w}2
   \Bigl[(X_{v,w})_{pq}-(X_{v,w})_{pr}\Bigr]
 =T'\Bigl(\sum_w\frac{\ell_w-\rho_w}2\,k_w\Bigr).           \tag{4}
\]

That gives the inclusion \(\subseteq\).  The reverse needs
\(\ker A'=\langle k_w\rangle\), i.e. linear independence of the 6561 rows.
That holds, and is now checked: a labelled matching monomial records the
colour of every site (each site lies in exactly one edge), so a monomial
determines its word, the 6561 row supports are pairwise disjoint, and the
rows are independent.  The checker verifies that all \(6561\times90\)
labelled monomials recover their word and that no monomial is shared.
Hence

\[
 \{\text{chart-odd literal tails}\}=T'(\ker A').             \tag{5}
\]

The checker verifies (4) directly, on all 81 columns of each deletion site
simultaneously, with deterministic exact rational coefficients, three
independent trials per site, and confirms that every cochain sees only the
kernel-vector tail.

## 2b. The connecting map over the whole kernel

Section 3 needs \(\Lambda_v(T'(k_w))\) for **all** 6561 words, not only the
five selected ones.  The checker computes exactly that: for each deletion
site it sweeps every word, forms the literal \(pq\)-chart marked tail
through `chart_partition`, and evaluates the mass.  **Exactly one** word
per site has a nonzero value — the selected polar row \(c_v\) — with value
exactly \(1\).

This is precisely where the companion note
[`h3-chart-parity-schur-repair-reduction.md`](h3-chart-parity-schur-repair-reduction.md)
failed and this one does not.  Its analogous claim was refuted by a
chart-odd witness supported on a **single** monomial of \(h_v\); no literal
source tail is like that, because a marked derivative of a hafnian is
always a full three-term face hafnian.  The sweep makes that difference
exact rather than informal.

## 3. What follows

Put (5) and the sweep together with the parity fact from the companion
note:

* **chart-neutral** material pairs to zero with every \(\Lambda_v\), so it
  contributes nothing to the connecting matrix;
* **chart-odd** material is, by (5), the tail of a kernel element, and the
  sweep shows the connecting map over the whole literal complex is
  exactly \(I_5\).

So among literal chart-labelled tails, \(-I_5\) is reachable only as the
tail of \(-k_v\).

**What this does not settle.**  Whether supplying the tail of \(-k_v\)
counts as a repair or merely restates the kernel vector is a question
about the unconstructed comparison complex, and is *not* decided here.  An
earlier draft asserted it was "not a new source datum" and titled itself a
rigidity theorem on that basis; the phrase was never formalized, so both
have been withdrawn.  Relatedly, the "must contribute \(-I_5\) on the five
kernel vectors" framing is inherited from the no-go's section 5, and
adding a repair column could in principle change \(\ker A'\) itself — an
assumption neither artifact states.

## 4. What is left

The no-go's escapes are now cut down to one shape.  Any operation that can
still cancel \(I_5\) must have a tail that is **not** a literal
chart-labelled source tail — it must break the chart symmetry that (2)
imposes on the entire complex.  By (2), that symmetry is a consequence of
two things only:

1. \(\partial_{a_{pq}^{00}}\) forcing the \(pq\) edge, and
2. the direct-free hypothesis \(A_{pr}=0\).

So a replacement operation must have a tail **outside the literal
chart-labelled source rows**.  It does *not* follow that it must change
the marking or leave the direct-free specialization: the Hasse/Spencer
totalization the no-go leaves open, and denominator or cap material, can
have such a tail while keeping both.  An earlier draft claimed the
stronger dichotomy; it does not follow from what is proved and has been
withdrawn.

Nothing here says such an operation exists.  It may equally be that the
polar route is dead and the chart-25 class must reach the full-nine
curvature residue by a different comparison entirely — the interface
\((24)\)–\((25)\) of
[`n8-chart25-schur-bockstein-dual-lift.md`](n8-chart25-schur-bockstein-dual-lift.md)
remains the specification either way.

## 5. Scope

1. Finite, \(h=3\), direct-free specialization
   \(x=0,\ D=(1,2,3,4,5),\ p=6,\ q=7,\ r=3,\ A_{pr}=0\).
2. Facts A and B are proved by exhaustion over all 6561 global words and
   all five markings — not sampled.
3. Statement (4) is verified on the full 81-column family of each deletion
   site with three exact rational coefficient trials, with the two chart
   tails built independently through `chart_partition` (so the identity
   depends on Fact B, not on the tagging); the algebra displayed above is
   the proof.
4. The row-independence behind (5) and the full-kernel sweep behind 2b are
   proved by exhaustion, not sampled.
5. This constrains tails that are literal chart-labelled source tails.  It
   does **not** exclude an operation of a different shape, does not decide
   whether the tail of \(-k_v\) constitutes a repair, and constructs no
   replacement.  Nothing on the certified spine changes and Krenn's
   conjecture remains open.

## 6. Verification

Run

~~~text
python3 computations/verify_h3_full_nine_connecting_class_rigidity.py
python3 -O computations/verify_h3_full_nine_connecting_class_rigidity.py
python3 -I computations/verify_h3_full_nine_connecting_class_rigidity.py
python3 -S computations/verify_h3_full_nine_connecting_class_rigidity.py
python3 -I -S computations/verify_h3_full_nine_connecting_class_rigidity.py
~~~

The checker sweeps all 6561 words, verifies
the chart partitions and the direct-free split, verifies that the
\(pq\)-star and \(pr\)-direct marked tails vanish identically and the two
surviving tails are equal, counts the 405 nonzero tails and the 81
marked-support words per site, verifies row-support disjointness on all
\(6561\times90\) labelled monomials, verifies (4) on fifteen exact rational
trials with the two chart tails built independently through
`chart_partition`, sweeps all 6561 words to show exactly one literal tail
per site meets each cochain with value 1, and re-derives the connecting
matrix \(I_5\).  Runtime is about fifteen seconds.  Its frozen ledger
digest is

~~~text
b2e0a4d4bbbfd07fbc354df7f3b5a1ac776929bd06ed4ffc0458ea894a637c4c
~~~

Mutation-tested: inverting the equal-tails assertion, inverting the
kernel-tail identity, perturbing the kernel coefficient, and changing the
nonzero-tail count each raise under both `python3` and `python3 -O`, with a
message naming the broken property.
