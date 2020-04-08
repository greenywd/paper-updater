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
        print('Build does not exist in /builds, downloading now.')
        url = "https://papermc.io/api/v1/paper/%s/%s/download" % (version, build)
        r = requests.get(url, allow_redirects=True)
        open('builds/' + re.findall("filename=(.+)", r.headers['content-disposition'])[0], 'wb').write(r.content)


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
    parser.add_argument('-b', '--builds', type=str, help='List builds of a specfic version of the Paper Minecraft Server')
    parser.add_argument('-o', '--output-file', action='store_true', help='Filename that will be given to the server jar. Default is paper.jar.')
    args = parser.parse_args()

    paper = Paper()

    if args.versions:
        print('\n'.join(paper.getVersions()))
        quit()

    if args.builds:
        print('\n'.join(paper.getBuildsForVersion(args.builds)['all']))
        quit()

    # ---------------- Updating Paper ----------------
    if args.server_dir:
        server_dir = args.server_dir

        build_dir = 'builds'
        if not os.path.exists(build_dir):
            os.mkdir(build_dir)

        try:
            paper.downloadPaper()
        except FileExistsError as err:
            print(err)
    # copyPaper()
