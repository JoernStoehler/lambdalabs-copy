#!/usr/bin/env python3
import argparse
import subprocess
import os.path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address")
    parser.add_argument("--port", "-p", help="Port", default="22")
    parser.add_argument("local", help="Local folder")
    parser.add_argument("remote", help="Remote folder", nargs='?', default=None)
    parser.add_argument("--user", "-u", help="Remote user", default="ubuntu")
    parser.add_argument("--reverse", "-x", help="Sync from remote to local instead", action="store_true")
    args = parser.parse_args()

    if args.remote is None:
        args.remote = "/home/" + args.user + "/" + os.path.basename(args.local)

    # make abspaths
    # watch out: the home directory is not always /home/<local user>
    args.local = os.path.abspath(args.local)
    args.remote = os.path.abspath(args.remote.replace("~", "/home/" + args.user))

    args.remote_parent = os.path.dirname(args.remote)
    args.local_parent = os.path.dirname(args.local)

    if not args.reverse:
        # check if local folder exists
        if not os.path.exists(args.local):
            print("Error: local folder does not exist")
            exit(1)

    if args.reverse:
        # check if remote folder exists
        cmd = ["ssh", args.user + "@" + args.ip, "-p", args.port, "test -d " + args.remote]
        print(" ".join(cmd))
        if subprocess.run(cmd).returncode != 0:
            print("Error: remote folder does not exist")
            exit(1)

    if not args.reverse:
        # rsync local folder to remote
        cmd = ["rsync", "-uraz", "--delete", "-e", f"ssh -p {args.port}", args.local, args.user + "@" + args.ip + ":" + args.remote_parent + "/"]
        print(" ".join(cmd))
        subprocess.run(cmd)
    
    if not args.reverse:
        # check if vscode is installed
        if not os.path.exists("/usr/bin/code"):
            print("Error: vscode is not installed")
            exit(1)

        # start vscode
        if args.port != "22":
            print("cannot start vscode with non-standard port")
            print("please start vscode manually")
        else:
            cmd = ["code", "--remote", "ssh-remote+" + args.user + "@" + args.ip, args.remote]
            print(" ".join(cmd))
            subprocess.run(cmd)
    
    if args.reverse:
        # rsync remote folder to local
        cmd = ["rsync", "-uraz", "--delete", args.user + "@" + args.ip + ":" + args.remote, args.local_parent + "/"]
        print(" ".join(cmd))
        subprocess.run(cmd)

    