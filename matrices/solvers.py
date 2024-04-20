from matrix_generator import Matrix, VectorB
import time
import copy
import abc

class Solver(abc.ABC):
    def __init__(self, name, A, b, debug=False):
        self.name = name
        self.A = A
        self.b = b
        self.duration = 0
        self.x = None
        self.debug = debug
        self.errors = []

    def solve(self, A, b):
        pass

    def get_solution_error(self):
        return (self.A * self.x - self.b).norm()
    
    def __str__(self) -> str:
        return f"{self.name} duration: {self.duration}, error: {self.get_solution_error()}"

class GaussSolver(Solver):
    def __init__(self, A, b, debug=False):
        super().__init__("Gauss", A, b, debug)
        self.x, self.duration, self.errors = self.solve(A, b)

    def solve(self, A, b):
        n = A.n
        x = VectorB(n)

        start = time.time()
        
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A.matrix[k][i]) > abs(A.matrix[max_row][i]):
                    max_row = k
            A.matrix[i], A.matrix[max_row] = A.matrix[max_row], A.matrix[i]
            b.matrix[i], b.matrix[max_row] = b.matrix[max_row], b.matrix[i]

            for k in range(i+1, n):
                factor = A.matrix[k][i] / A.matrix[i][i]
                for j in range(i, n):
                    A.matrix[k][j] -= factor * A.matrix[i][j]
                b.matrix[k][0] -= factor * b.matrix[i][0]

        for i in range(n-1, -1, -1):
            x.matrix[i][0] = b.matrix[i][0] / A.matrix[i][i]
            for k in range(i-1, -1, -1):
                b.matrix[k][0] -= A.matrix[k][i] * x.matrix[i][0]

        end = time.time()

        return x, end-start
    
    
class JacobiSolver(Solver):
    def __init__(self, A, b, debug=False):
        super().__init__("Jacobi", A, b, debug)
        self.x, self.duration, self.errors = self.solve(A, b)

    def solve(self, A, b, max_iter=100, eps=1e-9):
        n = A.n
        x = VectorB(n)
        x_new = copy.deepcopy(x)
        errors = []

        start = time.time()

        for _ in range(max_iter):
            for i in range(n):
                s = b.matrix[i][0]
                for j in range(n):
                    if i != j:
                        s -= A.matrix[i][j] * x.matrix[j][0]
                x_new.matrix[i][0] = s / A.matrix[i][i]

            x = copy.deepcopy(x_new)

            res = A * x - b
            res_norm = res.norm()
            errors.append(res_norm)

            if res_norm < eps:
                break

            if self.debug:
                print(f"iteration {_}, error: {res_norm}")

        end = time.time()
        return x, end-start, errors
    
class GaussSeidelSolver(Solver):
    def __init__(self, A, b, debug=False):
        super().__init__("Gauss-Seidel", A, b, debug)
        self.x, self.duration, self.errors = self.solve(A, b)

    def solve(self, A, b, max_iter=100, eps=1e-9):
        n = A.n
        x = VectorB(n)
        x_new = copy.deepcopy(x)
        start = time.time()
        errors = []

        for _ in range(max_iter):
            for i in range(n):
                s = b.matrix[i][0]
                for j in range(i):
                    s -= A.matrix[i][j] * x_new.matrix[j][0]
                for j in range(i+1, n):
                    s -= A.matrix[i][j] * x.matrix[j][0]

                x_new.matrix[i][0] = s / A.matrix[i][i]

            x = copy.deepcopy(x_new)
            
            res = A * x - b
            res_norm = res.norm()

            errors.append(res_norm)

            if res_norm < eps:
                break

            if self.debug:
                print(f"iteration {_}, error: {res_norm}")

        end = time.time()
        return x, end-start, errors
    
class LUFactorizationSolver(Solver):
    def __init__(self, A, b, debug=False):
        super().__init__("LU Factorization", A, b, debug)
        self.x, self.duration, self.errors = self.solve(A, b)

    def solve(self, A, b):
        n = A.n
        U = copy.deepcopy(A)
        L = Matrix(n, n)
        for i in range(n):
            L.matrix[i][i] = 1
        y = VectorB(n, function="1")
        x = VectorB(n, function="1")

        start = time.time()

        for i in range(2, n+1):
            for j in range(1, i):
                L.matrix[i-1][j-1] = U.matrix[i-1][j-1] / U.matrix[j-1][j-1]
                for k in range(j, n):
                    U.matrix[i-1][k] -= L.matrix[i-1][j-1] * U.matrix[j-1][k]

        if self.debug:
            print("Finished LU factorization")

        for i in range(n):
            y.matrix[i][0] = b.matrix[i][0]
            for j in range(i):
                y.matrix[i][0] -= L.matrix[i][j] * y.matrix[j][0]

        if self.debug:
            print("Finished forward substitution")

        for i in range(n-1, -1, -1):
            x.matrix[i][0] = y.matrix[i][0]
            for j in range(i+1, n):
                x.matrix[i][0] -= U.matrix[i][j] * x.matrix[j][0]
            x.matrix[i][0] /= U.matrix[i][i]

        if self.debug:
            print("Finished backward substitution")

        end = time.time()

        error = (A * x - b).norm()

        return x, end-start, [error]
