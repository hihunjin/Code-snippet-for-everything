def print_wrapper(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"======== Start {func.__name__} ========")
        result = func(*args, **kwargs)
        print(f"OUTPUT\t\t{func.__name__}:\t{result}")
        return result

    return wrapper


@print_wrapper
def adder(a, b):
    return a + b


def multiplier(a, b):
    return a * b


if __name__ == "__main__":
    adder(1, 2)
    print_wrapper(multiplier)(1, 2)
