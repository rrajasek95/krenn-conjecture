/- UNAUDITED — lane L1, generated. Orbit 78 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit78Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_78.cnf")

def orbit78CNF : CNF Nat :=
  orbit78Parsed.map (·.cnf) |>.getD []

theorem orbit78Parsed_ok : orbit78Parsed.isSome = true := by
  native_decide

theorem orbit78Unsat : orbit78CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit78CNF
    (include_str "../../artifacts/n8k4_78.lrat")
  native_decide

end LratProbe.Orbits
