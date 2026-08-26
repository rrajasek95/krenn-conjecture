# Matrix-unit U7D complete same-multidegree target-block saturation exclusion

## Status

This is an exact **fixed-template eight-vertex exclusion** over `Q`, and hence
over every characteristic-zero field.  It answers the complete
same-multidegree question for the displayed endpoint-label support in the
preceding
[`U7D` sharpness theorem](MATRIX_UNIT_COMPLETE_PURE_TARGET_MOMENT_COMPATIBLE_ODD_HOLONOMY_SHARPNESS_THEOREM.md).

Let

```text
mu=(4,4,0)
```

be the multidegree of its three active-cycle words.  Among all `70` words of
this multidegree, the complete compatible matching fibres of the fixed `U7D`
label table have the exact distribution

```text
57 empty fibres;
10 singleton fibres;
 3 binomial fibres.
```

The three binomials are exactly the already-proved active cycle.  Every
singleton target equation is a nonzero physical matching monomial.  For
example, the word

```text
omega=00011011
```

has complete fibre

```text
F(omega)={01|24|37|56}.
```

Consequently its target-zero equation is

```text
lambda_01 lambda_24 lambda_37 lambda_56=0.          (1)
```

After localizing at all `28` physical amplitudes, the left side of (1) is a
unit.  Therefore the ideal obtained from the complete `(4,4,0)` target-zero
block, the pure normalizations, the cycle binomials, the definition of the
holonomy `H`, and every imported transport identity is the unit ideal.  Its
exact elimination ideal is

```text
I_same-degree intersect Q[H]=(1).                   (2)
```

This is decisive outcome **B** for the fixed `U7D` template: the complete
same-degree block rejects the support before a stronger holonomy polynomial
can arise.  It is not a contradiction in `H`, and it is not an arbitrary-
order matrix-unit exclusion.

The other two balanced binary blocks of the *unpermuted* table, with colour
pairs `{0,2}` and `{1,2}`, each have `70` empty fibres and contain no active
cycle.  If the entire endpoint-label table is globally colour-permuted, the
distribution `57/10/3` and the unit-ideal conclusion move to the permuted
copy of `(4,4,0)`.  These two statements must not be conflated.

At arbitrary order, equality of word multidegree is only a grading.  The
currently proved bridge transport preserves it but does not connect every
word in it.  A general continuation still requires a new theorem forcing a
Laurent-unit fibre or a nontrivial complete-block syzygy from an arbitrary
active cycle.  Aggregate fibres, cross-multiplicity coupling, pure-cofactor
branching or cycles, the deeper branch, the `r=1` matrix-unit branch, and the
global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Fixed label support and complete word block

Use vertices `0,...,7` and the complete endpoint-label table from `U7D`:

```text
01=(0,0)  02=(0,0)  03=(0,0)  04=(0,0)
05=(1,2)  06=(1,1)  07=(2,2)

12=(0,1)  13=(0,0)  14=(1,0)  15=(1,1)
16=(2,2)  17=(0,0)

23=(1,1)  24=(0,1)  25=(2,2)  26=(0,0)
27=(2,0)

34=(2,2)  35=(0,1)  36=(1,0)  37=(1,1)

45=(0,0)  46=(1,1)  47=(1,1)

56=(0,1)  57=(1,1)

67=(1,1).
```

The signs used by the sharpness specialization are not part of the fibre
support.  For this theorem, assign an independent nonzero variable
`lambda_ij` to every physical pair.  If `chi` is a word, let

```text
F(chi)={physical perfect matchings inducing chi},
C_chi=sum_(M in F(chi)) lambda(M),
lambda(M)=product_(ij in M) lambda_ij.               (3)
```

Define the complete same-multidegree word set

```text
W_mu={chi in {0,1,2}^8:
      |chi^(-1)(0)|=4, |chi^(-1)(1)|=4,
      |chi^(-1)(2)|=0}.                             (4)
```

Thus `|W_mu|=binomial(8,4)=70`.  The requested complete target-zero block is

```text
C_chi=0 for every chi in W_mu.                       (5)
```

Words with empty fibres contribute the tautology `0=0`; they are retained
in the count so that (5) is genuinely complete.

## 2. Exact fibre certificate

The complete nonempty part of (4) is the following table.  No signs are
attached to the monomials; each compatible matching contributes coefficient
one to (3).

