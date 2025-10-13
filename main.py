#!/usr/bin/env python3
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

FILE_PATH = os.getenv('FILE_PATH', './tmp')
UID = os.getenv('UID', '75de94bb-b5cb-4ad4-b72b-251476b36f3a')
S_PATH = os.getenv('S_PATH', UID)
PORT = int(os.getenv('SERVER_PORT', os.getenv('PORT', '3005')))
A_DOMAIN = os.getenv('A_DOMAIN', '')
A_AUTH = os.getenv('A_AUTH', '')
A_PORT = int(os.getenv('A_PORT', '8001'))
CIP = os.getenv('CIP', 'cf.877774.xyz')
CPORT = int(os.getenv('CPORT', '443'))
NAME = os.getenv('NAME', 'Vls')

current_domain: Optional[str] = None
current_links_content: Optional[str] = None
running_processes = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Starting setup in background...", flush=True)
    asyncio.create_task(setup_services())
    yield
    print("Application shutdown: Cleaning up processes...", flush=True)
    await cleanup_processes()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "Hello world!"

@app.get(f"/{S_PATH}")
async def get_links():
    return Response(content=current_links_content or "Links not ready", media_type="text/plain")

def create_directory():
    if not Path(FILE_PATH).exists():
        Path(FILE_PATH).mkdir(parents=True, exist_ok=True)
        print(f"{FILE_PATH} is created", flush=True)
    else:
        print(f"{FILE_PATH} already exists", flush=True)

def cleanup_old_files():
    for file in ['sub.txt', 'boot.log']:
        try:
            (Path(FILE_PATH) / file).unlink(missing_ok=True)
        except:
            pass

def generate_front_config():
    p_v = base64.b64decode('dmxlc3M=').decode('utf-8')
    p_f = base64.b64decode('eHRscy1ycHJ4LXZpc2lvbg==').decode('utf-8')
    o_f = base64.b64decode('ZnJlZWRvbQ==').decode('utf-8')
    o_b = base64.b64decode('YmxhY2tob2xl').decode('utf-8')
    config = {
        "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
        "inbounds": [
            {"port": A_PORT, "protocol": p_v, "settings": {"clients": [{"id": UID, "flow": p_f}], "decryption": "none", "fallbacks": [{"dest": 3001}, {"path": "/vla", "dest": 3002}]}, "streamSettings": {"network": "tcp"}},
            {"port": 3001, "listen": "127.0.0.1", "protocol": p_v, "settings": {"clients": [{"id": UID}], "decryption": "none"}, "streamSettings": {"network": "tcp", "security": "none"}},
            {"port": 3002, "listen": "127.0.0.1", "protocol": p_v, "settings": {"clients": [{"id": UID, "level": 0}], "decryption": "none"}, "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vla"}}, "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}}
        ],
        "dns": {"servers": ["https+local://8.8.8.8/dns-query"]},
        "outbounds": [{"protocol": o_f, "tag": "direct"}, {"protocol": o_b, "tag": "block"}]
    }
    with open(Path(FILE_PATH) / 'config.json', 'w') as f:
        json.dump(config, f, indent=2)

def get_system_architecture():
    arch = platform.machine().lower()
    return 'arm' if arch in ['arm', 'arm64', 'aarch64'] else 'amd'

def get_files_for_architecture(architecture):
    if architecture == 'arm':
        return [{"fileName": "front", "fileUrl": "https://arm.dogchild.eu.org/front"}, {"fileName": "backend", "fileUrl": "https://arm.dogchild.eu.org/backend"}]
    else:
        return [{"fileName": "front", "fileUrl": "https://amd.dogchild.eu.org/front"}, {"fileName": "backend", "fileUrl": "https://amd.dogchild.eu.org/backend"}]

async def download_file(file_name, file_url):
    file_path = Path(FILE_PATH) / file_name
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            expected_size = None
            async with aiofiles.open(file_path, 'wb') as f:
                async with client.stream('GET', file_url) as response:
                    response.raise_for_status()
                    content_length = response.headers.get('Content-Length')
                    if content_length:
                        expected_size = int(content_length)
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        if chunk:
                            await f.write(chunk)
            if expected_size:
                actual_file_size = file_path.stat().st_size
                if actual_file_size != expected_size:
                    print(f"文件大小不匹配: {file_name} - 预期: {expected_size} 字节, 实际: {actual_file_size} 字节", flush=True)
                    if file_path.exists():
                        file_path.unlink()
                    return False
            print(f"成功下载 {file_name}", flush=True)
            return True
    except Exception as e:
        print(f"Download {file_name} failed: {e}", flush=True)
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed incomplete file: {file_path}", flush=True)
            except Exception as delete_error:
                print(f"Failed to remove incomplete file {file_path}: {delete_error}", flush=True)
        return False

