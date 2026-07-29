# The coupled adjacent \(E_{20}\) line has a quotient fourth-cut obstruction

## 1. Status and scope

Keep the seven internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
35&E_{10},
\end{array}
\]

let \(A_{23}=X\in\operatorname{Mat}_{3\times3}(\mathbb C)\) be arbitrary,
and take

\[
                         A_{25}=E_{00}+tE_{20}.            \tag{1}
\]

The exact verifier excludes a fourth complete cut \(z\in\{0,1,5\}\) for
every \(X\) and every complex \(t\), with both boundary stars and
\(A_{67}\) arbitrary.  As for the companion \(E_{10}\) direction, the
moving stabilizer character is dependent:

\[
      \operatorname{wt}(t)=\operatorname{wt}(x_{20})-\operatorname{wt}(x_{00}),
                                                            \tag{2}
\]

with invariant \(\lambda=t\,x_{00}/x_{20}\) on the fully nonzero stratum.
Every case keeps \(t\) as an ordinary polynomial variable; each
certificate is a unit ideal over \(\mathbb Q[t]\) or
\(\mathbb Q[t,\lambda]\) and therefore covers every complex parameter
value, including \(t=0\) and every cross-ratio value.

An [independent clean-room reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-20-fourth-cut-obstruction-independent-audit.md)
rebuilds the partition, killed sets, affine interpolation, expanded
normals, lock functionals, and all unit ideals under different orderings.
The result is therefore promoted as an audited local theorem.

This remains a local statement for the displayed fixed six-site interior.
It does not allow arbitrary \(A_{25}\), and it does not prove the global
Krenn conjecture.

The consolidated primary verifier is

- [the \(E_{20}\) exact verifier](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_20_fourth_cut_obstruction.py),

sharing the
[coupled-quotient system builder](../computations/derive_three_cut_internal_23_adjacent_25_coupled_quotient_systems.py)
and the
[cross-ratio direction scan](../computations/explore_three_cut_internal_23_adjacent_25_crossratio_directions.py)
with the \(E_{10}\) theorem.

## 2. Direction geometry

Exact endpoint-ordered enumeration gives

\[
 |T_{20}|=35,\qquad
 (|T_{20}\cap R_{ab}|)_{ab}=(0,0,0,0,0,0,9,9,12),\qquad
 T_{20}\cap U_+=\emptyset,                                  \tag{3}
\]

with dependent deleted pairs \(03,04,13,34\) and no diagonal target word
inside \(T_{20}\).  Edges \(23\) and \(25\) share site \(2\); every
tensor and insertion column is jointly affine in \((X,t)\) with no
\(x_{ab}t\) term.

The sampled unprojected census over all \(512\) supports shows why this
direction is harder than \(E_{22}\): plane normals at cuts \(0,1\) occur
on nine supports — the seven nonzero subsets of
\(\{x_{01},x_{11},x_{21}\}\) and, unlike every previously closed
direction, the two \(x_{00}\)-open supports

\[
 \{x_{00},x_{20},x_{21}\},\qquad
 \{x_{00},x_{02},x_{11},x_{20},x_{22}\}.                    \tag{4}
\]

Both extra supports contain \(\{x_{00},x_{20}\}\), so by (2) both are
coupled: their strata carry a genuine \(\lambda\) modulus, and the second
has character rank four on five cells, hence an additional invariant.
No constant full-cylinder minor can exist on any chart containing them.
The quotient architecture below absorbs all of this uniformly: the two
supports of (4) land in the finite charts
\(\texttt{outside\_x20\_d0\_b1}\) and \(\texttt{outside\_x20\_d6\_b0}\),
whose packets close with the plain expanded overspace at dimension three.

## 3. Case structure and parameter-uniform systems

The case structure, quotient audits, affine-interpolation audits,
expanded overspaces \(N^{+}_z\), and lock functionals are exactly those
of the \(E_{10}\) theorem, built by the shared library for the direction
cell \((2,0)\): five old-locus classes, \(27\) finite outside charts, and
one \(\mathbb Q[t,\lambda]\) chart on the circuit
\(x_{12}+x_{21}=x_{11}+x_{22}\).  The verifier re-proves for this
direction the coupled-character identity (2), the moving-block geometry
(3), the literal eight-site boundary identity, the \(32+480\) partition
census, the killed-cell and member invariance audits at both parameter
specializations, membership of the projected direct tensor in every
overspace, and the exclusion of both selected diagonal targets from
every overspace span.

## 4. Exact ledger

All \(33\) cases close for every final cut: \(99\) case/cut systems,
\(39\) distinct Singular programs, every one with reduced basis \([1]\)
over characteristic zero.  Only the circuit chart needs lock rows; its
three systems have \(1932\), \(1908\), \(1976\) generators over
\(\mathbb Q[t,\lambda]\) with expanded-overspace dimensions \(3,3,5\).
Every finite chart closes with the plain overspace packet and colour pair
\((1,2)\), except \(\texttt{old\_no\_x00}\), which uses \((0,2)\).  The
frozen configuration ledger has SHA-256

    c3adc733e5ae2003f8b5a79987edc97106fb27524f817fca04443ab34ee7335e

and every program hash is pinned in the verifier.

## 5. Reproduction and audit status

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_20_fourth_cut_obstruction.py

The default run re-derives every audit listed above, all frozen program
hashes, and reruns all \(39\) distinct characteristic-zero programs.  It
must end with

    A23 arbitrary plus A25=E00+tE20 local fourth-cut obstruction: PASS
    coupled character wt(t)=wt(x20)-wt(x00); t kept symbolic: PASS
    512 masks partitioned 32+480; five classes, 27+1 outside charts: PASS
    99 case/cut systems, all exact characteristic-zero units: PASS
    every unit ideal is over Q[t(,lam)]: covers all complex t: PASS
    endpoint order, shared stars, ordered fibres, arbitrary A67: PASS

With this theorem and its \(E_{10}\) companion, all eight one-cell
affine directions \(A_{25}=E_{00}+tE_{cd}\) on the fixed repaired
interior are closed.  The next finite extensions in this model are a
two-dimensional affine slice in \(A_{25}\), an internal edge disjoint
from \(23\) where genuine mixed \(Xt\) terms appear, or the replacement
of the fixed interior altogether.
