import random


def read_data_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    e = []
    l = []
    d = []
    for i in range(1, n + 1):
        ei, li, di = map(int, lines[i].strip().split())
        e.append(ei)
        l.append(li)
        d.append(di)

    t = []

    for i in range(n + 1, 2 * n + 2):
        row = list(map(int, lines[i].strip().split()))
        t.append(row)

    return n, e, l, d, t


def read_data_from_keyboard():
    n = int(input())
    e = []
    l = []
    d = []
    for _ in range(n):
        ei, li, di = map(int, input().split())
        e.append(ei)
        l.append(li)
        d.append(di)

    t = []

    for _ in range(n+1):
        row = list(map(int, input().split()))
        t.append(row)

    return n, e, l, d, t


def print_data(n, e, l, d, t):
    print(n)
    for ei, li, di in zip(e, l, d):
        print(ei, li, di)
    for row in t:
        print(' '.join(map(str, row)))


filename = "dataset/input10.txt"
n, e, l, d, t = read_data_from_file(filename)
# n, e, l, d, t = read_data_from_keyboard()
e = [0] + e
l = [0] + l
d = [0] + d
inf = 9999999


loop_count = 10000


def generate_init_population(pop_size):
    population = []
    for _ in range(pop_size):
        individual = list(range(1, n + 1))
        random.shuffle(individual)
        i = 0
        while i < loop_count:
            if evaluate([0] + individual + [0]) < inf:
                break
            random.shuffle(individual)
            i += 1
        population.append([0] + individual + [0])
    return population


def fill_position(child, parent, start, end):
    parrent_current = 1
    for current in range(end, n+1):
        while (True):
            if parent[parrent_current] not in child:
                child[current] = parent[parrent_current]
                break
            parrent_current += 1
    for current in range(1, start):
        while (True):
            if parent[parrent_current] not in child:
                child[current] = parent[parrent_current]
                break
            parrent_current += 1


def evaluate(individual):
    current_time = 0
    for i in range(n):
        from_node = individual[i]
        to_node = individual[i+1]
        travel_time = t[from_node][to_node]
        service_time = d[to_node]

        current_time += travel_time
        start_time = e[to_node]
        end_time = l[to_node]

        if current_time > end_time:
            return inf
        if current_time < start_time:
            current_time = start_time

        current_time += service_time

    current_time += t[individual[n]][0]
    return current_time


def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(1, n), 2))

    child1 = [0] + [-1] * n + [0]
    child2 = [0] + [-1] * n + [0]

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    fill_position(child1, parent2, start, end)
    fill_position(child2, parent1, start, end)

    return child1, child2


def mutate(individual, mutation_rate=0.2):
    if random.random() > mutation_rate:
        return individual
    first, second = random.sample(range(1, n), 2)
    individual[first], individual[second] = individual[second], individual[first]
    return individual


def genetic_algorithm(pop_size=100, max_gen=1000, mutation_rate=0.2):
    population = generate_init_population(pop_size)
    for gen in range(max_gen):
        random.shuffle(population)
        next_population = population
        for i in range(0, len(population), 2):
            parent1, parent2 = population[i], population[i+1]
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            next_population.append(child1)
            next_population.append(child2)
        population = sorted(next_population, key=lambda x: evaluate(x))[
            :pop_size]

    best_individual = min(population, key=lambda x: evaluate(x))
    return best_individual, evaluate(best_individual)


if __name__ == '__main__':
    # genetic_algorithm()
    best_individual, best_value = genetic_algorithm()
    print_data(n, e, l, d, t)
    print(n)
    print(" ".join(map(str, best_individual[1:-1])))
