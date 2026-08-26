/- UNAUDITED — lane L1, generated. Orbit 8 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit8Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_8.cnf")

def orbit8CNF : CNF Nat :=
  orbit8Parsed.map (·.cnf) |>.getD []

theorem orbit8Parsed_ok : orbit8Parsed.isSome = true := by
  native_decide

theorem orbit8Unsat : orbit8CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit8CNF
    (include_str "../../artifacts/n8k4_8.lrat")
  native_decide

end LratProbe.Orbits
