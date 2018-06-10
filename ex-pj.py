import generic2 as gener
import copy
import game
import time

runer = gener.entity([[4, 8], [8, 8], [8, 4]], "net-brd", [200])
runer.arena = game.maze(400, 400, False)

def fitness(self, dna):
    self.arena.init_chaser(50, 50, 5)
    self.arena.init_runer(200, 200, 5, dna, self.prams)
    return self.arena.main()

runer.fitness = fitness

size = 3000

population = gener.generate_population(size, runer)
population.sort()
population.reverse()
print(population[0][0])

i = 0
while population[0][0] < 15000:
    i += 1
    start = time.time()
    population = gener.breed_next_generation(population, runer, 200, 200, "cut", "rand", "rand")
    population.sort()
    population.reverse()
    print(i, population[0][0], time.time()-start)


print(population[0][1])
arena = game.maze(400, 400, True, 40)
arena.init_chaser(50, 50, 5)
arena.init_runer(200, 200, 5, population[0][1], runer.prams)
print(arena.main())