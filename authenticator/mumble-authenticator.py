#!/usr/bin/env python

import configparser
import sys
import time

import Ice
import MySQLdb


# Read config
cfg = 'mumble-authenticator.ini'
config_num = 0
if len(sys.argv) > 1:
    try:
        config_num = int(sys.argv[1])
    except ValueError:
        pass
if config_num > 0:
    cfg = 'mumble-authenticator-{0}.ini'.format(config_num)
print('Reading config file: {0}'.format(cfg))
config = configparser.RawConfigParser()
config.read(cfg)
sql_host = config.get('mysql', 'sql_host')
sql_user = config.get('mysql', 'sql_user')
sql_pass = config.get('mysql', 'sql_pass')
sql_name = config.get('mysql', 'sql_name')

# Load slice
try:
    # noinspection PyArgumentList
    Ice.loadSlice('', ['-I' + Ice.getSliceDir(), config.get('ice', 'slice')])
except RuntimeError as e:
    print(format(e))
    sys.exit(0)
# noinspection PyUnresolvedReferences
import Murmur

# Test DB connection
try:
    db_test = MySQLdb.connect(sql_host, sql_user, sql_pass, sql_name)
    db_test.close()
except Exception as e:
    print("Database initialization failed: {0}".format(e))
    sys.exit(0)


# see https://www.mumble.info/documentation/slice/1.3.0/html/Murmur/ServerUpdatingAuthenticator.html
class ServerAuthenticatorI(Murmur.ServerUpdatingAuthenticator):

    # noinspection PyUnusedLocal
    @staticmethod
    def authenticate(name, pw, certificates, cert_hash, cer_strong, out_newname):
        db = None
        try:
            db = MySQLdb.connect(sql_host, sql_user, sql_pass, sql_name)

            return_fall_through = -2
            return_denied = -1

            # ---- Verify Params

            if not name or len(name) == 0:
                return return_denied, None, None

            if name == 'SuperUser':
                print('Fall through for SuperUser')
                return return_fall_through, None, None

            print("Info: Trying '{0}'".format(name))

            if not pw or len(pw) == 0:
                print("Fail: {0} did not send a password".format(name))
                return return_denied, None, None

            # ---- Retrieve User

            days_limit = config.getint('auth', 'update_days_limit')
            ts_min = int(time.time()) - (60 * 60 * 24 * days_limit)
            c = db.cursor(MySQLdb.cursors.DictCursor)
            c.execute(
                "SELECT character_id, corporation_id, alliance_id, mumble_password, `groups`, mumble_fullname "
                "FROM user WHERE mumble_username = %s AND updated_at > %s AND account_active = %s",
                (name, ts_min, 1)
            )
            row = c.fetchone()
            c.close()

            if not row:
                print("Fail: {0} not found in the database, not up to date or deactivated.".format(name))
                return return_denied, None, None

            character_id = row['character_id']
            corporation_id = row['corporation_id']
            alliance_id = row['alliance_id']
            mumble_password = row['mumble_password']
            group_string = row['groups']
            nick = row['mumble_fullname']

            groups = []
            if group_string:
                for g in group_string.split(','):
                    groups.append(g.strip())

            # ---- Verify Password

            if mumble_password != pw:
                print(
                    "Fail: {0} password does not match for {1}: '{2}' != '{3}'"
                    .format(name, character_id, mumble_password, pw)
                )
                return return_denied, None, None

            # ---- Check Bans

            c = db.cursor(MySQLdb.cursors.DictCursor)
            c.execute(
                "SELECT reason_public, reason_internal FROM ban WHERE filter = %s",
                ('alliance-' + str(alliance_id),)
            )
            row1 = c.fetchone()
            c.close()
            if row1:
                print(
                    "Fail: {0} alliance banned from server: {1} / {2}"
                    .format(name, row1['reason_public'], row1['reason_internal'])
                )
                return return_denied, None, None

            c = db.cursor(MySQLdb.cursors.DictCursor)
            c.execute(
                "SELECT reason_public, reason_internal FROM ban WHERE filter = %s",
                ('corporation-' + str(corporation_id),)
            )
            row2 = c.fetchone()
            c.close()
            if row2:
                print(
                    "Fail: {0} corporation banned from server: {1} / {2}"
                    .format(name, row2['reason_public'], row2['reason_internal'])
                )
                return return_denied, None, None

            c = db.cursor(MySQLdb.cursors.DictCursor)
            c.execute(
                "SELECT reason_public, reason_internal FROM ban WHERE filter = %s",
                ('character-' + str(character_id),)
            )
            row3 = c.fetchone()
            c.close()
            if row3:
                print(
                    "Fail: {0} character banned from server: {1} / {2}"
                    .format(name, row3['reason_public'], row3['reason_internal'])
                )
                return return_denied, None, None

            # ---- Done

            print("Success: '{0}' as '{1}' in {2}".format(character_id, nick, groups))
            return character_id, nick, groups

        except Exception as e2:
            print("Fail: {0}".format(e2))

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def getRegistration(userid, current=None):
        return -2, None, None

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def getRegisteredUsers(user_filter, current=None):
        return dict()

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def registerUser(info, current=None):
        print("Warn: Somebody tried to register user '{0}'".format(info))
        return -1

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def unregisterUser(user_id, current=None):
        print("Warn: Somebody tried to unregister user '{0}'".format(user_id))
        return -1

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def idToTexture(user_id, current=None):
        return None

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def idToName(user_id, current=None):
        return None

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def nameToId(name, current=None):
        return id

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def getInfo(user_id, current=None):
        return False, None

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def setInfo(user_id, info, current=None):
        print("Warn: Somebody tried to set info for '{0}'".format(user_id))
        return -1

    # noinspection PyPep8Naming,PyUnusedLocal
    @staticmethod
    def setTexture(userid, tex, current=None):
        print("Warn: Somebody tried to set a texture for '{0}'".format(userid))
        return -1


# Run
if __name__ == "__main__":
    print('Starting authenticator...')

    ice_host = config.get('ice', 'host')
    ice_port = config.getint('ice', 'port')
    ice = Ice.initialize(sys.argv)
    meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy('Meta -e 1.0:tcp -h %s -p %d' % (ice_host, ice_port)))
    print('established murmur meta')

    adapter = ice.createObjectAdapterWithEndpoints('Callback.Client', 'tcp -h %s' % ice_host)
    adapter.activate()

    server_ids = [int(x) for x in config.get('murmur', 'servers').split(',')]
    for server_id in server_ids:
        server = meta.getServer(server_id)
        print("Binding to server: {0}".format(server))
        serverR = Murmur.ServerUpdatingAuthenticatorPrx.uncheckedCast(adapter.addWithUUID(ServerAuthenticatorI()))
        server.setAuthenticator(serverR)

    try:
        ice.waitForShutdown()
    except KeyboardInterrupt:
        print('Aborting!')

    ice.shutdown()
    print('o7')
