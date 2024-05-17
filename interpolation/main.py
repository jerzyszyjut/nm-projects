from elevation_profiles import ElevationProfile, get_elevation_profile_from_files
from matrix import Matrix
from solvers import LUFactorizationSolver
import matplotlib.pyplot as plt
from math import pi, cos

data = get_elevation_profile_from_files(ElevationProfile.GRAND_CANYON)

def range_steps_count(start, end, steps_count, include_end=True):
  step = (end - start) / steps_count
  return [start + i * step for i in range(steps_count + 1 if include_end else steps_count)]

def get_evenly_spaced_indexes(data, anchor_points):
  return [int(i) for i in range_steps_count(0, len(data) - 1, anchor_points)]

def get_chebyshev_nodes_indexes(data, anchor_points):
  return list(set([int((len(data) - 1) / 2 * (1 + cos((2 * i + 1) * pi / (2 * anchor_points))) + 0.5) for i in range(anchor_points)]))

def lagrange_interpolation(data, interpolation_points=1000, anchor_points_indexes=None):
  if anchor_points_indexes is None:
    anchor_points_indexes = get_evenly_spaced_indexes(data, 5)
  
  x_fine = [data[i][0] for i in anchor_points_indexes]
  y_fine = [data[i][1] for i in anchor_points_indexes]
  
  x_coarse = range_steps_count(data[0][0], data[-1][0], interpolation_points)
  y_coarse = []
  
  for x in x_coarse:
    y = 0
    for i in range(len(x_fine)):
      l = 1
      for j in range(len(x_fine)):
        if i != j:
          l *= (x - x_fine[j]) / (x_fine[i] - x_fine[j])
      y += y_fine[i] * l
    y_coarse.append(y)
    
  return x_fine, y_fine, x_coarse, y_coarse

def splines(data, interpolation_points=1000, anchor_points_indexes=None):
  if anchor_points_indexes is None:
    anchor_points_indexes = get_evenly_spaced_indexes(data, 5)

  a = [data[i][1] for i in anchor_points_indexes]
  h = [data[i + 1][0] - data[i][0] for i in anchor_points_indexes[:-1]]
  
  A = Matrix(len(a), len(a))
  b = Matrix(len(a), 1)
  
  for i in range(1, len(a) - 1):
    A.matrix[i][i] = 2 * (h[i - 1] + h[i])
    A.matrix[i][i - 1] = h[i - 1]
    A.matrix[i][i + 1] = h[i]
    b.matrix[i][0] = 6 * ((a[i + 1] - a[i]) / h[i] - (a[i] - a[i - 1]) / h[i - 1])
    
  A[0][0] = 1
  A[-1][-1] = 1
    
  solver = LUFactorizationSolver(A, b)
  c = [x[0] for x in solver.x.matrix]
  
  b = [0] * len(a)
  d = [0] * len(a)
  
  for i in range(len(a) - 1):
    b[i] = (a[i + 1] - a[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 6
    d[i] = (c[i + 1] - c[i]) / (6 * h[i])
    
  x_coarse = range_steps_count(data[0][0], data[-1][0], interpolation_points)
  y_coarse = []
  
  for x in x_coarse:
    for i in range(len(a) - 1):
      if data[anchor_points_indexes[i]][0] <= x <= data[anchor_points_indexes[i + 1]][0]:
        y = a[i] + b[i] * (x - data[anchor_points_indexes[i]][0]) + c[i] * (x - data[anchor_points_indexes[i]][0]) ** 2 + d[i] * (x - data[anchor_points_indexes[i]][0]) ** 3
        y_coarse.append(y)
        break
    else:
      y_coarse.append(a[-1] + b[-1] * (x - data[anchor_points_indexes[-1]][0]) + c[-1] * (x - data[anchor_points_indexes[-1]][0]) ** 2 + d[-1] * (x - data[anchor_points_indexes[-1]][0]) ** 3)
      
  return x_coarse, y_coarse      

x_fine, y_fine, x_coarse, y_coarse = lagrange_interpolation(data)

plt.plot(x_fine, y_fine, 'ro', label="Anchor points")
plt.plot([x[0] for x in data], [x[1] for x in data], 'g', label="Original")
plt.plot(x_coarse, y_coarse, 'r', label="Coarse")
plt.xlabel("Distance")
plt.ylabel("Elevation")
plt.legend()
plt.show()

x_coarse, y_coarse = splines(data)

plt.plot([x[0] for x in data], [x[1] for x in data], 'g', label="Original")
plt.plot(x_coarse, y_coarse, 'r', label="Coarse")
plt.xlabel("Distance")
plt.ylabel("Elevation")
plt.legend()
plt.show()
