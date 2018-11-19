#!/usr/bin/env python
from argparse import ArgumentParser
from subprocess import Popen

app = "britecore-test"


def build(*args, **kwargs):
    cmd = "docker build -t %s:latest ." % app
    execute_cmd(cmd)


def start(*args, **kwargs):
    cmd = "docker run --name %s --rm -p 8080:8080 %s:latest" % (app, app)
    execute_cmd(cmd)


def stop(*args, **kwargs):
    cmd = "docker rm -f -v %s" % app
    execute_cmd(cmd)


def ssh(*args, **kwargs):
    cmd = "docker exec -it %s /bin/bash" % app
    execute_cmd(cmd)


def run_tests(*args, **kwargs):
    cmd = "docker exec -it %s /app/run_tests.sh" % app
    execute_cmd(cmd)


def execute_cmd(cmd):
    res = Popen(cmd, shell=True)
    output, error = res.communicate()

    if res.returncode != 0 and error is not None:
        print error


if __name__ == "__main__":
    parser = ArgumentParser(description="Docker Helper")
    subparser = parser.add_subparsers(title="Available commands", dest="command")

    sp_build_docker = subparser.add_parser("build")
    sp_start_docker = subparser.add_parser("start")
    sp_stop_docker = subparser.add_parser("stop")
    sp_ssh_docker = subparser.add_parser("ssh")
    sp_runtests_docker = subparser.add_parser("run_tests")

    args = parser.parse_args()
    params = dict(vars(args))

    try:
        locals()[args.command](**params)
    except Exception as e:
        print(e)
