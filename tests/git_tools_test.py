import sys
import git_tools as git


def read_cmd():
    result = {}
    argc = 1
    key = ""
    while argc < len(sys.argv):
        if sys.argv[argc].startswith("--"):
            if len(key):
                result[key] = "True"
            key = sys.argv[argc].replace("--", "")
        else:
            if len(key):
                result[key] = sys.argv[argc]
                key = ""
            else:
                print("[WARN] Argument \"{0}\" passed without a key".format(sys.argv[argc]))
        argc += 1

    return result


def main():
    arguments = read_cmd()
    main_repo = arguments.get("main")
    if main_repo is not None:
        git.status(arguments["main"])
        pass

    return

main()
exit()