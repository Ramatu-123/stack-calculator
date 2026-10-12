class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0



def precedence(op):
    """Higher number = done first. * and / beat + and -."""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_operator(numbers, operators):
    """Take one operator and two numbers, calculate, push the answer back."""
    op = operators.pop()
    right = numbers.pop()
    left = numbers.pop()

    if op == '+':
        numbers.push(left + right)
    elif op == '-':
        numbers.push(left - right)
    elif op == '*':
        numbers.push(left * right)
    elif op == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        numbers.push(left / right)


def evaluate(expression):
    """Evaluate one expression like '3 + 5 * 2' and return the answer."""
    numbers = Stack()
    operators = Stack()
    i = 0

    while i < len(expression):
        ch = expression[i]


        if ch == ' ':
            i += 1
            continue


        if ch.isdigit() or ch == '.':
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            numbers.push(float(expression[start:i]))
            continue


        elif ch == '(':
            operators.push(ch)


        elif ch == ')':
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator(numbers, operators)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()


        elif ch in '+-*/':
            while (not operators.is_empty()
                   and operators.peek() != '('
                   and precedence(operators.peek()) >= precedence(ch)):
                apply_operator(numbers, operators)
            operators.push(ch)

        else:
            raise ValueError(f"Invalid character: {ch}")

        i += 1


    while not operators.is_empty():
        if operators.peek() == '(':
            raise ValueError("Mismatched parentheses")
        apply_operator(numbers, operators)

    return numbers.pop()



def is_separator(line):
    """A separator line contains only dashes, like -----"""
    return len(line) > 0 and set(line) == {'-'}


def create_sample_input(filename):
    """If input.txt is missing, make a sample one so the program still runs."""
    with open(filename, 'w') as file:
        file.write("3 + 5 * 2\n")
        file.write("-----\n")
        file.write("(8 / 4) + 7 * 2\n")
        file.write("-----\n")
        file.write("10 - (2 + 3) * 4\n")
    print(f"{filename} was not found, so a sample file was created.")


def read_expressions(filename):
    """Read input.txt and return a list of expressions (separators skipped)."""
    expressions = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()

                if line == '':
                    continue
                if is_separator(line):
                    continue

                expressions.append(line)
    except FileNotFoundError:
        create_sample_input(filename)
        return read_expressions(filename)

    return expressions


def evaluate_all(expressions):
    """Evaluate every expression. A bad one gives an error message, not a crash."""
    results = []

    for expr in expressions:
        try:
            results.append(evaluate(expr))
        except (ValueError, ZeroDivisionError, IndexError) as error:
            results.append(f"Error: {error}")

    return results



def format_result(result):
    """Show 13.0 as 13, and keep decimals like 2.5 as they are."""
    if isinstance(result, float):
        if result.is_integer():
            return str(int(result))
        return str(round(result, 4))
    return str(result)


def write_results(filename, results):
    """Write one result per line with ----- between them."""
    with open(filename, 'w') as file:
        for i, result in enumerate(results):
            file.write(format_result(result) + "\n")
            if i < len(results) - 1:
                file.write("-----\n")



def main():
    expressions = read_expressions("input.txt")
    results = evaluate_all(expressions)

    # Show on screen too (good for your testing screenshots)
    for expr, result in zip(expressions, results):
        print(expr, "=", format_result(result))

    write_results("output.txt", results)
    print("Done! Results written to output.txt")


if __name__ == "__main__":
    main()