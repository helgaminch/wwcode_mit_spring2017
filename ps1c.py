
def find_best_savings_rate(starting_salary):
    low = 0
    high = 10000
    steps = 0
    # Bisection search for the best savings rate
    while True:
        steps += 1
        best_savings_rate_guess = (high + low) // 2
        current_savings = 0
        annual_salary = starting_salary
        for months in range(36):
            current_savings += annual_salary / 12 * best_savings_rate_guess / 10000 + current_savings * 0.04 / 12
            # Salary is raised for 7% AFTER every 6 months
            if months != 0 and months % 6 == 0:
                annual_salary += annual_salary * 0.07

        # Savings + or - 100$ are OK
        if 249900 <= current_savings <= 250100:
            print("Best savings rate:", best_savings_rate_guess / 10000)
            print("Steps in bisection search:", steps)
            return
        if current_savings < 249900:
            low = best_savings_rate_guess
        elif current_savings > 250100:
            high = best_savings_rate_guess
        if steps > 14:
            print("It is not possible to pay the down payment in three years.")
            return


salary = int(input("Enter the starting salary:"))
find_best_savings_rate(salary)
