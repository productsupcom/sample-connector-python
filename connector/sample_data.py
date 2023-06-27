import time
import os
import sys

from .container_api import ContainerApi, OutputFile, LogLevel, ContainerApiError

container_api = ContainerApi()


def append_sample_products():
    products = [
        {'id': 1, 'name': 'first_product', 'timestamp': time.time()},
        {'id': 2, 'name': 'second product', 'timestamp': time.time()}
    ]
    container_api.append_many_to_file(OutputFile.OUTPUT, products)

    product = {'id': 3, 'name': 'append just one', 'timestamp': time.time()}
    container_api.append_to_file(OutputFile.OUTPUT, product)


def failed_call_to_container_api():
    products = []
    try:
        container_api.append_many_to_file(OutputFile.OUTPUT, products)
    except ContainerApiError as error:
        container_api.log(LogLevel.ERROR, error.message)
        # alternatively you can also log to STDERR when there are issues with calling container api
        print(error.message, file=sys.stderr)


def log_something():
    message = 'Sample message, level {}'
    for level in LogLevel:
        container_api.log(level, message.format(level))


def read_env_var_and_exit():
    name = os.environ.get('NAME')
    if name:
        container_api.log(LogLevel.SUCCESS, 'Hello {}'.format(name))
    
    should_fail = os.environ.get('SHOULD_FAIL')
    if should_fail == '1':
        sys.exit(1)
    sys.exit(0)
