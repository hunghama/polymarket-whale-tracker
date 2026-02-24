import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import time
import json 
from datetime import datetime

# --- ⚠️ CHÚ Ý: ĐIỀN LẠI TOKEN VÀ CHAT ID CỦA ÔNG VÀO ĐÂY ⚠️ ---
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN" # <-- XÓA CHỮ NÀY VÀ DÁN TOKEN THẬT VÀO
CHAT_ID = "YOUR_CHAT_ID"          # <-- XÓA CHỮ NÀY VÀ DÁN CHAT ID THẬT VÀO

# NÂNG CẤP API: Thêm tham số `closed=false` để ép Polymarket loại bỏ kèo "đồ cổ" ngay từ gốc
API_URL = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=100" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "whale_chart_live.png")

def get_data_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json() 
        return None
    except Exception as e:
        print(f"❌ Lỗi kết nối API: {e}")
        return None

def process_data(data):
    df = pd.DataFrame(data)
    
    # 1. Ép kiểu Volume thành số
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna(0)
    
    # 2. Bộ lọc thời gian (Bây giờ API đã sạch hơn, nhưng ta vẫn giữ để đảm bảo an toàn 100%)
    df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')
    now = pd.to_datetime(datetime.now(), utc=True)
    df_active_only = df[df['endDate'] > now]

    if df_active_only.empty:
        print("⚠️ Cảnh báo: Lọc thời gian làm rỗng danh sách, đang bỏ qua bộ lọc này...")
        df_active_only = df

    # 3. Lọc Top 5 để làm Bản tin
    top_5 = df_active_only.sort_values('volume', ascending=False).head(5)
    
    # 4. Lọc Top 10 để Vẽ biểu đồ 
    top_10_plot = df_active_only.sort_values('volume', ascending=False).head(10).sort_values('volume', ascending=True)
    
    return top_5, top_10_plot

def create_chart(df_plot):
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 8))
    
    bars = plt.barh(df_plot['question'], df_plot['volume'], color='#2ecc71')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                 f' ${width:,.0f}', va='center', fontsize=10, fontweight='bold')

    plt.xlabel('Khối lượng giao dịch (USD)', fontweight='bold')
    plt.title(f'TOP 10 KÈO SÔI ĐỘNG NHẤT POLYMARKET\nCập nhật: {datetime.now().strftime("%d/%m/%Y %H:%M")}', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(IMAGE_PATH, dpi=300)
    plt.close()

def send_telegram_report(top_5, image_path):
    message = "🚨 *POLYMARKET LIVE REPORT* 🚨\n"
    message += "━" * 25 + "\n\n"
    
    for i, row in top_5.iterrows():
        prices = row.get('outcomePrices')
        yes_price = "N/A"
        
        # Sửa lỗi Giá N/A
        if isinstance(prices, str):
            try:
                prices = json.loads(prices)
            except:
                prices = []
                
        if isinstance(prices, list) and len(prices) > 0:
            try:
                yes_price = f"${float(prices[0]):.3f}" 
            except:
                yes_price = prices[0]

        question = row['question']
        if len(question) > 60:
            question = question[:57] + "..."
            
        message += f"*{i+1}. {question}*\n"
        message += f"💰 Vol: `${row['volume']:,.0f}`  |  📈 Giá Yes: `{yes_price}`\n\n"

    message += "🐋 _Hệ thống Whale Tracker API - Day 6_"

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            payload = {'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            if response.status_code == 200:
                print("✅ Đã gửi bản tin Telegram thành công!")
            else:
                print(f"❌ Lỗi gửi tin: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống khi gửi: {e}")

def main():
    print("🚀 Khởi động Bot Live API (Phiên bản Đã Fix Lỗi)...")
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Đang lấy dữ liệu từ Polymarket...")
        raw_data = get_data_from_api()
        
        if raw_data:
            top_5, top_10_plot = process_data(raw_data)
            create_chart(top_10_plot)
            send_telegram_report(top_5, IMAGE_PATH)
        
        print("⏳ Đang chờ 60 phút cho bản tin tiếp theo...")
        time.sleep(3600)

if __name__ == "__main__":
    main()