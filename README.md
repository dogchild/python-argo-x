<div align="center">

# nodejs-argo-x隧道代理

[![npm version](https://img.shields.io/npm/v/nodejs-argo-x.svg)](https://www.npmjs.com/package/nodejs-argo-x)
[![npm downloads](https://img.shields.io/npm/dm/nodejs-argo-x.svg)](https://www.npmjs.com/package/nodejs-argo-x)
[![License](https://img.shields.io/npm/l/nodejs-argo-x.svg)](https://github.com/eooce/nodejs-argo-x/blob/main/LICENSE)

nodejs-argo-x是一个强大的Argo隧道部署工具，专为PaaS平台和游戏玩具平台设计。它支持多种代理协议（VLESS、VMess、Trojan等）。

---

</div>

## 说明 （部署前请仔细阅读）

* 本项目是针对node环境的paas平台和游戏玩具而生，采用Argo隧道部署节点。
* node玩具平台只需上传index.js和package.json即可，paas平台需要docker部署的才上传Dockerfile。
* 不填写ARGO_DOMAIN和ARGO_AUTH两个变量即启用临时隧道，反之则使用固定隧道。

## 📋 环境变量

| 变量名 | 是否必须 | 默认值 | 说明 |
|--------|----------|--------|------|
| PORT | 否 | 3005 | HTTP服务监听端口 |
| ARGO_PORT | 否 | 8001 | Argo隧道端口 |
| UUID | 否 | 75de94bb-b5cb-4ad4-b72b-251476b36f3a | 用户UUID |
| ARGO_DOMAIN | 否 | - | Argo固定隧道域名 |
| ARGO_AUTH | 否 | - | Argo固定隧道密钥 |
| CFIP | 否 | cf.877774.xyz | 节点优选域名或IP |
| CFPORT | 否 | 443 | 节点端口 |
| NAME | 否 | Vls | 节点名称前缀 |
| FILE_PATH | 否 | ./tmp | 运行目录 |
| SUB_PATH | 否 | sub | 订阅路径 |

## 🌐 订阅地址

- 标准端口：`https://your-domain.com/sub`
- 非标端口：`http://your-domain.com:port/sub`

---

## 🚀 进阶使用

### 安装

```bash
# 全局安装（推荐）
npm install -g nodejs-argo-x

# 或者使用yarn
yarn global add nodejs-argo-x

# 或者使用pnpm
pnpm add -g nodejs-argo-x
```

### 基本使用

```bash
# 直接运行（使用默认配置）
nodejs-argo-x

# 使用npx运行
npx nodejs-argo-x

# 设置环境变量运行
PORT=3005 npx nodejs-argo-x
```

### 环境变量配置

可使用 `.env` 文件来配置环境变量运行


或者直接在命令行中设置：

```bash
export PORT=3005
export UUID="your-uuid-here"
```

## 📦 作为npm模块使用

```javascript
// CommonJS
const nodejsArgox = require('nodejs-argo-x');

// ES6 Modules
import nodejsArgox from 'nodejs-argo-x';

// 启动服务
nodejsArgox.start();
```

## 🔧 后台运行

### 使用screen（推荐）
```bash
# 创建screen会话
screen -S argo

# 运行应用
nodejs-argo-x

# 按 Ctrl+A 然后按 D 分离会话
# 重新连接：screen -r argo
```

### 使用tmux
```bash
# 创建tmux会话
tmux new-session -d -s argo

# 运行应用
tmux send-keys -t argo "nodejs-argo-x" Enter

# 分离会话：tmux detach -s argo
# 重新连接：tmux attach -t argo
```

### 使用PM2
```bash
# 安装PM2
npm install -g pm2

# 启动应用
pm2 start nodejs-argo-x --name "argo-service"

# 管理应用
pm2 status
pm2 logs argo-service
pm2 restart argo-service
```

### 使用systemd（Linux系统服务）
```bash
# 创建服务文件
sudo nano /etc/systemd/system/nodejs-argo-x.service

```
[Unit]
Description=Node.js Argo Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/test
Environment=ARGO_PORT=8001
Environment=PORT=3005
ExecStart=/usr/bin/npx nodejs-argo-x
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

# 启动服务
sudo systemctl start nodejs-argo-x
sudo systemctl enable nodejs-argo-x
```

## 🔄 更新

```bash
# 更新全局安装的包
npm update -g nodejs-argo-x

# 或者重新安装
npm uninstall -g nodejs-argo-x
npm install -g nodejs-argo-x
```

## 📚 更多信息

- [GitHub仓库](https://github.com/dogchild/nodejs-argo-x)
- [npm包页面](https://www.npmjs.com/package/nodejs-argo-x)
- [问题反馈](https://github.com/dogchild/nodejs-argo-x/issues)

---
  
# 免责声明
* 本程序仅供学习了解, 非盈利目的，请于下载后 24 小时内删除, 不得用作任何商业用途, 文字、数据及图片均有所属版权, 如转载须注明来源。
* 使用本程序必循遵守部署免责声明，使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责。
