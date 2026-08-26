/- UNAUDITED — lane L1, generated. Orbit 26 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit26Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_26.cnf")

def orbit26CNF : CNF Nat :=
  orbit26Parsed.map (·.cnf) |>.getD []

theorem orbit26Parsed_ok : orbit26Parsed.isSome = true := by
  native_decide

theorem orbit26Unsat : orbit26CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit26CNF
    (include_str "../../artifacts/n8k4_26.lrat")
  native_decide

end LratProbe.Orbits
