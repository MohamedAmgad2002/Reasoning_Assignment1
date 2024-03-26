from Parse import eliminate_implication

word = '(P(x) & L(y)) | (~Q(x) & M(y))'

def distribute(word: str):
    # Base case: if the expression does not contain an OR, return the expression as it is
    if '|' not in word:
        return word

    # Split the expression into two parts at the OR
    left, right = word.split('|', 1)

    # If either part is an AND expression, distribute the OR over the AND
    if '&' in left and '&' in right:
        left_subparts = left.split('&')
        right_subparts = right.split('&')
        return ' & '.join(f'({distribute(f"{left_subpart.strip()}|{right_subpart.strip()}")})' for left_subpart in left_subparts for right_subpart in right_subparts)
    elif '&' in left:
        subparts = left.split('&')
        return ' & '.join(f'({distribute(f"{subpart.strip()}|{right.strip()}")})' for subpart in subparts)
    elif '&' in right:
        subparts = right.split('&')
        return ' & '.join(f'({distribute(f"{left.strip()}|{subpart.strip()}")})' for subpart in subparts)

    # If neither part is an AND expression, return the expression as it is
    return word


print(distribute(word))