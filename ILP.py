#PYTHON Chu Thien Hai 20215360
# Quy hoạch nguyên tuyến tính

from ortools.linear_solver import pywraplp

def TSP_mixed_integer_programming(n, time_matrix, dist_matrix):
    model = pywraplp.Solver.CreateSolver('SCIP')

############## Danh sách input ###############################

    num_nodes = n + 1
    e = {}  # Thời điểm sớm nhất để giao hàng 
    l = {}  # Thời điểm muộn nhất để giao hàng
    d = {}  # Thời gian cần thiết để chuyển hàng
    C = {}  # C[i,j] = d[i] + dist_matrix[i][j]
    d[0] = 0
    e[0] = 0
    l[0] = 1e9
    for i in range(1, num_nodes):
        e[i] = time_matrix[i-1][0]
        l[i] = time_matrix[i-1][1]
        d[i] = time_matrix[i-1][2]
    for i in range(num_nodes):
        for j in range(num_nodes):
            C[i, j] = d[i] + dist_matrix[i][j]

############### Danh sách các biến ##############################

    x = {}  # x[i,j] = 1 if i -> j else 0
    M = {}  # M[i] = thời điểm tới vị trí i
    u = {} # u[i] = j if người i được thăm ở lần thăm thứ j
    w = {} # thời gian chờ đợi tại vị trí i
    t1 = {} 
    t2 = {} 

############### Miền xác định #########################

    for i in range(num_nodes):
        for j in range(num_nodes):
            if j != i:
                x[i, j] = model.IntVar(0, 1, 'x[%i,%i]' % (i, j))
            else:
                x[i, j] = model.IntVar(0,0, 'x[%i,%i]' % (i, j))

    M[0] = model.IntVar(0, 0, 'M[%i]' % 0)
    for i in range(1, num_nodes):
        M[i] = model.IntVar(0, l[i], 'M[%i]' % i)

    u[0] = model.IntVar(1, 1, 'u[%i]' % 0)
    for i in range(1, num_nodes):
        u[i] = model.IntVar(2, num_nodes, 'u[%i]' % i)

    w[0] = model.IntVar(0,0, 'w[%i]' % 0)
    for i in range(1, num_nodes):
        w[i] = model.IntVar(0, l[i], 'w[%i]' % i)


    for i in range(0, num_nodes):
        t1[i] = model.IntVar(0, 1, 't1[%i]' % i)
        t2[i] = model.IntVar(0, 1, 't2[%i]' % i)
    
 ############## Ràng buộc ###############################

    for i in range(num_nodes):
        model.Add(sum(x[i, j] for j in range(num_nodes) if j != i) == 1)
        model.Add(sum(x[j, i] for j in range(num_nodes) if j != i) == 1)

    # subtour elimination
    for i in range(1, num_nodes):
        for j in range(1, num_nodes):
            if i != j:
                model.Add(u[i] - u[j] + 1 <=  num_nodes * (1- x[i, j]))

    # time window
    for i in range(num_nodes): 
        for j in range(1, num_nodes):
            if i != j:
                model.Add(M[j] <= M[i] + w[i] + C[i, j] + (1 - x[i, j]) * 1e9)
                model.Add(M[j] >= M[i] + w[i] + C[i, j] - (1 - x[i, j]) * 1e9)

    # w[i] = max(0, e[i]-M[i])
    for i in range(1, num_nodes):
        model.Add(w[i] >= 0)
        model.Add(w[i] >= e[i] - M[i])
        model.Add(w[i] <= 1e9 * t1[i] + 0)
        model.Add(w[i] <= 1e9 * t2[i] + e[i] - M[i])
        model.Add(t1[i] + t2[i] <= 1)
                
                
############### Objective #################################
    model.Minimize(sum(C[i, j] * x[i, j] for i in range(num_nodes) for j in range(num_nodes) if j != i) + sum(w[i] for i in range(num_nodes)))

############### Solve #####################################
    status = model.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        route = [0 for _ in range(num_nodes - 1)]
        for i in range(1, num_nodes):
            route[int(u[i].solution_value() - 2)] = i
        print(*route)
    
    #     print('Objective value =', model.Objective().Value())
    #     for i in range(num_nodes):
    #         for j in range(num_nodes):
    #             if x[i, j].solution_value() > 0:
    #                 print('x[%i,%i] = %i' % (i, j, x[i, j].solution_value()))
        for i in range(num_nodes):
            print('M[%i] = %i' % (i, M[i].solution_value()))
            print(str(i) + ": " + str(l[i]))
        
    #     for i in range(num_nodes):
    #         print('w[%i] = %i' % (i, w[i].solution_value()))
    #     for i in range(num_nodes):
    #         print('u[%i] = %i' % (i, u[i].solution_value()))

    # return model.Objective().Value()

if __name__ == '__main__':

    # input_data = []
    # customers = []
    # t = []
    # with open('C:/Users/FPT Shop/Desktop/python/input1.txt', 'r') as file:
    # # Read the input
    #     N = int(file.readline())
        
    #     for _ in range(1, N+1):
    #         e, l, d = map(int, file.readline().split())
    #         customers.append([e, l, d])

    #     for _ in range(N+1):
    #         row = list(map(int, file.readline().split()))
    #         t.append(row)
    N = int(input())
    time_matrix = []
    for i in range(1,N + 1):
        eld = input().strip().split()
        e = int(eld[0])
        l = int(eld[1])
        d = int(eld[2])
        time_matrix.append([e,l,d])
    dist_matrix = [[0 for _ in range(N+1)] for _ in range(N+1)]

    for i in range(N+1):
            C = input().strip().split()
            for j in range(N+1):
                dist_matrix[i][j] = int(C[j])

    TSP_mixed_integer_programming(N, time_matrix, dist_matrix)
