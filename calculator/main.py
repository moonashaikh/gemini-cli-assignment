from calculator import add, subtract, multiply, divide

def main():
    print("Simple Calculator")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operation = input("Enter operation (+, -, *, /): ")

    result = None
    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        try:
            result = divide(num1, num2)
        except ValueError as e:
            print(e)
    else:
        print("Invalid operation")

    if result is not None:
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
