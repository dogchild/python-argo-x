#!/usr/bin/env node

require('dotenv').config({ override: true });
const express = require("express");
const app = express();
const axios = require("axios");
const os = require('os');
const fs = require("fs");
const path = require("path");
const { promisify } = require('util');
const exec = promisify(require('child_process').exec);
const { execSync } = require('child_process');
const FILE_PATH = process.env.FILE_PATH || './tmp';   // 运行目录,sub节点文件保存目录
const SUB_PATH = process.env.SUB_PATH || 'sub';       // 订阅路径
const PORT = process.env.SERVER_PORT || process.env.PORT || 3005;        // http服务订阅端口
const UUID = process.env.UUID || '75de94bb-b5cb-4ad4-b72b-251476b36f3a'; // 用户UUID
const ARGO_DOMAIN = process.env.ARGO_DOMAIN || '';          // 固定隧道域名,留空即启用临时隧道
const ARGO_AUTH = process.env.ARGO_AUTH || '';              // 固定隧道密钥json或token,留空即启用临时隧道,json获取地址：https://fscarmen.cloudflare.now.cc
const ARGO_PORT = process.env.ARGO_PORT || 8001;            // 固定隧道端口,使用token需在cloudflare后台设置和这里一致
const CFIP = process.env.CFIP || 'cf.877774.xyz';         // 节点优选域名或优选ip  
const CFPORT = process.env.CFPORT || 443;                   // 节点优选域名或优选ip对应的端口
const NAME = process.env.NAME || 'Vls';                     // 节点名称

//创建运行文件夹
if (!fs.existsSync(FILE_PATH)) {
  fs.mkdirSync(FILE_PATH);
  console.log(`${FILE_PATH} is created`);
} else {
  console.log(`${FILE_PATH} already exists`);
}

let webPath = path.join(FILE_PATH, 'web');
let botPath = path.join(FILE_PATH, 'bot');
let subPath = path.join(FILE_PATH, 'sub.txt');
let bootLogPath = path.join(FILE_PATH, 'boot.log');
let configPath = path.join(FILE_PATH, 'config.json');

//清理历史文件
function cleanupOldFiles() {
  const pathsToDelete = ['sub.txt', 'boot.log'];
  pathsToDelete.forEach(file => {
    const filePath = path.join(FILE_PATH, file);
    fs.unlink(filePath, () => {});
  });
}

// 根路由
app.get("/", function(req, res) {
  res.send("Hello world!");
});

// 生成xr-ay配置文件
const config = {
  log: { access: '/dev/null', error: '/dev/null', loglevel: 'none' },
  inbounds: [
    { port: ARGO_PORT, protocol: 'vless', settings: { clients: [{ id: UUID, flow: 'xtls-rprx-vision' }], decryption: 'none', fallbacks: [{ dest: 3001 }, { path: "/vless-argo", dest: 3002 }, { path: "/vmess-argo", dest: 3003 }, { path: "/trojan-argo", dest: 3004 }] }, streamSettings: { network: 'tcp' } },
    { port: 3001, listen: "127.0.0.1", protocol: "vless", settings: { clients: [{ id: UUID }], decryption: "none" }, streamSettings: { network: "tcp", security: "none" } },
    { port: 3002, listen: "127.0.0.1", protocol: "vless", settings: { clients: [{ id: UUID, level: 0 }], decryption: "none" }, streamSettings: { network: "ws", security: "none", wsSettings: { path: "/vless-argo" } }, sniffing: { enabled: true, destOverride: ["http", "tls", "quic"], metadataOnly: false } },
    { port: 3003, listen: "127.0.0.1", protocol: "vmess", settings: { clients: [{ id: UUID, alterId: 0 }] }, streamSettings: { network: "ws", wsSettings: { path: "/vmess-argo" } }, sniffing: { enabled: true, destOverride: ["http", "tls", "quic"], metadataOnly: false } },
    { port: 3004, listen: "127.0.0.1", protocol: "trojan", settings: { clients: [{ password: UUID }] }, streamSettings: { network: "ws", security: "none", wsSettings: { path: "/trojan-argo" } }, sniffing: { enabled: true, destOverride: ["http", "tls", "quic"], metadataOnly: false } },
  ],
  dns: { servers: ["https+local://8.8.8.8/dns-query"] },
  outbounds: [ { protocol: "freedom", tag: "direct" }, {protocol: "blackhole", tag: "block"} ]
};
fs.writeFileSync(path.join(FILE_PATH, 'config.json'), JSON.stringify(config, null, 2));

// 判断系统架构
function getSystemArchitecture() {
  const arch = os.arch();
  if (arch === 'arm' || arch === 'arm64' || arch === 'aarch64') {
    return 'arm';
  } else {
    return 'amd';
  }
}

