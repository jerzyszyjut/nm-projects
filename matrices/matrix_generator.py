from math import sin

class Matrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix = self.generate_matrix(n, m)
    
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
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                result.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return result
    
    def __add__(self, other):
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

    def generate_matrix(self, n, m):
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
    
    def get_diagonal(self):
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                if i == j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_lower(self):
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                if i > j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_upper(self):
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                if i < j:
                    result.matrix[i][j] = self.matrix[i][j]
                else:
                    result.matrix[i][j] = 0
        return result
    
    def get_determinant(self):
        if self.n != self.m:
            raise ValueError("Matrix is not square")
        
        if self.n == 1:
            return self.matrix[0][0]
        
        if self.n == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        
        result = 0
        for i in range(self.n):
            result += ((-1) ** i) * self.matrix[0][i] * self.get_minor(0, i).get_determinant()
        return result
    
    def get_minor(self, i, j):
        result = Matrix(self.n - 1, self.m - 1)
        for k in range(self.n):
            for l in range(self.m):
                if k != i and l != j:
                    result.matrix[k - (k > i)][l - (l > j)] = self.matrix[k][l]
        return result
    
    def get_transposed(self):
        result = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                result.matrix[j][i] = self.matrix[i][j]
        return result
    
    def get_inverted(self):
        determinant = self.get_determinant()
        if determinant == 0:
            raise ValueError("Matrix is not invertible")
        
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                result.matrix[i][j] = ((-1) ** (i + j)) * self.get_minor(i, j).get_determinant()
        result = result.get_transposed()
        result = result * (1 / determinant)
        return result
    
class UserMatrix(Matrix):
    def __init__(self, a1, a2, a3, index_number=193064, n=None, m=None):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

        if n is None:
            self.n = int("9" + str(index_number)[-2:])
        else:
            self.n = n

        if m is None:
            self.m = self.n
        else:
            self.m = m

        self.matrix = self.generate_matrix(self.n, self.a1, self.a2, self.a3)

    def generate_matrix(self, n, a1, a2, a3):
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(a1)
                elif i == j - 1 or i == j + 1:
                    row.append(a2)
                elif i == j - 2 or i == j + 2:
                    row.append(a3)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix

class VectorB(Matrix):
    def __init__(self, n=None, index_number=193064, function="0"):
        self.n = n
        if self.n is None:
            self.n = int("9" + str(index_number)[-2:])
        self.m = 1
        self.function = function
        self.index_number = index_number
        self.matrix = self.generate_vector(self.n, function)

    def generate_vector(self, n, function=None):
        if function == "0":
            function = lambda i: 0
        elif function == "1":
            function = lambda i: 1
        elif function == "n":
            f = int(str(self.index_number)[2])
            function = lambda n: sin(n * (f + 1))

        vector = []
        for i in range(n):
            vector.append([function(i)])
        return vector
    