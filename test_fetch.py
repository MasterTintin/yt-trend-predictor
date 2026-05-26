import os
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timezone

# 1. ตั้งค่า API และดิกชันนารีแปลงชื่อหมวดหมู่
API_KEY = "AIzaSyCnhhzxnPyL_O2PuJ-U0sBlgPGWt88xR5c"
api_service_name = "youtube"
api_version = "v3"

# ดิกชันนารีอ้างอิงตรงตาม YouTube API สเปซไทย
CATEGORY_MAP = {
    "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music", 
    "15": "Pets & Animals", "17": "Sports", "19": "Travel & Events", 
    "20": "Gaming", "22": "People & Blogs", "23": "Comedy", 
    "24": "Entertainment", "25": "News & Politics", "26": "Howto & Style", 
    "27": "Education", "28": "Science & Technology"
}

youtube = build(api_service_name, api_version, developerKey=API_KEY)

print("กำลังดึงข้อมูล YouTube Trending สเกลใหญ่ (50 คลิป)...")

# 2. ยิง API ขอข้อมูล
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="TH",
    maxResults=50  
)
response = request.execute()

video_list = []
current_time = datetime.now(timezone.utc) 

for item in response.get("items", []):
    pub_time_str = item["snippet"]["publishedAt"]
    pub_time = datetime.fromisoformat(pub_time_str)
    
    hours_since_published = round((current_time - pub_time).total_seconds() / 3600, 1)
    
    # ดึงเลข ID ออกมาก่อน แล้วเอาไปเทียบในดิกชันนารี ถ้าไม่เจอให้โชว์ตัวเลขเดิม (Unknown)
    cat_id = item["snippet"]["categoryId"]
    category_name = CATEGORY_MAP.get(cat_id, f"Unknown ({cat_id})")
    
    video_data = {
        "Title": item["snippet"]["title"],
        "Channel": item["snippet"]["channelTitle"],
        "Category": category_name,  # สวมชื่อจริงเข้าไปแทนเลข ID แล้วเพื่อน!
        "Views": int(item["statistics"].get("viewCount", 0)),
        "Likes": int(item["statistics"].get("likeCount", 0)),
        "Comments": int(item["statistics"].get("commentCount", 0)),
        "Hours_Since_Published": hours_since_published 
    }
    video_list.append(video_data)

# 3. แปลงเป็น DataFrame และเซฟลงไฟล์ CSV
df = pd.DataFrame(video_list)

os.makedirs("data", exist_ok=True)
csv_path = "data/yt_trending_data.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"\n✅ ดึงข้อมูลสำเร็จและจัดหมวดหมู่คลีนๆ เรียบร้อยที่: {csv_path}")
print("\n--- ตัวอย่างข้อมูล 5 แถวแรก (เวอร์ชันมนุษย์อ่านออก) ---")
print(df.head()[['Title', 'Category', 'Views', 'Hours_Since_Published']].to_string())