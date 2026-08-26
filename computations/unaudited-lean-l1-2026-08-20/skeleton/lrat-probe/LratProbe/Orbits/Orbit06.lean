/- UNAUDITED — lane L1, generated. Orbit 6 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit6Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_6.cnf")

def orbit6CNF : CNF Nat :=
  orbit6Parsed.map (·.cnf) |>.getD []

theorem orbit6Parsed_ok : orbit6Parsed.isSome = true := by
  native_decide

theorem orbit6Unsat : orbit6CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit6CNF
    (include_str "../../artifacts/n8k4_6.lrat")
  native_decide

end LratProbe.Orbits
