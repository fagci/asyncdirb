#!/usr/bin python3
import asyncio
from ipaddress import IPv4Address
from random import randint

T = (
    'GET %s HTTP/1.1\r\n'
    'Host: %s\r\n'
    'User-Agent: Mozilla/5.0\r\n'
    '\r\n'
)

async def check(ip):
    reader, writer = await asyncio.open_connection(ip, 80)
    writer.write((T%('/qwerty', ip)).encode())
    await writer.drain()
    data = await reader.read(1024)
    writer.close()
    await writer.wait_closed()

    if 


async def scan():
    ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
    if ip_address.is_global:
        await check(str(ip_address))


async def main():
    await asyncio.gather(scan() for _ in range(1024))

if __name__ == '__main__':
    asyncio.run(main())
