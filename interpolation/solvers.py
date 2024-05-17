from matrix import Matrix
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
    
    y = Matrix(n, 1)
    for i in range(n):
      y.matrix[i][0] = b.matrix[i][0]
    
    x = Matrix(n, 1)
    for i in range(n):
      x.matrix[i][0] = 0

    start = time.time()
    
    transform_matrix = Matrix(A.n, A.n)
    
    for i in range(n):
      transform_matrix.matrix[i][i] = 1
        
    for i in range(n):
      current_column = [U.matrix[j][i] for j in range(i, n)]
      pivot = max(current_column, key=abs)
      pivot_index = current_column.index(pivot) + i
      if pivot == 0:
        raise ValueError("Matrix is singular")
      if pivot_index != i:
        U.swap_rows(i, pivot_index)
        L.swap_rows(i, pivot_index)
        transform_matrix.swap_rows(i, pivot_index)
          
      for j in range(i+1, n):
        factor = U.matrix[j][i] / U.matrix[i][i]
        L.matrix[j][i] = factor
        for k in range(i, n):
          U.matrix[j][k] -= factor * U.matrix[i][k]
                
    if self.debug:
      print("Finished LU decomposition")

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
