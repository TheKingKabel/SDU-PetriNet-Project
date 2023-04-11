from main.PetriNet import *

fork = PetriNet("Forking")

P_Start = Place("P_Start", fork, 10)

IT_Start = ImmediateTransition("IT_Start", fork)

IA_Start = InputArc("IA_Start", fork, P_Start, IT_Start)

P_Up1 = Place("P_Up1", fork)
P_Mid1 = Place("P_Mid1", fork)
P_Low1 = Place("P_Low1", fork)

OA_Start1 = OutputArc("OA_Start1", fork, IT_Start, P_Up1)
OA_Start2 = OutputArc("OA_Start2", fork, IT_Start, P_Mid1)
OA_Start3 = OutputArc("OA_Start3", fork, IT_Start, P_Low1)

TT_Up1 = TimedTransition("TT_Up1", fork, 'NORM', 5.0, 1.5)
TT_Mid1 = TimedTransition("TT_Mid1", fork, 'NORM', 5.0, 1.5)
TT_Low1 = TimedTransition("TT_Low1", fork, 'NORM', 5.0, 1.5)

P_UpAux1 = Place("P_UpAux1", fork, 1)
P_MidAux1 = Place("P_MidAux1", fork, 1)
P_LowAux1 = Place("P_LowAux1", fork, 1)

IA_Up1 = InputArc("IA_Up1", fork, P_Up1, TT_Up1)
IA_Mid1 = InputArc("IA_Mid1", fork, P_Mid1, TT_Mid1)
IA_Low1 = InputArc("IA_Low1", fork, P_Low1, TT_Low1)

IA_UpAux1 = InputArc("IA_UpAux1", fork, P_UpAux1, TT_Up1)
IA_MidAux1 = InputArc("IA_MidAux1", fork, P_MidAux1, TT_Mid1)
IA_LowAux1 = InputArc("IA_LowAux1", fork, P_LowAux1, TT_Low1)

OA_UpAux1 = OutputArc("OA_UpAux1", fork, TT_Up1, P_UpAux1)
OA_MidAux1 = OutputArc("OA_MidAux1", fork, TT_Mid1, P_MidAux1)
OA_LowAux1 = OutputArc("OA_LowAux1", fork, TT_Low1, P_LowAux1)


P_Up2 = Place("P_Up2", fork)
P_Mid2 = Place("P_Mid2", fork)
P_Low2 = Place("P_Low2", fork)

OA_Up1 = OutputArc("OA_Up1", fork, TT_Up1, P_Up2)
OA_Mid1 = OutputArc("OA_Mid1", fork, TT_Mid1, P_Mid2)
OA_Low1 = OutputArc("OA_Low1", fork, TT_Low1, P_Low2)

IT_Up1 = ImmediateTransition("IT_Up1", fork)
TT_Mid2 = TimedTransition("TT_Mid2", fork, 'NORM', 7.0, 2.5)
IT_Low1 = ImmediateTransition("IT_Low1", fork)

IA_Up2 = InputArc("IA_Up2", fork, P_Up2, IT_Up1)
IA_Mid2 = InputArc("IA_Mid2", fork, P_Mid2, TT_Mid1)
IA_Low2 = InputArc("IA_Low2", fork, P_Low2, IT_Low1)

P_MidAux2 = Place("P_MidAux2", fork, 1)
IA_MidAux2 = InputArc("IA_MidAux2", fork, P_MidAux2, TT_Mid2)
OA_MidAux2 = OutputArc("OA_MidAux2", fork, TT_Mid2, P_MidAux2)

P_Up31 = Place("P_Up31", fork)
P_Up32 = Place("P_Up32", fork)
P_Up33 = Place("P_Up33", fork)

OA_Up21 = OutputArc("OA_Up21", fork, IT_Up1, P_Up31)
OA_Up22 = OutputArc("OA_Up22", fork, IT_Up1, P_Up32)
OA_Up23 = OutputArc("OA_Up23", fork, IT_Up1, P_Up33)

P_Low31 = Place("P_Low31", fork)
P_Low32 = Place("P_Low32", fork)

OA_Low21 = OutputArc("OA_Low21", fork, IT_Low1, P_Low31)
OA_Low22 = OutputArc("OA_Low22", fork, IT_Low1, P_Low32)


TT_Up21 = TimedTransition("TT_Up21", fork, 'NORM', 1.0, 10.0)
TT_Up22 = TimedTransition("TT_Up22", fork, 'NORM', 3.0, 10.0)
TT_Up23 = TimedTransition("TT_Up23", fork, 'NORM', 5.0, 10.0)

P_UpAux21 = Place("P_UpAux21", fork, 1)
P_UpAux22 = Place("P_UpAux22", fork, 1)
P_UpAux23 = Place("P_UpAux23", fork, 1)

IA_UpAux21 = InputArc("IA_UpAux21", fork, P_UpAux21, TT_Up21)
IA_UpAux22 = InputArc("IA_UpAux22", fork, P_UpAux22, TT_Up22)
IA_UpAux23 = InputArc("IA_UpAux23", fork, P_UpAux23, TT_Up23)

