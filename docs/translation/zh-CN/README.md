<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（见 LICENSE 文件） -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**端口、服务与网络角色扫描器（单一目标）**

> 由 [kraynux](https://github.com/kraynux) 为 [Omega-Server](https://kraynux.snake-mackarel.ts.net) 打造   

官方页面：[OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; 截图：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 界面和导出的报告提供 **17 种语言** — 见[界面语言](#界面语言)。  
**语言：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** 是一个 TUI + CLI 工具，用于扫描单一网络目标的端口，识别每个开放端口上运行的服务（协议、软件、版本、认证、WAF、TLS）并推断其可能的角色，绝不进行任何主动攻击。它是 `omega-` 套件中的一个工具，采用 Clean Architecture 构建 — 完整技术细节见 `docs/ARCHITECTURE.md`。

## 1. 愿景与范围

Omega-check 是面向系统管理的端口扫描器：快速查看一台机器（你自己的、局域网内的，或经授权的外部目标）上在监听什么、用的是什么，以及每条信息可信到什么程度。

### Omega-check 能做什么

- 在单一目标上扫描一组端口（系统配置、个人配置或自由输入）。
- 识别每个开放端口上运行的服务：协议（HTTP/HTTPS/SSH/TLS/VNC/通用）、软件及其版本（若已暴露）、是否需要认证。
- 根据实际协商的协议推断可能的角色（Web 服务器、Shell 访问、图形访问、数据库），绝不仅凭端口号猜测。
- 当响应头中声明了已知 WAF 签名（Cloudflare、Sucuri、Akamai、Imperva Incapsula）时将其检测出来。
- 在 TUI（Textual）或可脚本化的 CLI 中呈现结果，并提供三种导出：JSON、文本、HTML（5 种主题）。
- 为收集到的每条信息标注明确的可信度 — 见 [§7](#7-可信度策略)。
- 保留持久的扫描历史，可重放，并可随时间对比。
- 可以固定目标并创建个人端口配置，在多次扫描之间重复使用。

### Omega-check 不做什么

- 主动漏洞扫描：不做 SQLi、XSS 或 RCE。
- CVE 扫描。
- 操作系统指纹识别（数据模型预留了该字段，目前没有任何启发式规则填写它）。
- nmap 式的底层扫描技术（SYN 扫描、原始数据包）— 仅使用应用层 TCP 连接。
- 暴力破解或模糊测试工具。
- 多目标并行扫描。
- Web 仪表盘。

## 2. 安装

### 前提条件

- Python 3.10+
- 互联网连接，用于安装依赖

### 安装

```bash
[ -d omega-check ] && echo "ℹ️ 此处已解压，跳过此步骤。" || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`：

1. 如果虚拟环境 `.venv` 尚不存在，则创建它。
2. 安装依赖（`pip install -e .`；`pyproject.toml` 仍是唯一的权威来源）。
3. 使 `omega-check.sh` 和 `install.sh` 可执行。
4. 将别名 `check` 添加到 `~/.bashrc` 和 `~/.zshrc`（已存在时不会重复添加）。

### 依赖

在 `pyproject.toml` 中声明（不再有 `requirements.txt`）：
- `omega-lib`：套件的共享库（`ConfidenceLevel`、主题、终端检测）
- `textual`：TUI 界面、主题、自动适配终端
- `httpx`：HTTP/HTTPS 探测
- `cryptography`：读取协商得到的 TLS 证书
- `jinja2`：HTML 导出的模板
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`

## 3. 使用

### 交互模式（TUI）

推荐日常使用 — 不带参数启动：

```bash
./omega-check.sh
```
如果已创建别名，只需在终端输入 `check`：
```bash
check
```

流程：启动画面（按任意键或点击关闭）→ 主菜单（扫描 / 目标 / 配置 / 历史 / 设置 / 帮助）→ 输入目标（可从已固定目标中选择）并选择配置（选择 `complet` 时会有警告；选择 `CUSTOM` 时出现第二个字段，用于个人配置或自由输入端口）→ 扫描（不确定进度条和实时网络操作日志）→ 扫描详情（端口/服务/角色、导出）→ 从主菜单进入历史/对比/重放和设置。对终端的适配（颜色、尺寸、结构降级）是自动的。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏（在主屏上会确认是否退出） |
| `t` | 下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需确认） |

### 界面语言

界面提供 17 种语言：法语、英语、西班牙语、葡萄牙语（巴西）、意大利语、德语、荷兰语、波兰语、俄语、简体中文、越南语、泰语、印尼语、日语、韩语、印地语和阿拉伯语。在设置中选择（“Langue / Language”），重启界面后生效；变量 `OMEGA_CHECK_LANG`（例如 `OMEGA_CHECK_LANG=zh-CN ./omega-check.sh`）可在一次会话中强制使用某种语言。从 omega-suite 启动时，omega-check 使用套件的语言。在 Linux 文本控制台（TTY）上，非拉丁文字的语言在本次会话中以英语显示。命令行保持法语。

### 脚本模式（CLI）

任何子命令都会进入 CLI 模式：

```bash
# 用某个端口配置扫描目标
./omega-check.sh scan 192.168.1.10 --profile minimal

# 历史（可按目标筛选）
./omega-check.sh history --target 192.168.1.10 --limit 20

# 扫描详情（文本、JSON 或 HTML）— 5 种导出主题可选
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# 对比两次扫描（端口状态变化）
./omega-check.sh compare <scan_id_a> <scan_id_b>

# 个人端口配置
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "我的配置"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### 可接受的目标格式

```text
192.168.1.10                IPv4
example.org                 主机名
http://example.org          HTTP URL（解析前去掉协议）
https://example.org:8443    带端口的 HTTPS URL（去掉协议和端口）
```

协议和端口（如有）会在 DNS 解析前去掉（`domain/targets/validation.py::normalize_target_input`）— 粘贴完整 URL 也能用，只保留主机部分。

## 4. 扫描配置

| 配置 | 说明 | 已固定 |
|---|---|---|
| `minimal` | 超快速扫描：SSH + HTTP + HTTPS（22、80、443） | 是 |
| `classic` | 常见的互联网/局域网服务（37 个端口） | 是 |
| `web` | Web 服务及备用端口 | 否 |
| `db` | 数据库和数据服务 | 否 |
| `remote` | 远程访问 — Shell、桌面、RustDesk | 否 |
| `mail` | 邮件服务 | 否 |
| `dns` | DNS 服务 | 否 |
| `iot` | 物联网设备、摄像头、路由器、智能家居 | 否 |
| `dev` | 开发/实验环境 | 否 |
| `docker` | Docker、Swarm 及常见容器化服务 | 否 |
| `complet` | **即时生成**：以上所有配置排序去重后的并集 | 否 |
| `CUSTOM` | 在**配置**屏幕中创建的个人配置，和/或自由输入（`80` / `22,443,8080` / `1000-2000`）— 两者合并并去重 | 否 |

完整细节、校验规则和个人配置的管理：`docs/PROFILES.md`。

## 5. 架构

Omega-check 采用 **Clean Architecture** 构建（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared），与 `omega-` 套件的模板保持一致（见 `omega-scan`/`omega-stress`），每次修改都由 `import-linter` 验证。完整细节见 **`docs/ARCHITECTURE.md`**。

非常简短的概览：

```text
src/omega_check/
├── domain/          纯业务逻辑（扫描、目标、服务、配置、报告……）
├── application/     用例（commands/queries）
├── ports/           应用所需的契约（探测器、仓储、导出器……）
├── infrastructure/  具体实现（socket/httpx/cryptography、SQLite；Textual 不在这里）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），功能严格对等
├── app/             装配（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   通用词汇、非业务工具
└── plugins/         结构已就位，为空（尚无确定的扩展方向）
```

设计规则：
- `domain/services/policies.py`：对已收集的线索进行分类，从不访问网络。
- `infrastructure/network/`：负责网络访问（套接字、`httpx`、`cryptography`），从不做判断。
- `interfaces/`：只负责显示，不包含任何业务逻辑。
- `infrastructure/exporters/`：读取扫描结果，不重新计算任何东西。

## 6. 服务识别与角色

### 检测的协议

| 协议 | 探测方式 | 收集的细节 |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` 横幅、认证相关响应头 |
| TLS | `cryptography`（协商得到的证书，包括 `CERT_NONE`） | 版本、加密套件、证书主体/颁发者 |
| SSH | 原始横幅 | 软件和版本（如 `OpenSSH 10.4`） |
| VNC (RFB) | 服务器公布的安全类型代码 | 支持的认证类型 |
| 通用 | 未识别开放端口上的原始横幅 | 谨慎提取，不使用激进的启发式规则 |

### 推断的角色

根据**实际协商**的协议推断，绝不凭端口号猜测：

| 角色 | 条件 | 可信度 |
|---|---|---|
| `Web 服务器` | 已确认 HTTP/HTTPS 协议 | `INFERRED` |
| `Shell 访问` | 已确认 SSH 协议 | `CORROBORATED` |
| `图形访问` | 已确认 VNC 协议 | `CORROBORATED` |
| `数据库` | 端口位于系统配置 `db` 的范围内 | `INFERRED` |

### 已知 WAF 签名

通过声明式响应头（`server`、`x-sdk`）检测 — 其存在**由目标自行声明**，从不进行独立验证：Cloudflare、Sucuri、Akamai、Imperva Incapsula、AWS ELB（仅作参考列出，严格来说不是应用层 WAF）。

## 7. 可信度策略

收集到的每个字段都带有以下级别之一：

| 级别 | 含义 |
|---|---|
| `VERIFIED` | 直接观察到的协议事实，目标无法伪造（如：由 TCP RST 确认的关闭端口、实际协商的 TLS 版本）。 |
| `DECLARED` | 目标在其完全控制的字段中自行声明的值（如 `Server` 横幅）— 看似合理，但可被随意伪造。 |
| `CORROBORATED` | 一个 `DECLARED` 值被独立线索证实（如 SSH 角色，因为协议确实已协商）。 |
| `INFERRED` | 由模式/启发式规则推断，目标没有明确声明。 |
| `UNKNOWN` | 没有可用线索，或被目标主动隐藏。 |

## 8. 防范伪造的值

Omega-check 不会在未明确标注的情况下信任任何由目标自行声明的数据。`Server` 横幅或 `X-Powered-By` 响应头无论看起来多么可信，都只是 `DECLARED`，绝不是 `VERIFIED` — 它们由目标本身提供，可以被随意伪造。只有通过独立渠道的确认（例如为“Shell 访问”角色实际协商的 SSH 协议）才能使一条信息升为 `CORROBORATED`。这一区分由 `omega-lib`（`ConfidenceLevel`）承载，是结构性的：任何导出和任何视图都无法掩盖它。

## 9. 终端兼容性

TUI（Textual）会自动检测终端的能力（模拟器、尺寸），并据此调整其结构样式表（`complete`/`standard`/`reduced`/`mono`），无需手动选项。CLI 模式始终是纯文本，与终端无关。该策略由整个 `omega-` 套件共享（`omega-lib`、`terminal/policies.py`）。

### 按检测到的模拟器确定的配置

| 模拟器 | 初始配置 |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm、urxvt、现代 SSH | `reduced` |
| Linux TTY、旧版 SSH | `mono` |
| 无法识别的模拟器 | `reduced`（默认回退） |

### 按终端尺寸确定的配置

| 最小尺寸（列 × 行） | 配置上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 更小 | `mono` |

最终配置为**两者中更严格的一个**（模拟器和尺寸）— 全屏的 Ghostty 若缩小到 70 列，会降为 `mono`，即使其模拟器允许 `complete`。可用 `r` 键实时刷新。

## 10. 导出

文本和 HTML 报告使用设置中选择的语言编写（“导出语言”，默认与界面相同）；JSON 作为数据保持不翻译。报告默认生成在 `var/exports/`（运行时路径锚定在项目目录，可用 `$OMEGA_CHECK_VAR_DIR` 覆盖），或生成在指定路径（CLI 中用 `--output`，TUI 中用对话框）。文件名清晰并带时间戳：`scan-{配置}-{日期}.ext`，个人配置为 `scan-custom-{日期}.ext`，无配置的自由输入为 `scan-{日期}.ext`。

### JSON，权威来源

扫描的完整结构（`Scan` + `Host`），严格可序列化为 JSON，包含可信度级别。

### 文本，紧凑的可读报告

在终端之外也可阅读，不含 ANSI 代码。

### HTML，独立的网页报告

5 种主题可选（CLI 中用 `--theme`，TUI 中用选择器；若有对应主题，默认跟随当前界面主题）。专门的布局：容器、信息网格、按端口状态的统计框、彩色徽章 — 与 `omega-scan`/`omega-stress` 属于同一视觉风格。

## 11. 历史与对比

每次扫描都会保存（SQLite，`var/db/omega-check.db`）：可按目标查看历史、查看过往运行的详情、对比两次扫描（端口状态），以及对同一目标重放扫描而无需重新输入。

## 12. 测试

```bash
source .venv/bin/activate
lint-imports        # 检查 Dependency Rule
pytest -q           # 191 个测试
ruff check src tests
mypy -p omega_check
```

结构：`tests/unit/`（领域和应用层，无真实 I/O），`tests/integration/`（真实 SQLite/文件、模拟 HTTP 服务器 `pytest-httpserver`、通过 `trustme` 的 TLS）。

## 13. 范围之外

- CVE 扫描
- 主动检测 SQLi、XSS、RCE
- 操作系统指纹识别
- nmap 式的底层扫描技术（SYN 扫描、原始数据包）
- 爬取
- 模糊测试
- 暴力破解
- 多目标同时扫描
- Web 仪表盘

---

> Omega-check — 扫描、识别、定级、报告。
> 一个带有明确可信度的端口扫描器，而不是伪装成事实的猜测。
