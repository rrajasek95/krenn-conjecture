/- UNAUDITED — lane L1, generated. Orbit 14 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit14Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_14.cnf")

def orbit14CNF : CNF Nat :=
  orbit14Parsed.map (·.cnf) |>.getD []

theorem orbit14Parsed_ok : orbit14Parsed.isSome = true := by
  native_decide

theorem orbit14Unsat : orbit14CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit14CNF
    (include_str "../../artifacts/n8k4_14.lrat")
  native_decide

end LratProbe.Orbits
