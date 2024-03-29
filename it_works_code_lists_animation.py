"""
everything works 
Generates n amount of walkers and simulates their movement in a 2D 100x100 grid. With all but one of the walkers
starting off as healthy and one starting off as infected. The infected walker will infect any healthy walker if 
it comes into contact with them. The infected walker has a %p chance of infecting a healthy walker if they are
in the same position. Each walker has a %r chance of recovering at each step. Once a walker recovers they become
immune to the infection. The simulation will stop if all walkers have been infected or if there are no more infected
walkers. The simulation will also stop if the number of steps reaches the maximum number of steps.
"""


import random as random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import geom
import numpy as np #maybe can delte these but might switch to arrays later
from IPython.display import HTML # for displaying the animation in the notebook, but might not need it either


def infection_probability(p, num_infected):
    """
    Calculate the probability of infection on the nth trial using the geometric distribution, with the number of 
    trials reffering to the number of infected walkers in the same position as the healthy walker.

    p = the probability of infection
    num_infected = the number of infected walkers in the same position as the healthy walker
    """
    prob = geom.pmf(num_infected, p)
    return prob

def two_dimensional_random_walk(steps, start=(0, 0), grid_size=100):
    """
    Simulate a two-dimensional random walk with periodic boundary conditions. The walker starts at a randomly assinged
    position and takes a step in a random direction at each step. The walker's position is stored at each step.

    steps = the number of steps the walker will take
    start = the starting position of the walker
    grid_size = the size of the grid that the walker will move in, is fixed at 100x100, as per the requirements
    """
    x = [start[0]]
    y = [start[1]]
    for i in range(1, steps):
        direction = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
        new_x = (x[-1] + direction[0]) % grid_size  # Apply periodic boundary conditions for x
        new_y = (y[-1] + direction[1]) % grid_size  # Apply periodic boundary conditions for y
        x.append(new_x)
        y.append(new_y)
    
    return x, y

#def infection_probability(steps, num_infected):
    #the probability funciton for an infection to occur
 #   return min(1, 0.5 +0.1 *num_infected)


def simulate_multiple_walks(num_walks, steps, recovery_probability, base_inf_prob, grid_size=100):
    # Set the initial infected walker
    initial_infected = random.randint(0, num_walks-1)
    initial_positions = []
    final_positions = []
    infected_walkers = [initial_infected]  # Start with one infected walker
    recovered_walkers = []  # Keep track of the recovered walkers
    positions_at_each_step = []
    infected_walkers_at_each_step = []
    recovered_walkers_at_each_step = []

    # Create a list to hold the walkers' paths
    paths = [two_dimensional_random_walk(steps, start=(random.randint(0, grid_size), random.randint(0, grid_size)), grid_size=grid_size) for _ in range(num_walks)]

    # Check each step for all walkers
    for step in range(steps):
        #Print the current step every 100 steps
        if step % 100 == 0:
            print(f'Step {step} of {steps}')
        for i in range(num_walks):
            num_infected = sum(paths[j][0][step] == paths[i][0][step] and paths[j][1][step] == paths[i][1][step] for j in infected_walkers)
            for j in range(i+1, num_walks):
                # If two walkers are at the same position and one of them is infected, infect the other
                if paths[i][0][step] == paths[j][0][step] and paths[i][1][step] == paths[j][1][step]:
                    if i in infected_walkers and j not in recovered_walkers and random.random() < infection_probability(base_inf_prob, num_infected):
                        infected_walkers.append(j)
                    elif j in infected_walkers and i not in recovered_walkers and random.random() < infection_probability(base_inf_prob, num_infected):
                        infected_walkers.append(i)

            # Check for recovery
            if i in infected_walkers and random.random() < recovery_probability:
                infected_walkers.remove(i)
                recovered_walkers.append(i)

        # Append the current positions of the walkers to the list.
        current_positions = [(path[0][step], path[1][step]) for path in paths]
        positions_at_each_step.append(current_positions)

        # Append the current infected and recovered walkers to the lists
        infected_walkers_at_each_step.append(list(infected_walkers))
        recovered_walkers_at_each_step.append(list(recovered_walkers))

        # Check if there are no more infected walkers
        if not infected_walkers:
            print("Their are no more infected walkers!")
            return initial_positions, final_positions, infected_walkers, recovered_walkers, initial_infected, step
        
        num_infected = num_walks - len(infected_walkers) - len(recovered_walkers)
        if num_infected == 0:
            print("The whole population has been infected!")
            return positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, initial_positions, final_positions, infected_walkers, recovered_walkers, initial_infected, step



    # Get the initial and final positions
    for path in paths:
        initial_positions.append((path[0][0], path[1][0]))
        final_positions.append((path[0][-1], path[1][-1]))

    return positions_at_each_step,infected_walkers_at_each_step, recovered_walkers_at_each_step, initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, steps


