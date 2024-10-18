#!/usr/bin/env python3
# -*- coding: utf8 -*-

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=C0114  #      Missing module docstring (missing-module-docstring)
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement
from __future__ import annotations

import binascii
import os
import sys
from collections.abc import Iterable
from collections.abc import Sequence
from decimal import Decimal
from decimal import getcontext

from asserttool import ic


def sort_versions(
    versions: list[str],
) -> Sequence:
    ic(versions)
    versions.sort(key=lambda s: list(map(int, s.split("."))), reverse=True)
    ic(versions)
    return versions


def percent_of_total(
    *,
    part: float,
    total: float,
) -> float:
    ic(part, total)
    result = (part / total) * 100
    return result


def percent_difference(
    a,
    b,
) -> float:
    percent_total = percent_of_total(
        part=min(a, b),
        total=max(a, b),
    )
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
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
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


# def tag_union(tags):
#    tag_dict = return_tag_dict(tags)
#    all_valuess = get_values_from_dict(tag_dict)
#    union_set = set(flatten_list(all_values))
#    return(union_set)
#
#
# def tag_intersection(tags):
#    tag_dict = return_tag_dict(tags)
#    all_values = get_values_from_dict(tag_dict)
#    all_values_list_of_sets = list_of_lists_to_list_of_sets(all_values)
#    intersection_set = set.intersection(*all_values_list_of_sets)
#    return intersection_set


def dollar_string_to_float(string: str):
    negative = False
    if string[0] == "(":
        string = string[1:]
        negative = True
        if string[-1] != ")":
            print("ERROR: expected:", string, "to end with )")
            sys.exit(1)
        string = string[0:-1]
    if string[0] != "$":
        print("ERROR:, no $ in:", string)
        sys.exit(1)
    string = float(string[1:])
    if negative:
        string = -string
    return string


def dollar_string_to_decimal(string: str):
    string = string.replace(",", "")
    getcontext().prec = 16
    negative = False
    if string[0] == "(":
        string = string[1:]
        negative = True
        if string[-1] != ")":
            print("ERROR: expected:", string, "to end with )")
            sys.exit(1)
        string = string[0:-1]
    if string[0] != "$":
        print("ERROR:, no $ in:", string)
        sys.exit(1)
    number = Decimal(string[1:])
    if negative:
        number = -number
    return number


def get_random_hex_bytes(count: int) -> bytes:
    assert isinstance(count, int)
    return binascii.hexlify(os.urandom(count))


def get_random_hex_digits(count: int) -> str:
    assert isinstance(count, int)
    bytes_needed = count
    if count % 2 != 0:
        bytes_needed = int((count + 1) / 2)
    else:
        bytes_needed = int(count / 2)
    ans = get_random_hex_bytes(bytes_needed)[0:count]
    assert len(ans) == count
    return ans.decode("UTF8")
