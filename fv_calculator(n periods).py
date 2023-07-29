
#Visualising the number of months (n) it will take to reach a future value at a given interest rate

import math
import matplotlib.pyplot as plt

def solve_periods_for_future_value (fv, pv, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / 12
    periods_in_months = math.log(fv/pv) / math.log (1+ monthly_interest_rate)
    return periods_in_months

#Variables
future_value = 1500
present_value = 1000

#Creating a list of interest rates (1-20%) to visualise the time periods per rate
interest_rates = [i / 100 for i in range(1,21)]

#Calculating the number of periods in months for a given interest rate
periods_in_months = []
for rate in interest_rates:
    num_periods_in_months = solve_periods_for_future_value (future_value, present_value, rate)
    periods_in_months.append(num_periods_in_months)
    
#Plotting the data
plt.figure(figsize=(8, 6))
plt.plot(interest_rates, periods_in_months, marker='o')
plt.xlabel("Annual Interest Rate")
plt.ylabel("Number of Periods (Months)")
plt.title("Number of Periods vs. Annual Interest Rate")
plt.grid(True)
plt.xticks(interest_rates, [str(int(rate * 100)) + "%" for rate in interest_rates])

#Making the y-axis increment by 0.25
max_periods = math.ceil(max(periods_in_months))
plt.yticks(range(0, max_periods + 1, 25))

plt.show()
