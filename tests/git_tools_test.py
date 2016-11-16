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

    repo_main = arguments.get("main")
    repo_sub = arguments.get("sub")

    if repo_main is None or repo_sub is None:
        print("[FAIL] Invalid arguments")
        print("       Usage --main <main repo path> --sub <sub repo path>")
        exit()

    print("[INFO] {0}".format(git.status(repo_main)))
    print("[INFO] {0}".format(git.status(repo_sub)))
    print("[INFO] {0}".format(git.submodule.add(repository=repo_sub, path="externals/sub", cwd=repo_main)))

    return

main()
exit()
