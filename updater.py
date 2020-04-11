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

        if (os.path.isfile('builds/%s/paper-%s.jar' % (version, str(latest_build)))):
            raise FileExistsError("Build '%s' already exists in /builds/%s/." % (build, version))

        # If build doesn't exist in /builds, download it.
        print("Build %s does not exist in builds/%s/, downloading now." % (latest_build, version))
        url = "https://papermc.io/api/v1/paper/%s/%s/download" % (version, build)
        r = requests.get(url, allow_redirects=True)
        filepath = 'builds/%s/' % (version)

        # Create directory(/ies) if required.
        if not os.path.exists(filepath):
            os.makedirs(filepath, exist_ok=True)

        open(filepath + re.findall("filename=(.+)", r.headers['content-disposition'])[0], 'wb').write(r.content)


    def copyLatestPaper(self, dest: str, version: str = '1.15.2', output: str = 'paper.jar'):
        if (output == None):
            output = 'paper.jar'

        # Add a trailing / if one isn't given
        if (dest[-1:] != '/'):
            dest += '/'

        # Get the latest downloaded build of Paper and copy it to '<dest>/paper.jar'
        dir_path = 'builds/%s/' % (version)
        latest_downloaded_build = sorted(os.listdir(dir_path), reverse=True)[0]
        copyfile(dir_path + latest_downloaded_build, dest + output)

    def copyLatestPaperRecursively(self, root_dir: str, version: str = '1.15.2', output: str = 'paper.jar'):
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

    # TODO: Implement this
    def cleanupBuilds(self, keep_latest: int = 3):
        pass


if __name__ == "__main__":
    # TODO: Use groups to mutually exclude multiple args

    parser = argparse.ArgumentParser(prog='paper-updater', description='Paper Minecraft Server Helper', epilog='If no arguments are given, the latest version of Paper will automatically be downloaded but not moved.')
    show_group = parser.add_mutually_exclusive_group()

    parser.add_argument('--server-dir', type=str, help='Full directory of the Paper Server to be updated', metavar='/home/minecraft/servers/')
    parser.add_argument('-r', '--recursive', action='store_true', help='Update paper in every directory located inside of -d/--server-dir')
    show_group.add_argument('--show-versions', action='store_true', help='List versions of the Paper Minecraft Server')
    show_group.add_argument('--show-builds', type=str, help='List builds of a specfic version of the Paper Minecraft Server', metavar='version')
    show_group.add_argument('--show-local-versions', action='store_true', help='List downloaded versions of the Paper Minecraft Server')
    show_group.add_argument('--show-local-builds', type=str, help='List downloaded builds of a specfic version of the Paper Minecraft Server', metavar='version')
    parser.add_argument('--output-file', type=str, help='Filename that will be given to the server jar. Default is paper.jar.', metavar='paper.jar')
    parser.add_argument('--download-only', type=str, help='Download the latest build of Paper of the specified Minecraft version.', metavar='version')
    args = parser.parse_args()

    paper = Paper()

    # ---------------- Dont use --recursive without --server-dir! ---------------- #
    if args.recursive and not args.server_dir:
        print('Unable to use --recursive without --server-dir. Please specify --server-dir when attempting to use --recursive.')
        quit()

    # ---------------- Updating Paper ---------------- #
    if args.server_dir:
        server_dir = args.server_dir

        try:
            paper.downloadPaper()
        except:
            print('Already downloaded the latest build...')

        print('Copying paper jar...')
        if args.recursive:
            paper.copyLatestPaperRecursively(server_dir)
        else:
            paper.copyLatestPaper(server_dir)

        print('Done!')
        quit()

    # ---------------- List versions of Paper ---------------- #
    if args.show_versions:
        print('\n'.join(paper.getVersions()))
        quit()

    # ---------------- List builds of a specific version of Paper ---------------- #
    if args.show_builds:
        print('\n'.join(paper.getBuildsForVersion(args.show_builds)['all']))
        quit()

    # ---------------- List downloaded versions of Paper ---------------- #
    if args.show_local_versions:
        print('\n'.join(sorted(os.listdir('builds/'), reverse=True)))
        quit()

    # ---------------- List downloaded builds of a specific version of Paper ---------------- #
    if args.show_local_builds:
        print('\n'.join(sorted(os.listdir('builds/%s/' % (args.show_local_builds)), reverse=True)))
        quit()

    # ---------------- Download latest build of Paper ---------------- #
    if args.download_only:
        try:
            paper.downloadPaper(version=args.download_only)
        except:
            print('Already downloaded the latest build.')








            
