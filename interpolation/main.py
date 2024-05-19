from textwrap import wrap
from elevation_profiles import ElevationProfile, get_elevation_profile_from_files, apply_moving_average_to_elevation_profile
from matrix import Matrix
from solvers import LUFactorizationSolver
import matplotlib.pyplot as plt
from math import pi, cos
import os

def range_steps_count(start, end, steps_count, include_end=True):
  step = (end - start) / steps_count
  return [start + i * step for i in range(steps_count + 1 if include_end else steps_count)]

def get_evenly_spaced_indexes(data, anchor_points):
  return sorted(list(set([int(i) for i in range_steps_count(0, len(data) - 1, anchor_points)])))

def get_chebyshev_nodes_indexes(data, anchor_points):
  anchor_points = anchor_points - 1  
  return sorted(list(set([int((len(data) - 1) / 2 * (1 + cos((2 * i + 1) * pi / (2 * anchor_points))) + 0.5) for i in range(anchor_points)])))

def lagrange_interpolation(data, interpolation_points=1000, anchor_points_count=5, anchor_points_function=get_evenly_spaced_indexes):
  anchor_points_indexes = anchor_points_function(data, anchor_points_count)
  
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

def splines(data, interpolation_points=1000, anchor_points_count=5, anchor_points_function=get_evenly_spaced_indexes):
  x_fine = [x[0] for x in data]
  y_fine = [x[1] for x in data]
  
  anchor_points_indexes = anchor_points_function(data, anchor_points_count)
  
  n = len(anchor_points_indexes)
  h = [x_fine[anchor_points_indexes[i+1]] - x_fine[anchor_points_indexes[i]] for i in range(n-1)]
  a = [y_fine[i] for i in anchor_points_indexes]
  b = []
  d = []

  A = Matrix(n, n)
  b_vector = Matrix(n, 1)

  A[0][0] = 1
  A[n-1][n-1] = 1

  for i in range(1, n-1):
    A[i][i] = 2 * (h[i-1] + h[i])
    A[i][i-1] = h[i-1]
    A[i][i+1] = h[i]
    b_vector[i][0] = 3 * ((y_fine[anchor_points_indexes[i+1]] - y_fine[anchor_points_indexes[i]])/h[i] - (y_fine[anchor_points_indexes[i]] - y_fine[anchor_points_indexes[i-1]])/h[i-1])

  solver = LUFactorizationSolver(A, b_vector)
  c = solver.x
  c = [x[0] for x in c]

  b = [0] * n
  d = [0] * n

  for i in range(n-1):
    b[i] = ((y_fine[anchor_points_indexes[i+1]] - y_fine[anchor_points_indexes[i]])/h[i] - h[i]/3 * (2 * c[i] + c[i+1]))
    d[i] = ((c[i+1] - c[i])/(3 * h[i]))

  x_coarse = range_steps_count(x_fine[0], x_fine[-1], interpolation_points)
  y_coarse = []

  for x in x_coarse:
    current_index = n-1
    for i in range(len(anchor_points_indexes) - 1):
      if x_fine[anchor_points_indexes[i]] <= x < x_fine[anchor_points_indexes[i + 1]]:
        current_index = i
        break

    h = x-x_fine[anchor_points_indexes[current_index]]
    y_coarse.append(a[current_index] + b[current_index] * h + c[current_index] * h**2 + d[current_index] * h ** 3)

  x_fine = [x_fine[i] for i in anchor_points_indexes]
  y_fine = [y_fine[i] for i in anchor_points_indexes]

  return x_fine, y_fine, x_coarse, y_coarse

