# Exact referee: the 16-coordinate `Q` is not a matchgate signature

Status: **UNAUDITED exact three-mode PASS**.

## Verdict

The polarized 16-coordinate object `Q=(Q_s)_{s\in\{0,1\}^4}` is an
ordinary four-site tensor covariant, not a matchgate/pure-spinor signature.
The distinction is structural, not an artifact of the two frozen examples:
the polynomial map from six arbitrary `2x2` edge blocks (24 parameters) to
the 16 `Q_s` has exact Jacobian rank 16 over `Q`, hence is dominant.
Consequently `Q` obeys no universal nonzero polynomial equation, in
particular no universal Grassmann--Pluecker/Cartan quadric.

## Literal frozen-example checks

In lexicographic bit order the even arity-four pure-spinor quadric used here
is

```
q0000*q1111 - q0011*q1100 + q0101*q1010 - q0110*q1001.
```

* The frozen support-six family has support
  `{3,5,6,9,10,12}`, entirely even parity, but the quadric is exactly `4`
  in `Q[z]/(z^2+2z-1)`.  It therefore fails the matchgate equations despite
  passing parity.
* The frozen support-eight family has support
  `{1,3,4,5,6,9,10,12}`, of mixed parity, so it already fails the matchgate
  parity condition.  Its even-coordinate Cartan expression is independently
  exactly `4` in `Q(r,g)`, `r^2=2`, `g^2=65`, after the frozen specialization
  `u=v=w=t=1`.

## Generic covariance and dominance

Every monomial of `Q_s` chooses one clone at each of the four supervertices;
all 48 coordinate monomials were replayed.  Thus local `GL_2` changes act on
`Q` as on `V_0 tensor V_1 tensor V_2 tensor V_3`.

At the deterministic 24-entry integer point recorded in the JSON result, an
exact `16x16` Jacobian minor has determinant

```
-16002837332176992590143876032.
```

This proves generic rank 16.  Three additional deterministic controls give
ranks `15,16,16`; the rank-15 point is retained as a nongeneric control.

## Nearest theorem that actually applies

The standard arity-four matchgate/pure-spinor characterization -- definite
parity together with the single Cartan quadric -- applies here only as a
negative membership test.  General four-qubit tensor/SLOCC invariant theory
is the correct positive representation-theoretic setting, but dominance
means it supplies invariants rather than identities vanishing on all `Q`.

Proposition 1.2 of `notes/pairwise-matchgate-compatibility.md` concerns the
full normalized transversal chart as a paired restriction of a Pfaffian
signature on twice as many nodes.  It does not identify this signless
four-bit Hafnian contraction `Q` with a standard matchgate signature.

Scope guard: this referee classifies `Q` by itself.  It does not exclude a
source-relative paired-Pfaffian identity that retains the six block matrices
or lower-sector data.

## Reproduction

Run:

```
./.venv/bin/python computations/unaudited-codex-Q-matchgate-referee-2026-08-21/audit_Q_matchgate_spinor.py
```

The standard, `-O`, and isolated `-I -S` executions all returned the same
logical result digest:

```
ea95dcde0b976318efdaa22d295065c1186035ece596b6a6f86596e078eec6cf
```

The script contains must-fire controls for both Cartan residuals, mixed
parity, and the exact rank-16 Jacobian minor.
