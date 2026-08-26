/- UNAUDITED — lane L1, generated. Orbit 85 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit85Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_85.cnf")

def orbit85CNF : CNF Nat :=
  orbit85Parsed.map (·.cnf) |>.getD []

theorem orbit85Parsed_ok : orbit85Parsed.isSome = true := by
  native_decide

theorem orbit85Unsat : orbit85CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit85CNF
    (include_str "../../artifacts/n8k4_85.lrat")
  native_decide

end LratProbe.Orbits
