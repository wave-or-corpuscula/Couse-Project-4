import numpy as np


material_tables = [
    [
        [2, 4],
        [1, 1],
        [2, 1]
    ],
    [
        [2, 4, 5],
        [1, 8, 6],
        [7, 4, 5],
        [4, 6 ,7]
    ],
    [
        [0.8, 0.5, 1, 2, 1.1],
        [0.2, 0.1, 0.1, 0.1, 0.2],
        [0.3, 0.4, 0.6, 1.3, 0.05],
        [0.2, 0.3, 0.3, 0.7, 0.5],
        [0.7, 0.1, 0.9, 1.5, 0]
    ],
    [
        [0.1, 0.4],
        [0.01, 0.04]
    ],
    [
        [3, 2],
        [2, 5]
    ]
]

reserves = [
    [560, 170, 300],
    [120, 280, 240, 360],
    [1411, 149, 815.5, 466, 1080],
    [160, 24],
    [18, 20]
]

profits = [
    [4, 5],
    [10, 14, 12],
    [1, 0.7, 1, 2, 0.6],
    [1, 3],
    [-2, -3]
]


class EvolutionAlgorithm:

    def __init__(self, 
                 profits: list, 
                 constraints: list, 
                 reserves: list, 
                 population_size: int = 1000,
                 bounds: tuple = (0, 1000),
                 num_generations: int = 100,
                 mutation_rate: float = 0.1,
                 tournament_size: int = 10):
        self.profits = profits
        self.constraints = constraints
        self.reserves = reserves
        self.population_size = population_size
        self.bounds = bounds
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.solution = {}
        self.genetic_algorithm()
        

    # Функция для вычисления значения целевой функции
    def objective_function(self, arg: list):
        return np.dot(arg, self.profits)

    # Функция для проверки ограничений
    def in_constraints(self, arg: list):
        return np.all(np.dot(self.constraints, arg) <= self.reserves)

    # Функция для создания начальной популяции
    def initialize_population(self):
        valid_population = []
        num_variables = len(self.profits)
        while len(valid_population) < self.population_size:
            new_individual = np.random.uniform(low=self.bounds[:, 0], high=self.bounds[:, 1], size=num_variables)
            if self.in_constraints(new_individual):
                valid_population.append(new_individual)
        return np.array(valid_population)

    # Функция для выбора особей с использованием турнирного отбора
    def tournament_selection(self, population: list, fitness: list):
        selected_indices = []
        for _ in range(len(population)):
            tournament_indices = np.random.choice(len(population), self.tournament_size, replace=False)
            tournament_fitness = [fitness[i] for i in tournament_indices]
            selected_indices.append(tournament_indices[np.argmax(tournament_fitness)])
        return selected_indices

    # Функция для скрещивания двух родителей
    def crossover(self, parent1: list, parent2: list):
        crossover_point = np.random.randint(1, len(parent1))
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return child

    # Функция для мутации
    def mutate(self, child: list, gen_num: int):
        mutation_mask = np.random.rand(len(child)) < self.mutation_rate
        child[mutation_mask] += np.random.uniform(low=-10 / (gen_num + 1), high=10 / (gen_num + 1), size=np.sum(mutation_mask))
        zero_koef = np.random.uniform(0, 1) < self.mutation_rate
        if zero_koef:
            child[np.random.randint(len(child))] = 0
        return child

    # Генетический алгоритм
    def genetic_algorithm(self):
        population = self.initialize_population()
        print("Initialized!")
        
        best_solution = None
        best_fitness = float('-inf')  # Инициализация с минус бесконечностью
        
        for generation in range(num_generations):
            fitness = [self.objective_function(ind) for ind in population]
            
            # Проверка ограничения на лучшие особи
            current_best_index = np.argmax(fitness)
            current_best_fitness = fitness[current_best_index]
            if current_best_fitness > best_fitness:
                best_solution = population[current_best_index]
                best_fitness = current_best_fitness

            # Выбор лучших особей с использованием турнирного отбора
            selected_indices = self.tournament_selection(population, fitness)
            selected_population = population[selected_indices]
            
            # Создание новой популяции с использованием скрещивания и мутации
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = selected_population[np.random.choice(len(selected_population), 2, replace=False)]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                child1 = self.mutate(child1, generation)
                child2 = self.mutate(child2, generation)
                if self.in_constraints(child1):
                    new_population.extend([child1])
                if self.in_constraints(child2):
                    new_population.extend([child2])
            
            # Применение границ переменных
            new_population = np.clip(new_population, self.bounds[:, 0], self.bounds[:, 1])
            population = np.array(new_population)

        self.best_solution = best_solution
        self.best_fitness = best_fitness

# Параметры генетического алгоритма
population_size = 1000
num_generations = 30
mutation_rate = 0.5
tournament_size = 100

task_index = 2

# Границы переменных (x1 >= 0, x2 >= 0)
variable_bounds = np.array([[0, 1000] for _ in range(len(profits[task_index]))])

# Запуск генетического алгоритма


# variable_bounds = np.array([x_bounds, y_bounds, z_bounds])
method = EvolutionAlgorithm(
    profits=profits[task_index],
    constraints=material_tables[task_index],
    reserves=reserves[task_index],
    population_size=population_size,
    bounds=variable_bounds,
    mutation_rate=mutation_rate,
    tournament_size=tournament_size
)

print("Решение (x1, x2, x3):", method.best_solution)
print("Значение целевой функции (доход):", method.best_fitness)

