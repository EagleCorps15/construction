
import random
import numpy as np

try:
    import matplotlib.pyplot as plt
    _MATPLOTLIB_AVAILABLE = True
except Exception:
    plt = None
    _MATPLOTLIB_AVAILABLE = False

def percentile(data, percent):
    """Return the percentile of the data list (percent between 0-100)."""
    if not data:
        return 0.0
    k = (len(data) - 1) * (percent / 100.0)
    f = int(k)
    c = f + 1
    data_sorted = sorted(data)
    if c >= len(data_sorted):
        return float(data_sorted[-1])
    d0 = data_sorted[f] * (c - k)
    d1 = data_sorted[c] * (k - f)
    return float(d0 + d1)


# ---------------------------------
# Triangular Distribution Function
# ---------------------------------
def activity_duration(min_t, most_t, max_t):
    return random.triangular(min_t, max_t, most_t)


# ---------------------------------
# Input Helper
# ---------------------------------
def get_phase_input(name):
    while True:
        try:
            print(f"\n{name}")
            min_t = float(input("  Optimistic duration: "))
            most_t = float(input("  Most likely duration: "))
            max_t = float(input("  Pessimistic duration: "))

            if not (min_t <= most_t <= max_t):
                print("⚠ Values must follow: Optimistic ≤ Most Likely ≤ Pessimistic")
                continue

            return (min_t, most_t, max_t)

        except:
            print("⚠ Invalid input. Please enter numeric values.")


# ---------------------------------
# Main Program
# ---------------------------------

def main():

    print("\n===== High-Rise Construction Risk Analysis Simulation =====")

    try:
        number_of_floors = int(input("Enter number of floors: "))
        planned_duration = float(input("Enter planned project duration (days): "))
        simulations = int(input("Enter number of simulation runs: "))
    except:
        print("⚠ Invalid input. Restart program.")
        return

    # ---------------------------------
    # Base Construction Phases
    # ---------------------------------
    base_phases = {

        "Site Preparation": get_phase_input("Site Preparation"),
        "Foundation": get_phase_input("Foundation"),
        "Exterior Work": get_phase_input("Exterior Work"),
        "MEP Installation": get_phase_input("MEP Installation"),
        "Interior Finishing": get_phase_input("Interior Finishing")
    }

    print("\nFloor Construction Duration (per floor)")
    floor_activity = get_phase_input("Each Floor")

    # ---------------------------------
    # Storage Containers
    # ---------------------------------
    results = []

    phase_delay_contribution = {phase: 0 for phase in base_phases}
    floor_delay_contribution = 0

    # ---------------------------------
    # Monte Carlo Simulation
    # ---------------------------------
    for _ in range(simulations):

        total_time = 0
        phase_times = {}

        # Base phases
        for phase, duration in base_phases.items():
            time_taken = activity_duration(*duration)
            phase_times[phase] = time_taken
            total_time += time_taken

        # Floor repetition

        floor_time_total = 0
        for _ in range(number_of_floors):
            floor_time_total += activity_duration(*floor_activity)

        total_time += floor_time_total
        results.append(total_time)

        # Delay contribution tracking
        if total_time > planned_duration:
            for phase in phase_times:
             results_array = np.array(results)


    average_duration = np.mean(results_array)
    delay_probability  = np.sum(results_array > planned_duration) / simulations
    # Statistical Analysis
    # ---------------------------------
    results_array = np.array(results)


    average_duration = np.mean(results_array)
    delay_probabilit  = np.sum(results_array > planned_duration) / simulations

    # Confidence Levels
    p50 = np.percentile(results_array, 50)
    p80 = np.percentile(results_array, 80)
    p90 = np.percentile(results_array, 90)

    # Risk Contribution Calculation
    total_contribution = sum(phase_delay_contribution.values()) + floor_delay_contribution

    risk_percentages = {}

    if total_contribution > 0:
        for phase in phase_delay_contribution:
            risk_percentages[phase] = (

                phase_delay_contribution[phase] / total_contribution
            ) * 100

        risk_percentages["Floor Construction"] = (
            floor_delay_contribution / total_contribution
        ) * 100

    # ---------------------------------
    # OUTPUT RESULTS
    # ---------------------------------
    print("\n===== Simulation Summary =====")
    print(f"Average Completion Time: {average_duration:.2f} days")
    print(f"Probability of Delay: {delay_probability*100:.2f}%")

    print("\n===== Confidence Levels =====")
    print(f"P50 Completion Time: {p50:.2f} days")
    print(f"P80 Completion Time: {p80:.2f} days")
    print(f"P90 Completion Time: {p90:.2f} days")

    if total_contribution > 0:
        print("\n===== Risk Contribution Ranking =====")

        sorted_risks = sorted(
            risk_percentages.items(),
            key=lambda x: x[1],
            reverse=True
        )
    # ---------------------------------
    # Visualization – Completion Distribution
    # ---------------------------------
    if _MATPLOTLIB_AVAILABLE:
        plt.figure()
        plt.hist(results_array, bins=40)
        plt.axvline(planned_duration, color="red")
        plt.title("Project Completion Time Distribution")
        plt.xlabel("Duration (Days)")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("\nMatplotlib not available; skipping completion time plot.")

    # ---------------------------------
    # Visualization – Risk Contribution
    # ---------------------------------
    if total_contribution > 0:
        labels = list(risk_percentages.keys())
        values = list(risk_percentages.values())

        if _MATPLOTLIB_AVAILABLE:
            plt.figure()
            plt.bar(labels, values)
            plt.xticks(rotation=45)
            plt.title("Risk Contribution by Phase")
            plt.ylabel("Risk Contribution (%)")
            plt.show()
        else:
            print("\nMatplotlib not available; skipping risk contribution plot.")

        plt.figure()
        plt.bar(labels, values)
        plt.xticks(rotation=45)
        plt.title("Risk Contribution by Phase")
        plt.ylabel("Risk Contribution (%)")
        plt.show()


# ---------------------------------
# Run Program
# ---------------------------------
if __name__ == "__main__":
    main()





