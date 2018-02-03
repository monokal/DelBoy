import logging

from termcolor import colored


class CoxyLog(object):
    """ Provides a custom Coxy formatted logger. """

    def __init__(self, logger_name='coxy'):
        """
        :param logger_name: String: Name of the logger object to use.
        """

        self.logger = logging.getLogger(logger_name)

    def __call__(self, message, level, prompt=True):
        """
        :param message: (str) The message to log.
        :param level: (str) Level of the log message from success info,
                      warning, exception, debug.
        :param prompt: (bool) Prepend a fancy unicode icon to the message.
        """

        default_color = 'cyan'

        # INFO
        if level == 'info':
            colour = default_color

        # WARNING
        elif level == 'warning':
            colour = 'yellow'

        # DEBUG
        elif level == 'debug':
            colour = 'magenta'

        # SUCCESS
        elif level == 'success':
            level = 'info'
            colour = 'green'

        # EXCEPTION
        elif level == 'exception':
            colour = 'red'

        # RAW
        elif level == 'raw':
            level = 'info'
            colour = default_color

        # If we don't recognise the level, format it as an exception.
        else:
            colour = 'red'

        target_method = getattr(self.logger, level)

        if prompt:
            target_method(
                "{} {}".format(
                    colored('Coxy >', default_color, attrs=['bold']),
                    colored(message, colour)
                )
            )

        else:
            target_method(
                "{}".format(colored(message, colour))
            )
