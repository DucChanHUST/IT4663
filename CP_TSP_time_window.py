#TSP with Time windows
from ortools.sat.python import cp_model
import time

def TSP_CP(n, time_matrix, dist_matrix):
    model = cp_model.CpModel()

    # Define input
    num_nodes = n + 1
    e = {}  # earliest time to visit city i
    l = {}  # latest time to visit city i
    d = {}  # duration time to visit city i
    C = {}  # C[i,j] = d[i] + dist_matrix[i][j]
    
    # Initialize input
    d[0] = 0
    e[0] = 0
    l[0] = 1000000000
    for i in range(1, num_nodes):
        e[i] = time_matrix[i-1][0]
        l[i] = time_matrix[i-1][1]
        d[i] = time_matrix[i-1][2]
    for i in range(num_nodes):
        for j in range(num_nodes):    
            C[i, j] = d[i] + dist_matrix[i][j]
            
    # Define variables
    x = {}  # x[i,j] = 1 if i -> j else 0
    M = {}  # M[i] = time to deliver at city i = Arrival time at city i + time waiting at city i
    w = {}  # time waiting at city i
    
    # Initialize variables
    for i in range(num_nodes):
        for j in range(num_nodes):
            x[i, j] = model.NewIntVar(0, 1, 'x[%i,%i]' % (i, j))

    M[0] = model.NewIntVar(0, 0, 'M[%i]' % 0)
    for i in range(1, num_nodes):
        M[i] = model.NewIntVar(e[i], l[i], 'M[%i]' % i)

    for i in range(num_nodes):
        w[i] = model.NewIntVar(0, l[i] - e[i], 'w[%i]' % i)

    # Define constraints
    # Each city is visited exactly once
    for i in range(num_nodes):
        model.Add(sum(x[i, j] for j in range(num_nodes) if j != i) == 1)
        model.Add(sum(x[j, i] for j in range(num_nodes) if j != i) == 1)
        
    # Time window
    for i in range(num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                model.Add(M[i] + C[i, j]*x[i, j] - M[j] <= (1 - x[i, j]) * 1000000000)
                model.Add(w[j] == M[j] - M[i] - C[i, j]).OnlyEnforceIf(x[i, j])
                
    # Objective
    model.Minimize(sum(C[i, j] * x[i, j] for i in range(num_nodes) for j in range(num_nodes) if j != i) 
                   + sum(w[i] for i in range(num_nodes)))
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(n)
        solution = {}
        solution[0] = 0

        for i in range(1, num_nodes):
            solution[i] = solver.Value(M[i])
        solution = sorted(solution.items(), key=lambda x: x[1])

        for i in range(1, num_nodes):
            print(solution[i][0], end=' ')
        return solver.ObjectiveValue()
                    

if __name__ == '__main__':

    # input from file

    time_matrix = []
    dist_matrix = []
    with open('input.txt', 'r') as file:
        # Read the input
        N = int(file.readline())

        for i in range(1, N+1):
            e, l, d = map(int, file.readline().split())
            time_matrix.append([e, l, d])

        for i in range(N+1):
            line = list(map(int, file.readline().split()))
            dist_matrix.append(line)
    TSP_CP(N, time_matrix, dist_matrix)

    # # input from keyboard

    # N = int(input())
    # time_matrix = []
    # dist_matrix = []
    # for i in range(1, N+1):
    #     e, l, d = map(int, input().split())
    #     time_matrix.append([e, l, d])

    # for i in range(N+1):
    #     line = list(map(int, input().split()))
    #     dist_matrix.append(line)

    # TSP_CP(N, time_matrix, dist_matrix)
    
    
    # #Compute run time & Compare ans with output
    # with open('time.txt', 'w') as f:
    #     start_time = time.time()
    #     ans = TSP_CP(N, time_matrix, dist_matrix)
    #     end_time = time.time()
    #     f.write(str(end_time - start_time) + '\n')
        
    #     with open('output.txt', 'r') as file:
    #         num_nodes = int(file.readline())
    #         path = list(map(int, file.readline().split()))
    #         target = {}
    #         target[0] = 0
    #         path = [0] + path
    #         d = [0] + [time_matrix[i][2] for i in range(len(time_matrix))]
    #         e = [0] + [time_matrix[i][0] for i in range(len(time_matrix))]
    #         for k in range(1, len(path)):
    #             target[path[k]] = max(target[path[k-1]] + dist_matrix[path[k-1]][path[k]] + d[path[k-1]], e[path[k]])
    #         ogAns = target[path[num_nodes]] + dist_matrix[path[num_nodes]][0] + d[path[num_nodes]]
    #         # Total delivery start time at last visited city + Travel time back to start + Delivery time at last visited city
    #     if ans == ogAns:
    #         print('Correct')
    #     else:
    #         print('Wrong')
    