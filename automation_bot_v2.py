import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import time
import json 
from datetime import datetime
from dotenv import load_dotenv

# THÊM MỚI: Thư viện ghi nhật ký
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Kéo BASE_DIR lên đây để cấu hình log biết đường lưu file

# 🛠️ CẤU HÌNH HỘP ĐEN (LOGGING)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "whale_bot.log"), encoding='utf-8'), # Lưu vào file cứng
        logging.StreamHandler() # Vẫn tiếp tục in ra màn hình CMD cho ông xem
    ]
)

# 1. KHỞI TẠO VÀ ĐỌC KÉT SẮT (.env)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_LIMIT = os.getenv("API_FETCH_LIMIT", "100")

# 🧠 BÀI HỌC DAY 8: Lấy các thông số Nhịp tim và Còi báo động
HEARTBEAT = int(os.getenv("HEARTBEAT_SECONDS", "60"))
WHALE_THRESHOLD = float(os.getenv("WHALE_THRESHOLD_USD", "5000"))
SUMMARY_INTERVAL = int(os.getenv("SUMMARY_INTERVAL_SECONDS", "3600"))

if not TOKEN or not CHAT_ID:
    logging.error("❌ LỖI CHÍ MẠNG: Không tìm thấy Token trong két sắt (.env)!")
    exit()

API_URL = f"https://gamma-api.polymarket.com/markets?active=true&closed=false&limit={API_LIMIT}" 
IMAGE_PATH = os.path.join(BASE_DIR, "whale_chart_live.png")
STATE_FILE = os.path.join(BASE_DIR, "market_state.json")

# 2. HỆ THỐNG TRÍ NHỚ (STATE MANAGEMENT)
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_state(df):
    state = dict(zip(df['question'], df['volume']))
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=4)

# 3. KẾT NỐI MẠNG VÀ GỬI TIN TELEGRAM
def get_data_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200: return response.json() 
    except Exception as e:
        logging.error(f"❌ Lỗi API: {e}")
    return None

def send_telegram_alert(message):
    """Hàm mới: Gửi tin nhắn chữ khẩn cấp cực nhanh (Không cần tạo ảnh)"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try: requests.post(url, data=payload)
    except Exception as e: logging.error(f"❌ Lỗi gửi báo động: {e}")

def send_telegram_summary(message, image_path):
    """Hàm cũ: Gửi bưu kiện lớn gồm cả Ảnh biểu đồ và Chữ"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            payload = {'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}
            files = {'photo': photo}
            requests.post(url, data=payload, files=files)
            logging.info("✅ Đã gửi Báo cáo Tổng hợp thành công!")
    except Exception as e: logging.error(f"❌ Lỗi gửi báo cáo: {e}")

# 4. NHÀO NẶN DỮ LIỆU & VẼ BIỂU ĐỒ
def create_chart(df_plot):
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 8))
    bars = plt.barh(df_plot['question'], df_plot['volume'], color='#2ecc71')
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, f' ${width:,.0f}', va='center', fontsize=10, fontweight='bold')
    plt.xlabel('Khối lượng giao dịch (USD)', fontweight='bold')
    plt.title(f'TOP 10 KÈO SÔI ĐỘNG NHẤT POLYMARKET\nCập nhật: {datetime.now().strftime("%d/%m/%Y %H:%M")}', fontweight='bold')
    plt.tight_layout()
    plt.savefig(IMAGE_PATH, dpi=300)
    plt.close()

# 5. ĐỘNG CƠ CHÍNH (KIẾN TRÚC VÒNG LẶP KÉP)
def main():
    logging.info("🚀 Khởi động Bot Live API (Phiên bản DAY 8: HEARTBEAT & WHALE ALERT)...")
    
    # Ép Bot gửi báo cáo tổng hợp ngay ở lần chạy đầu tiên
    last_summary_time = time.time() - SUMMARY_INTERVAL 
    
    while True:
        logging.info("💓 Nhịp tim: Đang quét ngầm API...")
        raw_data = get_data_from_api()
        
        if raw_data:
            df = pd.DataFrame(raw_data)
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna(0)
            df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')
            now = pd.to_datetime(datetime.now(), utc=True)
            df_active = df[df['endDate'] > now]
            if df_active.empty: df_active = df

            # 🧠 Tính toán tiền bơm (Delta)
            previous_state = load_state()
            df_active['previous_volume'] = df_active['question'].map(previous_state).fillna(df_active['volume'])
            df_active['volume_change'] = df_active['volume'] - df_active['previous_volume']
            
            # Cập nhật Trí nhớ ngay lập tức cho chu kỳ 60s tiếp theo
            save_state(df_active)

            # 🚨 LUỒNG 1: QUÉT CÁ MẬP VÀ BÁO ĐỘNG KHẨN CẤP (Chạy mỗi phút)
            whales = df_active[df_active['volume_change'] >= WHALE_THRESHOLD]
            
            if not whales.empty:
                logging.info("🚨 PHÁT HIỆN CÁ MẬP! Đang réo còi báo động Telegram...")
                alert_msg = "🚨 *WHALE ALERT! PHÁT HIỆN DÒNG TIỀN ĐỘT BIẾN* 🚨\n\n"
                for _, row in whales.iterrows():
                    question = row['question']
                    if len(question) > 55: question = question[:52] + "..."
                    alert_msg += f"🔥 *{question}*\n"
                    alert_msg += f"💸 Cá mập vừa bơm: `+${row['volume_change']:,.0f}`\n"
                    alert_msg += f"💰 Tổng Vol hiện tại: `${row['volume']:,.0f}`\n\n"
                alert_msg += f"⏱️ _Phát hiện trong {HEARTBEAT}s qua_"
                send_telegram_alert(alert_msg)

            # 📊 LUỒNG 2: BÁO CÁO TỔNG HỢP (Chạy mỗi giờ / theo SUMMARY_INTERVAL)
            current_time = time.time()
            if current_time - last_summary_time >= SUMMARY_INTERVAL:
                logging.info("📊 Đã đến giờ gửi Báo cáo Tổng hợp. Đang vẽ biểu đồ...")
                
                top_10_plot = df_active.sort_values('volume', ascending=False).head(10).sort_values('volume', ascending=True)
                create_chart(top_10_plot)
                
                top_5 = df_active.sort_values('volume', ascending=False).head(5)
                summary_msg = "📊 *BÁO CÁO TỔNG HỢP ĐỊNH KỲ* 📊\n"
                summary_msg += "━" * 25 + "\n\n"
                for i, row in top_5.iterrows():
                    question = row['question']
                    if len(question) > 60: question = question[:57] + "..."
                    summary_msg += f"*{i+1}. {question}*\n"
                    summary_msg += f"💰 Vol: `${row['volume']:,.0f}`\n\n"
                summary_msg += "🐋 _Hệ thống Whale Tracker - Day 8_"
                
                send_telegram_summary(summary_msg, IMAGE_PATH)
                last_summary_time = current_time # Reset lại đồng hồ báo cáo

        logging.info(f"💤 Ngủ {HEARTBEAT} giây chờ nhịp tim tiếp theo...")
        time.sleep(HEARTBEAT)

if __name__ == "__main__":
    main()