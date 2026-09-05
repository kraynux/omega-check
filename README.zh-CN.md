<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（见 LICENSE 文件） -->
<div align="center">
  <img src="docs/assets/omega-check.png" alt="Omega-Check" width="256">
</div>

#  OMEGA-CHECK

**单目标网络端口、服务和角色扫描器**

> 由 **kraynux** 为 **Omega-server** 开发  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

官方页面：[OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; 预览：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**语言：**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-check** 是一个 TUI + CLI 工具，用于扫描单个网络目标的端口，识别每个开放端口上运行的服务（协议、软件、版本、身份验证、WAF、TLS），并推断其可能的角色，但绝不执行主动攻击。它是 `omega-` 套件中的第四个工具（继 `omega-fire`、`omega-stress` 和 `omega-scan` 之后），采用 Clean Architecture 组织；完整技术说明请参阅 `docs/ARCHITECTURE.md`。

## 1. 愿景与范围

Omega-check 是面向系统管理的端口扫描器：用于快速检查一台机器（本机、LAN 主机或已授权的外部目标）上有哪些端口正在监听、运行什么服务，以及每条信息可以获得多大程度的信任。

### Omega-check 的功能

- 在单个目标上扫描端口列表（系统配置文件、个人配置文件或自由输入）。
- 识别每个开放端口上的服务：协议（HTTP/HTTPS/SSH/TLS/VNC/通用）、公开的软件和版本（如果可见）以及身份验证要求。
- 根据**实际协商的协议**推断可能角色（Web 服务器、Shell 访问、图形访问、数据库），而不是简单依据端口号猜测。
- 当请求头声明存在时，检测已知 WAF 特征（Cloudflare、Sucuri、Akamai、Imperva Incapsula）。
- 通过 Textual TUI 或可脚本化 CLI 输出结果，并提供 JSON、文本和 HTML（5 种主题）三种导出格式。
- 为每条收集的信息标记明确的可信度等级；参阅[§7](#7-可信度策略)。
- 持久化保存扫描历史，支持随时间重放和比较。
- 支持固定目标以及可在不同扫描中复用的个人端口配置文件。

### Omega-check 不做什么

- 不执行主动漏洞扫描，不检测 SQLi、XSS 或 RCE。
- 不扫描 CVE。
- 不进行操作系统指纹识别（数据模型包含该字段，但目前没有启用填充它的启发式规则）。
- 不使用类似 nmap 的低级扫描技术（SYN 扫描、原始数据包），只使用应用层 TCP 连接。
- 不是暴力破解或模糊测试工具。
- 不执行并行多目标扫描。
- 不提供 Web 控制面板。

## 2. 安装

### 前置要求

- Python 3.10+
- 用于安装依赖的 Internet 连接

### 安装

```bash
[ -d omega-check ] && echo "ℹ️ 已在此处解压，跳过该步骤。" || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh` 会：

1. 在不存在时创建 `.venv` 虚拟环境。
2. 安装依赖（`pip install -e .`；`pyproject.toml` 仍是唯一可信来源）。
3. 为 `omega-check.sh` 和 `install.sh` 添加执行权限。
4. 将 `check` 别名添加到 `~/.bashrc` 和 `~/.zshrc`，如果已存在则不会重复添加。

### 依赖

依赖声明位于 `pyproject.toml` 中（不再使用 `requirements.txt`）：
- `omega-lib`：套件共享库（`ConfidenceLevel`、主题和终端检测）。
- `textual`：TUI、主题和终端自动适配。
- `httpx`：HTTP/HTTPS 探测。
- `cryptography`：读取协商得到的 TLS 证书。
- `jinja2`：HTML 导出模板。
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`。

## 3. 使用方法

### 交互模式（TUI）

推荐日常使用，直接无参数启动：

```bash
./omega-check.sh
```

如果已创建别名，也可以直接在终端中输入：

```bash
check
```

操作流程：启动画面（按键或单击关闭）→ 主菜单（扫描器 / 目标 / 配置文件 / 历史 / 设置 / 帮助）→ 输入目标（可从固定目标选择器中选择）并选择配置文件（`complet` 会显示警告；个人配置文件使用第二个字段；使用 `CUSTOM` 时可自由输入端口）→ 扫描（显示不确定进度和实时网络操作）→ 扫描详情（端口/服务/角色、导出）→ 从主菜单访问历史、比较、重放和设置。终端适配（颜色、尺寸和结构降级）会自动完成。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏幕（在首页确认退出） |
| `t` | 切换到下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需要确认） |

### 可脚本化模式（CLI）

任何子命令都会启动 CLI：

```bash
# 使用端口配置文件扫描目标
./omega-check.sh scan 192.168.1.10 --profile minimal

# 历史（可按目标过滤）
./omega-check.sh history --target 192.168.1.10 --limit 20

# 扫描详情（文本、JSON 或 HTML），可选择 5 种导出主题
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# 比较两次扫描（端口状态变化）
./omega-check.sh compare <scan_id_a> <scan_id_b>

# 个人端口配置文件
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "我的配置文件"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### 支持的目标格式

```text
192.168.1.10                IPv4
example.org                 主机名
http://example.org          HTTP URL（解析前移除协议）
https://example.org:8443    带端口的 HTTPS URL（移除协议和端口）
```

在 DNS 解析前会移除协议和可能存在的端口（`domain/targets/validation.py::normalize_target_input`）：可以粘贴完整 URL，最终只保留主机。

## 4. 扫描配置文件

| 配置文件 | 描述 | 已固定 |
|---|---|---|
| `minimal` | 超快速扫描：SSH + HTTP + HTTPS（22、80、443） | 是 |
| `classic` | 经典 Internet/LAN 服务（37 个端口） | 是 |
| `web` | Web 服务和替代端口 | 否 |
| `db` | 数据库和数据服务 | 否 |
| `remote` | 远程访问：Shell、桌面和 RustDesk | 否 |
| `mail` | 邮件服务 | 否 |
| `dns` | DNS 服务 | 否 |
| `iot` | IoT 设备、摄像头、网关和智能家居 | 否 |
| `dev` | 开发和实验环境 | 否 |
| `docker` | Docker、Swarm 和常见容器服务 | 否 |
| `complet` | **动态生成**：上述所有配置文件的排序去重并集 | 否 |
| `CUSTOM` | 在**配置文件**中创建的个人配置文件和/或自由输入（`80` / `22,443,8080` / `1000-2000`）；两者会合并并去重 | 否 |

完整说明、验证规则和个人配置文件管理见：`docs/PROFILES.md`。

## 5. 架构

Omega-check 采用 **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared）组织，与 `omega-` 套件模板保持一致（参阅 `omega-scan`/`omega-stress`），并在每次修改后通过 `import-linter` 验证。完整说明位于 **`docs/ARCHITECTURE.md`**。

```text
src/omega_check/
├── domain/          纯业务逻辑（扫描、目标、服务、配置文件、报告……）
├── application/     用例（commands/queries）
├── ports/           应用所需契约（probers、repositories、exporters……）
├── infrastructure/  具体实现（socket/httpx/cryptography、SQLite；Textual 不在此处）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），功能严格对等
├── app/             组装（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   跨领域词汇和非业务工具
└── plugins/         已建立但为空的结构（尚无确认的扩展方向）
```

设计规则：
- `domain/services/policies.py`：对已收集的线索进行分类，从不执行网络操作。
- `infrastructure/network/`：执行网络操作（sockets、`httpx`、`cryptography`），但从不做判断。
- `interfaces/`：显示数据，不包含业务逻辑。
- `infrastructure/exporters/`：读取扫描结果，不重新计算。

## 6. 服务与角色识别

### 检测的协议

| 协议 | 探测方式 | 收集的信息 |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` 横幅、认证请求头 |
| TLS | `cryptography`（协商证书，包括 `CERT_NONE`） | 版本、cipher、证书主题/颁发者 |
| SSH | 原始横幅 | 软件和版本（例如 `OpenSSH 10.4`） |
| VNC（RFB） | 服务器声明的安全代码 | 支持的认证类型 |
| 通用 | 对未识别开放端口读取原始横幅 | 谨慎提取，不使用激进启发式规则 |

### 推断的角色

角色依据**实际协商的协议**推断，而不是依据假定的端口号：

| 角色 | 条件 | 可信度 |
|---|---|---|
| `Web 服务器` | 已确认 HTTP/HTTPS 协议 | `INFERRED` |
| `Shell 访问` | 已确认 SSH 协议 | `CORROBORATED` |
| `图形访问` | 已确认 VNC 协议 | `CORROBORATED` |
| `数据库` | 端口属于系统 `db` 配置文件的范围 | `INFERRED` |

### 已知 WAF 特征

通过声明性请求头（`server`、`x-sdk`）检测；其存在由**目标自行声明**，从不独立验证：Cloudflare、Sucuri、Akamai、Imperva Incapsula、AWS ELB（仅作参考列出，严格来说不是应用 WAF）。

## 7. 可信度策略

每个收集到的字段都具有以下一种可信度等级：

| 等级 | 含义 |
|---|---|
| `VERIFIED` | 直接观察到且目标无法伪造的协议事实（例如由 TCP RST 确认的关闭端口，或实际协商的 TLS 版本）。 |
| `DECLARED` | 目标在完全由其控制的字段中自行声明的值（例如 `Server` 横幅）；看似合理，但可以随意伪造。 |
| `CORROBORATED` | 由独立信号确认的 `DECLARED` 值（例如实际协商出 SSH 协议后得到的 SSH 角色）。 |
| `INFERRED` | 根据模式或启发式规则推断，没有目标的明确声明。 |
| `UNKNOWN` | 没有可用证据，或目标主动隐藏了信息。 |

## 8. 防范伪造值

Omega-check 不会默认信任目标自行声明的数据，并会明确标示这一点。无论看起来多么合理，`Server` 横幅或 `X-Powered-By` 请求头都保持为 `DECLARED`，而不是 `VERIFIED`：这些信息由目标提供，也可以随意伪造。只有通过独立渠道确认（例如“Shell 访问”角色对应的 SSH 协议确实完成协商）才能将信息提升为 `CORROBORATED`。这一由 `omega-lib`（`ConfidenceLevel`）承载的区别是结构性的，任何导出或界面都无法隐藏它。

## 9. 终端兼容性

Textual TUI 会自动检测终端能力（模拟器和尺寸），并相应调整结构化样式（`complete`/`standard`/`reduced`/`mono`），无需手动参数。CLI 始终使用纯文本，与终端无关。该策略由整个 `omega-` 套件共享（`omega-lib`、`terminal/policies.py`）。

### 按模拟器确定配置

| 模拟器 | 初始配置 |
|---|---|
| Ghostty、Alacritty、WezTerm、Kitty | `complete` |
| Konsole、GNOME Terminal、Terminator、Xfce4 Terminal | `standard` |
| xterm、urxvt、现代 SSH | `reduced` |
| Linux TTY、旧版 SSH | `mono` |
| 未识别的模拟器 | `reduced`（默认回退） |

### 按终端尺寸确定配置

| 最小尺寸（列 × 行） | 配置上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 更小 | `mono` |

最终配置取两个条件（模拟器和尺寸）中**限制最严格的一个**。例如，Ghostty 即使允许 `complete`，当窗口缩小到 70 列时也会降级为 `mono`。可以使用 `r` 键实时刷新。

## 10. 导出

报告默认生成在 `var/exports/`（运行时路径以项目目录为基准，可通过 `$OMEGA_CHECK_VAR_DIR` 覆盖），也可以写入指定路径（CLI 使用 `--output`，TUI 使用对话框）。文件名明确并带时间戳：`scan-{profile}-{date}.ext`，个人配置文件使用 `scan-custom-{date}.ext`，无配置文件的自由输入使用 `scan-{date}.ext`。

### JSON，事实来源

完整的扫描结构（`Scan` + `Host`），严格可序列化为 JSON，并包含可信度等级。

### 文本，紧凑的人类可读报告

无需 ANSI 控制码，在终端之外也能阅读。

### HTML，独立 Web 报告

提供 5 种主题（CLI 使用 `--theme`，TUI 使用选择器；如果存在对应主题，默认跟随当前界面主题）。专用布局包含信息网格、端口状态统计和彩色徽章，整体视觉风格与 `omega-scan`/`omega-stress` 保持一致。

## 11. 历史与比较

每次扫描都会保存到 SQLite（`var/db/omega-check.db`）：可以按目标查询历史、查看过去运行的详情、比较两次扫描（端口状态），并在无需重新输入目标的情况下重放同一目标的扫描。

## 12. 测试

```bash
source .venv/bin/activate
lint-imports        # 验证 Dependency Rule
pytest -q           # 173 个测试
ruff check src tests
mypy -p omega_check
```

目录结构：`tests/unit/`（领域和应用，无真实 I/O）、`tests/integration/`（SQLite/真实文件、`pytest-httpserver` 虚拟 HTTP 服务器、通过 `trustme` 提供 TLS）。

## 13. 不在范围内

- CVE 扫描。
- 主动检测 SQLi、XSS 和 RCE。
- 操作系统指纹识别。
- 类似 nmap 的低级扫描技术（SYN 扫描、原始数据包）。
- 爬取。
- 模糊测试。
- 暴力破解。
- 同时扫描多个目标。
- Web 控制面板。

---

> Omega-check —— 扫描、识别、评估、报告。  
> 具有明确可信度的端口扫描器，而不是把猜测伪装成事实。
