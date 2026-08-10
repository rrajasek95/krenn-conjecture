# The orbit-1 unit repairs form two successor palettes

## Exact repair census

For each of the eight ordinary one-class identities frozen by the first
closed exchange census, retain its target source polynomial and every
plus-binomial source row actually used by the pivot-ordered Laurent
reduction.  A repair mask is an inclusion-minimal set of absent cells that
activates a new matching in one of those source fibres.

The complete 135-cell-universe census is

```text
12 singleton masks + 111 double masks = 123 minimal repairs.
```

There are no larger inclusion-minimal masks.  Every double mask immediately
exports between 10 and 28 fresh singleton fibres, all using a newly added
cell.  This is exact propagation debt, not by itself an anchor-preserving
descent: later cells could still mate those singletons.

The twelve singleton masks occur on six of the eight supports and are only

```text
x25_01   or   x34_10.
```

They preserve the complete no-singleton shadow, producing twelve localized
38-cell successor charts.

## A uniform successor-unit family

All twelve successors are again coefficient-empty by an ordinary one-class
Laurent identity.  After exact source reconstruction their target rows have
only two coefficient palettes.

Eight are translated trinomials:

\[
                       -M+M+M=M.                       \tag{1}
\]

The other four are six-term rows.  Their six monomials reduce to two Laurent
classes; one class cancels with coefficient sum zero, while the other has
coefficient `+2` or `-2`:

\[
                 (\text{four-term zero class})\;\;\pm2N. \tag{2}
\]

Thus the phenomenon is a translated/factorized family rather than twelve
unrelated support computations.  Computing the complete repair masks of
these twelve identities gives

```text
16 singleton masks + 173 double masks = 189 successor repairs.
```

The remaining sixteen singleton masks show that (1)–(2) are a recurrence
atom, not yet a termination theorem.

## The first escape from the proposed trichotomy

The lexicographically first singleton repair is

```text
first orbit-1 closure + x25_01.
```

It has

```text
38 localized cells,
no forbidden singleton fibre,
no odd character dependency in its initial plus-binomial lattice,
no literal factorized shared-zero tensor pair.
```

The last check exhausts all six right-pair/complement-factor top candidates
and both off-diagonal response tensors before Laurent substitution.  Hence
this chart escapes the three *literal checked* alternatives “shared fan,
odd circuit, or singleton support descent.”  It is not a coefficient
counterexample: its replacement obstruction is the first trinomial unit
(1).

This distinction is load-bearing.  Hidden tensor quotients after nonlinear
substitution are not excluded, and the double-mask singleton debt is not
called descent without constructing the associated source modification.
What is proved is that a fourth local mechanism—successor one-class
collapse—is necessary in any exhaustive repair theorem.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_unit_repair_masks.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_unit_repair_masks.py
```

Both modes must print

```text
3946d0a9a46b2d330913dcd43b1e1bd5c10b358910e15a8884cb4b11e8b9a9d1
```
