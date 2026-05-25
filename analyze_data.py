import pandas as pd

# 1. โหลดข้อมูลจากไฟล์ CSV ที่เราเซฟไว้
csv_path = "data/yt_trending_data.csv"
try:
    df = pd.read_csv(csv_path)
    print(f"📊 โหลดข้อมูลจาก {csv_path} สำเร็จ! มีทั้งหมด {len(df)} แถว\n")
except FileNotFoundError:
    print("❌ ไม่พบไฟล์ข้อมูล กรุณารัน test_fetch.py")
    exit()

print("========== INSIGHTS จาก YOUTUBE TRENDING THAILAND ==========")

# 2. หาภาพรวมสถิติพื้นฐาน (เฉลี่ย, สูงสุด) ของยอดวิว ไลก์ คอมเมนต์
print("\n📈 สถิติภาพรวมของวิดีโอติดเทรนด์:")
stats = df[['Views', 'Likes', 'Comments', 'Hours_Since_Published']].describe().loc[['mean', 'max', 'min']]
stats.index = ['ค่าเฉลี่ย (Mean)', 'สูงสุด (Max)', 'ต่ำสุด (Min)']
print(stats.round(1).to_string())

# 3. หาว่าวิดีโอตัวไหน "พุ่งติดเทรนด์เร็วที่สุด"
print("\n⚡ Top 3 วิดีโอที่พุ่งมาติดเทรนด์เร็วที่สุด:")
fastest_videos = df.sort_values(by="Hours_Since_Published").head(3)
for idx, row in fastest_videos.iterrows():
    print(f"- [{row['Hours_Since_Published']} ชม.] {row['Title']} (ช่อง: {row['Channel']})")

# 4. คำนวณหา "Engagement Rate"
# สูตร: (Likes + Comments) / Views * 100
df['Engagement_Rate'] = ((df['Likes'] + df['Comments']) / df['Views']) * 100

print("\n🔥 Top 3 วิดีโอที่มี Engagement Rate สูงสุด (แฟนคลับเหนียวแน่น):")
top_engagement = df.sort_values(by="Engagement_Rate", ascending=False).head(3)
for idx, row in top_engagement.iterrows():
    print(f"- [{round(row['Engagement_Rate'], 2)}%] {row['Title']} (ช่อง: {row['Channel']})")

# 5. นับดูว่า Category ไหนโผล่มาในหน้าเทรนด์เยอะที่สุด
print("\n🏷️ จำนวนวิดีโอแยกตาม Category ID (หมวดหมู่ไหนกำลังฮิต):")
category_counts = df['Category_ID'].value_counts()
print(category_counts.to_string())