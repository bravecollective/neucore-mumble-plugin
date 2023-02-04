# Changelog

## next

- Breaking: Added new configuration variables to mumble-authenticator.ini.
- Breaking: Changed database schema: `ALTER TABLE user ADD account_active TINYINT DEFAULT 1 NULL;`
- Breaking: Groups `alliance-{id}` and `corporation-{id}` will no longer be added to Mumble.
- Fix: Accounts are now disabled if the player does not have any group required by the plugin.
- Fix: Allow SuperUser login.
- New: Show full name for admins and in the Neucore player modal window.

## 0.4.0, 2023-01-28

- Breaking: Removed NEUCORE_MUMBLE_PLUGIN_DB_USERNAME and NEUCORE_MUMBLE_PLUGIN_DB_PASSWORD environment variables.
  Add user and password to NEUCORE_MUMBLE_PLUGIN_DB_DSN.
- Support for multiple Mumble servers (one per service plugin).

## 0.3.0, 2023-01-28

- Breaking: Changed configuration data to YAML.
- Breaking: Moved NEUCORE_MUMBLE_PLUGIN_BANNED_GROUP environment variable to the configuration data.
- Breaking: Moved the hard coded additional tags (CEO, pronouns) to the configuration data. The example configuration
  in plugin.yml contains a compatible configuration.
- Breaking: Added "Nickname" configuration value.
- Breaking: Added "MainTagReplacesCorporationTicker" configuration value.
- Change: Previously the last found pronoun from the list in the configuration data was used, now it's the first.
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
- Nickname based on character name, corporation and Neucore groups (tags).
- Bans based on Neucore group.
