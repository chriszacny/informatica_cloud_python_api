import logging
import argparse
import sys
import abc
import unittest
from unittest import TextTestRunner


class CommandLineArgs(object):
    def __init__(self):
        self.parser = None
        self.parsed_arguments = None

    @abc.abstractmethod
    def get_program_description(self):
        pass

    @abc.abstractmethod
    def add_program_specific_arguments(self):
        pass

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def set_parsed_args_on_class(self):
        pass

    def has_required_command_line_arguments(self):
        return False

    def get(self):
        self.parser = argparse.ArgumentParser(description=self.get_program_description())
        self.add_program_specific_arguments()
        self.parsed_arguments = self.parser.parse_args()
        self.set_parsed_args_on_class()

        if self.has_required_command_line_arguments() and len(sys.argv) <= 1:
            self.parser.print_help()
            sys.exit()


class StandardPythonApp(object):
    def __init__(self):
        self.initialize_logger()
        self.command_line_args = self.instantiate_command_line_args()
        self.command_line_args.get()
        self.command_line_args.validate()

    def initialize_logger(self):
        logging.basicConfig(level=logging.INFO)

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def instantiate_command_line_args(self):
        pass

    def bootstrapper(self):
        self.execute()


