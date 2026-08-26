/- UNAUDITED — lane L1, generated. Orbit 42 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit42Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_42.cnf")

def orbit42CNF : CNF Nat :=
  orbit42Parsed.map (·.cnf) |>.getD []

theorem orbit42Parsed_ok : orbit42Parsed.isSome = true := by
  native_decide

theorem orbit42Unsat : orbit42CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit42CNF
    (include_str "../../artifacts/n8k4_42.lrat")
  native_decide

end LratProbe.Orbits
