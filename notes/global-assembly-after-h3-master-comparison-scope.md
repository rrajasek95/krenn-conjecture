# Global assembly after the pointed \(h=3\) master comparison

## Outcome

The literal pointed augmented comparison currently formulated in the
repository is an \(h=3\), hence \(N=8\), theorem. Even if that theorem is
granted with its odd \(\Xi/M_v/q\), generic-even packet/\(W\), Bockstein \(V\),
and pointed-anchor restrictions, it does **not by itself** imply

\[
                         k_{\max}(N)\leq2
                         \qquad(N\geq6\text{ even}).                 \tag{1}
\]

The minimal-order induction after a uniform bridge is complete. The global
gap is before the induction: the \(h=3\) comparison has not been promoted to
every \(h\geq3\), every automatic packet, and every rootless/inactive branch;
nor does a local \(q\)-row Fredholm alternative automatically produce an
actual source-terminal contradiction.

Thus the exact answer is:

* **yes**, if “the single comparison-or-terminal theorem” is read as the
  uniform, branch-complete, source-terminal theorem stated below;
* **no**, if it means the literal canonical \(h=3\) comparison, even with all
  four of its displayed restrictions.

This is a scope audit, not a new claim that the comparison exists.

## Precise conditional closure theorem

For \(h\geq3\), put \(N=2h+2\). Assume the following statement
\(\mathsf{PAComp}(h)\).

> For every finite exact ternary source on \(N\) sites, choose the committed
> maximum-anchor/minimum-support representative and its automatic full-nine
> two-chart packet. On the **actual complete physical relative source
> complex**, not merely a presentation or coarse quotient, there is one
> pointed, \(k[\beta]\)-linear, \(\rho\)-equivariant comparison-or-terminal
> construction. It has the literal word/fine/repeated grading, protected
> rows, and source labels, and it has all of the following consequences.
>
> 1. Its odd restriction realizes the selected occurrence-local
>    \(\Xi^-\) comparison with physical \(M_v\) and physical \(q\).
> 2. Its even restriction realizes the complete product-rule packet and
>    \(W\), for both mixed chart assignments and every relevant maximal
>    shore.
> 3. Its \(\beta=0\) connecting morphism is the physical Bockstein \(V\), and
>    the comparison is pointed, so the anchor conormal and scalar unit are
>    transported on the source algebra.
> 4. The construction covers all rootless residual tails; all inactive
>    normal, trace, horizontal-Rees, and intrinsic order-\(h\) faces; and the
>    simultaneous deleted-face-zero stratum.
> 5. Every non-lifting alternative is promoted to the actual
>    source-provenant terminal/Macaulay quotient. Its generator or left
>    separator is therefore a physical terminal contradiction, not only a
>    class in a finite presentation cokernel.
> 6. The exhaustive branch output is either such a contradiction or an
>    active clean cap satisfying the exact homogeneous cap equation
>    \({\cal E}_{p,q}(K)=0\) and
>    \(s\kappa_0\kappa_1\kappa_2\ne0\).

**Conditional theorem.** If \(\mathsf{PAComp}(h)\) holds for every
\(h\geq3\), then (1) holds for every even \(N\geq6\).

**Proof.** If a decorated source with at least three colours exists, palette
projection gives an exact ternary aggregate source. Choose one of minimum
even order. Order six is excluded by SP-K6, so its order is at least eight.
Apply \(\mathsf{PAComp}(h)\). A terminal outcome contradicts the assumed
source. Otherwise it supplies the active clean cap required by SP-DESCENT,
which reconstructs a finite exact ternary decorated source on \(N-2\) sites.
This contradicts minimality. Hence no exact ternary source, and therefore no
source with palette at least three, exists. \(\square\)

The proof needs no new induction invariant. Exactness and the three-colour
palette are reconstructed by SP-DESCENT; minimality avoids any ambiguity
about iterating chosen charts. Equivalently, one may reselect the committed
maximum-anchor/minimum-support representative after each descent.

## Dependency audit

