# Gate II is one fan-grade physical odd comparison from closure

## Verdict

The normalized active-fan coloop gate is **not yet unconditional**, but the
remaining statement is now singular.  After composing `32ce01c`,
`7a3ad78`, and `99f926a` with the finite saturation and target-augmented
Cartan theorems, there is no separate carrier, anchor, Hall-orbit, or
termination problem.

The one missing theorem is:

> **Fan-grade physical odd comparison.**  For every trapped carrier packet
> supplied by the complete-row coloop pivot, construct a source-valid
> fine/word/common-tail preserving map
> \[
>                         J_0\Phi=A J,
> \]
> from the fan-coloop packet to the canonical endpoint-odd packet, and
> identify on both domains the literal physical rows
> \[
>                         q=M-a.
> \]
> Every retained Cartan corner and protected readout must belong to this one
> complete packet.

The ambient physical Cartan prism supplies a marked odd occurrence, but it
does not prove this complete comparison.  In particular it does not by
itself identify all coefficient multipliers, fine labels, response rows,
and anchor-incidence contributions of the desired `U/V` packet.

Checker:
[`verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py`](../computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py).

## What is already complete

### 1. Physical carrier and Hall-shore typing

For a pure-colour coloop edge with nonzero cell `alpha`, `32ce01c` proves

\[
                  \alpha U_i-d_iV_i=\alpha.           \tag{1}
\]

Thus every other target channel contains a literal pure or two-site-mixed
matching omitting the coloop.  Its matching skeleton, common residual `q`,
endpoint partners and orientation, response heads, fine word, and remote
decorated tail are all physical.  An outside hole strictly enlarges the
current closed shore; a wholly trapped packet physically types that shore.

### 2. Finite termination

The `K6` hole closure has `446` closed ordered concepts and six symmetry
types.  Every outside physical hole strictly decreases

\[
                         15-|\operatorname {cl}(A)|.
\]

Starting from a nonempty shore there are at most fourteen strict growth
steps.  Once the shore is trapped, the proof applies the odd comparison
alternative once; it does not restart saturation by choosing another
witness.  Hence no additional support or reselection potential is needed
after the missing comparison is supplied.

### 3. Packet disagreement

Given the physical `Phi` and literal `q=M-a` rows, `7a3ad78` makes packet
agreement exhaustive:

\[
 [q-q_0\Phi]\ne0
   \quad\Longrightarrow\quad
   \text{physical q witness / typed saturated exit},
\]

while a zero class is removed by a protected-row correction.  The physical
signless pivot and corrected odd row then give `(S+D)/2` and `(S-D)/2`, the
two oriented target-bearing affine rows.  There is no third mismatch arm.

### 4. Every target circuit lands

Choose a minimum target circuit in the resulting complete affine packet.
The placed Cartan column has the exact internal/external alternative.

* If the physical anchor is bright, the rectangular theorem gives the
  two-rank landing for an external Cartan column and an adjusted unit-Cartan
  kernel for an internal one.
* If the physical anchor is dark, `99f926a` writes
  `h_phys=lambda A_D`.  The bordered residual either gives the normalized
  target-dark separator, the ordinary external cokernel separator, or an
  anchor-compatible unit-Cartan kernel.

Thus the independent condition `h_phys(k)!=0` has disappeared from the
exhaustive Gate-II assembly.  It remains relevant only if one insists on
the bright two-rank outcome rather than accepting the physical separator or
unit-kernel arms.

### 5. The later normalized coloop chain

Once the endpoint/common-`q` target-coloop packet is reached, the committed
`h=3` chain already consumes the old `C6/C8`, diagonal-return,
punctured-`C4`, and conjugate double-coloop labels.  These are not additional
residual theorems.

## Exact branch map

```text
active-fan pure-colour coloop
        |
        v
complete-row omit-coloop carrier (1)
        |
        +-- hole outside closure -> strict finite saturation growth
        |
        `-- trapped physical shore
                |
                `-- MISSING fan-grade physical Phi and q=M-a typing
                        |
                        +-- q defect nonzero -> typed exit/generator
                        |
                        `-- q defect zero -> protected S/D split
                                                  |
                                                  v
                                         minimum target circuit
                                                  |
                       +--------------------------+------------------+
                       |                                             |
                 anchor bright                                  anchor dark
                       |                                             |
             rank-two or unit kernel                  separator or unit kernel
```

Every branch below `Phi` is terminal in the already accepted localized
source/Fitting/relative alternatives.  The single open arrow is the
construction of `Phi` itself.

## Scope and verification

This is a scoped assembly of pinned local theorems.  It neither constructs
the fan-grade comparison nor proves global entry from an arbitrary
maximum-anchor/minimum-support source into an active fan.

Run

```text
python3 computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py
python3 -O computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py
python3 -I -S computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py
```

Frozen ledger SHA-256:

```text
bd21d3fff8fe163241ab5fa5b8610028a5aeb1c0137ba9844293d7ca0049793a
```
