import sys
import yaml

from .log import CoxyLog


class CoxyConfig(object):
    """ Provides methods to interact with Coxy configuration. """

    def __init__(self):
        self.log = CoxyLog()

    def load(self, path):
        """
        Returns a parsed dictionary from a YAML config file.

        :param path: (str) Path to the YAML config file.
        :return: (dict) The parsed configuration dictionary.
        """

        try:
            config_file = open(path)
            config_dict = yaml.safe_load(config_file)
            config_file.close()

        except Exception as e:
            self.log(
                "Failed to load config file ({}) with exception:\n"
                "{}.".format(path, e), 'exception'
            )
            sys.exit(1)

        self.log("Loaded Coxy config:\n{}".format(config_dict), 'debug')
        return config_dict
