#!/usr/bin/env python3
"""
Python-Argo-X
通过 Argo 提供订阅链接的 Python 工具
原作者: dogchild
"""

import os
import asyncio
import json
import base64
import platform
import stat
import re
import signal
import sys
from pathlib import Path
from typing import Optional

import httpx
import aiofiles
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

# 加载.env文件配置，优先级：.env文件 > 系统环境变量 > 默认值
load_dotenv(override=True)

# 环境变量配置
FILE_PATH = os.getenv('FILE_PATH', './tmp')  # 运行目录,sub节点文件保存目录
SUB_PATH = os.getenv('SUB_PATH', 'sub')      # 订阅路径
PORT = int(os.getenv('SERVER_PORT', os.getenv('PORT', '3005')))  # HTTP服务订阅端口
UUID = os.getenv('UUID', '75de94bb-b5cb-4ad4-b72b-251476b36f3a')  # 用户UUID
ARGO_DOMAIN = os.getenv('ARGO_DOMAIN', '')   # 固定隧道域名，留空即启用临时隧道
ARGO_AUTH = os.getenv('ARGO_AUTH', '')       # 固定隧道密钥json或token，留空即启用临时隧道
ARGO_PORT = int(os.getenv('ARGO_PORT', '8001'))  # 固定隧道端口，使用token需在cloudflare后台设置和这里一致
CFIP = os.getenv('CFIP', 'cf.877774.xyz')    # 节点优选域名或优选IP
CFPORT = int(os.getenv('CFPORT', '443'))     # 节点优选域名或优选IP对应的端口
NAME = os.getenv('NAME', 'Vls')              # 节点名称前缀

current_domain: Optional[str] = None
current_subscription: Optional[str] = None
running_processes = []
app = FastAPI()

@app.get("/")
async def root():
    return "Hello world!"

@app.get(f"/{SUB_PATH}")
async def subscription():
    return current_subscription or "Subscription not ready"

def create_directory():
    if not Path(FILE_PATH).exists():
        Path(FILE_PATH).mkdir(parents=True, exist_ok=True)
        print(f"{FILE_PATH} is created")
    else:
        print(f"{FILE_PATH} already exists")

def cleanup_old_files():
    """清理旧的日志和订阅文件"""
    for file in ['sub.txt', 'boot.log']:
        try:
            (Path(FILE_PATH) / file).unlink(missing_ok=True)
        except:
            pass

