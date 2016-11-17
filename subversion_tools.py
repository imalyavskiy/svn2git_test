# -*- coding: utf-8 -*-
import subprocess


class Client:
    def __init__(self):
        pass

    def run(self, args):
        pipe = subprocess.PIPE
        cmd_str = "svn " + args
        print("[INFO] Call \"{0}\"... ".format(cmd_str), end='', flush=True)
        output = subprocess.Popen(cmd_str, shell=True, stdin=pipe, stdout=pipe,
                                  stderr=subprocess.STDOUT).stdout.read()
        print("Done.")
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


def repository_info(path):
    result = Client().run("info " + path)
    result = result.replace("\r\n", "\n")
    result = result.replace(" - ", "\n")
    result = result.replace("\n\n", "\n")
    strings = result.split(sep="\n")

    hdr_url_root = "Repository Root: "
    hdr_url_repo_rel = "Relative URL: "
    hdr_path_wrk_cpy_root = "Path: "

    url_root = ""
    url_repo_rel = ""
    path_wrk_cpy_root = ""

    for string in strings:
        if string.startswith(hdr_url_root):
            url_root = string[len(hdr_url_root):]
        if string.startswith(hdr_url_repo_rel):
            url_repo_rel = string[len(hdr_url_repo_rel):]
        if string.startswith(hdr_path_wrk_cpy_root):
            path_wrk_cpy_root = string[len(hdr_path_wrk_cpy_root):]

    return url_root, url_repo_rel, path_wrk_cpy_root

if __name__ == "__main__":
    print("[FAIL] This script cannot be run directly.")


