🐋 Polymarket Whale Tracker (Day 5/180)

English below | Tiếng Việt ở dưới

🇺🇸 ENGLISH VERSION

An automated Data Pipeline built with Python to track smart money ("Whales") on the Polymarket prediction market and deliver visual reports directly via Telegram.

🌟 Core Features

Data Ingestion: Automatically scans and reads the latest market report datasets.

Data Filtering: Uses Pandas to filter out markets with a trading volume exceeding $10,000,000.

Data Visualization: Generates professional Bar Charts using Matplotlib to visualize smart money flow.

Telegram Integration: Automatically pushes charts and summary text to mobile devices via the Telegram Bot API.

Background Automation: Runs 24/7 on Windows as a Background Service, executing scheduled reports every 60 minutes.

🛠️ Tech Stack

Language: Python 3.x

Libraries: pandas, matplotlib, requests, glob, logging

Environment: Miniconda

OS Execution: Windows VBScript & Batch Script for stealth background running.

🚀 Project Structure

automation_bot.py: Main Bot source code.

chay_bot.bat: Script to activate the Conda environment and trigger the Bot.

giau_cua_so.vbs: VBScript to hide the CMD window for full background execution.

bot_log.txt: System activity log file.

👨‍💻 Author

Phi Hung (Hùng $\pi^2$)

Developed as part of the: 180-Day Web3 Coding Challenge (Day 5).

🇻🇳 PHIÊN BẢN TIẾNG VIỆT

Một hệ thống tự động (Automated Data Pipeline) được xây dựng bằng Python để theo dõi dòng tiền thông minh ("Cá mập") trên thị trường dự đoán Polymarket và gửi báo cáo trực quan qua Telegram.

🌟 Tính năng cốt lõi

Data Ingestion: Tự động quét và đọc file dữ liệu báo cáo thị trường mới nhất.

Data Filtering: Sử dụng Pandas để lọc ra các kèo (markets) có khối lượng giao dịch trên 10 triệu USD.

Data Visualization: Vẽ biểu đồ Bar Chart chuyên nghiệp bằng Matplotlib để hiển thị dòng tiền.

Telegram Integration: Tự động gửi biểu đồ và tóm tắt báo cáo trực tiếp về điện thoại qua Telegram Bot API.

Background Automation: Chạy ngầm 24/7 trên Windows như một Background Service, tự động báo cáo mỗi 60 phút.

🛠️ Công nghệ sử dụng

Ngôn ngữ: Python 3.x

Thư viện: pandas, matplotlib, requests, glob, logging

Môi trường: Miniconda

Hệ điều hành: Khởi chạy ngầm qua Windows VBScript & Batch Script.

🚀 Cấu trúc dự án

automation_bot.py: Mã nguồn chính của Bot.

chay_bot.bat: Script khởi động môi trường Conda và gọi Bot.

giau_cua_so.vbs: Script ẩn cửa sổ CMD để Bot chạy ngầm hoàn toàn.

bot_log.txt: File ghi lại nhật ký hoạt động của hệ thống.

👨‍💻 Tác giả

Phi Hùng (Hùng $\pi^2$)

Được phát triển trong khuôn khổ: Thử thách 180 Ngày Lập Trình Web3 (Day 5).
