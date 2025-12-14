import os
import asyncio
import json
import base64
import platform
import stat
import re
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager
import httpx
import aiofiles
from fastapi import FastAPI, Response
import uvicorn
from dotenv import load_dotenv
load_dotenv(override=True)
OOO0O00O0O0O = os.getenv('FILE_PATH', './tmp')
O0O0O000OOO0 = os.getenv('UID', '75de94bb-b5cb-4ad4-b72b-251476b36f3a')
OOOO0O0OO0OO = os.getenv('S_PATH', O0O0O000OOO0)
OO0O0000OO00 = int(os.getenv('SERVER_PORT', os.getenv('PORT', '3005')))
O0O0OOOO000O = os.getenv('A_DOMAIN', '')
O000O00OO0O0 = os.getenv('A_AUTH', '')
O0O0OO0O0OOO = int(os.getenv('A_PORT', '8001'))
OO00O0OOO000 = os.getenv('CIP', 'cf.877774.xyz')
OO00O000OO0O = int(os.getenv('CPORT', '443'))
OO00OOO00OO0 = os.getenv('NAME', 'Vls')
O00OO00O00OO = os.getenv('MLKEM_S', 'mlkem768x25519plus.native.600s.ugygldXvD2pi5St4XBlF4Cgd-55qGCdaOrcJsxdIR5aHGFeYh-Dm1BDsSluXrHUmscV5n9_hPJ8zPfBP4HEgaA')
O000O0O00O00 = os.getenv('MLKEM_C', 'mlkem768x25519plus.native.0rtt.h7xFrUkiWbhXfCNmehc209OOlXhUaPM-2bgKIQyRRLt7WXmEJFsY64QT8se8HcGNLNkKPlTGS1W5XIgRZfFVuNqATbcyuNa7O9BveTB5GaESadgUsWMCs-ugCyTG3WNonYlL0otGzxMEhnohNnkTnoCchQgVULxZAGZW8oYbaNcS-UUZJGhoSvBbz4gZj8RVqDQhd1ReD1E4IMFd2tANlCANZcyZJKykjPdCrqRxiDsxSHGwB6kB4UikaOEAzCSgXNZcJleylvJVkkg54sh4pnGfC0pXp2GjiZFe_cIFRGJJr4mlaCSHphsvecYzctZQiYw3p4xxxRsCtgpUQ2KWReg6YmZCBDy-ckYg8pNp5LtcZBRWE9nDZKVnbpOqL0s442XLqniTLuI1exkbjMJEz-vLIZSNXDA6DieyFyKOUPtFbjcutoq9QGxICAgmvpGn0Qw_JBVoBsJZqwG43wiBcedwBJotJ_SV7klDZEiF-Nud3OaNcmnJWDcEf3O2BiNknpcKbHmrstg8Y0y5kjtfMrau9NDNoiVidNtKtYwQXHA8ndVo15YutaGKs-N9YCavxYUX62fAunulLJAuc6KsDXs_rDlhrFMfxhumq6kNpZxC0vJsvVSQRcVmd-pi8gseXAUOY_zD2paGv2JEQilTtqlrh9cCn-GCP_cYErud-QSsRyCIz5dpGZdEggrPumAlQ4C5j4JniKYaELScBWQWK6E1Y1SPhQFsLgxJFSC9w0pNmIyfleSEEXcd9uOPdVvF0QpJ04dHHKO4r6ekTkkM4XZc7lp1pTwvB8B-tqmjl9Fu4kcgZ0PCQDqGLeq9U3kJUhBsxLhCH8zNzjtaeGooPZAdw_eCJ8dsQmXByaiAs4ofocko4HEfiWh1urqO5dxJMuS3f7WPs6BWthW5vXCuA3mJ_Go87GUY0XEilpE3OJvNNLiBoidadIFnOFI_fqfGGNhxseEGjdF1cLlEtpdLQjWxxcB1BNudQAdWc6tO1StI0KVQwQeFOYS7v3LK2usU1qQmH6UIbmiN5TtmVxodk8FM3xE6fvZZXON1POM_08KPU8QcoYATmUu_sRaWGrlFmTY59zZNoASc7zPHxJm66ZYOiVFcsSh-pmenuzCCa9UcvUSR-OxLNvi9XoZrWOy6n8iP26gnUmcygTQB0phUajxa6fa_85JF6adgD8ylDXiuGpbOchwokbwGbTUMGwmsBSnKDWKqRffDUPq-pZxQOXuwlblsEWUU87DJFHwI2eVKj9sjYVBzm7onKZpt9yRwCEUajIIggzwDRDQwlPil5MS1vWFd4TsIO4oLtbKrR3YK3Xp-kIeZBUMJBliBJfld0vDJNFMnWKXAE_gPySFO9blD8lGgsHKSSYCgF1VUx6B0nsS1nIPMIFvKB6CwKbeHh0gpR9YepBFm99ZAkRRH2Gu0Xtd59fWoOHRFDYVTWtWTA8gY0oxzE4gcFyePjxw0-7Ax2-gg_fnJZia1fwEAZmZnIAg28OAlRutOPVfLFDBIplSb2NCnsfh6tDcruSt6bZhPlwwDS8pggEKdudxNBkNPYeICnErthTVl5qYB_gQ')
OOOO0OO0O00O = os.getenv('M_AUTH', 'ML-KEM-768, Post-Quantum')
current_domain: Optional[str] = None
current_links_content: Optional[str] = None
running_processes = []

