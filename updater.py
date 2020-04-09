#!/usr/bin/python3

import requests
import os
import argparse
import json
import re
from shutil import copyfile

class Paper:
    def getVersions(self) -> list:
        req = requests.get('https://papermc.io/api/v1/paper/', headers={'User-Agent' : 'Paper Python'})
        text = json.loads(req.content)
        return text['versions']

    def getBuildsForVersion(self, version: str) -> list:
        req = requests.get('https://papermc.io/api/v1/paper/%s/' % (version), headers={'User-Agent' : "Paper Python"})
        text = json.loads(req.content)
        return text['builds']

    def downloadPaper(self, version: str = '1.15.2', build: str = 'latest'):
        # Check to see if we've already downloaded the build before saving.
        builds = self.getBuildsForVersion(version)
        latest_build = builds['latest']

        if (os.path.isfile('builds/paper-%s.jar' % (str(latest_build)))):
            raise FileExistsError("Build '%s' already exists in /builds." % (build))

        # If build doesn't exist in /builds, download it.
        print('Build does not exist in builds/%s/, downloading now.' % (version))
        url = "https://papermc.io/api/v1/paper/%s/%s/download" % (version, build)
        r = requests.get(url, allow_redirects=True)
        filepath = 'builds/%s/' % (version)

        if not os.path.exists(filepath):
            os.makedirs(filepath, exist_ok=True)

        open(filepath + re.findall("filename=(.+)", r.headers['content-disposition'])[0], 'wb').write(r.content)


def copyLatestPaper(dest: str, version: str = '1.15.2', output: str = 'paper.jar'):
    if (output == None):
        output = 'paper.jar'

    # Get the latest downloaded build of Paper and copy it to '<dest>/paper.jar'
    dir_path = 'builds/%s/' % (version)
    latest_downloaded_build = sorted(os.listdir(dir_path), reverse=True)[0]
    copyfile(dir_path + latest_downloaded_build, dest + output)

def copyLatestPaperRecursively(root_dir: str, version: str = '1.15.2', output: str = 'paper.jar'):
    if (output == None):
        output = 'paper.jar'
        
    dir_path = 'builds/%s/' % (version)
    latest_downloaded_build = sorted(os.listdir(dir_path), reverse=True)[0]
    
    # Add a trailing / if one isn't given
    if (root_dir[-1:] != '/'):
        root_dir += '/'

    minecraft_server_dirs = next(os.walk(root_dir))[1]

    for dir in minecraft_server_dirs:
        full_dir = root_dir + dir
        copyfile(dir_path + latest_downloaded_build, '%s/%s' % (full_dir, output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='paper-updater', description='Paper Minecraft Server Helper', epilog='If no arguments are given, the latest version of Paper will automatically be downloaded.')
    parser.add_argument('-d', '--server-dir', type=str, help='Full directory of the Paper Server to be updated')
    parser.add_argument('-r', '--recursive', action='store_true', help='Update paper in every directory located inside of -d/--server-dir')
    parser.add_argument('-v', '--versions', action='store_true', help='List versions of the Paper Minecraft Server')
    parser.add_argument('-b', '--builds', type=str, help='List builds of a specfic version of the Paper Minecraft Server')
    parser.add_argument('-o', '--output-file', action='store_true', help='Filename that will be given to the server jar. Default is paper.jar.')
    args = parser.parse_args()

    paper = Paper()
    print (args.builds)
    if args.versions:
        print('\n'.join(paper.getVersions()))
        quit()

    if args.builds:
        print('\n'.join(paper.getBuildsForVersion(args.builds)['all']))
        quit()

    # ---------------- Updating Paper ---------------- #
    if args.server_dir:
        server_dir = args.server_dir

        if args.recursive:
            copyLatestPaperRecursively(server_dir)