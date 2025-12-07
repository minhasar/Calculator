"""
Simple Python Calculator
Supports basic arithmetic operations: addition, subtraction, multiplication, division
"""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    """Main calculator loop."""
    print("=== Python Calculator ===")
    print("Operations: +, -, *, /")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("Enter expression (e.g., 5 + 3): ").strip()

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Parse input
            parts = user_input.split()
            if len(parts) == 1:
                # Try to parse without spaces (e.g., "4+5")
                for op_char in ['+', '-', '*', '/']:
                    if op_char in user_input:
                        parts = user_input.replace(op_char, f' {op_char} ').split()
                        break
            
            if len(parts) != 3:
                print("Invalid format. Use: number operator number (e.g., 4 + 5 or 4+5)\n")
                continue

            a, op, b = parts
            try:
                a, b = float(a), float(b)
            except ValueError:
                print("Invalid numbers. Please enter valid numbers.\n")
                continue

            # Calculate
            if op == "+":
                result = add(a, b)
            elif op == "-":
                result = subtract(a, b)
            elif op == "*":
                result = multiply(a, b)
            elif op == "/":
                result = divide(a, b)
            else:
                print("Invalid operator. Use: +, -, *, /\n")
                continue

            print(f"Result: {result}\n")

        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Invalid input: {e}\n")


if __name__ == "__main__":
    main()
