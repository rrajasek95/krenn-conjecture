/- UNAUDITED — lane L1, generated. Orbit 52 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit52Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_52.cnf")

def orbit52CNF : CNF Nat :=
  orbit52Parsed.map (·.cnf) |>.getD []

theorem orbit52Parsed_ok : orbit52Parsed.isSome = true := by
  native_decide

theorem orbit52Unsat : orbit52CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit52CNF
    (include_str "../../artifacts/n8k4_52.lrat")
  native_decide

end LratProbe.Orbits