@asynccontextmanager
async def O0OO0OOO00O0(OOOOO000OOOO: FastAPI):
    print('Application startup: Starting setup in background...', flush=True)
    asyncio.create_task(OOO0O000O0OO())
    yield
    print('Application shutdown: Cleaning up processes...', flush=True)
    await O0OO0O000O0O()
OO00OO0O0000 = FastAPI(lifespan=O0OO0OOO00O0)

@OO00OO0O0000.get('/')
async def OOOOO0000O0O():
    return 'Hello world!'

@OO00OO0O0000.get(f'/{OOOO0O0OO0OO}')
async def O00000OOOOO0():
    return Response(content=current_links_content or 'Links not ready', media_type='text/plain')

def O000OO00O0OO():
    if not Path(OOO0O00O0O0O).exists():
        Path(OOO0O00O0O0O).mkdir(parents=True, exist_ok=True)
        print(f'{OOO0O00O0O0O} is created', flush=True)
    else:
        print(f'{OOO0O00O0O0O} already exists', flush=True)

def OO0O00OOOO00():
    for O000OOO0000O in ['sub.txt', 'boot.log']:
        try:
            (Path(OOO0O00O0O0O) / O000OOO0000O).unlink(missing_ok=True)
        except:
            pass

async def OOOO0O00O0O0():
    O00O0O000OOO = base64.b64decode('dmxlc3M=').decode('utf-8')
    OO0OOOO0O000 = base64.b64decode('eHRscy1ycHJ4LXZpc2lvbg==').decode('utf-8')
    OOOO0OOOOO0O = base64.b64decode('ZnJlZWRvbQ==').decode('utf-8')
    OO00O00O0OO0 = base64.b64decode('YmxhY2tob2xl').decode('utf-8')
    OO0O000000OO = {'log': {'access': '/dev/null', 'error': '/dev/null', 'loglevel': 'none'}, 'inbounds': [{'port': O0O0OO0O0OOO, 'protocol': O00O0O000OOO, 'settings': {'clients': [{'id': O0O0O000OOO0, 'flow': OO0OOOO0O000}], 'decryption': 'none', 'fallbacks': [{'dest': 3001}, {'path': '/vla', 'dest': 3002}]}, 'streamSettings': {'network': 'tcp'}}, {'port': 3001, 'listen': '127.0.0.1', 'protocol': O00O0O000OOO, 'settings': {'clients': [{'id': O0O0O000OOO0}], 'decryption': 'none'}, 'streamSettings': {'network': 'tcp', 'security': 'none'}}, {'port': 3002, 'listen': '127.0.0.1', 'protocol': O00O0O000OOO, 'settings': {'clients': [{'id': O0O0O000OOO0}], 'decryption': O00OO00O00OO, 'selectedAuth': OOOO0OO0O00O}, 'streamSettings': {'network': 'ws', 'security': 'none', 'wsSettings': {'path': '/vla'}}, 'sniffing': {'enabled': True, 'destOverride': ['http', 'tls', 'quic'], 'metadataOnly': False}}], 'dns': {'servers': ['https+local://8.8.8.8/dns-query']}, 'outbounds': [{'protocol': OOOO0OOOOO0O, 'tag': 'direct'}, {'protocol': OO00O00O0OO0, 'tag': 'block'}]}
    async with aiofiles.open(Path(OOO0O00O0O0O) / 'config.json', 'w') as O0O0OO0O0O00:
        await O0O0OO0O0O00.write(json.dumps(OO0O000000OO, indent=2))

