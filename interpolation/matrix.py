class Matrix:
  def __init__(self, n, m, starting_value=0):
    self.n = n
    self.m = m
    self.matrix = self.generate_matrix(n, m, starting_value)
  
  def __str__(self):
    result = "[\n"
    for row in self.matrix:
      for element in row:
        result += str(element) + ",\t"
      result = result[:-2]
      result += ";\n"
    result += "]"
    return result
  
  def __sub__(self, other):
    if self.n != other.n or self.m != other.m:
      raise ValueError("Matrix dimensions do not match")

    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        result.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
    return result
  
  def __add__(self, other):
    if self.n != other.n or self.m != other.m:
      raise ValueError("Matrix dimensions do not match")
    
    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
    return result
  
  def _multiply_matrices(self, other):
    if self.m != other.n:
      raise ValueError("Matrix dimensions do not match")
    
    result = Matrix(self.n, other.m)
    for i in range(self.n):
      for j in range(other.m):
        for k in range(self.m):
          result.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
    return result
  
  def _multiply_scalar(self, scalar):
    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        result.matrix[i][j] = self.matrix[i][j] * scalar
    return result

  def __mul__(self, other):
    if isinstance(other, Matrix):
      return self._multiply_matrices(other)
    elif isinstance(other, (int, float)):
      return self._multiply_scalar(other)
    else:
      raise ValueError("Unsupported operand type")

  def generate_matrix(self, n, m, starting_value=0):
    matrix = []
    for _ in range(n):
      row = []
      for _ in range(m):
        row.append(0)
      matrix.append(row)
    return matrix
  
  def norm(self):
    result = 0
    for i in range(self.n):
      for j in range(self.m):
        result += self.matrix[i][j] ** 2
    return result ** 0.5
  
  def diagonal(self):
    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        if i == j:
          result.matrix[i][j] = self.matrix[i][j]
        else:
          result.matrix[i][j] = 0
    return result
  
  def lower(self):
    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        if i > j:
          result.matrix[i][j] = self.matrix[i][j]
        else:
          result.matrix[i][j] = 0
    return result
  
  def upper(self):
    result = Matrix(self.n, self.m)
    for i in range(self.n):
      for j in range(self.m):
        if i < j:
          result.matrix[i][j] = self.matrix[i][j]
        else:
          result.matrix[i][j] = 0
    return result
  
  def transposed(self):
    result = Matrix(self.m, self.n)
    for i in range(self.n):
      for j in range(self.m):
        result.matrix[j][i] = self.matrix[i][j]
    return result
  
  def swap_rows(self, i, j):
    self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
    
  def from_list(data):
    matrix = Matrix(len(data), 1)
    for i in range(len(data)):
      matrix.matrix[i][0] = data[i]
    return matrix
    
  def __getitem__(self, key):
    return self.matrix[key]