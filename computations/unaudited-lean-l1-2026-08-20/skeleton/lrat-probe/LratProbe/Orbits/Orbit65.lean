/- UNAUDITED — lane L1, generated. Orbit 65 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit65Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_65.cnf")

def orbit65CNF : CNF Nat :=
  orbit65Parsed.map (·.cnf) |>.getD []

theorem orbit65Parsed_ok : orbit65Parsed.isSome = true := by
  native_decide

theorem orbit65Unsat : orbit65CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit65CNF
    (include_str "../../artifacts/n8k4_65.lrat")
  native_decide

end LratProbe.Orbits
