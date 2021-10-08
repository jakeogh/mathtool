#!/usr/bin/env python3
# -*- coding: utf8 -*-

# flake8: noqa           # flake8 has no per file settings :(
# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  #      Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]

import os
import sys
import time
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
import sh

signal(SIGPIPE, SIG_DFL)
import binascii
import collections
from decimal import Decimal
from decimal import getcontext
from pathlib import Path
from typing import ByteString
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from asserttool import eprint
from asserttool import ic
from asserttool import nevd
from asserttool import validate_slice
from asserttool import verify
from enumerate_input import enumerate_input
from retry_on_exception import retry_on_exception


def sort_versions(versions,
                  verbose: bool = False,
                  ):
    if verbose:
        ic(versions)
    versions.sort(key=lambda s: list(map(int, s.split('.'))), reverse=True)
    if verbose:
        ic(versions)
    return versions


def percent_of_total(*, part, total, verbose: bool = False):
    if verbose:
        ic(part, total)
    result = (part / total) * 100
    return result


def percent_difference(a, b, verbose: bool = False):
    percent_total = percent_of_total(part=min(a, b), total=max(a, b), verbose=verbose)
    if verbose:
        ic(percent_total)

    result = 100 - abs(percent_total)
    return result


def is_digits(string):
    for char in string:
        if not char.isdigit():
            return False
    return True


def make_flatten_generator(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            for sub in make_flatten_generator(el):
                yield sub
        else:
            yield el


def flatten_list(l):
    return [item for item in make_flatten_generator(l)]


def list_of_lists_to_list_of_sets(l):
    list_of_sets = []
    for item in l:
        list_of_sets.append(set(item))
    return list_of_sets


#def tag_union(tags):
#    tag_dict = return_tag_dict(tags)
#    all_valuess = get_values_from_dict(tag_dict)
#    union_set = set(flatten_list(all_values))
#    return(union_set)
#
#
#def tag_intersection(tags):
#    tag_dict = return_tag_dict(tags)
#    all_values = get_values_from_dict(tag_dict)
#    all_values_list_of_sets = list_of_lists_to_list_of_sets(all_values)
#    intersection_set = set.intersection(*all_values_list_of_sets)
#    return intersection_set


def dollar_string_to_float(string: str):
    negative = False
    if string[0] == '(':
        string = string[1:]
        negative = True
        if string[-1] != ')':
            print("ERROR: expected:", string, "to end with )")
            quit(1)
        string = string[0:-1]
    if string[0] != '$':
        print("ERROR:, no $ in:", string)
        quit(1)
    string = float(string[1:])
    if negative:
        string = -string
    return string


def dollar_string_to_decimal(string: str):
    string = string.replace(',', '')
    getcontext().prec = 16
    negative = False
    if string[0] == '(':
        string = string[1:]
        negative = True
        if string[-1] != ')':
            print("ERROR: expected:", string, "to end with )")
            quit(1)
        string = string[0:-1]
    if string[0] != '$':
        print("ERROR:, no $ in:", string)
        quit(1)
    number = Decimal(string[1:])
    if negative:
        number = -number
    return number


def get_random_hex_bytes(count):
    assert isinstance(count, int)
    return binascii.hexlify(os.urandom(count))


def get_random_hex_digits(count):
    assert isinstance(count, int)
    bytes_needed = count
    if count % 2 != 0:
        bytes_needed = int((count + 1) / 2)
    else:
        bytes_needed = int(count / 2)
    ans = get_random_hex_bytes(bytes_needed)[0:count]
    assert len(ans) == count
    return ans.decode('UTF8')

#@click.group()
#@click.option('--verbose', is_flag=True)
#@click.option('--debug', is_flag=True)
#@click.pass_context
#def cli(ctx,
#        verbose: bool,
#        debug: bool,
#        ):
#
#    null, end, verbose, debug = nevd(ctx=ctx,
#                                     printn=False,
#                                     ipython=False,
#                                     verbose=verbose,
#                                     debug=debug,)


# update setup.py if changing function name
@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.pass_context
def cli(ctx,
        verbose: bool,
        debug: bool,
        ):

    null, end, verbose, debug = nevd(ctx=ctx,
                                     printn=False,
                                     ipython=False,
                                     verbose=verbose,
                                     debug=debug,)


