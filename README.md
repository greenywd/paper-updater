# Paper Updater
Small Python 3 script to automatically update the [Paper](https://papermc.io/) server jar.

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