def generate_web_config():
    """生成web配置文件，支持VLESS、VMess、Trojan三种协议"""
    config = {
        "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
        "inbounds": [
            {"port": ARGO_PORT, "protocol": "vless", "settings": {"clients": [{"id": UUID, "flow": "xtls-rprx-vision"}], "decryption": "none", "fallbacks": [{"dest": 3001}, {"path": "/vless-argo", "dest": 3002}, {"path": "/vmess-argo", "dest": 3003}, {"path": "/trojan-argo", "dest": 3004}]}, "streamSettings": {"network": "tcp"}},
            {"port": 3001, "listen": "127.0.0.1", "protocol": "vless", "settings": {"clients": [{"id": UUID}], "decryption": "none"}, "streamSettings": {"network": "tcp", "security": "none"}},
            {"port": 3002, "listen": "127.0.0.1", "protocol": "vless", "settings": {"clients": [{"id": UUID, "level": 0}], "decryption": "none"}, "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vless-argo"}}, "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}},
            {"port": 3003, "listen": "127.0.0.1", "protocol": "vmess", "settings": {"clients": [{"id": UUID, "alterId": 0}]}, "streamSettings": {"network": "ws", "wsSettings": {"path": "/vmess-argo"}}, "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}},
            {"port": 3004, "listen": "127.0.0.1", "protocol": "trojan", "settings": {"clients": [{"password": UUID}]}, "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/trojan-argo"}}, "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}}
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
        return [{"fileName": "web", "fileUrl": "https://arm.dogchild.eu.org/xray"}, {"fileName": "bot", "fileUrl": "https://arm.dogchild.eu.org/cloudflared"}]
    else:
        return [{"fileName": "web", "fileUrl": "https://amd.dogchild.eu.org/xray"}, {"fileName": "bot", "fileUrl": "https://amd.dogchild.eu.org/cloudflared"}]

async def download_file(file_name, file_url):
    file_path = Path(FILE_PATH) / file_name
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(file_url)
            response.raise_for_status()
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(response.content)
            print(f"Download {file_name} successfully")
            return True
    except Exception as e:
        print(f"Download {file_name} failed: {e}")
        return False

async def download_files_and_run():
    """下载web和bot二进制文件并设置执行权限"""
    architecture = get_system_architecture()
    all_files = get_files_for_architecture(architecture)
    if not all_files:
        print("Can't find files for current architecture")
        return False
    
    files_to_download = [f for f in all_files if not (Path(FILE_PATH) / f["fileName"]).exists()]
    if not files_to_download:
        print("All required files already exist, skipping download")
    else:
        results = await asyncio.gather(*[download_file(f["fileName"], f["fileUrl"]) for f in files_to_download])
        if not all(results):
            print("Error downloading files")
            return False
    
    # 设置可执行权限
    for file_name in ['web', 'bot']:
        file_path = Path(FILE_PATH) / file_name
        if file_path.exists():
            try:
                file_path.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
                print(f"Empowerment success for {file_path}: 775")
            except Exception as e:
                print(f"Empowerment failed for {file_path}: {e}")
    return True

async def start_web():
    web_path = Path(FILE_PATH) / 'web'
    config_path = Path(FILE_PATH) / 'config.json'
    try:
        process = await asyncio.create_subprocess_exec(
            str(web_path), '-c', str(config_path),
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(process)
        print('web is running')
        await asyncio.sleep(1)
        return process
    except Exception as e:
        print(f"web running error: {e}")
        return None

def setup_bot_config():
    """为固定bot设置配置文件(bot.json和bot.yml)"""
    if not ARGO_AUTH or 'TunnelSecret' not in ARGO_AUTH:
        return
    try:
        auth_data = json.loads(ARGO_AUTH)
        bot_json_path = Path(FILE_PATH) / 'bot.json'
        with open(bot_json_path, 'w') as f:
            json.dump(auth_data, f, indent=2)
        
        bot_id = auth_data.get('TunnelID') or next((k for k in auth_data.keys() if len(k) > 30), list(auth_data.keys())[0])
        bot_yml_content = f"""tunnel: {bot_id}
credentials-file: {bot_json_path}
protocol: http2

ingress:
  - hostname: {ARGO_DOMAIN}
    service: http://localhost:{ARGO_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
"""
        with open(Path(FILE_PATH) / 'bot.yml', 'w') as f:
            f.write(bot_yml_content)
    except Exception as e:
        print(f"Error setting up bot config: {e}")

async def start_bot():
    """启动bot服务，支持token、json配置和临时隧道三种模式"""
    bot_path = Path(FILE_PATH) / 'bot'
    if not bot_path.exists():
        print("Bot binary not found")
        return None
    
    # 根据ARGO_AUTH类型选择启动参数
    if ARGO_AUTH and re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):  # Token模式
        args = ['tunnel', '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', 'run', '--token', ARGO_AUTH]
    elif ARGO_AUTH and 'TunnelSecret' in ARGO_AUTH:  # JSON配置模式
        setup_bot_config()
        args = ['tunnel', '--edge-ip-version', 'auto', '--config', str(Path(FILE_PATH) / 'bot.yml'), 'run']
    else:  # 临时隧道模式
        args = ['tunnel', '--edge-ip-version', 'auto', '--no-autoupdate', '--protocol', 'http2', '--logfile', str(Path(FILE_PATH) / 'boot.log'), '--loglevel', 'info', '--url', f'http://localhost:{ARGO_PORT}']
    
    try:
        process = await asyncio.create_subprocess_exec(str(bot_path), *args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        running_processes.append(process)
        print('bot is running')
        await asyncio.sleep(2)
        return process
    except Exception as e:
        print(f"Error executing bot: {e}")
        return None

async def extract_domains():
    """提取隧道域名，优先使用固定域名，否则从日志中解析临时域名"""
    global current_domain
    if ARGO_AUTH and ARGO_DOMAIN:
        current_domain = ARGO_DOMAIN
        print(f'ARGO_DOMAIN: {current_domain}')
        return current_domain
    
    # 从boot.log中提取临时域名
    boot_log_path = Path(FILE_PATH) / 'boot.log'
    for attempt in range(15):
        try:
            if boot_log_path.exists():
                async with aiofiles.open(boot_log_path, 'r') as f:
                    content = await f.read()
                matches = re.findall(r'https?://([^\s]*trycloudflare\.com)/?', content)
                if matches:
                    current_domain = matches[0]
                    print(f'ArgoDomain: {current_domain}')
                    return current_domain
        except:
            pass
        await asyncio.sleep(2)
    print('ArgoDomain not found, re-running bot to obtain ArgoDomain')
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

async def generate_links(argo_domain):
    """生成VLESS、VMess、Trojan订阅链接并保存为Base64编码"""
    global current_subscription
    try:
        isp = await get_isp_info()
        vless_link = f"vless://{UUID}@{CFIP}:{CFPORT}?encryption=none&security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Fvless-argo%3Fed%3D2560#{NAME}-{isp}-vl"
        vmess_config = {'v': '2', 'ps': f'{NAME}-{isp}-vm', 'add': CFIP, 'port': CFPORT, 'id': UUID, 'aid': '0', 'scy': 'none', 'net': 'ws', 'type': 'none', 'host': argo_domain, 'path': '/vmess-argo?ed=2560', 'tls': 'tls', 'sni': argo_domain, 'alpn': ''}
        vmess_link = f"vmess://{base64.b64encode(json.dumps(vmess_config).encode()).decode()}"
        trojan_link = f"trojan://{UUID}@{CFIP}:{CFPORT}?security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Ftrojan-argo%3Fed%3D2560#{NAME}-{isp}-tr"
        
        sub_content = f"{vless_link}\n\n{vmess_link}\n\n{trojan_link}\n"
        current_subscription = base64.b64encode(sub_content.encode()).decode()
        
        async with aiofiles.open(Path(FILE_PATH) / 'sub.txt', 'w') as f:
            await f.write(current_subscription)
        
        print(f"{Path(FILE_PATH) / 'sub.txt'} saved successfully")
        print(current_subscription[:100] + "..." if len(current_subscription) > 100 else current_subscription)
        return current_subscription
    except Exception as e:
        print(f"Error generating subscription: {e}")
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

def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}, shutting down...")
    asyncio.create_task(cleanup_processes())
    sys.exit(0)

async def start_server():
    print("=" * 60)
    print("Python-Argo-X - Cloudflare Argo隧道代理工具")
    print("原作者: dogchild | Python重写版本")
    print("=" * 60)
    
    create_directory()
    cleanup_old_files()
    generate_web_config()
    
    if not await download_files_and_run():
        print("Failed to download required files")
        return
    
    web_process = await start_web()
    if not web_process:
        print("Failed to start web")
        return
    
    bot_process = await start_bot()
    if not bot_process:
        print("Failed to start bot")
        return
    
    await asyncio.sleep(5)
    domain = await extract_domains()
    if not domain:
        print("Failed to extract domain")
        return
    
    await generate_links(domain)
    
    print(f"\nService started successfully!")
    print(f"Port: {PORT}")
    print(f"Subscription URL: http://localhost:{PORT}/{SUB_PATH}")
    print(f"Domain: {domain}")
    print("=" * 60)
    
    config = uvicorn.Config(app=app, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # 设置信号处理
    if sys.platform != 'win32':
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    else:
        signal.signal(signal.SIGINT, signal_handler)
    
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Program exited")