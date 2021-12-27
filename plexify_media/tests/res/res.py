import os


def get_resources_location():
    return os.path.dirname(os.path.abspath(__file__))


def get_test_input_location():
    return os.path.join(get_resources_location(), 'test_input')


def get_test_output_location():
    return os.path.join(get_resources_location(), 'test_output')