// 下载对应系统架构的依赖文件
function downloadFile(fileName, fileUrl, callback) {
  const filePath = path.join(FILE_PATH, fileName);
  const writer = fs.createWriteStream(filePath);

  axios({
    method: 'get',
    url: fileUrl,
    responseType: 'stream',
  })
    .then(response => {
      response.data.pipe(writer);

      writer.on('finish', () => {
        writer.close();
        console.log(`Download ${fileName} successfully`);
        callback(null, fileName);
      });

      writer.on('error', err => {
        fs.unlink(filePath, () => { });
        const errorMessage = `Download ${fileName} failed: ${err.message}`;
        console.error(errorMessage); // 下载失败时输出错误消息
        callback(errorMessage);
      });
    })
    .catch(err => {
      const errorMessage = `Download ${fileName} failed: ${err.message}`;
      console.error(errorMessage); // 下载失败时输出错误消息
      callback(errorMessage);
    });
}

// 下载并运行依赖文件
async function downloadFilesAndRun() {
  const architecture = getSystemArchitecture();
  const allFiles = getFilesForArchitecture(architecture);

  if (allFiles.length === 0) {
    console.log(`Can't find a file for the current architecture`);
    return;
  }

  // 过滤掉已存在的文件，只下载不存在的文件
  const filesToDownload = allFiles.filter(fileInfo => {
    const filePath = path.join(FILE_PATH, fileInfo.fileName);
    const exists = fs.existsSync(filePath);
    if (exists) {
      console.log(`${fileInfo.fileName} already exists, skipping download`);
    }
    return !exists;
  });

  if (filesToDownload.length === 0) {
    console.log('All required files already exist, skipping download');
  }

  const downloadPromises = filesToDownload.map(fileInfo => {
    return new Promise((resolve, reject) => {
      downloadFile(fileInfo.fileName, fileInfo.fileUrl, (err, fileName) => {
        if (err) {
          reject(err);
        } else {
          resolve(fileName);
        }
      });
    });
  });

  try {
    await Promise.all(downloadPromises);
  } catch (err) {
    console.error('Error downloading files:', err);
    return;
  }
  // 授权和运行
  function authorizeFiles(filePaths) {
    const newPermissions = 0o775;
    filePaths.forEach(relativeFilePath => {
      const absoluteFilePath = path.join(FILE_PATH, relativeFilePath);
      if (fs.existsSync(absoluteFilePath)) {
        fs.chmod(absoluteFilePath, newPermissions, (err) => {
          if (err) {
            console.error(`Empowerment failed for ${absoluteFilePath}: ${err}`);
          } else {
            console.log(`Empowerment success for ${absoluteFilePath}: ${newPermissions.toString(8)}`);
          }
        });
      }
    });
  }
  
  const filesToAuthorize = ['./web', './bot'];
  authorizeFiles(filesToAuthorize);

  //运行xr-ay
  const command1 = `nohup ${FILE_PATH}/web -c ${FILE_PATH}/config.json >/dev/null 2>&1 &`;
  try {
    await exec(command1);
    console.log('web is running');
    await new Promise((resolve) => setTimeout(resolve, 1000));
  } catch (error) {
    console.error(`web running error: ${error}`);
  }

  // 运行cloud-fared
  if (fs.existsSync(path.join(FILE_PATH, 'bot'))) {
    let args;

    if (ARGO_AUTH.match(/^[A-Z0-9a-z=]{120,250}$/)) {
      args = `tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token ${ARGO_AUTH}`;
    } else if (ARGO_AUTH.match(/TunnelSecret/)) {
      args = `tunnel --edge-ip-version auto --config ${FILE_PATH}/tunnel.yml run`;
    } else {
      args = `tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile ${FILE_PATH}/boot.log --loglevel info --url http://localhost:${ARGO_PORT}`;
    }

    try {
      await exec(`nohup ${FILE_PATH}/bot ${args} >/dev/null 2>&1 &`);
      console.log('bot is running');
      await new Promise((resolve) => setTimeout(resolve, 2000));
    } catch (error) {
      console.error(`Error executing command: ${error}`);
    }
  }
  await new Promise((resolve) => setTimeout(resolve, 5000));

}

//根据系统架构返回对应的url
function getFilesForArchitecture(architecture) {
  let baseFiles;
  if (architecture === 'arm') {
    baseFiles = [
      { fileName: "web", fileUrl: "https://arm.dogchild.eu.org/xray" },
      { fileName: "bot", fileUrl: "https://arm.dogchild.eu.org/cloudflared" }
    ];
  } else {
    baseFiles = [
      { fileName: "web", fileUrl: "https://amd.dogchild.eu.org/xray" },
      { fileName: "bot", fileUrl: "https://amd.dogchild.eu.org/cloudflared" }
    ];
  }

  return baseFiles;
}

