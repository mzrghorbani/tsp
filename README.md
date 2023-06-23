# Traveling Salesman Problem:

If the Traveling Salesman Problem (TSP) consists of five cities (A, B, C, D, E), the goal is to find the shortest possible route that the salesman visits every city once and returns to the origin city, A in this case. The route should be a closed loop.

Given the list of cities and their coordinates, the problem is to find the route with the minimum total distance. The actual solution will depend on the method used to solve the TSP.

One common approach is to use a greedy algorithm, which always goes to the nearest unvisited city next. However, the greedy approach doesn't always yield the optimal solution. To find the true optimal solution, we would have to enumerate all possible routes and calculate their lengths, which becomes computationally intensive for a large number of cities. Hence two versions of the code are implemented, single-process and multi-processes.

In the algorithm, the routing would work with a simple greedy approach as follow;

	1. Start from city 'A'. (Current route: A)
	2. Move to the closest unvisited city from 'A', which is 'B'. (Current route: A-B)
	3. From 'B', move to the closest unvisited city, which might be 'C'. (Current route: A-B-C)
	4. From 'C', move to the closest unvisited city, which might be 'D'. (Current route: A-B-C-D)
	5. Finally, move to the last unvisited city, 'E'. (Current route: A-B-C-D-E)
	6. Return to the origin city 'A'. (Final route: A-B-C-D-E-A)

This is just a simplified example. The actual optimal route might be different. We would need to run the TSP algorithm on the provided cities to find the actual optimal route.


# Instructions (non-mpi):

	1. Install the required python packages.
	2. Clone the TSP repository from GitHub.
	3. Change the directory to the cloned repository.
	4. Run `python tsp.py` first, and then,
	5. Run `python tsp.py true` to visualise the routing process.


# Instructions (with-mpi):

	1. Install the required python packages including mpirun.
	2. Clone the TSP repository from GitHub.
	3. Change directory to the cloned repository.
	4. Run `mpirun -np 2 python tsp.py` first, and then,
	5. Run `mpirun -np 2 python tsp.py true` to visualise the routing process.


# Results:

    If the visualisation option is not passed, a route.geojson will be created in the output_files/ directory.
    If the visualisation option is passed, a GIF image will be created in the results/ directory.


