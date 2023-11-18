# Function to generate three-address code for a boolean expression
def generate_boolean_expression_code(expression):
    code = []
    label_count = 1

    # Function to generate new temporary variables
    def new_temp():
        nonlocal label_count
        temp_var = f"t{label_count}"
        label_count += 1
        return temp_var

    # Stack to manage operands and operators
    operand_stack = []
    operator_stack = []

    # Operator precedence
    precedence = {"NOT": 3, "AND": 2, "OR": 1}

    # Split the expression into tokens
    tokens = expression.split()
    # Sample: ['A', 'AND', 'B', 'OR', 'C']
    for token in tokens:
        if token not in ["AND", "OR", "NOT"]:
            operand_stack.append(token)
            print("Current operand stack: ", operand_stack)
        elif token in ["AND", "OR", "NOT"]:
            while (
                operator_stack
                and operator_stack[-1] != "("
                and precedence[operator_stack[-1]] >= precedence[token]
                and len(operand_stack) >= 2
            ):
                operator = operator_stack.pop()
                if operator == "NOT":
                    operand1 = operand_stack.pop()
                    temp = new_temp()
                    code.append(f"{temp} = NOT {operand1}")
                    operand_stack.append(temp)
                else:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    temp = new_temp()
                    code.append(f"{temp} = {operand1} {operator} {operand2}")
                    operand_stack.append(temp)
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                operator = operator_stack.pop()
                if operator == "NOT":
                    operand1 = operand_stack.pop()
                    temp = new_temp()
                    code.append(f"{temp} = NOT {operand1}")
                    operand_stack.append(temp)
                else:
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    temp = new_temp()
                    code.append(f"{temp} = {operand1} {operator} {operand2}")
                    operand_stack.append(temp)
            if operator_stack and operator_stack[-1] == "(":
                operator_stack.pop()

    # Process any remaining operators
    while operator_stack:
        operator = operator_stack.pop()
        if operator == "NOT":
            operand1 = operand_stack.pop()
            temp = new_temp()
            code.append(f"{temp} = NOT {operand1}")
            operand_stack.append(temp)
        else:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            temp = new_temp()
            code.append(f"{temp} = {operand1} {operator} {operand2}")
            operand_stack.append(temp)
    return code

# Function to generate three-address code for an if statement (unchanged)
def generate_if_statement_code(condition, code_if_true, code_if_false):
    code = []
    # Code for evaluating the condition and branching
    code.append(f"if {condition} goto true_label")
    code.extend(code_if_false)
    code.append("goto end_label")
    code.append("true_label:")
    code.extend(code_if_true)
    code.append("end_label:")
    return code

# Function to generate three-address code for a switch statement (unchanged)
def generate_switch_statement_code(expression, cases, default_case, default_code):
    code = []
    # Code for evaluating the expression
    result = "result"
    code.append(f"{result} = {expression}")
    
    # Create labels for case branches
    case_labels = [f"case_{i}" for i in range(len(cases))]
    
    # Code for branching to the appropriate case
    for i, case_value in enumerate(cases):
        code.append(f"if {result} == {case_value} goto {case_labels[i]}")
    
    # Default case code
    code.append(f"goto {default_case}")
    
    # Code for each case
    for i, case_value in enumerate(cases):
        code.append(f"{case_labels[i]}:")
        code.extend(cases[case_value])
    
    # Default case code
    code.append(f"{default_case}:")
    code.extend(default_code)
    
    return code

# Function to generate three-address code for a while loop
def generate_while_loop_three_address_code(condition, body):
    code = []
    label_count = 1

    # Create labels for loop and end of loop
    loop_label = f"loop_{label_count}"
    end_loop_label = f"end_loop_{label_count}"
    
    # Add label for the start of the loop
    code.append(f"{loop_label}:")

    # Generate code for evaluating the loop condition
    code.extend(generate_boolean_expression_code(condition))

    # Add a conditional jump to the end of the loop
    # code.append(f"if {t3} == False goto {end_loop_label}")

    # Generate code for the loop body
    code.extend(body)

    # Add an unconditional jump back to the start of the loop
    code.append(f"goto {loop_label}")

    # Add label for the end of the loop
    code.append(f"{end_loop_label}:")

    return code

# Main program (expanded with while loop)
while True:
    print("\nPlease choose the functionality you want to generate code for:")
    print("1. Boolean Expression")
    print("2. If Statement")
    print("3. Switch Statement")
    print("4. While Loop")
    print("5. Exit")

    choice = input("Enter the corresponding number (1/2/3/4/5): ")

    if choice == '1':
        # Take user input for a boolean expression
        expression = input("Enter a boolean expression: ")
        # Generate three-address code for the boolean expression
        three_address_code = generate_boolean_expression_code(expression)
    

    elif choice == '2':
        condition = input("Enter the condition: ")
        code_if_true = []

        print("Enter code for the true branch (end with an empty line):")
        while True:
            line = input()
            if not line:
                break
            code_if_true.append(line)
        code_if_false = []

        print("Enter code for the false branch (end with an empty line):")
        while True:
            line = input()
            if not line:
                break
            code_if_false.append(line)

        # Generate the three-address code for the if statement
        three_address_code = generate_if_statement_code(condition, code_if_true, code_if_false)

    elif choice == '3':
        expression = input("Enter the expression for the switch statement: ")
        cases = {}
        default_case = input("Enter the label for the default case: ")
        default_code = []

        while True:
            case_value = input("Enter a case value (or 'done' to finish): ")
            if case_value.lower() == 'done':
                break
            case_code = []

            while True:
                line = input(f"Enter code for case {case_value} (or 'done' to finish): ")
                if line.lower() == 'done':
                    break
                case_code.append(line)

            cases[case_value] = case_code

        # Generate the three-address code for the switch statement
        three_address_code = generate_switch_statement_code(expression, cases, default_case, default_code)

    elif choice == '4':
        condition = input("Enter the loop condition: ")
        loop_code = []

        print("Enter code for the loop body (end with an empty line):")
        while True:
            line = input()
            if not line:
                break
            loop_code.append(line)

        # Generate the three-address code for the while loop
        three_address_code = generate_while_loop_three_address_code(condition, loop_code)

    elif choice == '5':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please choose 1, 2, 3, 4, or 5.")

    # Print the generated three-address code
    print("Generated Three-Address Code:")
    for i, line in enumerate(three_address_code, start=1):
        print(f"{i}. {line}")