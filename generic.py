import random
import math
import copy


# this is a setup file.
# the functions in here can be used
# or the file can be inported

# contains functions as:
# generate_dna_int()
# generate_dna_weights()
# fitness_str()
# fitness_net()
# draw()
# generate_entity_str()
# generate_entity_net()
# mutateor()
# mutate_str()
# mutate2_str()
# mutate_net()
# generate_population_str()
# generate_population_net()
# pick_entity()
# pick_brake_points()
# breed()
# sig()
# iterate()
# generate_weights
# mutater()
# generate_dna_net()
# selection()


# -----------------------------------------------
# functions for generating difrent types of lists

#integers in range(a, b)
def generate_dna_int(length, a, b):
    l = []
    for i in range(length):
        l.append(random.randint(a, b))
    return l

#decimals in range(0, 1)
def generate_dna_weights(length):
    l = []
    for i in range(length):
        l.append(mutateor(1) * random.random())
    return l

def generate_dna_net(prams):
    length = 0
    for i in range(0, len(prams)):
        length += prams[i][0] * prams[i][1]
    l = []
    for i in range(length):
        l.append(mutateor(1) * random.random())
    return l


# -------------------------------------------------
# funcitons for determenig the fitness of an entity

#fitness fucn for gening a word, takes the target world as target
def fitness_str(dna, target):
    en = generate_entity_str(dna)
    f = 0
    for i in range(len(en)):
        f += (ord(target[i]) - dna[i])**2
    return f

#tests the output of the net by the table
# table = [[[input], [expected output]], [[input], [expected output]]]
def fitness_net(table, dna, prams):
    e = 0
    for t in range(0, len(table)):
        output = generate_entity_net(dna, prams, table[t][0])
        for n in range(0, len(table[0][1])):
            e += abs(table[t][1][n] - output[n])
    return e**2


def draw(table, dna, prams):
    print(dna)
    for i in range(0, len(table)):
        output = round_list(generate_entity_net(dna, prams, table[i][0]))
        print(table[i], output)

def round_list(dna):
    l = []
    for i in range(0, len(dna)):
        l.append(round(dna[i], 2))
    return l


# --------------------------------------------------
# functions for generateing the entity from an dna

#gens a str from list of inegers
def generate_entity_str(dna):
    e = ""
    for i in range(0, len(dna)):
        e += chr(dna[i])
    return e

# calculates the output of the net, takes in l1 as the first layer/ input, prams for generating the weights
# uses the generate_weights fucntion, iterate fucnton
def generate_entity_net(dna, prams, l1):
    ws = generate_weights(prams, dna)
    for i in range(0, len(ws)):
        l1 = copy.copy(iterate(l1, ws[i]))
    return l1


# --------------------------------------------------
# funcitons for changeing the entitys dna

#a sub fucntion used to negative or positive values of v
def mutateor(v):
    if random.randint(0, 1) == 1:
        return v
    else:
        return -v

#randomy changes one point by v, of a numbers list
def mutate_str(dna, v):
    a = random.randint(0, len(dna)-1)
    b = mutateor(v)
    while dna[a]+b < 0:
        a = random.randint(0, len(dna)-1)
        b = mutateor(v)
    dna[a] += b
    return dna

def mutater(a):
    a = random.randint(0, a)
    b = random.random()
    return a * b * mutateor(1)

#randomy changes one point by v, of a numbers list
#does it for n times
def mutate2_str(dna, v, n):
    for i in range(n):
        a = random.randint(0, len(dna)-1)
        b = mutateor(v)
        while dna[a]+b < 0:
            a = random.randint(0, len(dna)-1)
            b = mutateor(v)
        dna[a] += b
    return dna

def mutate_net(dna, v, n):
    for i in range(n):
        p = random.randint(0, len(dna)-1)
        dna[p] += mutateor(v)
    return dna


# ---------------------------------------------------
# fucntions for generating lists of dna and their fitness

# generates list of dnas [fitness_value, dna] uses the generate_dna_int funciton
# and the fitness_str() function, takes in size for len of list and target for the fitness function
def generate_population_str(size, target):
    l = []
    for i in range(size):
        dna = generate_dna_int(len(target), 0, 100)
        l.append([fitness_str(dna, target), dna])
    return l

def generate_population_net(size, prams, table):
    length = 0
    for i in range(0, len(prams)):
        length += prams[i][0] * prams[i][1]
    l = []
    for i in range(size):
        dna = generate_dna_weights(length)
        l.append([fitness_net(table, dna, prams), dna])
    return l




# ---------------------------------------------------------
# functions used for breeding two dnas

# randomly chooses a number between 0 and size with a grater chance of it beeing small 
def pick_entity(size):
    a = random.random() * random.random() * (size-1)
    return int(a)

# choose two different points in range(0, size), always in increesing order
def pick_brake_points(size):
    a = random.randint(0, size-1)
    b = random.randint(0, size-1)
    while b == a:
        b = random.randint(0, size-1)
    if a > b:
        a, b = b, a
    return a, b

# randomly chooses tow different dnas and joins them in random points using the pick_brake_points_function
# and pick_entity fucntion
def breed(population):
    a = pick_entity(len(population))
    b = pick_entity(len(population))
    while b == a:
        b = pick_entity(len(population))
    p1, p2 = pick_brake_points(len(population))
    child = copy.copy(population[a][1])
    child[p1 : p2] = population[b][1][p1 : p2]
    return child


def selection(population):
    select = population[0 : int(len(population)/2)]
    return select

"""
population
sel = selection(population)
for i in range(int(len(population)/2)):
    l.append(breed(sel))
population = sel + l
"""

    
# ----------------------------------------------------------------
# functions for generating and makeing and using neural nets

# funcitn that takes an num and turns it in to an float in range(0, 1)
def sig(a):
    if a > 37:
        return 1.0
    elif a < -600:
        return 0
    else:
        return 1 / (1 + math.exp(-a))

# function that preforms a matrix multiplication between layers generating the second layer 
# uses the sig fucntion
""" 
l1 = [1, 1]
w1 = [
    [1, 1],
    [0, 0],
    [0, 0]]
l2 = [0, 0, 0]
"""
def iterate(l1, w1):
    l2 = []
    for y in range(0, len(w1)):
        a = 0
        for x in range(0, len(w1[0])):
            a += l1[x] * w1[y][x]
        l2.append(sig(a))
    return l2

# function that generates weights form a list of weights and instructions of the ammounth
# and size of the weights in prams 
# [[x, y], [x, y]]
""" 
       y
l1 = [1, 1]
w1 = [
       x
    [1, 1],
    [0, 0], y
    [0, 0]]
        y
l2 = [0, 0, 0]
"""
def generate_weights(prams, dn):
    dna = copy.copy(dn)
    ret = []
    for i in range(0, len(prams)):
        w1 = []
        for y in range(prams[i][0]):
            w = []
            for x in range(prams[i][1]):
                w.append(dna[0])
                del dna[0]
            w1.append(w)
        ret.append(w1)
    return ret


