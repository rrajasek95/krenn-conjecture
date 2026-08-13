# Matching interference preserves heads; Cartan supplies the transverse move

## Outcome

The proof has two genuinely different layers.

1. **Matching interference** controls cancellation, phase, common tails, and
   component potentials inside one output word.
2. **Cartan/Spencer transport** changes an output word and is therefore the
   first operation capable of repairing a deficient local head.

No amount of additional same-word matching enumeration can replace the
second layer.  Conversely, once one source-typed transverse Cartan connector
is attached to a minimal interference component, the rank-one-adjugate
theorem leaves only a Schur unit or an exact component potential.

Checker:
[`verify_matching_interference_head_invariance_cartan_gate.py`](../computations/verify_matching_interference_head_invariance_cartan_gate.py).

## 1. The fixed-word invariant

Fix an output word `w` and a physical site `v`.  Every perfect-matching
monomial in the complete coefficient `H_w` uses exactly one decorated edge
incident to `v`, and the local colour on that edge is always

\[
                              w_v.                     \tag{1}
\]

Changing the matching skeleton changes the neighbour and the opposite-end
colour, but never (1).  Therefore every linear combination constructed from

* common-tail `C4/C6/C8` exchanges;
* complete same-word matching rows;
* binomial SCC holonomy;
* a component-exact matching potential; or
* further contamination in the same coefficient

has zero projection to a local-head quotient transverse to `e_(w_v)`.

The `N=8` checker exhausts all `3^8` words, all 105 perfect matchings, and all
eight local sites: 5,511,240 site/matching occurrences.  The statement is
tautologically uniform in the even order; the census freezes the physical
source convention.

This explains the failed tempting shortcut through hybrid avoiding mates.
They vary the colours at the opposite ends of their new arms, while their
local heads at the two exceptional sites remain fixed.  Hybrid propagation
is powerful source-exhaustivity data, but it cannot by itself raise local
star rank.

## 2. The first transverse operation is word-changing

A one-site root move changes `w_v=a` to `c!=a`.  The local heads `e_a,e_c`
are independent.  The physical Cartan theorem proves, in the canonical
selected repeated grade, that this is not a formal target operation:

\[
                 X_{\rm src}H_w=H_{X_{\rm out}w},       \tag{2}
\]

and endpoint oddization kills the GHZ target defect.  Hence the Cartan prism
is a genuine relative cell in the complete physical principal-parts source
resolution.  It supplies exactly the type of word-changing connector which
same-word interference cannot produce.

The current theorem is canonical rather than global.  Extending (2) with
the required repeated-grade/readout typing to every critical component is
the main remaining construction.

## 3. Why one connector would close an interference component

Let `M` be a minimal zero-holonomy critical matching block.  Then

\[
       \operatorname{adj}(M)=\kappa c\ell^T,
       \qquad \operatorname{rank}M=n-1.                \tag{3}
\]

For a coordinate pure row `h` and a physically typed Cartan connector `g`,

\[
 \det\begin{pmatrix}M&g\\h^T&\alpha\end{pmatrix}
       =-\kappa(h^Tc)(\ell^Tg).                         \tag{4}
\]

Minimality makes `h^Tc` nonzero when `h` selects the marked matching class.
Thus:

* `ell^T g != 0` gives the localized Schur/Fitting unit;
* `ell^T g = 0` is equivalent to `g in im(M)`, so the connector is an exact
  component potential.

If the potential in the second branch is a dependence among complete
occupied physical columns, the pinned same-row theorem deletes support
anchor-safely.  If a contaminating term leaves the component, the typed
component grows and the interference test restarts.  If `g` is visible in
both deficient local-head quotients, it repairs transverse rank.

This is the prospective endgame theorem.  It is not another graph census:
it is a source-typing statement connecting (2) to the critical block (3).

## 4. Revised proof map

The shortest structural route is now:

```text
maximum anchors / minimum support
        |
        v
protected frame circuit through every occupied cell
        |
        v
literal hybrid propagation into a finite matching component
        |
        +-- odd holonomy ------------------------> source unit
        |
        `-- coherent even holonomy --------------> rank-one charge
                                                     |
                              physical Cartan connector
                                                     |
                  +------------------+---------------+
                  |                                  |
             nonzero charge                    exact potential
                  |                                  |
             Schur unit                  support deletion / typed exit
                                                     or transverse rank
```

After transverse four-good landing, the existing clean-cap descent reduces
the order and the six-site obstruction terminates the induction.

## 5. What this retires and what remains

Retired as proof targets:

* longer same-word `C4/C6/C8` support censuses for the purpose of restoring a
  head;
* the hope that more hybrid mates alone repair `(2,2,3,3)`;
* treating phase/source connectivity and transverse rank as one lemma.

Still open:

1. a **uniform componentwise Cartan attachment theorem** with complete
   matching-row, target, residue, and terminal typing;
2. a **potential-to-physical-dependence/exit theorem** on its dark branch;
3. the final **double-quotient visibility** or clean-cap landing when the
   connector exits rather than deletes.

The selected `h=3` Cartan packet, its complete activity census, and its
double-coloop conjugate closure are strong evidence for item 1.  The exact
same-head counterguard shows why the word-changing hypothesis cannot be
omitted.

## Verification

Run:

```text
python3 computations/verify_matching_interference_head_invariance_cartan_gate.py
python3 -O computations/verify_matching_interference_head_invariance_cartan_gate.py
python3 -I -S computations/verify_matching_interference_head_invariance_cartan_gate.py
```

Frozen ledger SHA-256:

```text
7fd4e54f63e0b2c27a623dc0b544392e4cd70cad84b8a6dc8cc296121fd6b443
```
