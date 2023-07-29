import numpy as np
import matplotlib.pyplot as plt

def effective_interest_rate(nominal_rate, compounding_periods_per_year):
    effective_rate_calc = (1 + nominal_rate / compounding_periods_per_year) ** compounding_periods_per_year
    return effective_rate_calc - 1

nominal_rate_input = float(input("Enter the nominal annual interest rate (as a decimal): "))

# Generate compounding periods from 1 to 365 (daily compounding)
compounding_periods = np.arange(1, 366)
effective_rates = effective_interest_rate(nominal_rate_input, compounding_periods)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(compounding_periods, effective_rates * 100, label='Effective Interest Rate')
plt.xlabel('Compounding Periods per Year')
plt.ylabel('Effective Interest Rate (%)')
plt.title('Effective Interest Rate vs. Compounding Periods')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
