/- UNAUDITED — lane L1, generated. Orbit 50 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit50Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_50.cnf")

def orbit50CNF : CNF Nat :=
  orbit50Parsed.map (·.cnf) |>.getD []

theorem orbit50Parsed_ok : orbit50Parsed.isSome = true := by
  native_decide

theorem orbit50Unsat : orbit50CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit50CNF
    (include_str "../../artifacts/n8k4_50.lrat")
  native_decide

end LratProbe.Orbits
