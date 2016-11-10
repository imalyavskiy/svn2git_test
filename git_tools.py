# -*- coding: utf-8 -*-
import subprocess


class Client:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        output = subprocess.Popen("git "+args, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
        if 0 == len(output):
            return ""
        return output.decode('utf8', 'ignore')


class ClientSVN:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        output = subprocess.Popen("git svn "+args, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
        if 0 == len(output):
            return ""
        return output.decode('utf8', 'ignore')

    def clone(self, url, revision, location):
        # implement here
        pass

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

git = Client()
svn = ClientSVN()


def check():
    output = git.run("--version")
    if output.startswith("git version"):
        return True
    return False
