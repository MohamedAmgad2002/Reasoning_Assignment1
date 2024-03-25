import re

# regular expression to match a function expression
FUNC_EXPR = r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)"

def get_params(param_str):
    open_index = param_str.find('(')
    close_index = param_str.rfind(')')
    return param_str[open_index+1:close_index]


def is_variable(param):
    return param.islower() and len(param.strip()) == 1


def is_func(param):
    return bool(re.search(FUNC_EXPR, param))


def is_constant(param):
    return param.isupper() and len(param.strip()) >= 1


def replace_innermost_func(code, idx):
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\((\w+)\)"

    def repl(match):
        return f"{match.group(1)}({match.group(2)}{idx})"
    return re.sub(pattern, repl, code)


def standardize(kb):
    for idx, clause in enumerate(kb):
        clause = clause[1:-1]
        literals = clause.split('|')
        for i in range(len(literals)):
            # Extract parameters and their positions in the literal
            params = get_params(literals[i])
            params = params.split(',')
            for j in range(len(params)):
                # If the parameter is a variable, append the clause index to it
                if is_variable(params[j]):
                    params[j] = params[j] + str(idx)
                # If the parameter is a function expression
                elif is_func(params[j]):
                    params[j] = replace_innermost_func(params[j], idx)
            # Replace the literal parameters with the new parameters
            literals[i] = literals[i][:literals[i].find(
                '(')+1] + ','.join(params) + literals[i][literals[i].find(')'):]
        # Replace the original clause with the new clause
        kb[idx] = '(' + '|'.join(literals) + ')'
    return kb


def unify(clause1, clause2):
    # Remove the first and last characters from each clause (presumably parentheses)
    clause1 = clause1[1:-1]
    clause2 = clause2[1:-1]

    # Split each clause into literals using '|' as the delimiter
    literals1 = clause1.split('|')
    literals2 = clause2.split('|')

    # Iterate over each literal in the first clause
    for i in range(len(literals1)):
        # Extract the predicate and parameters from the literal
        pred1 = literals1[i][:literals1[i].find('(')].strip()
        params1 = get_params(literals1[i]).split(',')

        unify_flag = False

        # Iterate over each literal in the second clause
        for j in range(len(literals2)):
            # Extract the predicate and parameters from the literal
            pred2 = literals2[j][:literals2[j].find('(')].strip()
            params2 = get_params(literals2[j]).split(',')

            # Check if the predicates are negations of each other
            if pred1.startswith('~') and not pred2.startswith('~') and pred1[1:] == pred2:
                unify_flag = True
            elif not pred1.startswith('~') and pred2.startswith('~') and pred1 == pred2[1:]:
                unify_flag = True

            # If the predicates are negations of each other, attempt to unify the parameters
            if unify_flag:
                for k in range(len(params1)):
                    # If the first parameter is a variable and the second is a constant, replace the variable with the constant
                    if is_variable(params1[k]) and is_constant(params2[k]):
                        clause1 = clause1.replace(params1[k], params2[k])
                        clause2 = clause2.replace(params1[k], params2[k])
                    # If the first parameter is a constant and the second is a variable, replace the variable with the constant
                    elif is_constant(params1[k]) and is_variable(params2[k]):
                        clause1 = clause1.replace(params2[k], params1[k])
                        clause2 = clause2.replace(params2[k], params1[k])
                    # If the first parameter is a variable and the second is a function, replace the function with the variable
                    elif is_variable(params1[k]) and is_func(params2[k]):
                        clause1 = clause1.replace(params2[k], params1[k])
                        clause2 = clause2.replace(params2[k], params1[k])
                    # If the first parameter is a function and the second is a variable, replace the variable with the function
                    elif is_func(params1[k]) and is_variable(params2[k]):
                        clause1 = clause1.replace(params1[k], params2[k])
                        clause2 = clause2.replace(params1[k], params2[k])
                    # If none of the above conditions are met, replace the first parameter with the second
                    else:
                        clause1 = clause1.replace(params1[k], params2[k])
                        clause2 = clause2.replace(params1[k], params2[k])
                unify_flag = False

    # Add parentheses back to the clauses
    clause1 = '(' + clause1 + ')'
    clause2 = '(' + clause2 + ')'

    return clause1, clause2


def resolve(clause1, clause2):
    # Unify the two clauses
    clause1, clause2 = unify(clause1, clause2)

    # Split each clause into literals using '|' as the delimiter
    literals1 = clause1[1:-1].split('|')
    literals2 = clause2[1:-1].split('|')

    can_resolve = False

    # Iterate over each literal in the first clause
    for i in range(len(literals1)):
        # Iterate over each literal in the second clause
        for j in range(len(literals2)):
            # Check if the first literal is a negation of the second literal
            if literals1[i].startswith('~') and not literals2[j].startswith('~') and literals1[i][1:].strip() == literals2[j].strip():
                # If it is, remove the literals from their respective clauses
                literals1.pop(i)
                literals2.pop(j)
                # Set the flag to indicate that resolution is possible
                can_resolve = True
                break
            # Check if the second literal is a negation of the first literal
            elif not literals1[i].startswith('~') and literals2[j].startswith('~') and literals1[i].strip() == literals2[j][1:].strip():
                # If it is, remove the literals from their respective clauses
                literals1.pop(i)
                literals2.pop(j)
                # Set the flag to indicate that resolution is possible
                can_resolve = True
                break

    # If resolution is possible, join the remaining literals together with '|' and return the result
    if can_resolve:
        return '(' + '|'.join(literals1 + literals2) + ')'
    # If resolution is not possible, return None
    return None

# demo
KB = ["(loves(x, f(y)) | ~kill(x,y))", "(kill(John,Ali))", "(bird(tweety))"]
standardize(KB)
print(KB)


clause1 = "(Dog(f(x)))"
clause2 = "(~Dog(y) | ~Owns(x, y) | AnimalLover(x))"
clause1, clause2 = standardize([clause1, clause2])
print(resolve(clause1, clause2))
