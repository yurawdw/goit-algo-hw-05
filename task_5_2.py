'''
    Task 2. Module 5
'''

import re
from typing import Callable


def generator_numbers(text: str):
    '''
    A generator that iterates over all real numbers in the text.
    '''
    pattern = r'\s([-+]?[0-9]*\.?[0-9]+)\s'
    for match in re.finditer(pattern, f' {text} '):
        yield float(match.group(1))


def sum_profit(text: str, func: Callable):
    '''
    Calculates the total sum of numbers in the input string
    '''
    return sum(func(text))


def main():

    # sample data
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
