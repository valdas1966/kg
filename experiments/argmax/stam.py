import inspect
import time


def log_function_call(func):
    def wrapper(*args, **kwargs):
        # Retrieve the caller's information from the call stack
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0]).__name__
        caller_function = caller_frame.function

        module_name = func.__module__
        function_name = func.__name__
        start_time = time.time()
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        args_info = ", ".join(
            f"{name}({type(arg).__name__})={arg}" for name, arg in
            zip(arg_names, args))
        kwargs_info = ", ".join(
            f"{key}({type(value).__name__})={value}" for key, value in
            kwargs.items())

        print(
            f"Called from {caller_module}.{caller_function}. {module_name}."
            f"{function_name} starts at {start_time} with arguments: "
            f"{args_info} {kwargs_info}")
        result = func(*args, **kwargs)
        finish_time = time.time()
        print(
            f"{module_name}.{function_name} ends at {finish_time} with return "
            f"value: {type(result).__name__}={result}")
        return result

    return wrapper


def wrap_functions_with_logging():
    main_frame = inspect.currentframe().f_back.f_globals
    for name, obj in list(main_frame.items()):
        if inspect.isfunction(
                obj) and obj != wrap_functions_with_logging and obj.__name__ \
                != 'log_function_call':
            main_frame[name] = log_function_call(obj)


def inner_function(x):
    return x * 2


def example_function(a, b, c=0):
    val = inner_function(a) + inner_function(b) + c
    return val


@log_function_call
def explicitly_decorated_function(x, y):
    return x + y


def main():
    wrap_functions_with_logging()
    example_function(1, 2, c=3)
    explicitly_decorated_function(4, 5)


if __name__ == "__main__":
    main()
