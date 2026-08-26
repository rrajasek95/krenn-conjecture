/- UNAUDITED — lane L1, generated. Orbit 25 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit25Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_25.cnf")

def orbit25CNF : CNF Nat :=
  orbit25Parsed.map (·.cnf) |>.getD []

theorem orbit25Parsed_ok : orbit25Parsed.isSome = true := by
  native_decide

theorem orbit25Unsat : orbit25CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit25CNF
    (include_str "../../artifacts/n8k4_25.lrat")
  native_decide

end LratProbe.Orbits
