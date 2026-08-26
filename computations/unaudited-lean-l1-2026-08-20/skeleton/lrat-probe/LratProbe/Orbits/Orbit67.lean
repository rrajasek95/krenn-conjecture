/- UNAUDITED — lane L1, generated. Orbit 67 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit67Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_67.cnf")

def orbit67CNF : CNF Nat :=
  orbit67Parsed.map (·.cnf) |>.getD []

theorem orbit67Parsed_ok : orbit67Parsed.isSome = true := by
  native_decide

theorem orbit67Unsat : orbit67CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit67CNF
    (include_str "../../artifacts/n8k4_67.lrat")
  native_decide

end LratProbe.Orbits
