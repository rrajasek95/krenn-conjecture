/- UNAUDITED — lane L1, generated. Orbit 58 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit58Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_58.cnf")

def orbit58CNF : CNF Nat :=
  orbit58Parsed.map (·.cnf) |>.getD []

theorem orbit58Parsed_ok : orbit58Parsed.isSome = true := by
  native_decide

theorem orbit58Unsat : orbit58CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit58CNF
    (include_str "../../artifacts/n8k4_58.lrat")
  native_decide

end LratProbe.Orbits
