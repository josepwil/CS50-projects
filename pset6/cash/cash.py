import cs50

# init value of coins
quarter = 25
dime = 10
nickel = 5
penny = 1


while True:
    dollars = cs50.get_float("Change to give: ")
    if (dollars > 0): 
        break

cents = round(dollars * 100)
coins = 0

while (cents > 0):
    if (cents - quarter >= 0):
        cents = cents - 25
        coins += 1
    elif (cents - dime >= 0):
        cents = cents - 10
        coins += 1
    elif (cents - nickel >= 0):
        cents = cents - 5
        coins += 1
    else: 
        cents = cents - 1
        coins += 1
print(coins)        