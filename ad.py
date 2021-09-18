#!/usr/bin/env python3
import asyncio
from ipaddress import IPv4Address
from random import randint

T = 'GET /wp-content/uploads/ HTTP/1.1\r\nHost: %s\r\n\r\n'


async def check(ip):
    conn = asyncio.open_connection(ip, 80)

    try:
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=1)
        except asyncio.TimeoutError:
            return False

        writer.write((T % ip).encode('ascii'))
        await writer.drain()

        data = await reader.read(1024)

        writer.close()
        await writer.wait_closed()

        conn.close()

        return b'Index of' in data
    except ConnectionError:
        pass
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
