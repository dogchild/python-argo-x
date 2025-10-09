#!/usr/bin/env python3
"""
Python-A-X
提供订阅链接的 Python 工具
原作者: dogchild
"""

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

# 加载.env文件配置，优先级：.env文件 > 系统环境变量 > 默认值
load_dotenv(override=True)

# 环境变量配置
FILE_PATH = os.getenv('FILE_PATH', './tmp')  # 运行目录,sub节点文件保存目录
ID = os.getenv('ID', '75de94bb-b5cb-4ad4-b72b-251476b36f3a')  # 用户ID
S_PATH = os.getenv('S_PATH', ID)      # 订阅路径
PORT = int(os.getenv('SERVER_PORT', os.getenv('PORT', '3005')))  # HTTP服务订阅端口
A_DOMAIN = os.getenv('A_DOMAIN', '')   # 固定隧道域名，留空即启用临时隧道
A_AUTH = os.getenv('A_AUTH', '')       # 固定隧道token，留空即启用临时隧道
A_PORT = int(os.getenv('A_PORT', '8001'))  # 固定隧道端口，使用token需在cloudflare后台设置和这里一致
CIP = os.getenv('CIP', 'cf.877774.xyz')    # 节点优选域名或优选IP
CPORT = int(os.getenv('CPORT', '443'))     # 节点优选域名或优选IP对应的端口
NAME = os.getenv('NAME', 'Vls')            # 节点名称前缀

current_domain: Optional[str] = None
current_subscription: Optional[str] = None
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
async def subscription():
    return Response(content=current_subscription or "Subscription not ready", media_type="text/plain")

def create_directory():
    if not Path(FILE_PATH).exists():
        Path(FILE_PATH).mkdir(parents=True, exist_ok=True)
        print(f"{FILE_PATH} is created", flush=True)
    else:
        print(f"{FILE_PATH} already exists", flush=True)

def cleanup_old_files():
    """清理旧的日志和订阅文件"""
    for file in ['sub.txt', 'boot.log']:
        try:
            (Path(FILE_PATH) / file).unlink(missing_ok=True)
        except:
            pass

def generate_front_config():
    """生成 front 服务配置文件"""
    config = {
        "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
        "inbounds": [
            {"port": A_PORT, "protocol": "vless", "settings": {"clients": [{"id": ID, "flow": "xtls-rprx-vision"}], "decryption": "none", "fallbacks": [{"dest": 3001}, {"path": "/vla", "dest": 3002}]}, "streamSettings": {"network": "tcp"}},
            {"port": 3001, "listen": "127.0.0.1", "protocol": "vless", "settings": {"clients": [{"id": ID}], "decryption": "none"}, "streamSettings": {"network": "tcp", "security": "none"}},
            {"port": 3002, "listen": "127.0.0.1", "protocol": "vless", "settings": {"clients": [{"id": ID, "level": 0}], "decryption": "none"}, "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vla"}}, "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}}
        ],
        "dns": {"servers": ["https+local://8.8.8.8/dns-query"]},
        "outbounds": [{"protocol": "freedom", "tag": "direct"}, {"protocol": "blackhole", "tag": "block"}]
    }
    with open(Path(FILE_PATH) / 'config.json', 'w') as f:
        json.dump(config, f, indent=2)

def get_system_architecture():
    """检测系统架构，返回arm或amd"""
    arch = platform.machine().lower()
    return 'arm' if arch in ['arm', 'arm64', 'aarch64'] else 'amd'

def get_files_for_architecture(architecture):
    """根据架构返回需要下载的文件列表"""
    if architecture == 'arm':
        return [{"fileName": "front", "fileUrl": "https://arm.dogchild.eu.org/front"}, {"fileName": "backend", "fileUrl": "https://arm.dogchild.eu.org/backend"}]
    else:
        return [{"fileName": "front", "fileUrl": "https://amd.dogchild.eu.org/front"}, {"fileName": "backend", "fileUrl": "https://amd.dogchild.eu.org/backend"}]

