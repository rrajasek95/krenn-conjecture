# The four-cube descent defect needs a φ-surviving edge-degree-zero term

The fourth-Hasse cone audit
[`h3-full-hasse-cone-d4-descent-obstruction.md`](h3-full-hasse-cone-d4-descent-obstruction.md)
constructs the formal chain \(n_I=s_I-T\) with \(dn_I=Yw\), zero target and
zero cap residue, and identifies the exact obstruction to physical
descent: the diagonal projection has chain-map defect

\[
                     (H_0-u)\,e_0,                             \tag{1}
\]

and no target-zero repair exists in the two-row span, since
\(bH_m=H_0-u\) has no polynomial solution (its equation (26)).

This note extends that obstruction to every row family satisfying two
checkable hypotheses, covering all 6560 mixed reset rows **and** the
φ-surviving denominator \(a=0\) columns at once.  An earlier draft titled
this result "invisible to the entire row space" and claimed no
φ-surviving row had been proposed; an independent audit refuted both (the
denominator \(a=0\) columns are φ-surviving generators of the same cone)
and supplied the edge-degree argument that genuinely covers them.  This
version states the corrected theorem.

Krenn's conjecture remains open.  Nothing here changes the certified
spine.

## 1. The specialization and the two facts

Let \(\varphi\) be the **pure-colour specialization**: the ring
homomorphism sending every edge variable whose colour pair is not
\((0,0)\) to zero, and fixing the pure edges and the homogenizing \(u\).

**A.**  For every one of the 6560 mixed words \(c\), every monomial of the
direct-free hafnian \(H_c\) contains a mixed-colour edge, so
\(\varphi(H_c)=0\).  (A mixed word has a site \(s\) with \(c_s\ne0\), and
the matching edge covering \(s\) carries that colour at its
\(s\)-endpoint.)  The checker sweeps all \(6561\times90\) monomials; since
the colours are assigned from the word by construction, this sweep
re-derives a definitional fact — the content of the note is the theorem
below, not the sweep.  The all-\(1\) and all-\(2\) pure words fall under
**A** (their edges carry colours \((1,1)\)/\((2,2)\)) and, like every
reset row in this model, carry target zero.

