#!/usr/bin/env python

"""
Simple script to manage virtual servers.

This needs the same setup as mumble-authenticator.py.
"""

import sys
import Ice

# Config

ice_slice = '/usr/share/slice/Murmur.ice'
ice_host = '127.0.0.1'
ice_port = 6502


# Run

try:
    # noinspection PyArgumentList
    Ice.loadSlice('', ['-I' + Ice.getSliceDir(), ice_slice])
except RuntimeError as e:
    print(format(e))
    sys.exit(0)
# noinspection PyUnresolvedReferences
import Murmur

ice = Ice.initialize(sys.argv)
meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy('Meta -e 1.0:tcp -h %s -p %s' % (ice_host, ice_port)))


if len(sys.argv) > 1 and sys.argv[1] == 'list':
    servers = meta.getAllServers()
    for server in servers:
        print('id: {0}, running: {1}, port: {2}, registerName: {3}'.format(
            server.id(),
            server.isRunning(),
            server.getConf('port'),
            server.getConf('registerName'),
        ))

elif len(sys.argv) > 1 and sys.argv[1] == 'conf-all':
    if len(sys.argv) < 3:
        print('usage: manage-server.py conf-all 2')
    else:
        server = meta.getServer(int(sys.argv[2]))
        if server is None:
            print('invalid id')
        else:
            for key, value in server.getAllConf().items():
                print('{0}: {1}'.format(key, value))

elif len(sys.argv) > 1 and sys.argv[1] == 'create':
    new_server = meta.newServer()
    print('new id: {}'.format(new_server.id()))

elif len(sys.argv) > 1 and sys.argv[1] == 'pw':
    if len(sys.argv) < 4:
        print('usage: manage-server.py pw 2 super-user-pw')
    else:
        server = meta.getServer(int(sys.argv[2]))
        if server is None:
            print('invalid id')
        else:
            server.setSuperuserPassword(sys.argv[3])
            print('done')

elif len(sys.argv) > 1 and sys.argv[1] == 'set-conf':
    if len(sys.argv) < 5:
        print('usage: manage-server.py set-conf 2 name value')
        print('valid names: port, registerName, welcometext, ...')
    else:
        server = meta.getServer(int(sys.argv[2]))
        if server is None:
            print('invalid id')
        else:
            server.setConf(sys.argv[3], sys.argv[4])
            print('done')

elif len(sys.argv) > 1 and sys.argv[1] == 'start':
    if len(sys.argv) < 3:
        print('usage: manage-server.py start 2')
    else:
        server = meta.getServer(int(sys.argv[2]))
        if server is None:
            print('invalid id')
        else:
            server.start()
            print('done')

elif len(sys.argv) > 1 and sys.argv[1] == 'stop':
    if len(sys.argv) < 3:
        print('usage: manage-server.py stop 2')
    else:
        server = meta.getServer(int(sys.argv[2]))
        if server is None:
            print('invalid id')
        else:
            server.stop()
            print('done')

elif len(sys.argv) > 1 and sys.argv[1] == 'delete':
    if len(sys.argv) < 3:
        print('usage: manage-server.py delete 2')
    else:
        server_id = int(sys.argv[2])
        if server_id == 1:
            print('No, not deleting server 1.')
        else:
            server = meta.getServer(server_id)
            if server is None:
                print('invalid id')
            else:
                sys.stdout.write('Are you sure? [yes/No] ')
                if input().lower() == 'yes':
                    server.delete()
                    print('deleted server')
                else:
                    print('no')

else:
    print('usage: manage-server.py list|conf-all|create|pw|set-conf|start|stop|delete')


ice.destroy()
