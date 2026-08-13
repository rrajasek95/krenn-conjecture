# The centered occurrence class has two uniform physical descent debts

## Exact verdict

At intrinsic response order (h), the selected response has (2h) sites
(inside the ambient (2h+2)-site descent packet) and

\[
                     N_h=2h(2h-1)(2h-3)!!             \tag{U1}
\]

literal occurrences.  Thus `90` is the (h=3) specialization, not the
uniform coefficient.  For the selected response head/word `11:110000`, the physical operations
currently available in the same coarse block do not realize

\[
                     c_f=90e_f-\sum_{M=1}^{90}e_M.     \tag{1}
\]

This failure occurs before fine-grade or terminal subtleties.  The
word-preserving site stabilizer has five occurrence orbits of sizes

```text
6, 24, 24, 12, 24,
```

and the marked occurrence lies in the six-element orbit.  Complete response
rows, target-compatible diagonal stabilizers, word-preserving permutation
bars, and response-head differences have rank-one projection—the total
90-term sum—in the selected head/word block.  The class (1) has both a
marked-within-orbit component and a separate orbit-marginal component.

Uniformly, physical descent of
(c_{f,h}=N_he_f-\sum_Me_M) would give the sufficient scaled anchor law
(N_h[du_f]=[du]).  Since (N_h) is a unit in characteristic zero, this
transports anchor visibility exactly as well as the unscaled law.  The
count and decomposition are uniform, but fixed-pair spectator extension
does not carry (c_{f,h}) to (c_{f,h+1}), even modulo the complete row.

Checker:
[`verify_h3_centered_occurrence_same_grade_physical_gate.py`](../computations/verify_h3_centered_occurrence_same_grade_physical_gate.py).

## 1. Uniform count and fixed-word orbit structure

For the word (11,0^{2h-2}), the stabilizer is
(S_2\times S_{2h-2}).  Put (d_h=(2h-3)!!).  The five occurrence-orbit
sizes are

\[
\begin{array}{c|c}
\text{endpoint/residual type}&\text{orbit size}\\ \hline
11&2d_h\\
10&2(2h-2)d_h\\
01&2(2h-2)d_h\\
00,\ \text{the two 1-sites paired}&
(2h-2)(2h-3)(2h-5)!!\\
00,\ \text{the two 1-sites split}&
(2h-2)(2h-3)(2h-4)(2h-5)!!.
\end{array}                                             \tag{U2}
\]

Their sum is (U1).  The marked orbit has size

\[
 s_h=2(2h-3)!!,\qquad r_h=N_h/s_h=h(2h-1).             \tag{U3}
\]

At (h=3), (U2) specializes to `6,24,24,12,24`.

### The exact h=3 block

Write an occurrence as

\[
                 (p\text{-site},s\text{-site},
                   \text{matching on the four residual sites}).
\]

There are `6*5*3=90` such occurrences.  The stabilizer of `110000` is

\[
                         S_2\times S_4,                \tag{2}
\]

of order 48.  Exact orbit enumeration gives sizes
`6,24,24,12,24`.  The marked occurrence

\[
 p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0]              \tag{3}
\]

is in the size-six orbit `O` consisting of the two endpoint orientations
at sites `0,1` and the three residual matchings on `2,3,4,5`.

Every occurrence covers every output site exactly once in the colour
prescribed by the word.  Hence every target-compatible diagonal stabilizer
has one common character on all 90 terms.  It scales the complete response
row and cannot split an occurrence.  Every permutation in (2) fixes the
complete sum.  Its group-bar boundary on that complete row is therefore
zero.

Changing response head does not help.  The four physical head rows occupy
four labelled direct-sum blocks.  A difference of two heads projects to a
multiple of the complete all-ones row in either block, not to an occurrence
difference.  Thus the selected-block image of all these operations has rank
one.

This is already a coarse-word no-go.  Refining to literal word/fine/repeated
grade cannot produce a class that is absent after forgetting those labels.
In fact, a nontrivial permutation in (2) generally transports the marked
fine label rather than returning an occurrence-local class in its original
grade.

## 2. The two independent pieces of `c_f`

Let `1_O` be the sum on the marked size-six orbit and let `1_(O^c)` be the
sum on the other 84 occurrences.  Then