| word | complete compatible fibre |
|---|---|
| `00001111` | `01|24|35|67`, `02|13|46|57` |
| `00011011` | `01|24|37|56` |
| `00011101` | `01|24|36|57` |
| `00100111` | `04|12|35|67` |
| `00101011` | `03|12|47|56` |
| `00110011` | `01|23|45|67`, `04|12|37|56` |
| `00110101` | `04|12|36|57` |
| `01000111` | `02|14|35|67` |
| `01001101` | `03|15|26|47` |
| `01010011` | `02|14|37|56` |
| `01010101` | `02|14|36|57`, `04|15|26|37` |
| `10001110` | `06|17|24|35` |
| `10110010` | `06|17|23|45` |

### Theorem 1 (complete fixed-template census)

The table above lists every compatible matching in every word of `W_mu`.
In particular:

```text
empty fibres:     57;
singleton fibres: 10;
binomial fibres:   3.                               (6)
```

The binomial words are exactly

```text
chi_0=00001111,
chi_1=00110011,
chi_2=01010101.                                    (7)
```

### Proof

There are `105=(8-1)!!` physical perfect matchings.  Recursively pair the
least unused vertex with each larger unused vertex.  For each resulting
matching, the fixed endpoint labels determine exactly one word.  Retain the
matching precisely when that word has four zeroes and four ones.  The
resulting `16` matching records group into the `13` rows displayed above;
the other `57` words in (4) receive none.  This establishes both exhaustion
and (6).

The primary verifier performs this matching-first enumeration and compares
the complete result with the displayed certificate.  The no-import audit
instead loops over all `70` words and uses target-constrained least-bit
recursion to reconstruct each fibre.  The distinct routes agree on (6), the
three binomial words, and two different singleton unit certificates.

The `U7D` specialization assigns signs to `12`, `14`, and `24`.  On the
three binomial rows it gives one diagonal term of value `1` and one
offdiagonal term of value `-1`, recovering the preceding cycle equations.
The present census is stronger only in breadth: it classifies every word of
their multidegree for this one label table.

## 3. The exact Laurent ideal and elimination

Let

```text
L=product_(ij in K_8) lambda_ij
```

and work in

```text
R=Q[lambda_ij^(+/-1):ij in K_8,H].                  (8)
```

Use the imported cycle data

```text
E_0=24|35,  B_0=23|45,
E_1=12|56,  B_1=15|26,
E_2=14|36,  B_2=46|13.                              (9)
```

The holonomy definition in polynomial Laurent form is

```text
H lambda(E_0)lambda(E_1)lambda(E_2)
 -lambda(B_0)lambda(B_1)lambda(B_2)=0.              (10)
```

Let `I_same-degree` be generated in `R` by:

1. the three unique pure matching normalizations;
2. the three cycle binomials in (7);
3. equation (10);
4. every complete target equation (5); and
5. any exact identities obtained from the already-proved selected bridge
   transport, word-shore rematching, and active-core response data.

### Theorem 2 (saturation exclusion)

```text
I_same-degree=R,
I_same-degree intersect Q[H]=(1).                   (11)
```

### Proof

The complete equation for `omega=00011011` is (1).  Its left side has the
inverse

```text
lambda_01^(-1) lambda_24^(-1)
lambda_37^(-1) lambda_56^(-1)                       (12)
```

in `R`.  Multiplying the generator (1) by (12) gives `1`.  Hence the ideal is
the unit ideal.  Equation (11) follows immediately.

Equivalently, before localization let `J` be the corresponding ideal in
`Q[lambda_ij,H]`.  Then

```text
(J:L^infinity)=(1).                                 (13)
```

No Groebner basis, random specialization, or unrecorded denominator is
used.  The only excluded divisor is `L=0`, exactly the boundary leaving the
complete nonzero `r=1` torus.  Before saturation, (1) says that at least one
of `01,24,37,56` has zero physical amplitude; it does not say that `H`
satisfies a stronger polynomial.

The pure normalizations, cycle equations, transport identities, and (10)
are included to match the full requested subsystem, but they are not needed
for the unit certificate.  The complete same-degree block alone already
contains (1).

## 4. Closure under the currently proved operations

The distinction between four different notions of coupling is essential.

### 4.1 Proved transport closure

For the selected `U7D` data, the imported `U7B` bridge operations send the
three active words cyclically among (7).  Their incoming diagonal and
outgoing offdiagonal matchings are the two complete terms in their fibres.
The selected word-shore rematchings and active-core responses therefore
close on those three equations.

### 4.2 Same multidegree is not a proved operation

Every bridge transport preserves colour multiplicities.  The converse is
not proved: two words with the same multiplicities need not be joined by a
bridge sequence, rematching, or active-core response.  Thus the smallest
subsystem closed under the currently selected transport data is the
three-cycle subsystem, not all `70` equations.

