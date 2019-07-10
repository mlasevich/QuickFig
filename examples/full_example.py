#!/usr/bin/env python3
"""
Full Example of using QuickFig
"""
from argparse import ArgumentParser, Action, ArgumentError
from argparse import RawDescriptionHelpFormatter
import os
import sys

from quickfig import QuickFig
import yaml

__version__ = 1.0
__updated__ = ""

SCHEMA_YAML = '''
debug:
  desc: General Debug Flag
  type: bool
  default: false
  env:
    - APP_DEBUG
    - DEBUG

app.component1.enabled:
  desc: Component 1 Enabled Flag
  type: bool
  default: false

app.component1.host:
  desc: Component 1 Hostname
  type: str
  default: google.com

app.component1.port:
  desc: Component 1 Port Number
  type: int
  default: 443

app.component2.enabled:
  desc: Component 2 Enabled Flag
  type: bool
  default: no

app.component2.delay:
  desc: Delay in seconds for component 2 to startup
  type: float
  default: 0.5
'''

SCHEMA = yaml.safe_load(SCHEMA_YAML)


class StoreNameValuePair(Action):
    ''' Action to store an section.option = value pair into the  '''

    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            try:
                (key, value) = value.split("=", 2)
            except ValueError:
                raise ArgumentError(self,
                                    "Could not parse argument %s as section.option=value format" % value)
            config = getattr(namespace, self.dest) or {}
            config[key] = value
            setattr(namespace, self.dest, config)


def sep(text=""):
    ''' Print a separator '''
    print('{:^60}'.format("-" * 60))
    print('---- {:^50} ----'.format(text))
    print('{:^60}'.format("-" * 60))


def component1(config, debug):
    ''' Run component 1 '''
    print("Starting component 1")
    print("Connecting to: %s:%s" % (config.host, config.port))
    if debug:
        print("Component 1 Config:\n%s" % config)


def component2(config, debug):
    ''' Run component 2 '''
    print("Starting component 2")
    print("Delay is: %s" % config.delay)
    if debug:
        print("Component 2 Config:\n%s" % config)


def run():
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)

    parser = ArgumentParser()
    parser.add_argument("-D", dest="debug", action="store_true",
                        help="set debug mode [default: %(default)s]")

    parser.add_argument("-P", dest="options", metavar="option=value",
                        action=StoreNameValuePair, nargs="+",
                        help="Override config parameters, use option=value syntax")

    parser.add_argument('-V', '--version', action='version',
                        version=program_version_message)

    # Process arguments
    args = parser.parse_args()

    # Determine overrides based on cli args
    overrides = {}
    if args.options:
        overrides.update(args.options)
    if args.debug:
        overrides['debug'] = True

    # Create our config
    config = QuickFig(definitions=SCHEMA, overrides=overrides)

    # load the config
    config.quickfig_load_from_file("full_example.conf")
    sep("Starting...")

    print("Debug Mode is: %s" % ("on" if config.debug else "off"))

    if config.debug:
        print("Total Config: \n%s" % config)

    # run component1 if enabled
    if config.app.component1.enabled:
        sep("Component 1")
        # Run component 1 and give it only the config it needs
        component1(config.section('app.component1'), config.debug)

    # run component2 if enabled
    if config.app.component2.enabled:
        sep("Component 2")
        # Run component 1 and give it only the config it needs
        component2(config.section('app.component2'), config.debug)
    sep("Finished")


if __name__ == "__main__":
    run()
