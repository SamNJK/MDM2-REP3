"""
This code plots the dynamics of the SIR model for infectious diseases.
"""

import numpy as np
import matplotlib.pyplot as plt

# Basic parameters
beta = 0.3  # Infection rate
gamma = 0.05  # Recovery rate
N = 1000  # Total population
I0 = 1  # Initial number of infected individuals
S0 = N - I0  # Initial number of susceptible individuals
R0 = 0  # Initial number of recovered individuals
days = 160  # Simulation duration in days

# Initialize SIR values
S, I, R = [S0], [I0], [R0]

# Simulate the SIR update for each day
for _ in range(days):
    next_S = S[-1] - (beta * S[-1] * I[-1]) / N
    next_I = I[-1] + (beta * S[-1] * I[-1]) / N - gamma * I[-1]
    next_R = R[-1] + gamma * I[-1]

    S.append(next_S)
    I.append(next_I)
    R.append(next_R)

# Plot the dynamics of the SIR model
plt.figure(figsize=(10, 6))
plt.plot(S, label="Susceptible")
plt.plot(I, label="Infected")
plt.plot(R, label="Recovered")
plt.xlabel("Days")
plt.ylabel("Number of Individuals")
plt.legend()
plt.title("SIR Model Simulation")
plt.show()
