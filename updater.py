#!/usr/bin/env python

import requests
import os
import argparse
import json
import re
import sys
from mcrcon import MCRcon
from shutil import copyfile

class PaperError(Exception):
    pass

class PaperVersionNotFound(PaperError):
    def __init__(self, message):
        self.message = message

class Paper:
    def getVersions(self) -> list:
        req = requests.get('https://papermc.io/api/v1/paper/', headers={'User-Agent' : 'Paper Python'})
        text = json.loads(req.content)
        return text['versions']

    def getBuildsForVersion(self, version: str) -> list:
        req = requests.get('https://papermc.io/api/v1/paper/%s/' % (version), headers={'User-Agent' : "Paper Python"})
        text = json.loads(req.content)
        if (req.status_code == 200):
            return text['builds']
        return None

    def downloadPaper(self, version: str = '1.15.2', build: str = 'latest'):
        # Check to see if we've already downloaded the build before saving.
        builds = self.getBuildsForVersion(version)
        if (builds is None):
            raise PaperVersionNotFound('No builds for version %s found.' % (version))

        build_to_download = builds['latest']

        # TODO: If `build` is later than latest, FileExistsError is raised as it's defaulting back to 'latest'. Need to make clear that is what's happening.
        if (build != 'latest'):
            all_builds = builds['all']

            if (build in all_builds):
                build_to_download = build

        if (os.path.isfile('builds/%s/paper-%s.jar' % (version, str(build_to_download)))):
            raise FileExistsError("Build '%s' already exists in /builds/%s/." % (build, version))

        # If build doesn't exist in /builds, download it.
        print("Build %s does not exist in builds/%s/, downloading now." % (build_to_download, version))
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

    def cleanupBuilds(self, keep_latest: int = 3):
        # Get all versions in a list i.e. ['1.15', '1.15.1', '1.15.2']
        versions = next(os.walk('builds/'))[1]

        # Prefix 'builds/' to each version
        for i, version in enumerate(versions):
            versions[i] = 'builds/' + versions[i]

        for version in versions:
            builds = os.listdir(version)
            builds.sort()
            builds_to_delete = builds[:-keep_latest]

            for build in builds_to_delete:
                print(version + '/' + build)

    
    def restartServer(self, server_ip: str, rconport: int, rconpassword: str):
        ip_re = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",server_ip)

        if not ip_re:
            raise ValueError('server_ip should be formatted as an IP address (i.e. 192.168.1.1).')

        with MCRcon(server_ip, rconpassword, rconport) as mcr:
            resp = mcr.command("restart")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='paper-updater', description='Paper Minecraft Server Helper', epilog='If no arguments are given, paper-updater will not do anything.')
    show_group = parser.add_mutually_exclusive_group()
    restart_recursive_group = parser.add_mutually_exclusive_group()

    parser.add_argument('--server-dir', type=str, help='Full directory of the Paper Server to be updated', metavar='/home/minecraft/servers/')
    restart_recursive_group.add_argument('-r', '--recursive', action='store_true', help='Update paper in every directory located inside of -d/--server-dir')
    restart_recursive_group.add_argument('--restart', nargs=3, type=str, help='Restart the server after updating by calling /restart. Only works if you have restart-script specified in spigot.yml otherwise server will fail to restart, and rcon configured.', metavar=("'192.168.1.1'", "'25575'", "'password'"))
    show_group.add_argument('--show-versions', action='store_true', help='List versions of the Paper Minecraft Server')
    show_group.add_argument('--show-builds', type=str, help='List builds of a specfic version of the Paper Minecraft Server', metavar='version')
    show_group.add_argument('--show-local-versions', action='store_true', help='List downloaded versions of the Paper Minecraft Server')
    show_group.add_argument('--show-local-builds', type=str, help='List downloaded builds of a specfic version of the Paper Minecraft Server', metavar='version')
    parser.add_argument('-o', '--output-file', type=str, help='Filename that will be given to the server jar. Default is paper.jar.', metavar='paper.jar')
    parser.add_argument('--download', type=str, nargs=argparse.ONE_OR_MORE, help='Download the latest build of Paper of the specified version.', metavar='version')
    args = parser.parse_args()

    paper = Paper()

    # ---------------- Dont use --recursive without --server-dir! ---------------- #
    if args.recursive and not args.server_dir:
        print('Unable to use --recursive without --server-dir. Please specify --server-dir when attempting to use --recursive.')
        sys.exit(1)

    # ---------------- Dont use --restart without --server-dir! ---------------- #
    if args.restart and not args.server_dir:
        print('Unable to use --restart without --server-dir. Please specify --server-dir when attempting to use --restart.')
        sys.exit(1)

    # ---------------- Updating Paper ---------------- #
    if args.server_dir:
        server_dir = args.server_dir
        filename = 'paper.jar'

        if args.output_file:
            filename = args.output_file

        try:
            paper.downloadPaper()
        except:
            print('Already downloaded the latest build...')

        print('Copying paper jar...')
        if args.recursive:
            paper.copyLatestPaperRecursively(server_dir, output=filename)
        else:
            paper.copyLatestPaper(server_dir, output=filename)

            if args.restart:
                print('Restarting server on %s with rcon port %s' % (args.restart[0], args.restart[1]))
                paper.restartServer(args.restart[0], int(args.restart[1]), args.restart[2])

        print('Done!')
        sys.exit()

    # ---------------- List versions of Paper ---------------- #
    if args.show_versions:
        print('\n'.join(paper.getVersions()))
        sys.exit()

    # ---------------- List builds of a specific version of Paper ---------------- #
    if args.show_builds:
        builds = paper.getBuildsForVersion(args.show_builds)
        if (builds is not None):
            print('\n'.join(builds['all']))
        else:
            print('No builds found for version %s.' % (args.show_builds))
        sys.exit()

    # ---------------- List downloaded versions of Paper ---------------- #
    if args.show_local_versions:
        print('\n'.join(sorted(os.listdir('builds/'), reverse=True)))
        sys.exit()

    # ---------------- List downloaded builds of a specific version of Paper ---------------- #
    if args.show_local_builds:
        dir = 'builds/%s/' % (args.show_local_builds)
        if (os.path.isdir(dir)):
            print('\n'.join(sorted(os.listdir(dir), reverse=True)))
        else:
            print('No builds for version %s found.' % (args.show_local_builds))
        sys.exit()

    # ---------------- Download latest build of Paper ---------------- #
    if len(args.download) < 3:
        # If only version provided, download latest build. Otherwise, download the specified build of version.
        if (len(args.download) == 1):
            try:
                paper.downloadPaper(version=args.download[0])
            except PaperVersionNotFound as e:
                print(e)
            except FileExistsError as e:
                print('Already downloaded the latest build.')
        elif (len(args.download) == 2):
            try:
                paper.downloadPaper(version=args.download[0], build=args.download[1])
            except PaperVersionNotFound as e:
                print(e)
            except FileExistsError as e:
                print('Already downloaded the specified build.')

        sys.exit()

    else:
        print('Too many arguments provided.')
        sys.exit(1)

    paper.cleanupBuilds(keep_latest=1)