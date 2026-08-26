/- UNAUDITED — lane L1, generated. Orbit 4 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit4Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_4.cnf")

def orbit4CNF : CNF Nat :=
  orbit4Parsed.map (·.cnf) |>.getD []

theorem orbit4Parsed_ok : orbit4Parsed.isSome = true := by
  native_decide

theorem orbit4Unsat : orbit4CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit4CNF
    (include_str "../../artifacts/n8k4_4.lrat")
  native_decide

end LratProbe.Orbits
