import numpy


class ConfigManager:
    """
    This is used to keep configurations that need to ba changed and applied in the run time

    Adding a new config: Add the config to the _init_ and define the set method with the same name as config with set_
    prefix
    """

    def __init__(self):
        # numpy
        self.printthreshold = 1000

    def set_printthreshold(self, value):
        self.printthreshold = value
        numpy.set_printoptions(threshold=int(value))
        return "Print output threshold set to " + str(value)

    def set_config(self, config_name, value):
        try:
            set_func = getattr(self, "set_" + config_name)
            set_func(value)
            return "Config " + config_name + " is set to " + str(value)
        except AttributeError:
            return "Error: Config Not Found"

    def get_config(self, config_name):
        try:
            return config_name + ": " + str(getattr(self, config_name))
        except AttributeError:
            return "Error: Config Not Found"
