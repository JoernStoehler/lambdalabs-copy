#!/usr/bin/env python3
import argparse
import subprocess
import os.path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address")
    parser.add_argument("folder", help="Project folder")
    parser.add_argument("remote", help="Remote folder", nargs='?', default=None)
    parser.add_argument("--user", help="Remote user", default="ubuntu")
    args = parser.parse_args()

    if args.remote is None:
        args.remote = "~/" + os.path.basename(args.folder)

    # check if vscode is installed
    if not os.path.exists("/usr/bin/code"):
        print("Error: vscode is not installed")
        exit(1)

    # check if local folder exists
    if not os.path.exists(args.folder):
        print("Error: local folder does not exist")
        exit(1)

    # rsync local folder to remote
    subprocess.run(["rsync", "-urazvh", "--delete", args.folder, args.user + "@" + args.ip + ":" + args.remote])

    # start vscode
    subprocess.run(["code", "--remote", "ssh-remote+" + args.user + "@" + args.ip, args.remote])