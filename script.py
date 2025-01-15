inputNumber = int(input("Your number: "))

def stepCalculator(inputNumber):
    steps = "0"
    if inputNumber < 25:
        steps = "8000"
    elif inputNumber >= 25 & inputNumber < 50:
        steps = "7000"
    elif inputNumber >= 50 & inputNumber < 60:
        steps = "6000"
    else:
        steps = "5000"
    
    return steps

steps = stepCalculator(inputNumber)

print(steps)