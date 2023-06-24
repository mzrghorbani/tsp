import json
import math
import sys
import os
from mpi4py import MPI
from visualise_tsp import visualise_tsp

def calculate_distance(city1, city2):
    x1, y1 = city1['x'], city1['y']
    x2, y2 = city2['x'], city2['y']
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def tsp_solver(cities):
    num_cities = len(cities)
    optimal_path = []
    total_distance = 0

    # Start with the first city
    current_city_index = 0
    current_city = cities[current_city_index]
    visited_cities = [current_city_index]

    while len(visited_cities) < num_cities:
        min_distance = float('inf')
        closest_city_index = None

        for idx, city in enumerate(cities):
            if idx not in visited_cities:
                distance = calculate_distance(current_city, city)
                if distance < min_distance:
                    min_distance = distance
                    closest_city_index = idx

        optimal_path.append(closest_city_index)
        total_distance += min_distance
        visited_cities.append(closest_city_index)
        current_city_index = closest_city_index
        current_city = cities[current_city_index]

    return optimal_path, total_distance


def solve_tsp(cities):
    print("Solving TSP...")
    optimal_path_indices, min_distance = tsp_solver(cities)
    print("TSP solved.")

    # Convert indices back to city data
    optimal_path = [cities[i] for i in optimal_path_indices]

    # Add the start city to the beginning and end of the optimal path
    start_city = cities[0]
    optimal_path.insert(0, start_city)
    optimal_path.append(start_city)

    return optimal_path, min_distance


def save_result(result, output_dir):
    print("Saving result...")
    output_file = os.path.join(output_dir, 'result.json')
    with open(output_file, 'w') as f:
        # Append total_distance to the best_route list
        result['best_route'].append({'total_distance': result['min_distance']})
        json.dump(result['best_route'], f, indent=2)  # pretty-print JSON data
    print("Result saved.")


def load_input(input_dir):
    print("Loading input...")
    input_file = os.path.join(input_dir, 'cities.json')
    with open(input_file, 'r') as f:
        cities = json.load(f)
    print("Input loaded.")
    return cities


def main():
    if len(sys.argv) != 3:
        print("Usage: mpirun -np <num_processes> python3 run_par.py <input_dir> <output_dir>")
        return

    input_dir = sys.argv[1].lower()
    output_dir = sys.argv[2].lower()

    # Initialize MPI
    comm = MPI.COMM_WORLD
    num_processes = comm.Get_size()
    rank = comm.Get_rank()

    # Load input
    cities = None
    if rank == 0:
        cities = load_input(input_dir)

    # Broadcast cities to all processes
    cities = comm.bcast(cities, root=0)

    # Divide the cities among processes
    num_cities = len(cities)
    cities_per_process = num_cities // num_processes
    start_index = rank * cities_per_process
    end_index = (rank + 1) * cities_per_process
    if rank == num_processes - 1:
        end_index = num_cities
    process_cities = cities[start_index:end_index]

    # Each process performs its own local search for the optimal path
    optimal_path, min_distance = solve_tsp(process_cities)

    # Gather the local optimal paths and distances from all processes
    all_optimal_paths = comm.gather(optimal_path, root=0)
    all_min_distances = comm.gather(min_distance, root=0)

    # Process 0 combines the results from all processes to obtain the final optimal path and minimum distance
    if rank == 0:
        # Concatenate the optimal paths from all processes
        optimal_path = [city for sublist in all_optimal_paths for city in sublist]

        # Calculate the final minimum distance
        min_distance = sum(all_min_distances)

        # Add the start city to the beginning and end of the optimal path
        start_city = cities[0]
        optimal_path.insert(0, start_city)
        optimal_path.append(start_city)

        # Prepare result
        result = {
            'best_route': optimal_path,
            'min_distance': min_distance
        }

        # Save result
        save_result(result, output_dir)

        # Visualise the result if the "visualise" flag is provided
        visualise_tsp(optimal_path, cities)

    # Terminate MPI
    MPI.Finalize()


if __name__ == '__main__':
    main()
