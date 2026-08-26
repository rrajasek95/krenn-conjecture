/- UNAUDITED — lane L1, generated. Orbit 40 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit40Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_40.cnf")

def orbit40CNF : CNF Nat :=
  orbit40Parsed.map (·.cnf) |>.getD []

theorem orbit40Parsed_ok : orbit40Parsed.isSome = true := by
  native_decide

theorem orbit40Unsat : orbit40CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit40CNF
    (include_str "../../artifacts/n8k4_40.lrat")
  native_decide

end LratProbe.Orbits
