import numpy as np
import pandas as pd

# Example Monte Carlo for three activities
def sample_duration(opt, ml, pes):
    # Triangular distribution
    return np.random.triangular(opt, ml, pes)

# Define tasks with (optimistic, most_likely, pessimistic)
tasks = {
    "Task1": (5, 8, 12),
    "Task2": (3, 5, 7),
    "Task3": (4, 7, 10)
}

n_sims = 10000
results = []

for i in range(n_sims):
    total_duration = sum(
        sample_duration(*tasks[t]) for t in tasks
    )
    results.append(total_duration)

df = pd.DataFrame(results, columns=["Project_Duration"])
print(df.describe())