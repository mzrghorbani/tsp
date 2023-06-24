import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

def visualise_tsp(best_route, cities, sleep_time=0.5):
    fig, ax = plt.subplots(figsize=(8, 6))

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

    # Create a list to store individual frames of the animation
    frames = []

    for i in range(num_iterations):
        update_plot(i)
        # Draw the canvas to generate the frame
        fig.canvas.draw()
        # Convert the frame to an RGB array
        frame = np.array(fig.canvas.renderer._renderer)
        # Convert the RGB array to an image
        image = Image.fromarray(frame)
        # Append the image to the list of frames
        frames.append(image)

    # Save the frames as a GIF using Pillow
    frames[0].save("output_files/tsp_animation.gif", 
        format="GIF", 
        append_images=frames[1:], 
        save_all=True, 
        duration=int(sleep_time*1000), 
        loop=0,
        blit=True)

    plt.close(fig)