async def download_file(file_name, file_url):
    file_path = Path(FILE_PATH) / file_name
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 一次GET请求同时实现流式下载和获取文件大小信息
            expected_size = None
            
            async with aiofiles.open(file_path, 'wb') as f:
                # stream=True 参数启用流式下载
                async with client.stream('GET', file_url) as response:
                    response.raise_for_status()
                    
                    # 从GET响应头中获取预期的文件大小
                    content_length = response.headers.get('Content-Length')
                    if content_length:
                        expected_size = int(content_length)
                    
                    # 逐块写入文件
                    async for chunk in response.aiter_bytes(chunk_size=8192):  # 8KB chunks
                        if chunk:
                            await f.write(chunk)
            
            # 校验下载的文件大小是否与预期一致
            if expected_size:
                # 检查硬盘上已保存文件的实际大小
                actual_file_size = file_path.stat().st_size
                if actual_file_size != expected_size:
                    print(f"文件大小不匹配: {file_name} - 预期: {expected_size} 字节, 实际: {actual_file_size} 字节", flush=True)
                    # 删除不完整的文件
                    if file_path.exists():
                        file_path.unlink()
                    return False
            
            print(f"成功下载 {file_name}", flush=True)
            return True
    except Exception as e:
        print(f"Download {file_name} failed: {e}", flush=True)
        # 在异常时删除可能已创建的不完整文件
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed incomplete file: {file_path}", flush=True)
            except Exception as delete_error:
                print(f"Failed to remove incomplete file {file_path}: {delete_error}", flush=True)
        return False

async def download_files_and_run():
    """下载 front 和 backend 程序文件并设置执行权限"""
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
    
    # 设置可执行权限
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
    """启动 backend 服务，支持token和临时连接两种模式"""
    backend_path = Path(FILE_PATH) / 'backend'
    if not backend_path.exists():
        print("Backend program not found", flush=True)
        return None
    
    # 根据A_AUTH和A_DOMAIN类型选择启动参数
    if A_AUTH and A_DOMAIN and re.match(r'^[A-Z0-9a-z=]{120,250}$', A_AUTH):  # Token模式（需要同时配置域名和Token）
        args = ['tunnel', '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', 'run', '--token', A_AUTH]
    else:  # 临时连接模式
        args = ['tunnel', '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', '--logfile', str(Path(FILE_PATH) / 'boot.log'), '--loglevel', 'info', '--url', f'http://localhost:{A_PORT}']
    
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
    """提取服务域名，优先使用固定域名，否则从日志中解析连接域名"""
    global current_domain
    if A_AUTH and A_DOMAIN:
        current_domain = A_DOMAIN
        print(f'A_DOMAIN: {current_domain}', flush=True)
        return current_domain
    
    # 从boot.log中提取连接域名
    boot_log_path = Path(FILE_PATH) / 'boot.log'
    for attempt in range(15):
        try:
            if boot_log_path.exists():
                async with aiofiles.open(boot_log_path, 'r') as f:
                    content = await f.read()
                matches = re.findall(r'https?://([^\]*trycloudflare\.com)/?', content)
                if matches:
                    current_domain = matches[0]
                    print(f'ADomain: {current_domain}', flush=True)
                    return current_domain
        except:
            pass
        await asyncio.sleep(2)
    print('ADomain not found', flush=True)
    return None

async def get_isp_info():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get('https://speed.cloudflare.com/meta')
            response.raise_for_status()
            data = response.json()
            return f"{data.get('country', 'Unknown')}-{data.get('asOrganization', 'ISP')}".replace(' ', '_')
    except:
        return 'Unknown-ISP'

async def generate_links(a_domain):
    """生成网络连接配置链接并保存为Base64编码"""
    global current_subscription
    try:
        isp = await get_isp_info()
        vless_link = f"vless://{ID}@{CIP}:{CPORT}?encryption=none&security=tls&sni={a_domain}&type=ws&host={a_domain}&path=%2Fvla%3Fed%3D2560#{NAME}-{isp}-vl"
        
        sub_content = f"{vless_link}\n"
        current_subscription = base64.b64encode(sub_content.encode()).decode()
        
        async with aiofiles.open(Path(FILE_PATH) / 'sub.txt', 'w') as f:
            await f.write(current_subscription)
        
        print(f"{Path(FILE_PATH) / 'sub.txt'} saved successfully", flush=True)
        print(current_subscription, flush=True)
        return current_subscription
    except Exception as e:
        print(f"Error generating subscription: {e}", flush=True)
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
    """
    应用程序的主要设置逻辑。
    此函数创建目录、下载二进制文件、启动子进程并生成订阅链接。
    """
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
    print(f"Subscription URL: http://localhost:{PORT}/{S_PATH}", flush=True)
    print(f"Domain: {domain}", flush=True)
    print("=" * 60, flush=True)



if __name__ == "__main__":
    # 这部分代码允许在本地运行应用程序以进行测试。
    # 它使用 uvicorn 来运行 FastAPI 应用，这将正确触发
    # startup 和 shutdown 事件。
    print("Starting server locally with Uvicorn...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
