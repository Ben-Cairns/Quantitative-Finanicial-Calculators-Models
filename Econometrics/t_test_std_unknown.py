#This code will allow you to determine if the mean has changed with an unknown population std

import math
import scipy.stats as stats

def t_test(sample_mean, population_mean, sample_std, observations, confidence_interval):
    t = (sample_mean - population_mean) / (sample_std / math.sqrt(observations))

    if abs(t) > stats.t.ppf(1 - (1 - confidence_interval) / 2, observations - 1):
        print("Sufficient evidence to reject hypothesis")
    else:
        print("Insufficient evidence to reject hypothesis")

    return t

# User inputs
sample_mean = float(input('Enter the sample mean: '))
population_mean = float(input('Enter the population mean: '))
sample_std = float(input('Enter the sample std: '))
observations = float(input('Enter the number of observations: '))

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

t_score = t_test(sample_mean, population_mean, sample_std, observations, confidence_interval)

print(f"Calculated t-score: {t_score}")