\[
\begin{aligned}
 c_f={}&15(6e_f-1_O)\\
      &+(14\,1_O-1_{O^c}).                            \tag{4}
\end{aligned}

The first line is the genuinely occurrence-local debt inside `O`.  The
second is invariant under the word stabilizer but distinguishes the marked
endpoint-colour/matching orbit from the other four orbits.  Both have total
augmentation zero, and together with the complete all-ones row they have
rank three.

Two primitive integral covectors make the failure explicit.

* Put `5` on `f`, `-1` on the other five members of `O`, and zero outside
  `O`.  It kills the complete row and reads `450` on `c_f`.
* Put `14` on `O` and `-1` on `O^c`.  It kills the complete row and reads
  `1260` on `c_f`.

These are exact cokernel covectors in the occurrence presentation.  They
are not yet physical terminals: both distinguish terms inside one complete
source polynomial, and neither has been identified with physical
`q`, anchor incidence, target, residue, eta/sigma, or `W` on a source-valid
relative cell.

The same two-debt decomposition holds at every (h\ge3):

\[
 c_{f,h}=r_h(s_he_f-1_O)
       +\big((r_h-1)1_O-1_{O^c}\big).                 \tag{U4}
\]

The first term separates the marked occurrence inside its (s_h)-element
orbit.  The second separates that orbit from the other four orbit types.
Both have augmentation zero and are independent modulo the complete row.

## 3. The relative occurrence projector stops at its scalar face

The coefficient Euler product selecting (3) gives `P_f(R)=f`.  Centering it
against the complete response Euler gives

\[
                       90P_f(R)-R.                    \tag{5}

At the trapped source, `R=0` and `f!=0`.  Normalizing `f=1`, the zero-face
of (5) is exactly `90`.  Thus the centered projector has the desired
associated occurrence vector (1), but it is not a tangent/source operation.
Its first unavoidable boundary is

\[
                             90f(x).                  \tag{6}

This restates the source-validity obstruction without a free-occurrence
bar.  A positive relative projector must carry a same-grade physical scalar
or target face `-90f(x)` as well as (1).  Simply dropping (6), differentiating
the point equation, or using a complete-row permutation would assume the
desired comparison.

Uniformly the formal anchor decomposition is

\[
 N_hz_f-u=(N_hz_f-\sum_Mz_M)+(\sum_Mz_M-u).           \tag{U5}
\]

The centered Euler projector has scalar face (N_hf(x)).  Formula (U1)
changes with (h), so the (h=3) correction cannot simply be tensored with
spectator matching edges.

## 4. Fixed-pair spectator extension is not centered-class stable

Embed the (h)-occurrence module in the (h+1)-module by adding two fixed
spectator sites paired to each other and allowing neither new site to be a
response endpoint.  The image has (N_h) coordinates, while the new
complete packet has (N_{h+1}) coordinates.  On every coordinate outside
the embedded support, the embedded centered class is zero and
(c_{f,h+1}) is `-1`.

This mismatch cannot be repaired by the complete row.  If

\[
 \lambda\,\iota(c_{f,h})+b1=\mu c_{f,h+1},             \tag{U6}
\]

an outside coordinate gives (b=-\mu).  An embedded unmarked coordinate
then gives (lambda=0), and the marked coordinate gives (mu=0).  Thus
(U6) has only the zero solution.  The checker verifies the first instance
(N_3=90<N_4=840) directly.

This does not exclude a uniform transfer cell.  It proves that such a cell
must resolve the new endpoint placements and new residual matchings; a
local six-site cell with one fixed spectator factor is insufficient.

## 5. Why the occurrence cokernel is not already a terminal

An arbitrary augmented cokernel functional is not one of the accepted
Fredholm terminals.  In the smallest guard, the complete response row has
zero target/residue/physical-terminal projection while either centered
occurrence covector above detects (1).  This is consistent because the
covectors live on tagged occurrences, not on the complete physical source
domain.

There is, however, no additional terminal theorem to invent once a physical
relative occurrence cell exists.  The pinned physical readout is

\[
                 \Lambda=\sum_{i=1}^{6}m_i-\operatorname{ainc}.   \tag{7}

For a complete augmented correction map `J`, the existing exact dichotomy
is:

```text
Lambda nonzero on ker(J)  -> normalize the kernel vector to the relative generator;
Lambda kills ker(J)       -> Lambda descends as the Fredholm separator.
```

Therefore failure of zero indeterminacy is already the positive generator
branch.  The missing datum is not another separator; it is the physical
typing of (7) on the new same-grade occurrence comparison.  A natural
occurrence dual becomes terminal only after proving that its difference
from (7) is a complete protected-row coboundary.

That conclusion is local to the physically typed (h=3) packet.  The
uniform count does not prove either global PAComp(h) clause:

* the simultaneous deleted-face-zero stratum is not routed.  The pinned
  curvature guards have nonzero curvature and all five (h_v=0), so
  curvature alone does not force a face-open chart;
* an occurrence cokernel dual is not automatically the
  source-terminal/Macaulay Fredholm covector.  The linear kernel/separator
  alternative becomes terminal only after that physical quotient is
  identified.

In particular, fixed-pair spectator extension promotes neither the
centered cell nor its physical `Lambda` typing to all (h).

## Minimal positive theorem

> **Uniform same-grade centered occurrence comparison.** For every
> (h\ge3), construct one source-valid relative cell in the selected
> word/fine/repeated grade whose occurrence boundary is (c_{f,h}), whose
> scalar/target boundary cancels (N_hf(x)), and whose transfer includes all
> endpoint-placement and residual-matching orbits.  Identify its physical
> `q`/anchor dual with the source-provenant terminal quotient, and include
> the simultaneous deleted-face-zero routing.

Then (U4) need not be solved by two separate cells: one cell may carry both
debts.  At (h=3), the already proved `Lambda`-on-kernel alternative gives
either the relative generator or the Fredholm separator after physical
typing.  Combined with the symmetric target normal, the uniform boundary
yields `N_h[H]=Phi^*[h_Eq]`, closing Interface II.

## Scope

This proves the uniform occurrence count, five orbit types, two-debt
decomposition, scaled anchor coefficient, and failure of fixed-pair
spectator stability.  At (h=3) it proves the rank-one image of the listed
complete physical operations and the scalar face of the relative
projector.  It does not exclude a higher PP/Hasse occurrence-local cell,
construct its uniform transfer/scalar correction, route the simultaneous
face-zero stratum, or identify the centered occurrence covectors with the
source-provenant physical terminal.

Run:

```text
python3 computations/verify_h3_centered_occurrence_same_grade_physical_gate.py
python3 -O computations/verify_h3_centered_occurrence_same_grade_physical_gate.py
python3 -I -S computations/verify_h3_centered_occurrence_same_grade_physical_gate.py
```

Frozen ledger SHA-256:

```text
bea8d7cf46c393fe352dc553dcbb54f987dba8597290abb038135aaae3c08a73
```
