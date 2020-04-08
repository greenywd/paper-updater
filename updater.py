#!/usr/bin/python3

import requests
import sys
import os
import argparse
import json
import urllib.request
from shutil import copyfile

def getVersions() -> List:
    req = urllib.request.Request('https://papermc.io/api/v1/paper/', headers={'User-Agent' : "Paper Python"})
    con = urllib.request.urlopen( req )
    text = json.loads(con.read())
    return text['versions']

def getBuildsForVersion(version: str) -> List:
    req = urllib.request.Request('https://papermc.io/api/v1/paper/%s/' % (version), headers={'User-Agent' : "Paper Python"})
    con = urllib.request.urlopen( req )
    text = json.loads(con.read())
    return text['builds']['all']

def downloadPaper(version: str = '1.15.2', build: str = 'latest'):
    link = "https://papermc.io/api/v1/paper/%s/%s/download" % (version, build)
    file_name = "paper.jar"
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()


def copyPaper(dir):
        copyfile('paper.jar', dir + '/paper.jar')

def copyPaperRecursively(root_dir):
    minecraft_server_dirs = next(os.walk(root_dir))[1]

    for dir in minecraft_server_dirs:
        full_dir = root_dir + dir
        print(full_dir)
        copyfile('paper.jar', full_dir + '/paper.jar')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='paper-updater', description='Paper Minecraft Server Helper', epilog='If no arguments are given, the latest version of Paper will automatically be downloaded.')
    parser.add_argument('-d', '--server-dir', type=str, help='Full directory of the Paper Server to be updated')
    parser.add_argument('-r', '--recursive', action='store_true', help='Update paper in every directory located inside of -d/--server-dir')
    parser.add_argument('-v', '--versions', action='store_true', help='List versions of the Paper Minecraft Server')
    parser.add_argument('-o', '--output-file', action='store_true', help='Filename that will be given to the server jar. Default is paper.jar.')
    args = parser.parse_args()

    print(args.server_dir)

    if args.versions:
        print('\n'.join(getVersions()))
        quit()
    # downloadPaper(versions[0])
    # copyPaper()
