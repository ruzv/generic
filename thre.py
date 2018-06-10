import copy
import random
import multiprocessing
from generic2 import tools
import generic2 as gener


# class for generating the next generation
# used by generate_next_gen function
class generation:

    # population sort front-good, back-bad
    # entity - entity object
    # mutation_times - the ammounth of times a dna is mutated
    # mutation_range - the mutaters range()
    # selection_type - "cut" / "rand"
    # breed_type - "avrg" / "rand"
    # mutate_type - "valu" / "rand"
    def __init__(self, population, entity, mutation_times, mutation_range, selection_type, breed_type, mutate_type):
        self.population = population
        self.entity = entity
        self.i = mutation_times
        self.v = mutation_range
        self.sel = selection_type
        self.bre = breed_type
        self.mut = mutate_type

    # function that defines in what way to select entitys from population
    # that will survive
    # use copy
    # population must be sorted
    def selection_cut(self):
        return self.population[0 : int(len(self.population)/2)]

    # function that defines in what way to select entitys from population
    # that will survive
    # population must be sorted 
    def selection_rand(self):
        self.population.reverse()
        for i in range(0, int(len(self.population)/2)):
            del self.population[tools.pick_entity(len(self.population))]
        self.population.reverse()
        return self.population

    # mutates dna by a set value + || -
    # v - the value
    # i - ammount of times for muation
    # dna - dna
    def mutate_by_val(self, v, i, dna):
        for a in range(i):
            p = random.randint(0, len(dna)-1)
            dna[p] += tools.mutateor(v)
        return dna

    # mutates dna by a value  in range(0, v) + || -
    # v - the value
    # i - ammount of times for muation
    # dna - dna
    def mutate_by_rand(self, v, i, dna):
        for a in range(i):
            p = random.randint(0, len(dna)-1)
            dna[p] += tools.mutater(v)
        return dna

    # breeds together two entitys
    # breeds by takeing the average of two points 
    def breed_by_avg(self):
        par1 = self.population[tools.pick_entity(len(self.population))][1]
        par2 = self.population[tools.pick_entity(len(self.population))][1]
        while par2 == par1:
            par2 = self.population[tools.pick_entity(len(self.population))][1]
        child = []
        for i in range(0, len(par1)):
            child.append((par1[i] + par2[i]) / 2)
        return child

    # breeds together two entitys
    # breeds by adding two lists together at random points
    def breed_by_rand(self):
        par1 = self.population[tools.pick_entity(len(self.population))][1]
        par2 = self.population[tools.pick_entity(len(self.population))][1]
        while par2 == par1:
            par2 = self.population[tools.pick_entity(len(self.population))][1]
        p = tools.reorder(tools.pick_points(len(self.population)-1))
        child = copy.copy(par1)
        child[p[0] : p[1]] = par2[p[0] : p[1]]
        return child

    # choise for breed
    def breed(self, i, output):
        l = []
        for a in range(i):
            if self.bre == "avrg":
                child = self.breed_by_avg()
            else:
                child = self.breed_by_rand()
            if self.mut == "valu":
                child = self.mutate_by_val(self.v, self.i, child)
            else:
                child = self.mutate_by_rand(self.v, self.i, child)
            l.append([self.entity.fitness(self.entity, child), child])
        
        output.put(l)

    #choise for breed
    def selection(self):
        if self.sel == "cut":
            self.population = copy.copy(self.selection_cut())
        else:
            self.population = copy.copy(self.selection_rand())

# function that generates the next generation uses generation class
# population sort front-good, back-bad
# entity - entity object
# mutation_times - the ammounth of times a dna is mutated
# mutation_range - the mutaters range()
# selection_type - "cut" / "rand"
# breed_type - "avrg" / "rand"
# mutate_type - "valu" / "rand"
def breed_next_generation(population, entity, mutation_times, mutation_range, selection_type, breed_type, mutate_type):

    gen = generation(population, entity, mutation_times, mutation_range, selection_type, breed_type, mutate_type)
    gen.selection()

    output = multiprocessing.Queue()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(name=i, target=gen.breed, args=[int(len(gen.population)/4), output])
        processes.append(p)
    for p in processes:
        p.start()

    l = gen.population
    for p in processes:
        l += output.get()
    return l

        

runer = gener.entity([[1, 3]], "brd", [0, 5])
def fitness(self, dna):
    return 0
runer.fitness = fitness


p = gener.generate_population(20, runer)
print(p)
print(len(p))
p = breed_next_generation(p, runer, 1, 10, "rand", "rand", "rand")
print(p)
print(len(p))

