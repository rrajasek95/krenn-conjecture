# Independent audit of the universal denominator reset no-go

This note independently audits commit `f09cbfb`.  It does not import the
primary checker and it does not construct a physical four-face homotopy,
full-source Tor class, or rational localized lift.  The unified overlap
theorem, SP-CLEAN-BRIDGE, and Krenn's conjecture remain open.

## Result

The universal polynomial no-go and its stated scope are correct.  For each
of the fifteen columns

\[
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]},
\]

the independent checker constructs the three perfect matchings of the four
sites in \(D\setminus\{v\}\) directly.  A nonzero coefficient occurs on the
81 words with \(w_v=a\), and each coefficient contains three labelled
quadratic monomials.  This gives \(15\cdot81\cdot3=3645\) features.

Every feature has a unique word owner.  Its two labelled edges recover the
colours on the four retained sites, while the column label \((v,a)\)
recovers the omitted colour.  Conversely, each of the 243 words owns
fifteen features.  This verifies the full universal denominator map, not
only the five columns met by the selected reset.

## Lowest-degree and augmentation obstruction

Write a polynomial functional as

\[
 L=\sum_w\ell_w(q)\epsilon_w,
 \qquad c_w=\ell_w(0).
\]

Since every entry of the denominator matrix is homogeneous of
\(q\)-degree two, the degree-two part of \(L\delta\) depends only on the
constants \(c_w\).  In a fixed denominator column, the coefficient of a
feature is its unique owner's \(c_w\).  Thus the initial map on the 243
constants has rank 243 and \(L\delta=0\) forces every \(c_w=0\).
In particular, \(\ell_{12112}=1\) is impossible; higher-degree polynomial
terms enter too late to cancel its uniquely owned quadratic feature.

This argument excludes a normalized **polynomial** annihilator over the
universal internal ring.  It does not exclude an annihilator with all
coefficients in the augmentation ideal, a rational projector after
localizing at internal minors, or a new kernel after non-flat full-source
specialization.

## Pure and mixed deletion faces

At output \(Y_0=e_{00000}\), the old denominator presentation has exactly
the five nonzero face polynomials

\[
 g_v=\operatorname {Haf}(q_{00000}|_{D\setminus\{v\}}).
\]

The selected mixed word \(12112\) gives

\[
 h_v=\operatorname {Haf}(q_{12112}|_{D\setminus\{v\}}).
\]

The independent formulas for all five \(h_v\) agree term by term with
`f09cbfb`.  Different deletion sites have different four-site supports, so
the five \(g_v\) are independent and the five \(h_v\) are independent.
Every edge variable in a \(g_v\) has colour label \(00\), whereas the
\(h_v\) use only labels \(1,2\).  Hence the two monomial supports are
disjoint and exact sparse row reduction gives

\[
 \operatorname {rank}\langle g_1,\ldots,g_5\rangle=5,
 \qquad
 \operatorname {rank}\langle g_1,\ldots,g_5,h_1,\ldots,h_5\rangle=10.
\]

The mixed pure-output defect therefore has cokernel rank five at its lowest
\(q\)-degree.  Polynomial coefficients multiplying old target rows cannot
alter this degree except through their constant terms.

## Minimal abstract repair and survival of \(Y_0\)

Adjoining abstract generators \(\tau_v\) with

\[
 d\tau_v=h_vY_0
\]

gives an exact fifteen-column chain identity: send the five columns
\(d_{v,(12112)_v}\) to the corresponding \(\tau_v\), and send the other ten
to zero.  The checker verifies this equality as a sparse polynomial on
every column.  Five generators are minimal in the associated
degree-two/pure-output piece because the five \(h_v\) have independent
classes modulo the old \(g_v\)-span.

All old denominator boundaries and all five new boundaries lie in the
square of the \(q\)-augmentation ideal.  Evaluation at \(q=0\) annihilates
their entire polynomial submodule but sends the constant basis vector
\(Y_0\) to one.  Therefore the abstract repair does not kill \(Y_0\).

## Provenance scope

The five \(\tau_v\) are a minimal presentation of missing initial data,
not evidence that those data occur in the physical complex.  The abstract
records contain no full-nine source row, no cancellation of physical
target or ordinary residue, no cancellation of other EqSystem boundary
components, and no full-source Tor transgression.  Those are precisely the
remaining obligations.  Likewise, the polynomial no-go says nothing
against rational constructions on smaller opens.

Thus the strict nonclaim in `f09cbfb` is essential and correct: the result
identifies the five initial components a successful source-provenant lift
must realize, but does not realize them.

## Executable verification

The dependency-free audit is
[audit_h3_universal_denominator_reset_polynomial_no_go_independent.py](../computations/audit_h3_universal_denominator_reset_polynomial_no_go_independent.py).
It uses `require`/`RuntimeError` and provides `all`, `denominator`,
`initial`, `faces`, `repair`, and `provenance` modes.  The combined exact
ledger is frozen by SHA-256.

```text
c7fdfc45332832602e08d580be9a73c48c18113ea113066fec6ef9d9c7240342
```
