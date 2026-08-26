/- UNAUDITED — lane L1, generated. Orbit 20 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit20Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_20.cnf")

def orbit20CNF : CNF Nat :=
  orbit20Parsed.map (·.cnf) |>.getD []

theorem orbit20Parsed_ok : orbit20Parsed.isSome = true := by
  native_decide

theorem orbit20Unsat : orbit20CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit20CNF
    (include_str "../../artifacts/n8k4_20.lrat")
  native_decide

end LratProbe.Orbits
