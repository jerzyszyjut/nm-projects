from math import sin
from matrix_generator import UserMatrix, VectorB
from solvers import GaussSolver, JacobiSolver, GaussSeidelSolver, LUFactorizationSolver
import matplotlib.pyplot as plt
import pickle
import os

if not os.path.exists("snapshots"):
    os.makedirs("snapshots")
if not os.path.exists("images"):
    os.makedirs("images")


index_number = 193064
e = int(str(index_number)[3])
f = int(str(index_number)[2])
a1 = 5 + e
a2 = a3 = -1
function = "n"

# A

A = UserMatrix(a1, a2, a3, index_number=index_number)
b = VectorB(index_number=index_number, function=function)
# B
print("B")
try:
    jacobi_solver = pickle.load(open("snapshots/jacobi_b.pkl", "rb"))
    print("Loaded Jacobi from file!")
except:
    jacobi_solver = JacobiSolver(A, b)
    print("Jacobi finished!")
    pickle.dump(jacobi_solver, open("snapshots/jacobi_b.pkl", "wb"))
print(f"Duration: {jacobi_solver.duration}")
print(f"Iters: {len(jacobi_solver.errors)}")
print(f"Error: {jacobi_solver.errors[-1]}")

try:
    gauss_solver = pickle.load(open("snapshots/gauss_seidel_b.pkl", "rb"))
    print("Loaded Gauss-Seidel from file!")
except:
    gauss_solver = GaussSeidelSolver(A, b)
    print("Gauss-Seidel finished!")
    pickle.dump(gauss_solver, open("snapshots/gauss_seidel_b.pkl", "wb"))
print(f"Duration: {gauss_solver.duration}")
print(f"Iters: {len(gauss_solver.errors)}")
print(f"Error: {gauss_solver.errors[-1]}")

plt.title("Błędy w kolejnych iteracjach dla a1 = 5 + e (5), a2 = a3 = -1")
plt.plot(gauss_solver.errors, label="Gauss-Seidel")
plt.plot(jacobi_solver.errors, label="Jacobi")
plt.yscale('log')
plt.legend(["Gauss-Seidel", "Jacobi"])
plt.ylabel("Norma wektora residuum")
plt.xlabel("Iteracja")
plt.savefig("images/bledy_zbiezne.png")
plt.close()

# C 
print("C")
a1 = 3 
a2 = a3 = -1
A = UserMatrix(a1, a2, a3, index_number=index_number)
b = VectorB(index_number=index_number, function=function)

try:
    jacobi_solver = pickle.load(open("snapshots/jacobi_c.pkl", "rb"))
    print("Loaded Jacobi from file!")
except:
    jacobi_solver = JacobiSolver(A, b)
    print("Jacobi finished!")
    pickle.dump(jacobi_solver, open("snapshots/jacobi_c.pkl", "wb"))
print(f"Duration: {jacobi_solver.duration}")
print(f"Errors: {jacobi_solver.errors[-1]}")
print(f"Iters: {len(jacobi_solver.errors)}")

try:
    gauss_solver = pickle.load(open("snapshots/gauss_seidel_c.pkl", "rb"))
    print("Loaded Gauss-Seidel from file!")
except:
    gauss_solver = GaussSeidelSolver(A, b)
    print("Gauss-Seidel finished!")
    pickle.dump(gauss_solver, open("snapshots/gauss_seidel_c.pkl", "wb"))
print(f"Duration: {gauss_solver.duration}")
print(f"Errors: {gauss_solver.errors[-1]}")
print(f"Iters: {len(gauss_solver.errors)}")

plt.title("Błędy w kolejnych iteracjach dla a1 = 3, a2 = a3 = -1")
plt.plot(gauss_solver.errors, label="Gauss-Seidel")
plt.plot(jacobi_solver.errors, label="Jacobi")
plt.yscale('log')
plt.legend(["Gauss-Seidel", "Jacobi"])
plt.ylabel("Norma wektora residuum")
plt.xlabel("Iteracja")
plt.savefig("images/bledy_rozbiezne.png")
plt.close()

# D 
print("D")
A = UserMatrix(a1, a2, a3, index_number=index_number)
b = VectorB(index_number=index_number, function=function)
try:
    lu_solver = pickle.load(open("snapshots/lu_d.pkl", "rb"))
    print("Loaded LU from file!")
except:
    lu_solver = LUFactorizationSolver(A, b, debug=True)
    pickle.dump(lu_solver, open("snapshots/lu_d.pkl", "wb"))
    print("LU finished!")
print(f"Duration: {lu_solver.duration}")
print(f"Errors: {lu_solver.errors}")

# E
print("E")
a1 = 5 + e
a2 = a3 = -1
sizes = [100, 500, 1000, 2000, 3000, 4000]

durations_jacobi = []
durations_gauss_seidel = []
durations_lu = []

for size in sizes:
    A = UserMatrix(a1, a2, a3, index_number=index_number, n=size)
    b = VectorB(index_number=index_number, function=function, n=size)

    try:
        jacobi_solver = pickle.load(open(f"snapshots/jacobi_{size}.pkl", "rb"))
        print(f"Loaded Jacobi {size} from file!")
    except:
        jacobi_solver = JacobiSolver(A, b)
        pickle.dump(jacobi_solver, open(f"snapshots/jacobi_{size}.pkl", "wb"))
        print(f"Jacobi {size} finished!")
    print(f"Duration: {jacobi_solver.duration}")
    print(f"Error: {jacobi_solver.errors[-1]}")
    print(f"Iters: {len(jacobi_solver.errors)}")
    durations_jacobi.append(jacobi_solver.duration)
    
    try:
        gauss_seidel_solver = pickle.load(open(f"snapshots/gauss_seidel_{size}.pkl", "rb"))
        print(f"Loaded Gauss-Seidel {size} from file!")
    except:
        gauss_seidel_solver = GaussSeidelSolver(A, b)
        pickle.dump(gauss_seidel_solver, open(f"snapshots/gauss_seidel_{size}.pkl", "wb"))
        print(f"Gauss-Seidel {size} finished!")
    print(f"Duration: {gauss_seidel_solver.duration}")
    print(f"Error: {jacobi_solver.errors[-1]}")
    print(f"Iters: {len(gauss_seidel_solver.errors)}")
    durations_gauss_seidel.append(gauss_seidel_solver.duration)

    try:
        lu_solver = pickle.load(open(f"snapshots/lu_{size}.pkl", "rb"))
        print(f"Loaded LU {size} from file!")
    except:
        lu_solver = LUFactorizationSolver(A, b)
        pickle.dump(lu_solver, open(f"snapshots/lu_{size}.pkl", "wb"))
        print(f"LU {size} finished!")
    print(f"Duration: {lu_solver.duration}")
    print(f"Error: {lu_solver.errors[-1]}")
    durations_lu.append(lu_solver.duration)

plt.close()
plt.title("Czas wykonania w zależności od rozmiaru macierzy")
plt.plot(sizes, durations_jacobi)
plt.plot(sizes, durations_gauss_seidel)
plt.plot(sizes, durations_lu)
plt.legend(["Jacobi", "Gauss-Seidel", "LU"])
plt.ylabel("Czas wykonania [s]")
plt.xlabel("Rozmiar macierzy")
plt.savefig("images/czas_wykonania.png")

