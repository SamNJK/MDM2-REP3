import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.integrate import odeint

S = [999]
I = [1]
R = [0]
t = [500]

tend = 500
beta = 0.04     # Infection Rate (1/beta = Infectious period)
gamma = 0.01    # Recovery Rate (1/gamma = Recovery period)

""" 
    R number (R_0) = beta/gamma, for Covid this is ~2.63
    This is the expected number of new infections from a single infected person.
"""

    # Gillespie algorithm
while t[-1] < tend and (S[-1] + I[-1] >= 1):

    N = S[-1] + I[-1] + R[-1]
    props = [beta*I[-1]*S[-1]/N, gamma*I[-1]]
    # props = propensity - The tendency/behaviour of the system for the events: [susceptible to infected, infected to recovered]
    prop_sum = sum(props)

    if prop_sum==0:
        print("Infected individual has recovered before infecting anyone else, restart simulation (for *not* weird results)")
        break

    tau = np.random.exponential(scale=1/prop_sum)
    t.append(t[-1]+tau)

    rand = random.uniform(0,1)
    # Susceptible becomes Infected
    if rand * prop_sum <= props[0]:
            S.append(S[-1] - 1)
            I.append(I[-1] + 1)
            R.append(R[-1])

    # Infected becomes Recovered
    # elif rand * prop_sum > props[0] and rand * prop_sum <= sum(props[:2]): <- (For more events)
    else:
            S.append(S[-1])
            I.append(I[-1] - 1)
            R.append(R[-1] + 1)    


figure1,(ax1,ax2,ax3) = plt.subplots(3) # Plotting Gillespie ODE in figure 1:

line1 = ax1.plot(t,S) # S
line2 = ax2.plot(t,I) # I
line3 = ax3.plot(t,R) # R

ax1.set_ylabel("Susceptible")
ax2.set_ylabel("Infected")
ax3.set_ylabel("Recovered")
ax3.set_xlabel("Time (arbitrary units)")
plt.suptitle("Stochastic SIR Model")

    # Overlapping normal ODE and Gillespie algorithm ODE:

figure2,(ax1,ax2,ax3) = plt.subplots(3)

# First plotting Gillespie ODE (again but now on figure 2):
line1 = ax1.plot(t,S) # S
line2 = ax2.plot(t,I) # I
line3 = ax3.plot(t,R) # R

# Standard (deterministic) SIR ODE:
t = np.linspace(0,tend, num=500)
params = [beta,gamma]
y0 = [999, 1, 0]


def sim(variables, t, params):

    S = variables[0]
    I = variables[1]
    R = variables[2]

    N = S + I + R

    beta = params[0]
    gamma = params[1]

    dSdt = -beta * I * S / N
    dIdt = beta * I * S / N - gamma * I
    dRdt = gamma * I

    return([dSdt, dIdt, dRdt])


y = odeint(sim, y0, t, args=(params,))

# Now plotting standard ODE results (over Gillespie ODE in figure 2):
line1 = ax1.plot(t,y[:,0]) # S
line2 = ax2.plot(t,y[:,1]) # I
line3 = ax3.plot(t,y[:,2]) # R

ax1.set_ylabel("Susceptible")
ax2.set_ylabel("Infected")
ax3.set_ylabel("Recovered")
ax3.set_xlabel("Time Steps")
ax1.legend(["Stochastic SIR","Deterministic SIR"],loc="upper right")
plt.suptitle("Deterministic vs Stochastic SIR Model")

plt.show()
