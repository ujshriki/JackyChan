from micropython import const
import constants
DEFAULT_NO_FUNCTION_NAME = const("-function name not given-")
DEFAULT_NO_DESCRIPTION = const("-error description not given-")

class Program_Filter_Exceptions(Exception):
    def __init__(self, description=DEFAULT_NO_DESCRIPTION, function_name=DEFAULT_NO_FUNCTION_NAME):
        super().__init__(description) # initialises the exception with the custom message
        self.function_name = function_name # adds the name of the function where it was raised
    
    # overriding the __str__ function to print all added fields of the exception
    def __str__(self):
        return f"In Function: {self.function_name} -> {super().__str__()}"


