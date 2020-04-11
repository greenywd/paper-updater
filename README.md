# Paper Updater
Small Python 3 script to automatically update the [Paper](https://papermc.io/) server jar. I host a few Minecraft servers for friends and after a few weeks I found out that it's a pain keeping them up to date - especially when there can be multiple updates a day! This is still a huge WIP, but hopefully it's something that simplifies my life a bit (and maybe yours!).

## Usage
```
└ python updater.py -h                        
usage: paper-updater [-h] [--server-dir /home/minecraft/servers/] [-r] [--show-versions | --show-builds version | --show-local-versions | --show-local-builds version] [-o paper.jar] [--download version]

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
  -o paper.jar, --output-file paper.jar
                        Filename that will be given to the server jar. Default is paper.jar.
  --download version    Download the latest build of Paper of the specified version.

If no arguments are given, the latest version of Paper will automatically be downloaded but not moved.
```

## Examples
#### Update Paper for a specific server
`python updater.py --server-dir /minecraft/servers/server-1/`

This will grab the latest Paper build and place it in `/minecraft/servers/server-1/`.

#### Update Paper for all servers in a directory
`python updater.py --server-dir /minecraft/servers/ -r`

This will grab the latest Paper build and place it in each folder located in `/minecraft/servers/`, i.e. `/minecraft/servers/server-1/paper.jar`, `/minecraft/servers/server-2/paper.jar`

#### Update Paper with a specific filename
Appending `-o` or `--output-file` will rename `paper.jar` upon moving it into the server directory.

`python updater.py --server-dir /minecraft/servers/server-1/ -o "paper-server.jar"`

Result:
`/minecraft/servers/server-1/paper-server.jar`

#### Download the latest build of a specific version
`python updater.py --download 1.15.2`

#### Display all versions of the Paper server
`python updater.py --show-versions`
```
1.15.2
1.15.1
1.15
1.14.4
1.14.3
...
```

#### Display all builds of a specific version
`python updater.py --show-builds 1.15.2`
```
170                                 
169                                 
168                               
167
166
...
```

#### Display downloaded versions/builds
`python updater.py --show-local-versions`
```
1.15.2
1.14.4
```
`python updater.py --show-local-builds 1.15.2`
```
paper-170.jar
paper-168.jar
paper-165.jar
```

## To-Do
- Specify specific version of Paper to install to --server-dir
- Download specific build of version (partially implemented)
- Clean builds folder (keep latest x builds of each version)
- Keep track of what --server-dir has what version/build installed
- Use rcon to automatically restart the server after installing the new jar ([mcrcon](https://pypi.org/project/mcrcon/)?)