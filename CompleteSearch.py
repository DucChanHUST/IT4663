class Solver:
    def __init__(self, filename):
        self.MAX_N = 1000
        self.N = 0
        self.e = [0] * (self.MAX_N + 1)
        self.l = [0] * (self.MAX_N + 1)
        self.d = [0] * (self.MAX_N + 1)
        self.t = [[0] * (self.MAX_N + 1) for _ in range(self.MAX_N + 1)]
        self.s = [0] * (self.MAX_N + 1)
        self.visited = [False] * (self.MAX_N + 1)
        self.C = [[0] * (self.MAX_N + 1) for _ in range(self.MAX_N + 1)]
        self.M = [0] * (self.MAX_N + 1)
        self.BEST = 1000000000
        self.path = [0] * (self.MAX_N + 1)
        self.Cmin = 1000000000

        self.input(filename)

    def input(self, filename):
        with open(filename, 'r') as fin:
            self.N = int(fin.readline().strip())
            for i in range(1, self.N + 1):
                self.e[i], self.l[i], self.d[i] = map(int, fin.readline().strip().split())
            for i in range(self.N + 1):
                self.t[i] = list(map(int, fin.readline().strip().split()))

        # Initialize C matrix and find Cmin
        for i in range(self.N + 1):
            for j in range(self.N + 1):
                self.C[i][j] = self.d[i] + self.t[i][j]
                if i != j:
                    self.Cmin = min(self.Cmin, self.C[i][j])

    def solution(self):
        temp_total = self.M[self.s[self.N]] + self.C[self.s[self.N]][0]
        if temp_total < self.BEST:
            self.BEST = temp_total
            for i in range(self.N + 1):
                self.path[i] = self.s[i]

    def TRY(self, k, prev):
        for i in range(1, self.N + 1):
            if not self.visited[i] and self.M[prev] + self.C[prev][i] <= self.l[i]:
                self.visited[i] = True
                self.s[k] = i
                M_prev = self.M[i]
                if self.M[prev] + self.C[prev][i] < self.e[i]:
                    self.M[i] = self.e[i]
                else:
                    self.M[i] = self.M[prev] + self.C[prev][i]
                if self.M[i] > self.BEST - self.Cmin * (self.N - k + 1):
                    self.visited[i] = False
                    self.M[i] = M_prev
                    continue
                if k == self.N:
                    self.solution()
                else:
                    self.TRY(k + 1, i)
                self.visited[i] = False
                self.M[i] = M_prev
        return 1000000000

    def solve(self):
        self.s[0] = 0
        self.M[0] = 0
        self.TRY(1, 0)

    def output(self, output_filename):
        with open(output_filename, 'w') as fout:
            fout.write(f"{self.N}\n")
            fout.write(" ".join(map(str, self.path[1:self.N + 1])))


def main():
    solver = Solver("testcase/tutao/test1.txt")
    solver.solve()
    solver.output("python/test1.txt")


if __name__ == "__main__":
    main()
