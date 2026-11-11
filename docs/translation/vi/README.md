<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Giấy phép MIT (xem tệp LICENSE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-check.png" alt="Omega-Check" width="512">
</div>

#  OMEGA-CHECK

**Công cụ quét cổng, dịch vụ và vai trò mạng (một mục tiêu)**

> Được [kraynux](https://github.com/kraynux) xây dựng cho [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Trang chính thức: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; Ảnh chụp màn hình: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Giao diện và báo cáo xuất có sẵn bằng **17 ngôn ngữ** — xem [Ngôn ngữ giao diện](#ngôn-ngữ-giao-diện).  
**Ngôn ngữ:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-check** là công cụ TUI + CLI quét các cổng của một mục tiêu mạng duy nhất, nhận diện dịch vụ chạy trên mỗi cổng mở (giao thức, phần mềm, phiên bản, xác thực, WAF, TLS) và suy ra vai trò có khả năng của nó, không bao giờ thực hiện tấn công chủ động. Đây là một công cụ của bộ `omega-`, được tổ chức theo Clean Architecture — xem `docs/ARCHITECTURE.md` để biết đầy đủ chi tiết kỹ thuật.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-check/D.png" width="24%" />
</p>

## 1. Tầm nhìn và phạm vi

Omega-check là công cụ quét cổng hướng tới quản trị hệ thống: kiểm tra nhanh những gì đang lắng nghe trên một máy (máy của bạn, mạng LAN, hoặc một mục tiêu bên ngoài được phép), bằng gì, và mỗi thông tin đáng tin đến mức nào.

### Omega-check làm gì

- Quét một danh sách cổng (cấu hình hệ thống, cấu hình cá nhân hoặc nhập tự do) trên một mục tiêu duy nhất.
- Nhận diện dịch vụ chạy trên mỗi cổng mở: giao thức (HTTP/HTTPS/SSH/TLS/VNC/chung), phần mềm và phiên bản khi chúng được lộ ra, yêu cầu xác thực.
- Suy ra một vai trò có khả năng (máy chủ web, truy cập shell, truy cập đồ họa, cơ sở dữ liệu) từ giao thức thực sự được thương lượng, không bao giờ chỉ dựa vào phỏng đoán theo số cổng.
- Phát hiện chữ ký WAF đã biết (Cloudflare, Sucuri, Akamai, Imperva Incapsula) khi chúng được khai báo trong tiêu đề.
- Hiển thị kết quả trong TUI (Textual) hoặc CLI có thể viết script, và qua ba kiểu xuất: JSON, văn bản, HTML (5 giao diện màu).
- Gán cho mỗi thông tin thu thập một mức độ tin cậy rõ ràng — xem [§7](#7-chính-sách-tin-cậy).
- Lưu lịch sử quét lâu dài, có thể chạy lại và so sánh theo thời gian.
- Cho phép ghim mục tiêu và tạo cấu hình cổng cá nhân, dùng lại giữa các lần quét.

### Omega-check không làm gì

- Quét lỗ hổng chủ động: không SQLi, XSS hay RCE.
- Quét CVE.
- Nhận diện hệ điều hành (mô hình dữ liệu có sẵn trường này, nhưng hiện chưa có quy tắc suy đoán nào điền vào).
- Kỹ thuật quét cấp thấp kiểu nmap (quét SYN, gói tin thô) — chỉ kết nối TCP ở tầng ứng dụng.
- Công cụ dò mật khẩu hay fuzzing.
- Quét song song nhiều mục tiêu.
- Bảng điều khiển web.

## 2. Cài đặt

### Yêu cầu

- Python 3.10+
- Kết nối Internet, để cài các phụ thuộc

### Cài đặt

```bash
[ -d omega-check ] && echo "ℹ️ Đã giải nén ở đây, bỏ qua bước này." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Tạo môi trường ảo `.venv` nếu chưa có.
2. Cài các phụ thuộc (`pip install -e .`; `pyproject.toml` vẫn là nguồn chuẩn duy nhất).
3. Cấp quyền thực thi cho `omega-check.sh` và `install.sh`.
4. Thêm bí danh `check` vào `~/.bashrc` và `~/.zshrc` (không trùng lặp nếu đã có).

### Phụ thuộc

Khai báo trong `pyproject.toml` (không còn `requirements.txt`):
- `omega-lib`: thư viện dùng chung của bộ công cụ (`ConfidenceLevel`, giao diện màu, nhận diện terminal)
- `textual`: giao diện TUI, giao diện màu, tự động thích ứng với terminal
- `httpx`: thăm dò HTTP/HTTPS
- `cryptography`: đọc chứng chỉ TLS đã thương lượng
- `jinja2`: mẫu cho bản xuất HTML
- Phụ thuộc phát triển (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Sử dụng

### Chế độ tương tác (TUI)

Khuyên dùng hằng ngày — chạy không có đối số:

```bash
./omega-check.sh
```
nếu đã tạo bí danh, chỉ cần gõ `check` trong terminal:
```bash
check
```

Trình tự: màn hình khởi động (đóng bằng một phím hoặc một cú nhấp) → menu chính (Quét / Mục tiêu / Cấu hình / Lịch sử / Thiết lập / Trợ giúp) → nhập mục tiêu (có bộ chọn mục tiêu đã ghim) và chọn cấu hình (cảnh báo với `complet`, trường thứ hai cho cấu hình cá nhân hoặc nhập cổng tự do với `CUSTOM`) → quét (thanh tiến trình không xác định và nhật ký thao tác mạng trực tiếp) → chi tiết lần quét (cổng/dịch vụ/vai trò, xuất) → lịch sử/so sánh/chạy lại và thiết lập từ menu chính. Việc thích ứng với terminal (màu, kích thước, giản lược cấu trúc) là tự động.

#### Phím tắt

| Phím | Thao tác |
|---|---|
| `↑` / `↓` | Di chuyển giữa các mục trên màn hình |
| `Tab` / `Shift+Tab` | Di chuyển giữa các trường của biểu mẫu |
| `Esc` | Quay lại màn hình trước (xác nhận thoát ở màn hình chính) |
| `t` | Giao diện màu tiếp theo (áp dụng ngay, không cần xác nhận) |
| `r` | Làm mới việc nhận diện terminal |
| `a` | Hiện trợ giúp |
| `q` | Thoát (có xác nhận) |

### Ngôn ngữ giao diện

Giao diện có sẵn bằng 17 ngôn ngữ: tiếng Pháp, tiếng Anh, tiếng Tây Ban Nha, tiếng Bồ Đào Nha (Brasil), tiếng Ý, tiếng Đức, tiếng Hà Lan, tiếng Ba Lan, tiếng Nga, tiếng Trung giản thể, tiếng Việt, tiếng Thái, tiếng Indonesia, tiếng Nhật, tiếng Hàn, tiếng Hindi và tiếng Ả Rập. Ngôn ngữ được chọn trong Thiết lập (“Langue / Language”) và có hiệu lực sau khi khởi động lại giao diện; biến `OMEGA_CHECK_LANG` (ví dụ `OMEGA_CHECK_LANG=vi ./omega-check.sh`) buộc dùng một ngôn ngữ trong một phiên. Khi được chạy từ omega-suite, omega-check dùng ngôn ngữ của bộ công cụ. Trên console văn bản Linux (TTY), giao diện hiển thị bằng tiếng Anh trong phiên đó đối với tiếng Việt và các ngôn ngữ không dùng chữ Latinh. Dòng lệnh vẫn bằng tiếng Pháp.

### Liên hệ và hỗ trợ

Phần trợ giúp (phím `a`) có màn hình **Liên hệ và hỗ trợ**: *Mời một ly cà phê* (trang PayPal của nhà phát triển), *Liên hệ hỗ trợ* (địa chỉ email và biểu mẫu liên hệ của trang web, hiển thị rõ ràng), *Khai báo là người dùng (ẩn danh)* và *Kiểm tra cập nhật*. Việc khai báo là tự nguyện, tắt theo mặc định và chỉ gửi một lần: nó chỉ dùng để đếm số người dùng và, nếu bạn muốn, châu lục hoặc quốc gia của họ (danh sách đóng, không bao giờ là văn bản tự do). Nó gửi một khóa được tạo ngẫu nhiên, tên phần mềm (`omega-check`) và phiên bản của nó; không bao giờ gửi tên, tên máy, thiết lập, mục tiêu hay kết quả. Địa chỉ IP không được lưu trong các khai báo, nhưng, như mọi lượt truy cập, nó đi qua các kiểm tra bảo mật và nhật ký của máy chủ nhận. Có thể rút lại bất cứ lúc nào từ cùng màn hình (*Không khai báo tôi nữa*). Việc kiểm tra cập nhật chỉ đọc danh sách các phiên bản đã phát hành trên trang web, và không bao giờ khi chưa nhấp.

### Chế độ script (CLI)

Bất kỳ lệnh con nào cũng kích hoạt chế độ CLI:

```bash
# Quét một mục tiêu với một cấu hình cổng
./omega-check.sh scan 192.168.1.10 --profile minimal

# Lịch sử (lọc được theo mục tiêu)
./omega-check.sh history --target 192.168.1.10 --limit 20

# Chi tiết một lần quét (văn bản, JSON hoặc HTML) — chọn 1 trong 5 giao diện xuất
./omega-check.sh show <scan_id> --format html --theme omega-base --output baocao.html

# So sánh hai lần quét (thay đổi trạng thái cổng)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# Cấu hình cổng cá nhân
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "Cấu hình của tôi"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### Định dạng mục tiêu được chấp nhận

```text
192.168.1.10                IPv4
example.org                 Tên máy chủ
http://example.org          URL HTTP  (bỏ giao thức trước khi phân giải)
https://example.org:8443    URL HTTPS có cổng  (bỏ giao thức và cổng)
```

Giao thức và cổng (nếu có) được bỏ đi trước khi phân giải DNS (`domain/targets/validation.py::normalize_target_input`) — dán nguyên một URL vẫn được, chỉ giữ lại máy chủ.

## 4. Cấu hình quét

| Cấu hình | Mô tả | Đã ghim |
|---|---|---|
| `minimal` | Quét siêu nhanh: SSH + HTTP + HTTPS (22, 80, 443) | có |
| `classic` | Dịch vụ Internet/LAN thông dụng (37 cổng) | có |
| `web` | Dịch vụ web và cổng thay thế | không |
| `db` | Cơ sở dữ liệu và dịch vụ dữ liệu | không |
| `remote` | Truy cập từ xa — shell, màn hình, RustDesk | không |
| `mail` | Dịch vụ thư | không |
| `dns` | Dịch vụ DNS | không |
| `iot` | Thiết bị IoT, camera, bộ định tuyến, nhà thông minh | không |
| `dev` | Môi trường phát triển/thử nghiệm | không |
| `docker` | Docker, Swarm và các dịch vụ thường chạy trong container | không |
| `complet` | **Tạo tức thì**: hợp đã sắp xếp và loại trùng của mọi cấu hình ở trên | không |
| `CUSTOM` | Một cấu hình cá nhân tạo trong màn hình **Cấu hình**, và/hoặc nhập tự do (`80` / `22,443,8080` / `1000-2000`) — hai thứ cộng dồn, loại trùng | không |

Chi tiết đầy đủ, quy tắc kiểm tra và quản lý cấu hình cá nhân: `docs/PROFILES.md`.

## 5. Kiến trúc

Omega-check được tổ chức theo **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), thống nhất với mẫu của bộ `omega-` (xem `omega-scan`/`omega-stress`) và được `import-linter` kiểm tra ở mỗi thay đổi. Chi tiết đầy đủ nằm trong **`docs/ARCHITECTURE.md`**.

Tổng quan rất ngắn:

```text
src/omega_check/
├── domain/          Logic nghiệp vụ thuần (quét, mục tiêu, dịch vụ, cấu hình, báo cáo...)
├── application/     Ca sử dụng (commands/queries)
├── ports/           Hợp đồng mà ứng dụng cần (bộ thăm dò, kho lưu trữ, bộ xuất...)
├── infrastructure/  Triển khai cụ thể (socket/httpx/cryptography, SQLite; Textual KHÔNG nằm ở đây)
├── interfaces/      tui/ (Textual) và cli/ (viết script được), tương đương chức năng nghiêm ngặt
├── app/             Lắp ráp (DependencyContainer, bootstrap, vòng đời)
├── core/, shared/   Từ vựng dùng chung, tiện ích không thuộc nghiệp vụ
└── plugins/         Đã có cấu trúc, đang trống (chưa có hướng mở rộng nào được xác nhận)
```

Quy tắc thiết kế:
- `domain/services/policies.py`: phân loại các dấu hiệu đã thu thập, không bao giờ truy cập mạng.
- `infrastructure/network/`: truy cập mạng (socket, `httpx`, `cryptography`), không bao giờ đánh giá.
- `interfaces/`: hiển thị, không chứa logic nghiệp vụ nào.
- `infrastructure/exporters/`: đọc kết quả quét, không tính lại gì cả.

## 6. Nhận diện dịch vụ và vai trò

### Giao thức được phát hiện

| Giao thức | Cách thăm dò | Chi tiết thu thập |
|---|---|---|
| HTTP / HTTPS | `httpx` | Banner `Server`, tiêu đề xác thực |
| TLS | `cryptography` (chứng chỉ đã thương lượng, kể cả `CERT_NONE`) | Phiên bản, bộ mã hóa, chủ thể/bên cấp chứng chỉ |
| SSH | Banner thô | Phần mềm và phiên bản (ví dụ `OpenSSH 10.4`) |
| VNC (RFB) | Mã bảo mật do máy chủ công bố | Các kiểu xác thực được hỗ trợ |
| Chung | Banner thô trên cổng mở không nhận diện được | Trích xuất thận trọng, không dùng suy đoán mạnh tay |

### Vai trò được suy ra

Suy ra từ giao thức **thực sự được thương lượng**, không bao giờ từ phỏng đoán theo số cổng:

| Vai trò | Điều kiện | Độ tin cậy |
|---|---|---|
| `máy chủ web` | Đã xác nhận giao thức HTTP/HTTPS | `INFERRED` |
| `truy cập shell` | Đã xác nhận giao thức SSH | `CORROBORATED` |
| `truy cập đồ họa` | Đã xác nhận giao thức VNC | `CORROBORATED` |
| `cơ sở dữ liệu` | Cổng nằm trong dải của cấu hình hệ thống `db` | `INFERRED` |

### Chữ ký WAF đã biết

Phát hiện qua một tiêu đề khai báo (`server`, `x-sdk`) — sự hiện diện **do mục tiêu tự khai báo**, không bao giờ được xác minh độc lập: Cloudflare, Sucuri, Akamai, Imperva Incapsula, AWS ELB (liệt kê để tham khảo, thực ra không hẳn là WAF ứng dụng).

## 7. Chính sách tin cậy

Mỗi trường thu thập mang một trong các mức sau:

| Mức | Ý nghĩa |
|---|---|
| `VERIFIED` | Sự kiện giao thức quan sát trực tiếp, mục tiêu không thể giả mạo (ví dụ: cổng đóng được xác nhận bằng TCP RST, phiên bản TLS thực sự được thương lượng). |
| `DECLARED` | Giá trị do mục tiêu tự công bố trong một trường mà nó hoàn toàn kiểm soát (ví dụ: banner `Server`) — có vẻ hợp lý nhưng có thể giả mạo tùy ý. |
| `CORROBORATED` | Một giá trị `DECLARED` được xác nhận bởi một dấu hiệu độc lập (ví dụ: vai trò SSH, vì giao thức đã thực sự được thương lượng). |
| `INFERRED` | Suy ra từ một mẫu/quy tắc suy đoán, không có khai báo rõ ràng từ mục tiêu. |
| `UNKNOWN` | Không có dấu hiệu dùng được, hoặc bị mục tiêu chủ động che giấu. |

## 8. Bảo vệ trước giá trị giả mạo

Omega-check không tin bất kỳ dữ liệu nào do mục tiêu tự khai báo mà không đánh dấu rõ điều đó. Một banner `Server` hay tiêu đề `X-Powered-By` vẫn là `DECLARED`, không bao giờ là `VERIFIED`, dù có vẻ hợp lý đến đâu — chính mục tiêu cung cấp chúng và có thể giả mạo tùy ý. Chỉ một xác nhận qua kênh độc lập (ví dụ giao thức SSH thực sự được thương lượng cho vai trò “truy cập shell”) mới đưa một thông tin lên `CORROBORATED`. Sự phân biệt này, nằm trong `omega-lib` (`ConfidenceLevel`), mang tính cấu trúc: không bản xuất hay màn hình nào có thể che giấu nó.

## 9. Tương thích terminal

TUI (Textual) tự động nhận diện khả năng của terminal (trình giả lập, kích thước) và điều chỉnh bảng kiểu cấu trúc tương ứng (`complete`/`standard`/`reduced`/`mono`), không cần tùy chọn thủ công. Chế độ CLI luôn là văn bản thuần, không phụ thuộc terminal. Đây là chính sách chung của toàn bộ `omega-` (`omega-lib`, `terminal/policies.py`).

### Cấu hình theo trình giả lập được nhận diện

| Trình giả lập | Cấu hình ban đầu |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH hiện đại | `reduced` |
| TTY Linux, SSH cũ | `mono` |
| Trình giả lập không nhận diện được | `reduced` (dự phòng mặc định) |

### Cấu hình theo kích thước terminal

| Kích thước tối thiểu (cột × dòng) | Mức trần cấu hình |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| nhỏ hơn | `mono` |

Cấu hình cuối cùng là **cấu hình hạn chế hơn trong hai** (trình giả lập và kích thước) — một Ghostty toàn màn hình bị thu nhỏ còn 70 cột sẽ hạ xuống `mono`, dù trình giả lập cho phép `complete`. Có thể làm mới trực tiếp bằng phím `r`.

## 10. Xuất

Báo cáo văn bản và HTML được viết bằng ngôn ngữ chọn trong Thiết lập (“Ngôn ngữ bản xuất”, mặc định là ngôn ngữ giao diện); JSON vẫn là dữ liệu, không được dịch. Báo cáo được tạo mặc định trong `var/exports/` (đường dẫn khi chạy gắn với thư mục dự án, dùng `$OMEGA_CHECK_VAR_DIR` để thay đổi), hoặc tại đường dẫn được chỉ định (`--output` trong CLI, hộp thoại trong TUI). Tên tệp rõ ràng, có dấu thời gian: `scan-{cấu-hình}-{ngày}.ext`, `scan-custom-{ngày}.ext` cho cấu hình cá nhân, `scan-{ngày}.ext` cho nhập tự do không có cấu hình.

### JSON, nguồn chuẩn

Toàn bộ cấu trúc của lần quét (`Scan` + `Host`), tuần tự hóa JSON nghiêm ngặt, kèm các mức tin cậy.

### Văn bản, báo cáo dễ đọc gọn nhẹ

Đọc được ngoài terminal, không có mã ANSI.

### HTML, báo cáo web độc lập

5 giao diện màu để chọn (`--theme` trong CLI, bộ chọn trong TUI; mặc định theo giao diện đang dùng nếu có tương đương). Bố cục riêng: khung chứa, lưới thông tin, ô thống kê theo trạng thái cổng, nhãn màu — cùng phong cách với `omega-scan`/`omega-stress`.

## 11. Lịch sử và so sánh

Mỗi lần quét đều được lưu (SQLite, `var/db/omega-check.db`): xem lịch sử theo mục tiêu, chi tiết một lần chạy trước, so sánh hai lần quét (trạng thái cổng), và chạy lại một lần quét trên cùng mục tiêu mà không cần nhập lại.

## 12. Kiểm thử

```bash
source .venv/bin/activate
lint-imports        # kiểm tra Dependency Rule
pytest -q           # 191 bài kiểm thử
ruff check src tests
mypy -p omega_check
```

Cấu trúc: `tests/unit/` (domain và ứng dụng, không có I/O thật), `tests/integration/` (SQLite/tệp thật, máy chủ HTTP giả `pytest-httpserver`, TLS qua `trustme`).

## 13. Ngoài phạm vi

- Quét CVE
- Phát hiện chủ động SQLi, XSS, RCE
- Nhận diện hệ điều hành
- Kỹ thuật quét cấp thấp kiểu nmap (quét SYN, gói tin thô)
- Thu thập trang (crawling)
- Fuzzing
- Dò mật khẩu
- Quét đồng thời nhiều mục tiêu
- Bảng điều khiển web

---

> Omega-check — Quét, nhận diện, đánh giá, báo cáo.
> Một công cụ quét cổng với độ tin cậy rõ ràng, không phải một phỏng đoán đội lốt sự thật.
