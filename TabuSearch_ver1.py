import sys
import numpy as np
from collections import deque

class TabuSearchVer1:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.N = 0
        self.e = None
        self.l = None
        self.d = None
        self.c = None
        self.cd = None
        self.route = None

    def read_input(self):
        with open(self.input_filename, 'r') as fin:
            self.N = int(fin.readline().strip())
            self.e = np.zeros(self.N + 1, dtype=int)
            self.l = np.zeros(self.N + 1, dtype=int)
            self.d = np.zeros(self.N + 1, dtype=int)
            self.c = np.zeros((self.N + 1, self.N + 1), dtype=int)
            self.cd = np.zeros((self.N + 1, self.N + 1), dtype=int)
            for i in range(1, self.N + 1):
                self.e[i], self.l[i], self.d[i] = map(int, fin.readline().strip().split())
            for i in range(self.N + 1):
                self.c[i] = np.array(list(map(int, fin.readline().strip().split())))
                self.cd[i] = self.c[i] + self.d

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

    def tabu_search(self, fout):
        currentRoute = np.copy(self.route[:self.N + 1])
        currentCost = self.evaluate(currentRoute)
        bestRoute = np.copy(currentRoute)
        bestCost = currentCost

        tabuList = deque()
        tabuTenure = 10
        maxIterations = 1000
        iteration = 0

        while iteration < maxIterations:
            bestNeighbor = np.copy(currentRoute)
            bestNeighborCost = sys.maxsize

            for i in range(1, self.N + 1):
                for j in range(i + 1, self.N + 1):
                    neighbor = np.copy(currentRoute)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    if not any(np.array_equal(neighbor, t) for t in tabuList):
                        neighborCost = self.evaluate(neighbor)
                        if neighborCost < bestNeighborCost:
                            bestNeighbor = np.copy(neighbor)
                            bestNeighborCost = neighborCost

            if bestNeighborCost < bestCost:
                bestRoute = np.copy(bestNeighbor)
                bestCost = bestNeighborCost

            currentRoute = np.copy(bestNeighbor)
            currentCost = bestNeighborCost

            tabuList.append(np.copy(currentRoute))
            if len(tabuList) > tabuTenure:
                tabuList.popleft()

            iteration += 1

        fout.write(f"{self.N}\n")
        for i in range(1, self.N + 1):
            fout.write(f"{bestRoute[i]} ")
        fout.write("\n")

    def solve(self):
        try:
            self.read_input()
        except FileNotFoundError:
            print("Không thể mở file đầu vào!", file=sys.stderr)
            return 1

        self.route = np.zeros(self.N + 1, dtype=int)
        orderByL = [(self.l[i], i) for i in range(1, self.N + 1)]
        orderByL.sort()
        for i in range(1, self.N + 1):
            self.route[i] = orderByL[i - 1][1]

        try:
            with open(self.output_filename, 'w') as fout:
                self.tabu_search(fout)
        except IOError:
            print("Không thể tạo file đầu ra!", file=sys.stderr)
            return 1

        return 0

if __name__ == "__main__":
    input_filename = "testcase/tutao/test1.txt"  # Đường dẫn đến file đầu vào
    output_filename = "python/test1.txt"  # Đường dẫn đến file đầu ra

    solver = TabuSearchVer1(input_filename, output_filename)
    solver.solve()
