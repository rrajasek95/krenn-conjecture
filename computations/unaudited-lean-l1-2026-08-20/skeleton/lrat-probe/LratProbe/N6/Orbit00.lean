/- UNAUDITED — lane L1, generated. N=6 orbit 0 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit0Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_0.cnf")

def orbit0CNF : CNF Nat :=
  orbit0Parsed.map (·.cnf) |>.getD []

theorem orbit0Parsed_ok : orbit0Parsed.isSome = true := by
  native_decide

theorem orbit0Unsat : orbit0CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit0CNF
    (include_str "../../artifacts/n6/n6_0.lrat")
  native_decide

end LratProbe.N6
