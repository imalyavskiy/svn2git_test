import sys
import os.path
import subversion_tools as svn


def is_path(path):
# use regexp https://docs.python.org/3/howto/regex.html
# to determine does this string is a path
    pass


def process_directory(path):
    path += "/"

    if not svn.is_controlled(path):
        return

    externals = svn.propget_recursive(path=path, prop="svn:externals")
    externals = externals.replace(" - ", "\r\n")
    strings = externals.split(sep="\r\n")
    strings_new = []
    for string in strings:
        if 0 == len(string):
            continue

        strings_new.append(string)

    strings = strings_new
    del strings_new

    for string in strings:
        if is_path(string):
            pass
        else:
            pass
    return


def main():
    if not svn.check_access():
        print("Subversion client does not installed.")
        exit()
    else:
        print("Subversion  [ OK ].")

    if len(sys.argv) < 2:
        print("Not enough parameters.")
        exit()

    print("Directory to process: {0}".format(sys.argv[1]))

    if not svn.is_controlled(sys.argv[1]):
        print("This folder is not an SVN working copy.")
        exit()

    print("This is a valid working copy. Starting with contents...")

    process_directory(sys.argv[1])

    print("Done.")
    return

main()
exit()
