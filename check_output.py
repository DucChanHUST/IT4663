def read_input_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    index = 0
    
    # Number of delivery locations
    N = int(lines[index].strip())
    index += 1
    
    # Time matrix initialization
    time_matrix = [(0, 1e9, 0)]  # Start point time constraints

    # Reading time constraints for each delivery point
    for i in range(1, N + 1):
        e, l, d = map(int, lines[index].strip().split())
        time_matrix.append([e, l, d])
        index += 1

    # Distance matrix initialization
    dist_matrix = []
    for i in range(N + 1):
        dist_matrix.append(list(map(int, lines[index].strip().split())))
        index += 1

    # Number of points in the route
    N_out = int(lines[index].strip())
    index += 1

    # Route output
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

# Replace 'input.txt' with the path to your input file
file_path = "C:/Users/FPT Shop/Desktop/res1.txt"
check_delivery_route(file_path)
