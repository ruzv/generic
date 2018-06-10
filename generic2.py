import random
import math
import threading
import multiprocessing
import copy


# a class with small throw in functions for other to use
class tools:

    # returns pozitive or negative valuse of v
    def mutateor(self, v):
        if random.randint(0, 1) == 1:
            return v
        else:
            return -v

    # returns a random decimal number in range(-v, +v)
    def mutater(self, v):
        v = random.randint(0, v)
        return self.mutateor(v * random.random())

    # returns random number in range(0, size-1) with a larger chance of it beeing small
    # size is the len(population)
    def pick_entity(self, size):
        a = random.random() * random.random() * (size-1)
        return int(a)

    # turns a given number a in range(0, 1)
    def sig(self, a):
        if a > 37:
            return 1.0
        elif a < -600:
            return 0
        else:
            return 1 / (1 + math.exp(-a))

    # reorders elements of list a, len(a) = 2, in decreesing or increesing order
    # order = les/gtr
    def reorder(self, a, order="gtr"):
        if order == "les":
            if a[1] > a[0]:
                return [a[0], a[1]]
        else:
            if a[0] > a[1]:
                return [a[1], a[0]]
        return a

    # picks two diferent points in range(0, rang)
    # rang >= 0
    def pick_points(self, rang):
        a = random.randint(0, rang)
        b = random.randint(0, rang)
        while a == b:
            b = random.randint(0, rang)
        return [a, b]


tools = tools()


# class for generating population used by generate_population() function
class population:

    # entity - object that contains the parameters that define the entity
    def __init__(self, entity):
        self.type = entity.dna_type
        self.entity = entity
        self.range = entity.dna_range
        self.length = entity.length
        self.population = []

    # generates a ammounth of dna, defined by size
    # uses parameters of the entity object
    def add_entity_dna(self, size, output):
        #print(threading.currentThread().getName(), "starting")
        for i in range(size):
            if self.type == "net":
                dna = generate_dna_net(self.length)
            elif self.type == "brd":
                dna = generate_dna_brd(self.length, self.range)
            elif self.type == "net-brd":
                dna = generate_dna_net_brd(self.length, self.range)
            self.population.append([self.entity.fitness(self.entity, dna), dna])
        output.put(self.population)
        #print(threading.currentThread().getName(), "exiting")

# generates dna - list of random number of len(length)
# a - list - [0, 1] defines the random.randint()
def generate_dna_brd(length, a):
    a = tools.reorder(a)
    l = []
    for i in range(length):
        l.append(random.randint(a[0], a[1]))
    return l
# generates dna - list of random number of len(length)
# reqires no a value a = random.random()
def generate_dna_net(length):
    l = []
    for i in range(length):
        l.append(random.random())
    return l
# generates dna - list of random number of len(length)
# uses tools.mutater(a)
def generate_dna_net_brd(lenght, a):
    l = []
    for i in range(lenght):
        l.append(tools.mutater(abs(a[0])))
    return l

# generates all population
# uses entitys objects parameters
# size defines the size of the population
def generate_population(size, entity):
    popul = population(entity)
    output = multiprocessing.Queue()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(name=i, target=popul.add_entity_dna, args=[int(size/4), output,])
        processes.append(p)
    for p in processes:
        p.start()
    
    l = []
    for p in processes:
        l += output.get()
    return l

"""
def generate_population(size, entity, threds):
    popul = population(entity)

    threads = []
    for i in range(threds):
        t = threading.Thread(target = popul.add_entity_dna, args=[int(size/threds),])
        threads.append(t)
    for i in threads:
        i.start()
    while True:
        a = 0
        for i in threads:
            if i.isAlive() == False:
                a += 1
        if a == threds:
            break
    return popul.population
"""

# class where the prameters of an entity/dna are stored
# must contain fitness() function witch can be modified to fit the requirements
class entity():

    # prams - defines the size and structure of the neural net [[1, 3], [3, 1]], [input, output]
    # dna_type - defines the way the weights are generated (more info generate_dna_*() functions)
    # dna_range - parameter used together with dna_type
    def __init__(self, prams, dna_type="brd", dna_range=[0,0]):
        self.prams = prams
        self.dna_type = dna_type
        self.dna_range = dna_range
        self.length = 0
        for i in range(len(self.prams)):
            self.length += self.prams[i][0] * self.prams[i][1]

    # function that takes in the dna and outputs the fitness of it
    fitness = None
    """    
    def fitness(self, dna):
        return 0 # fitness
    """


# a class witch calculates the output of a neural net with set parameters
# class of witch you shoud only call calculate_net()
class net():

    # initalizet networks prams
    # l1 - input layer
    # dna - defines the weights
    # prams - defines the size and length of layers and weights
    def __init__(self, l1, dna, prams):
        self.l1 = l1
        self.dna = dna
        self.prams = prams

    # calculates the next layer
    # l1 - the input layer
    # w - weight matrix
    def calculate_layer(self, l1, w):
        l2 = []
        for l2n in range(0, len(w)):
            a = 0
            for l1n in range(0, len(w[0])):
                a += l1[l1n] * w[l2n][l1n]
            l2.append(tools.sig(a))
        return l2

    # makes a 3d matrix of weights from dna
    def make_weights(self):
        dna = copy.copy(self.dna)
        weights = []
        for i in range(0, len(self.prams)):
            w = []
            for y in range(0, self.prams[i][1]):
                l = []
                for x in range(0, self.prams[i][0]):
                    l.append(dna[0])
                    del dna[0]
                w.append(l)
            weights.append(w)
        return weights

    # calculates the last layer of neural net
    # uses all of the above functions
    def calculate_net(self):
        l = self.l1
        for i in self.make_weights():
            l = self.calculate_layer(l, i)
        return l


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


