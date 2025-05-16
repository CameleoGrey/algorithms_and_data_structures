def evaluate_expression(expression):
    """
    Evaluates a mathematical expression using Dijkstra's Two-Stack Algorithm.
    Supports +, -, *, /, parentheses, and negative numbers with proper operator precedence.
    """
    import re
    
    # Improved tokenization that handles negative numbers and spaces
    tokens = re.findall(r"(\d+\.?\d*|[-+*/()]|-\d+\.?\d*)", expression.replace(" ", ""))
    
    operand_stack = []
    operator_stack = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            # Process all operations until matching '('
            while operator_stack and operator_stack[-1] != '(':
                apply_operation(operand_stack, operator_stack)
            if not operator_stack:
                raise ValueError("Mismatched parentheses")
            operator_stack.pop()  # Remove the '('
        elif token in precedence:
            # Handle negative numbers (unary minus)
            if token == '-' and (i == 0 or tokens[i-1] == '(' or tokens[i-1] in precedence):
                # It's a negative number, not subtraction
                i += 1
                if i >= len(tokens):
                    raise ValueError("Incomplete expression")
                operand_stack.append(-float(tokens[i]))
            else:
                # Process higher or equal precedence operations
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    apply_operation(operand_stack, operator_stack)
                operator_stack.append(token)
        else:  # Number
            try:
                operand_stack.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid number: {token}")
        i += 1
    
    # Process remaining operations
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        apply_operation(operand_stack, operator_stack)
    
    if len(operand_stack) != 1:
        raise ValueError("Invalid expression")
    
    return operand_stack.pop()

def apply_operation(operand_stack, operator_stack):
    """Applies the top operator to the top two operands."""
    if len(operand_stack) < 2:
        raise ValueError("Not enough operands for operation")
    
    operator = operator_stack.pop()
    right = operand_stack.pop()
    left = operand_stack.pop()
    
    if operator == '+':
        operand_stack.append(left + right)
    elif operator == '-':
        operand_stack.append(left - right)
    elif operator == '*':
        operand_stack.append(left * right)
    elif operator == '/':
        if right == 0:
            raise ValueError("Division by zero")
        operand_stack.append(left / right)
    else:
        raise ValueError(f"Unknown operator: {operator}")

# Example usage
if __name__ == "__main__":
    expressions = [
        "3 + 4 * 5",
        "(3 + 4) * 5",
        "10 - 2 * 3",
        "(10 - 2) * 3",
        "2 * (3 + 4 * 5) - 6 / 2",
        "2.5 * 4 + 1.5",
        "-5 + 3 * 2",
        "3 * (-4 + 2)",
        "10 / (2 + 3)",
        "1 + 2 * (3 + 4) - 5"
    ]
    
    for expr in expressions:
        try:
            result = evaluate_expression(expr)
            print(f"Expression: {expr} = {result}")
        except ValueError as e:
            print(f"Error evaluating '{expr}': {e}")