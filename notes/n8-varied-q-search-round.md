# Exact \(n=8\) varied-\(q\) search, round 1: a complete negative census

## 1. Region and sanction

The audit file's counterexample directive (Section 6, Priority 5, and
the sparse-advance rule "at least four new cells, vary \(q\) itself")
sanctions exactly the region searched here: all variations of the
polarized seed quadratic \(q\) by **four distinct cells outside
\(\operatorname{supp}(q)\)** with coefficients
\(t\in(\mathbb C^*)^4\), i.e.

\[
   Q=q+t_1e_1+t_2e_2+t_3e_3+t_4e_4,
\]

lifted against the unrestricted aggregate system
\(H_8(A)=\Delta_{8,3}\) and against the pair-cap variety
\(z=aq+4ps\).  The fixed-\(q\) affine-preimage theorem, the one- to
three-cell sparse families, and the compatible-triple censuses are all
recorded closures and were not re-searched.

## 2. Census of the four-cell region

All \(\binom{243}{4}=141{,}722{,}460\) quadruples were classified
exactly, by two independent implementations that agree perfectly: a
constructive Python census with an anchor-lemma completeness proof
([census driver](../computations/search_n8_varied_q_round_1_census.py))
and an exhaustive C scan re-deriving all debts from raw cell data
([scanner](../computations/search_n8_varied_q_round_1_exhaustive_scan.c)).

\[
\begin{array}{r|l}
140{,}488{,}938&\text{rejected by a singleton Laurent debt}\\
99&\text{support survivors, torus-inconsistent (the }z\text{-triple}\\
&\text{plus one compatible cell; hand-checkable)}\\
10{,}611&\text{cancellation families on explicit binomial loci}\\
1{,}222{,}812&\text{identically compatible }K_4\text{ quadruples}
\end{array}
\]

Every cancellation family satisfies \(zQ^{[3]}=\Delta_{8,3}\) on its
locus and carries an exact rational witness, certified end-to-end by
substitution and re-expansion over \(\mathbb Q\)
([witness verifier](../computations/search_n8_varied_q_round_1_aggregate_and_witness_verify.py)).
The four relation classes are \(8{,}811\) of type \(t_i+t_jt_k\),
\(1{,}377\) of type \(1+t_jt_k\), \(279\) of the new cross-cross type
\(t_it_j+t_kt_l\), and \(144\) with two simultaneous relations.

## 3. Aggregate emptiness

The literal unrestricted system \(Q^{[4]}=\Delta_{8,3}\) has **zero**
support-feasible quadruples in the entire region: proven by the full C
scan and independently by a constructive argument reducing to \(258\)
complete candidates, each failing padding-word cancellation.  No
four-cell variation of \(q\) reaches \(\Delta\) or any nonzero multiple
of it directly.

## 4. Pair-cap closure of all cancellation lifts

The \(1{,}233{,}423\) polarized families (cancellation families plus
compatible \(K_4\) quadruples) were tested against the pair-cap variety:

* \(1{,}216{,}345\) closed by the parameter-safe projective Gram-parity
  argument ([closure driver](../computations/search_n8_varied_q_round_1_paircap_closure.py));
  the ported four-tag argument reproduces the audited three-cell
  ledgers exactly, including the seven recorded survivors of that
  earlier round;
* the remaining \(17{,}078\) went to saturated characteristic-zero
  Singular ideals on their cancellation loci: **all \(17{,}078\) unit**,
  zero non-unit, zero timeouts or errors.

A deterministic stride-\(10\) subsample of \(1{,}709\) ideals was
re-verified by a clean-room reconstruction
([independent checker](../computations/search_n8_varied_q_round_1_ideal_independent.py))
that shares no expansion code with the primary driver: the element
\((aQ+4ps)Q^{[3]}\) is rebuilt by literal square-zero-algebra
multiplication, words are emitted in descending order, the variable
order is reversed, and the engine is slimgb.  Result:
\(1{,}709/1{,}709\) unit, none non-unit.

## 5. Conclusion and artifacts

**No counterexample candidate exists anywhere in the sanctioned
four-cell varied-\(q\) region**: the polarized escape survives the
thickening as \(1.23\)M exact cancellation families, but every family
misses the pair-cap variety, and the direct aggregate system is
support-impossible on the whole region.  This is falsification work in
the census sequence; it is not a uniform proof and does not bear on the
even-\(n\ge8\) upper bound route.

Machine-readable summary with artifact SHA-256 stamps:
[results JSON](../computations/search_n8_varied_q_round_1_results.json).
The job ledgers, full survivor list, and the \(17{,}078\)-line unit
ledger are archived compressed under
`computations/n8_varied_q_round_1_artifacts/` (the 75 MB compatible
projective ledger is summarized by its hash only).  The survivor
schema with the seed \(q\) is
[survivors JSON](../computations/search_n8_varied_q_round_1_survivors.json).

Next rounds in this sequence, per the same sanction: five-cell
variations, larger shared-block families, or joint \((q,z)\) variation.