def plot_initial_positions(initial_positions, initial_infected, grid_size):
    initial_x, initial_y = zip(*initial_positions)

    plt.figure(figsize=(5, 5))
    plt.scatter(initial_x, initial_y, color='blue', label='Initial Positions')
    plt.scatter(initial_x[initial_infected], initial_y[initial_infected], color='red', label='Infected Walker')  # Plot the infected walker
    plt.title('Initial Positions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)
    plt.show()


def plot_final_positions(final_positions, infected_walkers, recovered_walkers, grid_size):
    final_x, final_y = zip(*final_positions)

    plt.figure(figsize=(5, 5))
    plt.scatter(final_x, final_y, color='blue', label='Final Positions')

    # Create arrays for the x and y positions of the infected and recovered walkers
    infected_x = [final_x[walker] for walker in infected_walkers]
    infected_y = [final_y[walker] for walker in infected_walkers]
    recovered_x = [final_x[walker] for walker in recovered_walkers]
    recovered_y = [final_y[walker] for walker in recovered_walkers]

    # Create a single scatter plot for all infected walkers and another for all recovered walkers
    plt.scatter(infected_x, infected_y, color='red', label='Infected Walkers')
    plt.scatter(recovered_x, recovered_y, color='green', label='Recovered Walkers')

    plt.title('Final Positions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)

    plt.show()

def animate_positions(i, positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, grid_size):
    plt.gca().clear()
    positions = positions_at_each_step[i]
    infected_walkers = infected_walkers_at_each_step[i]
    recovered_walkers = recovered_walkers_at_each_step[i]
    healthy_positions = [pos for index, pos in enumerate(positions) if index not in infected_walkers and index not in recovered_walkers]
    infected_positions = [pos for index, pos in enumerate(positions) if index in infected_walkers]
    recovered_positions = [pos for index, pos in enumerate(positions) if index in recovered_walkers]
    
    # Plot each group with different colors
    if healthy_positions:
        plt.scatter(*zip(*healthy_positions), color='blue', label='Healthy')
    if infected_positions:
        plt.scatter(*zip(*infected_positions), color='red', label='Infected')
    if recovered_positions:
        plt.scatter(*zip(*recovered_positions), color='green', label='Recovered')

    # Set plot limits, labels, and title
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.title('An infection spreading among a randomly moving population, where after a walker recovers they become immune')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)

def plot_initial_final_positions(initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, grid_size):
    initial_x, initial_y = zip(*initial_positions)
    final_x, final_y = zip(*final_positions)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(initial_x, initial_y, color='blue', label='Initial Positions')
    plt.scatter(initial_x[initial_infected], initial_y[initial_infected], color='red', label='Infected Walker')  # Plot the infected walker
    plt.title('Initial Positions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.legend(loc='upper right')

    plt.subplot(1, 2, 2)
    plt.scatter(final_x, final_y, color='green', label='Final Positions')


    # Create arrays for the x and y positions of the infected and recovered walkers
    infected_x = [final_x[walker] for walker in infected_walkers]
    infected_y = [final_y[walker] for walker in infected_walkers]
    recovered_x = [final_x[walker] for walker in recovered_walkers]
    recovered_y = [final_y[walker] for walker in recovered_walkers]

    # Create a single scatter plot for all infected walkers and another for all recovered walkers
    plt.scatter(infected_x, infected_y, color='red', label='Infected Walkers')
    plt.scatter(recovered_x, recovered_y, color='black', label='Recovered Walkers')


    plt.title('Final Positions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


"""
The parameters
num_walks = the number of total walkers in the model, including the initial infected walker
steps = the number of steps each walker will take
grid_size = the size of the grid that the walkers will move in, is fixed at 100x100, as per the requirements
base_inf_prob = the base infection probability, which is the probability that an infected walker will infect a healthy 
walker if they are in the same position
recovery_probability = the probability that a walker will recover at each step
"""
# Parameters
num_walks = 1000
steps = 100  # Increase the number of steps
#n = 10 #frequency of steps shown
grid_size = 100
base_inf_prob = 0.5
recovery_probability = 0.001  # Define the recovery probability, e.g. 0.05 = 5% chance of recovery at each step

#create the infection probability


# Simulate multiple walks and get initial and final positions
positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, stps = simulate_multiple_walks(num_walks, steps, recovery_probability, base_inf_prob, grid_size)
print(stps)  # Print the number of steps taken



# Plot initial and final positions
plot_initial_positions(initial_positions, initial_infected, grid_size)

"""
#here i am trying to plot the animation of all the positions
"""
# Create a figure.
fig = plt.figure()

# Create an animation.

ani = animation.FuncAnimation(fig, animate_positions, frames=steps, fargs=(positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, grid_size), repeat=False)
# Display the animation.
plt.show()
#can do windows + alt + r to screen record the animation



plot_final_positions(final_positions, infected_walkers, recovered_walkers, grid_size)



#can plot both of them in the same figure if needs be
#plot_initial_final_positions(initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, grid_size)
#justifying my actions, why i did what i did, " i researched this so i did that"