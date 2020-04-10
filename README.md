# Paper Updater
Small Python 3 script to automatically update the [Paper](https://papermc.io/) server jar. I host a few Minecraft servers for friends and after a few weeks I found out that it's a pain keeping them up to date - especially when there can be multiple updates a day! This is still a huge WIP, but hopefully it's something that simplifies my life a bit (and maybe yours!).

## Usage
```
usage: paper-updater [-h] [--server-dir /home/minecraft/servers/] [-r] [--show-versions] [--show-builds version] [--show-local-versions] [--show-local-builds version] [--output-file paper.jar] [--download-only version]

Paper Minecraft Server Helper

optional arguments:
  -h, --help            show this help message and exit
  --server-dir /home/minecraft/servers/
                        Full directory of the Paper Server to be updated
  -r, --recursive       Update paper in every directory located inside of -d/--server-dir
  --show-versions       List versions of the Paper Minecraft Server
  --show-builds version
                        List builds of a specfic version of the Paper Minecraft Server
  --show-local-versions
                        List downloaded versions of the Paper Minecraft Server
  --show-local-builds version
                        List downloaded builds of a specfic version of the Paper Minecraft Server
  --output-file paper.jar
                        Filename that will be given to the server jar. Default is paper.jar.
  --download-only version
                        Download the latest build of Paper of the specified Minecraft version.

If no arguments are given, the latest version of Paper will automatically be downloaded but not moved.
```

## To-Do
- Specify specific version of Paper to install to --server-dir
- Clean builds folder (keep latest x builds of each version)
- Keep track of what --server-dir has what version/build installed
- Use rcon to automatically restart the server after installing the new jar ([mcrcon](https://pypi.org/project/mcrcon/)?)