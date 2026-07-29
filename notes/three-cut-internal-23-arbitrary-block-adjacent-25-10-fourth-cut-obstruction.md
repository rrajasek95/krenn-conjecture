# The coupled adjacent \(E_{10}\) line has a quotient fourth-cut obstruction

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
                         A_{25}=E_{00}+tE_{10}.            \tag{1}
\]

The exact verifier excludes a fourth complete cut \(z\in\{0,1,5\}\) for
every \(X\) and every complex \(t\), with both boundary stars and
\(A_{67}\) arbitrary.  Unlike the five previously closed adjacent
directions, the moving stabilizer character is dependent:

\[
      \operatorname{wt}(t)=\operatorname{wt}(x_{10})-\operatorname{wt}(x_{00}),
                                                            \tag{2}
\]

so no independent normalization of \(t\) exists and the fully nonzero
stratum carries the invariant \(\lambda=t\,x_{00}/x_{10}\).  Every case of
the proof therefore keeps \(t\) as an ordinary polynomial variable.  Each
certificate is a unit ideal over \(\mathbb Q[t]\) or
\(\mathbb Q[t,\lambda]\), hence covers every complex parameter value,
including \(t=0\) and every cross-ratio value; no separate inheritance of
the \(t=0\) arbitrary-\(A_{23}\) theorem is needed, although the
\(t=0\) slice reproduces exactly that audited statement.

An [independent clean-room reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-10-fourth-cut-obstruction-independent-audit.md)
rebuilds the partition, killed sets, affine interpolation, expanded
normals, lock functionals, and all unit ideals under different orderings.
The result is therefore promoted as an audited local theorem.

This remains a local statement for the displayed fixed six-site interior.
It does not allow arbitrary \(A_{25}\), and it does not prove the global
Krenn conjecture.

The consolidated primary verifier is

- [the \(E_{10}\) exact verifier](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_10_fourth_cut_obstruction.py).

Its shared generator library is

- [the coupled-quotient system builder](../computations/derive_three_cut_internal_23_adjacent_25_coupled_quotient_systems.py),

and the reconnaissance that fixed the route is

- [the cross-ratio direction scan](../computations/explore_three_cut_internal_23_adjacent_25_crossratio_directions.py).

## 2. Why the full-cylinder route of \(E_{22}\) does not transplant

Exact endpoint-ordered enumeration gives the moving-block geometry

\[
 |T_{10}|=35,\qquad
 (|T_{10}\cap R_{ab}|)_{ab}=(0,0,0,9,9,12,0,0,0),\qquad
 |T_{10}\cap U_+|=2,                                        \tag{3}
\]

with dependent deleted pairs \(03,04,13,34\) and no diagonal target word
inside \(T_{10}\).  Edges \(23\) and \(25\) share site \(2\), so no
matching uses an \(A_{23}\) cell and the moving cell simultaneously;
every tensor and insertion column is jointly affine in \((X,t)\) with no
\(x_{ab}t\) term.

Two exact findings force a different proof shape than the audited
\(E_{22}\) theorem:

1. On the \(x_{00}\)-open chart with all eight other entries and \(t\)
   symbolic, the simultaneous four-cylinder representation matrix has
   rank \(167\), \(167\), \(170\) (cuts \(0,1,5\)) at the subspace
   \(X=E_{00}\), against \(176\) generically.  The insertion-column
   relation spaces jump on coordinate subspaces even though the
   intersection stays a line, so no constant \(176\)-minor exists on the
   full chart and the \(E_{22}\)-style certificate cannot be issued.
2. The sampled unprojected census over all \(512\) supports finds plane
   normals at cuts \(0,1\) exactly on the seven nonzero supports inside
   \(\{x_{01},x_{11},x_{21}\}\), and the exact stabilizer computation
   shows \(\operatorname{wt}(t)\) lies in the span of those three
   characters.  The exceptional strata of any full-cylinder treatment
   would therefore carry a genuine \(\mathbb Q[\lambda]\) modulus rather
   than the exact torus representatives available to \(E_{22}\).

The proof below instead upgrades the quotient architecture of the audited
\(E_{11}\) theorem to coupled directions.

## 3. Case structure

The \(512\) supports of \(X\) split exactly as in the audited
arbitrary-\(A_{23}\) and \(E_{11}\) theorems:

- the old five-cell locus (\(32\) masks inside
  \(\{x_{00},x_{01},x_{02},x_{11},x_{21}\}\)) partitions into five
  classes by \(x_{00},x_{11},x_{21}\) membership;
- the \(480\) outside masks partition by their first nonzero cell in the
  order \(x_{10},x_{12},x_{20},x_{22}\) into \(27\) finite retained
  charts and one \(\mathbb Q[t,\lambda]\) chart on the circuit
  \(x_{12}+x_{21}=x_{11}+x_{22}\).