def OOOO0O0OO00O():
    OO0000O000O0 = platform.machine().lower()
    return 'arm' if OO0000O000O0 in ['arm', 'arm64', 'aarch64'] else 'amd'

def OOOOOOOOOOOO(O00000000000):
    if O00000000000 == 'arm':
        return [{'fileName': 'front', 'fileUrl': 'https://arm.dogchild.eu.org/front'}, {'fileName': 'backend', 'fileUrl': 'https://arm.dogchild.eu.org/backend'}]
    else:
        return [{'fileName': 'front', 'fileUrl': 'https://amd.dogchild.eu.org/front'}, {'fileName': 'backend', 'fileUrl': 'https://amd.dogchild.eu.org/backend'}]

async def OO000OOO0O0O(O00OOOO0OOO0, OOO000OOO0OO):
    O00O0OO0OO00 = Path(OOO0O00O0O0O) / O00OOOO0OOO0
    try:
        async with httpx.AsyncClient(timeout=30.0) as O0O0OO0O000O:
            O00OOOOOO0O0 = None
            async with aiofiles.open(O00O0OO0OO00, 'wb') as O0OOO0OO0OOO:
                async with O0O0OO0O000O.stream('GET', OOO000OOO0OO) as O0OO000OO000:
                    O0OO000OO000.raise_for_status()
                    OOO00OO0OO0O = O0OO000OO000.headers.get('Content-Length')
                    if OOO00OO0OO0O:
                        O00OOOOOO0O0 = int(OOO00OO0OO0O)
                    async for O0000O000OO0 in O0OO000OO000.aiter_bytes(chunk_size=8192):
                        if O0000O000OO0:
                            await O0OOO0OO0OOO.write(O0000O000OO0)
            if O00OOOOOO0O0:
                OO000OOO00OO = O00O0OO0OO00.stat().st_size
                if OO000OOO00OO != O00OOOOOO0O0:
                    print(f'文件大小不匹配: {O00OOOO0OOO0} - 预期: {O00OOOOOO0O0} 字节, 实际: {OO000OOO00OO} 字节', flush=True)
                    if O00O0OO0OO00.exists():
                        O00O0OO0OO00.unlink()
                    return False
            print(f'成功下载 {O00OOOO0OOO0}', flush=True)
            return True
    except Exception as e:
        print(f'Download {O00OOOO0OOO0} failed: {e}', flush=True)
        if O00O0OO0OO00.exists():
            try:
                O00O0OO0OO00.unlink()
                print(f'Removed incomplete file: {O00O0OO0OO00}', flush=True)
            except Exception as delete_error:
                print(f'Failed to remove incomplete file {O00O0OO0OO00}: {delete_error}', flush=True)
        return False

