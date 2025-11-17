import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

avg = 1
std_dev = .1
num_reps = 500
num_simulations = 10000


team1_expected_score = 23
team2_expected_score = 20

team1_score = np.random.poisson(team1_expected_score, size = num_simulations)
team2_score = np.random.poisson(team2_expected_score, size = num_simulations)

team1_wins = np.sum(team1_score > team2_score)
team2_wins = np.sum(team2_score > team1_score)
tie = np.sum(team1_score == team2_score)

team1_win_prob = team1_wins / num_simulations
team2_win_prob = team2_wins / num_simulations
tie_prob = tie / num_simulations

print(f"Team 1 win probability: {team1_win_prob:.3%}")
print(f"Team 2 win probability: {team2_win_prob:.3%}")
print(f"Tie probability: {tie_prob:.3%}")

plt.figure(figsize=(10,5))
plt.hist(team1_score, bins=range(0, 60), alpha=0.5, label="Team 1")
plt.hist(team2_score, bins=range(0, 60), alpha=0.5, label="Team 2")
plt.title("Simulated Score Distributions")
plt.xlabel("Points Scored")
plt.ylabel("Frequency")
plt.legend()
plt.show()
