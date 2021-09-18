#!/usr/bin/env python3
from ipaddress import IPv4Address
from random import randint
from socket import IPPROTO_TCP, TCP_NODELAY, setdefaulttimeout, socket, timeout
from threading import Event, Thread

running_event = Event()


def check(ip):
    with socket() as s:
        s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)

        if s.connect_ex((ip, 80)) != 0:
            return False

        req = ('GET /wp-content/uploads/ HTTP/1.1\r\n'
               'Host: %s\r\n'
               'Connection: close\r\n'
               'User-Agent: Mozilla/5.0\r\n'
               '\r\n') % ip

        try:
            s.send(req.encode())
            return b'Index of' in s.recv(1024)
        except (ConnectionError, timeout, IndexError, ValueError):
            pass

    return False


def scan():
    while running_event.is_set():
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if ip_address.is_global:
            ip = str(ip_address)
            if check(ip):
                print('[+]', ip)


def main():
    pool = []
    running_event.set()

    setdefaulttimeout(1)

    for _ in range(1024):
        t = Thread(target=scan)
        t.start()
        pool.append(t)

    try:
        for t in pool:
            t.join()
    except KeyboardInterrupt:
        running_event.clear()
        print('\rInterrupt')


if __name__ == '__main__':
    main()
