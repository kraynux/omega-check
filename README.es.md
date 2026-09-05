<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (consulta el archivo LICENSE) -->
<div align="center">
  <img src="docs/assets/omega-check.png" alt="Omega-Check" width="256">
</div>

#  OMEGA-CHECK

**Escáner de puertos, servicios y roles de red para un único objetivo**

> Desarrollado por **kraynux** para **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Vista previa: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

**Idiomas:**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-check** es una herramienta TUI + CLI que escanea los puertos de un único objetivo de red, identifica el servicio que se ejecuta en cada puerto abierto (protocolo, software, versión, autenticación, WAF y TLS) e infiere su rol probable sin realizar nunca un ataque activo. Es la cuarta herramienta de la suite `omega-` (después de `omega-fire`, `omega-stress` y `omega-scan`) y está estructurada según Clean Architecture; consulta `docs/ARCHITECTURE.md` para ver todos los detalles técnicos.

## 1. Visión y alcance

Omega-check es un escáner de puertos orientado a la administración de sistemas: comprueba rápidamente qué está escuchando en una máquina (la propia, una máquina de la LAN o un objetivo externo autorizado), qué servicio hay detrás y con qué nivel de confianza puede aceptarse cada información.

### Qué hace Omega-check

- Escanea una lista de puertos (perfil del sistema, perfil personal o entrada libre) sobre un único objetivo.
- Identifica el servicio de cada puerto abierto: protocolo (HTTP/HTTPS/SSH/TLS/VNC/genérico), software y versión cuando se exponen, y requisitos de autenticación.
- Infiere un rol probable (servidor web, acceso shell, acceso gráfico o base de datos) a partir del protocolo realmente negociado, nunca de una simple suposición basada en el número de puerto.
- Detecta firmas WAF conocidas (Cloudflare, Sucuri, Akamai e Imperva Incapsula) cuando aparecen declaradas en las cabeceras.
- Presenta el resultado en una TUI de Textual o en un CLI programable y ofrece tres formatos de exportación: JSON, texto y HTML (5 temas).
- Asigna un nivel de confianza explícito a cada dato recopilado; consulta [§7](#7-política-de-confianza).
- Conserva un historial persistente de los escaneos, que se puede repetir y comparar con el tiempo.
- Permite fijar objetivos y crear perfiles personales de puertos reutilizables entre escaneos.

### Qué no hace Omega-check

- No realiza escaneo activo de vulnerabilidades, SQLi, XSS ni RCE.
- No escanea CVE.
- No realiza fingerprinting del sistema operativo (el modelo de datos contempla el campo, pero ninguna heurística lo rellena actualmente).
- No utiliza técnicas de escaneo de bajo nivel como nmap (SYN scan, paquetes sin procesar): solo conexiones TCP de nivel aplicativo.
- No es una herramienta de bruteforce ni fuzzing.
- No realiza escaneo paralelo de múltiples objetivos.
- No proporciona un dashboard web.

## 2. Instalación

### Requisitos

- Python 3.10+
- Conexión a Internet para las dependencias

### Instalación

```bash
[ -d omega-check ] && echo "ℹ️ Ya está extraído aquí; se omite el paso." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si todavía no existe.
2. Instala las dependencias (`pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-check.sh` e `install.sh`.
4. Añade el alias `check` a `~/.bashrc` y `~/.zshrc` sin duplicarlo.

### Dependencias

Declaradas en `pyproject.toml` (ya no existe `requirements.txt`):
- `omega-lib`: biblioteca compartida de la suite (`ConfidenceLevel`, temas y detección del terminal).
- `textual`: interfaz TUI, temas y adaptación automática al terminal.
- `httpx`: sonda HTTP/HTTPS.
- `cryptography`: lectura del certificado TLS negociado.
- `jinja2`: plantillas para la exportación HTML.
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`.

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario; se inicia sin argumentos:

```bash
./omega-check.sh
```

Si se creó el alias, escribe simplemente `check` en el terminal:

```bash
check
```

Flujo: pantalla de inicio (se cierra con una tecla o un clic) → menú principal (Escáner / Objetivos / Perfiles / Historial / Ajustes / Ayuda) → introducción del objetivo (con selector de objetivos fijados) y elección del perfil (advertencia para `complet`, segundo campo para un perfil personal o entrada libre de puertos con `CUSTOM`) → escaneo (barra de progreso indeterminada y operaciones de red en directo) → detalles del escaneo (puertos/servicios/roles y exportación) → historial, comparación, repetición y ajustes desde el menú principal. La adaptación al terminal (colores, tamaño y degradación estructural) es automática.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Navegar entre los elementos de una pantalla |
| `Tab` / `Mayús+Tab` | Navegar entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Siguiente tema (se aplica inmediatamente, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir con confirmación |

### Modo programable (CLI)

Cualquier subcomando inicia el modo CLI:

```bash
# Escanear un objetivo con un perfil de puertos
./omega-check.sh scan 192.168.1.10 --profile minimal

# Historial (filtrable por objetivo)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Detalle de un escaneo (texto, JSON o HTML), con 5 temas disponibles
./omega-check.sh show <scan_id> --format html --theme omega-base --output informe.html

# Comparar dos escaneos (cambios en el estado de los puertos)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Perfiles personales de puertos
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Mi perfil"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Formatos de objetivo aceptados

```text
192.168.1.10                IPv4
example.org                 Nombre de host
http://example.org          URL HTTP (se elimina el esquema antes de resolver)
https://example.org:8443    URL HTTPS con puerto (se eliminan esquema y puerto)
```

El esquema y el puerto, si existen, se eliminan antes de la resolución DNS (`domain/targets/validation.py::normalize_target_input`): se puede pegar una URL completa y solo se conserva el host.

## 4. Perfiles de escaneo

| Perfil | Descripción | Fijado |
|---|---|---|
| `minimal` | Escaneo ultrarrápido: SSH + HTTP + HTTPS (22, 80, 443) | sí |
| `classic` | Servicios clásicos de Internet/LAN (37 puertos) | sí |
| `web` | Servicios web y alternativas | no |
| `db` | Bases de datos y servicios de datos | no |
| `remote` | Acceso remoto: shell, escritorio y RustDesk | no |
| `mail` | Servicios de correo | no |
| `dns` | Servicios DNS | no |
| `iot` | Equipos IoT, cámaras, gateways y domótica | no |
| `dev` | Entornos de desarrollo/laboratorio | no |
| `docker` | Docker, Swarm y servicios habituales en contenedores | no |
| `complet` | **Generado al vuelo**: unión ordenada y sin duplicados de todos los perfiles anteriores | no |
| `CUSTOM` | Perfil personal creado en **Perfiles** y/o entrada libre (`80` / `22,443,8080` / `1000-2000`); ambas fuentes se combinan sin duplicados | no |

Descripción completa, reglas de validación y gestión de perfiles personales: `docs/PROFILES.md`.

## 5. Arquitectura

Omega-check está estructurado mediante **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineado con la plantilla de la suite `omega-` (consulta `omega-scan`/`omega-stress`) y verificado por `import-linter` tras cada modificación. El detalle completo se encuentra en **`docs/ARCHITECTURE.md`**.

```text
src/omega_check/
├── domain/          Lógica de negocio pura (escaneos, objetivos, servicios, perfiles, informes...)
├── application/     Casos de uso (commands/queries)
├── ports/           Contratos esperados por la aplicación (probers, repositories, exporters...)
├── infrastructure/  Implementaciones concretas (socket/httpx/cryptography, SQLite; Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (programable), con estricta paridad funcional
├── app/             Ensamblaje (DependencyContainer, bootstrap y ciclo de vida)
├── core/, shared/   Vocabulario transversal y utilidades no pertenecientes al dominio
└── plugins/         Estructura preparada y vacía (sin eje de extensión confirmado)
```

Reglas de diseño:
- `domain/services/policies.py`: clasifica los indicios ya recopilados y nunca realiza operaciones de red.
- `infrastructure/network/`: realiza operaciones de red (sockets, `httpx`, `cryptography`) y nunca juzga.
- `interfaces/`: muestra datos y no contiene lógica de negocio.
- `infrastructure/exporters/`: lee los resultados del escaneo y nunca los recalcula.

## 6. Identificación de servicios y roles

### Protocolos detectados

| Protocolo | Sonda | Datos recopilados |
|---|---|---|
| HTTP / HTTPS | `httpx` | Banner `Server`, cabeceras de autenticación |
| TLS | `cryptography` (certificado negociado, incluido `CERT_NONE`) | Versión, cipher, sujeto/emisor del certificado |
| SSH | Banner sin procesar | Software y versión (por ejemplo, `OpenSSH 10.4`) |
| VNC (RFB) | Códigos de seguridad anunciados por el servidor | Tipos de autenticación compatibles |
| Genérico | Banner sin procesar en un puerto abierto no reconocido | Extracción prudente, sin heurística agresiva |

### Roles inferidos

Se deducen del protocolo **realmente negociado**, nunca de una suposición basada en el número de puerto:

| Rol | Condición | Confianza |
|---|---|---|
| `servidor web` | Protocolo HTTP/HTTPS confirmado | `INFERRED` |
| `acceso shell` | Protocolo SSH confirmado | `CORROBORATED` |
| `acceso gráfico` | Protocolo VNC confirmado | `CORROBORATED` |
| `base de datos` | El puerto pertenece al rango del perfil de sistema `db` | `INFERRED` |

### Firmas WAF conocidas

Se detectan mediante cabeceras declarativas (`server`, `x-sdk`); su presencia es **declarada por el objetivo** y nunca se verifica de forma independiente: Cloudflare, Sucuri, Akamai, Imperva Incapsula y AWS ELB (incluido como referencia; estrictamente, no es un WAF de aplicación).

## 7. Política de confianza

Cada campo recopilado recibe uno de estos niveles:

| Nivel | Significado |
|---|---|
| `VERIFIED` | Hecho protocolario observado directamente que el objetivo no puede falsificar (por ejemplo, un puerto cerrado confirmado por TCP RST o la versión TLS realmente negociada). |
| `DECLARED` | Valor anunciado por el objetivo en un campo que controla por completo (por ejemplo, el banner `Server`); plausible, pero falsificable libremente. |
| `CORROBORATED` | Valor `DECLARED` confirmado por una señal independiente (por ejemplo, un rol SSH después de negociar realmente el protocolo). |
| `INFERRED` | Deducción basada en un patrón o heurística sin declaración explícita del objetivo. |
| `UNKNOWN` | No hay pruebas útiles o el objetivo las oculta activamente. |

## 8. Protección contra valores falsificados

Omega-check no confía en los datos autodeclarados por el objetivo sin indicarlo claramente. Un banner `Server` o una cabecera `X-Powered-By` sigue siendo `DECLARED`, nunca `VERIFIED`, independientemente de su plausibilidad: el objetivo los proporciona y puede falsificarlos. Solo la confirmación mediante un canal independiente (por ejemplo, el protocolo SSH realmente negociado para el rol «acceso shell») eleva la información a `CORROBORATED`. Esta distinción, implementada en `omega-lib` (`ConfidenceLevel`), es estructural: ninguna exportación ni vista puede ocultarla.

## 9. Compatibilidad con terminales

La TUI de Textual detecta automáticamente las capacidades del terminal (emulador y tamaño) y adapta su hoja de estilos estructural (`complete`/`standard`/`reduced`/`mono`) sin flags manuales. El modo CLI siempre usa texto simple y es independiente del terminal. La política es compartida por toda la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil según el emulador

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antiguo | `mono` |
| Emulador no reconocido | `reduced` (fallback predeterminado) |

### Perfil según el tamaño del terminal

| Tamaño mínimo (columnas × filas) | Límite de perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| inferior | `mono` |

El perfil final es **el más restrictivo de los dos** (emulador y tamaño). Un Ghostty en pantalla completa reducido a 70 columnas bajará a `mono`, aunque su emulador permitiera `complete`. Se puede actualizar en directo con la tecla `r`.

## 10. Exportaciones

Los informes se generan por defecto en `var/exports/` (ruta de ejecución anclada al directorio del proyecto; se puede sobrescribir con `$OMEGA_CHECK_VAR_DIR`) o en la ruta indicada (`--output` en CLI, diálogo en TUI). Se utilizan nombres explícitos con marca temporal: `scan-{perfil}-{fecha}.ext`, `scan-custom-{fecha}.ext` para un perfil personal y `scan-{fecha}.ext` para una entrada libre sin perfil.

### JSON, fuente de verdad

Estructura completa del escaneo (`Scan` + `Host`), estrictamente serializable como JSON e incluyendo los niveles de confianza.

### Texto, informe humano compacto

Legible fuera del terminal, sin códigos ANSI.

### HTML, informe web autónomo

5 temas disponibles (`--theme` en CLI o selector en TUI; por defecto sigue el tema activo de la interfaz si existe un equivalente). Diseño específico con cuadrícula de información, estadísticas del estado de los puertos y badges de colores, en la misma familia visual que `omega-scan`/`omega-stress`.

## 11. Historial y comparación

Cada escaneo se persiste en SQLite (`var/db/omega-check.db`): historial consultable por objetivo, detalles de ejecuciones anteriores, comparación entre dos escaneos (estados de los puertos) y repetición de un escaneo sobre el mismo objetivo sin volver a introducirlo.

## 12. Pruebas

```bash
source .venv/bin/activate
lint-imports        # verifica la Dependency Rule
pytest -q           # 173 pruebas
ruff check src tests
mypy -p omega_check
```

Estructura: `tests/unit/` (dominio y aplicación, sin I/O real), `tests/integration/` (SQLite/archivos reales, servidor HTTP ficticio `pytest-httpserver`, TLS mediante `trustme`).

## 13. Fuera del alcance

- Escaneo de CVE.
- Detección activa de SQLi, XSS y RCE.
- Identificación del sistema operativo.
- Técnicas de escaneo de bajo nivel como nmap (SYN scan, paquetes sin procesar).
- Crawling.
- Fuzzing.
- Bruteforce.
- Escaneo simultáneo de múltiples objetivos.
- Dashboard web.

---

> Omega-check — escanear, identificar, calificar e informar.  
> Un escáner de puertos con confianza explícita, no una suposición disfrazada de hecho.