Every case retains its nonzero cells at torus-normalized value one
(\(x_{21}=\lambda\) on the circuit chart), kills the \(35\)-coordinate
output blocks of all non-retained cells, and keeps \(t\) symbolic.  The
verifier re-proves mechanically, for every case and both parameter
specializations:

- adding any non-retained cell changes neither the projected word terms
  nor any of the six projected insertion-column spans (outside charts),
  and every old-locus class member reproduces its representative's
  projected data exactly;
- the retained-cell character matrices have full rank (the audited
  partition/torus audits of the base theorems are re-run verbatim), so
  the coupled relation (2) costs nothing: the torus element normalizing
  the retained cells merely moves \(t\), which stays symbolic.

## 4. Parameter-uniform necessary systems

All word terms and insertion columns are jointly affine in \((t,\lambda)\)
with no cross terms; the verifier asserts this exactly at probe points
\((1,1)\) and \((2,3)\) after interpolating from
\((0,0),(1,0),(0,1)\).  Two sound weakenings produce necessary systems
with rational coefficients in the stars and polynomial coefficients in
the parameters:

1. **Expanded overspace.**  For each final cut \(z\in\{0,1,5\}\), the
   parameter-independent space
   \[
    N^{+}_z=\bigcap_{w\in\{2,3,4,z\}}
      \operatorname{span}\bigl(\pi C_w(\theta_0),\ldots,
      \pi C_w(\theta_k)\bigr)
   \]
   over the affine specialization points contains the projected common
   normal at every parameter value, because every column at \(\theta\) is
   an affine combination of the specialized columns.  The projected
   direct tensor lies in \(N^{+}_z\) at every specialization, hence at
   every \(\theta\).
2. **Pointwise lock functionals.**  On the circuit chart the overspace
   alone is too coarse.  There, for each cut
   \(w\in\{2,3,4,z\}\), the verifier computes the full space of
   functionals \(\varphi(\theta)=\varphi_0+t\varphi_1+\lambda\varphi_2\)
   with \(\varphi(\theta)\cdot c(\theta)=0\) for every insertion column
   and every \(\theta\) (constant, linear, and quadratic coefficient
   equations), re-checks them at three probe points, and adds the rows
   \(\varphi(\theta)\cdot(\pi\beta_{ab}-\delta_{ab}e_a^{\otimes6})=0\).

For the selected two-colour packet the membership rows of \(N^{+}_z\),
plus lock rows where used, give one ideal per case and cut over
\(\mathbb Q[t(,\lambda),\text{stars}]\).  A solution of the full
three-colour fourth-cut system at any \((X,t)\) would specialize to a
common zero, so a unit ideal excludes the fourth cut on the whole case.

## 5. Exact ledger

All \(33\) cases close for every final cut: \(99\) case/cut systems,
\(49\) distinct Singular programs, every one with reduced basis
\([1]\) over characteristic zero.  Only the circuit chart needs lock
rows; its three systems have \(1876\), \(1868\), \(1964\) generators
over \(\mathbb Q[t,\lambda]\) with expanded-overspace dimensions
\(4,4,3\).  Every finite chart closes with the plain overspace packet,
with colour pair \((1,2)\) except \(\texttt{old\_no\_x00}\), which uses
\((0,2)\).  The frozen configuration ledger has SHA-256

    4e416cc3692242531735f9e5a66dbb4082a2bfdae3f938103a4580e045792abd

and every program hash is pinned in the verifier.

## 6. Reproduction and audit status

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_10_fourth_cut_obstruction.py

The default run re-derives the geometry, the coupled-character identity,
the literal eight-site boundary identity, the partition census, all
killed-cell and member invariance audits, the affine exactness probes,
the expanded normals, the lock functionals with their probe checks, and
every frozen program hash, then reruns all \(49\) distinct
characteristic-zero programs.  It must end with

    A23 arbitrary plus A25=E00+tE10 local fourth-cut obstruction: PASS
    coupled character wt(t)=wt(x10)-wt(x00); t kept symbolic: PASS
    512 masks partitioned 32+480; five classes, 27+1 outside charts: PASS
    99 case/cut systems, all exact characteristic-zero units: PASS
    every unit ideal is over Q[t(,lam)]: covers all complex t: PASS
    endpoint order, shared stars, ordered fibres, arbitrary A67: PASS

The independent audit reconstructs the partition, quotients, affine
interpolation, expanded overspaces, lock functionals, and all unit
ideals from fresh endpoint-ordered enumeration under different variable
and generator orders.  After this theorem and its \(E_{20}\) companion,
the adjacent one-cell frontier of the fixed repaired interior is closed
in all eight directions.
