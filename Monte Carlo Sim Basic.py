import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

avg = 1
std_dev = .1
num_reps = 500
num_simulations = 1000

results = []

for i in range(num_simulations):
    draws = np.random.normal(avg, std_dev, num_reps)
    results.append(draws.mean())

results = np.array(results) 

plt.figure(figsize=(10, 5))
plt.hist(results, bins=30)
plt.title("Monte Carlo Simulation Results")
plt.xlabel("Mean Value")
plt.ylabel("Frequency")
plt.show()