// 获取固定隧道json
function argoType() {
  if (!ARGO_AUTH || !ARGO_DOMAIN) {
    console.log("ARGO_DOMAIN or ARGO_AUTH variable is empty, use quick tunnels");
    return;
  }

  if (ARGO_AUTH.includes('TunnelSecret')) {
    fs.writeFileSync(path.join(FILE_PATH, 'tunnel.json'), ARGO_AUTH);
    const tunnelYaml = `
  tunnel: ${ARGO_AUTH.split('"')[11]}
  credentials-file: ${path.join(FILE_PATH, 'tunnel.json')}
  protocol: http2
  
  ingress:
    - hostname: ${ARGO_DOMAIN}
      service: http://localhost:${ARGO_PORT}
      originRequest:
        noTLSVerify: true
    - service: http_status:404
  `;
    fs.writeFileSync(path.join(FILE_PATH, 'tunnel.yml'), tunnelYaml);
  } else {
    console.log("ARGO_AUTH mismatch TunnelSecret,use token connect to tunnel");
  }
}
argoType();

// 获取临时隧道domain
async function extractDomains() {
  let argoDomain;

  if (ARGO_AUTH && ARGO_DOMAIN) {
    argoDomain = ARGO_DOMAIN;
    console.log('ARGO_DOMAIN:', argoDomain);
    await generateLinks(argoDomain);
  } else {
    try {
      const fileContent = fs.readFileSync(path.join(FILE_PATH, 'boot.log'), 'utf-8');
      const lines = fileContent.split('\n');
      const argoDomains = [];
      lines.forEach((line) => {
        const domainMatch = line.match(/https?:\/\/([^ ]*trycloudflare\.com)\/?/);
        if (domainMatch) {
          const domain = domainMatch[1];
          argoDomains.push(domain);
        }
      });

      if (argoDomains.length > 0) {
        argoDomain = argoDomains[0];
        console.log('ArgoDomain:', argoDomain);
        await generateLinks(argoDomain);
      } else {
        console.log('ArgoDomain not found, re-running bot to obtain ArgoDomain');
        // 删除 boot.log 文件，等待 2s 重新运行 server 以获取 ArgoDomain
        fs.unlinkSync(path.join(FILE_PATH, 'boot.log'));
        async function killBotProcess() {
          try {
            await exec('pkill -f "[b]ot" > /dev/null 2>&1');
          } catch (error) {
            // 忽略输出
          }
        }
        killBotProcess();
        await new Promise((resolve) => setTimeout(resolve, 3000));
        const args = `tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile ${FILE_PATH}/boot.log --loglevel info --url http://localhost:${ARGO_PORT}`;
        try {
          await exec(`nohup ${path.join(FILE_PATH, 'bot')} ${args} >/dev/null 2>&1 &`);
          console.log('bot is running.');
          await new Promise((resolve) => setTimeout(resolve, 3000));
          await extractDomains(); // 重新提取域名
        } catch (error) {
          console.error(`Error executing command: ${error}`);
        }
      }
    } catch (error) {
      console.error('Error reading boot.log:', error);
    }
  }

  // 生成 sub 信息
  async function generateLinks(argoDomain) {
    let ISP = '';
    try {
      const response = await axios.get('https://speed.cloudflare.com/meta');
      const data = response.data;
      // 使用从JSON数据中提取的字段构建ISP信息
      ISP = `${data.country}-${data.asOrganization}`.replace(/\s/g, '_');
    } catch (error) {
      console.error('Error fetching Cloudflare meta data:', error);
      ISP = 'Unknown-ISP'; // 提供默认值以防止程序崩溃
    }

    return new Promise((resolve) => {
      setTimeout(() => {
        const VMESS = { v: '2', ps: `${NAME}-${ISP}-vm`, add: CFIP, port: CFPORT, id: UUID, aid: '0', scy: 'none', net: 'ws', type: 'none', host: argoDomain, path: '/vmess-argo?ed=2560', tls: 'tls', sni: argoDomain, alpn: '' };
        const subTxt = `
vless://${UUID}@${CFIP}:${CFPORT}?encryption=none&security=tls&sni=${argoDomain}&type=ws&host=${argoDomain}&path=%2Fvless-argo%3Fed%3D2560#${NAME}-${ISP}-vl
  
vmess://${Buffer.from(JSON.stringify(VMESS)).toString('base64')}
  
trojan://${UUID}@${CFIP}:${CFPORT}?security=tls&sni=${argoDomain}&type=ws&host=${argoDomain}&path=%2Ftrojan-argo%3Fed%3D2560#${NAME}-${ISP}-tr
    `;
        // 打印 sub.txt 内容到控制台
        console.log(Buffer.from(subTxt).toString('base64'));
        fs.writeFileSync(subPath, Buffer.from(subTxt).toString('base64'));
        console.log(`${FILE_PATH}/sub.txt saved successfully`);
        // 将内容进行 base64 编码并写入 SUB_PATH 路由
        app.get(`/${SUB_PATH}`, (req, res) => {
          const encodedContent = Buffer.from(subTxt).toString('base64');
          res.set('Content-Type', 'text/plain; charset=utf-8');
          res.send(encodedContent);
        });
        resolve(subTxt);
      }, 2000);
    });
  }
}



// 回调运行
async function startserver() {
  cleanupOldFiles();
  await downloadFilesAndRun();
  await extractDomains();
}
startserver();

app.listen(PORT, () => console.log(`http server is running on port:${PORT}!`));
