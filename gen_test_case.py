import random
import os

# Number of customers
N = 50

def generate_test_case(file_path):
    # Generating e(i), l(i), d(i)
    time_windows = []
    for i in range(N):
        e_i = random.randint(500, 250000)
        
        l_i1 = random.randint(2,4) * 10
        l_i = e_i + l_i1
        d_i = random.randint(1, 4) * 5
        time_windows.append((e_i, l_i, d_i))

    # Generating t(i, j)
    distance_matrix = []
    for i in range(N+1):
        row = []
        for j in range(N+1):
            if i == j:
                row.append(0)
            else:
                row.append(random.randint(1, 240) * 5)
        distance_matrix.append(row)

    with open(file_path, 'w') as f:
        # Print the testcase
        f.write(str(N) + '\n')
        for tw in time_windows:
            f.write(f"{tw[0]} {tw[1]} {tw[2]}\n")
        for row in distance_matrix:
            f.write(' '.join(map(str, row)) + '\n')

def read_input_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    index = 0
    N = int(lines[index].strip())
    index += 1

    time_matrix = [(0, 1e9, 0)]
    for i in range(1, N + 1):
        e, l, d = map(int, lines[index].strip().split())
        time_matrix.append((e, l, d))
        index += 1

    dist_matrix = []
    for i in range(N + 1):
        dist_matrix.append(list(map(int, lines[index].strip().split())))
        index += 1

    N_out = int(lines[index].strip())
    index += 1

    route_out = [0] + list(map(int, lines[index].strip().split())) + [0]

    return N, time_matrix, dist_matrix, N_out, route_out

def check_delivery_route(file_path):
    N, time_matrix, dist_matrix, N_out, route_out = read_input_from_file(file_path)

    time_come = 0
    is_valid = True

    for k in range(N_out + 1):
        location = route_out[k]

        if time_come > time_matrix[location][1]:
            print(f"Algorithm does not satisfy constraints at location {location}")
            is_valid = False
            break

        if time_come < time_matrix[location][0]:
            time_come = time_matrix[location][0]

        time_come += time_matrix[location][2]
        time_come += dist_matrix[route_out[k]][route_out[k + 1]]

    if is_valid:
        print(f"Final time: {time_come}")
        print(f"Route: {route_out}")
        return True
    return False

def main():
    file_path = os.path.join(os.path.expanduser("~"), "Desktop", "test_case1.txt")
    final_check = True
    stt = 0
    while final_check:
        stt += 1
        random.seed(stt)
        generate_test_case(file_path)
        import sys
        NMAX = 1005
        e = [0] * NMAX
        l = [0] * NMAX
        d = [0] * NMAX
        c = [[0] * NMAX for _ in range(NMAX)]
        cd = [[0] * NMAX for _ in range(NMAX)]
        visited = [False] * NMAX
        route = [0] * NMAX
        timeCome = [0] * NMAX
        orderByL = []

        def input_data():
            global N
            with open(file_path, 'r') as f:
                lines = f.readlines()
                N = int(lines[0].strip())
                idx = 1
                for i in range(1, N + 1):
                    e[i], l[i], d[i] = map(int, lines[idx].strip().split())
                    orderByL.append((l[i], i))
                    idx += 1
                for i in range(N + 1):
                    c[i] = list(map(int, lines[idx].strip().split()))
                    idx += 1
                for i in range(N + 1):
                    for j in range(N + 1):
                        cd[i][j] = c[i][j] + d[j]

        def changeOrderToCome(high, low, oldOrder):
            tmp = oldOrder[high]
            for i in range(high, low, -1):
                oldOrder[i] = oldOrder[i - 1]
            oldOrder[low] = tmp

        input_data()
        orderToCome = [0] * NMAX
        orderByL.sort()
        for i in range(1, N + 1):
            orderToCome[i] = orderByL[i - 1][1]

        visited[0] = True
        route[0] = 0
        timeCome[0] = 0

        for i in range(1, N + 1):
            nextLocation = orderToCome[i]
            selectedLocation = nextLocation
            lastestTimeCome = l[selectedLocation]
            selectedTimeCome = max(e[selectedLocation], timeCome[route[i - 1]] + cd[route[i - 1]][selectedLocation])
            tmp_j = 0

            for j in range(i + 1, N + 1):
                choice = orderToCome[j]
                tmpTimeCome = max(e[choice], timeCome[route[i - 1]] + cd[route[i - 1]][choice])
                if tmpTimeCome + cd[choice][selectedLocation] < lastestTimeCome:
                    lastestTimeCome = tmpTimeCome + cd[choice][selectedLocation]
                    selectedLocation = choice
                    selectedTimeCome = tmpTimeCome
                    tmp_j = j

            if selectedLocation != nextLocation:
                changeOrderToCome(tmp_j, i, orderToCome)

            route[i] = selectedLocation
            timeCome[route[i]] = selectedTimeCome

        with open(file_path, 'r') as f_src:
            content = f_src.read()

        res_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "res1.txt")
        with open(res_file_path, 'w') as f_dst:
            f_dst.write(content)

        with open(res_file_path, 'a') as f:
            f.write(f"{N}\n")
            f.write(' '.join(map(str, route[1:N + 1])) + '\n')

        if check_delivery_route(res_file_path):
            final_check = False

if __name__ == "__main__":
    main()
