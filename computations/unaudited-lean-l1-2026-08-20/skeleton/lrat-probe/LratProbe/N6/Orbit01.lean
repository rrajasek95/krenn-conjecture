/- UNAUDITED — lane L1, generated. N=6 orbit 1 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit1Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_1.cnf")

def orbit1CNF : CNF Nat :=
  orbit1Parsed.map (·.cnf) |>.getD []

theorem orbit1Parsed_ok : orbit1Parsed.isSome = true := by
  native_decide

theorem orbit1Unsat : orbit1CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit1CNF
    (include_str "../../artifacts/n6/n6_1.lrat")
  native_decide

end LratProbe.N6
