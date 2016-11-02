import subprocess


def run(args):
    pipe = subprocess.PIPE
    output = subprocess.Popen("svn "+args, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT).stdout.read()
    if 0 == len(output):
        return ""
    return output.decode('utf8', 'ignore')


def check_access():
    output = run("--version")
    if output.startswith("svn, version"):
        return True
    return False


def is_controlled(path):
    output = run("info "+path)
    if output.startswith("Path:"):
        return True
    return False


def propget_recursive(path, prop):
    return run("propget -R " + prop + " " + path)