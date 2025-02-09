'''
    Task 1. Module 5
'''


def caching_fibonacci():
    '''
    Outer function for calculating Fibonacci numbers
    '''
    cache = {0: 0, 1: 1}

    def fibonacci(n):
        '''
        Calculating Fibonacci numbers with cache check
        '''
        if n not in cache:
            cache[n] = fibonacci(n - 2) + fibonacci(n - 1)
        return cache[n]

    return fibonacci


if __name__ == "__main__":

    fib = caching_fibonacci()
    {print(f'{x}:\t{fib(x)}') for x in range(41)}

# 0, 1, 1, 2, 3, 5, 8, ...
