import re

import patterns


def remove_whitespaces(expression):
    return re.sub(r"\s+", '', expression)


def find_subexpression(expression):
    result = expression
    if result.find('(') != -1 and result.find(')') != -1:
        result = re.search(patterns.DEEPMOST_BRACKETS, result).group(0)
    return result


def add(subexpression):
    parts = subexpression.split('+')
    left_operand, right_operand = extract_operands(parts)

    return left_operand + right_operand


def subtract(subexpression):

    parts = subexpression.split('-')
    if len(parts) == 3:
        if parts[0] == '':
            parts[0] = '-' + parts[1]
            parts[1] = parts[2]
            del(parts[2])
        elif parts[1] == '':
            parts[1] = '-' + parts[2]
            del (parts[2])

    elif len(parts) == 4:
        parts[0] = '-' + parts[1]
        parts[1] = '-' + parts[3]
        del(parts[3])
        del(parts[2])

    left_operand, right_operand = extract_operands(parts)

    return left_operand - right_operand


def multiply(subexpression):
    parts = subexpression.split('*')
    left_operand, right_operand = extract_operands(parts)

    return left_operand * right_operand


def divide(subexpression):
    parts = subexpression.split('/')
    left_operand, right_operand = extract_operands(parts)

    if right_operand == 0:
        raise ValueError('Cannot divide by zero')
    return left_operand / right_operand


def extract_operands(parts):
    left_operand = float(parts[0])
    right_operand = float(parts[1])

    return left_operand, right_operand


def calculate_subexpression(expression):
    result = expression

    subexpression_pattern = patterns.NUM + patterns.MLDV + patterns.NUM
    subexpression = re.search(subexpression_pattern, result)

    while subexpression is not None:
        subexpression_result = None

        print(subexpression.group(0))
        if subexpression.group(0).find('*') != -1:
            subexpression_result = multiply(subexpression.group(0))
        else:
            subexpression_result = divide(subexpression.group(0))

        result = result.replace(subexpression.group(0), (str(subexpression_result)))
        subexpression = re.search(subexpression_pattern, result)

    subexpression_pattern = patterns.NUM + patterns.ADSB + patterns.NUM
    subexpression = re.search(subexpression_pattern, result)

    while subexpression is not None:
        subexpression_result = None

        if subexpression.group(0).find('+') != -1:
            subexpression_result = add(subexpression.group(0))
        else:
            subexpression_result = subtract(subexpression.group(0))

        result = result.replace(subexpression.group(0), (str(subexpression_result)))
        subexpression = re.search(subexpression_pattern, result)

    result = result.replace('(', '')
    result = result.replace(')', '')

    return result


def calculate(expression):
    result = remove_whitespaces(expression)
    subexpression = find_subexpression(expression)
    while result != subexpression:
        try:
            result = result.replace(subexpression, calculate_subexpression(subexpression))
        except ValueError:
            print('Cannot divide by zero')
        subexpression = find_subexpression(result)
    try:
        result = result.replace(subexpression, calculate_subexpression(subexpression))
    except ValueError:
        print('Cannot divide by zero')
        return None
    if result[len(result)-1] == '.':
        result = result[:len(result)-1]
    r = 0.0
    try:
        r = float(result)
    except ValueError:
        print("Cannot parse expression")
    return r


