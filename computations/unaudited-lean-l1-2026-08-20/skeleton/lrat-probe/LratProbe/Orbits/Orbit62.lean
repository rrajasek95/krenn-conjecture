/- UNAUDITED — lane L1, generated. Orbit 62 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit62Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_62.cnf")

def orbit62CNF : CNF Nat :=
  orbit62Parsed.map (·.cnf) |>.getD []

theorem orbit62Parsed_ok : orbit62Parsed.isSome = true := by
  native_decide

theorem orbit62Unsat : orbit62CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit62CNF
    (include_str "../../artifacts/n8k4_62.lrat")
  native_decide

end LratProbe.Orbits
