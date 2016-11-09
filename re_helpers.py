# -*- coding: utf-8 -*-
import re

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

revision_old = re.compile(
    "-r\s?\d+"                  # -r[ ]XXX
)

number_decimal = re.compile(
    "\d+"                       #d[d...]
)

url_common = re.compile(
    "http(s)?://"               # "https://" or http://
    "(/?((\w|%|-|\.)+\.?)+)+"   # server[.folder[.folder[...]]]/[...]
)

url_subversion = re.compile(
    "((http(s)?://)|(\^/))"     # "https://" or http:// or "^/"
    "(/?((\w|%|-|\.)+\.?)+)+"   # server[.folder[.folder[...]]]/[...]
)

revision_new = re.compile(
    "@\d+"                      # @XXX
)

path_relative = re.compile(
    "(/?((\w|-)+\.?)+)+"        # folder/folder
)

leading_space = re.compile(
    "^\s+"                      #a space(s) in the beginning of the string
)

path_absolute = \
    re.compile(
        "([A-Za-z]:)?(((\\\\)|(/))[\w.]*)*((\\\\)|(/))?"  # "[d:]<\|/><dir name><\|/><dir name>[\|/]"
    )

subversion_external_property_item = re.compile(
        "(^\s*)?"
        "(-r\s\d+\s)?"  # -r 122
        "((http(s)?://)|(\^/))"  # "https://" or "^/"
        "(/?((\w|%|-)+\.?)+)+"  # server.com/folder.f/folder
        "(@\d+)?"  # @122
        "\s"  # space
        "(/?((\w|-)+\.?)+)+"  # folder/folder
    )

subversion_folder_property_report_header = re.compile(
        "Properties on \'"
        "((http(s)?://)|(\^/))"  # "https://" or "^/"
        "(/?((\w|%|-)+\.?)+)+"  # server.com/folder.f/folder
        "\':"
    )

subversion_property_name = re.compile(
        "^\s*svn:\w*"
    )
