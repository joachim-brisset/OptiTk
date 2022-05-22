from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus, GLPK, LpInteger
import numpy as np;

model2 = LpProblem(name="test-problem", sense=LpMinimize)

prod = np.array([[50,50,30,30],[60,50,50,40],[80,80,80,70]])
cost = np.array([[80,120,120,80],[100,150,100,120],[150,140,150,130]])

stock_order = np.array([[7000],[2000],[8000],[2000]])
stock_init = np.array([[2000],[0],[2000],[1000]])
stock_secu = np.array([[1000],[1000],[2000],[1000]])

t1_1 = LpVariable(name="t1_1", lowBound=0, upBound=144, cat=LpInteger)
t1_2 = LpVariable(name="t1_2", lowBound=0, upBound=144, cat=LpInteger)
t1_3 = LpVariable(name="t1_3", lowBound=0, upBound=144, cat=LpInteger)
t1_4 = LpVariable(name="t1_4", lowBound=0, upBound=144, cat=LpInteger)

t2_1 = LpVariable(name="t2_1", lowBound=0, upBound=144, cat=LpInteger)
t2_2 = LpVariable(name="t2_2", lowBound=0, upBound=144, cat=LpInteger)
t2_3 = LpVariable(name="t2_3", lowBound=0, upBound=144, cat=LpInteger)
t2_4 = LpVariable(name="t2_4", lowBound=0, upBound=144, cat=LpInteger)

t3_1 = LpVariable(name="t3_1", lowBound=0, upBound=144, cat=LpInteger)
t3_2 = LpVariable(name="t3_2", lowBound=0, upBound=144, cat=LpInteger)
t3_3 = LpVariable(name="t3_3", lowBound=0, upBound=144, cat=LpInteger)
t3_4 = LpVariable(name="t3_4", lowBound=0, upBound=144, cat=LpInteger)

T = np.array([[t1_1,t1_2,t1_3,t1_4],[t2_1,t2_2,t2_3,t2_4],[t3_1,t3_2,t3_3,t3_4]])

model2 += lpSum(T[:, 0] * prod[:, 0]) >= stock_secu[0] - stock_init[0] + stock_order[0]
model2 += lpSum(T[:, 1] * prod[:, 1]) >= stock_secu[1] - stock_init[1] + stock_order[1]
model2 += lpSum(T[:, 2] * prod[:, 2]) >= stock_secu[2] - stock_init[2] + stock_order[2]
model2 += lpSum(T[:, 3] * prod[:, 3]) >= stock_secu[3] - stock_init[3] + stock_order[3]

model2 += 0.1 * lpSum(T * prod * cost)

print("Solving model2 ...")
model2.solve(GLPK(options=["--ranges "]))

print(f"Status : {LpStatus[model2.status]}")
print(f"Objective : {model2.objective.value()}")

for var in model2.variables():
    print(f"{var.name} - {var.value()} reduced cost = {var.dj}")

print("name\tshadow price\tslack")
for name, constraint in model2.constraints.items():
    print(f"{name}\t{constraint.pi}\t\t{constraint.slack}")
