# Orbit-85 extended-ring Nullstellensatz DAG and tail interface

## Outcome

The orbit-85 Boolean proof and all literal clause compilers now form one
replayable straight-line arithmetic certificate whose root is the empty-clause
polynomial 1. The certificate is not expanded into a static sum. It is frozen
as certificate_dag.json and independently replayed by replay_certificate.py.

The exact first off-diagonal coefficient is zero. Every source-amplitude leaf
used by this diagonal certificate has three even colour classes, while one
cross-colour matching edge would leave two colour classes with odd external
degree. The first possible tail order is therefore epsilon squared, and its
coefficient is frozen as a linearized copy of the same proof DAG with each
mixed diagonal amplitude leaf replaced by its explicit two-cross-edge
coefficient.

This remains an orbit-85 constructible-branch certificate. It is the requested
algebraic interface, not yet a global off-diagonal obstruction: its free-set
branch equations and complement localizers are held epsilon-constant. A
general off-diagonal arc need not preserve that branch.

## Arithmetic DAG

The antecedent ledger has the following exact census:

| antecedent type | count |
|---|---:|
| mixed diagonal amplitude rows | 1,638 |
| Boolean axioms | 5,592 |
| selector zero links | 384 |
| selector guarded inverses | 384 |
| Laplace witness definitions | 5,208 |
| inside-free product-zero equations | 448 |
| outside-free complement localizers | 7 |
| unguarded pure/witness opens | 9 |
| total | 13,670 |

These equations use 6,284 variables, have maximum input degree six, and have
39,949 expanded input monomial occurrences.

Backward LRAT trimming selects 502 original clauses. Each becomes a
compile_clause node pointing to its literal antecedents and one of the exact
A0/A1/A2/A3/A3g/C0/Cnz/Ch/FR/XF identities from the preceding audit. The
RUP proof then becomes:

| operation | count |
|---|---:|
| compiled core clauses | 502 |
| polynomial resolution nodes | 1,652 |
| polynomial weakening nodes | 5 |
| total macro nodes | 2,159 |

At a resolution node, if the right clause contains x and the left contains
not-x, the node stores the exact falsity factors missing from either side and
implements

    M_(right without x) * M_left
      + M_(left without not-x) * M_right
      = M_resolvent.

The stored factors omit overlaps, so the identity is integral and
characteristic-free. The 1,652 resolution macros correspond to 4,956
primitive multiply/multiply/add gates; the five weakenings add five
multiplications. The final node r:1652 carries the empty clause, whose
polynomial is 1.

Propagating the explicit compiler degrees through this unexpanded circuit
gives a conservative maximum arithmetic degree bound of 398. This is a bound
for the emitted naive straight-line composition, not a lower bound and not a
claim about the degree of a reduced static Nullstellensatz certificate.

## Off-diagonal jet

Use the endpoint-ordered substitution

    A_ij^(ab) = delta_(a,b) d_ij^a + epsilon T_ij^(ab),

with T present only when a differs from b. Selectors, inverse variables, and
constructible-branch witnesses are epsilon-constant.

For a word w and perfect matching M, its matching monomial has epsilon order
equal to the number k(M,w) of matching edges joining differently coloured
vertices. Hence

    F_w(A(epsilon))
      = sum_M epsilon^k(M,w)
          product_(same-colour ij in M) d_ij^(w_i)
          product_(cross-colour ij in M) T_ij^(w_i,w_j).

All 185 distinct source-amplitude leaves in the core have profiles 6+2+0,
4+4+0, or 4+2+2. In each case k=1 is impossible. Thus

    [epsilon] F_w(A(epsilon)) = 0

for every amplitude leaf, and therefore

    [epsilon] C(epsilon) = 0

for the entire certificate circuit.

The first possible coefficient is

    Tail2_w(d,T)
      = sum_(M: k(M,w)=2)
          product_(same-colour ij in M) d_ij^(w_i)
          product_(cross-colour ij in M) T_ij^(w_i,w_j).

For exactly two cross edges, the colour-incidence multigraph has even degree
at every colour, so the two edges are parallel between one pair of colours.
Equivalently, choose two vertices from each of two colour classes, use either
of their two cross pairings, and hafnian-match every remaining colour class.

The exact leaf census is:

| profile | distinct leaves | Tail2 terms per leaf |
|---|---:|---:|
| 6+2+0 | 22 | 90 |
| 4+4+0 | 9 | 72 |
| 4+2+2 | 154 | 30 |

There are 7,248 Tail2 monomial occurrences across the 185 distinct leaves.
The 502 clause compilers reference amplitude leaves 569 times, giving 20,208
weighted Tail2 monomial occurrences before the proof-DAG multipliers.

The order-two circuit C2 is explicit without expansion:

1. retain the same 2,159-node linear proof DAG and every stored multiplier;
2. replace each mixed_diagonal_amplitude antecedent by Tail2 for its three
   stored colour-class masks;
3. replace every other antecedent by zero.

With the convention used in certificate_dag.json,

    C(epsilon) = 1 + epsilon^2 C2 + O(epsilon^3),
    1-C(epsilon) = -epsilon^2 C2 + O(epsilon^3).

Thus the desired first-order tail map is identically zero; the first
informative diagonal-to-tail map supplied by this proof is the quadratic
circuit C2.

## Scope

This composition proves a unit identity in the extended exact orbit-85 branch
ring. The 448 inside-free equations and seven outside-free localizers encode
the branch and are not full arbitrary-matrix amplitude rows. Consequently the
quadratic jet is a branch-relative interface. Turning it into a global
statement requires either:

1. algebraically gluing the constructible free-set cover before taking the
   tail jet, or
2. proving that a hypothetical off-diagonal arc admits compatible branch
   witnesses to the required order.

Neither is inferred from the vanishing linear coefficient.

## Replay

    python3 computations/unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23/generate_certificate.py
    python3 computations/unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23/replay_certificate.py
    python3 -O computations/unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23/replay_certificate.py
    python3 -I -S computations/unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23/replay_certificate.py
