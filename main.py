import numpy as np
from numpy.random import choice
import random

def TOP_GENES():
    return 10

def check(x, y, height, width):
    return 0 <= x < height and 0 <= y < width


def move(garden, genes, number, height, width):
    counter = 0
    if genes[0] < 2 * width:
        direction = True
        if genes[0] < width:  # dole
            x = 0
            y = genes[0]
            x_inc = 1
            y_inc = 0
        else:  # hore
            x = height - 1
            y = genes[0] - width
            x_inc = -1
            y_inc = 0
    else:
        direction = False
        if genes[0] < 2 * width + height:  # doprava
            y = 0
            x = genes[0] - (2 * width)
            x_inc = 0
            y_inc = 1
        else:  # dolava
            y = width - 1
            x = genes[0] - (2 * width) - height
            x_inc = 0
            y_inc = -1

    if garden[x][y]:
        return counter
    else:
        garden[x][y] = number
        counter += 1

    while True:
        if not check(x + x_inc, y + y_inc, height, width):
            break
        elif garden[x + x_inc][y + y_inc]:
            x_inc, y_inc = y_inc, x_inc
            if direction:           # VERTICAL
                if genes[1]:        # RIGHT
                    x_inc, y_inc = -x_inc, -y_inc
            else:                   # HORIZONTAL
                if not genes[1]:    # LEFT
                    x_inc, y_inc = -x_inc, -y_inc

            if not check(x + x_inc, y + y_inc, height, width) or garden[x + x_inc][y + y_inc]:
                x_inc, y_inc = -x_inc, -y_inc
            if not check(x + x_inc, y + y_inc, height, width) or garden[x + x_inc][y + y_inc]:
                break

            direction = not direction
        else:
            garden[x + x_inc][y + y_inc] = number
            x += x_inc
            y += y_inc
            counter += 1
    return counter

def fitness(genes_numb, monk, height, width, garden):
    rating = 0
    for i in range(genes_numb):
        rating += move(garden, monk[i], i + 1, height, width)
    return rating

def generate_monk(numb_of_genes, circuit):
    monk = []
    for j in range(0, numb_of_genes):
        monk.append((random.randint(0, circuit), bool(random.getrandbits(1))))
    return monk


def reproduction(package, monk_numb, genes_numb, height, width):
    mutation_factor = 2
    reproducted_monks = []

    for i in range(TOP_GENES()):
        reproducted_monks.append(package[i][1])

    sum = 0

    for i in range(monk_numb):
        sum += package[i][0]

    weights = [package[i][0]/sum for i in range(monk_numb)]
    for i in range(monk_numb-TOP_GENES()):

        option_x = option_y = choice(np.arange(0, monk_numb), p=weights)
        x = package[option_x]
        while option_y == option_x:
            option_y = choice(np.arange(0, monk_numb), p=weights)
        y = package[option_y]
        x_indexes = random.sample(range(genes_numb), int(genes_numb/2))
        y_indexes = random.sample(range(genes_numb), int(genes_numb/2))
        if random.randint(0, 100) < mutation_factor:
            reproducted_monks.append(mutate([x[1][x_indexes[i]] for i in range(int(genes_numb / 2))]
                + [y[1][y_indexes[i]] for i in range(int(genes_numb / 2))], genes_numb, height, width))
        else:
            reproducted_monks.append([x[1][x_indexes[i]] for i in range(int(genes_numb / 2))]
                + [y[1][y_indexes[i]] for i in range(int(genes_numb / 2))])
    return reproducted_monks


def mutate(monk, genes_numb, height, width):
    select = [True, False]
    weights = [0.8, 0.2]
    x = random.randint(0, genes_numb-1)
    y = choice(select, p=weights)
    if y:
        monk[x] = list(monk[x])
        monk[x][0] = random.randint(0, ((height + width) * 2) - 1)
        monk[x] = tuple(monk[x])
    else:
        monk[x] = list(monk[x])
        monk[x][1] = not monk[x][1]
        monk[x] = tuple(monk[x])
    return monk


if __name__ == "__main__":
    monks = []
    package = []
    rock_numb = 0

    height = int(input("set y size of the garden: "))
    width = int(input("set x size of the garden: "))

    garden = np.zeros((height, width))

    obscales = [int(i) for i in input("set (x,y) obscales in garden: ").split(" ")]
    for i in range(len(obscales)//2):
        garden[obscales[i]][obscales[i+1]] = -1
        rock_numb += 1

    monk_numb = int(input("set number of monks in one generation: "))
    genes_numb = int(input("set number of genes in one monk: "))
    generation_numb = int(input("set max number of generations: "))

    if genes_numb < int((((height + width) * 2) - 1)/2) + rock_numb:
        garden_temp = np.copy(garden)
        for i in range(monk_numb):
            monks.append(generate_monk(genes_numb, ((height + width) * 2) - 1))

        for i in range(generation_numb):
            ratings = []
            for j in range(monk_numb):
                ratings.append(fitness(genes_numb, monks[j], height, width, garden))
                garden = np.copy(garden_temp)
            package = list(zip(ratings, monks))
            package = sorted(package, key=lambda tup: tup[0], reverse=True)
            print("{}. -> {}".format(i+1, package[0]))
            monks = reproduction(package, monk_numb, genes_numb, height, width)
            if package[0][0] == (height*width)-rock_numb:
                print("BEST CASE: program reached a best case\n")
                break

        garden = np.copy(garden_temp)
        fitness(genes_numb, package[0][1], height, width, garden)
        print(np.array(garden))
    else:
        print("ERROR: number of genes must be less than circle of garden + number of rocks\n")