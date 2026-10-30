<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT ライセンス（LICENSE ファイルを参照） -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**ポート・サービス・ネットワーク上の役割のスキャナー（単一ターゲット）**

> **Omega-server** のために **kraynux** が開発 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

公式ページ：[OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; スクリーンショット：[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 インターフェースとエクスポートされるレポートは **17 言語** に対応 — [インターフェースの言語](#インターフェースの言語)を参照。  
**言語：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** は、単一のネットワークターゲットのポートをスキャンし、開いている各ポートで動作するサービス（プロトコル、ソフトウェア、バージョン、認証、WAF、TLS）を特定して、その役割を推定する TUI + CLI ツールです。能動的な攻撃は一切行いません。`omega-` スイートのツールで、Clean Architecture で構成されています — 技術的な詳細はすべて `docs/ARCHITECTURE.md` を参照してください。

## 1. ビジョンと範囲

Omega-check はシステム管理向けのポートスキャナーです：あるマシン（自分のマシン、LAN、または許可された外部ターゲット）で何が待ち受けているのか、何で動いているのか、そして各情報をどこまで信頼できるのかを素早く確認します。

### Omega-check ができること

- 単一ターゲットに対してポートの一覧（システムプロファイル、個人プロファイル、または自由入力）をスキャンします。
- 開いている各ポートのサービスを特定します：プロトコル（HTTP/HTTPS/SSH/TLS/VNC/汎用）、公開されていればソフトウェアとバージョン、認証の要否。
- 実際にネゴシエートされたプロトコルから、想定される役割（Web サーバー、シェルアクセス、グラフィカルアクセス、データベース）を推定します。ポート番号だけからの推測は決して行いません。
- ヘッダーで宣言されている場合、既知の WAF シグネチャ（Cloudflare、Sucuri、Akamai、Imperva Incapsula）を検出します。
- 結果を TUI（Textual）またはスクリプト可能な CLI で表示し、3 種類のエクスポート（JSON、テキスト、5 テーマの HTML）を備えます。
- 収集したすべての情報に明示的な信頼度を付けます — [§7](#7-信頼度ポリシー) を参照。
- スキャン履歴を永続的に保存し、再実行や経時的な比較ができます。
- ターゲットのピン留めや、スキャン間で再利用できる個人用ポートプロファイルの作成ができます。

### Omega-check がしないこと

- 能動的な脆弱性スキャン：SQLi、XSS、RCE は行いません。
- CVE スキャン。
- OS のフィンガープリント（データモデルにはフィールドがありますが、現時点で埋めるヒューリスティックはありません）。
- nmap 風の低レベルなスキャン技法（SYN スキャン、生パケット）— アプリケーションレベルの TCP 接続のみです。
- 総当たりやファジングのツール。
- 複数ターゲットの並列スキャン。
- Web ダッシュボード。

## 2. インストール

### 前提条件

- Python 3.10+
- 依存関係のためのインターネット接続

### インストール

```bash
[ -d omega-check ] && echo "ℹ️ ここに展開済みのため、この手順をスキップします。" || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`：

1. 仮想環境 `.venv` がまだなければ作成します。
2. 依存関係をインストールします（`pip install -e .`。`pyproject.toml` が唯一の正となる情報源です）。
3. `omega-check.sh` と `install.sh` を実行可能にします。
4. エイリアス `check` を `~/.bashrc` と `~/.zshrc` に追加します（既にあれば重複させません）。

### 依存関係

`pyproject.toml` で宣言（`requirements.txt` は廃止）：
- `omega-lib`：スイート共通ライブラリ（`ConfidenceLevel`、テーマ、端末検出）
- `textual`：TUI インターフェース、テーマ、端末への自動適応
- `httpx`：HTTP/HTTPS のプローブ
- `cryptography`：ネゴシエートされた TLS 証明書の読み取り
- `jinja2`：HTML エクスポートのテンプレート
- 開発用の依存関係（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`trustme`、`ruff`、`mypy`、`import-linter`

## 3. 使い方

### 対話モード（TUI）

日常の利用におすすめ — 引数なしで起動します：

```bash
./omega-check.sh
```
エイリアスを作成した場合は、端末で `check` と入力するだけです：
```bash
check
```

流れ：スプラッシュ画面（キーまたはクリックで閉じる）→ メインメニュー（スキャン / ターゲット / プロファイル / 履歴 / 設定 / ヘルプ）→ ターゲットの入力（ピン留めしたターゲットから選択可能）とプロファイルの選択（`complet` では警告、`CUSTOM` では個人プロファイルまたはポートの自由入力用の 2 つ目の欄）→ スキャン（不確定の進捗表示とネットワーク操作のリアルタイムログ）→ スキャンの詳細（ポート／サービス／役割、エクスポート）→ メインメニューから履歴／比較／再実行と設定。端末への適応（色、サイズ、構造の簡略化）は自動です。

#### キーボードショートカット

| キー | 操作 |
|---|---|
| `↑` / `↓` | 画面の項目間を移動 |
| `Tab` / `Shift+Tab` | フォームの入力欄間を移動 |
| `Esc` | 前の画面に戻る（ホーム画面では終了を確認） |
| `t` | 次のテーマ（確認なしですぐに適用） |
| `r` | 端末の検出を更新 |
| `a` | ヘルプを表示 |
| `q` | 終了（確認あり） |

### インターフェースの言語

インターフェースは 17 言語に対応しています：フランス語、英語、スペイン語、ポルトガル語（ブラジル）、イタリア語、ドイツ語、オランダ語、ポーランド語、ロシア語、簡体字中国語、ベトナム語、タイ語、インドネシア語、日本語、韓国語、ヒンディー語、アラビア語。設定（「Langue / Language」）で選択し、インターフェースの再起動後に反映されます。変数 `OMEGA_CHECK_LANG`（例：`OMEGA_CHECK_LANG=ja ./omega-check.sh`）で、1 セッションの間だけ言語を固定できます。omega-suite から起動した場合、omega-check はスイートの言語を使います。Linux のテキストコンソール（TTY）では、ラテン文字以外の言語はそのセッション中は英語で表示されます。コマンドラインはフランス語のままです。

### スクリプトモード（CLI）

サブコマンドを指定すると CLI モードになります：

```bash
# ポートプロファイルを指定してターゲットをスキャン
./omega-check.sh scan 192.168.1.10 --profile minimal

# 履歴（ターゲットで絞り込み可能）
./omega-check.sh history --target 192.168.1.10 --limit 20

# スキャンの詳細（テキスト、JSON、HTML）— エクスポートのテーマは 5 種類から選択
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# 2 つのスキャンを比較（ポート状態の変化）
./omega-check.sh compare <scan_id_a> <scan_id_b>

# 個人用ポートプロファイル
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "自分のプロファイル"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### 受け付けるターゲットの形式

```text
192.168.1.10                IPv4
example.org                 ホスト名
http://example.org          HTTP の URL（名前解決の前にスキームを除去）
https://example.org:8443    ポート付き HTTPS の URL（スキームとポートを除去）
```

スキームとポートがあれば、DNS の名前解決の前に除去されます（`domain/targets/validation.py::normalize_target_input`）— URL を丸ごと貼り付けても動作し、ホスト部分だけが残ります。

## 4. スキャンプロファイル

| プロファイル | 説明 | ピン留め |
|---|---|---|
| `minimal` | 超高速スキャン：SSH + HTTP + HTTPS（22、80、443） | はい |
| `classic` | 一般的なインターネット／LAN サービス（37 ポート） | はい |
| `web` | Web サービスとその代替ポート | いいえ |
| `db` | データベースとデータサービス | いいえ |
| `remote` | リモートアクセス — シェル、デスクトップ、RustDesk | いいえ |
| `mail` | メールサービス | いいえ |
| `dns` | DNS サービス | いいえ |
| `iot` | IoT 機器、カメラ、ルーター、ホームオートメーション | いいえ |
| `dev` | 開発／検証環境 | いいえ |
| `docker` | Docker、Swarm、コンテナでよく使われるサービス | いいえ |
| `complet` | **その場で生成**：上記すべてのプロファイルを並べ替え、重複を除いた和集合 | いいえ |
| `CUSTOM` | **プロファイル**画面で作成した個人プロファイル、および／または自由入力（`80` / `22,443,8080` / `1000-2000`）— 両方が合算され、重複は除かれます | いいえ |

完全な詳細、検証ルール、個人プロファイルの管理：`docs/PROFILES.md`。

## 5. アーキテクチャ

Omega-check は **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared）で構成され、`omega-` スイートのテンプレート（`omega-scan`/`omega-stress` を参照）に揃えてあり、変更のたびに `import-linter` で検証されます。完全な詳細は **`docs/ARCHITECTURE.md`** にあります。

ごく短い概要：

```text
src/omega_check/
├── domain/          純粋な業務ロジック（スキャン、ターゲット、サービス、プロファイル、レポート...）
├── application/     ユースケース（commands/queries）
├── ports/           アプリケーションが期待する契約（プローブ、リポジトリ、エクスポーター...）
├── infrastructure/  具体的な実装（socket/httpx/cryptography、SQLite。Textual はここにはありません）
├── interfaces/      tui/（Textual）と cli/（スクリプト可能）、機能は厳密に同等
├── app/             組み立て（DependencyContainer、bootstrap、ライフサイクル）
├── core/, shared/   横断的な語彙、業務外のユーティリティ
└── plugins/         構造のみ用意、空（確定した拡張の方向性なし）
```

設計ルール：
- `domain/services/policies.py`：収集済みの手がかりを分類し、ネットワークには一切アクセスしません。
- `infrastructure/network/`：ネットワークにアクセスし（ソケット、`httpx`、`cryptography`）、判断はしません。
- `interfaces/`：表示するだけで、業務ロジックは含みません。
- `infrastructure/exporters/`：スキャン結果を読むだけで、何も再計算しません。

## 6. サービスの特定と役割

### 検出するプロトコル

| プロトコル | プローブ | 収集する詳細 |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` バナー、認証ヘッダー |
| TLS | `cryptography`（ネゴシエートされた証明書、`CERT_NONE` を含む） | バージョン、暗号スイート、証明書のサブジェクト／発行者 |
| SSH | 生のバナー | ソフトウェアとバージョン（例：`OpenSSH 10.4`） |
| VNC (RFB) | サーバーが提示するセキュリティコード | 対応している認証方式 |
| 汎用 | 認識できない開いたポートの生のバナー | 慎重な抽出、強引なヒューリスティックは使わない |

### 推定する役割

ポート番号による推測ではなく、**実際にネゴシエートされた**プロトコルから導きます：

| 役割 | 条件 | 信頼度 |
|---|---|---|
| `Web サーバー` | HTTP/HTTPS プロトコルを確認 | `INFERRED` |
| `シェルアクセス` | SSH プロトコルを確認 | `CORROBORATED` |
| `グラフィカルアクセス` | VNC プロトコルを確認 | `CORROBORATED` |
| `データベース` | ポートがシステムプロファイル `db` の範囲内 | `INFERRED` |

### 既知の WAF シグネチャ

宣言的なヘッダー（`server`、`x-sdk`）から検出します — 存在は**ターゲット自身が宣言したもの**で、独立した検証は行いません：Cloudflare、Sucuri、Akamai、Imperva Incapsula、AWS ELB（参考として掲載。厳密にはアプリケーション WAF ではありません）。

## 7. 信頼度ポリシー

収集した各フィールドには、次のいずれかのレベルが付きます：

| レベル | 意味 |
|---|---|
| `VERIFIED` | 直接観測したプロトコル上の事実で、ターゲットが偽装できないもの（例：TCP RST で確認した閉じたポート、実際にネゴシエートされた TLS バージョン）。 |
| `DECLARED` | ターゲットが完全に制御するフィールドで自ら名乗った値（例：`Server` バナー）— もっともらしいが、自由に偽装できる。 |
| `CORROBORATED` | 独立した手がかりによって裏付けられた `DECLARED` の値（例：SSH の役割。プロトコルが実際にネゴシエートされているため）。 |
| `INFERRED` | ターゲットによる明示的な宣言なしに、パターンやヒューリスティックから推定したもの。 |
| `UNKNOWN` | 使える手がかりがない、またはターゲットが意図的に隠している。 |

## 8. 偽装された値への対策

Omega-check は、ターゲットが自ら宣言したデータを、そのことを明示せずに信用することはありません。`Server` バナーや `X-Powered-By` ヘッダーは、どれほどもっともらしくても `DECLARED` のままで、決して `VERIFIED` にはなりません — それらを提供するのはターゲット自身であり、自由に偽装できるからです。独立した経路での確認（たとえば「シェルアクセス」の役割に対して実際にネゴシエートされた SSH プロトコル）があって初めて、情報は `CORROBORATED` に上がります。この区別は `omega-lib`（`ConfidenceLevel`）が担う構造的なもので、どのエクスポートやビューでも隠すことはできません。

## 9. 端末との互換性

TUI（Textual）は端末の能力（エミュレーター、サイズ）を自動的に検出し、それに合わせて構造スタイルシート（`complete`/`standard`/`reduced`/`mono`）を調整します。手動の指定は不要です。CLI モードは常にプレーンテキストで、端末に依存しません。この方針は `omega-` スイート全体で共通です（`omega-lib`、`terminal/policies.py`）。

### 検出したエミュレーターによるプロファイル

| エミュレーター | 初期プロファイル |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm、urxvt、最近の SSH | `reduced` |
| Linux TTY、古い SSH | `mono` |
| 認識できないエミュレーター | `reduced`（既定の代替） |

### 端末サイズによるプロファイル

| 最小サイズ（列 × 行） | プロファイルの上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| それ未満 | `mono` |

最終的なプロファイルは**両者のうち制限の厳しい方**（エミュレーターとサイズ）です — 全画面の Ghostty を 70 列に縮めると、エミュレーターとしては `complete` が可能でも `mono` に下がります。`r` キーでその場で更新できます。

## 10. エクスポート

テキストと HTML のレポートは、設定で選んだ言語で書かれます（「エクスポートの言語」、既定はインターフェースと同じ）。JSON はデータのままで翻訳されません。レポートは既定で `var/exports/` に生成されます（実行時のパスはプロジェクトフォルダーに固定、`$OMEGA_CHECK_VAR_DIR` で変更可能）。または指定したパス（CLI では `--output`、TUI ではダイアログ）に生成されます。わかりやすいタイムスタンプ付きのファイル名：`scan-{プロファイル}-{日付}.ext`、個人プロファイルでは `scan-custom-{日付}.ext`、プロファイルなしの自由入力では `scan-{日付}.ext`。

### JSON、正となる情報源

スキャンの完全な構造（`Scan` + `Host`）、厳密に JSON シリアライズ可能で、信頼度も含みます。

### テキスト、コンパクトで読みやすいレポート

端末の外でも読めて、ANSI コードを含みません。

### HTML、単体で完結する Web レポート

5 種類のテーマから選択（CLI では `--theme`、TUI ではセレクター。対応するものがあれば、既定で現在のインターフェースのテーマに従います）。専用のレイアウト：コンテナー、情報グリッド、ポート状態ごとの統計ボックス、色付きバッジ — `omega-scan`/`omega-stress` と同じ見た目の系統です。

## 11. 履歴と比較

各スキャンは保存されます（SQLite、`var/db/omega-check.db`）：ターゲットごとの履歴の閲覧、過去の実行の詳細、2 つのスキャンの比較（ポートの状態）、同じターゲットに対する再入力なしの再実行ができます。

## 12. テスト

```bash
source .venv/bin/activate
lint-imports        # Dependency Rule をチェック
pytest -q           # 191 件のテスト
ruff check src tests
mypy -p omega_check
```

構成：`tests/unit/`（実際の I/O を伴わないドメインとアプリケーション）、`tests/integration/`（実際の SQLite／ファイル、模擬 HTTP サーバー `pytest-httpserver`、`trustme` による TLS）。

## 13. 範囲外

- CVE スキャン
- SQLi、XSS、RCE の能動的な検出
- OS のフィンガープリント
- nmap 風の低レベルなスキャン技法（SYN スキャン、生パケット）
- クロール
- ファジング
- 総当たり攻撃
- 複数ターゲットの同時スキャン
- Web ダッシュボード

---

> Omega-check — スキャンし、特定し、評価し、報告する。
> 信頼度を明示するポートスキャナー。事実を装った推測ではありません。
