import os
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timezone

# 1. ตั้งค่า API
API_KEY = "AIzaSyCnhhzxnPyL_O2PuJ-U0sBlgPGWt88xR5c"
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=API_KEY)

print("กำลังดึงข้อมูล YouTube Trending สเกลใหญ่ (50 คลิป)...")

# 2. ยิง API ขยับ maxResults เป็น 50
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="TH",
    maxResults=50  
)
response = request.execute()

video_list = []
# เปลี่ยนการดึงเวลาปัจจุบันให้เป็นแบบมี Timezone UTC กำกับ
current_time = datetime.now(timezone.utc) 

for item in response.get("items", []):
    # ดึงเวลาอัปโหลดคลิป และแปลงให้มี Timezone UTC ผูกไปด้วย
    pub_time_str = item["snippet"]["publishedAt"]
    pub_time = datetime.fromisoformat(pub_time_str)
    
    # คำนวณว่าปล่อยคลิปมาแล้วกี่ชั่วโมง
    hours_since_published = round((current_time - pub_time).total_seconds() / 3600, 1)
    
    video_data = {
        "Title": item["snippet"]["title"],
        "Channel": item["snippet"]["channelTitle"],
        "Category_ID": item["snippet"]["categoryId"],
        "Views": int(item["statistics"].get("viewCount", 0)),
        "Likes": int(item["statistics"].get("likeCount", 0)),
        "Comments": int(item["statistics"].get("commentCount", 0)),
        "Hours_Since_Published": hours_since_published 
    }
    video_list.append(video_data)

# 3. แปลงเป็น DataFrame และเซฟลงไฟล์ CSV
df = pd.DataFrame(video_list)

# สร้างโฟลเดอร์ data ถ้ายังไม่มี
os.makedirs("data", exist_ok=True)
csv_path = "data/yt_trending_data.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"\n✅ ดึงข้อมูลสำเร็จ! เซฟไฟล์ลงเรียบร้อยที่: {csv_path}")
print(f"จำนวนข้อมูลทั้งหมด: {len(df)} แถว")
print("\n--- ตัวอย่างข้อมูล 5 แถวแรก ---")
print(df.head().to_string())