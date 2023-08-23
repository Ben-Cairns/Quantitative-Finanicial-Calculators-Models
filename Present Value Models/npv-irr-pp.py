"""This model will calculate the NPV of future cash flows as well as the IRR and payback period of the investment 
in order to determine its profitablility and viability"""

def npv_calculation(initial_cost, cash_flows, discount_rate):
    npv = -initial_cost
    
    for t, cash_flow in enumerate(cash_flows, start=1):
        present_value = cash_flow / (1 + discount_rate)**t
        npv += present_value
    
    return npv

def irr_calculation(initial_cost, cash_flows):
    guess = 0.1 
    tolerance = 0.0001  
    max_iterations = 1000
    
    for _ in range(max_iterations):
        npv = npv_calculation(initial_cost, cash_flows, guess)
        derivative = 0
        
        for t, cash_flow in enumerate(cash_flows, start=1):
            derivative -= t * cash_flow / (1 + guess)**(t + 1)
        
        guess = guess - npv / derivative
        
        if abs(npv) < tolerance:
            return guess
    
    return None

def payback_periods_calculation(initial_cost, cash_flows):
    cost = initial_cost
    periods = 0
    
    for cash_flow in cash_flows:
        if cash_flow < cost:
            cost -= cash_flow
            periods += 1
            
            if cost <= 0:
                break
            
    return periods


def viable_investment(discount_rate):
    if irr > discount_rate:
        return "The investment is viable"
    else:
        return "The investment is not viable"
    


initial_cost = float(input("What is the initial cost of the investment?: "))
cash_flows = [float(x) for x in input("Input the expected cash flows per year (comma-separated): ").split(',')]
discount_rate = float(input("What is the discount rate? (%): ")) / 100

npv = npv_calculation(initial_cost, cash_flows, discount_rate)
npv_rounded = round(npv, 2)
print("NPV:", npv_rounded)

irr = irr_calculation(initial_cost, cash_flows)
irr_rounded = round(irr * 100, 2)
print("IRR:", irr_rounded,"%")

payback_period = payback_periods_calculation(initial_cost, cash_flows)
print("Payback Period:", payback_period, "Years")

difference = round(irr_rounded - discount_rate*100, 2)

viablility = viable_investment(discount_rate)
print(viablility, f"with a difference of {difference}" "%")


#Still need to implement argument to see whether the npv is positive and add it to viability


#Need to graph the path of the npv per cost of capital (evidenced in my excel doc)




