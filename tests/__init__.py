import vcr
import inspect
from functools import wraps

my_vcr = vcr.VCR()


def my_workingvcr(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        s = str(inspect.stack()[1][3]).split()[0][2:]

        path_name = f.__module__ + __name__ + f.__qualname__
        with my_vcr.use_cassette('cassettes/' + path_name + '.yml',
                                 filter_query_parameters=['_secret']):
            return f(*args, **kwds)

    return wrapper
