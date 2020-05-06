"""
This module provides access to the command line arguments that the program was called with.
"""

import getopt

class ArgumentError(Exception):
    """
    Base exception class for other argument exception classes to be derived from.
    Expects attribute for argument which caused the error.
    """

    def __init__(self, errored_argument_name, msg):
        super().__init__()
        self.errored_argument_name = errored_argument_name
        self.msg = msg

class UnknownArgumentError(ArgumentError):
    """
    This exception should be raised when an unknown argument is included by the user.
    """

    def __init__(self, errored_argument_name):
        super().__init__(errored_argument_name, "Unknown argument: " + errored_argument_name)

class ArgumentMissingError(ArgumentError):
    """
    This exception should be raised when an argument which is expected is missing.
    """

    def __init__(self, errored_argument_name):
        super().__init__(errored_argument_name, "Missing argument: " + errored_argument_name)

class Arguments:
    """
    This class handles the processing and population of command line arguments given an argv list.
    """

    def __init__(self, argv, expected_argument_list):
        # Gets expected_argument_list (list of tuples for each expected argument),
        # and short/long options for getopt to use.
        self.expected_argument_list, self.short_options, self.long_options = self._parse_arg_names_to_dashes(expected_argument_list)
        self.argv = argv

    @staticmethod
    def _parse_arg_names_to_dashes(expected_argument_list):
        short_options = ''
        long_options = []
        comparisons = []

        for opt in expected_argument_list:
            short_name, long_name = opt[0].split('/')

            short_options += short_name + ':'
            long_options.append(long_name + '=')

            # Append "required" boolean and default value to end of comparisons
            comparisons.append(('-' + short_name, "--" + long_name, opt[1], opt[2]))

        return (comparisons, short_options, long_options)

    def usage(self):
        """
        Returns a formatted usage string giving a brief description of command line usage.
        """

        formatted = ''

        for arg in self.expected_argument_list:
            formatted += ' ' + '/'.join(arg[0:2])

        return "Usage: " + self.argv[0] + formatted

    def get_argument_values(self):
        """
        This function takes a list of options (e.g. ["i/input", "o/output"]) and extracts the values from argv into a dictionary.
        """

        # Remove program name from arg list
        user_args = self.argv[1:]

        try:
            args, _ = getopt.getopt(user_args, self.short_options, self.long_options)     # '_' for unused var
        except getopt.GetoptError as arg_error:
            # Unrecognised option found or expected argument not given
            raise UnknownArgumentError("-" + arg_error.opt)

        arguments = {}

        for nextarg, nextval in args:
            for comp in self.expected_argument_list:
                if nextarg in comp:
                    arguments[comp[0]] = nextval

        if len(arguments) != len(self.expected_argument_list):
            for expected_arg in self.expected_argument_list:
                # If argument doesn't exist and it is not expected, add default value
                if expected_arg[0] not in arguments and not expected_arg[2]:
                    arguments[expected_arg[0]] = expected_arg[3]
                # If argument doesn't exist and it is expected
                elif expected_arg[0] not in arguments and expected_arg[2]:
                    raise ArgumentMissingError(expected_arg[0])

        return arguments
