/- UNAUDITED — lane L1, generated. Orbit 22 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit22Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_22.cnf")

def orbit22CNF : CNF Nat :=
  orbit22Parsed.map (·.cnf) |>.getD []

theorem orbit22Parsed_ok : orbit22Parsed.isSome = true := by
  native_decide

theorem orbit22Unsat : orbit22CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit22CNF
    (include_str "../../artifacts/n8k4_22.lrat")
  native_decide

end LratProbe.Orbits
