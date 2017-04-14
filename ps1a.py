annual_salary = int(input("Enter your annual salary:"))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal:"))
total_cost = int(input("Enter the cost of your dream home:"))

monthly_salary = annual_salary / 12
# Assume that our down payment is 25%
portion_down_payment = total_cost * 0.25
# Assume that our investments earn a return of 4% a year
r = 0.04
current_savings = 0
months_count = 0

while current_savings < portion_down_payment:
    months_count += 1

    current_savings += monthly_salary * portion_saved + current_savings * r / 12


print("Number of months:", months_count)