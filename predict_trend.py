import pandas as pd
import numpy as np

# 1. โหลดข้อมูลที่มีฟีเจอร์ครบถ้วนมาใช้งาน
csv_path = "data/yt_trending_data.csv"
try:
    df = pd.read_csv(csv_path)
    print("🤖 กำลังเปิดใช้งานระบบ YT Trend Predictor Engine...")
    
    if 'Views_per_Hour' not in df.columns:
        print("⚠️ ไม่พบฟีเจอร์ Views_per_Hour ในไฟล์ดิบ... ระบบกำลังทำการคำนวณสร้างให้ใหม่อัตโนมัติ")
        df['Views_per_Hour'] = round(df['Views'] / df['Hours_Since_Published'], 1)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        
    print(f"📊 โหลดคลังข้อมูลสำเร็จ! มีข้อมูลแนวโน้มทั้งหมด {len(df)} แถวสำหรับอ้างอิงสถิติ\n")
except FileNotFoundError:
    print("❌ ไม่พบไฟล์ข้อมูล กรุณารัน test_fetch.py ก่อนนะเพื่อน!")
    exit()

# 2. คำนวณขอบเขตสถิติ (Percentiles) เพื่อเอามาใช้เป็นเกณฑ์ตัดสินคะแนน
view_hour_high = df['Views_per_Hour'].quantile(0.75) 
view_hour_high = view_hour_high if view_hour_high > 0 else 1 
engagement_high = df['Likes'].quantile(0.75) / df['Views'].quantile(0.75) * 100 
engagement_high = engagement_high if engagement_high > 0 else 1


def predict_trend_score(views, likes, comments, hours, category):
    # คำนวณฟีเจอร์ Real-time
    vph = views / hours if hours > 0 else views
    engagement = ((likes + comments) / views) * 100 if views > 0 else 0
    
    # คะแนนส่วนที่ 1: ความเร็วยอดวิว (เต็ม 40)
    vph_score = min((vph / view_hour_high) * 40, 40)
    
    # คะแนนส่วนที่ 2: แรงขับเคลื่อนของผู้ชม (เต็ม 40)
    eng_score = min((engagement / engagement_high) * 40, 40)
    
    # คะแนนส่วนที่ 3: แต้มต่อหมวดหมู่ (เต็ม 20)
    cat_bonus = 0
    if category in ['Gaming', 'Music']:
        cat_bonus = 20
    elif category in ['Entertainment', 'People & Blogs']:
        cat_bonus = 15
    else:
        cat_bonus = 10
        
    # รวมคะแนนสุทธิ
    total_score = round(vph_score + eng_score + cat_bonus, 2)
    # จำกัดเรทให้อยู่ในช่วง 0 - 100%
    total_score = max(0.0, min(100.0, total_score))
    
    return total_score

# 3. รันระบบทำนายกับข้อมูล 5 อันดับแรกในตารางจริง
print("🔮 --- ระบบประมวลผลทำนายโอกาสของวิดีโอ 5 อันดับแรกในหน้าเทรนด์ปัจจุบัน ---")

# ดึง 5 แถวแรกมาวนลูปทำนายผล
for idx, row in df.head(5).iterrows():
    score = predict_trend_score(
        views=row["Views"], 
        likes=row["Likes"], 
        comments=row["Comments"], 
        hours=row["Hours_Since_Published"], 
        category=row["Category"]
    )
    
    print(f"\n🎬 วิดีโออันดับที่ {idx+1}: {row['Title']}")
    print(f"   หมวดหมู่: {row['Category']} | ยอดวิว: {row['Views']:,} วิวใน {row['Hours_Since_Published']} ชม.")
    print(f"   📊 คะแนนโอกาสรักษาระดับเทรนด์: {score}%")
    
    # แปลผลลัพธ์
    if score >= 75:
        print("   🔥 ผลทำนาย: คลิปนี้มีศักยภาพสูงมาก ดึงดูดคนดูได้แน่นหนาและรวดเร็ว!")
    elif score >= 50:
        print("   ✅ ผลทำนาย: ฟอร์มเสถียรตามมาตรฐาน เกาะหน้าเทรนด์ได้ดี")
    else:
        print("   💤 ผลทำนาย: สถิติเริ่มชะลอตัวลง มีโอกาสร่วงจากเทรนด์ในไม่ช้า")