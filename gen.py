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


# -------------------------------------------------
# funcitons for determenig the fitness of an entity

#fitness fucn for gening a word, takes the target world as target


#tests the output of the net by the table
# table = [[[input], [expected output]], [[input], [expected output]]]


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


# calculates the output of the net, takes in l1 as the first layer/ input, prams for generating the weights
# uses the generate_weights fucntion, iterate fucnton



# --------------------------------------------------
# funcitons for changeing the entitys dna

#a sub fucntion used to negative or positive values of v


#randomy changes one point by v, of a numbers list




#randomy changes one point by v, of a numbers list
#does it for n times


def mutate_net(dna, v, n):
    for i in range(n):
        p = random.randint(0, len(dna)-1)
        dna[p] += mutateor(v)
    return dna


# ---------------------------------------------------
# fucntions for generating lists of dna and their fitness

# generates list of dnas [fitness_value, dna] uses the generate_dna_int funciton
# and the fitness_str() function, takes in size for len of list and target for the fitness function





# ---------------------------------------------------------
# functions used for breeding two dnas

# randomly chooses a number between 0 and size with a grater chance of it beeing small 


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



