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
import numpy as np  # maybe can delte these but might switch to arrays later
from IPython.display import HTML  # for displaying the animation in the notebook, but might not need it either


def infection_probability(p, num_infected):
    """
    Calculate the probability of infection on the nth trial using the geometric distribution, with the number of
    trials reffering to the number of infected walkers in the same position as the healthy walker.

    p = the probability of infection
    num_infected = the number of infected walkers in the same position as the healthy walker
    """
    prob = geom.pmf(num_infected, p)
    return prob


def two_dimensional_random_walk(steps, start, grid_size, social_distancing=False, compliance_rate=1.0, min_distance=2):
    x, y = [start[0]], [start[1]]
    for i in range(1, steps):
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        if social_distancing:
            # Check each direction for compliance with social distancing rules
            new_directions = []
            for direction in directions:
                new_x = (x[-1] + direction[0]) % grid_size
                new_y = (y[-1] + direction[1]) % grid_size
                # Check if this new position is too close to any other walker
                too_close = any(
                    abs(new_x - other_x) <= min_distance and abs(new_y - other_y) <= min_distance
                    for other_x, other_y in zip(x, y)
                )
                if not too_close or random.random() > compliance_rate:
                    new_directions.append(direction)
            # If there are no directions that adhere to social distancing, take the original direction
            direction = random.choice(new_directions) if new_directions else random.choice(directions)
        else:
            direction = random.choice(directions)
        x.append((x[-1] + direction[0]) % grid_size)
        y.append((y[-1] + direction[1]) % grid_size)
    return x, y




def simulate_multiple_walks(num_walks, steps, recovery_probability, base_inf_prob, grid_size=100):
    """
    This function simulates multiple random walks in a 2D grid, with the walkers having a chance of becoming infected
    when they are in the same position as an infected walker. If a walker becomes infected, they have a chance of recovering,
    and once they recover they become immune to the infection. The simulation will stop if all walkers have been infected, or
    if there are no more infected walkers. The simulation will also stop if the number of steps reaches the maximum number of steps.
    It keeps track of all the walkers for all the steps.

    num_walks = the number of total walkers in the model, including the initial infected walker
    steps = the number of steps each walker will take
    recovery_probability = the probability that a walker will recover at each step
    base_inf_prob = the base infection probability, which is the probability that an infected walker will infect a healthy
    walker if they are in the same position
    grid_size = the size of the grid that the walkers will move in, is fixed at 100x100, as per the requirements
    """
    # Set the initial infected walker
    initial_infected = random.randint(0, num_walks - 1)
    initial_positions = []
    final_positions = []
    infected_walkers = [initial_infected]  # Start with one infected walker
    recovered_walkers = []  # Keep track of the recovered walkers
    positions_at_each_step = []
    infected_walkers_at_each_step = []
    recovered_walkers_at_each_step = []

    # Create a list to hold the walkers' paths
    paths = [two_dimensional_random_walk(steps, start=(random.randint(0, grid_size), random.randint(0, grid_size)),
                                         grid_size=grid_size) for _ in range(num_walks)]

    # Check each step for all walkers
    for step in range(steps):
        # Print the current step every 100 steps
        if step % 100 == 0:
            print(f'Step {step} of {steps}')
        for i in range(num_walks):
            num_infected = sum(
                paths[j][0][step] == paths[i][0][step] and paths[j][1][step] == paths[i][1][step] for j in
                infected_walkers)
            for j in range(i + 1, num_walks):
                # If two walkers are at the same position and one of them is infected, infect the other
                if paths[i][0][step] == paths[j][0][step] and paths[i][1][step] == paths[j][1][step]:
                    if i in infected_walkers and j not in recovered_walkers and random.random() < infection_probability(
                            base_inf_prob, num_infected):
                        infected_walkers.append(j)
                    elif j in infected_walkers and i not in recovered_walkers and random.random() < infection_probability(
                            base_inf_prob, num_infected):
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

    return positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, steps


def plot_initial_positions(initial_positions, initial_infected, grid_size):
    """
    Plot the initial positions of the walkers, with the infected walker in red and the healthy walkers in blue.
    initial_positions = the initial positions of the walkers
    initial_infected = the index of the initial infected walker
    grid_size = the size of the grid that the walkers will move in, is fixed at 100x100, as per the requirements
    """
    initial_x, initial_y = zip(*initial_positions)

    plt.figure(figsize=(5, 5))
    plt.scatter(initial_x, initial_y, color='blue', label='Initial Positions')
    plt.scatter(initial_x[initial_infected], initial_y[initial_infected], color='red',
                label='Infected Walker')  # Plot the infected walker
    plt.title('Initial Positions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)
    plt.show()


def plot_final_positions(final_positions, infected_walkers, recovered_walkers, grid_size):
    """
    Plotting the final positions of the model, with the final positions of the infected walkers in red, the final positions
    of the walkers in blue, and the final positions of the recovered walkers in green.
    final_positions = the final positions of the walkers
    infected_walkers = the indices of the infected walkers
    recovered_walkers = the indices of the recovered walkers
    grid_size = the size of the grid that the walkers will move in, is fixed at 100x100, as per the requirements
    """
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


def animate_positions(i, positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step,
                      grid_size):
    """
    Making an animation of the results of the model, with the positions of the walkers at each step. Keep in mind that it does not save the animation.
    So I will have to screen record it if I want to save it. Or come up with a way to save the animation
    i = the current step
    positions_at_each_step = the positions of the walkers at each step
    infected_walkers_at_each_step = the indices of the infected walkers at each step
    recovered_walkers_at_each_step = the indices of the recovered walkers at each step
    grid_size = the size of the grid that the walkers will move in, is fixed at 100x100, as per the requirements
    """
    plt.gca().clear()
    positions = positions_at_each_step[i]
    infected_walkers = infected_walkers_at_each_step[i]
    recovered_walkers = recovered_walkers_at_each_step[i]
    healthy_positions = [pos for index, pos in enumerate(positions) if
                         index not in infected_walkers and index not in recovered_walkers]
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
    plt.title(f'Step {i + 1}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)


def plot_initial_final_positions(initial_positions, final_positions, infected_walkers, initial_infected,
                                 recovered_walkers, grid_size):
    initial_x, initial_y = zip(*initial_positions)
    final_x, final_y = zip(*final_positions)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(initial_x, initial_y, color='blue', label='Initial Positions')
    plt.scatter(initial_x[initial_infected], initial_y[initial_infected], color='red',
                label='Infected Walker')  # Plot the infected walker
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
steps = 100
grid_size = 100
base_inf_prob = 0.5
recovery_probability = 0.001

# running simulate_multiple_walks
positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, initial_positions, final_positions, infected_walkers, initial_infected, recovered_walkers, stps = simulate_multiple_walks(
    num_walks, steps, recovery_probability, base_inf_prob, grid_size)
print(stps)  # So i know whether it did run through all of the steps or not

# Plot initial positions
plot_initial_positions(initial_positions, initial_infected, grid_size)

"""
#here i am plotting the animation of all the positions over the steps
"""
# Create a figure.
fig = plt.figure()

# Create an animation.

ani = animation.FuncAnimation(fig, animate_positions, frames=steps, fargs=(
positions_at_each_step, infected_walkers_at_each_step, recovered_walkers_at_each_step, grid_size), repeat=False)
# Display the animation.
plt.show()
# can do windows + alt + r to screen record the animation


plot_final_positions(final_positions, infected_walkers, recovered_walkers, grid_size)

# justifying my actions, why i did what i did, " i researched this so i did that"