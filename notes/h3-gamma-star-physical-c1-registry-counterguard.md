# The declared Gamma-star grammar is not yet the physical C1 registry

## Verdict

The degree-one census in `9ad603f` is exact for the free cellular grammar it
declares, but the present source definitions do not prove literal essential
surjectivity from the full physical complex.  There is not yet one executable
object

\[
 C^{\rm phys}_{1,\Gamma_*}
   \longrightarrow C^{\rm grammar}_{1,\Gamma_*}
\]

whose generators are enumerated by the census.  The code-level comparison is
instead:

```text
declared grammar:
    operation_census() has zero parameters and zero constructor calls;
    it returns 17 fixed records;
    the eight kappa normal forms are a formal I_8 basis.

largest executable named map:
    186 coordinates, 146 columns, rank 90;
    four direct-sum blocks;
    25 columns in the final 27-row cap block;
    the cross-word AugP2 source object is explicitly unconstructed;
    no literal kappa column is present.
```

Thus `9ad603f` proves

\[
 C^{\rm grammar}_{1,\Gamma_*}/
 (C^{\rm can}_{1,\Gamma_*}+C^{\rm dark}_{1,\Gamma_*})
   =\langle\kappa_{0012},\ldots,\kappa_{2112}\rangle,
\]

but it does not yet prove the same statement after replacing `grammar` by
`phys`.  This is a source-interface gap, not an additional ordinary-syzygy
gap.

Exact checker:
[`verify_h3_gamma_star_physical_c1_registry_counterguard.py`](../computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py).

## 1. What the source definitions actually construct

The new checker imports and executes the constructors, rather than accepting
their prose scope pins.

The census function itself has the exact Python signature

```text
operation_census() -> tuple[17 records]
```

and its abstract syntax tree contains no call node.  Its class split is

```text
canonical       1
chi-dark        9
off-grade       6
kappa type      1.
```

The eight kappas arise only after the separate quotient routine constructs
the eight unit vectors indexed by the one-root neighbours

```text
0012, 0102, 0110, 0111, 0122, 0212, 1112, 2112.
```

This is a valid normal-form proof inside the declared grammar.  It is not an
enumeration of objects supplied by another physical-source constructor.

The largest actual named row map is independently rebuilt by
`verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py`.  It has

```text
block dimensions       108, 3, 48, 27
block column counts     19, 2, 100, 25
total coordinates       186
total columns            146
total rank                90.
```

The first 121 columns are in response or intermediate word/fine/repeated
summands and have literal zero projection to the cap `B/Eq` block.  The 25
cap columns have rank 23 in all 27 augmented rows and rank 7 in the eight
`B/Eq` rows.  Every one is killed by

\[
 \Psi=\frac14\delta\cdot(B-Eq),\qquad
 \delta=(1,1,-1,-1).
\]

Most importantly, the packaging constructor returns

```text
existing_AugP2_status.constructed_literal_source_object = false.
```

So the maximal executable map is deliberately not the cross-word physical
complex whose mixed interchanges would be the eight kappas.  The comparison
functor needed for essential surjectivity has no implemented domain yet.

## 2. Smallest exact counterguard

Copy the complete tag retained by the census:

```text
word               01211222
fine packet        six distinct 24-coordinate occurrence degrees
repeated shape     P3+K2
operation parent   response-to-AugP2 mixed orbit/K_Eq
window             2345 with literal occurrence labels
relative degree    1.
```

Adjoin one primitive source symbol `epsilon` with zero canonical
coefficient/PP shadow and full augmented boundary

\[
 d\epsilon=(B,Eq,\mathrm{target},W,\mathrm{ores},M,ainc,q,
             P_f,\mathrm{ridge},\eta,\sigma)
            =(\delta,0,0,0,0,0,0,0,0,0,0,0).       \tag{1}
\]

This is one literal 27-entry column.  Exact rational elimination gives

```text
full cap rank             23 -> 24
B/Eq projection rank       7 -> 8
q = M - ainc               0 = 0 - 0
Psi(d epsilon)             1.
```

At source-quotient level, the declared eight basis vectors have rank eight
in a nine-dimensional extension, while `epsilon` raises the rank to nine.
Hence it does not factor through canonical plus the eight declared kappas.
The guard is dimension-minimal: any failure of surjectivity has cokernel
dimension at least one, and (1) realizes one primitive integral dimension.

`epsilon` is **not** asserted to be a GHZ source operation.  Its role is
sharper: all executable interfaces used by the census are unchanged when it
is adjoined, because none accepts a physical generator registry as input.
Consequently those interfaces cannot prove that such a generator is absent.

## 3. Exact theorem still needed

The missing theorem should be stated against source data, not an elected
operation vocabulary:

> Construct a finite registry `Gen_phys(Gamma*)` containing every primitive
> physical total-degree-one source constructor whose differential lands at
> the full word/fine/repeated/operation/occurrence grade `Gamma*`.  Construct
> a chain- and augmentation-preserving comparison functor from that registry
> to the canonical cellular/bar grammar.  Then prove that every registry
> entry is canonical, `Psi`-dark, or one of the eight literal kappa
> instances.

Under this theorem, the result of `9ad603f` promotes immediately to literal
essential surjectivity.  Without it, the sentence “no independently
primitive noncellular operation is admitted” is the missing hypothesis
rather than its proof.

## 4. Shortest attack

The source construction can be made finite at `h=3` and the fixed fine
grade.

1. Construct the missing literal
   `11110000 -> 01211222` PP/AugP2 placement with its six `P3+K2` and six
   `3K2` faces.
2. Generate the eight one-root `K_Eq` interchange cells from that object,
   retaining word, fine, repeated, window and operation-parent tags.
3. Require each physical degree-one constructor (coefficient, PP/Hasse,
   reinsertion, Cartan/Weyl, cap, Eq, Tate/KS and mapping-cylinder) to emit
   its fixed-grade registry records.
4. Run one finite comparison: factor each boundary through the canonical
   image, test `Psi`, or identify it with one of the eight kappas.

There are then only two outcomes.  If every registered column factors or is
dark, essential surjectivity and the terminal reduction are proved.  The
first registered column with nonzero `delta.(B-Eq)` is instead the actual
bright filler whose remaining faces must be closed.

## Reproduction

```bash
python3 computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py --mode all
python3 computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py --mode interface
python3 computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py --mode guard
python3 -O computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py --mode all
python3 -I -S computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py --mode all
```

All modes return the frozen ledger

```text
b069c7e0061f080507e3538288e57b20b2f4640f0b61898b9cee2333a832c53b
```
