/- UNAUDITED — lane L1, generated. Orbit 71 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit71Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_71.cnf")

def orbit71CNF : CNF Nat :=
  orbit71Parsed.map (·.cnf) |>.getD []

theorem orbit71Parsed_ok : orbit71Parsed.isSome = true := by
  native_decide

theorem orbit71Unsat : orbit71CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit71CNF
    (include_str "../../artifacts/n8k4_71.lrat")
  native_decide

end LratProbe.Orbits