OA_UpAux21 = OutputArc("OA_UpAux21", fork, TT_Up21, P_UpAux21)
OA_UpAux22 = OutputArc("OA_UpAux22", fork, TT_Up22, P_UpAux22)
OA_UpAux23 = OutputArc("OA_UpAux23", fork, TT_Up23, P_UpAux23)

IA_Up31 = InputArc("IA_Up31", fork, P_Up31, TT_Up21)
IA_Up32 = InputArc("IA_Up32", fork, P_Up32, TT_Up22)
IA_Up33 = InputArc("IA_Up33", fork, P_Up33, TT_Up23)


TT_Low21 = TimedTransition("TT_Low21", fork, 'NORM', 3.0, 6.0)
TT_Low22 = TimedTransition("TT_Low22", fork, 'NORM', 3.0, 9.0)

P_LowAux21 = Place("P_LowAux21", fork, 1)
P_LowAux22 = Place("P_LowAux22", fork, 1)

IA_LowAux21 = InputArc("IA_LowAux21", fork, P_LowAux21, TT_Low21)
IA_LowAux22 = InputArc("IA_LowAux22", fork, P_LowAux22, TT_Low22)

OA_LowAux21 = OutputArc("OA_LowAux21", fork, TT_Low21, P_LowAux21)
OA_LowAux22 = OutputArc("OA_LowAux22", fork, TT_Low22, P_LowAux22)

IA_Low21 = InputArc("IA_Low21", fork, P_Low31, TT_Low21)
IA_Low22 = InputArc("IA_Low22", fork, P_Low32, TT_Low22)

P_Low41 = Place("P_Low41", fork)
P_Low42 = Place("P_Low42", fork)

OA_Low31 = OutputArc("OA_Low31", fork, TT_Low21, P_Low41)
OA_Low32 = OutputArc("OA_Low32", fork, TT_Low22, P_Low42)


P_Up41 = Place("P_Up41", fork)
OA_Up31 = OutputArc("OA_Up31", fork, TT_Up21, P_Up41)

TT_Up31 = TimedTransition("TT_Up31", fork, 'NORM', 5.0, 10.0)
P_UpAux31 = Place("P_UpAux31", fork, 1)
IA_UpAux31 = InputArc("IA_UpAux31", fork, P_UpAux31, TT_Up31)
OA_UpAux31 = OutputArc("OA_UpAux31", fork, TT_Up31, P_UpAux31)

IA_Up41 = InputArc("IA_Up41", fork, P_Up41, TT_Up31)

P_Up51 = Place("P_Up51", fork)
P_Up52 = Place("P_Up52", fork)
P_Up53 = Place("P_Up53", fork)

OA_Up41 = OutputArc("OA_Up41", fork, TT_Up31, P_Up51)
OA_Up42 = OutputArc("OA_Up42", fork, TT_Up22, P_Up52)
OA_Up43 = OutputArc("OA_Up43", fork, TT_Up23, P_Up53)

P_Mid3 = Place("P_Mid3", fork)
OA_Mid2 = OutputArc("OA_Mid2", fork, TT_Mid2, P_Mid3)


IT_Low2 = ImmediateTransition("IT_Low2", fork)
IA_Low31 = InputArc("IA_Low31", fork, P_Low41, IT_Low2)
IA_Low32 = InputArc("IA_Low32", fork, P_Low42, IT_Low2)

P_Low5 = Place("P_Low5", fork)
OA_Low4 = OutputArc("OA_Low4", fork, IT_Low2, P_Low5)

TT_Low3 = TimedTransition("TT_Low3", fork, 'NORM', 3.5, 7.0)
P_LowAux3 = Place("P_LowA3", fork, 1)
IA_LowAux3 = InputArc("IA_LowAux3", fork, P_LowAux3, TT_Low3)
OA_LowAux3 = OutputArc("OA_LowAux3", fork, TT_Low3, P_LowAux3)

IA_Low4 = InputArc("IA_Low4", fork, P_Low5, TT_Low3)

P_Low6 = Place("P_Low6", fork)
OA_Low5 = OutputArc("OA_Low5", fork, TT_Low3, P_Low6)

IT_Up2 = ImmediateTransition("IT_Up2", fork)
IA_Up51 = InputArc("IA_Up51", fork, P_Up51, IT_Up2)
IA_Up52 = InputArc("IA_Up52", fork, P_Up52, IT_Up2)
IA_Up53 = InputArc("IA_Up53", fork, P_Up53, IT_Up2)

P_Up6 = Place("P_Up6", fork)
OA_Up5 = OutputArc("OA_Up5", fork, IT_Up2, P_Up6)

IT_End = ImmediateTransition("IT_End", fork)
IA_End1 = InputArc("IA_End1", fork, P_Up6, IT_End)
IA_End2 = InputArc("IA_End2", fork, P_Mid3, IT_End)
IA_End3 = InputArc("IA_End3", fork, P_Low6, IT_End)

P_End = Place("P_End", fork)
OA_End = OutputArc("OA_End", fork, IT_End, P_End)


fork.runSimulation(100)
