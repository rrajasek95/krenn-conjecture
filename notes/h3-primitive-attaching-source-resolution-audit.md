# No committed source-resolution cell kills the primitive attaching row

## Outcome

Let

\[
                 A=16T+\sum_{|S|=3}m_S,
 \qquad T=Q_3,                                          \tag{1}
\]

be the primitive row isolated in commit `cdc746d`.  The committed
three-set source-relative identity (`cd52b2b`) is the exact bridge to the
older attaching/Rees calculations.  Its connecting class

\[
 \mathcal K=\sum_{|S|=3}(M_S+\alpha\varepsilon_S)
\]

satisfies

\[
 \mathcal K-16\alpha Q_3
   =\sum_{|S|=3}F_{01}(w_S)-8\alpha H_2.                \tag{2}
\]

Consequently, in the quotient by the 20 literal middle rows and the
through-Hamming-two row,

\[
                         \boxed{[\mathcal K]=\alpha[A].} \tag{3}
\]

Thus a committed source-resolution generator maps to the *class* of the
primitive only in the weak sense (3): the three-set construction names it
as \(\mathcal K\), but does not null-homotope it.  On the selected open
\(\alpha\ne0\), killing \(A\) is exactly equivalent to producing an
invisible boundary for \(\mathcal K\).

The exact quotient presentation can be written on coordinates
\((T,S,\mathcal K)\), where \(S=\sum_Sm_S\).  Its two available rows are

\[
              S=0,\qquad \mathcal K-16\alpha T-S=0.    \tag{4}
\]

They have rank two in dimension three.  The separator

\[
                         (1,0,16\alpha)                 \tag{5}

kills (4), evaluates to 16 on \(A\), and to \(16\alpha\) on
\(\mathcal K\).  Adding \(\mathcal K=0\) closes the module with determinant
\(16\alpha\).  This is the smallest exact attaching obstruction.

## Audit of the committed candidate generators

The relevant committed source-resolution artifacts exhaust the named
low-order routes to (3):

| artifact | exact contribution | why it does not kill \(A\) |
|---|---|---|
| `cd52b2b` three-set class | identifies \([\mathcal K]=\alpha[A]\) | no nullhomotopy for \(\mathcal K\) |
| `b7f5856`, `bfc39cb` Hasse/Bianchi and flat overlap | typed difference/curvature identities | no response-to-middle attaching lift; ordinary differentiation is not tangent |
| `a6fc3ae`, `f81f6cf` literal Schur tails | every literal chart-odd tail is a kernel-vector tail | cannot supply a nonliteral attaching cell |
| `e7723de` shifted principal-parts square | real two-chart Rees polar | its lower faces have positive internal \(q\)-degree and vanish at \(q=0\) |
| `ed60e2c` denominator-marked four-cube | first canonical \(q\)-degree-zero polynomial symbol | cap chain and target/ordinary-residue maps are conditional, not constructed |
| `e9962c0` Reynolds/cap audit | tests that symbol against the old cap complex | proves no target-and-residue-invisible lift exists there |
| `befda3f` mixed-word reset | crosses the literal word gap | still lacks the relative first syzygy/chain lift |

The obstruction is multigraded, not a failure of coefficient search.  All
principal-parts faces before total order four have positive internal
\(q\)-degree, so \(q\mapsto0\) kills them while retaining the unit initial
component of (3).  The exact committed ladder is

\[
\begin{array}{c|c|c}
 \text{PP order}&q\text{-degree}&\text{stabilizer weight}\\ \hline
 2&2&\ne0\\
 3&1&\ne0\\
 4&0&0.
\end{array}                                             \tag{6}
\]

Thus order four is the first possible grade.  The order-four Reynolds
symbol reaches that grade, but the old cap module has basis
\((T_v,\rho_v)\) with

\[
\begin{array}{c|cc}
 &T_v&\rho_v\\ \hline
 d&-Yw_v&w_v\\
 \operatorname{tgt}&1&0\\
 \operatorname{ores}&0&1.
\end{array}                                             \tag{7}
\]

The common kernel of target and ordinary residue is zero.  Hence it cannot
contain a chain with nonzero boundary, over any localization or base
change that retains that boundary.  This is the smallest exact
localization obstruction; higher polynomial multipliers in the same free
cap module cannot repair it.

## Minimal new source row

The first possible new object is a cap-degree-one, denominator-marked,
order-four Rees/connection chain \(n_A\) satisfying

\[
 \boxed{
   dn_A=\mathcal K=\alpha A,qquad
   \operatorname{tgt}(n_A)=0,qquad
   \operatorname{ores}(n_A)=0.}                       \tag{8}
\]

Equivariantly this is the family called \(n_v\) in `e9962c0`.  Its
associated graded must be the \(q\)-zero Reynolds/denominator-marked
four-cube of `ed60e2c`; its lower curvature/connection face must have
nonzero \(q\)-augmentation, as required by `e7723de`; and it must be
constructed simultaneously with the relative first syzygy isolated in
`befda3f`.  Declaring (8) would close the module, but would assume the
missing theorem.  No committed source generator has all three faces in
(8).

This is a bounded all-existing-artifact audit.  It proves no global
nonexistence theorem for arbitrary future resolutions, and it does not
widen to higher Hasse order, support search, or Gröbner computation.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_primitive_attaching_source_resolution_audit.py
```

The checker reruns the formal sparse-polynomial three-set identity,
exhausts the selected endpoint fine-degree routes, verifies the quotient
separator and determinant at three rational \(\alpha\), rechecks the
principal-parts grade frontier and the exact old-cap augmented-rank
obstruction, and freezes the complete artifact-routing ledger.
