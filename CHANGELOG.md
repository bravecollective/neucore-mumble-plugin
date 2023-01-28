# Changelog

## next

- Breaking: Changed configuration data to YAML.
- Breaking: Moved NEUCORE_MUMBLE_PLUGIN_BANNED_GROUP environment variable to configuration data.
- NEUCORE_MUMBLE_PLUGIN_DB_USERNAME and NEUCORE_MUMBLE_PLUGIN_DB_PASSWORD are now optional: user and password
  can be added to NEUCORE_MUMBLE_PLUGIN_DB_DSN.
- Removed unused config values from mumble-authenticator.ini.

## 0.2.0, 2023-01-22

- Breaking: Changed names of the environment variables.
- Fix: Mumble accounts from characters that no longer exist on Neucore are now removed.
- Added support for encrypted database connection.

## 0.1.0, 2023-01-15

First release, simply a copy/merge of [neucore-plugin-mumble](https://github.com/bravecollective/neucore-plugin-mumble)
and [mumble-sso](https://github.com/bravecollective/mumble-sso) with minimal adjustments.

- Permissions based on Neucore groups.
- Display name based on Neucore groups.
- Bans based on Neucore group.
