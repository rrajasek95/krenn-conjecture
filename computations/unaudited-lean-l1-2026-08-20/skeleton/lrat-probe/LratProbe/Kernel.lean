/-
UNAUDITED — lane L1. Kernel-only variant of the orbit-0 replay.

`Reflect.verifyCert_correct` is a kernel-proved soundness theorem either way;
the question this file answers is whether its *hypothesis*
`verifyCert cnf lrat = true` can also be discharged by kernel reduction
(`decide`) instead of by the compiled runtime (`native_decide`). Doing so
would remove `Lean.ofReduceBool` and `Lean.trustCompiler` from the axiom
closure. See BUILD-STATUS.md for the measured outcome.
-/
import LratProbe.CnfCheck

namespace LratProbe

open Std.Sat
open Std.Tactic.BVDecide

def orbit0ParsedK : Option ParsedDimacs :=
  parseDimacs (include_str "../artifacts/n8k4_0.cnf")

def orbit0CNFK : CNF Nat :=
  orbit0ParsedK.map (·.cnf) |>.getD []

set_option maxRecDepth 100000 in
theorem orbit0UnsatKernel : orbit0CNFK.Unsat := by
  apply Reflect.verifyCert_correct orbit0CNFK
    (include_str "../artifacts/n8k4_0.lrat")
  decide

end LratProbe