| Dependency | Status | What the global implication uses |
|---|---|---|
| Aggregate source model and palette projection | Proved in the mathematical spine | Reduces any palette \(D\geq3\) source to an exact ternary source; FORMALIZATION.md records remaining Lean work, not an extra mathematical hypothesis here |
| Maximum-anchor/minimum-support selection and curvature synchronization | Proved | Places the physical curvature line on a source representative |
| Automatic two-chart extraction | Proved | Supplies the common full-nine packet and tilted/direct-free alternative |
| Pointed \(k[\beta]\), \(\rho\)-equivariant comparison | **Assumed only at \(h=3\)** | The master note explicitly says “At \(h=3\)” and targets \(\Phi:U_{15}\to L_{h=3}\) |
| Uniform source-labelled prolongation | **Open** | Must construct the comparison on every intrinsic order-\(h\) packet; literal site suspension is expressly insufficient |
| Exhaustive rootless/inactive routing | **Open** | Must cover both mixed assignments, inactive normal/trace/Rees faces, and all maximal-shore cases |
| Simultaneous deleted-face-zero routing | **Open** | No theorem says a rootless source has some \(h_v\ne0\), or sends the all-zero stratum to a closed inactive/unit branch |
| Physical terminal promotion | **Open unless included in the assumed theorem** | A linear \(q\)-extension/Fredholm dichotomy is terminal only after identifying its quotient with the actual source-provenant terminal/Macaulay quotient |
| Comparison output \(\Rightarrow\) active-clean cap or contradiction | **Must be part of the assumed global theorem** | The local parity/Bockstein identities alone do not state this implication |
| SP-DESCENT | Proved | Turns one active clean cap into an exact ternary source on \(N-2\) sites |
| SP-K6 | Certified | Excludes the terminal six-site source |
| Minimal-order induction | Complete | SP-K6 plus uniform descent admits no nonempty set of bad even orders |

## The first unavoidable missing global implication

The shortest unsupported arrow is

\[
 \boxed{
 \begin{gathered}
   \text{one canonical pointed comparison at }h=3\\
   \not\Longrightarrow\\[-2pt]
   \texttt{SP-CLEAN-BRIDGE for every automatic packet at every }h\geq3.
 \end{gathered}}
                                                               \tag{2}
\]

The uniform-prolongation audit explains why ordinary site suspension cannot
fill (2): the terminal Macaulay degree, activity degree, and intrinsic
normal faces change with \(h\). The unified full-nine theorem is explicitly
uniform in \(h\), while its \(h=3\) grade split is labelled only a bounded
test.

There are then two independent scope guards even at the local-to-global
interface.

1. **Face-zero guard.** The five deleted-face values may vanish
   simultaneously. Curvature does not force one of them to be nonzero, and
   the simultaneous zero locus is not yet identified with the all-inactive
   branch.
2. **Terminal guard.** The six-term and pentagon alternatives prove a
   finite linear generator/separator dichotomy. The cited theorem itself
   says it does not manufacture the physical map, and its Fredholm separator
   becomes the missing annihilator only when the quotient is the
   source-provenant terminal/Macaulay quotient.

The pointed anchor law removes an anchor ambiguity once the comparison is an
actual pointed source-algebra map; it does not supply either guard or the
uniform prolongation.

## Certified-spine status

certification/BASELINE.md still records SP-CLEAN-BRIDGE as open, and
certification/SUPERSESSIONS.md contains no accepted replacement for that
dependency. Later local research commits therefore do not yet change the
certified global conclusion.

The separate Lean ledger still marks aggregation/source-palette exactness
and the literal \(k_{\max}\) identification as ready to formalize rather than
formalized. This is a mechanization tail: the committed prose descent proof
already reconstructs the finite decorated source and proves the palette
projection used in the conditional proof above.

## Verification

Run

~~~text
python3 computations/verify_global_assembly_after_h3_master_comparison_scope.py
python3 -O computations/verify_global_assembly_after_h3_master_comparison_scope.py
python3 -I -S computations/verify_global_assembly_after_h3_master_comparison_scope.py
~~~

The checker pins the literal \(h=3\) scope, the uniform-prolongation warning,
the terminal and face-zero guards, and the certified dependency ledger. It
also exhausts every subset of the even orders \(6,8,\ldots,20\): after
imposing the six-site obstruction and uniform \(N\mapsto N-2\) descent, the
empty bad-order set is the unique survivor. That finite exhaustion audits
the logical induction pattern; it is not a finite-order proof of the
conjecture.

Frozen ledger SHA-256:

~~~text
11fd5ec313498002fd3013883626a117d4d2bad22b72abfce605d352bf3283c0
~~~
