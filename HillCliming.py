import sys

class HillClimbingSolver:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.N = 0
        self.e = []
        self.l = []
        self.d = []
        self.c = []
        self.cd = []
        self.route = []

    def read_input(self):
        with open(self.input_filename, 'r') as fin:
            self.N = int(fin.readline().strip())
            self.e = [0] * (self.N + 1)
            self.l = [0] * (self.N + 1)
            self.d = [0] * (self.N + 1)
            self.c = [[0] * (self.N + 1) for _ in range(self.N + 1)]
            self.cd = [[0] * (self.N + 1) for _ in range(self.N + 1)]
            self.route = [0] * (self.N + 1)

            for i in range(1, self.N + 1):
                self.e[i], self.l[i], self.d[i] = map(int, fin.readline().strip().split())
            for i in range(1, self.N + 1):
                line = list(map(int, fin.readline().strip().split()))
                for j in range(1, self.N + 1):
                    self.c[i][j] = line[j-1]
                    self.cd[i][j] = self.c[i][j] + self.d[j]

    def evaluate(self, route):
        currentTime = 0
        totalDistance = 0
        for i in range(1, self.N + 1):
            prev = route[i - 1]
            next = route[i]
            currentTime += self.c[prev][next]
            currentTime = max(currentTime, self.e[next])
            currentTime += self.d[next]
            if currentTime > self.l[next]:
                return sys.maxsize
            totalDistance += self.c[prev][next]
        return totalDistance

    def hill_climbing(self):
        currentRoute = self.route[:self.N + 1]
        currentCost = self.evaluate(currentRoute)
        improved = True

        while improved:
            improved = False
            for i in range(1, self.N):
                for j in range(i + 1, self.N + 1):
                    currentRoute[i], currentRoute[j] = currentRoute[j], currentRoute[i]
                    newCost = self.evaluate(currentRoute)
                    if newCost < currentCost:
                        currentCost = newCost
                        improved = True
                    else:
                        currentRoute[i], currentRoute[j] = currentRoute[j], currentRoute[i]

        with open(self.output_filename, 'w') as fout:
            fout.write(f"{self.N}\n")
            for i in range(1, self.N + 1):
                fout.write(f"{currentRoute[i]} ")
            fout.write("\n")

    def solve(self):
        try:
            self.read_input()
        except FileNotFoundError:
            print("Không thể mở file đầu vào!")
            return 1

        # Khởi tạo lời giải bằng sắp xếp đơn giản
        orderByL = [(self.l[i], i) for i in range(1, self.N + 1)]
        orderByL.sort()
        for i in range(1, self.N + 1):
            self.route[i] = orderByL[i - 1][1]

        try:
            self.hill_climbing()
        except Exception as e:
            print(f"Không thể tạo file đầu ra: {e}")
            return 1

        return 0

if __name__ == "__main__":
    input_filename = "testcase/tutao/test1.txt"  # Đường dẫn đến file đầu vào
    output_filename = "python/test1.txt"  # Đường dẫn đến file đầu ra

    solver = HillClimbingSolver(input_filename, output_filename)
    solver.solve()
