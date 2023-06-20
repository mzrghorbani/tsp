import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualise_tsp(best_route, cities, sleep_time=0.1):
    fig, ax = plt.subplots()

    def update_plot(iteration):
        ax.clear()

        # Plot the cities
        x = [city['x'] for city in cities]
        y = [city['y'] for city in cities]
        ax.scatter(x, y, color='red', label='Cities')

        # Annotate city names
        for i, city in enumerate(cities):
            ax.annotate(city['name'], (x[i], y[i]))

        # Plot the best route so far
        current_route = best_route[:iteration+1]
        
        # Add the first city to the end to complete the cycle
        current_route.append(cities[0])

        x = [city['x'] for city in current_route]
        y = [city['y'] for city in current_route]
        ax.plot(x, y, color='blue', label='Best Route')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'TSP Solver (Iteration {iteration+1}/{len(best_route) - 1})')
        ax.legend()

    num_iterations = len(best_route) - 1

    ani = animation.FuncAnimation(fig, update_plot, frames=num_iterations, interval=int(sleep_time*5000), repeat=False)

    plt.show()
