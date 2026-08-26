/-
UNAUDITED — lane L1, staged 2026-08-20, pinned HEAD f9a3bd6.

Replay of orbit 0 of the 87 N=8 diagonal case refutations.

  artifacts/n8k4_0.cnf   5592 variables, 13740 clauses
                         (byte-identical to
                          computations/unaudited-promotion-diag-2026-08-20/
                          certified_package/orbits/n8k4_0.cnf)
  artifacts/n8k4_0.lrat  262 KiB, produced by
                          drat-trim n8k4_0.cnf n8k4_0.drat -L n8k4_0.lrat
                         in BACKWARD mode, independently re-checked by
                         drat-trim's own `lrat-check` (`c VERIFIED`).

`Reflect.verifyCert_correct` is the soundness theorem of Lean's standard LRAT
checker: it is proved in the kernel. Only the *execution* of the checker is
delegated, here by `native_decide`. See Kernel.lean for the kernel-only
variant and BUILD-STATUS.md for the measured comparison.
-/

import LratProbe.CnfCheck

namespace LratProbe

open Std.Sat
open Std.Tactic.BVDecide

/-- Orbit 0 of the N = 8 diagonal case ledger, parsed from DIMACS. -/
def orbit0Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../artifacts/n8k4_0.cnf")

def orbit0CNF : CNF Nat :=
  orbit0Parsed.map (·.cnf) |>.getD []

/-- The DIMACS file really is well formed: the header count and every literal range check out. -/
theorem orbit0Parsed_ok : orbit0Parsed.isSome = true := by
  native_decide

/-- The refutation. -/
theorem orbit0Unsat : orbit0CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit0CNF
    (include_str "../artifacts/n8k4_0.lrat")
  native_decide

end LratProbe
