lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII = str, all, print, int, bool, __name__, Exception, range

from os import getenv as IllIllIlIlIllI
from asyncio import wait_for as lIlIIIlllIlIIl, create_task as IIlIlIlIllIllI, sleep as llllIIIlIlIIII, create_subprocess_exec as lIlIlIIllIIIlI, gather as IIllIlllIllIIl
from base64 import b64encode as llIIIIlIlIlIll, b64decode as IIIIIIIIlIIlll
from json import dump as IlIlIIlIIlIlIl
from platform import machine as IIlIllIIlllIII
from httpx import AsyncClient as lllIllllIIIlll
from aiofiles import open as IlIllIIIIlIlll
from stat import S_IXOTH as llIllllIllIIII, S_IRWXU as llllllIlIIlllI, S_IRWXG as IIIIIIIlIllIIl, S_IROTH as IIIIlIllllIIlI
from asyncio.subprocess import DEVNULL as IIllIIIIIIlIIl
from re import findall as lIlllIlIllllIl, match as IllIIIllIIIIII
from uvicorn import run as IIllIIIlIIIIII
from pathlib import Path as lIIlIlIlIIIIlI
from typing import Optional as IllIlIIIlllIIl
from contextlib import asynccontextmanager as IIIllIllIIlIIl
from fastapi import FastAPI as lIllIIllIlllll, Response as IlIIllllIllIII
from dotenv import load_dotenv as llllIIllIllIII
llllIIllIllIII(override=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
llIIlIIIlIIIlIlIlI = IllIllIlIlIllI('FILE_PATH', './tmp')
IIIlIIIIllIIIllIII = IllIllIlIlIllI('UID', '75de94bb-b5cb-4ad4-b72b-251476b36f3a')
IIlllIllIllllllIII = IllIllIlIlIllI('S_PATH', IIIlIIIIllIIIllIII)
IIlllllllIIllIlIIl = lllllllllllllII(IllIllIlIlIllI('SERVER_PORT', IllIllIlIlIllI('PORT', '3005')))
IlIllllIIIIllllIlI = IllIllIlIlIllI('A_DOMAIN', '')
llIIlIIIIlIlllIIll = IllIllIlIlIllI('A_AUTH', '')
IIIlIlIllIIlIIIllI = lllllllllllllII(IllIllIlIlIllI('A_PORT', '8001'))
IlIlIllIIllIllIlII = IllIllIlIlIllI('CIP', 'cf.877774.xyz')
IIlllIlllllIlIlIII = lllllllllllllII(IllIllIlIlIllI('CPORT', '443'))
IlIlIllllIIlIllIIl = IllIllIlIlIllI('NAME', 'Vls')
IIlIIIIIIIIllIlIII: IllIlIIIlllIIl[lllllllllllllll] = None
IlIIIlIlIllIllIIlI: IllIlIIIlllIIl[lllllllllllllll] = None
lIlllIIIlIIlIIllIl = []

@IIIllIllIIlIIl
async def llllllllllIlIllIlI(app: lIllIIllIlllll):
    lllllllllllllIl('Application startup: Starting setup in background...', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    IIlIlIlIllIllI(llIlIIlllIlIIIIIII())
    yield
    lllllllllllllIl('Application shutdown: Cleaning up processes...', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    await IIIIlIlIllIlllIlIl()
app = lIllIIllIlllll(lifespan=llllllllllIlIllIlI)

@app.get('/')
async def lllIlIIIlIlIIlllII():
    return 'Hello world!'

@app.get(f'/{IIlllIllIllllllIII}')
async def IlIIlIIIlIllIIIlII():
    return IlIIllllIllIII(content=IlIIIlIlIllIllIIlI or 'Links not ready', media_type='text/plain')

def llIllIIIlllIIIIIlI():
    if not lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI).exists():
        lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI).mkdir(parents=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), exist_ok=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        lllllllllllllIl(f'{llIIlIIIlIIIlIlIlI} is created', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    else:
        lllllllllllllIl(f'{llIIlIIIlIIIlIlIlI} already exists', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

def lIlIlIIlIIlllIlIll():
    for lllIIllIllllllllIl in ['sub.txt', 'boot.log']:
        try:
            (lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / lllIIllIllllllllIl).unlink(missing_ok=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        except:
            pass

def IllIIlllIIIIIlllII():
    IlIlllIIlIlIlllIIl = IIIIIIIIlIIlll('dmxlc3M=').decode('utf-8')
    lllllIIIIllIIlIIIl = IIIIIIIIlIIlll('eHRscy1ycHJ4LXZpc2lvbg==').decode('utf-8')
    IllllIlllIIIIlIllI = IIIIIIIIlIIlll('ZnJlZWRvbQ==').decode('utf-8')
    lIIIlllIIllIIlllII = IIIIIIIIlIIlll('YmxhY2tob2xl').decode('utf-8')
    llllIIIIllIlllllIl = {'log': {'access': '/dev/null', 'error': '/dev/null', 'loglevel': 'none'}, 'inbounds': [{'port': IIIlIlIllIIlIIIllI, 'protocol': IlIlllIIlIlIlllIIl, 'settings': {'clients': [{'id': IIIlIIIIllIIIllIII, 'flow': lllllIIIIllIIlIIIl}], 'decryption': 'none', 'fallbacks': [{'dest': 3001}, {'path': '/vla', 'dest': 3002}]}, 'streamSettings': {'network': 'tcp'}}, {'port': 3001, 'listen': '127.0.0.1', 'protocol': IlIlllIIlIlIlllIIl, 'settings': {'clients': [{'id': IIIlIIIIllIIIllIII}], 'decryption': 'none'}, 'streamSettings': {'network': 'tcp', 'security': 'none'}}, {'port': 3002, 'listen': '127.0.0.1', 'protocol': IlIlllIIlIlIlllIIl, 'settings': {'clients': [{'id': IIIlIIIIllIIIllIII, 'level': 0}], 'decryption': 'none'}, 'streamSettings': {'network': 'ws', 'security': 'none', 'wsSettings': {'path': '/vla'}}, 'sniffing': {'enabled': llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), 'destOverride': ['http', 'tls', 'quic'], 'metadataOnly': llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)}}], 'dns': {'servers': ['https+local://8.8.8.8/dns-query']}, 'outbounds': [{'protocol': IllllIlllIIIIlIllI, 'tag': 'direct'}, {'protocol': lIIIlllIIllIIlllII, 'tag': 'block'}]}
    with IlIllIIIIlIlll(lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'config.json', 'w') as lllIIIlllIIlllIIII:
        IlIlIIlIIlIlIl(llllIIIIllIlllllIl, lllIIIlllIIlllIIII, indent=2)

def lIlIlIlIIlllIIlIll():
    lIlIIlIIlIIIllllII = IIlIllIIlllIII().lower()
    return 'arm' if lIlIIlIIlIIIllllII in ['arm', 'arm64', 'aarch64'] else 'amd'

def IllIIlIIIIIllIllIl(lIIIlIllIIlIllllII):
    if lIIIlIllIIlIllllII == 'arm':
        return [{'fileName': 'front', 'fileUrl': 'https://arm.dogchild.eu.org/front'}, {'fileName': 'backend', 'fileUrl': 'https://arm.dogchild.eu.org/backend'}]
    else:
        return [{'fileName': 'front', 'fileUrl': 'https://amd.dogchild.eu.org/front'}, {'fileName': 'backend', 'fileUrl': 'https://amd.dogchild.eu.org/backend'}]

async def IllIIllIllIIIIIIll(IlIIlIIlIllIIlIIII, lIllIIIIlIlllllIII):
    lllIIIIIlIIlIllIIl = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / IlIIlIIlIllIIlIIII
    try:
        async with lllIllllIIIlll(timeout=30.0) as client:
            llIlIIllIIIlIllIll = None
            async with IlIllIIIIlIlll(lllIIIIIlIIlIllIIl, 'wb') as lllIIIlllIIlllIIII:
                async with client.stream('GET', lIllIIIIlIlllllIII) as lIlIllIlIlllllIIll:
                    lIlIllIlIlllllIIll.raise_for_status()
                    llllIlllIlIIIIllIl = lIlIllIlIlllllIIll.headers.get('Content-Length')
                    if llllIlllIlIIIIllIl:
                        llIlIIllIIIlIllIll = lllllllllllllII(llllIlllIlIIIIllIl)
                    async for chunk in lIlIllIlIlllllIIll.aiter_bytes(chunk_size=8192):
                        if chunk:
                            await lllIIIlllIIlllIIII.write(chunk)
            if llIlIIllIIIlIllIll:
                llllIIIllIIllllIIl = lllIIIIIlIIlIllIIl.stat().st_size
                if llllIIIllIIllllIIl != llIlIIllIIIlIllIll:
                    lllllllllllllIl(f'文件大小不匹配: {IlIIlIIlIllIIlIIII} - 预期: {llIlIIllIIIlIllIll} 字节, 实际: {llllIIIllIIllllIIl} 字节', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                    if lllIIIIIlIIlIllIIl.exists():
                        lllIIIIIlIIlIllIIl.unlink()
                    return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
            lllllllllllllIl(f'成功下载 {IlIIlIIlIllIIlIIII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    except llllllllllllIIl as llIIIlIlIIIIlIIlII:
        lllllllllllllIl(f'Download {IlIIlIIlIllIIlIIII} failed: {llIIIlIlIIIIlIIlII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        if lllIIIIIlIIlIllIIl.exists():
            try:
                lllIIIIIlIIlIllIIl.unlink()
                lllllllllllllIl(f'Removed incomplete file: {lllIIIIIlIIlIllIIl}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            except llllllllllllIIl as lllllIlIlIlIlIllIl:
                lllllllllllllIl(f'Failed to remove incomplete file {lllIIIIIlIIlIllIIl}: {lllllIlIlIlIlIllIl}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

async def IIllIIIlIllIlIIIII():
    lIIIlIllIIlIllllII = lIlIlIlIIlllIIlIll()
    IIllIIlIIllIIIlIII = IllIIlIIIIIllIllIl(lIIIlIllIIlIllllII)
    if not IIllIIlIIllIIIlIII:
        lllllllllllllIl("Can't find files for current architecture", flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    lIIIlIllIIlllllIlI = [lllIIIlllIIlllIIII for lllIIIlllIIlllIIII in IIllIIlIIllIIIlIII if not (lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / lllIIIlllIIlllIIII['fileName']).exists()]
    if not lIIIlIllIIlllllIlI:
        lllllllllllllIl('All required files already exist, skipping download', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    else:
        IllIlIlIIIIlIlIlll = await IIllIlllIllIIl(*[IllIIllIllIIIIIIll(lllIIIlllIIlllIIII['fileName'], lllIIIlllIIlllIIII['fileUrl']) for lllIIIlllIIlllIIII in lIIIlIllIIlllllIlI])
        if not llllllllllllllI(IllIlIlIIIIlIlIlll):
            lllllllllllllIl('Error downloading files', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    for IlIIlIIlIllIIlIIII in ['front', 'backend']:
        lllIIIIIlIIlIllIIl = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / IlIIlIIlIllIIlIIII
        if lllIIIIIlIIlIllIIl.exists():
            try:
                lllIIIIIlIIlIllIIl.chmod(llllllIlIIlllI | IIIIIIIlIllIIl | IIIIlIllllIIlI | llIllllIllIIII)
                lllllllllllllIl(f'Empowerment success for {lllIIIIIlIIlIllIIl}: 775', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            except llllllllllllIIl as llIIIlIlIIIIlIIlII:
                lllllllllllllIl(f'Empowerment failed for {lllIIIIIlIIlIllIIl}: {llIIIlIlIIIIlIIlII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

async def lIIIIIlllIIllIIIll():
    IIllIlIIlIllIIllIl = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'front'
    IIIIlIllllIIIIIIlI = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'config.json'
    try:
        llllIllIIIllIlIlIl = await lIlIlIIllIIIlI(lllllllllllllll(IIllIlIIlIllIIllIl), '-c', lllllllllllllll(IIIIlIllllIIIIIIlI), stdout=IIllIIIIIIlIIl, stderr=IIllIIIIIIlIIl)
        lIlllIIIlIIlIIllIl.append(llllIllIIIllIlIlIl)
        lllllllllllllIl('front is running', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await llllIIIlIlIIII(1)
        return llllIllIIIllIlIlIl
    except llllllllllllIIl as llIIIlIlIIIIlIIlII:
        lllllllllllllIl(f'front running error: {llIIIlIlIIIIlIIlII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return None

async def lIIllIlIIlIllllIIl():
    llllIlIlllIllIlIll = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'backend'
    if not llllIlIlllIllIlIll.exists():
        lllllllllllllIl('Backend program not found', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return None
    llIIllIlIlIlIlllIl = IIIIIIIIlIIlll('dHVubmVs').decode('utf-8')
    if llIIlIIIIlIlllIIll and IlIllllIIIIllllIlI and IllIIIllIIIIII('^[A-Z0-9a-z=]{120,250}$', llIIlIIIIlIlllIIll):
        lIllIlIIIllIllIIlI = [llIIllIlIlIlIlllIl, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', 'run', '--token', llIIlIIIIlIlllIIll]
    else:
        lIllIlIIIllIllIIlI = [llIIllIlIlIlIlllIl, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', '--logfile', lllllllllllllll(lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'boot.log'), '--loglevel', 'info', '--url', f'http://localhost:{IIIlIlIllIIlIIIllI}']
    try:
        llllIllIIIllIlIlIl = await lIlIlIIllIIIlI(lllllllllllllll(llllIlIlllIllIlIll), *lIllIlIIIllIllIIlI, stdout=IIllIIIIIIlIIl, stderr=IIllIIIIIIlIIl)
        lIlllIIIlIIlIIllIl.append(llllIllIIIllIlIlIl)
        lllllllllllllIl('backend is running', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await llllIIIlIlIIII(2)
        return llllIllIIIllIlIlIl
    except llllllllllllIIl as llIIIlIlIIIIlIIlII:
        lllllllllllllIl(f'Error executing backend: {llIIIlIlIIIIlIIlII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return None

async def IlllIllIllllIIIllI():
    global IIlIIIIIIIIllIlIII
    if llIIlIIIIlIlllIIll and IlIllllIIIIllllIlI:
        IIlIIIIIIIIllIlIII = IlIllllIIIIllllIlI
        lllllllllllllIl(f'Service Domain: {IIlIIIIIIIIllIlIII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return IIlIIIIIIIIllIlIII
    lllIIllIIIllllIIII = lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'boot.log'
    IllIlllllllIllIIII = IIIIIIIIlIIlll('dHJ5Y2xvdWRmbGFyZS5jb20=').decode('utf-8')
    for llIIIlIIlIIIllIllI in llllllllllllIII(15):
        try:
            if lllIIllIIIllllIIII.exists():
                async with IlIllIIIIlIlll(lllIIllIIIllllIIII, 'r') as lllIIIlllIIlllIIII:
                    lIllllIIIIlIlIllll = await lllIIIlllIIlllIIII.read()
                lllllIlIlllIIlIllI = lIlllIlIllllIl(f'https?://([^\\]*{IllIlllllllIllIIII})/?', lIllllIIIIlIlIllll)
                if lllllIlIlllIIlIllI:
                    IIlIIIIIIIIllIlIII = lllllIlIlllIIlIllI[0]
                    lllllllllllllIl(f'Service Domain: {IIlIIIIIIIIllIlIII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                    return IIlIIIIIIIIllIlIII
        except:
            pass
        await llllIIIlIlIIII(2)
    lllllllllllllIl('Service Domain not found', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    return None

async def llllIIIIIlllIIIIlI():
    try:
        async with lllIllllIIIlll(timeout=10.0) as client:
            lllIIIIIlIIllIIllI = IIIIIIIIlIIlll('aHR0cHM6Ly9zcGVlZC5jbG91ZGZsYXJlLmNvbS9tZXRh').decode('utf-8')
            lIlIllIlIlllllIIll = await client.get(lllIIIIIlIIllIIllI)
            lIlIllIlIlllllIIll.raise_for_status()
            IIIlllIlIIlIIIIIII = lIlIllIlIlllllIIll.json()
            return f"{IIIlllIlIIlIIIIIII.get('country', 'Unknown')}-{IIIlllIlIIlIIIIIII.get('asOrganization', 'ISP')}".replace(' ', '_')
    except:
        return 'Unknown-ISP'

async def lIllIIlIIIIIIIIIll(lIIIlIlIlIlIllllll):
    global IlIIIlIlIllIllIIlI
    try:
        IIIllIllllIllIllll = await llllIIIIIlllIIIIlI()
        IlIlllIIlIlIlllIIl = IIIIIIIIlIIlll('dmxlc3M=').decode('utf-8')
        llIlIIlIlIIIIlIIII = f'{IlIlllIIlIlIlllIIl}://{IIIlIIIIllIIIllIII}@{IlIlIllIIllIllIlII}:{IIlllIlllllIlIlIII}?encryption=none&security=tls&sni={lIIIlIlIlIlIllllll}&fp=chrome&type=ws&host={lIIIlIlIlIlIllllll}&path=%2Fvla%3Fed%3D2560#{IlIlIllllIIlIllIIl}-{IIIllIllllIllIllll}-vl'
        llIlIlIIIIIIIllllI = f'{llIlIIlIlIIIIlIIII}\n'
        IlIIIlIlIllIllIIlI = llIIIIlIlIlIll(llIlIlIIIIIIIllllI.encode()).decode()
        async with IlIllIIIIlIlll(lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'sub.txt', 'w') as lllIIIlllIIlllIIII:
            await lllIIIlllIIlllIIII.write(IlIIIlIlIllIllIIlI)
        lllllllllllllIl(f"{lIIlIlIlIIIIlI(llIIlIIIlIIIlIlIlI) / 'sub.txt'} saved successfully", flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        lllllllllllllIl(IlIIIlIlIllIllIIlI, flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return IlIIIlIlIllIllIIlI
    except llllllllllllIIl as llIIIlIlIIIIlIIlII:
        lllllllllllllIl(f'Error generating links: {llIIIlIlIIIIlIIlII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return None

async def IIIIlIlIllIlllIlIl():
    for llllIllIIIllIlIlIl in lIlllIIIlIIlIIllIl:
        try:
            llllIllIIIllIlIlIl.terminate()
            await lIlIIIlllIlIIl(llllIllIIIllIlIlIl.wait(), timeout=5.0)
        except:
            try:
                llllIllIIIllIlIlIl.kill()
                await llllIllIIIllIlIlIl.wait()
            except:
                pass
    lIlllIIIlIIlIIllIl.clear()

async def llIlIIlllIlIIIIIII():
    llIllIIIlllIIIIIlI()
    lIlIlIIlIIlllIlIll()
    IllIIlllIIIIIlllII()
    if not await IIllIIIlIllIlIIIII():
        lllllllllllllIl('Failed to download required files', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    IIlIlIlllIlllllIII = await lIIIIIlllIIllIIIll()
    if not IIlIlIlllIlllllIII:
        lllllllllllllIl('Failed to start front', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    IIIlIllIIIlIIlllIl = await lIIllIlIIlIllllIIl()
    if not IIIlIllIIIlIIlllIl:
        lllllllllllllIl('Failed to start backend', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    await llllIIIlIlIIII(5)
    IIlIIIIlIIlIIIIllI = await IlllIllIllllIIIllI()
    if not IIlIIIIlIIlIIIIllI:
        lllllllllllllIl('Failed to extract domain', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    await lIllIIlIIIIIIIIIll(IIlIIIIlIIlIIIIllI)
    lllllllllllllIl(f'\nService setup complete!', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    lllllllllllllIl(f'Port: {IIlllllllIIllIlIIl}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    lllllllllllllIl(f'Access URL: http://localhost:{IIlllllllIIllIlIIl}/{IIlllIllIllllllIII}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    lllllllllllllIl(f'Service Domain: {IIlIIIIlIIlIIIIllI}', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    lllllllllllllIl('=' * 60, flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
if llllllllllllIlI == '__main__':
    lllllllllllllIl('Starting server locally with Uvicorn...', flush=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    IIllIIIlIIIIII(app, host='0.0.0.0', port=IIlllllllIIllIlIIl)