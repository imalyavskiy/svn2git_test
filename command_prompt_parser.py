# -*- coding: utf-8 -*-
import sys

# the Parser class is intended to read command line and provide settings read from keys


class Parser:
    def __init__(self):
        self.repository_url = ""
        self.repository_rev = ""
        self.working_copy_path = ""
        pass

    def read(self):
        if len(sys.argv) < 3:
            print("[FAIL] Not enough parameters.")
            return False

        self.repository_url = sys.argv[1]
        if len(self.repository_url):
            print("[ OK ] Source URL.")
        else:
            print("[FAIL] no source provided URL")

        self.working_copy_path = sys.argv[2]
        if len(self.working_copy_path):
            print("[ OK ] destination path.")
        else:
            print("[FAIL] no destination path provided")

        return True

    def __str__(self):
        return ""
