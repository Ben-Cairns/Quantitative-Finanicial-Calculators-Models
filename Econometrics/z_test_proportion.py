import math
from scipy.stats import norm

def z_proportion(successes, num, proportion):
    
    sample_proportion = successes/num
    z = (sample_proportion - proportion) / math.sqrt(((proportion*(1-proportion))/num))

    return z

#User Inputs
successes = float(input("Enter the number of successes in the sample: "))
proportion = float(input("Enter the hypothesised proportion of successes in the population (decimal format): "))
num = float(input("Enter the sample size: "))

confidence_level = input('Enter the desired confidence level (99%, 95%, or 90%): ')
confidence_interval = 0.0

if confidence_level == '99%':
    confidence_interval = 0.99
elif confidence_level == '95%':
    confidence_interval = 0.95
elif confidence_level == '90%':
    confidence_interval = 0.90
else:
    print("Invalid confidence level entered.")

z_score = z_proportion(successes, num, proportion)

print(z_score)

# Calculate the critical z-score based on the desired confidence interval
critical_z = norm.ppf(1 - (1 - confidence_interval) / 2)

if abs(z_score) <= critical_z:
    print("Insufficient evidence to reject the hypothesis.")
else:
    print("Sufficient evidence to reject the hypothesis.")