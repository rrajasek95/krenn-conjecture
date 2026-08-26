/- UNAUDITED — lane L1, generated. Orbit 41 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit41Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_41.cnf")

def orbit41CNF : CNF Nat :=
  orbit41Parsed.map (·.cnf) |>.getD []

theorem orbit41Parsed_ok : orbit41Parsed.isSome = true := by
  native_decide

theorem orbit41Unsat : orbit41CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit41CNF
    (include_str "../../artifacts/n8k4_41.lrat")
  native_decide

end LratProbe.Orbits
