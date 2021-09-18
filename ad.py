#!/usr/bin/env python3
import asyncio
from ipaddress import IPv4Address
from random import randint

T = ('GET %s HTTP/1.1\r\n' 'Host: %s\r\n' 'User-Agent: Mozilla/5.0\r\n' '\r\n')


async def get(ip, path):
    conn = asyncio.open_connection(ip, 80)

    try:
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=1)
        except asyncio.TimeoutError:
            return 0, b''
        writer.write((T % (path, ip)).encode())
        await writer.drain()

        data = await reader.read(1024)

        writer.close()
        await writer.wait_closed()
    except ConnectionError:
        return 0, b''

    return int(data.splitlines()[0].split(None, 2)[1]), data


async def check(ip):
    res, data = await get(ip, '/qwerty')
    if not res:
        return False
    if 200 <= res < 300:
        print('SPA', flush=True)
        return False
    print('not SPA', flush=True)

    res, data = await get(ip, '/wp-content/uploads/')

    if 200 <= res < 300 and b'Index of' in data:
        return True

    return False


async def scan():
    while True:
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if ip_address.is_global:
            ip = str(ip_address)
            if await check(ip):
                print('[+]', ip)


async def main():
    await asyncio.gather(asyncio.wait([scan() for _ in range(1024)]))


if __name__ == '__main__':
    asyncio.run(main())