async def O00O00000O00():
    O0OO0O00O00O = OOOO0O0OO00O()
    O000OO0O00O0 = OOOOOOOOOOOO(O0OO0O00O00O)
    if not O000OO0O00O0:
        print("Can't find files for current architecture", flush=True)
        return False
    OOOO00OO0000 = [OO000OO0OOOO for OO000OO0OOOO in O000OO0O00O0 if not (Path(OOO0O00O0O0O) / OO000OO0OOOO['fileName']).exists()]
    if not OOOO00OO0000:
        print('All required files already exist, skipping download', flush=True)
    else:
        OOOOO00OOOO0 = await asyncio.gather(*[OO000OOO0O0O(OO0O0OO00O0O['fileName'], OO0O0OO00O0O['fileUrl']) for OO0O0OO00O0O in OOOO00OO0000])
        if not all(OOOOO00OOOO0):
            print('Error downloading files', flush=True)
            return False
    for OOOOO0O0O0OO in ['front', 'backend']:
        O00OO00OOO00 = Path(OOO0O00O0O0O) / OOOOO0O0O0OO
        if O00OO00OOO00.exists():
            try:
                O00OO00OOO00.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
                print(f'Empowerment success for {O00OO00OOO00}: 775', flush=True)
            except Exception as e:
                print(f'Empowerment failed for {O00OO00OOO00}: {e}', flush=True)
    return True

