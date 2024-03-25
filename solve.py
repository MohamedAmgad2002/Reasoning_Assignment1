import re

FUNC_EXPR = r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)"

def get_params(param_str):
    open_index = param_str.find('(')
    close_index = param_str.rfind(')')
    return param_str[open_index+1:close_index], open_index, close_index

def is_variable(param):
    return param.islower() and len(param.strip()) == 1

def standardize(kb):
    for idx, clause in enumerate(kb):
        clause = clause[1:-1]
        literals = clause.split('|')
        for i in range(len(literals)):
            # Extract parameters and their positions in the literal
            params, open_index, close_index = get_params(literals[i])
            params = params.split(',')
            for j in range(len(params)):
                # If the parameter is a variable, append the clause index to it
                if is_variable(params[j]):
                    params[j] = params[j] + str(idx)
                # If the parameter is a function expression
                elif bool(re.search(FUNC_EXPR, params[j])):
                    # Extract parameters of the function expression
                    func_params, _, _ = get_params(params[j])
                    func_params = func_params.split(',')
                    for k in range(len(func_params)):
                        # If the function parameter is a variable, append the clause index to it
                        if is_variable(func_params[k]):
                            func_params[k] = func_params[k] + str(idx)
                    # Replace the function parameters with the new function parameters
                    params[j] = params[j][0] + '(' + ','.join(func_params) + ')'
            # Replace the literal parameters with the new parameters
            literals[i] = literals[i][:open_index+1] + ','.join(params) + literals[i][close_index:]
        # Replace the original clause with the new clause
        kb[idx] = '(' + '|'.join(literals) + ')'


# demo
KB = ["(loves(x, f(y)) | ~kill(x,y))", "(hates(y,z))", "(bird(tweety))"]
standardize(KB)
print(KB)