**B.**  Every monomial of \(H_0\) is pure of edge-degree 4, and the
fourth-Hasse defect \(B=H_0-u\) is fixed by \(\varphi\) (checked through
that module's own `kill_mixed_variables`) and contains the standalone
monomial \(-u\) of **edge-degree 0**.  Its edge-degree support is exactly
\(\{0,4\}\).

## 2. The theorem

> Let \(\{\rho_i\}\) be any family of **target-zero** physical rows whose
> \(e_0\)-boundary coefficients \(\beta_i\) satisfy: every monomial of
> \(\varphi(\beta_i)\) has edge-degree \(\ge1\).  Then no chain
> \(x=a\,r_0+\sum_ib_i\rho_i\) with target zero has \(e_0\)-boundary
> \((H_0-u)e_0\).

*Proof.*  In the fourth-Hasse model the target is \(R\)-linear — the
polynomial coefficient of \(r_0\)
(`target_of_hasse_chain`, `verify_h3_full_hasse_cone_d4_descent_obstruction.py:239-241`) —
so target zero forces \(a=0\) identically.  Then every monomial of

\[
 \varphi\Bigl(\sum_ib_i\beta_i\Bigr)=\sum_i\varphi(b_i)\varphi(\beta_i)
\]

has edge-degree \(\ge1\), while \(\varphi(H_0-u)=H_0-u\) contains \(-u\)
of edge-degree \(0\).  \(\square\)

Both hypotheses are load-bearing.  Without target-zero on the \(\rho_i\),
a row with target \(t\ne0\) admits \(a=-b\,t\ne0\) and the argument
fails.  Without the edge-degree bound, a φ-surviving constant would
reach \(-u\) directly.

## 3. Who is covered

* **All 6560 mixed reset rows** \(H_c\,e_0\), with arbitrary polynomial
  coefficients and with or without corrections whose \(e_0\)-components
  die under \(\varphi\): they are φ-null by **A**, satisfying the
  hypothesis vacuously.
* **The denominator \(a=0\) columns.**  The complete denominator
  presentation \(\delta(d_{s,a})=\sum_{c:c_s=a}
  \operatorname{Haf}(q_c|_{D\setminus\{s\}})e_c\) (fourth-Hasse (18)) has,
  for \(a=0\), an \(e_0\)-component equal to the **pure** face hafnian
  \(\operatorname{Haf}(q_0|_{D\setminus\{s\}})\): three monomials, all
  pure, all of edge-degree exactly 2 — verified for all five sites.
  These are genuine φ-surviving generators of the cited cone; they
  violate φ-nullity but satisfy the edge-degree hypothesis, so no
  combination of them reaches the \(-u\) term.  (Whether they carry
  target zero is not decided by any artifact; the edge-degree argument
  covers the \(e_0\) slot either way.)

For accuracy about the cited audit: the denominator *differential* lands
in the EqSystem rows \(e_c\); it is the proposed denominator
*attachment* that would send the top face to \(-Yw\) in the cap row, and
that audit checks only the \(e_m\)-projected support ladder (its (24)).

## 4. Consequence

The defect is reachable only by a row whose \(e_0\)-coefficient has a
φ-surviving **edge-degree-0** term — a \(q\)-zero unit.  Producing that
unit source-faithfully is exactly the Spencer-generator problem the
fourth-Hasse audit isolates (its (28)): the order-four generator
\(r_m[I]\) has terminal coefficient \(\partial_IH_m=1\), which is
precisely such a unit, and it exists only in the prolonged complex.  So
the route's remaining task is unchanged and now sharper: a source-valid
fourth Hasse–Schmidt/Spencer lift, or a proof that none exists.  See
[`h3-source-valid-tower-first-obstruction.md`](h3-source-valid-tower-first-obstruction.md)
for the first obstructions on that object.

## 5. Scope

1. Finite, \(h=3\), direct-free, bounded model of the fourth-Hasse audit,
   with that model's \(R\)-linear target convention (under an
   evaluation-style target the theorem as stated would not follow).
2. Facts **A**, **B**, and the denominator computation are verified
   exhaustively; the theorem is the displayed argument.
3. A row violating either hypothesis — nonzero target, or a φ-surviving
   edge-degree-0 boundary term — is not excluded.  Constructing the
   latter source-faithfully **is** the open problem.
4. This closes the row-space alternative under the stated hypotheses
   only.  It constructs no Spencer lift and does not prove Krenn's
   conjecture, which remains open.

## 6. Verification

Run

~~~text
python3 computations/verify_h3_descent_defect_row_space_invisibility.py
python3 -O computations/verify_h3_descent_defect_row_space_invisibility.py
python3 -I computations/verify_h3_descent_defect_row_space_invisibility.py
python3 -S computations/verify_h3_descent_defect_row_space_invisibility.py
python3 -I -S computations/verify_h3_descent_defect_row_space_invisibility.py
~~~

Runtime is under one second.  The checker sweeps all \(6561\times90\)
monomials for **A**, verifies the defect's \(\{0,4\}\) edge-degree support
and its \(-u\) coefficient through the fourth-Hasse module's own objects,
cross-checks that the two independent hafnian constructions agree **as
monomial sets** for both the mixed word \(m_8\) (which is required to
equal `HASSE.MIXED8`) and the pure word, computes the five denominator
\(a=0\) face hafnians and their edge-degrees, and binds the geometry into
the ledger through a content hash of all compared monomial sets.  Its
frozen ledger digest is

~~~text
10c3511560ee5c9b1693b08bd680dae3d333385bd0d458063a0d358a247d5022
~~~

Mutation-tested, including the three silent-pass mutations found by the
audit of the earlier draft: changing the fourth-Hasse module's
direct-free pair, its mixed word, or the base module's direct-free pair
now each raise (the monomial-set comparison catches them), as do flipping
the \(-u\) coefficient, inverting the set comparison, and demanding an
edge-degree-0 generator — all under both `python3` and `python3 -O`.