def plot_interpolation(data, interpolation_function, anchor_points=[7, 11, 17, 21], anchor_points_function=get_evenly_spaced_indexes, filename='interpolation'):
  os.makedirs('charts', exist_ok=True)
  for anchor_points_count in anchor_points:
    x_fine, y_fine, x_coarse, y_coarse = interpolation_function(data, anchor_points_count=anchor_points_count, anchor_points_function=anchor_points_function)
    
    if interpolation_function == lagrange_interpolation:
      nazwa = 'Lagrange\'a'
    elif interpolation_function == splines:
      nazwa = 'funkcjami sklejanymi'
    
    if anchor_points_function == get_evenly_spaced_indexes:
      rodzaj = 'równoodległymi'
    elif anchor_points_function == get_chebyshev_nodes_indexes:
      rodzaj = 'Czebyszewa'
      
    title = f'Interpolacja {nazwa} z wykorzystaniem węzłów {rodzaj} dla {anchor_points_count} węzłów. Trasa {filename}'
    plt.title('\n'.join(wrap(title, 60)))
    plt.plot(x_fine, y_fine, 'ro', label="Węzły interpolacji")
    plt.plot([x[0] for x in data], [x[1] for x in data], 'g', label="Funkcja oryginalna")
    plt.plot(x_coarse, y_coarse, 'r', label="Funkcja interpolująca")
    plt.xlabel("Odległość [km]")
    plt.ylabel("Wzniesienie [m]")
    plt.legend()
    plt.savefig(f'charts/{filename.lower()}_{nazwa[0].lower()}_{rodzaj[0].lower()}_{anchor_points_count}.png')
    plt.clf() 
  
def main():
  [os.remove(f'charts/{f}') for f in os.listdir('charts') if f.endswith('.png')]
  cewice_data = get_elevation_profile_from_files(ElevationProfile.CEWICE_LEBA)
  plot_interpolation(cewice_data, lagrange_interpolation, anchor_points=[5, 7, 10, 15], anchor_points_function=get_evenly_spaced_indexes, filename='Cewice')
  plot_interpolation(cewice_data, splines, anchor_points=[5, 10, 20, 50], anchor_points_function=get_evenly_spaced_indexes, filename='Cewice')
  plot_interpolation(cewice_data, lagrange_interpolation, anchor_points=[5, 7, 10, 15, 50], anchor_points_function=get_chebyshev_nodes_indexes, filename='Cewice')
  
  wiezyca_data = get_elevation_profile_from_files(ElevationProfile.WIEZYCA)
  wiezyca_data = apply_moving_average_to_elevation_profile(wiezyca_data, 20)
  current_distance = wiezyca_data[-1][0]
  reversed_data = [[ 2 * current_distance - x[0], x[1]] for x in wiezyca_data[::-1]]
  wiezyca_data += reversed_data
  plot_interpolation(wiezyca_data, lagrange_interpolation, anchor_points=[7, 11, 17, 21], anchor_points_function=get_evenly_spaced_indexes, filename='Wieżyca')
  plot_interpolation(wiezyca_data, splines, anchor_points=[5, 7, 15, 50], anchor_points_function=get_evenly_spaced_indexes, filename='Wieżyca')
  plot_interpolation(wiezyca_data, lagrange_interpolation, anchor_points=[7, 11, 17, 50], anchor_points_function=get_chebyshev_nodes_indexes, filename='Wieżyca')

  szklarka_data = get_elevation_profile_from_files(ElevationProfile.SZKLARKA)
  szklarka_data = apply_moving_average_to_elevation_profile(szklarka_data, 300)
  plot_interpolation(szklarka_data, lagrange_interpolation, anchor_points=[5, 7, 12, 20], anchor_points_function=get_evenly_spaced_indexes, filename='Szklarka')
  plot_interpolation(szklarka_data, splines, anchor_points=[5, 10, 20, 30], anchor_points_function=get_evenly_spaced_indexes, filename='Szklarka')
  plot_interpolation(szklarka_data, lagrange_interpolation, anchor_points=[5, 7, 12, 20, 50], anchor_points_function=get_chebyshev_nodes_indexes, filename='Szklarka')

  
if __name__ == '__main__':
  main()    
    