async def O000OO00000O():
    O000O0O0O0O0 = Path(OOO0O00O0O0O) / 'front'
    O0O000O00OOO = Path(OOO0O00O0O0O) / 'config.json'
    try:
        OO000O00O000 = await asyncio.create_subprocess_exec(str(O000O0O0O0O0), '-c', str(O0O000O00OOO), stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(OO000O00O000)
        print('front is running', flush=True)
        await asyncio.sleep(1)
        return OO000O00O000
    except Exception as e:
        print(f'front running error: {e}', flush=True)
        return None

async def O00O0O0OOO0O():
    OOOOOOOO0OO0 = Path(OOO0O00O0O0O) / 'backend'
    if not OOOOOOOO0OO0.exists():
        print('Backend program not found', flush=True)
        return None
    OOOOOOO000OO = base64.b64decode('dHVubmVs').decode('utf-8')
    if O000O00OO0O0 and O0O0OOOO000O and re.match('^[A-Z0-9a-z=]{120,250}$', O000O00OO0O0):
        O0OO00OO0O00 = [OOOOOOO000OO, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', 'run', '--token', O000O00OO0O0]
    else:
        O0OO00OO0O00 = [OOOOOOO000OO, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', '--logfile', str(Path(OOO0O00O0O0O) / 'boot.log'), '--loglevel', 'info', '--url', f'http://localhost:{O0O0OO0O0OOO}']
    try:
        O0OO00OOO00O = await asyncio.create_subprocess_exec(str(OOOOOOOO0OO0), *O0OO00OO0O00, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(O0OO00OOO00O)
        print('backend is running', flush=True)
        await asyncio.sleep(2)
        return O0OO00OOO00O
    except Exception as e:
        print(f'Error executing backend: {e}', flush=True)
        return None

async def O00OO00000O0():
    global current_domain
    if O000O00OO0O0 and O0O0OOOO000O:
        current_domain = O0O0OOOO000O
        print(f'Service Domain: {current_domain}', flush=True)
        return current_domain
    OO00OO0OOOOO = Path(OOO0O00O0O0O) / 'boot.log'
    O0O00OO00000 = base64.b64decode('dHJ5Y2xvdWRmbGFyZS5jb20=').decode('utf-8')
    for O0O00O0O0O0O in range(15):
        try:
            if OO00OO0OOOOO.exists():
                async with aiofiles.open(OO00OO0OOOOO, 'r') as O00O0O00OOO0:
                    OO0O000OO0OO = await O00O0O00OOO0.read()
                OO0OOO00OO00 = re.findall(f'https?://([^\\]*{O0O00OO00000})/?', OO0O000OO0OO)
                if OO0OOO00OO00:
                    current_domain = OO0OOO00OO00[0]
                    print(f'Service Domain: {current_domain}', flush=True)
                    return current_domain
        except:
            pass
        await asyncio.sleep(2)
    print('Service Domain not found', flush=True)
    return None

async def O0O0O0OO000O():
    try:
        async with httpx.AsyncClient(timeout=10.0) as O0OO0O0OO0O0:
            OO00O00O0OOO = 'https://ipapi.co/json/'
            O00O0OOOO000 = await O0OO0O0OO0O0.get(OO00O00O0OOO)
            O00O0OOOO000.raise_for_status()
            O0000O00OO0O = O00O0OOOO000.json()
            return f"{O0000O00OO0O.get('country_code', 'Unknown')}-{O0000O00OO0O.get('org', 'ISP')}".replace(' ', '_')
    except Exception as e:
        print(f'Error fetching meta data: {e}', flush=True)
        return 'Unknown-ISP'

async def O0OOO0O00OO0(OOOO0O0O00OO):
    global current_links_content
    try:
        O00O0OO00O00 = await O0O0O0OO000O()
        OOOO00O0O00O = base64.b64decode('dmxlc3M=').decode('utf-8')
        OOO000OO00O0 = f'{OOOO00O0O00O}://{O0O0O000OOO0}@{OO00O0OOO000}:{OO00O000OO0O}?encryption={O000O0O00O00}&security=tls&sni={OOOO0O0O00OO}&fp=chrome&type=ws&host={OOOO0O0O00OO}&path=%2Fvla%3Fed%3D2560#{OO00OOO00OO0}-{O00O0OO00O00}'
        O00O0O00OOOO = f'{OOO000OO00O0}\n'
        current_links_content = base64.b64encode(O00O0O00OOOO.encode()).decode()
        async with aiofiles.open(Path(OOO0O00O0O0O) / 'sub.txt', 'w') as O00OO00O0000:
            await O00OO00O0000.write(current_links_content)
        print(f"{Path(OOO0O00O0O0O) / 'sub.txt'} saved successfully", flush=True)
        print(current_links_content, flush=True)
        return current_links_content
    except Exception as e:
        print(f'Error generating links: {e}', flush=True)
        return None

async def O0OO0O000O0O():
    for OOO0OOOOOOO0 in running_processes:
        try:
            OOO0OOOOOOO0.terminate()
            await asyncio.wait_for(OOO0OOOOOOO0.wait(), timeout=5.0)
        except:
            try:
                OOO0OOOOOOO0.kill()
                await OOO0OOOOOOO0.wait()
            except:
                pass
    running_processes.clear()

async def OOO0O000O0OO():
    O000OO00O0OO()
    OO0O00OOOO00()
    await OOOO0O00O0O0()
    if not await O00O00000O00():
        print('Failed to download required files', flush=True)
        return
    OO0OOOOOOO00 = await O000OO00000O()
    if not OO0OOOOOOO00:
        print('Failed to start front', flush=True)
        return
    O000O0O0000O = await O00O0O0OOO0O()
    if not O000O0O0000O:
        print('Failed to start backend', flush=True)
        return
    await asyncio.sleep(5)
    O0O00000O0O0 = await O00OO00000O0()
    if not O0O00000O0O0:
        print('Failed to extract domain', flush=True)
        return
    await O0OOO0O00OO0(O0O00000O0O0)
    print(f'\nService setup complete!', flush=True)
    print(f'Port: {OO0O0000OO00}', flush=True)
    print(f'Access URL: http://localhost:{OO0O0000OO00}/{OOOO0O0OO0OO}', flush=True)
    print(f'Service Domain: {O0O00000O0O0}', flush=True)
    print('=' * 60, flush=True)
if __name__ == '__main__':
    print('Starting server locally with Uvicorn...', flush=True)
    uvicorn.run(OO00OO0O0000, host='0.0.0.0', port=OO0O0000OO00)