Equation (5) is a deliberate complete-block enlargement required by the
target tensor, not an inference that every same-degree word is a transport
successor.

### 4.3 Shared variables are not a transport theorem

The singleton equations share many physical variables with the cycle.  For
example, (1) shares `24`, `37`, and `56` with cycle terms.  This algebraic
overlap does not prove a transport edge.  It matters here only because the
complete target system independently requires both equations.

### 4.4 Algebraic elimination

Once the entire target block is imposed, algebraic elimination is allowed
to use all its generators regardless of transport reachability.  The unit
certificate is such an elimination fact.  It is not a claim that the
singleton word is a fourth active-cycle vertex.

## 5. Colour permutations

For the endpoint labels exactly as displayed in Section 1:

```text
four 0 / four 1: 57 empty, 10 singleton, 3 binomial;
four 0 / four 2: 70 empty;
four 1 / four 2: 70 empty.                           (14)
```

The last two lines contain no supported physical matching and hence no
active cycle.  Their target equations are tautologies for this fixed table.

Now let `sigma` be any permutation of `{0,1,2}` and apply it to **every**
endpoint label in the table.  Matching compatibility commutes with this
global relabelling:

```text
F_(sigma(table))(sigma chi)=F_table(chi).            (15)
```

Therefore the `57/10/3` distribution and the Laurent-unit certificate move
to the multidegree obtained by permuting `(4,4,0)`.  All six global colour
permutations have the same saturation conclusion.  Equation (15), rather
than an unsupported symmetry of the unpermuted table, is the precise colour-
permutation statement.

## 6. Local, fixed-template, and arbitrary-order scopes

The scopes are:

```text
local order:             exactly eight vertices;
label support:           exactly the displayed complete U7D table;
physical amplitudes:     independent and nonzero after Laurent saturation;
word family:             all 70 words of multidegree (4,4,0);
field:                   Q, hence characteristic zero by base change;
complete-block ideal:    unit ideal;
holonomy elimination:    unit ideal, not a stronger P(H);
global colour copies:    all six relabellings covered;
arbitrary active cycle:  not classified;
arbitrary order:         not classified.
```

The fixed table was already known not to be a witness because of the
outside-multidegree exposed word.  The new result gives a sharper and
earlier exit: its own active transport multidegree already contains ten
Laurent-unit target equations.  This is a genuine same-degree exclusion of
the template, not a new witness-locus theorem.

For an arbitrary active binomial cycle, the exact missing structural lemma
can be stated as follows.

> **Complete same-multidegree unit-or-syzygy lemma (open).**  From the label
> support and response data of an arbitrary complete nonzero `r=1` active
> cycle, prove that its complete same-multidegree target block either contains
> a singleton nonzero matching monomial, is inconsistent after saturation,
> or yields an exact finite family of binomial/aggregate syzygies whose
> elimination in the cycle holonomy can be decided.

Existing `U7A`--`U7C` results do not prove this lemma.  They provide one
word-preserving diagonal rematching for an active fibre and transport one
selected cofactor-active term while preserving multiplicity.  They do not
classify every compatible matching in every word of that multiplicity.

Thus the method outcome is:

```text
fixed U7D same-degree block:                     UNIT IDEAL;
fixed U7D support survives complete block:       FALSE;
stronger compatible polynomial P(H):             NOT APPLICABLE;
universal same-degree unit/syzygy mechanism:      UNKNOWN;
aggregate active fibres:                          UNKNOWN;
cross-multiplicity coupling:                      UNKNOWN;
pure cofactor branching / alternating cycles:    UNKNOWN;
deeper-blocker branch:                            UNKNOWN;
r=1 matrix-unit branch:                           UNKNOWN;
global Krenn--Gu conjecture:                      UNRESOLVED.
```

## Replay

```powershell
python claims/arbitrary-order/verify_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py
python claims/arbitrary-order/audit_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py claims/arbitrary-order/audit_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py claims/arbitrary-order/audit_matrix_unit_u7d_complete_same_multidegree_target_block_saturation_exclusion.py
```

The primary verifier imports only the predecessor's fixed table and matching
conventions, enumerates all `105` physical matchings once, compares the
complete `13`-row certificate literally, checks the upstream cycle and
holonomy, constructs a Laurent inverse for one singleton, and tests all six
global colour permutations.  The independent no-import audit hard-codes
decimal endpoint labels, visits each of the `70` words separately with a
target-constrained least-bit recursion, uses a different singleton unit
certificate, reconstructs `H` from separate numerator/denominator ledgers,
and independently checks the colour relabellings.  The scripts prove the
bounded census; the Laurent-unit and scope conclusions are the written
arguments above.
