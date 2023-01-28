# Neucore Mumble plugin

This package provides a solution for managing access to a Mumble server using Neucore groups.

Features:
- Permissions based on Neucore groups.
- Display name based on character name, corporation and Neucore groups (tags).
- Bans based on Neucore group.

## How it works

The plugin uses its own database, which is populated by the Neucore service plugin and read by the Mumble 
authenticator.

### Permissions

All groups of anyone who creates a Mumble account in Neucore are added to the Mumble server. They are then 
available as groups in the ACL configuration.

Accounts that are members of the "banned" group (configurable ID from the plugin configuration data) cannot connect 
to Mumble.

### Names

The Mumble display name is set to the name of the EVE character, optionally followed by one or more tags.

The tags are added according to the configuration of the service plugin. Only the first tag from each group is used.

The "groupsToTags" configuration is one group, the main tag, it is always added last. The optional 
"additionalTagGroups" configuration defines additional groups, they are added after the character name in the 
order they are defined there. See plugin.yml for an example.

If there is no main tag for a character, the corporation ticker is used instead.

## Requirements

- A [Neucore](https://github.com/tkhamez/neucore) installation.
- Its own MySQL/MariaDB database.
- Python 3.8
- Mumble Server

## Install the plugin

See [Neucore Plugins.md](https://github.com/tkhamez/neucore/blob/main/doc/Plugins.md) for general installation 
instructions.

- Create a new database (e.g. neucore_mumble)
- Create database tables by importing create.sql.

The plugin needs the following environment variables:
- NEUCORE_MUMBLE_PLUGIN_DB_DSN=mysql:host=127.0.0.1;dbname=neucore_mumble;user=mumble;password=pass
- NEUCORE_MUMBLE_PLUGIN_DB_USERNAME=username # Only required if DSN does not include user
- NEUCORE_MUMBLE_PLUGIN_DB_PASSWORD=password # Only required if DSN does not include password

Create a new service on Neucore for this plugin and adjust the "Configuration Data" text area.

## Install Mumble

Debian/Ubuntu:

- Optional: `sudo add-apt-repository ppa:mumble/release`
- `sudo apt install mumble-server libqt5sql5-mysql`
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

## Install the authenticator

Ubuntu 20.04 (Python 3.8):

- Setup:
  - `sudo apt install python3-venv python3-dev build-essential libmysqlclient-dev libbz2-dev`
  - `cd /opt/neucore-mumble-plugin/authenticator/`
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install wheel`
  - `pip install zeroc-ice mysqlclient`
  - `deactivate`
- Edit `authenticator/mumble-authenticator.ini` (copy from mumble-authenticator.ini.dist)
- Systemd service:
  - Copy the file `authenticator/mumble-authenticator.service` to 
    `/etc/systemd/system/mumble-authenticator.service` and adjust user and paths in it if needed.
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable mumble-authenticator`
  - `sudo systemctl start mumble-authenticator`
