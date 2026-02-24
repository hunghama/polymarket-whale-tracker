🐋 Polymarket Whale Tracker (Day 6/180)

🔗 GitHub Repository: https://github.com/hunghama/polymarket-whale-tracker

English below | Tiếng Việt ở dưới

🇺🇸 ENGLISH VERSION

An automated Real-Time Data Pipeline built with Python to track smart money ("Whales") on the Polymarket prediction market. The bot fetches live blockchain data via API, processes nested JSONs, and delivers visual financial newsletters directly via Telegram.

🌟 Core Features (Day 6 Upgrades)

Live API Ingestion: Upgraded from static CSVs to fetching real-time data directly from Polymarket's Gamma API.

Deep JSON Parsing: Extracts nested betting odds (outcomePrices) to provide live "Yes/No" token prices.

Data Cleaning & Error Handling: Automatically coerces messy strings into numeric types and handles missing data gracefully (Zero N/As).

Smart Time-Filter: Built-in logic to automatically filter out expired/historical markets (e.g., 2020/2021 events), ensuring only active future markets are reported.

Data Visualization: Generates professional Bar Charts using Matplotlib to visualize the top 10 highest-volume markets.

Automated Newsletter: Pushes formatted Markdown reports (including emojis and bold texts) paired with the generated chart to Telegram 24/7.

🛠️ Tech Stack

Language: Python 3.x

Libraries: requests, pandas, matplotlib, json, datetime

Architecture: ETL (Extract, Transform, Load) Pipeline.

👨‍💻 Author

Phi Hung (Hùng $\pi^2$)

Developed as part of the: 180-Day Web3 Coding Challenge (Day 6).

🇻🇳 PHIÊN BẢN TIẾNG VIỆT

Một hệ thống Data Pipeline thời gian thực được xây dựng bằng Python để theo dõi dòng tiền thông minh ("Cá mập") trên Polymarket. Bot tự động lấy dữ liệu trực tiếp qua API, xử lý JSON lồng nhau và gửi bản tin tài chính trực quan qua Telegram.

🌟 Tính năng cốt lõi (Bản nâng cấp Day 6)

Live API Ingestion: Nâng cấp từ đọc file CSV tĩnh sang gọi API lấy dữ liệu thời gian thực từ Polymarket.

Deep JSON Parsing: Bóc tách dữ liệu JSON lồng nhau để lấy ra giá cược Live (Outcome Prices) một cách chính xác.

Data Cleaning: Tự động làm sạch dữ liệu rác, ép kiểu dữ liệu an toàn để hệ thống không bị crash khi API trả về lỗi.

Smart Time-Filter: Thuật toán lọc thời gian thông minh giúp tự động loại bỏ các kèo "đồ cổ" (đã hết hạn từ 2020/2021), chỉ giữ lại các sự kiện ở tương lai.

Data Visualization: Vẽ biểu đồ Bar Chart chuyên nghiệp bằng Matplotlib hiển thị Top 10 kèo giao dịch lớn nhất.

Automated Newsletter: Gửi bản tin định dạng Markdown (kèm ảnh biểu đồ) tự động về Telegram 24/7.

🛠️ Công nghệ sử dụng

Ngôn ngữ: Python 3.x

Thư viện: requests, pandas, matplotlib, json, datetime

Kiến trúc: Quy trình ETL (Trích xuất, Biến đổi, Tải lên).

👨‍💻 Tác giả

Phi Hùng (Hùng $\pi^2$)

Được phát triển trong khuôn khổ: Thử thách 180 Ngày Lập Trình Web3 (Day 6).
