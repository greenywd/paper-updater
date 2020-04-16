# Paper Updater
Small Python 3 script to automatically update the [Paper](https://papermc.io/) server jar. I host a few Minecraft servers for friends and after a few weeks I found out that it's a pain keeping them up to date - especially when there can be multiple updates a day! This is still a huge WIP, but hopefully it's something that simplifies my life a bit (and maybe yours!).

## Usage
```
└ ./updater.py -h
usage: paper-updater [-h] [--server-dir /home/minecraft/servers/] [-r | --restart '192.168.1.1' '25575' 'password'  --show-versions | --show-builds version | --show-local-versions | --show-local-builds version] [-o paper.jar] [--download version [version ...]]

Paper Minecraft Server Helper

optional arguments:
  -h, --help            show this help message and exit
  --server-dir /home/minecraft/servers/
                        Full directory of the Paper Server to be updated
  -r, --recursive       Update paper in every directory located inside of -d/--server-dir
  --restart '192.168.1.1' '25575' 'password'
                        Restart the server after updating by calling /restart. Only works if you have restart-script specified in spigot.yml otherwise server will fail to restart, and rcon configured.
  --show-versions       List versions of the Paper Minecraft Server
  --show-builds version
                        List builds of a specfic version of the Paper Minecraft Server
  --show-local-versions
                        List downloaded versions of the Paper Minecraft Server
  --show-local-builds version
                        List downloaded builds of a specfic version of the Paper Minecraft Server
  -o paper.jar, --output-file paper.jar
                        Filename that will be given to the server jar. Default is paper.jar.
  --download version [version ...]
                        Download the latest build of Paper of the specified version.

If no arguments are given, paper-updater will not do anything.
```

## Examples
#### Update Paper for a specific server
`./updater.py --server-dir /minecraft/servers/server-1/`

This will grab the latest Paper build and place it in `/minecraft/servers/server-1/`.

#### Update Paper for all servers in a directory
`./updater.py --server-dir /minecraft/servers/ -r`

This will grab the latest Paper build and place it in each folder located in `/minecraft/servers/`, i.e. `/minecraft/servers/server-1/paper.jar`, `/minecraft/servers/server-2/paper.jar`

#### Update Paper with a specific filename
Appending `-o` or `--output-file` will rename `paper.jar` upon moving it into the server directory.

`./updater.py --server-dir /minecraft/servers/server-1/ -o "paper-server.jar"`

Result:
`/minecraft/servers/server-1/paper-server.jar`

#### Restart Paper after updating
The server can be restarted after updating by making use of [rcon](https://wiki.vg/RCON) and [Spigot's restart command](https://www.spigotmc.org/wiki/spigot-configuration/).

`--restart` takes three arguments, `<server_ip>`, `<rcon_port>` and `<password>`.

`./updater.py --server-dir /minecraft/servers/server-1/ --restart '192.168.1.1' '25575' 'password'`

Note: `/restart` isn't recommended by one of the Paper developers [here](https://github.com/PaperMC/Paper/issues/1559#issuecomment-428917299). I assume it's still the case now, but it's the only way I could semi-reliably implement restarting. Due to this, `--restart` isn't compatible with `--recursive` to avoid servers not starting up, left in limbo, or worse.


#### Download the latest build of a specific version
`./updater.py --download 1.15.2`

#### Download a specific build of a specific version
`./updater.py --download 1.15.2 184`

Note: Attempting to download a build later than latest will download the latest build instead. 

#### Display all versions of the Paper server
`./updater.py --show-versions`
```
1.15.2
1.15.1
1.15
1.14.4
1.14.3
...
```

#### Display all builds of a specific version
`./updater.py --show-builds 1.15.2`
```
170                                 
169                                 
168                               
167
166
...
```

#### Display downloaded versions/builds
`./updater.py --show-local-versions`
```
1.15.2
1.14.4
```
`./updater.py --show-local-builds 1.15.2`
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