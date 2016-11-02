import os
import sys
import subprocess


def run_subversion(args):
    pipe = subprocess.PIPE
    output = subprocess.Popen("svn "+args, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
    if 0 == len(output):
        return ""
    return output.decode('utf8', 'ignore')


def check_svn():
    output = run_subversion("--version")
    if output.startswith("svn, version"):
        return True
    return False


def check_svn_control(path):
    output = run_subversion("info "+path)
    if output.startswith("Path:"):
        return True
    return False


def print_properties(path):
    output = run_subversion("propget svn:externals " + path)
    if output.startswith("svn: warning: W200017:"):
        return
    print(path)
    print("\t{0}".format(output))
    return


def process_directory(path):
    path += "/"

    if not check_svn_control(path):
        return

    print_properties(path)

    for entry in os.scandir(path):
        if not entry.name.startswith('.') and not entry.is_file():
            process_directory(path + entry.name)

    return


def main():
    if not check_svn():
        print("Subversion client does not installed.")
        exit()
    else:
        print("Subversion  [ OK ].")

    if len(sys.argv) < 2:
        print("Not enough parameters.")
        exit()

    print("Directory to process: {0}".format(sys.argv[1]))

    if not check_svn_control(sys.argv[1]):
        print("This folder is not an SVN working copy.")
        exit()

    print("This is a valid working copy. Starting with contents...")

    process_directory(sys.argv[1])

    print("Done.")
    return

main()
exit()
