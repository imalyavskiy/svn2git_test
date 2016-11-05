# -*- coding: utf-8 -*-
import subprocess


class Client:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        output = subprocess.Popen("svn " + args, shell=True, stdin=pipe, stdout=pipe,
                                  stderr=subprocess.STDOUT).stdout.read()
        if 0 == len(output):
            return ""
        return output.decode('cp1251', 'replace')

    def check_access(self):
        output = self.run("--version")
        if output.startswith("svn, version"):
            return True
        return False

    def propget_recursive(self, path, prop):
        result = self.run("propget -v -R " + prop + " " + path)
        result = result.replace("\r\n", "\n")
        result = result.replace(" - ", "\n")
        result = result.replace("\n\n", "\n")
        return result


def check():
    output = Client().run("--version")
    if output.startswith("svn, version"):
        return True
    return False


def controlled(path):
    output = Client().run("info " + path)
    if output.startswith("Path:"):
        return True
    return False

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")


