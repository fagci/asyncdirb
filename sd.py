#!/usr/bin/env python3
from ipaddress import IPv4Address
from random import randint
from socket import socket, timeout as Timeout
from threading import Thread

T = ('GET %s HTTP/1.1\r\n' 'Host: %s\r\n' 'User-Agent: Mozilla/5.0\r\n' '\r\n')


def get(ip, path):
    with socket() as s:
        s.settimeout(1)
        try:
            if s.connect_ex((ip, 80)) != 0:
                return 0, b''

            s.send((T % (path, ip)).encode())
            data = s.recv(1024)
        except (ConnectionError, Timeout):
            return 0, b''

    return int(data.splitlines()[0].split(None, 2)[1]), data


def check(ip):
    res, data = get(ip, '/qwerty')
    if not res:
        return False
    if 200 <= res < 300:
        print('SPA', flush=True)
        return False
    print('not SPA', flush=True)

    res, data = get(ip, '/wp-content/uploads/')

    if 200 <= res < 300 and b'Index of' in data:
        return True

    return False


def scan():
    while True:
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if ip_address.is_global:
            ip = str(ip_address)
            if check(ip):
                print('[+]', ip)


def main():
    pool = []
    for _ in range(1024):
        t = Thread(target=scan)
        t.start()
        pool.append(t)

    for t in pool:
        t.join()


if __name__ == '__main__':
    main()
