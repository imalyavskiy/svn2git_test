# -*- coding: utf-8 -*-
import subprocess


class Client:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        cmd_str = "git "+args
        print("[INFO] Call \"{0}\"... ".format(cmd_str), end='')
        output = subprocess.Popen(cmd_str, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
        print("Done.")
        if 0 == len(output):
            return ""
        return output.decode('utf8', 'ignore')


class ClientSVN:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        cmd_str = "git svn "+args
        print("[INFO] Call \"{0}\"... ".format(cmd_str), end='')
        output = subprocess.Popen(cmd_str, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
        print("Done.")
        if 0 == len(output):
            return ""
        return output.decode('utf8', 'ignore')

    def clone(self, url, revision, location):
        result = svn.run("clone " + url + " -r " + revision + " " + location)
        return result

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")

git = Client()
svn = ClientSVN()


def check():
    output = git.run("--version")
    if output.startswith("git version"):
        return True
    return False
