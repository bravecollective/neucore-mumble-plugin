# Neucore Mumble plugin

This package provides a solution for managing access to a Mumble server using Neucore groups.

Features:
- Permissions based on Neucore groups.
- Display name based on Neucore groups.
- Bans based on Neucore group.

## How it works

The plugin uses its own database that the Neucore service plugin fills and the Mumble authenticator script 
will read.

### Permissions

All groups from anyone that creates a Mumble account in Neucore will be added to the Mumble server. They are then 
available as groups in the ACL configuration.

Accounts that are members of the "banned" group (see NEUCORE_PLUGIN_MUMBLE_BANNED_GROUP) will not be able
to connect to Mumble.

### Names

The Mumble display name is set to the EVE character name, optionally followed by one or more tags.

Tags are added according to the configuration from the service plugin. Only the first from the list is used, with
two exceptions:

- CEO: This tag is added additionally.
- Pronouns: If the assign tag matches a predefined list (He/Him, She/Her, They/Them etc.)
  it is also added additionally.

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
- NEUCORE_PLUGIN_MUMBLE_DB_DSN=mysql:dbname=neucore_mumble;host=127.0.0.1
- NEUCORE_PLUGIN_MUMBLE_DB_USERNAME=username
- NEUCORE_PLUGIN_MUMBLE_DB_PASSWORD=password
- NEUCORE_PLUGIN_MUMBLE_BANNED_GROUP=18 # Optional Neucore group ID, members of this group will not be able to connect.

Create a new service on Neucore for this plugin, add a groups-to-tags configuration to the "Configuration Data"
text area, example:
```
alliance.leadership: Leadership
alliance.fleet-commander: FC

alliance.ceo: CEO

pronoun.he: He/Him
pronoun.she: She/Her
pronoun.they: They/Them
```

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
