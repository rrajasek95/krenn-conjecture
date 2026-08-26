/- UNAUDITED — lane L1, generated. Orbit 51 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit51Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_51.cnf")

def orbit51CNF : CNF Nat :=
  orbit51Parsed.map (·.cnf) |>.getD []

theorem orbit51Parsed_ok : orbit51Parsed.isSome = true := by
  native_decide

theorem orbit51Unsat : orbit51CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit51CNF
    (include_str "../../artifacts/n8k4_51.lrat")
  native_decide

end LratProbe.Orbits
