# Hệ Thống Giám Sát Và Phát Hiện Tấn Công Mạng Dựa Trên Phân Tích Hành Vi Mạng (RF-NIDS)

Hệ thống giám sát an ninh mạng thời gian thực (NIDS) ứng dụng Machine Learning với kiến trúc **Random Jungle (2 luồng - 2 bậc)** giúp phát hiện, phân loại và cảnh báo các hành vi tấn công mạng phổ biến (Port Scan, DoS/DDoS, Brute Force) dựa trên phân tích hành vi lưu lượng mạng (Network Behavior Analysis - NBA)[cite: 8, 34, 57].

---

## Tính Năng Chính

* **Thu thập & Bóc tách Lưu lượng (Network Reader):** Lắng nghe gói tin thô qua giao diện mạng (hỗ trợ Npcap Loopback), bóc tách 17 đặc trưng định lượng ở mức kết nối (Flow-based) và thiết bị (Host-based)[cite: 29, 30, 47, 48].
* **Phân tích Hành vi Phân cấp (Random Jungle Engine):**
  * **2 Luồng (Stream):** Song song phân tích hành vi mức kết nối (Flow Stream) và mức thiết bị (Host Stream)[cite: 34, 35].
  * **2 Bậc (Stage):** Bậc 1 lọc nhị phân (Normal/Attack), Bậc 2 phân loại chi tiết dạng tấn công (TCP/UDP Scan, UDP Flood, SSH Brute Force)[cite: 35, 36].
* **Hợp nhất Quyết định (Decision Fusion):** Tự động tổng hợp kết quả dự đoán từ 4 mô hình con dựa trên độ tin cậy (Confidence Score) để tối ưu độ chính xác và giảm thiểu cảnh báo giả (False Positives)[cite: 36, 37].
* **Quản lý Cảnh báo Tập trung (AlertManager):** Định nghĩa mức độ nghiêm trọng (Low, Medium, High, Critical), lưu trữ dữ liệu bền vững bằng SQLite (chế độ WAL) và tự động đồng bộ[cite: 38].
* **API Backend & Real-time Communication:** Cung cấp đầy đủ RESTful API (FastAPI) quản lý cảnh báo và kênh WebSocket truyền dữ liệu cảnh báo tức thì[cite: 39, 40].
* **Dashboard Giám sát Trực quan (Web UI):** Giao diện Dark Mode/Glassmorphism hiển thị chỉ số uptime, biểu đồ thống kê xu hướng (Chart.js), danh sách và chi tiết cảnh báo thời gian thực[cite: 40, 41].

---

## Kiến Trúc Hệ Thống

Chương trình hoạt động theo mô hình chuỗi xử lý (Pipeline) khép kín[cite: 28, 57]:

```text
  [Network Reader]  ──>  [Decision Engine] ──> [AlertManager] ──> [FastAPI Backend] ──> [Web Dashboard]
 (Capture / Extract)      (Random Jungle)       (SQLite WAL)      (REST / WebSocket)     (Real-time UI)
```

**1. Network Reader:** Thu thập gói tin thô $\rightarrow$ Phân giải PacketParser $\rightarrow$ Cửa sổ trượt Sliding Window (Host & Flow) $\rightarrow$ Trích xuất 17 đặc trưng (Feature Vector).

**2. Decision Engine:** Tiền xử lý dữ liệu (Preprocessor) $\rightarrow$ Đưa qua 4 mô hình Random Forest $\rightarrow$ Hợp nhất quyết định bằng Decision Fusion.

**3. AlertManager:** Tiếp nhận kết quả $\rightarrow$ Gán độ nghiêm trọng $\rightarrow$ Lưu SQLite & Phát tán cảnh báo.

**4. API & Dashboard:** Truyền nhận dữ liệu thời gian thực qua WebSocket & REST API lên giao diện người dùng.

---

## Hướng Dẫn Cài Đặt

**1. Yêu cầu Môi trường**

* **Hệ điều hành:** Windows / Linux (Đã tối ưu chạy tốt trên Windows với Npcap).
* **Python:** Phiên bản `3.9` trở lên.
* **Trình điều khiển mạng:** [Npcap](https://npcap.com/) (Bắt buộc cho môi trường Windows Loopback).

**2. Cài đặt Driver Npcap (Dành cho Windows)**

1. Tải và cài đặt Npcap từ trang chủ [npcap.com](https://npcap.com/).

2. Trong quá trình cài đặt, **bắt buộc tích chọn**:

* `Support raw 802.11 traffic (monitor mode) for wireless adapters`
* `Install Npcap in WinPcap API-compatible Mode`

**3. Cài đặt Mã Nguồn & Môi Trường**

**Bước 1: Clone repository về máy local**

```bash
git clone [https://github.com/your-username/RF-NIDS.git](https://github.com/your-username/RF-NIDS.git)
cd RF-NIDS
```

**Bước 2: Tạo và kích hoạt môi trường ảo Python**

```bash
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên Linux/macOS:
source .venv/bin/activate
```

**Bước 3: Cài đặt các thư viện phụ thuộc**

```bash
pip install -r requirements.txt
```

**Bước 4: Huấn luyện mô hình (Nếu chưa có sẵn các tệp `.pkl`)**

```bash
python Train/TrainScript.py
```

*(Hoạt động này sẽ huấn luyện 4 mô hình Random Forest và xuất các file `.pkl` tương ứng)*.

---

## Hướng Dẫn Sử Dụng

**1. Khởi chạy Hệ thống Giám sát IDS Service**

Mở Terminal với **quyền Quản trị viên (Run as Administrator)** và chạy lệnh:

```bash
python app.py
```

* **Dashboard Web UI:** Truy cập địa chỉ `http://localhost:8000` (hoặc port được cấu hình) để theo dõi giao diện giám sát thời gian thực.

**2. Triển khai Giả lập Tấn công (Kiểm thử Hệ thống)**

Mở một cửa sổ Terminal song song và chạy kịch bản giả lập các luồng lưu lượng bất thường vào `127.0.0.1`:

```bash
python tancong.py
```

Menu kịch bản giả lập bao gồm:

**1. Mô phỏng hành vi Quét cổng (Port Scan / TCP Full Scan)**

**2. Mô phỏng hành vi UDP Flood**

**3. Mô phỏng hành vi SSH Brute Force**

**4. Chạy tất cả kịch bản liên tiếp (Scan $\rightarrow$ UDP $\rightarrow$ Brute)**

---

## Tác Giả

* Đỗ Mai Thu Trang
* Nguyễn Đức Việt
* Lê Tuấn Khải
