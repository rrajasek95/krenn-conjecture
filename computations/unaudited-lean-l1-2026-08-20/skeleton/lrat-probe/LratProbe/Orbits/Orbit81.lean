/- UNAUDITED — lane L1, generated. Orbit 81 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit81Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_81.cnf")

def orbit81CNF : CNF Nat :=
  orbit81Parsed.map (·.cnf) |>.getD []

theorem orbit81Parsed_ok : orbit81Parsed.isSome = true := by
  native_decide

theorem orbit81Unsat : orbit81CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit81CNF
    (include_str "../../artifacts/n8k4_81.lrat")
  native_decide

end LratProbe.Orbits
