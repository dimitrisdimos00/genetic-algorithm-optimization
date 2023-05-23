import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from population import population

# rastrigin search domain: -5.12 <= x,y <= 5.12, min: f(0,0) = 0
def rastrigin(x, y):
    return 20 + x**2 - 10*np.cos(2*np.pi*x) + y**2 - 10*np.cos(2*np.pi*y)
# ackley search domain: -5 <= x,y <= 5, min: f(0,0) = 0
def ackley(x, y):
    return -20 * np.exp( -0.2 * np.sqrt( 0.5 * (x ** 2 + y ** 2))) - np.exp( 0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.exp(1) + 20
# sphere search domain: -inf <= x,y <= +inf, min: f(0,0) = 0
def sphere(x, y):
    return x**2 + y**2
# booth search domain: -10 <= x,y <= 10, min: f(1,3) = 0
def booth(x, y):
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

def plotGraph(population, function):    
    x_array = [None]*population.size
    y_array = [None]*population.size
    for i in range(population.size):
        x_array[i] = population.population[i][0]
        y_array[i] = population.population[i][1]
    ax = plt.figure().add_subplot(projection='3d')
    for i in range(len(x_array)):
        values = function(x_array[i], y_array[i])
    ax.scatter(x_array, y_array, values)
    a = b = np.linspace(-5.12, 5.12, num=50)
    X, Y = np.meshgrid(a, b)
    Z = function(X, Y)
    ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, color="red")
    # plt.show()

# population variables
central_point = (0,0)
radius = 4
size = 100
function = sphere

# recreation variables
crossover_probability = 0.95
mutation_probability = 0.1
standard_deviation_limit = 0.01


p = population(size, central_point, radius, function)
plotGraph(p, function)
iterations = 0
while(not p.converges(standard_deviation_limit)): #and max(p.fitness_values) < 0.99):
    p.print()
    p.recreate(crossover_probability, mutation_probability)
    iterations+= 1
p.print()
print(iterations, "iterations")
plotGraph(p, function)
plt.show()
