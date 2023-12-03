
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
    ]
]

reserves = [
    [560, 170, 300],
    [120, 280, 240, 360],
    [1411, 149, 815.5, 466, 1080],
    [160, 24]
]

profits = [
    [4, 5],
    [10, 14, 12],
    [1, 0.7, 1, 2, 0.6],
    [1, 3]
]


class SimplexMethod:

    def __init__(self, materials: list, reserve: list, profit: list, objective = 'max'):
        add_vars = len(materials[0])

        # Формируем симплекс-таблицу
        self.simplex_table = [materials[i] + [0 if var != i else 1 for var in range(add_vars)] for i in range(len(materials))]
        self.basis = [i + add_vars for i in range(len(materials))]
        self.profits = [prof for prof in profit] + [0 for _ in range(len(materials))]

        for row in self.simplex_table:
            print(row)

        self.reserve = reserve
        
        print(f"basis: {self.basis}")
        print(f"profits: {self.profits}")
        print(f"reserves: {self.reserve}")

        self.deltas = self.recount_deltas()
        print(f"Delatas: {self.deltas}")

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
    def min_delta_index(self):
        return self.deltas.index(min(self.deltas))

    # Возвращает индекс минимального отношения запасов к количеству на единицу товара
    def min_q_index(self, min_profit_ind: int):
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

    def target_function(self):
        return sum([self.profits[bas_ind] * self.reserve[i] for i, bas_ind in enumerate(self.basis)])
    
    def iteration(self):
        print()
        print("==== Iteration ====")

        min_delta_column = self.min_delta_index()
        print(f"Deltas: {self.deltas}, min index: {min_delta_column}")
        min_q_row = self.min_q_index(min_delta_column)
        print(f"Min Q index: {min_q_row}")
        self.recount_table(min_q_row, min_delta_column)
        print(f"Target function: {self.target_function()}")

    def solve(self):
        while (any(delta < 0 for delta in self.deltas)):
            self.iteration() 
        # self.reserve = [int(res) for res in self.reserve]
        print(f"Target function: {self.target_function()}")


if __name__ == "__main__":
    task_index = 3
    method = SimplexMethod(material_tables[task_index], reserves[task_index], profits[task_index])
    