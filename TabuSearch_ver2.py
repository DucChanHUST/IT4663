import numpy as np
from collections import deque
import sys

class TabuSearchVer2:
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
        self.timeCome = None
        self.orderToCome = []
        self.orderByL = []

    def change_order_to_come(self, high, low, old_order):
        tmp = old_order[high]
        for i in range(high, low, -1):
            old_order[i] = old_order[i - 1]
        old_order[low] = tmp

    def evaluate(self, route):
        currentTime = 0
        for i in range(1, self.N + 1):
            customer = route[i]
            currentTime += self.c[route[i - 1]][customer]
            currentTime = max(currentTime, self.e[customer])
            currentTime += self.d[customer]
            if currentTime > self.l[customer]:
                return sys.maxsize  # Vi phạm điều kiện time window
        return currentTime

    def tabu_search(self, route):
        currentCost = self.evaluate(route)
        bestCost = currentCost
        bestRoute = list(route)

        tabuList = deque()
        tabuTenure = 10

        for iteration in range(1000):
            bestNeighbor = list(bestRoute)
            bestNeighborCost = sys.maxsize

            for i in range(1, self.N):
                for j in range(i + 1, self.N + 1):
                    neighbor = list(bestRoute)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    if neighbor not in tabuList:
                        neighborCost = self.evaluate(neighbor)
                        if neighborCost < bestNeighborCost:
                            bestNeighbor = neighbor
                            bestNeighborCost = neighborCost

            bestRoute = bestNeighbor
            bestCost = bestNeighborCost

            tabuList.append(list(bestRoute))
            if len(tabuList) > tabuTenure:
                tabuList.popleft()

        for i in range(len(bestRoute)):
            route[i] = bestRoute[i]

    def read_input(self):
        with open(self.input_filename, "r") as fin:
            self.N = int(fin.readline().strip())
            self.e = np.zeros(self.N + 1, dtype=int)
            self.l = np.zeros(self.N + 1, dtype=int)
            self.d = np.zeros(self.N + 1, dtype=int)
            self.c = np.zeros((self.N + 1, self.N + 1), dtype=int)
            self.cd = np.zeros((self.N + 1, self.N + 1), dtype=int)
            for i in range(1, self.N + 1):
                self.e[i], self.l[i], self.d[i] = map(int, fin.readline().strip().split())
                self.orderByL.append((self.l[i], i))
            for i in range(self.N + 1):
                self.c[i] = np.array(list(map(int, fin.readline().strip().split())))
                self.cd[i] = self.c[i] + self.d

    def solve(self):
        self.read_input()
        
        self.route = np.zeros(self.N + 1, dtype=int)
        self.timeCome = np.zeros(self.N + 1, dtype=int)
        self.orderToCome = np.zeros(self.N + 1, dtype=int)
        
        self.orderByL.sort()
        for i in range(1, self.N + 1):
            self.orderToCome[i] = self.orderByL[i - 1][1]

        self.route[0] = 0
        self.timeCome[0] = 0
        for i in range(1, self.N + 1):
            nextLocation = self.orderToCome[i]
            selectedLocation = nextLocation
            lastestTimeCome = self.l[selectedLocation]
            selectedTimeCome = max(self.e[selectedLocation], self.timeCome[self.route[i - 1]] + self.cd[self.route[i - 1]][selectedLocation])
            tmp_j = i
            for j in range(i + 1, self.N + 1):
                choice = self.orderToCome[j]
                tmpTimeCome = max(self.e[choice], self.timeCome[self.route[i - 1]] + self.cd[self.route[i - 1]][choice])
                if tmpTimeCome + self.cd[choice][selectedLocation] < lastestTimeCome:
                    lastestTimeCome = tmpTimeCome + self.cd[choice][selectedLocation]
                    selectedLocation = choice
                    selectedTimeCome = tmpTimeCome
                    tmp_j = j
            if selectedLocation != nextLocation:
                self.change_order_to_come(tmp_j, i, self.orderToCome)
            self.route[i] = selectedLocation
            self.timeCome[self.route[i]] = selectedTimeCome

        # Áp dụng Tabu Search để cải thiện giải pháp từ Greedy
        self.tabu_search(self.route)

        # Ghi kết quả cải tiến từ Tabu Search vào file output
        with open(self.output_filename, "w") as fout:
            fout.write(f"{self.N}\n")
            for i in range(1, self.N + 1):
                fout.write(f"{self.route[i]} ")
            fout.write("\n")

if __name__ == "__main__":
    input_filename = "testcase/tutao/test1.txt"  # Đường dẫn đến file đầu vào
    output_filename = "python/test1.txt"  # Đường dẫn đến file đầu ra

    solver = TabuSearchVer2(input_filename, output_filename)
    solver.solve()
