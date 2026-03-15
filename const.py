import random
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Triangular Distribution
# -----------------------------
def activity_duration(min_t, most_t, max_t):
    return random.triangular(min_t, max_t, most_t)

print("\n===== High-Rise Construction Risk Analysis Simulation =====")

# ---------------------
# --------
# USER INPUT
# -----------------------------
number_of_floors = int(input("Enter number of floors: "))
PLANNED_DURATION = float(input("Enter planned project duration (days): "))
SIMULATIONS = int(input("Enter number of simulation runs: "))

print("\n--- Enter Base Phase Durations ---")

def get_phase_input(name):
    min_t = float(input(f"{name} - Optimistic duration: "))
    most_t = float(input(f"{name} - Most likely duration: "))
    max_t = float(input(f"{name} - Pessimistic duration: "))
    return (min_t, most_t, max_t)

base_phases = {
    "Site Preparation": get_phase_input("Site Preparation"),
    "Foundation": get_phase_input("Foundation"),
    "Exterior Work": get_phase_input("Exterior Work"),
    "MEP Installation": get_phase_input("MEP Installation"),
    "Interior Finishing": get_phase_input("Interior Finishing")
}

print("\n--- Floor Construction Duration ---")
floor_activity = get_phase_input("Each Floor")

# -----------------------------
# STORAGE
# -----------------------------
results = []
phase_delay_contribution = {phase: 0 for phase in base_phases}
floor_delay_contribution = 0

# -----------------------------
# MONTE CARLO SIMULATION
# -----------------------------
for _ in range(SIMULATIONS):

    total_time = 0
    phase_times = {}

    # Base phases simulation
    for phase, duration in base_phases.items():
        time_taken = activity_duration(*duration)
        phase_times[phase] = time_taken
        total_time += time_taken

    # Floor simulation
    floor_time_total = 0
    for _ in range(number_of_floors):
        floor_time_total += activity_duration(*floor_activity)

    total_time += floor_time_total

    results.append(total_time)

    # ----- Delay contribution tracking -----
    if total_time > PLANNED_DURATION:

        for phase in phase_times:
            phase_delay_contribution[phase] += phase_times[phase]

        floor_delay_contribution += floor_time_total

# -----------------------------
# STATISTICS
# -----------------------------
average_duration = np.mean(results)
delay_probability = sum(1 for r in results if r > PLANNED_DURATION) / SIMULATIONS

# -----------------------------
# Confidence Intervals (95%)
# -----------------------------
n = SIMULATIONS
if n > 1:
    std_dev = np.std(results, ddof=1)
    se_mean = std_dev / np.sqrt(n)
    z = 1.96
    ci_mean = (average_duration - z * se_mean, average_duration + z * se_mean)
else:
    ci_mean = (average_duration, average_duration)

# CI for delay probability (proportion)
p = delay_probability
if n > 0:
    se_p = np.sqrt(p * (1 - p) / n)
    ci_p = (max(0.0, p - z * se_p), min(1.0, p + z * se_p))
else:
    ci_p = (p, p)

# Normalize contribution percentages
total_contribution = sum(phase_delay_contribution.values()) + floor_delay_contribution

risk_percentages = {}

for phase in phase_delay_contribution:
    risk_percentages[phase] = (phase_delay_contribution[phase] / total_contribution) * 100

risk_percentages["Floor Construction"] = (floor_delay_contribution / total_contribution) * 100

# -----------------------------
# OUTPUT RESULTS
# -----------------------------
print("\n===== Simulation Summary =====")
print(f"Average Completion Time: {average_duration:.2f} days")
print(f"Probability of Delay: {delay_probability*100:.2f}%")
print(f"95% CI (average completion time): {ci_mean[0]:.2f} - {ci_mean[1]:.2f} days")
print(f"95% CI (delay probability): {ci_p[0]*100:.2f}% - {ci_p[1]*100:.2f}%")

print("\n===== Risk Contribution Ranking =====")

sorted_risks = sorted(risk_percentages.items(), key=lambda x: x[1], reverse=True)

for phase, risk in sorted_risks:
    print(f"{phase}: {risk:.2f}%")

# -----------------------------
# VISUALIZATION 1 – Completion Distribution
# -----------------------------
plt.figure()
plt.hist(results, bins=40)
plt.axvline(PLANNED_DURATION)
plt.title("Project Completion Time Distribution")
plt.xlabel("Duration (Days)")
plt.ylabel("Frequency")
plt.show()

# -----------------------------
# VISUALIZATION 2 – Risk Contribution
# -----------------------------
labels = list(risk_percentages.keys())
values = list(risk_percentages.values())

plt.figure()
plt.bar(labels, values)
plt.xticks(rotation=45)
plt.title("Risk Contribution by Construction Phase")
plt.ylabel("Risk Contribution (%)")
plt.show()
