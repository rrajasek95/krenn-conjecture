/- UNAUDITED — lane L1, generated. Orbit 75 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit75Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_75.cnf")

def orbit75CNF : CNF Nat :=
  orbit75Parsed.map (·.cnf) |>.getD []

theorem orbit75Parsed_ok : orbit75Parsed.isSome = true := by
  native_decide

theorem orbit75Unsat : orbit75CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit75CNF
    (include_str "../../artifacts/n8k4_75.lrat")
  native_decide

end LratProbe.Orbits
