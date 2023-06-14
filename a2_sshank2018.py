"""
Name: Sadie Shank
Course: CAP 4630
Date: 06.07.23
Instructor: Dr. Oge
Assignment #: 2

Description: This is a program that performs the traveling salesman problem using the genetic algorithm. I started with the towardsdatascience source which I 
have listed below in my source list, and I worked on that to create code that is unique in its own way. There are still some aspects to my starter code
that are still apparent in the code below, but for the most part I changed it. One major difference is that I decided to implement tournament selection
instead of using fitness proportionate selection. 

Sources: 
https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
https://levelup.gitconnected.com/how-to-implement-a-traveling-salesman-problem-genetic-algorithm-in-python-ea32c7bef20f
https://www.geeksforgeeks.org/traveling-salesman-problem-using-genetic-algorithm/
"""

import random
import math

#This is the city class that defines my x and y coordinates. 
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

#This shuffles all of the routes in the city list and returns a random one
def create_random_route(city_list):
    route = city_list[:]
    random.shuffle(route)
    return route

#This calculates the distance between cities in a route
def calculate_distance(route):
    total_distance = 0
    num_cities = len(route)

    #This shuffles through all the cities in the route and then calculates the distance using the pythagorean theorem
    for i in range(num_cities):
        current_city = route[i]
        next_city = route[(i + 1) % num_cities]
        distance = math.sqrt((next_city.x - current_city.x) ** 2 + (next_city.y - current_city.y) ** 2)
        total_distance += distance

    return total_distance

#This creates the initial population, which is a collection of all possible routes
def create_initial_population(pop_size, city_list):
    population = []
    #This is creating a random route and appending it to the population for as many routes as we wanted, so there are many random routes
    #If we input 20 routes, then this creates 20 random routes
    for _ in range(pop_size):
        population.append(create_random_route(city_list))
    #We then return this new population that has a collection of a set number of random routes

    return population

#For every route in the population (ie. 20 routes if we input 20 for pop_size), we calculate the distance for that route.
# I went and added those values to the fitness_values structure that keeps
#track of all the different fitnesses and then I added the distance up so there is a total distance for each route. 
def evaluate_population(population):
    fitness_values = []
    for route in population:
        distance=calculate_distance(route)
        fitness_values.append(distance)
    return fitness_values

#This is my selection algorithm, it utilizes the fitness_values that were created in the last function to calculate the min fitness. 
#It then creates the list of parents and sets the fitness to a high number so it can start at scratch for the next step and not mess up that
# minimum fitness.  
def selection(population, fitness_values, num_parents):
    parents = []
    for _ in range(num_parents):
        min_fitness_index = fitness_values.index(min(fitness_values))
        if min_fitness_index < len(population):
            parents.append(population[min_fitness_index])
            #I set this to a super small number so it doesn't mess up the min
            #It keeps adding the smallest fitness index to the parents and then modifying that so
            #it is not chosen again. In this way, only the smallest are chosen. 
            fitness_values[min_fitness_index] = float(999999)
    return parents


#This takes the parents and performs a crossover so that offspring is chosen from each side which leads to diversity in selection 
#This is order crossover and it is taking a random part of parent 1 and then pulling the rest of the cities from parent 2
def crossover(parents, offspring_size):
    offspring = []
    if len(parents) == 0 or len(parents[0]) == 0:
        return offspring

    num_cities = len(parents[0])

    for _ in range(offspring_size):
        parent1, parent2 = random.sample(parents, 2)
        start_index = random.randint(0, num_cities - 1)
        end_index = random.randint(start_index, num_cities - 1)

        offspring.append(parent1[start_index:end_index]+[city for city in parent2 if city not in parent1[start_index:end_index]])

    return offspring


#Takes in the offspring that the crossover returned, along with the mutation_rate, to perform mutation
def mutation(offspring, mutation_rate):
    mutated_offspring = []
    num_cities = len(offspring[0])

    #This swaps individuals to provide more routes for the program to look at than if there was no mutation
    for individual in offspring:
        if random.random() < mutation_rate:
            i, j = random.sample(range(num_cities), 2)
            individual[i], individual[j] = individual[j], individual[i]
        mutated_offspring.append(individual)

    return mutated_offspring

#This is similar to a driver function, it calls everything in a loop so it can bring down the distance. Specifically, and this is my genetic algorithm function 
# itself which calls each individual function in its proper place
def tsp_ga(city_list, pop_size, num_generations, num_parents, offspring_size, mutation_rate):
    #This creates the initial population
    population = create_initial_population(pop_size, city_list)

    #This is evaluating the fitness of that initial population
    fitness_values = evaluate_population(population)

    for _ in range(num_generations):
        #This selects the parents
        parents = selection(population, fitness_values, num_parents)

        #This creates the offspring through crossover
        offspring = crossover(parents, offspring_size)

        #This takes the offspring that was produced through crossover and does mutation on it
        mutated_offspring = mutation(offspring, mutation_rate)

        #Finally, this creates the new population by combining parents and the offspring that was previously mutated 
        #This then puts it back through the loop
        population = parents + mutated_offspring

    # This selects the best route from the final population
    best_route = min(population, key=calculate_distance)

    #This prints out the final distance once all the calculations have been made
    final_distance = calculate_distance(best_route)
    print("Final Distance:", final_distance)

    return best_route

#This works like a driver and sets the values and calls the tsp_ga function that runs it all
city_list = []
for i in range(0,25):
    city_list.append(City(x=int(random.random() * 200), y=int(random.random() * 200)))

#I had issues with my input values, so I changed it so that the num_parents and the offspring_size is dependent on other variables. 
pop_size = int(input("Enter the population size: "))
num_generations = int(input("Enter the number of generations: "))
num_parents = int(0.1 * pop_size)
offspring_size = pop_size
mutation_rate = float(input("Enter the mutation rate: "))

initial_distance = calculate_distance(city_list)

print("Initial Distance: ", initial_distance)

#This calls the entire program
best_route = tsp_ga(city_list, pop_size, num_generations, num_parents, offspring_size, mutation_rate)