#!/usr/bin/env python

"""
Simple script to manage virtual servers.

This needs the same setup as mumble-authenticator.py.
"""


import os
import sys
import Ice


# load slice
ice_slice = os.getcwd() + '/Murmur.ice'
if len(sys.argv) > 3:
    ice_slice = sys.argv[3]
try:
    # noinspection PyArgumentList
    Ice.loadSlice('', ['-I' + Ice.getSliceDir(), ice_slice])
except RuntimeError as e:
    print(format(e))
    sys.exit(0)
# noinspection PyUnresolvedReferences
import Murmur


class ManageServer:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.ice = None
        self.meta: Murmur.Meta = None

    def connect(self) -> bool:
        self.ice = Ice.initialize(sys.argv)
        try:
            proxy = self.ice.stringToProxy('Meta -e 1.0:tcp -h %s -p %s' % (self.host, self.port))
        except Exception as ex:
            write(str(ex))
            return False
        self.meta = Murmur.MetaPrx.checkedCast(proxy)
        write("Connected to {0}:{1}".format(ice_host, ice_port))
        return True

    def destroy(self):
        self.ice.destroy()

    def list(self):
        for server in self.meta.getAllServers():
            write('id: {0}, running: {1}, port: {2}, registerName: {3}'.format(
                server.id(),
                server.isRunning(),
                server.getConf('port') if server.getConf('port') else 'n/a',
                server.getConf('registerName') if server.getConf('registerName') else 'n/a',
            ))

    def conf_show(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        items = server.getAllConf().items()
        if len(items) == 0:
            write('(none)')
        else:
            for key, value in server.getAllConf().items():
                write('{0}: {1}'.format(key, value))

    def new(self):
        new_server = self.meta.newServer()
        write('New id: {}'.format(new_server.id()))

    def pw(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        password = input('Password: ')
        server.setSuperuserPassword(password)
        write('Done')

    def conf_set(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        key = input('Key (port, registerName, welcometext, ...): ')
        value = input('Value: ')
        server.setConf(key, value)
        write('Done')

    def start(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        server.start()
        write('Done')

    def stop(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        server.stop()
        write('Done')

    def delete(self):
        server_id = input('Server id: ')
        server = self.meta.getServer(int(server_id))
        if server is None:
            write('Invalid id')
            return

        sys.stdout.write('Are you sure? [yes/No] ')
        if input().lower() == 'yes':
            server.delete()
            write('Server deleted')
        else:
            write('No')


def write(text: str):
    print(text)


# Run

if len(sys.argv) > 2:
    ice_host = sys.argv[1]
    ice_port = sys.argv[2]
else:
    write('Usage: manage-server.py host port [ice file]')
    sys.exit(0)

write('')
write(' Virtual Mumble Server Manager ')
write('')
write('  !! Attention, be careful! ')
write('  !! This script can delete ALL servers, ')
write('  !! including the default server with ID 1. ')
write('')

manage_server = ManageServer(ice_host, ice_port)
run = manage_server.connect()

while run:
    try:
        command = input('command (list, conf-show, new, pw, conf-set, start, stop, delete, quit): ')
        if command == 'list':
            manage_server.list()
        elif command == 'conf-show':
            manage_server.conf_show()
        elif command == 'new':
            manage_server.new()
        elif command == 'pw':
            manage_server.pw()
        elif command == 'conf-set':
            manage_server.conf_set()
        elif command == 'start':
            manage_server.start()
        elif command == 'stop':
            manage_server.stop()
        elif command == 'delete':
            manage_server.delete()
        elif command == 'quit':
            run = False
    except KeyboardInterrupt:
        run = False
        write('')

manage_server.destroy()
