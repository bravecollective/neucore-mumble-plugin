# Neucore Mumble plugin

_Needs [Neucore](https://github.com/tkhamez/neucore) version 1.45.0 or higher._

This package provides a solution for accessing a Mumble server using Neucore groups for permissions.

Features:
- Permissions based on Neucore groups.
- Configurable nickname based on character data and Neucore groups (tags).
- Avatars
- Bans based on Neucore groups, corporation or alliance.
- Support for multiple Mumble servers.

## How it works

The plugin uses its own database, which is populated by the Neucore service plugin and read by the Mumble 
authenticator.

### Permissions

All Neucore groups of anyone who connects to Mumble are added to the server. They are then available as groups 
in the ACL configuration.

Accounts that are members of the "banned" group (configurable ID from the plugin configuration data) cannot connect 
to Mumble.

It is also possible to ban entire corporations or alliances. To do this, manually add an entry to the ban table, e.g.:  
`INSERT INTO ban (filter, reason_public, reason_internal) VALUES ('alliance-99001861', '', '');`  
`INSERT INTO ban (filter, reason_public, reason_internal) VALUES ('corporation-605398057', '', '');`

### Names

The Mumble display name is set to the string from the "Nickname" configuration. There are the following placeholders: 
{allianceTicker}, {corporationTicker}, {characterName} (required) and {tags}. Characters that come directly before 
or after a placeholder are removed if there is no value for the placeholder. If there are characters that come 
directly before or after the {tags} placeholder, they are used around every tag.

The tags are added according to the "GroupsToTags" configuration of the service plugin. Only the first tag from 
each group is used. Every tag not included in the optional "AdditionalTagGroups" configuration is part of the main 
tag group, they are added as the last tag. The optional "AdditionalTagGroups" configuration defines 
additional groups, they are added in the order they are defined there before the main tag. See plugin.yml for 
an example.

The main tag can optionally be used instead of the corporation ticker at its position, configured by the 
"MainTagReplacesCorporationTicker" configuration value.

## Requirements

- A [Neucore](https://github.com/tkhamez/neucore) installation.
- Its own MySQL/MariaDB database.
- Python 3.8
- Mumble Server

## Install the plugin

See [Neucore Plugins.md](https://github.com/tkhamez/neucore/blob/main/doc/Plugins.md#install-a-plugin) for 
general installation instructions.

- Create a new database (e.g. neucore_mumble)
- Create the database tables by importing create.sql.

The plugin needs the following environment variable:
- `NEUCORE_MUMBLE_PLUGIN_DB_DSN=mysql:host=127.0.0.1;dbname=neucore_mumble;user=mumble;password=pass`  
  The name of the environment variable can be changed with "DatabaseEnvVar" from the configuration
  data of the plugin. This makes it possible to add several Mumble services for different Mumble servers.

Optional environment variables:
- `NEUCORE_MUMBLE_PLUGIN_DB_SSL_CA="/path/to/ca-cert.pem"`  
  Setting this will enable encryption for the database connection, even if it is set to an empty value.
- `NEUCORE_MUMBLE_PLUGIN_DB_SSL_VERIFY=1`

Create a new service on Neucore for this plugin and adjust the "Configuration Data" text area and other
configuration values that you want to change.

## Install Mumble

Debian/Ubuntu:

- Optional: `sudo add-apt-repository ppa:mumble/release`
- `sudo apt install mumble-server libqt5sql5-mysql`
- `sudo dpkg-reconfigure mumble-server` to set the SuperUser password.
- Edit `/etc/mumble-server.ini`
  ```
  database=mumble
  
  dbDriver=QMYSQL
  dbUsername=mumble_user
  dbPassword=password
  dbHost=127.0.0.1
  
  ice="tcp -h 127.0.0.1 -p 6502"
  
  serverpassword=a-password
  
  ... other settings that you wish to change
  ```

To reload the server certificate, e.g. after certbot renewed it (using its `--post-hook` argument from the 
cronjob), execute:
```
sudo /usr/bin/killall -SIGUSR1 murmurd
```

There's a simple script included to manage virtual servers:
[authenticator/manage-server.py](authenticator/manage-server.py).

To run a second Mumble instance the following systemd unit file can be used, for example:
```
[Unit]
Description = Mumble 2
After = network.target
After = mysql.service

[Service]
Type = simple
User = root
ExecStart = /usr/sbin/murmurd -ini "/etc/mumble-server2.ini" -fg
Restart = always
RestartSec = 5s

[Install]
WantedBy = multi-user.target
```

## Install the authenticator

Example for Ubuntu 20.04 (Python 3.8):

- Setup:
  - `sudo apt install python3-venv python3-dev build-essential libmysqlclient-dev libbz2-dev`
  - `cd /opt/neucore-mumble-plugin/authenticator/`
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install wheel`
  - `pip install zeroc-ice mysqlclient`
  - `deactivate`
- Create and edit `authenticator/mumble-authenticator-1.ini` (copy from mumble-authenticator.ini.dist). The number
  in the  filename corresponds to the number from the systemd service parameter below (@1).
- Systemd service:
  - Copy the file `authenticator/mumble-authenticator@.service` to 
    `/etc/systemd/system/mumble-authenticator@.service` and adjust user and paths in it if needed.
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable mumble-authenticator@1`
  - `sudo systemctl start mumble-authenticator@1`