async def download_files_and_run():
    architecture = get_system_architecture()
    all_files = get_files_for_architecture(architecture)
    if not all_files:
        print("Can't find files for current architecture", flush=True)
        return False
    files_to_download = [f for f in all_files if not (Path(FILE_PATH) / f["fileName"]).exists()]
    if not files_to_download:
        print("All required files already exist, skipping download", flush=True)
    else:
        results = await asyncio.gather(*[download_file(f["fileName"], f["fileUrl"]) for f in files_to_download])
        if not all(results):
            print("Error downloading files", flush=True)
            return False
    for file_name in ['front', 'backend']:
        file_path = Path(FILE_PATH) / file_name
        if file_path.exists():
            try:
                file_path.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
                print(f"Empowerment success for {file_path}: 775", flush=True)
            except Exception as e:
                print(f"Empowerment failed for {file_path}: {e}", flush=True)
    return True

async def start_front():
    front_path = Path(FILE_PATH) / 'front'
    config_path = Path(FILE_PATH) / 'config.json'
    try:
        process = await asyncio.create_subprocess_exec(
            str(front_path), '-c', str(config_path),
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(process)
        print('front is running', flush=True)
        await asyncio.sleep(1)
        return process
    except Exception as e:
        print(f"front running error: {e}", flush=True)
        return None

async def start_backend():
    backend_path = Path(FILE_PATH) / 'backend'
    if not backend_path.exists():
        print("Backend program not found", flush=True)
        return None
    c_t = base64.b64decode('dHVubmVs').decode('utf-8')
    if A_AUTH and A_DOMAIN and re.match(r'^[A-Z0-9a-z=]{120,250}$', A_AUTH):
        args = [c_t, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', 'run', '--token', A_AUTH]
    else:
        args = [c_t, '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', '--logfile', str(Path(FILE_PATH) / 'boot.log'), '--loglevel', 'info', '--url', f'http://localhost:{A_PORT}']
    try:
        process = await asyncio.create_subprocess_exec(str(backend_path), *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(process)
        print('backend is running', flush=True)
        await asyncio.sleep(2)
        return process
    except Exception as e:
        print(f"Error executing backend: {e}", flush=True)
        return None

async def extract_domains():
    global current_domain
    if A_AUTH and A_DOMAIN:
        current_domain = A_DOMAIN
        print(f'Service Domain: {current_domain}', flush=True)
        return current_domain
    boot_log_path = Path(FILE_PATH) / 'boot.log'
    tcf_domain = base64.b64decode('dHJ5Y2xvdWRmbGFyZS5jb20=').decode('utf-8')
    for attempt in range(15):
        try:
            if boot_log_path.exists():
                async with aiofiles.open(boot_log_path, 'r') as f:
                    content = await f.read()
                matches = re.findall(rf'https?://([^\]*{tcf_domain})/?', content)
                if matches:
                    current_domain = matches[0]
                    print(f'Service Domain: {current_domain}', flush=True)
                    return current_domain
        except:
            pass
        await asyncio.sleep(2)
    print('Service Domain not found', flush=True)
    return None

async def get_isp_info():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            cf_speed_url = base64.b64decode('aHR0cHM6Ly9zcGVlZC5jbG91ZGZsYXJlLmNvbS9tZXRh').decode('utf-8')
            response = await client.get(cf_speed_url)
            response.raise_for_status()
            data = response.json()
            return f"{data.get('country', 'Unknown')}-{data.get('asOrganization', 'ISP')}".replace(' ', '_')
    except:
        return 'Unknown-ISP'

async def generate_links(a_domain):
    global current_links_content
    try:
        isp = await get_isp_info()
        p_v = base64.b64decode('dmxlc3M=').decode('utf-8')
        v_link = f"{p_v}://{UID}@{CIP}:{CPORT}?encryption=none&security=tls&sni={a_domain}&fp=chrome&type=ws&host={a_domain}&path=%2Fvla%3Fed%3D2560#{NAME}-{isp}-vl"
        sub_content = f"{v_link}\n"
        current_links_content = base64.b64encode(sub_content.encode()).decode()
        async with aiofiles.open(Path(FILE_PATH) / 'sub.txt', 'w') as f:
            await f.write(current_links_content)
        print(f"{Path(FILE_PATH) / 'sub.txt'} saved successfully", flush=True)
        print(current_links_content, flush=True)
        return current_links_content
    except Exception as e:
        print(f"Error generating links: {e}", flush=True)
        return None

async def cleanup_processes():
    for process in running_processes:
        try:
            process.terminate()
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except:
            try:
                process.kill()
                await process.wait()
            except:
                pass
    running_processes.clear()

async def setup_services():
    create_directory()
    cleanup_old_files()
    generate_front_config()
    if not await download_files_and_run():
        print("Failed to download required files", flush=True)
        return
    front_process = await start_front()
    if not front_process:
        print("Failed to start front", flush=True)
        return
    backend_process = await start_backend()
    if not backend_process:
        print("Failed to start backend", flush=True)
        return
    await asyncio.sleep(5)
    domain = await extract_domains()
    if not domain:
        print("Failed to extract domain", flush=True)
        return
    await generate_links(domain)
    print(f"\nService setup complete!", flush=True)
    print(f"Port: {PORT}", flush=True)
    print(f"Access URL: http://localhost:{PORT}/{S_PATH}", flush=True)
    print(f"Service Domain: {domain}", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    print("Starting server locally with Uvicorn...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
