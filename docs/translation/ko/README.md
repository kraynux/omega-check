<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 라이선스 (LICENSE 파일 참조) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**포트, 서비스, 네트워크 역할 스캐너 (단일 대상)**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net)를 위해 [kraynux](https://github.com/kraynux)가 개발   

공식 페이지: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; 미리보기: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 인터페이스와 내보낸 보고서는 **17개 언어**로 제공됩니다 — [인터페이스 언어](#인터페이스-언어) 참조.  
**언어:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check**는 단일 네트워크 대상의 포트를 스캔하고, 열린 각 포트에서 실행 중인 서비스(프로토콜, 소프트웨어, 버전, 인증, WAF, TLS)를 식별해 그 역할을 추정하는 TUI + CLI 도구이며, 능동적인 공격은 절대 하지 않습니다. `omega-` 제품군의 도구이며 Clean Architecture로 구성되어 있습니다 — 기술적인 세부 사항은 모두 `docs/ARCHITECTURE.md`를 참조하세요.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-check/D.png" width="24%" />
</p>

## 1. 비전과 범위

Omega-check는 시스템 관리를 위한 포트 스캐너입니다: 어떤 머신(자신의 머신, LAN, 또는 허가받은 외부 대상)에서 무엇이 수신 대기 중인지, 무엇으로 돌아가는지, 각 정보를 얼마나 신뢰할 수 있는지 빠르게 확인합니다.

### Omega-check가 하는 일

- 단일 대상에서 포트 목록(시스템 프로필, 개인 프로필 또는 자유 입력)을 스캔합니다.
- 열린 각 포트의 서비스를 식별합니다: 프로토콜(HTTP/HTTPS/SSH/TLS/VNC/일반), 노출된 경우 소프트웨어와 버전, 인증 필요 여부.
- 실제로 협상된 프로토콜에서 가능성 있는 역할(웹 서버, 셸 접근, 그래픽 접근, 데이터베이스)을 추정하며, 포트 번호만으로 짐작하지 않습니다.
- 헤더에 선언된 경우 알려진 WAF 시그니처(Cloudflare, Sucuri, Akamai, Imperva Incapsula)를 탐지합니다.
- 결과를 TUI(Textual) 또는 스크립트용 CLI로 보여 주며, 세 가지 내보내기(JSON, 텍스트, 5가지 테마의 HTML)를 제공합니다.
- 수집한 모든 정보에 명시적인 신뢰 수준을 붙입니다 — [§7](#7-신뢰-정책) 참조.
- 스캔 기록을 영구 보관하며, 다시 실행하고 시간에 따라 비교할 수 있습니다.
- 대상을 고정하고, 스캔마다 재사용할 수 있는 개인 포트 프로필을 만들 수 있습니다.

### Omega-check가 하지 않는 일

- 능동적 취약점 스캔: SQLi, XSS, RCE 없음.
- CVE 스캔.
- 운영 체제 핑거프린팅(데이터 모델에 필드는 있지만 아직 이를 채우는 휴리스틱은 없습니다).
- nmap 방식의 저수준 스캔 기법(SYN 스캔, 원시 패킷) — 애플리케이션 수준의 TCP 연결만 사용합니다.
- 무차별 대입이나 퍼징 도구.
- 여러 대상의 병렬 스캔.
- 웹 대시보드.

## 2. 설치

### 요구 사항

- Python 3.10+
- 의존성을 위한 인터넷 연결

### 설치

```bash
[ -d omega-check ] && echo "ℹ️ 이미 여기에 압축이 풀려 있어 이 단계를 건너뜁니다." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. 가상 환경 `.venv`가 아직 없으면 만듭니다.
2. 의존성을 설치합니다(`pip install -e .`; `pyproject.toml`이 유일한 기준 정보로 남습니다).
3. `omega-check.sh`와 `install.sh`를 실행 가능하게 만듭니다.
4. 별칭 `check`를 `~/.bashrc`와 `~/.zshrc`에 추가합니다(이미 있으면 중복하지 않습니다).

### 의존성

`pyproject.toml`에 선언(`requirements.txt`는 더 이상 없음):
- `omega-lib`: 제품군 공용 라이브러리(`ConfidenceLevel`, 테마, 터미널 감지)
- `textual`: TUI 인터페이스, 테마, 터미널 자동 적응
- `httpx`: HTTP/HTTPS 프로브
- `cryptography`: 협상된 TLS 인증서 읽기
- `jinja2`: HTML 내보내기용 템플릿
- 개발 의존성(`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. 사용법

### 대화형 모드 (TUI)

일상적인 사용에 권장 — 인수 없이 실행합니다:

```bash
./omega-check.sh
```
별칭을 만들었다면 터미널에 `check`만 입력하면 됩니다:
```bash
check
```

흐름: 시작 화면(키를 누르거나 클릭하면 닫힘) → 메인 메뉴(스캔 / 대상 / 프로필 / 기록 / 설정 / 도움말) → 대상 입력(고정된 대상 선택기 포함)과 프로필 선택(`complet`이면 경고, `CUSTOM`이면 개인 프로필이나 포트 자유 입력을 위한 두 번째 필드) → 스캔(불확정 진행 표시와 실시간 네트워크 작업 로그) → 스캔 상세(포트/서비스/역할, 내보내기) → 메인 메뉴에서 기록/비교/다시 실행과 설정. 터미널에 대한 적응(색상, 크기, 구조 단순화)은 자동입니다.

#### 단축키

| 키 | 동작 |
|---|---|
| `↑` / `↓` | 화면의 항목 사이 이동 |
| `Tab` / `Shift+Tab` | 양식의 필드 사이 이동 |
| `Esc` | 이전 화면으로 돌아가기(홈 화면에서는 종료 확인) |
| `t` | 다음 테마(확인 없이 즉시 적용) |
| `r` | 터미널 감지 새로 고침 |
| `a` | 도움말 표시 |
| `q` | 종료(확인 후) |

### 인터페이스 언어

인터페이스는 17개 언어로 제공됩니다: 프랑스어, 영어, 스페인어, 포르투갈어(브라질), 이탈리아어, 독일어, 네덜란드어, 폴란드어, 러시아어, 중국어 간체, 베트남어, 태국어, 인도네시아어, 일본어, 한국어, 힌디어, 아랍어. 설정(“Langue / Language”)에서 선택하며 인터페이스를 다시 시작한 뒤 적용됩니다. 변수 `OMEGA_CHECK_LANG`(예: `OMEGA_CHECK_LANG=ko ./omega-check.sh`)으로 한 세션 동안 언어를 강제할 수 있습니다. omega-suite에서 실행하면 omega-check는 제품군의 언어를 사용합니다. Linux 텍스트 콘솔(TTY)에서는 라틴 문자가 아닌 언어가 해당 세션 동안 영어로 표시됩니다. 명령줄은 프랑스어로 유지됩니다.

### 문의 및 지원

도움말(`a` 키)에는 **문의 및 지원** 화면이 있습니다: *커피 한 잔 사기*(개발자의 PayPal 페이지), *지원팀에 문의*(이메일 주소와 사이트의 문의 양식을 그대로 표시), *사용자로 등록(익명)*, *업데이트 확인*. 등록은 자발적이며 기본적으로 꺼져 있고 한 번만 전송됩니다. 사용자 수와, 원하면 사용자의 대륙 또는 국가(닫힌 목록, 자유 입력 없음)를 세는 데에만 쓰입니다. 무작위로 생성한 키, 소프트웨어 이름(`omega-check`)과 버전만 보내며, 이름, 컴퓨터 이름, 설정, 대상, 결과는 절대 보내지 않습니다. IP 주소는 등록 정보에 저장되지 않지만, 모든 방문과 마찬가지로 수신 서버의 보안 검사와 로그를 거칩니다. 같은 화면에서 언제든지 철회할 수 있습니다(*등록 취소*). 업데이트 확인은 사이트에 게시된 버전 목록만 읽으며, 클릭하지 않으면 절대 실행되지 않습니다.

### 스크립트 모드 (CLI)

하위 명령을 지정하면 CLI 모드가 됩니다:

```bash
# 포트 프로필로 대상 스캔
./omega-check.sh scan 192.168.1.10 --profile minimal

# 기록(대상별 필터 가능)
./omega-check.sh history --target 192.168.1.10 --limit 20

# 스캔 상세(텍스트, JSON 또는 HTML) — 내보내기 테마 5가지 중 선택
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# 두 스캔 비교(포트 상태 변화)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# 개인 포트 프로필
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "내 프로필"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### 허용되는 대상 형식

```text
192.168.1.10                IPv4
example.org                 호스트 이름
http://example.org          HTTP URL  (이름 해석 전에 스킴 제거)
https://example.org:8443    포트가 있는 HTTPS URL  (스킴과 포트 제거)
```

스킴과 포트가 있으면 DNS 해석 전에 제거됩니다(`domain/targets/validation.py::normalize_target_input`) — URL 전체를 붙여 넣어도 동작하며, 호스트만 남습니다.

## 4. 스캔 프로필

| 프로필 | 설명 | 고정 |
|---|---|---|
| `minimal` | 초고속 스캔: SSH + HTTP + HTTPS (22, 80, 443) | 예 |
| `classic` | 일반적인 인터넷/LAN 서비스(포트 37개) | 예 |
| `web` | 웹 서비스와 대체 포트 | 아니요 |
| `db` | 데이터베이스와 데이터 서비스 | 아니요 |
| `remote` | 원격 접근 — 셸, 데스크톱, RustDesk | 아니요 |
| `mail` | 메일 서비스 | 아니요 |
| `dns` | DNS 서비스 | 아니요 |
| `iot` | IoT 장비, 카메라, 공유기, 홈 오토메이션 | 아니요 |
| `dev` | 개발/실험 환경 | 아니요 |
| `docker` | Docker, Swarm, 컨테이너에서 흔히 쓰는 서비스 | 아니요 |
| `complet` | **즉석 생성**: 위의 모든 프로필을 정렬하고 중복을 제거한 합집합 | 아니요 |
| `CUSTOM` | **프로필** 화면에서 만든 개인 프로필, 및/또는 자유 입력(`80` / `22,443,8080` / `1000-2000`) — 둘이 합쳐지며 중복은 제거됩니다 | 아니요 |

전체 세부 사항, 검증 규칙, 개인 프로필 관리: `docs/PROFILES.md`.

## 5. 아키텍처

Omega-check는 **Clean Architecture**(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)로 구성되어 있으며, `omega-` 제품군의 템플릿(`omega-scan`/`omega-stress` 참조)에 맞추고 변경할 때마다 `import-linter`로 검증합니다. 전체 세부 사항은 **`docs/ARCHITECTURE.md`**에 있습니다.

아주 짧은 개요:

```text
src/omega_check/
├── domain/          순수 업무 로직(스캔, 대상, 서비스, 프로필, 보고서...)
├── application/     사용 사례(commands/queries)
├── ports/           애플리케이션이 기대하는 계약(프로브, 저장소, 내보내기 도구...)
├── infrastructure/  구체 구현(socket/httpx/cryptography, SQLite; Textual은 여기에 없음)
├── interfaces/      tui/(Textual)와 cli/(스크립트용), 기능이 엄격히 동일
├── app/             조립(DependencyContainer, bootstrap, 수명 주기)
├── core/, shared/   공통 어휘, 업무 외 유틸리티
└── plugins/         구조만 마련됨, 비어 있음(확정된 확장 방향 없음)
```

설계 규칙:
- `domain/services/policies.py`: 이미 수집된 단서를 분류하며 네트워크에는 접근하지 않습니다.
- `infrastructure/network/`: 네트워크에 접근하며(소켓, `httpx`, `cryptography`) 판단하지 않습니다.
- `interfaces/`: 표시만 하며 업무 로직을 담지 않습니다.
- `infrastructure/exporters/`: 스캔 결과를 읽기만 하며 아무것도 다시 계산하지 않습니다.

## 6. 서비스 식별과 역할

### 탐지하는 프로토콜

| 프로토콜 | 프로브 | 수집하는 세부 정보 |
|---|---|---|
| HTTP / HTTPS | `httpx` | `Server` 배너, 인증 헤더 |
| TLS | `cryptography`(협상된 인증서, `CERT_NONE` 포함) | 버전, 암호 스위트, 인증서 주체/발급자 |
| SSH | 원시 배너 | 소프트웨어와 버전(예: `OpenSSH 10.4`) |
| VNC (RFB) | 서버가 알리는 보안 코드 | 지원하는 인증 유형 |
| 일반 | 인식하지 못한 열린 포트의 원시 배너 | 신중한 추출, 공격적인 휴리스틱 없음 |

### 추정하는 역할

포트 번호에 대한 짐작이 아니라 **실제로 협상된** 프로토콜에서 도출합니다:

| 역할 | 조건 | 신뢰도 |
|---|---|---|
| `웹 서버` | HTTP/HTTPS 프로토콜 확인 | `INFERRED` |
| `셸 접근` | SSH 프로토콜 확인 | `CORROBORATED` |
| `그래픽 접근` | VNC 프로토콜 확인 | `CORROBORATED` |
| `데이터베이스` | 포트가 시스템 프로필 `db` 범위 안에 있음 | `INFERRED` |

### 알려진 WAF 시그니처

선언적 헤더(`server`, `x-sdk`)를 통해 탐지합니다 — 존재 여부는 **대상이 스스로 선언한 것**이며 독립적으로 검증하지 않습니다: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB(참고용으로 기재, 엄밀히는 애플리케이션 WAF가 아님).

## 7. 신뢰 정책

수집된 각 필드에는 다음 수준 중 하나가 붙습니다:

| 수준 | 의미 |
|---|---|
| `VERIFIED` | 직접 관찰한 프로토콜상의 사실로, 대상이 위조할 수 없습니다(예: TCP RST로 확인한 닫힌 포트, 실제로 협상된 TLS 버전). |
| `DECLARED` | 대상이 완전히 통제하는 필드에서 스스로 알린 값(예: `Server` 배너) — 그럴듯하지만 마음대로 위조할 수 있습니다. |
| `CORROBORATED` | 독립적인 단서로 확인된 `DECLARED` 값(예: SSH 역할, 프로토콜이 실제로 협상되었으므로). |
| `INFERRED` | 대상의 명시적 선언 없이 패턴/휴리스틱으로 추정한 값. |
| `UNKNOWN` | 쓸 만한 단서가 없거나 대상이 의도적으로 숨긴 경우. |

## 8. 위조된 값에 대한 보호

Omega-check는 대상이 스스로 선언한 데이터를 명시적으로 표시하지 않고는 신뢰하지 않습니다. `Server` 배너나 `X-Powered-By` 헤더는 아무리 그럴듯해도 `DECLARED`로 남으며 절대 `VERIFIED`가 되지 않습니다 — 이것들은 대상 자신이 제공하며 마음대로 위조할 수 있기 때문입니다. 독립적인 경로를 통한 확인(예: “셸 접근” 역할에 대해 실제로 협상된 SSH 프로토콜)이 있어야만 정보가 `CORROBORATED`로 올라갑니다. 이 구분은 `omega-lib`(`ConfidenceLevel`)가 담당하는 구조적인 것이어서, 어떤 내보내기나 화면도 이를 숨길 수 없습니다.

## 9. 터미널 호환성

TUI(Textual)는 터미널의 능력(에뮬레이터, 크기)을 자동으로 감지하고 그에 맞게 구조 스타일시트(`complete`/`standard`/`reduced`/`mono`)를 조정합니다. 수동 옵션은 필요 없습니다. CLI 모드는 항상 일반 텍스트이며 터미널과 무관합니다. 이 정책은 `omega-` 제품군 전체가 공유합니다(`omega-lib`, `terminal/policies.py`).

### 감지된 에뮬레이터에 따른 프로필

| 에뮬레이터 | 초기 프로필 |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, 최신 SSH | `reduced` |
| Linux TTY, 구형 SSH | `mono` |
| 인식할 수 없는 에뮬레이터 | `reduced`(기본 대체값) |

### 터미널 크기에 따른 프로필

| 최소 크기(열 × 행) | 프로필 상한 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 그보다 작음 | `mono` |

최종 프로필은 **둘 중 더 엄격한 쪽**(에뮬레이터와 크기)입니다 — 전체 화면의 Ghostty를 70열로 줄이면, 에뮬레이터가 `complete`를 허용하더라도 `mono`로 내려갑니다. `r` 키로 바로 새로 고칠 수 있습니다.

## 10. 내보내기

텍스트와 HTML 보고서는 설정에서 고른 언어로 작성됩니다(“내보내기 언어”, 기본값은 인터페이스와 같음). JSON은 데이터로 남으며 번역되지 않습니다. 보고서는 기본적으로 `var/exports/`에 생성되며(실행 경로는 프로젝트 폴더에 고정, `$OMEGA_CHECK_VAR_DIR`로 변경 가능), 지정한 경로(CLI에서는 `--output`, TUI에서는 대화 상자)에 생성할 수도 있습니다. 명확하고 시각이 들어간 파일 이름: `scan-{프로필}-{날짜}.ext`, 개인 프로필은 `scan-custom-{날짜}.ext`, 프로필 없는 자유 입력은 `scan-{날짜}.ext`.

### JSON, 기준 정보

스캔의 전체 구조(`Scan` + `Host`), 엄격하게 JSON 직렬화 가능하며 신뢰 수준도 포함합니다.

### 텍스트, 간결하고 읽기 쉬운 보고서

터미널 밖에서도 읽을 수 있으며 ANSI 코드가 없습니다.

### HTML, 독립형 웹 보고서

테마 5가지 중 선택(CLI에서는 `--theme`, TUI에서는 선택기. 대응하는 테마가 있으면 기본적으로 현재 인터페이스 테마를 따름). 전용 레이아웃: 컨테이너, 정보 격자, 포트 상태별 통계 상자, 색상 배지 — `omega-scan`/`omega-stress`와 같은 시각적 계열입니다.

## 11. 기록과 비교

각 스캔은 저장됩니다(SQLite, `var/db/omega-check.db`): 대상별 기록 조회, 지난 실행의 상세, 두 스캔의 비교(포트 상태), 같은 대상에 대해 다시 입력하지 않고 스캔 다시 실행.

## 12. 테스트

```bash
source .venv/bin/activate
lint-imports        # Dependency Rule 검사
pytest -q           # 테스트 191개
ruff check src tests
mypy -p omega_check
```

구조: `tests/unit/`(실제 I/O 없는 도메인과 애플리케이션), `tests/integration/`(실제 SQLite/파일, 가짜 HTTP 서버 `pytest-httpserver`, `trustme`를 통한 TLS).

## 13. 범위 밖

- CVE 스캔
- SQLi, XSS, RCE의 능동적 탐지
- 운영 체제 핑거프린팅
- nmap 방식의 저수준 스캔 기법(SYN 스캔, 원시 패킷)
- 크롤링
- 퍼징
- 무차별 대입
- 여러 대상의 동시 스캔
- 웹 대시보드

---

> Omega-check — 스캔하고, 식별하고, 평가하고, 보고한다.
> 신뢰도를 명시하는 포트 스캐너이지, 사실로 꾸민 짐작이 아니다.
