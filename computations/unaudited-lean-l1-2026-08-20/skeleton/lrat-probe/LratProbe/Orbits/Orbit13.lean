/- UNAUDITED — lane L1, generated. Orbit 13 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit13Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_13.cnf")

def orbit13CNF : CNF Nat :=
  orbit13Parsed.map (·.cnf) |>.getD []

theorem orbit13Parsed_ok : orbit13Parsed.isSome = true := by
  native_decide

theorem orbit13Unsat : orbit13CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit13CNF
    (include_str "../../artifacts/n8k4_13.lrat")
  native_decide

end LratProbe.Orbits
