from copy import deepcopy


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


class SimplexMethod:

    def __init__(self, materials: list, reserve: list, profit: list, objective = 'max'):
        add_vars = len(materials)
        self.vars_amount = len(materials[0])

        self.solution = {
            "iterations": [],
            "parameters": {}
        }

        self.permissive_column_meth = {
            'max': lambda deltas : deltas.index(min(deltas)),
            'min': lambda deltas : deltas.index(max(deltas))
        }[objective]

        self.is_not_optimal = {
            'max': lambda deltas : any(delta < 0 for delta in deltas),
            'min': lambda deltas : any(delta > 0 for delta in deltas)
        }[objective]

        # Формируем симплекс-таблицу
        self.simplex_table = [materials[i] + [0 if var != i else 1 for var in range(len(materials))] for i in range(len(materials))]
        self.basis = [i + add_vars for i in range(len(materials))]
        if objective == 'max':
            self.profits = [prof for prof in profit] + [0 for _ in range(len(materials))]
        elif objective == 'min':
            self.profits = [-prof for prof in profit] + [0 for _ in range(len(materials))]

        for row in self.simplex_table:
            print(row)

        self.reserve = reserve
        
        print(f"basis: {self.basis}")
        print(f"profits: {self.profits}")
        print(f"reserves: {self.reserve}")

        self.deltas = self.recount_deltas()
        print(f"Delatas: {self.deltas}")
        self.save_iteration()
        self.solve()

    def recount_deltas(self):
        new_deltas = []
        i = 0
        for j in range(len(self.simplex_table[i])):
            sum = 0
            for i in range(len(self.simplex_table)):
                # print(f"{self.simplex_table[i][j]} * {self.profits[self.basis[i]]} + ")
                sum += self.simplex_table[i][j] * self.profits[self.basis[i]]
            sum -= self.profits[j]
            # print(f"Delta[{j}] = {sum}")
            new_deltas.append(sum)
        return new_deltas

    # Возвращает индекс минимального (отрицательного) значения стоимости товара
    def permissive_column(self):
        return self.permissive_column_meth(self.deltas)

    # Возвращает индекс минимального отношения запасов к количеству на единицу товара
    def permissive_row(self, min_profit_ind: int):
        min_index = 0
        min_value = float("inf")
        for i in range(len(self.simplex_table)):
            if self.simplex_table[i][min_profit_ind] <= 0:
                continue
            frac = self.reserve[i] / self.simplex_table[i][min_profit_ind]
            if frac < min_value:
                min_index = i
                min_value = frac
            print(f"Fraction: {frac}, min ind: {min_index}")
        return min_index
    
    # Пересчитывает всю симплекс-таблицу
    def recount_table(self, row_index: int, col_index: int):
        # Изменяем базисные переменные
        self.basis[row_index] = col_index
        print(f"New basis: {self.basis}")

        # Разрешающий элемент
        permissive_element = self.simplex_table[row_index][col_index]

        # Пересчитывем запасы
        new_reserves = []
        for i, reserve in enumerate(self.reserve):
            if i == row_index:
                new_reserves.append(reserve / self.simplex_table[i][col_index])
            else:
                new_reserves.append(reserve - self.reserve[row_index] / permissive_element * self.simplex_table[i][col_index])
        self.reserve = new_reserves
        print(f"New reserves: {self.reserve}")

        # Пересчитываем коэффициенты симплекс-таблицы
        new_simplex_table = [[None for _ in row] for row in self.simplex_table]
        for i in range(len(self.simplex_table)):
            for j in range(len(self.simplex_table[i])):
                if i == row_index:
                    new_simplex_table[i][j] = self.simplex_table[i][j] / permissive_element
                else:
                    new_simplex_table[i][j] = self.simplex_table[i][j] - self.simplex_table[row_index][j] / permissive_element * self.simplex_table[i][col_index]

        self.simplex_table = new_simplex_table
        print("New Simplex table")
        for row in self.simplex_table:
            print(row)

        self.deltas = self.recount_deltas()
        print(f"New deltas: {self.deltas}")

    # Значение целевой функции
    def target_function(self):
        return sum([self.profits[bas_ind] * self.reserve[i] for i, bas_ind in enumerate(self.basis)])
    
    # Итерация
    def iteration(self):
        print()
        print("==== Iteration ====")

        min_delta_column = self.permissive_column()
        print(f"Deltas: {self.deltas}, min index: {min_delta_column}")
        min_q_row = self.permissive_row(min_delta_column)
        print(f"Min Q index: {min_q_row}")
        self.recount_table(min_q_row, min_delta_column)
        print(f"Target function: {self.target_function()}")

    # Сохранение данных текущей итерации
    def save_iteration(self):
        self.solution["iterations"].append( 
            {
                "simplex_table": deepcopy(self.simplex_table),
                "basis": deepcopy(self.basis),
                "deltas": deepcopy(self.deltas),
                "reserves": deepcopy(self.reserve),
                "function": self.target_function(),
                "profits": deepcopy(self.profits)
            }
        )

    def save_results(self):
        parameters = {self.basis[i]: self.reserve[i] for i in range(len(self.basis))}
        real_keys = []
        for key in sorted(parameters.keys()):
            if key < self.vars_amount:
                real_keys.append(key)
        parameters = {key: parameters[key] for key in real_keys}
        self.solution["parameters"] = parameters
        self.solution["function"] = self.target_function()

    def solve(self):
        while (self.is_not_optimal(self.deltas)):
            self.iteration()
            self.save_iteration()
        self.save_results()
        print(f"Target function: {self.target_function()}")


if __name__ == "__main__":
    task_index = 4
    method = SimplexMethod(material_tables[task_index], 
                           reserves[task_index], 
                           profits[task_index], 
                           'min')
    # for iter in method.iterations:
    #     print(iter)
    