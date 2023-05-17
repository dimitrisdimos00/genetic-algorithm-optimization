import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from population import population

# rastrigin search domain: -5.12 <= x, y <= 5.12
def rastrigin(x, y):
    return 20 + x**2 - 10*np.cos(2*np.pi*x) + y**2 - 10*np.cos(2*np.pi*y)
# ackley search domain: -5 <= x, y <= 5
def ackley(x, y):
    return -20 * np.exp( -0.2 * np.sqrt( 0.5 * (x ** 2 + y ** 2))) - np.exp( 0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.exp(1) + 20
# sphere search domain: -inf <= xi <= +inf
def sphere(x, y):
    return x**2 + y**2

def plotGraph(x_array, y_array, function):
    ax = plt.figure().add_subplot(projection='3d')
    for i in range(len(x_array)):
        values = function(x_array[i], y_array[i])
    ax.scatter(x_array, y_array, values)
    a = b = np.linspace(-5.12, 5.12, num=50)
    X, Y = np.meshgrid(a, b)
    Z = function(X, Y)
    ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, color="red")
    plt.show()

cp = (0,0)
r = 5
size = 20
p = population(size, cp, r, sphere)

x_array_start = [None]*p.size
y_array_start = [None]*p.size
for i in range(p.size):
    x_array_start[i] = p.population[i][0]
    y_array_start[i] = p.population[i][1]

iterations = 0
while(not p.converges(0.000005)): #and max(p.fitness_values) < 0.99):
    p.print()
    p.recreate(0.95, 0.05)
    iterations+= 1
p.print()
print(iterations, "iterations")

plotGraph(x_array_start, y_array_start, sphere)

x_array_end = [None]*p.size
y_array_end = [None]*p.size
for i in range(p.size):
    x_array_end[i] = p.population[i][0]
    y_array_end[i] = p.population[i][1]
plotGraph(x_array_end, y_array_end, sphere)
