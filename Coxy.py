#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from flask import Flask, \
    request
from loremipsum import generate_sentence
from pymessenger.bot import Bot

from engine.core.config import CoxyConfig
from engine.core.log import CoxyLog

# Initialise a global logger.
try:
    logger = logging.getLogger('coxy')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    out.setFormatter(formatter)
    logger.addHandler(out)

except Exception as e:
    print("Failed to initialise logging with exception:\n{}".format(e))
    sys.exit(1)

app = Flask(__name__)


class CoxyStart(object):
    def __init__(self, args, config):
        self.args = args
        self.log = CoxyLog()
        self.config = config

        self.bot = Bot(self.config['messenger']['access_token'])

    def __call__(self):
        app.run(debug=True)


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:
        output = request.get_json()

        for event in output['entry']:
            messaging = event['messaging']

            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']

                    if message['message'].get('text'):
                        response_sent_text = generate_sentence

                        send_message(recipient_id, response_sent_text)

    return "Message processed."


def verify_fb_token(token_sent):
    if token_sent == self.config['messenger']['verify_token']:
        return request.args.get("hub.challenge")

    return 'Invalid verification token'


def send_message(self, recipient_id, response):
    self.bot.send_text_message(recipient_id, response)
    return "success"


class _Coxy(object):
    def __init__(self, args):
        self.args = args
        self.log = CoxyLog()
        self.config = CoxyConfig()

    def __call__(self):
        config = self.config.load(self.args.config)

        # Instantiate and call the given class.
        target_class = self.args.func(self.args, config)
        return target_class()


def main():
    """
    Handle argument routing.
    :return: None
    """

    # Configure argument parsing.
    parser = argparse.ArgumentParser(
        prog="coxy",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Top-level arguments.
    parser.add_argument(
        "-d",
        "--debug",
        required=False,
        action="store_true",
        help="output in debug verbosity"
    )

    parser.add_argument(
        "-c",
        "--config",
        required=False,
        type=str,
        nargs=1,
        metavar='CONFIG_PATH',
        help="path to the config.yaml file",
        default="{}/config.yaml".format(
            os.path.dirname(os.path.realpath(__file__)))
    )

    # Subparser arguments.
    subparsers = parser.add_subparsers()

    #
    # Start "start" subparser.
    parser_start = subparsers.add_parser(
        'start',
        help='start a Coxy server'
    )

    parser_start.set_defaults(func=CoxyStart)
    # End "start" subparser.
    #

    try:
        args = parser.parse_args()

    except Exception as e:
        print("Failed to parse arguments with exception:\n{}".format(e))
        sys.exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = _Coxy(args)

    try:
        return client()

    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()




###############

coxyd = Flask(__name__)


class CoxyDaemon(object):
    def __init__(self, args, config):
        """
        :param args: (list) Arguments from the COXY command-line.
        :param config: (dict) Config loaded from the COXY YAML file.
        """

        self.args = args
        self.config = config

        self.log = CoxyLog()

        coxyd.secret_key = os.urandom(24)

        if args.debug:
            coxyd.logger.setLevel(logging.DEBUG)

        if args.start:
            self.start(debug=args.debug)

    def __call__(self):
        pass

    def start(self, host='0.0.0.0', port=5000, debug=False):
        """
        Start the Coxy daemon.
        :return:
        """

        self.log("Starting Coxy...", 'info')

        try:
            coxyd.run(host=host, port=port, debug=debug)

        except Exception as e:
            self.log(
                "Failed to start the Coxy daemon with error:\n{}".format(e),
                'exception'
            )
            sys.exit(1)


#
# Page routing.
#

# Tools.
@coxyd.route('/tools/hunt')
def hunt():
    return render_template('tools/hunt.html')
