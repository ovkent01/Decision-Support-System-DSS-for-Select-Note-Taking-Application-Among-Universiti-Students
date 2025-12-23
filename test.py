def fib(num):
    if num in (1, 2):
        return 1
    return fib(num - 1) + fib(num - 2)