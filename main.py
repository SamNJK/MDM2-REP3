import numpy as np
import matplotlib.pyplot as plt

grid_size = 100
n_individuals = 1000
p1 = 0.2
p2 = 0.01
n_steps = 100

# Initialize status: 0 for susceptible, 1 for infected, 2 for recovered
status = np.zeros(n_individuals, dtype=int)
status[0] = 1  # Initialize the first individual as infected

# Initialize the positions of individuals
positions = np.random.randint(0, grid_size, (n_individuals, 2))

# Simulate each time step
infected_counts = []
for _ in range(n_steps):
    # Random walk: Change the position of each individual randomly
    steps = np.random.randint(-1, 2, (n_individuals, 2))
    positions = (positions + steps) % grid_size  # Apply periodic boundary conditions

    # Infection process
    for i in range(n_individuals):
        if status[i] == 1:  # For each infected individual
            for j in range(n_individuals):
                if i != j and status[j] == 0:
                    if np.array_equal(positions[i], positions[j]) and np.random.rand() < p1:
                        status[j] = 1  # Susceptible individual becomes infected

    # Recovery process
    for i in range(n_individuals):
        if status[i] == 1 and np.random.rand() < p2:  # Infected individual recovers with a certain probability
            status[i] = 2

    # Track the number of infected individuals
    infected_counts.append(np.sum(status == 1))

# Plotting
plt.plot(infected_counts, label='Infected')
plt.xlabel('Time Steps')
plt.ylabel('Number of Infected Individuals')
plt.title('Spread of Disease over Time')
plt.legend()
plt.show()
