import numpy as np
import matplotlib.pyplot as plt

# Input parameters
min_days = 8
most_likely = 10
max_days = 15
iterations = 10000

# Monte Carlo Simulation
duration_samples = np.random.triangular(
    min_days, most_likely, max_days, iterations
)

# Results
mean_duration = np.mean(duration_samples)
p_delay = np.sum(duration_samples > 12) / iterations

print("Expected Duration:", round(mean_duration, 2))
print("Probability of exceeding 12 days:", round(p_delay*100, 2), "%")

# Visualization
plt.hist(duration_samples, bins=50)
plt.xlabel("Project Duration (days)")
plt.ylabel("Frequency")
plt.title("Monte Carlo Simulation of Project Duration")
plt.show()
