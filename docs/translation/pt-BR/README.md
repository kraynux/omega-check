<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licença MIT (ver o arquivo LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Scanner de portas, serviços e papéis de rede (alvo único)**

> Desenvolvido por **kraynux** para **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Capturas de tela: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface e relatórios exportados disponíveis em **17 idiomas** — veja [Idiomas da interface](#idiomas-da-interface).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** é uma ferramenta TUI + CLI que escaneia as portas de um único alvo de rede, identifica o serviço que roda em cada porta aberta (protocolo, software, versão, autenticação, WAF, TLS) e infere seu papel provável, sem jamais realizar um ataque ativo. Ferramenta da suíte `omega-`, estruturada em Clean Architecture — veja `docs/ARCHITECTURE.md` para todos os detalhes técnicos.

## 1. Visão e escopo

Omega-check é um scanner de portas voltado à administração de sistemas: verificar rapidamente o que está escutando em uma máquina (a sua, a LAN ou um alvo externo autorizado), com o quê, e com quanta confiança cada informação pode ser tomada como certa.

### O que o Omega-check faz

- Escaneia uma lista de portas (perfil do sistema, perfil pessoal ou entrada livre) em um alvo único.
- Identifica o serviço que roda em cada porta aberta: protocolo (HTTP/HTTPS/SSH/TLS/VNC/genérico), software e versão quando expostos, exigência de autenticação.
- Infere um papel provável (servidor web, acesso shell, acesso gráfico, banco de dados) a partir do protocolo realmente negociado, nunca de uma simples suposição pela porta.
- Detecta assinaturas de WAF conhecidas (Cloudflare, Sucuri, Akamai, Imperva Incapsula) quando declaradas nos cabeçalhos.
- Apresenta o resultado em TUI (Textual) ou em CLI scriptável, e por meio de três exportações: JSON, texto, HTML (5 temas).
- Atribui a cada informação coletada um nível de confiança explícito — veja [§7](#7-política-de-confiança).
- Mantém um histórico persistente de escaneamentos, repetível e comparável ao longo do tempo.
- Permite fixar alvos e criar perfis de portas pessoais, reutilizáveis de um escaneamento para outro.

### O que o Omega-check não faz

- Varredura ativa de vulnerabilidades: nada de SQLi, XSS ou RCE.
- Varredura de CVE.
- Identificação do sistema operacional (o modelo de dados prevê o campo, nenhuma heurística o preenche por enquanto).
- Técnicas de varredura de baixo nível no estilo nmap (SYN scan, pacotes brutos) — apenas conexão TCP de aplicação.
- Ferramenta de força bruta ou de fuzzing.
- Escaneamento paralelo de vários alvos.
- Painel web.

## 2. Instalação

### Pré-requisitos

- Python 3.10+
- Conexão com a Internet, para as dependências

### Instalação

```bash
[ -d omega-check ] && echo "ℹ️ Já extraído aqui, etapa ignorada." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Cria o ambiente virtual `.venv` se ele ainda não existir.
2. Instala as dependências (`pip install -e .`; `pyproject.toml` continua sendo a única fonte de verdade).
3. Torna `omega-check.sh` e `install.sh` executáveis.
4. Adiciona o alias `check` a `~/.bashrc` e `~/.zshrc` (sem duplicar se já existir).

### Dependências

Declaradas em `pyproject.toml` (sem mais `requirements.txt`):
- `omega-lib`: biblioteca compartilhada da suíte (`ConfidenceLevel`, temas, detecção do terminal)
- `textual`: interface TUI, temas, adaptação automática ao terminal
- `httpx`: sonda HTTP/HTTPS
- `cryptography`: leitura do certificado TLS negociado
- `jinja2`: templates para a exportação HTML
- Dependências de desenvolvimento (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interativo (TUI)

Recomendado para o uso diário — iniciado sem argumentos:

```bash
./omega-check.sh
```
se você criou o alias, basta digitar `check` no terminal:
```bash
check
```

Percurso: tela de abertura (fecha com uma tecla ou um clique) → menu principal (Escanear / Alvos / Perfis / Histórico / Configurações / Ajuda) → informar o alvo (com seletor de alvos fixados) e escolher o perfil (aviso com `complet`, um segundo campo para um perfil pessoal ou uma entrada livre de portas com `CUSTOM`) → escaneamento (indicador indeterminado e registro das operações de rede ao vivo) → detalhe do escaneamento (portas/serviços/papéis, exportação) → histórico/comparação/repetição e configurações a partir do menu principal. A adaptação ao terminal (cores, tamanho, degradação estrutural) é automática.

#### Atalhos de teclado

| Tecla | Ação |
|---|---|
| `↑` / `↓` | Navegar entre os itens de uma tela |
| `Tab` / `Shift+Tab` | Navegar entre os campos de um formulário |
| `Esc` | Voltar à tela anterior (confirmação de saída na tela inicial) |
| `t` | Próximo tema (aplicado na hora, sem confirmação) |
| `r` | Atualizar a detecção do terminal |
| `a` | Mostrar a ajuda |
| `q` | Sair (com confirmação) |

### Idiomas da interface

A interface está disponível em 17 idiomas: francês, inglês, espanhol, português (Brasil), italiano, alemão, holandês, polonês, russo, chinês simplificado, vietnamita, tailandês, indonésio, japonês, coreano, hindi e árabe. A escolha é feita em Configurações («Langue / Language») e vale após reiniciar a interface; a variável `OMEGA_CHECK_LANG` (por exemplo `OMEGA_CHECK_LANG=pt-BR ./omega-check.sh`) força um idioma durante uma sessão. Iniciado pelo omega-suite, o omega-check usa o idioma da suíte. Em um console de texto Linux (TTY), os idiomas de escrita não latina aparecem em inglês durante a sessão. A linha de comando continua em francês.

### Modo scriptável (CLI)

Qualquer subcomando ativa o modo CLI:

```bash
# Escanear um alvo com um perfil de portas
./omega-check.sh scan 192.168.1.10 --profile minimal

# Histórico (filtrável por alvo)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Detalhe de um escaneamento (texto, JSON ou HTML) — 5 temas de exportação à escolha
./omega-check.sh show <scan_id> --format html --theme omega-base --output relatorio.html

# Comparar dois escaneamentos (mudanças de estado de porta)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Perfis de portas pessoais
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Meu perfil"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Formatos de alvo aceitos

```text
192.168.1.10                IPv4
example.org                 Nome de host
http://example.org          URL HTTP  (esquema removido antes da resolução)
https://example.org:8443    URL HTTPS com porta  (esquema e porta removidos)
```

O esquema e a porta, se houver, são removidos antes da resolução DNS (`domain/targets/validation.py::normalize_target_input`) — colar uma URL inteira funciona, só o host é mantido.

## 4. Perfis de escaneamento

| Perfil | Descrição | Fixado |
|---|---|---|
| `minimal` | Escaneamento ultrarrápido: SSH + HTTP + HTTPS (22, 80, 443) | sim |
| `classic` | Serviços clássicos de Internet/LAN (37 portas) | sim |
| `web` | Serviços web e alternativos | não |
| `db` | Bancos de dados e serviços de dados | não |
| `remote` | Acessos remotos — shell, área de trabalho, RustDesk | não |
| `mail` | Serviços de e-mail | não |
| `dns` | Serviços DNS | não |
| `iot` | Equipamentos IoT, câmeras, roteadores, automação residencial | não |
| `dev` | Ambientes de desenvolvimento/laboratório | não |
| `docker` | Docker, Swarm e serviços comuns em contêineres | não |
| `complet` | **Gerado na hora**: união ordenada e sem duplicatas de todos os perfis acima | não |
| `CUSTOM` | Um perfil pessoal criado na tela **Perfis**, e/ou uma entrada livre (`80` / `22,443,8080` / `1000-2000`) — os dois se somam, sem duplicatas | não |

Detalhe completo, regras de validação e gestão dos perfis pessoais: `docs/PROFILES.md`.

## 5. Arquitetura

O Omega-check é estruturado em **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alinhada ao modelo da suíte `omega-` (veja `omega-scan`/`omega-stress`) e verificada pelo `import-linter` a cada alteração. Todos os detalhes estão em **`docs/ARCHITECTURE.md`**.

Visão geral bem curta:

```text
src/omega_check/
├── domain/          Lógica de negócio pura (escaneamentos, alvos, serviços, perfis, relatórios...)
├── application/     Casos de uso (commands/queries)
├── ports/           Contratos esperados pela aplicação (sondas, repositórios, exportadores...)
├── infrastructure/  Implementações concretas (socket/httpx/cryptography, SQLite; o Textual NÃO está aqui)
├── interfaces/      tui/ (Textual) e cli/ (scriptável), com paridade funcional estrita
├── app/             Montagem (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulário transversal, utilitários fora do negócio
└── plugins/         Estrutura pronta, vazia (nenhum eixo de extensão confirmado)
```

Regras de design:
- `domain/services/policies.py`: classifica os indícios já coletados, nunca faz rede.
- `infrastructure/network/`: faz rede (sockets, `httpx`, `cryptography`), nunca julga.
- `interfaces/`: exibe, não contém nenhuma lógica de negócio.
- `infrastructure/exporters/`: leem o resultado do escaneamento, não recalculam nada.

## 6. Identificação de serviços e papéis

### Protocolos detectados

| Protocolo | Sonda | Detalhe coletado |
|---|---|---|
| HTTP / HTTPS | `httpx` | Banner `Server`, cabeçalhos de autenticação |
| TLS | `cryptography` (certificado negociado, `CERT_NONE` incluído) | Versão, cifra, sujeito/emissor do certificado |
| SSH | Banner bruto | Software e versão (ex. `OpenSSH 10.4`) |
| VNC (RFB) | Códigos de segurança anunciados pelo servidor | Tipos de autenticação suportados |
| Genérico | Banner bruto em porta aberta não reconhecida | Extração cautelosa, sem heurística agressiva |

### Papéis inferidos

Deduzidos do protocolo **realmente negociado**, nunca de uma suposição pelo número da porta:

| Papel | Condição | Confiança |
|---|---|---|
| `servidor web` | Protocolo HTTP/HTTPS confirmado | `INFERRED` |
| `acesso shell` | Protocolo SSH confirmado | `CORROBORATED` |
| `acesso gráfico` | Protocolo VNC confirmado | `CORROBORATED` |
| `banco de dados` | Porta dentro da faixa do perfil do sistema `db` | `INFERRED` |

### Assinaturas WAF conhecidas

Detectadas por meio de um cabeçalho declarativo (`server`, `x-sdk`) — presença **declarada pelo alvo**, nunca verificada de forma independente: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (listado a título indicativo, não é propriamente um WAF de aplicação).

## 7. Política de confiança

Cada campo coletado traz um destes níveis:

| Nível | Significado |
|---|---|
| `VERIFIED` | Fato de protocolo observado diretamente, que o alvo não pode falsificar (ex.: porta fechada confirmada por um RST TCP, versão TLS realmente negociada). |
| `DECLARED` | Valor autoanunciado pelo alvo em um campo que ele controla totalmente (ex.: banner `Server`) — plausível, mas falsificável à vontade. |
| `CORROBORATED` | Um valor `DECLARED` confirmado por um indício independente (ex.: papel SSH, já que o protocolo foi de fato negociado). |
| `INFERRED` | Deduzido de um padrão/heurística, sem declaração explícita do alvo. |
| `UNKNOWN` | Nenhum indício utilizável, ou ocultado ativamente pelo alvo. |

## 8. Proteção contra valores falsificados

O Omega-check não confia em nenhum dado autodeclarado pelo alvo sem sinalizá-lo explicitamente. Um banner `Server` ou um cabeçalho `X-Powered-By` continua `DECLARED`, nunca `VERIFIED`, por mais plausível que seja — é o próprio alvo que os fornece e pode falsificá-los à vontade. Só uma confirmação por um canal independente (o protocolo SSH realmente negociado para o papel «acesso shell», por exemplo) faz uma informação passar a `CORROBORATED`. Essa distinção, mantida no `omega-lib` (`ConfidenceLevel`), é estrutural: nenhuma exportação e nenhuma visão podem ocultá-la.

## 9. Compatibilidade com terminais

A TUI (Textual) detecta automaticamente as capacidades do terminal (emulador, tamanho) e adapta sua folha de estilo estrutural de acordo (`complete`/`standard`/`reduced`/`mono`), sem opção manual. O modo CLI continua sempre em texto simples, independente do terminal. Política compartilhada por toda a suíte `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil conforme o emulador detectado

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antigo | `mono` |
| Emulador não reconhecido | `reduced` (alternativa padrão) |

### Perfil conforme o tamanho do terminal

| Tamanho mínimo (colunas × linhas) | Teto de perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| abaixo | `mono` |

O perfil final é **o mais restritivo dos dois** (emulador e tamanho) — um Ghostty em tela cheia redimensionado para 70 colunas desce para `mono`, mesmo que seu emulador permitisse `complete`. Atualizável ao vivo com a tecla `r`.

## 10. Exportações

Os relatórios de texto e HTML são escritos no idioma escolhido em Configurações («Idioma das exportações», por padrão o da interface); o JSON continua sendo um dado, não traduzido. Os relatórios são gerados em `var/exports/` por padrão (caminho de execução ancorado na pasta do projeto, `$OMEGA_CHECK_VAR_DIR` para alterá-lo), ou no caminho indicado (`--output` na CLI, caixa de diálogo na TUI). Nome de arquivo explícito e com data: `scan-{perfil}-{data}.ext`, `scan-custom-{data}.ext` para um perfil pessoal, `scan-{data}.ext` para uma entrada livre sem perfil.

### JSON, fonte de verdade

Estrutura completa do escaneamento (`Scan` + `Host`), estritamente serializável em JSON, níveis de confiança incluídos.

### Texto, relatório legível compacto

Legível fora do terminal, sem códigos ANSI.

### HTML, relatório web autônomo

5 temas à escolha (`--theme` na CLI, seletor na TUI; segue por padrão o tema ativo da interface quando existe um equivalente). Layout próprio: contêiner, grade de informações, quadros de estatísticas por estado de porta, selos coloridos — mesma família visual de `omega-scan`/`omega-stress`.

## 11. Histórico e comparação

Cada escaneamento é salvo (SQLite, `var/db/omega-check.db`): histórico consultável por alvo, detalhe de uma execução anterior, comparação entre dois escaneamentos (estado das portas) e repetição de um escaneamento no mesmo alvo sem redigitá-lo.

## 12. Testes

```bash
source .venv/bin/activate
lint-imports        # verifica a Dependency Rule
pytest -q           # 191 testes
ruff check src tests
mypy -p omega_check
```

Estrutura: `tests/unit/` (domínio e aplicação, sem E/S real), `tests/integration/` (SQLite/arquivos reais, servidor HTTP falso `pytest-httpserver`, TLS via `trustme`).

## 13. Fora do escopo

- Varredura de CVE
- Detecção ativa de SQLi, XSS, RCE
- Identificação do sistema operacional
- Técnicas de varredura de baixo nível no estilo nmap (SYN scan, pacotes brutos)
- Rastreamento (crawling)
- Fuzzing
- Força bruta
- Escaneamento simultâneo de vários alvos
- Painel web

---

> Omega-check — Escanear, identificar, qualificar, relatar.
> Um scanner de portas com confiança explícita, não uma suposição disfarçada de fato.
