<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (ver el archivo LICENSE) -->
<div align="center">
  <img src="../../assets/omega-check.png" alt="Omega-Check" width="384">
</div>

#  OMEGA-CHECK

**Escáner de puertos, servicios y roles de red (objetivo único)**

> Desarrollado por [kraynux](https://github.com/kraynux) para [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Página oficial: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Capturas: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interfaz e informes exportados disponibles en **17 idiomas** — ver [Idiomas de la interfaz](#idiomas-de-la-interfaz).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** es una herramienta TUI + CLI que escanea los puertos de un único objetivo de red, identifica el servicio que se ejecuta en cada puerto abierto (protocolo, software, versión, autenticación, WAF, TLS) e infiere su rol probable, sin realizar nunca un ataque activo. Herramienta de la suite `omega-`, estructurada en Clean Architecture — ver `docs/ARCHITECTURE.md` para todos los detalles técnicos.

## 1. Visión y alcance

Omega-check es un escáner de puertos orientado a la administración de sistemas: comprobar rápidamente qué escucha en una máquina (la propia, la LAN o un objetivo externo autorizado), con qué, y con cuánta confianza puede darse por cierta cada información.

### Lo que hace Omega-check

- Escanea una lista de puertos (perfil del sistema, perfil personal o entrada libre) en un objetivo único.
- Identifica el servicio que se ejecuta en cada puerto abierto: protocolo (HTTP/HTTPS/SSH/TLS/VNC/genérico), software y versión cuando están expuestos, necesidad de autenticación.
- Infiere un rol probable (servidor web, acceso shell, acceso gráfico, base de datos) a partir del protocolo realmente negociado, nunca de una simple suposición por el puerto.
- Detecta firmas de WAF conocidas (Cloudflare, Sucuri, Akamai, Imperva Incapsula) cuando aparecen declaradas en las cabeceras.
- Presenta el resultado en TUI (Textual) o en CLI scriptable, y mediante tres exportaciones: JSON, texto, HTML (5 temas).
- Asigna a cada información recogida un nivel de confianza explícito — ver [§7](#7-política-de-confianza).
- Conserva un historial persistente de escaneos, repetible y comparable en el tiempo.
- Permite fijar objetivos y crear perfiles de puertos personales, reutilizables de un escaneo a otro.

### Lo que Omega-check no hace

- Escaneo activo de vulnerabilidades: nada de SQLi, XSS ni RCE.
- Escaneo de CVE.
- Identificación del sistema operativo (el modelo de datos prevé el campo, ninguna heurística lo rellena por ahora).
- Técnicas de escaneo de bajo nivel al estilo nmap (SYN scan, paquetes en bruto) — solo conexión TCP de aplicación.
- Herramienta de fuerza bruta o de fuzzing.
- Escaneo paralelo de varios objetivos.
- Panel web.

## 2. Instalación

### Requisitos

- Python 3.10+
- Conexión a Internet, para las dependencias

### Instalación

```bash
[ -d omega-check ] && echo "ℹ️ Ya extraído aquí, paso omitido." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si aún no existe.
2. Instala las dependencias (`pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-check.sh` e `install.sh`.
4. Añade el alias `check` a `~/.bashrc` y `~/.zshrc` (sin duplicado si ya está presente).

### Dependencias

Declaradas en `pyproject.toml` (ya sin `requirements.txt`):
- `omega-lib`: biblioteca compartida de la suite (`ConfidenceLevel`, temas, detección del terminal)
- `textual`: interfaz TUI, temas, adaptación automática al terminal
- `httpx`: sonda HTTP/HTTPS
- `cryptography`: lectura del certificado TLS negociado
- `jinja2`: plantillas para la exportación HTML
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario — se lanza sin argumentos:

```bash
./omega-check.sh
```
si ha creado el alias, escriba simplemente `check` en el terminal:
```bash
check
```

Recorrido: pantalla de inicio (se cierra con una tecla o un clic) → menú principal (Escanear / Objetivos / Perfiles / Historial / Ajustes / Ayuda) → introducción del objetivo (con selector de objetivos fijados) y elección del perfil (aviso con `complet`, un segundo campo para un perfil personal o una entrada libre de puertos con `CUSTOM`) → escaneo (indicador indeterminado y registro de las operaciones de red en directo) → detalle del escaneo (puertos/servicios/roles, exportación) → historial/comparación/repetición y ajustes desde el menú principal. La adaptación al terminal (colores, tamaño, degradación estructural) es automática.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Moverse entre los elementos de una pantalla |
| `Tab` / `Mayús+Tab` | Moverse entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Tema siguiente (aplicado de inmediato, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir (con confirmación) |

### Idiomas de la interfaz

La interfaz está disponible en 17 idiomas: francés, inglés, español, portugués (Brasil), italiano, alemán, neerlandés, polaco, ruso, chino simplificado, vietnamita, tailandés, indonesio, japonés, coreano, hindi y árabe. La elección se hace en Ajustes («Langue / Language») y se aplica tras reiniciar la interfaz; la variable `OMEGA_CHECK_LANG` (por ejemplo `OMEGA_CHECK_LANG=es ./omega-check.sh`) fuerza un idioma durante una sesión. Lanzado desde omega-suite, omega-check adopta el idioma de la suite. En una consola de texto Linux (TTY), los idiomas de escritura no latina se muestran en inglés durante la sesión. La línea de comandos sigue en francés.

### Modo scriptable (CLI)

Cualquier subcomando activa el modo CLI:

```bash
# Escanear un objetivo con un perfil de puertos
./omega-check.sh scan 192.168.1.10 --profile minimal

# Historial (filtrable por objetivo)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Detalle de un escaneo (texto, JSON o HTML) — 5 temas de exportación a elegir
./omega-check.sh show <scan_id> --format html --theme omega-base --output informe.html

# Comparar dos escaneos (cambios de estado de puerto)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Perfiles de puertos personales
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
http://example.org          URL HTTP  (esquema eliminado antes de la resolución)
https://example.org:8443    URL HTTPS con puerto  (esquema y puerto eliminados)
```

El esquema y el puerto, si los hay, se eliminan antes de la resolución DNS (`domain/targets/validation.py::normalize_target_input`) — pegar una URL completa funciona, solo se conserva el host.

## 4. Perfiles de escaneo

| Perfil | Descripción | Fijado |
|---|---|---|
| `minimal` | Escaneo ultrarrápido: SSH + HTTP + HTTPS (22, 80, 443) | sí |
| `classic` | Servicios clásicos de Internet/LAN (37 puertos) | sí |
| `web` | Servicios web y alternativos | no |
| `db` | Bases de datos y servicios de datos | no |
| `remote` | Accesos remotos — shell, escritorio, RustDesk | no |
| `mail` | Servicios de correo | no |
| `dns` | Servicios DNS | no |
| `iot` | Equipos IoT, cámaras, routers, domótica | no |
| `dev` | Entornos de desarrollo/laboratorio | no |
| `docker` | Docker, Swarm y servicios habituales en contenedores | no |
| `complet` | **Generado al vuelo**: unión ordenada y sin duplicados de todos los perfiles anteriores | no |
| `CUSTOM` | Un perfil personal creado en la pantalla **Perfiles**, y/o una entrada libre (`80` / `22,443,8080` / `1000-2000`) — ambos se suman, sin duplicados | no |

Detalle completo, reglas de validación y gestión de los perfiles personales: `docs/PROFILES.md`.

## 5. Arquitectura

Omega-check está estructurado en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineada con la plantilla de la suite `omega-` (ver `omega-scan`/`omega-stress`) y verificada por `import-linter` en cada cambio. Todos los detalles están en **`docs/ARCHITECTURE.md`**.

Vista general muy breve:

```text
src/omega_check/
├── domain/          Lógica de negocio pura (escaneos, objetivos, servicios, perfiles, informes...)
├── application/     Casos de uso (commands/queries)
├── ports/           Contratos que espera la aplicación (sondas, repositorios, exportadores...)
├── infrastructure/  Implementaciones concretas (socket/httpx/cryptography, SQLite; Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (scriptable), con paridad funcional estricta
├── app/             Ensamblaje (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulario transversal, utilidades no de negocio
└── plugins/         Estructura preparada, vacía (ningún eje de extensión confirmado)
```

Reglas de diseño:
- `domain/services/policies.py`: clasifica los indicios ya recogidos, nunca hace red.
- `infrastructure/network/`: hace red (sockets, `httpx`, `cryptography`), nunca juzga.
- `interfaces/`: muestra, no contiene ninguna lógica de negocio.
- `infrastructure/exporters/`: leen el resultado del escaneo, no recalculan nada.

## 6. Identificación de servicios y roles

### Protocolos detectados

| Protocolo | Sonda | Detalle recogido |
|---|---|---|
| HTTP / HTTPS | `httpx` | Banner `Server`, cabeceras de autenticación |
| TLS | `cryptography` (certificado negociado, `CERT_NONE` incluido) | Versión, cifrado, sujeto/emisor del certificado |
| SSH | Banner en bruto | Software y versión (p. ej. `OpenSSH 10.4`) |
| VNC (RFB) | Códigos de seguridad anunciados por el servidor | Tipos de autenticación admitidos |
| Genérico | Banner en bruto en un puerto abierto no reconocido | Extracción prudente, sin heurística agresiva |

### Roles inferidos

Deducidos del protocolo **realmente negociado**, nunca de una suposición por el número de puerto:

| Rol | Condición | Confianza |
|---|---|---|
| `servidor web` | Protocolo HTTP/HTTPS confirmado | `INFERRED` |
| `acceso shell` | Protocolo SSH confirmado | `CORROBORATED` |
| `acceso gráfico` | Protocolo VNC confirmado | `CORROBORATED` |
| `base de datos` | Puerto dentro del rango del perfil del sistema `db` | `INFERRED` |

### Firmas WAF conocidas

Detectadas mediante una cabecera declarativa (`server`, `x-sdk`) — presencia **declarada por el objetivo**, nunca verificada de forma independiente: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (listado a título indicativo, no es estrictamente un WAF de aplicación).

## 7. Política de confianza

Cada campo recogido lleva uno de estos niveles:

| Nivel | Significado |
|---|---|
| `VERIFIED` | Hecho de protocolo observado directamente, que el objetivo no puede falsificar (p. ej.: puerto cerrado confirmado por un RST TCP, versión TLS realmente negociada). |
| `DECLARED` | Valor autoanunciado por el objetivo en un campo que controla por completo (p. ej.: banner `Server`) — plausible pero falsificable a voluntad. |
| `CORROBORATED` | Un valor `DECLARED` confirmado por un indicio independiente (p. ej.: rol SSH, al haberse negociado realmente el protocolo). |
| `INFERRED` | Deducido de un patrón/heurística, sin declaración explícita del objetivo. |
| `UNKNOWN` | Ningún indicio aprovechable, u ocultado activamente por el objetivo. |

## 8. Protección contra valores falsificados

Omega-check no confía en ningún dato autodeclarado por el objetivo sin señalarlo explícitamente. Un banner `Server` o una cabecera `X-Powered-By` siguen siendo `DECLARED`, nunca `VERIFIED`, por plausibles que parezcan — es el propio objetivo quien los proporciona y puede falsificarlos a voluntad. Solo una confirmación por un canal independiente (el protocolo SSH realmente negociado para el rol «acceso shell», por ejemplo) hace pasar una información a `CORROBORATED`. Esta distinción, llevada en `omega-lib` (`ConfidenceLevel`), es estructural: ninguna exportación ni ninguna vista puede ocultarla.

## 9. Compatibilidad con terminales

La TUI (Textual) detecta automáticamente las capacidades del terminal (emulador, tamaño) y adapta en consecuencia su hoja de estilo estructural (`complete`/`standard`/`reduced`/`mono`), sin opción manual. El modo CLI siempre sigue en texto simple, independiente del terminal. Política compartida por toda la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil según el emulador detectado

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antiguo | `mono` |
| Emulador no reconocido | `reduced` (valor de reserva por defecto) |

### Perfil según el tamaño del terminal

| Tamaño mínimo (columnas × líneas) | Tope de perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| por debajo | `mono` |

El perfil final es **el más restrictivo de los dos** (emulador y tamaño) — un Ghostty a pantalla completa redimensionado a 70 columnas baja a `mono`, aunque su emulador permitiría `complete`. Se puede actualizar en directo con la tecla `r`.

## 10. Exportaciones

Los informes de texto y HTML se escriben en el idioma elegido en Ajustes («Idioma de las exportaciones», por defecto el de la interfaz); el JSON sigue siendo un dato, sin traducir. Los informes se generan por defecto en `var/exports/` (ruta de ejecución anclada en la carpeta del proyecto, `$OMEGA_CHECK_VAR_DIR` para cambiarla), o en la ruta indicada (`--output` en CLI, cuadro de diálogo en la TUI). Nombre de archivo explícito y con fecha: `scan-{perfil}-{fecha}.ext`, `scan-custom-{fecha}.ext` para un perfil personal, `scan-{fecha}.ext` para una entrada libre sin perfil.

### JSON, fuente de verdad

Estructura completa del escaneo (`Scan` + `Host`), estrictamente serializable en JSON, niveles de confianza incluidos.

### Texto, informe legible compacto

Legible fuera del terminal, sin códigos ANSI.

### HTML, informe web autónomo

5 temas a elegir (`--theme` en CLI, selector en la TUI; sigue por defecto el tema activo de la interfaz cuando existe un equivalente). Maquetación propia: contenedor, cuadrícula de información, recuadros de estadísticas por estado de puerto, insignias de colores — misma familia visual que `omega-scan`/`omega-stress`.

## 11. Historial y comparación

Cada escaneo se guarda (SQLite, `var/db/omega-check.db`): historial consultable por objetivo, detalle de una ejecución anterior, comparación entre dos escaneos (estado de los puertos) y repetición de un escaneo sobre el mismo objetivo sin volver a introducirlo.

## 12. Pruebas

```bash
source .venv/bin/activate
lint-imports        # comprueba la Dependency Rule
pytest -q           # 191 pruebas
ruff check src tests
mypy -p omega_check
```

Estructura: `tests/unit/` (dominio y aplicación, sin E/S real), `tests/integration/` (SQLite/archivos reales, servidor HTTP ficticio `pytest-httpserver`, TLS mediante `trustme`).

## 13. Fuera de alcance

- Escaneo de CVE
- Detección activa de SQLi, XSS, RCE
- Identificación del sistema operativo
- Técnicas de escaneo de bajo nivel al estilo nmap (SYN scan, paquetes en bruto)
- Rastreo (crawling)
- Fuzzing
- Fuerza bruta
- Escaneo simultáneo de varios objetivos
- Panel web

---

> Omega-check — Escanear, identificar, calificar, informar.
> Un escáner de puertos con una confianza explícita, no una suposición disfrazada de hecho.
