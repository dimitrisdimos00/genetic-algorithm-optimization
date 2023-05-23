import numpy as np
import random

class population:
    def __init__(self, size, central_point, radius, function, mode="min"):
        self.size = size
        self.function = function
        self.mode = mode
        x_min = central_point[0] - radius
        x_max = central_point[0] + radius
        y_min = central_point[1] - radius
        y_max = central_point[1] + radius
        self.population = []
        current_size = 0
        while (current_size < size):
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            d = np.sqrt((central_point[0] - x)**2 + (central_point[1] - y)**2)
            if (d <= radius):
                self.population.append((x, y))
                current_size +=1

        self.fitness_values = [None] * self.size
        self.average = 0
        self.evaluate()

    def evaluate(self):
        if(self.mode == "min"):
            # find the fitness value F(x) = 1 / (1 + f(x)) for minimum
            for i in range(self.size):
                self.fitness_values[i] = (1 / (1 + self.function(self.population[i][0], self.population[i][1])))
        else:
            # find the fitness value F(x) = f(x) for maximum
            for i in range(self.size):
                self.fitness_values[i] = self.function(self.population[i][0], self.population[i][1])
        self.average = sum(self.fitness_values) / self.size

    def recreate(self, crossover_probability, mutation_probability):
        def crossover(g1, g2, alpha=0.5):
            # g1_chance = random.uniform(0,1)
            # if (g1_chance > 0.5):
            #     return g1
            # return g2
            gamma = random.uniform(-alpha, 1 + alpha)
            return gamma * g1 + (1 - gamma) * g2
        n = self.size
        selection_probability = [None] * n
        value_sum = sum(self.fitness_values)
        for i in range(n):
            selection_probability[i] = self.fitness_values[i] / value_sum
        
        cummulative_probability = [None] * n
        prob_sum = selection_probability[0]
        for i in range(0, n):
            cummulative_probability[i] = prob_sum
            prob_sum += selection_probability[i]
        
        mates = [None] * n
        for j in range(n):
            # find the index of the element to be selected with roulette method
            index = 0
            r = random.uniform(0, 1)
            for i in range(1, n):
                if cummulative_probability[i - 1] < r and r <= cummulative_probability[i]:
                    index = i
            mates[j] = self.population[index]

        new_population = mates.copy()

        # crossovers
        parent1 = parent2 = False
        parent1_index = parent2_index = 0
        for i in range(n):
            if random.uniform(0, 1) <= crossover_probability:
                if not parent1:
                    parent1_index = i
                    parent1 = True
                elif not parent2:
                    parent2_index = i
                    parent2 = True
                else:
                    offspring1 = (crossover(mates[parent1_index][0], mates[parent2_index][0]), crossover(mates[parent1_index][1], mates[parent2_index][1]))
                    offspring2 = (crossover(mates[parent1_index][0], mates[parent2_index][0]), crossover(mates[parent1_index][1], mates[parent2_index][1]))
                    new_population[parent1_index] = offspring1
                    new_population[parent2_index] = offspring2
                    parent1 = parent2 = False
        
        # mutations
        for i in range(n):
            if random.uniform(0, 1) <= mutation_probability:
                m = (new_population[i][1], new_population[i][0])
                new_population[i] = m
        
        self.population = new_population
        self.evaluate()
    
    def converges(self, limit):
        def standard_deviation(values):
            n = len(values)
            mean = sum(values) / n
            diff = [i - mean for i in values]
            diff_2 = [x ** 2 for x in diff]
            my_sum = sum(diff_2)
            return np.sqrt(my_sum / n)
        
        x_array = self.population[:][0]
        y_array = self.population[:][1]
        if standard_deviation(x_array) <= limit and standard_deviation(y_array) <= limit:
            return True
        return False

    def print(self):
        # for i in range(self.size):
            # print("no.", i + 1, self.population[i])
            # print(self.population[i])
        fvmin = min(self.fitness_values)
        fvmax = max(self.fitness_values)
        indmax = self.fitness_values.index(fvmax)
        indmin = self.fitness_values.index(fvmin)
        print("average:", self.average, ",max fitness value: ", fvmax, "of candidate: ", self.population[indmax])