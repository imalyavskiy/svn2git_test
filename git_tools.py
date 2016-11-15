# -*- coding: utf-8 -*-
import subprocess
import os


class Client:
    def __init__(self):
        pass

    def run(self, args, **kwargs):
        pipe = subprocess.PIPE
        cmd_str = "git "+args

        cwd_str = os.getcwd()
        cwd = kwargs.get("cwd")
        if cwd is not None:
            cwd_str = cwd

        print("[INFO] Call \"{0}\"... ".format(cmd_str), end='')
        output = subprocess.Popen(cmd_str,
                                  shell=True,
                                  stdin=pipe,
                                  stdout=pipe,
                                  stderr=subprocess.STDOUT,
                                  cwd=cwd_str).stdout.read()
        print("Done.")
        if 0 == len(output):
            return ""
        return output.decode('utf8', 'ignore')

class Submodule:
    def __init__(self, _client):
        self.client = _client
        pass

    def add(self, **kwargs):
        result = ""
        string = ""
        cwd_str = ""

        quiet = kwargs.get("quiet")
        if quiet is not None:
            string += "--quiet "

        string += "add"

        branch = kwargs.get("branch")
        if branch is not None:
            pass

        force = kwargs.get("force")
        if force is not None:
            pass

        name = kwargs.get("name")
        if name is not None:
            pass

        reference = kwargs.get("reference")
        if reference is not None:
            pass

        depth = kwargs.get("depth")
        if depth is not None:
            pass

        repository = kwargs.get("repository")
        if repository is not None:
            string += " " + repository

        path = kwargs.get("path")
        if path is not None:
            string += " " + path

        cwd = kwargs.get("cwd")
        if cwd is not None:
            cwd_str = cwd

        result = self.client.run(string, cwd=cwd_str)
        return result

    def status(self):
        return str()

    def init(self):
        return str()

    def deinit(self):
        return str()

    def update(self):
        return str()

    def summary(self):
        return str()

    def foreach(self):
        return str()

    def sync(self):
        return str()


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

__git__ = Client()
submodule = Submodule(__git__)
svn = ClientSVN()


def check():
    output = __git__.run("--version")
    if output.startswith("git version"):
        return True
    return False


def clone(**kwargs):
    string = "clone"

    repository = kwargs.get("repository")
    if repository is not None:
        string += " " + repository
    else:
        return None

    path = kwargs.get("path")
    if path is not None:
        string += " " + path
    else:
        return None

    return __git__.run(string)
