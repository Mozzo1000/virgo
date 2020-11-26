#!/usr/bin/env python3

import sys
import os
import socket
import selectors
import traceback
import argparse
from virgo.server_message import ServerMessage
from virgo.sitemap import SitemapGenerator


sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser(prog='virgo server', description='An experimental virgo protocol server')
parser.add_argument('-v', '--version', action='version', version='virgo server 1.0')

group = parser.add_argument_group('Server configuration')
group.add_argument('--host', help='Server address', default='127.0.0.1')
group.add_argument('-p', '--port', help='Server port', type=int, default=1784)
group.add_argument('-d', '--directory', help='Root directory on the filesystem to serve', default=os.path.abspath(os.path.join(__file__, os.pardir)) + '/tests/www')

sitemap = SitemapGenerator(root=parser.parse_args().directory, domain=parser.parse_args().host)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = ServerMessage(sel, conn, addr, parser.parse_args().directory, sitemap)
    sel.register(conn, selectors.EVENT_READ, data=message)


def main():
    args = parser.parse_args()
    host = args.host
    port = args.port
    
    sitemap.generate()

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()


if __name__ == "__main__":
    main()
