# Python-Argo-X

通过 Cloudflare Argo 隧道提供 Xray 订阅链接的 Python 工具。这是原 [nodejs-argo-x](https://github.com/dogchild/nodejs-argo-x) 的 Python 重写版本，保持完全相同的功能特性。

## ✨ 特性

- 🐍 **纯 Python 实现** - 使用现代 Python 异步编程
- 🚀 **高性能异步** - 基于 asyncio 和 FastAPI 框架
- 🔄 **完全兼容** - 与原 Node.js 版本 API 完全兼容
- 🌐 **多协议支持** - VLESS、VMess、Trojan 三种协议
- 🔧 **灵活配置** - 支持临时隧道和固定隧道
- 📦 **容器化部署** - Docker 支持，适合 PaaS 平台
- 🔒 **安全可靠** - 自动处理进程管理和错误恢复
- 📊 **详细监控** - 进程状态监控和日志记录

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Linux/Windows/macOS

### 本地运行

1. **克隆项目**
   ```bash
   git clone https://github.com/dogchild/python-argo-x.git
   cd python-argo-x
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

### Docker 部署

1. **构建镜像**
   ```bash
   docker build -t python-argo-x .
   ```

2. **运行容器**
   ```bash
   docker run -d -p 3005:3005 \
     -e UUID=你的UUID \
     -e NAME=你的节点名称 \
     python-argo-x
   ```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `FILE_PATH` | `./tmp` | 运行目录，存储节点文件 |
| `SUB_PATH` | `sub` | 订阅路径 |
| `SERVER_PORT` / `PORT` | `3005` | HTTP 服务端口 |
| `UUID` | `75de94bb-b5cb-4ad4-b72b-251476b36f3a` | 用户 UUID |
| `ARGO_DOMAIN` | `` | 固定隧道域名，留空启用临时隧道 |
| `ARGO_AUTH` | `` | 固定隧道密钥，支持 JSON/Token 格式 |
| `ARGO_PORT` | `8001` | 固定隧道端口 |
| `CFIP` | `cf.877774.xyz` | 节点优选域名或 IP |
| `CFPORT` | `443` | 节点端口 |
| `NAME` | `Vls` | 节点名称前缀 |

### 隧道配置模式

#### 1. 临时隧道（默认）
```bash
# 不设置 ARGO_DOMAIN 和 ARGO_AUTH，自动生成临时域名
python main.py
```

#### 2. 固定隧道 - Token 认证
```bash
export ARGO_DOMAIN="your-domain.example.com"
export ARGO_AUTH="your-120-250-character-token"
python main.py
```

#### 3. 固定隧道 - JSON 认证
```bash
export ARGO_DOMAIN="your-domain.example.com" 
export ARGO_AUTH='{"TunnelSecret":"...","TunnelID":"..."}'
python main.py
```

## 📡 API 接口

### 基础接口

- `GET /` - 健康检查，返回 "Hello world!"
- `GET /health` - 健康状态检查
- `GET /info` - 服务信息查询  

### 订阅接口

- `GET /{SUB_PATH}` - 订阅服务，返回 Base64 编码的订阅内容
  - 默认路径：`/sub`
  - 响应格式：`text/plain`
  - 内容编码：Base64

### 使用示例

```bash
# 获取订阅链接
curl http://localhost:3005/sub

# 获取服务信息
curl http://localhost:3005/info
```

## 🔧 技术架构

### 核心模块

```
Python-Argo-X/
├── main.py                 # 主程序入口
├── config_manager.py       # 配置管理模块
├── architecture_detector.py # 系统架构检测
├── file_downloader.py      # 文件下载管理
├── process_manager.py      # 进程管理模块
├── tunnel_manager.py       # 隧道管理模块
├── subscription_service.py # 订阅服务模块
├── web_server.py           # Web 服务模块
└── requirements.txt        # Python 依赖
```

### 技术栈对比

| 组件 | Node.js 版本 | Python 版本 | 说明 |
|------|--------------|-------------|------|
| Web 框架 | Express | FastAPI | 现代异步 Web 框架 |
| HTTP 客户端 | axios | httpx | 支持异步 HTTP 请求 |
| 进程管理 | child_process | asyncio.subprocess | 异步进程管理 |
| 文件操作 | fs/path | pathlib + aiofiles | 异步文件 I/O |
| 异步处理 | async/await | asyncio | Python 内置异步 |

## 🔍 监控和调试

### 日志输出

程序运行时会输出详细的日志信息：

```
============================================================
Python-Argo-X v1.0.0 - Cloudflare Argo 隧道代理工具
原作者: dogchild | Python 重写版本
============================================================

🚀 开始初始化...
配置摘要:
- 运行目录: ./tmp
- 服务端口: 3005
- 订阅路径: /sub
- UUID: 75de94bb-b5cb-4ad4-b72b-251476b36f3a
- Argo 域名: 临时隧道
- 节点名称: Vls
- CF IP: cf.877774.xyz:443
```
  
## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/dogchild/python-argo-x.git
cd python-argo-x

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\\Scripts\\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

### 提交规范

- feat: 新功能
- fix: 修复 Bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 其他修改

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢原作者 [dogchild](https://github.com/dogchild) 的 [nodejs-argo-x](https://github.com/dogchild/nodejs-argo-x) 项目
- 感谢 Cloudflare 提供的 Argo 隧道服务
- 感谢 Xray 项目提供的代理核心

## 📞 支持

如果这个项目对你有帮助，请给个 ⭐ Star！

有问题可以通过以下方式联系：

- 📧 提交 [GitHub Issue](https://github.com/dogchild/python-argo-x/issues)
- 💬 参与 [GitHub Discussions](https://github.com/dogchild/python-argo-x/discussions)
