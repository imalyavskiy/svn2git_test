# -*- coding: utf-8 -*-
import subprocess


def run(args):
    pipe = subprocess.PIPE
    output = subprocess.Popen("git "+args, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
    if 0 == len(output):
        return ""
    return output.decode('utf8', 'ignore')


def check_access():
    output = run("--version")
    if output.startswith("git version"):
        return True
    return False
