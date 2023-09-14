import datetime


def time_execution(func):
    """
    calc time of execution func in milliseconds
    :param func:
    :return:
    """
    def wrapper_func(*args, **kwargs):
        t_start = datetime.datetime.now()
        result = func(*args, **kwargs)
        t_finish = datetime.datetime.now()
        t_delta = t_finish - t_start
        print(f"{func.__name__}:", t_delta.microseconds / 1000, 'ms')
        return result
    return wrapper_func
